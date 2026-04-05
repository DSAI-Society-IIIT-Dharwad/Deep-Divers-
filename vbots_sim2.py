import pygame
import sys
import math
import random

pygame.init()

# ---------------- SCREEN ----------------
WIDTH, HEIGHT = 500, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Robot Delivery - REAL SHOP")

clock = pygame.time.Clock()

# ---------------- COLORS ----------------
GRASS = (70, 170, 90)
ROAD = (50, 50, 50)
LANES = (230, 230, 230)

SHOP_WALL = (210, 210, 215)
SHOP_ROOF = (160, 160, 170)
SHOP_GLASS = (180, 220, 255)
SHOP_DOOR = (120, 90, 70)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

ROBOT_BODY = (190, 190, 200)
ROBOT_DARK = (120, 120, 130)

SENSOR = (0, 255, 255)

CAR1 = (220, 60, 60)
CAR2 = (60, 120, 255)

GOAL_COLOR = (0, 255, 180)

ITEM_COLORS = {
    "bottle": (80, 180, 255),
    "fruit": (255, 80, 80),
    "box": (200, 140, 80)
}

# ---------------- ROAD ----------------
ROAD_X = 200
ROAD_W = 100

# ---------------- SHOP (REAL BUILDING) ----------------
shop_x, shop_y = 30, 360
SHOP_W, SHOP_H = 120, 100

items = ["bottle", "fruit", "box"]
current_item = random.choice(items)

# ---------------- ROBOT ----------------
x, y = 60.0, 60.0
speed = 2.8

ROBOT_W, ROBOT_H = 22, 26
has_item = False

goal = (430, 430)

# ---------------- CARS ----------------
cars = [
    {"x": ROAD_X + 10, "y": 50, "v": 2.2, "color": CAR1},
    {"x": ROAD_X + 55, "y": 250, "v": -2.0, "color": CAR2},
]

# ---------------- HELPERS ----------------
def robot_rect():
    return pygame.Rect(int(x), int(y), ROBOT_W, ROBOT_H)

def goal_rect():
    return pygame.Rect(goal[0]-18, goal[1]-18, 36, 36)

def shop_rect():
    return pygame.Rect(shop_x, shop_y, SHOP_W, SHOP_H)

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

def move_cars():
    for c in cars:
        c["y"] += c["v"]
        if c["y"] > HEIGHT + 40:
            c["y"] = -40
        if c["y"] < -40:
            c["y"] = HEIGHT + 40

def car_collision():
    rr = robot_rect()
    for c in cars:
        car_rect = pygame.Rect(c["x"], c["y"], 35, 18)
        if rr.colliderect(car_rect):
            return True
    return False

# ---------------- SMALL SENSORS ----------------
def draw_sensors():
    sensor_range = 25

    sx = x + ROBOT_W // 2
    sy = y

    for a in [-20, 0, 20]:
        rad = math.radians(a)
        ex = sx + math.cos(rad) * sensor_range
        ey = sy + math.sin(rad) * sensor_range

        pygame.draw.line(screen, SENSOR, (sx, sy), (ex, ey), 1)
        pygame.draw.circle(screen, SENSOR, (int(ex), int(ey)), 2)

