import pygame
import random
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim

pygame.init()

# ---------------- SCREEN ----------------
WIDTH, HEIGHT = 500, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("VBots DQN Simulation")

clock = pygame.time.Clock()

# ---------------- COLORS ----------------
GRASS = (70, 170, 90)
ROAD = (50, 50, 50)
LANES = (220, 220, 220)

SHOP = (200, 200, 210)
GOAL_COLOR = (0, 255, 180)
ROBOT_COLOR = (180, 180, 200)
CAR_COLOR = (220, 60, 60)
SENSOR = (0, 255, 255)

# ---------------- ENV ----------------
ROAD_X = 200
ROAD_W = 100

shop = (60, 420)
goal = (430, 60)

cars = [
    pygame.Rect(210, 0, 40, 20),
    pygame.Rect(270, 250, 40, 20),
]

# ---------------- DQN ----------------
class DQN(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(4, 64),
            nn.ReLU(),
            nn.Linear(64, 64),
            nn.ReLU(),
            nn.Linear(64, 4)
        )

    def forward(self, x):
        return self.net(x)

model = DQN()
optimizer = optim.Adam(model.parameters(), lr=0.001)
loss_fn = nn.MSELoss()

# ---------------- ROBOT ----------------
x, y = 60.0, 60.0
has_item = False

def robot_rect():
    return pygame.Rect(int(x), int(y), 20, 20)

# ---------------- STATE ----------------
def get_state():
    return np.array([
        x / WIDTH,
        y / HEIGHT,
        (shop[0] - x) / WIDTH,
        (goal[0] - x) / WIDTH
    ], dtype=np.float32)

# ---------------- ACTION ----------------
def act(state):
    if random.random() < 0.2:
        return random.randint(0, 3)

    with torch.no_grad():
        q = model(torch.tensor(state))
        return torch.argmax(q).item()

# ---------------- MOVE ----------------
def move(action):
    global x, y
    if action == 0: y -= 5
    if action == 1: y += 5
    if action == 2: x -= 5
    if action == 3: x += 5

# ---------------- TRAIN ----------------
def train(s, a, r, ns):
    s = torch.tensor(s)
    ns = torch.tensor(ns)

    q = model(s)
    q_next = model(ns)

    target = q.clone().detach()
    target[a] = r + 0.95 * torch.max(q_next)

    loss = loss_fn(q, target)

    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

# ---------------- REWARD ----------------
def reward(crash, picked, done):
    if crash:
        return -50
    if picked:
        return 10
    if done:
        return 20
    return -0.1

# ---------------- COLLISION ----------------
def crash_check():
    rr = robot_rect()
    for c in cars:
        if rr.colliderect(c):
            return True
    return False

# ---------------- DRAW ----------------
def draw():
    screen.fill(GRASS)

    # road
    pygame.draw.rect(screen, ROAD, (ROAD_X, 0, ROAD_W, HEIGHT))
    for i in range(0, HEIGHT, 25):
        pygame.draw.rect(screen, LANES, (ROAD_X + 48, i, 4, 10))

    # shop
    pygame.draw.rect(screen, SHOP, (shop[0], shop[1], 60, 40))

    # goal
    pygame.draw.circle(screen, GOAL_COLOR, goal, 15)

    # cars
    for c in cars:
        pygame.draw.rect(screen, CAR_COLOR, c)

    # robot
    rr = robot_rect()
    pygame.draw.rect(screen, ROBOT_COLOR, rr, border_radius=4)

    # sensors (small)
    sx, sy = int(x + 10), int(y + 10)
    for angle in [-20, 0, 20]:
        ex = sx + angle
        ey = sy - 25
        pygame.draw.line(screen, SENSOR, (sx, sy), (ex, ey), 1)
        pygame.draw.circle(screen, SENSOR, (ex, ey), 2)

# ---------------- MAIN TRAIN LOOP ----------------
for episode in range(300):

    x, y = 60, 60
    has_item = False

    for step in range(200):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        state = get_state()
        action = act(state)

        move(action)

        crash = crash_check()

        # pickup
        if abs(x - shop[0]) < 25 and abs(y - shop[1]) < 25:
            has_item = True

        # goal
        done = has_item and abs(x - goal[0]) < 25 and abs(y - goal[1]) < 25

        next_state = get_state()
        r = reward(crash, has_item and not done, done)

        train(state, action, r, next_state)

        if crash:
            x, y = 60, 60

        draw()
        pygame.display.update()
        clock.tick(30)

        if done:
            break

pygame.quit()