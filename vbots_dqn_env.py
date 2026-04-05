import pygame
import math
import random
import numpy as np

WIDTH, HEIGHT = 500, 500

STORE = (60, 380)
GOAL = (430, 60)

class VBotsEnv:
    def __init__(self):
        self.reset()

    def reset(self):
        self.x, self.y = 60, 60
        self.has_item = False
        self.done = False
        self.steps = 0
        return self.get_state()

    def get_state(self):
        return np.array([
            self.x / WIDTH,
            self.y / HEIGHT,
            self.has_item * 1.0,
            STORE[0] / WIDTH,
            STORE[1] / HEIGHT,
            GOAL[0] / WIDTH,
            GOAL[1] / HEIGHT
        ], dtype=np.float32)

    def step(self, action):
        # actions: 0 up, 1 down, 2 left, 3 right

        if action == 0:
            self.y -= 5
        elif action == 1:
            self.y += 5
        elif action == 2:
            self.x -= 5
        elif action == 3:
            self.x += 5

        self.x = max(0, min(WIDTH, self.x))
        self.y = max(0, min(HEIGHT, self.y))

        reward = -0.1
        self.steps += 1

        # pickup
        if not self.has_item and self.distance(STORE) < 25:
            self.has_item = True
            reward = 10

        # delivery
        if self.has_item and self.distance(GOAL) < 25:
            reward = 20
            self.done = True

        # crash penalty (optional simple boundary)
        if self.steps > 500:
            self.done = True

        return self.get_state(), reward, self.done

    def distance(self, point):
        return math.hypot(self.x - point[0], self.y - point[1])