# ---------------- SHOP DRAW (REALISTIC) ----------------
def draw_shop():
    rect = shop_rect()

    # walls
    pygame.draw.rect(screen, SHOP_WALL, rect, border_radius=6)

    # roof
    pygame.draw.polygon(screen, SHOP_ROOF, [
        (rect.x, rect.y),
        (rect.x + rect.w // 2, rect.y - 25),
        (rect.x + rect.w, rect.y)
    ])

    # glass front
    pygame.draw.rect(screen, SHOP_GLASS, (rect.x + 10, rect.y + 20, rect.w - 20, 35))

    # door
    pygame.draw.rect(screen, SHOP_DOOR, (rect.x + rect.w//2 - 10, rect.y + 55, 20, 45))

    # signboard
    font = pygame.font.SysFont(None, 22)
    text = font.render("SHOP", True, BLACK)
    screen.blit(text, (rect.x + 40, rect.y + 5))

    # items inside shop (visible on shelves)
    shelf_y = rect.y + 30

    for i, item in enumerate(items):
        color = ITEM_COLORS[item]
        pygame.draw.rect(screen, color, (rect.x + 15 + i*30, shelf_y, 12, 12))

# ---------------- ITEM DISPLAY ----------------
def draw_current_item():
    if has_item:
        return

    rect = shop_rect()
    ix = rect.x + 50
    iy = rect.y + 40

    color = ITEM_COLORS[current_item]

    if current_item == "bottle":
        pygame.draw.rect(screen, color, (ix, iy, 6, 14))
    elif current_item == "fruit":
        pygame.draw.circle(screen, color, (ix+5, iy+6), 6)
    elif current_item == "box":
        pygame.draw.rect(screen, color, (ix, iy, 12, 12))

# ---------------- ROBOT ----------------
def draw_robot():
    rr = robot_rect()

    pygame.draw.rect(screen, ROBOT_BODY, rr, border_radius=6)
    pygame.draw.rect(screen, ROBOT_DARK,
                     (rr.x + 4, rr.y - 10, ROBOT_W - 8, 10),
                     border_radius=4)

    pygame.draw.circle(screen, WHITE, (rr.x + 7, rr.y - 5), 2)
    pygame.draw.circle(screen, WHITE, (rr.x + 15, rr.y - 5), 2)

    pygame.draw.circle(screen, BLACK, (rr.x + 5, rr.y + ROBOT_H), 3)
    pygame.draw.circle(screen, BLACK, (rr.x + 17, rr.y + ROBOT_H), 3)

    if has_item:
        pygame.draw.circle(screen, (255, 215, 0), (rr.x + 11, rr.y - 15), 4)

    draw_sensors()

# ---------------- WORLD ----------------
def draw_world():
    screen.fill(GRASS)
    pygame.draw.rect(screen, ROAD, (ROAD_X, 0, ROAD_W, HEIGHT))

    for i in range(0, HEIGHT, 25):
        pygame.draw.rect(screen, LANES, (ROAD_X + 48, i, 4, 12))

def draw_cars():
    for c in cars:
        x1, y1 = int(c["x"]), int(c["y"])

        pygame.draw.rect(screen, c["color"], (x1, y1, 35, 18), border_radius=4)
        pygame.draw.rect(screen, (200, 220, 255), (x1+5, y1+3, 10, 6))
        pygame.draw.rect(screen, (200, 220, 255), (x1+18, y1+3, 10, 6))

        pygame.draw.circle(screen, BLACK, (x1+7, y1+18), 3)
        pygame.draw.circle(screen, BLACK, (x1+28, y1+18), 3)

def draw_goal():
    pygame.draw.circle(screen, GOAL_COLOR, goal, 18)
    pygame.draw.circle(screen, WHITE, goal, 6)

# ---------------- MAIN LOOP ----------------
running = True

while running:
    clock.tick(60)

    move_cars()

    # ---------------- LOGIC ----------------
    if not has_item:
        target = (shop_x + SHOP_W // 2, shop_y + SHOP_H // 2)
    else:
        target = goal

    move_robot(target)

    rr = robot_rect()

    # pickup from SHOP
    if rr.colliderect(shop_rect()) and not has_item:
        has_item = True
        current_item = random.choice(items)
        print("Picked:", current_item)

    # delivery
    if rr.colliderect(goal_rect()) and has_item:
        print("Delivered:", current_item)
        has_item = False
        x, y = 60, 60

    # crash
    if car_collision():
        print("CRASH RESET")
        has_item = False
        x, y = 60, 60

    # events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # ---------------- DRAW ----------------
    draw_world()
    draw_shop()
    draw_current_item()
    draw_goal()
    draw_cars()
    draw_robot()

    pygame.display.update()

pygame.quit()