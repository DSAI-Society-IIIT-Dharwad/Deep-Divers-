import pygame
import sys
import random
import math

pygame.init()

# ---------------- SCREEN ----------------
WIDTH, HEIGHT = 400, 400
CELL = 40
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("VBots DRL Phase Learning (Realistic Sim)")

clock = pygame.time.Clock()

# ---------------- COLORS ----------------
ROAD = (55, 55, 55)
GRASS = (35, 140, 60)
WHITE = (255, 255, 255)
YELLOW = (240, 230, 70)
RED = (220, 60, 60)
BLUE = (40, 140, 255)
BROWN = (120, 80, 40)
BLACK = (0, 0, 0)

# ---------------- OBJECTS ----------------
x, y = 0, 0
start = (0, 0)
goal = (360, 360)

trees = [(120, 120), (160, 160), (240, 120)]

cars = [
    {"x": 200, "y": 50, "speed": 4},
    {"x": 280, "y": 200, "speed": 3}
]

actions = ["UP", "DOWN", "LEFT", "RIGHT"]

Q = {}
alpha = 0.7
gamma = 0.9

phase = 1
epsilon = 0.4

collision_count = 0
path = []

# ---------------- HELPERS ----------------

def state(x, y):
    return (x // CELL, y // CELL)

def init(s):
    if s not in Q:
        Q[s] = {a: 0 for a in actions}

def danger(nx, ny):
    for c in cars:
        if abs(nx - c["x"]) < CELL and abs(ny - c["y"]) < CELL:
            return True
    for t in trees:
        if abs(nx - t[0]) < CELL and abs(ny - t[1]) < CELL:
            return True
    return False

def dist(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)

# ---------------- REWARD ----------------

def reward(nx, ny, px, py):
    if (nx, ny) == goal:
        return 250

    if danger(nx, ny):
        return -150

    old_d = dist(px, py, goal[0], goal[1])
    new_d = dist(nx, ny, goal[0], goal[1])

    return (old_d - new_d) * 8

# ---------------- ACTION ----------------

def choose(s, x, y):
    global epsilon

    if phase == 1:
        epsilon = 0.4
    else:
        epsilon = 0.03

    if random.random() < epsilon:
        if phase == 2:
            if abs(goal[0] - x) > abs(goal[1] - y):
                return "RIGHT" if goal[0] > x else "LEFT"
            else:
                return "DOWN" if goal[1] > y else "UP"

        return random.choice(actions)

    return max(Q[s], key=Q[s].get)

# ---------------- MOVE ----------------

def move(x, y, a):
    if a == "UP": y -= CELL
    if a == "DOWN": y += CELL
    if a == "LEFT": x -= CELL
    if a == "RIGHT": x += CELL

    x = max(0, min(WIDTH - CELL, x))
    y = max(0, min(HEIGHT - CELL, y))
    return x, y

def reset():
    global x, y
    x, y = start

def move_cars():
    for c in cars:
        c["y"] += c["speed"]
        if c["y"] > HEIGHT:
            c["y"] = -CELL
            c["x"] = random.choice([160, 200, 240, 280])

# ---------------- DRAW HELPERS ----------------

def draw_road():
    screen.fill(GRASS)

    # road
    pygame.draw.rect(screen, ROAD, (160, 0, 80, HEIGHT))

    # lane markings
    for i in range(0, HEIGHT, 30):
        pygame.draw.rect(screen, YELLOW, (198, i, 4, 15))

def draw_tree(tx, ty):
    pygame.draw.rect(screen, BROWN, (tx+15, ty+20, 10, 20))
    pygame.draw.circle(screen, (20, 120, 40), (tx+20, ty+15), 15)
    pygame.draw.circle(screen, (30, 160, 60), (tx+20, ty+5), 12)

def draw_car(c):
    # body
    pygame.draw.rect(screen, RED, (c["x"], c["y"], CELL, CELL))
    # windows
    pygame.draw.rect(screen, (200, 200, 255), (c["x"]+5, c["y"]+5, 10, 10))
    pygame.draw.rect(screen, (200, 200, 255), (c["x"]+25, c["y"]+5, 10, 10))
    # wheels
    pygame.draw.circle(screen, BLACK, (c["x"]+8, c["y"]+35), 4)
    pygame.draw.circle(screen, BLACK, (c["x"]+32, c["y"]+35), 4)

def draw_robot(x, y):
    # shadow
    pygame.draw.circle(screen, (0, 0, 0, 50), (x+20, y+20), 18)

    # body
    pygame.draw.rect(screen, BLUE, (x, y, CELL, CELL), border_radius=8)

    # head sensor
    pygame.draw.circle(screen, WHITE, (x+20, y+10), 5)

def draw_goal():
    pygame.draw.circle(screen, (0, 255, 120), goal, 18)
    pygame.draw.circle(screen, (255, 255, 255), goal, 10, 2)

# ---------------- MAIN LOOP ----------------

running = True

while running:
    clock.tick(20)
    move_cars()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    s = state(x, y)
    init(s)

    a = choose(s, x, y)

    px, py = x, y
    nx, ny = move(x, y, a)

    r = reward(nx, ny, px, py)

    ns = state(nx, ny)
    init(ns)

    Q[s][a] += alpha * (r + gamma * max(Q[ns].values()) - Q[s][a])

    if danger(nx, ny):
        collision_count += 1
        reset()
        phase = 2
        continue

    x, y = nx, ny

    if phase == 2:
        path.append((x, y))

    if (x, y) == goal:
        print("🎯 GOAL REACHED")
        running = False

    # ---------------- DRAW ----------------
    draw_road()

    for t in trees:
        draw_tree(*t)

    for c in cars:
        draw_car(c)

    draw_goal()
    draw_robot(x, y)

    # path trail
    for px, py in path:
        pygame.draw.circle(screen, (0, 255, 255), (px+20, py+20), 2)

    font = pygame.font.SysFont(None, 24)
    screen.blit(font.render(f"Phase: {phase}", True, WHITE), (10, 10))
    screen.blit(font.render(f"Collisions: {collision_count}", True, WHITE), (10, 30))

    pygame.display.update()

pygame.quit()