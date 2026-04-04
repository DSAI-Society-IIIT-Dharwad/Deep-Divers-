import gymnasium as gym
from gymnasium import spaces
import numpy as np
import math


class RobotEnv(gym.Env):
    metadata = {"render_modes": ["human"]}

    def __init__(self, goal=None, obstacles=None, world_size=6.0, max_steps=250):
        super().__init__()

        self.action_space = spaces.Discrete(3)

        self.observation_space = spaces.Box(
            low=-100,
            high=100,
            shape=(14,),
            dtype=np.float32
        )

        self.world_size = float(world_size)
        self.max_steps = int(max_steps)

        self.goal = np.array(goal if goal is not None else [5.0, 5.0], dtype=np.float32)

        default_obstacles = [
            [2.5, 2.5],
            [3.5, 3.0],
        ]
        obstacle_points = obstacles if obstacles is not None else default_obstacles
        self.obstacles = [np.array(p, dtype=np.float32) for p in obstacle_points]

        self.phase = 1

        self.reset()

    def set_phase(self, phase):
        self.phase = phase

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)

        self.position = np.array([0.5, 0.5], dtype=np.float32)
        self.theta = 0.0
        self.velocity = 0.0
        self.time_step = 0

        return self._get_obs(), {}

    def _get_obs(self):
        dist_to_goal = np.linalg.norm(self.goal - self.position)

        sensors = [np.linalg.norm(obs - self.position) for obs in self.obstacles]

        while len(sensors) < 4:
            sensors.append(10.0)

        collision_flag = 1.0 if self._check_collision() else 0.0

        return np.array([
            self.position[0], self.position[1], self.theta,
            self.goal[0], self.goal[1],
            dist_to_goal,
            sensors[0], sensors[1], sensors[2], sensors[3],
            self.velocity,
            collision_flag,
            self.time_step,
            float(self.phase)
        ], dtype=np.float32)

    def _check_collision(self):
        for obs in self.obstacles:
            if np.linalg.norm(self.position - obs) < 1.0:
                return True
        return False

    def step(self, action):
        self.time_step += 1

        self.velocity = 0.15

        if action == 1:
            self.theta += 0.2
        elif action == 2:
            self.theta -= 0.2

        prev_dist = np.linalg.norm(self.goal - self.position)

        new_x = self.position[0] + self.velocity * math.cos(self.theta)
        new_y = self.position[1] + self.velocity * math.sin(self.theta)

        new_x = np.clip(new_x, 0, self.world_size)
        new_y = np.clip(new_y, 0, self.world_size)

        self.position = np.array([new_x, new_y], dtype=np.float32)

        new_dist = np.linalg.norm(self.goal - self.position)

        reward = 0.0
        done = False

        if self.phase == 1:
            reward += (prev_dist - new_dist) * 5
            if self._check_collision():
                reward -= 50
                done = True
        else:
            reward += (prev_dist - new_dist) * 20

            for obs in self.obstacles:
                dist = np.linalg.norm(self.position - obs)
                if dist < 1.5:
                    reward -= (1.5 - dist) * 5

            if self._check_collision():
                reward -= 60
                done = True

            if new_dist < 0.8:
                reward += 250
                done = True

        reward -= 0.01

        if self.time_step >= self.max_steps:
            done = True

        return self._get_obs(), reward, done, False, {}

    def render(self):
        print(f"Phase: {self.phase} | Pos: {self.position} | Goal: {self.goal}")