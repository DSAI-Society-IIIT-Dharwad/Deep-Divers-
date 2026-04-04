from src.env.robot_env import RobotEnv
from src.env.ros2_gazebo_env import Ros2GazeboEnv


def create_env(config):
    env_name = config.get("environment", {}).get("name", "mock")
    env_config = config.get("environment", {}).get("params", {})

    if env_name == "mock":
        return RobotEnv(**env_config)

    if env_name == "ros2_gazebo":
        return Ros2GazeboEnv(**env_config)

    raise ValueError(f"Unsupported environment '{env_name}'")
