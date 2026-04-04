import math
import time

import gymnasium as gym
from gymnasium import spaces
import numpy as np


class Ros2GazeboEnv(gym.Env):
    metadata = {"render_modes": ["human"]}

    def __init__(
        self,
        goal=None,
        laser_sample_count=4,
        command_duration=0.2,
        max_steps=250,
        namespace="",
        cmd_vel_topic="/cmd_vel",
        scan_topic="/scan",
        odom_topic="/odom",
        reset_service="/reset_simulation",
    ):
        super().__init__()

        self.goal = np.array(goal if goal is not None else [5.0, 5.0], dtype=np.float32)
        self.laser_sample_count = int(laser_sample_count)
        self.command_duration = float(command_duration)
        self.max_steps = int(max_steps)
        self.namespace = namespace.strip("/")
        self.cmd_vel_topic = self._namespaced(cmd_vel_topic)
        self.scan_topic = self._namespaced(scan_topic)
        self.odom_topic = self._namespaced(odom_topic)
        self.reset_service = self._namespaced(reset_service)

        self.action_space = spaces.Discrete(3)
        self.observation_space = spaces.Box(
            low=-100.0,
            high=100.0,
            shape=(14,),
            dtype=np.float32,
        )

        self._step_count = 0
        self._latest_position = np.array([0.0, 0.0], dtype=np.float32)
        self._latest_theta = 0.0
        self._latest_speed = 0.0
        self._latest_scan = np.full(self.laser_sample_count, 10.0, dtype=np.float32)
        self._collision = False

        self._setup_ros_interfaces()

    def _namespaced(self, topic_name):
        topic_name = topic_name if topic_name.startswith("/") else f"/{topic_name}"
        if not self.namespace:
            return topic_name
        return f"/{self.namespace}{topic_name}"

    def _setup_ros_interfaces(self):
        try:
            import rclpy
            from geometry_msgs.msg import Twist
            from nav_msgs.msg import Odometry
            from sensor_msgs.msg import LaserScan
            from std_srvs.srv import Empty
        except ImportError as exc:
            raise ImportError(
                "ROS 2 Python packages are required for the 'ros2_gazebo' environment. "
                "Install ROS 2 Humble or newer and source the environment before training."
            ) from exc

        self._rclpy = rclpy
        self._Twist = Twist
        self._Empty = Empty

        if not self._rclpy.ok():
            self._rclpy.init(args=None)

        self._node = self._rclpy.create_node("drl_nav_gym_bridge")
        self._cmd_pub = self._node.create_publisher(Twist, self.cmd_vel_topic, 10)
        self._node.create_subscription(Odometry, self.odom_topic, self._odom_callback, 10)
        self._node.create_subscription(LaserScan, self.scan_topic, self._scan_callback, 10)
        self._reset_client = self._node.create_client(Empty, self.reset_service)

    def _odom_callback(self, msg):
        self._latest_position = np.array(
            [msg.pose.pose.position.x, msg.pose.pose.position.y],
            dtype=np.float32,
        )
        orientation = msg.pose.pose.orientation
        siny_cosp = 2.0 * (orientation.w * orientation.z + orientation.x * orientation.y)
        cosy_cosp = 1.0 - 2.0 * (orientation.y * orientation.y + orientation.z * orientation.z)
        self._latest_theta = math.atan2(siny_cosp, cosy_cosp)
        linear = msg.twist.twist.linear
        self._latest_speed = math.sqrt(linear.x ** 2 + linear.y ** 2)

    def _scan_callback(self, msg):
        ranges = np.array(msg.ranges, dtype=np.float32)
        finite_ranges = np.where(np.isfinite(ranges), ranges, 10.0)

        if len(finite_ranges) == 0:
            self._latest_scan = np.full(self.laser_sample_count, 10.0, dtype=np.float32)
        else:
            indices = np.linspace(0, len(finite_ranges) - 1, self.laser_sample_count, dtype=int)
            self._latest_scan = finite_ranges[indices]

        self._collision = bool(np.min(self._latest_scan) < 0.25)

    def _spin_once(self, timeout=0.1):
        self._rclpy.spin_once(self._node, timeout_sec=timeout)

    def _build_observation(self):
        dist_to_goal = np.linalg.norm(self.goal - self._latest_position)
        sensors = list(self._latest_scan[:4])
        while len(sensors) < 4:
            sensors.append(10.0)

        return np.array(
            [
                self._latest_position[0],
                self._latest_position[1],
                self._latest_theta,
                self.goal[0],
                self.goal[1],
                dist_to_goal,
                sensors[0],
                sensors[1],
                sensors[2],
                sensors[3],
                self._latest_speed,
                1.0 if self._collision else 0.0,
                float(self._step_count),
                0.0,
            ],
            dtype=np.float32,
        )

    def _publish_action(self, action):
        twist = self._Twist()
        twist.linear.x = 0.15
        if action == 1:
            twist.angular.z = 0.6
        elif action == 2:
            twist.angular.z = -0.6
        self._cmd_pub.publish(twist)

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self._step_count = 0

        if self._reset_client.wait_for_service(timeout_sec=2.0):
            future = self._reset_client.call_async(self._Empty.Request())
            self._rclpy.spin_until_future_complete(self._node, future, timeout_sec=3.0)

        for _ in range(5):
            self._spin_once()

        return self._build_observation(), {}

    def step(self, action):
        self._step_count += 1
        self._publish_action(action)

        deadline = time.time() + self.command_duration
        while time.time() < deadline:
            self._spin_once(timeout=min(0.05, self.command_duration))

        obs = self._build_observation()
        dist_to_goal = np.linalg.norm(self.goal - self._latest_position)

        reward = -0.05
        terminated = False

        if dist_to_goal < 0.8:
            reward += 120.0
            terminated = True

        if self._collision:
            reward -= 40.0
            terminated = True

        truncated = self._step_count >= self.max_steps
        return obs, reward, terminated, truncated, {}

    def render(self):
        print(
            f"Robot: {self._latest_position} Goal: {self.goal} "
            f"Collision: {self._collision}"
        )

    def close(self):
        if hasattr(self, "_node"):
            self._node.destroy_node()
        if hasattr(self, "_rclpy") and self._rclpy.ok():
            self._rclpy.shutdown()
