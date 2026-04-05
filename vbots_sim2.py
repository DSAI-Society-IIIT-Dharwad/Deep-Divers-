import pygame
import sys
import math
import random

pygame.init()

# ---------------- SCREEN ----------------
WIDTH, HEIGHT = 500, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("VBots - Complete Delivery Simulation")

clock = pygame.time.Clock()

# ---------------- COLORS ----------------
GRASS = (70, 170, 90)
ROAD = (45, 45, 45)
LANE = (230, 230, 230)

ROBOT = (200, 200, 210)
SENSOR = (0, 255, 255)

STORE_WALL = (210, 210, 215)
STORE_ROOF = (170, 170, 180)
GLASS = (160, 220, 255)

GOAL_COLOR = (0, 255, 180)

CAR1 = (220, 60, 60)
CAR2 = (60, 120, 255)

BLACK = (0, 0, 0)

# ---------------- ROAD ----------------
ROAD_X = 200
ROAD_W = 100

# ---------------- STORE ----------------
store_x, store_y = 40, 380
STORE_W, STORE_H = 120, 90

# ---------------- ITEMS ----------------
ITEMS = [
    {"name": "Bottle", "color": (80, 180, 255), "shape": "rect"},
    {"name": "Apple", "color": (255, 80, 80), "shape": "circle"},
    {"name": "Box", "color": (200, 140, 80), "shape": "square"}
]

current_item = random.choice(ITEMS)

# ---------------- ROBOT ----------------
x, y = 60.0, 60.0
speed = 2.6
ROBOT_SIZE = 22

has_item = False

# ---------------- DELIVERY ----------------
items_collected = 0
total_items = len(ITEMS)

goal = (430, 60)

# ---------------- CARS ----------------
cars = [
    {"x": ROAD_X + 10, "y": 80, "v": 2.0, "color": CAR1},
    {"x": ROAD_X + 55, "y": 250, "v": -2.2, "color": CAR2}
]

# ---------------- HELPERS ----------------
def robot_rect():
    return pygame.Rect(int(x), int(y), ROBOT_SIZE, ROBOT_SIZE)

def store_rect():
    return pygame.Rect(store_x, store_y, STORE_W, STORE_H)

def goal_rect():
    return pygame.Rect(goal[0]-15, goal[1]-15, 30, 30)

# ---------------- MOVE ROBOT ----------------
def move_robot(target):
    global x, y

    dx = target[0] - x
    dy = target[1] - y

    dist = math.hypot(dx, dy)
    if dist > 0:
        dx /= dist
        dy /= dist

    x += dx * speed
    y += dy * speed

# ---------------- CARS ----------------
def move_cars():
    for c in cars:
        c["y"] += c["v"]
        if c["y"] > HEIGHT:
            c["y"] = -30
        if c["y"] < -30:
            c["y"] = HEIGHT

def car_collision():
    rr = robot_rect()
    for c in cars:
        car_rect = pygame.Rect(c["x"], c["y"], 35, 18)
        if rr.colliderect(car_rect):
            return True
    return False

# ---------------- SMALL SENSORS ----------------
def draw_sensors():
    sx = x + ROBOT_SIZE // 2
    sy = y + ROBOT_SIZE // 2

    for angle in [-25, 0, 25]:
        rad = math.radians(angle)
        ex = sx + math.cos(rad) * 15
        ey = sy + math.sin(rad) * 15

        pygame.draw.line(screen, SENSOR, (sx, sy), (ex, ey), 1)
        pygame.draw.circle(screen, SENSOR, (int(ex), int(ey)), 2)

# ---------------- STORE ----------------
def draw_store():
    rect = store_rect()

    pygame.draw.rect(screen, STORE_WALL, rect, border_radius=8)

    pygame.draw.polygon(screen, STORE_ROOF, [
        (rect.x, rect.y),
        (rect.x + rect.w // 2, rect.y - 20),
        (rect.x + rect.w, rect.y)
    ])

    pygame.draw.rect(screen, GLASS, (rect.x + 10, rect.y + 20, rect.w - 20, 30))

# ---------------- ITEMS ----------------
def draw_items():
    rect = store_rect()

    for i, item in enumerate(ITEMS):
        cx = rect.x + 20 + i * 30
        cy = rect.y + 50

        if item["shape"] == "rect":
            pygame.draw.rect(screen, item["color"], (cx, cy, 10, 10))
        elif item["shape"] == "circle":
            pygame.draw.circle(screen, item["color"], (cx + 5, cy + 5), 5)
        else:
            pygame.draw.rect(screen, item["color"], (cx, cy, 12, 12))

# ---------------- CURRENT ITEM ----------------
def draw_current_item():
    if has_item:
        return

    rect = store_rect()
    item = current_item

    cx = rect.x + 55
    cy = rect.y + 45

    if item["shape"] == "rect":
        pygame.draw.rect(screen, item["color"], (cx, cy, 8, 8))
    elif item["shape"] == "circle":
        pygame.draw.circle(screen, item["color"], (cx, cy), 5)
    else:
        pygame.draw.rect(screen, item["color"], (cx, cy, 10, 10))

# ---------------- ROBOT ----------------
def draw_robot():
    rr = robot_rect()

    pygame.draw.rect(screen, ROBOT, rr, border_radius=5)

    pygame.draw.circle(screen, (255, 255, 255), (rr.x + 6, rr.y + 6), 2)
    pygame.draw.circle(screen, (255, 255, 255), (rr.x + 15, rr.y + 6), 2)

    pygame.draw.circle(screen, BLACK, (rr.x + 5, rr.y + 22), 3)
    pygame.draw.circle(screen, BLACK, (rr.x + 17, rr.y + 22), 3)

    if has_item:
        pygame.draw.circle(screen, (255, 215, 0), (rr.x + 11, rr.y - 5), 4)

    draw_sensors()

# ---------------- WORLD ----------------
def draw_world():
    screen.fill(GRASS)

    pygame.draw.rect(screen, ROAD, (ROAD_X, 0, ROAD_W, HEIGHT))

    for i in range(0, HEIGHT, 25):
        pygame.draw.rect(screen, LANE, (ROAD_X + 48, i, 4, 10))

def draw_cars():
    for c in cars:
        pygame.draw.rect(screen, c["color"], (c["x"], c["y"], 35, 18))

def draw_goal():
    pygame.draw.circle(screen, GOAL_COLOR, goal, 16)
    pygame.draw.circle(screen, (255, 255, 255), goal, 6)

# ---------------- MAIN LOOP ----------------
running = True

while running:
    clock.tick(60)

    move_cars()

    # ---------------- LOGIC ----------------
    if not has_item:
        target = (store_x + STORE_W // 2, store_y + STORE_H // 2)
    else:
        target = goal

    move_robot(target)

    rr = robot_rect()

    # PICKUP
    if rr.colliderect(store_rect()) and not has_item:
        has_item = True
        current_item = random.choice(ITEMS)
        print("Picked:", current_item["name"])

    # DELIVERY
    if rr.colliderect(goal_rect()) and has_item:
        print("Delivered:", current_item["name"])
        has_item = False
        items_collected += 1
        x, y = 60, 60

    # END CONDITION ⭐
    if items_collected >= total_items:
        print("ALL ITEMS COLLECTED & DELIVERED!")
        running = False

    # CRASH
    if car_collision():
        print("CRASH RESET")
        has_item = False
        x, y = 60, 60

    # EVENTS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # ---------------- DRAW ----------------
    draw_world()
    draw_store()
    draw_items()
    draw_current_item()
    draw_goal()
    draw_cars()
    draw_robot()

    pygame.display.update()

pygame.quit()