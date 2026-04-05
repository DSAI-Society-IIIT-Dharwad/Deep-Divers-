import pygame
import sys
import math

pygame.init()

# ---------------- SCREEN ----------------
WIDTH, HEIGHT = 500, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("VBots - Dynamic Obstacles + Path")

clock = pygame.time.Clock()

# ---------------- COLORS ----------------
GRASS = (70, 170, 90)
ROAD = (40, 40, 40)
WHITE = (255, 255, 255)
RED = (220, 60, 60)
BLUE = (60, 120, 255)
GRAY = (120, 120, 120)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 180)

# ---------------- OBJECTS ----------------
store = pygame.Rect(50, 400, 80, 60)
goal = pygame.Rect(420, 50, 50, 50)

# 2 STATIC obstacles
static_obstacles = [
    pygame.Rect(150, 150, 60, 20),
    pygame.Rect(300, 300, 80, 20)
]

# 2 MOVING cars (dynamic obstacles)
cars = [
    {"rect": pygame.Rect(200, 0, 30, 18), "speed": 2},
    {"rect": pygame.Rect(260, 500, 30, 18), "speed": -2.5}
]

# ---------------- ROBOT ----------------
robot = pygame.Rect(60, 60, 22, 22)
speed = 2.2

phase = 1
has_item = False

# ---------------- HELPERS ----------------
def distance(a, b):
    return math.hypot(a.x - b.x, a.y - b.y)

def move_robot(target):
    global robot

    dx = target.centerx - robot.centerx
    dy = target.centery - robot.centery

    dist = math.hypot(dx, dy)
    if dist == 0:
        return

    dx /= dist
    dy /= dist

    new_rect = robot.move(dx * speed, dy * speed)

    # ❌ BLOCK IF STATIC OBSTACLE
    for obs in static_obstacles:
        if new_rect.colliderect(obs):
            return  # stop movement

    # ❌ BLOCK IF CAR IN FRONT (DYNAMIC)
    for car in cars:
        if new_rect.colliderect(car["rect"]):
            return  # robot stops

    robot = new_rect

def update_cars():
    for car in cars:
        car["rect"].y += car["speed"]

        if car["rect"].y > HEIGHT:
            car["rect"].y = -20
        if car["rect"].y < -20:
            car["rect"].y = HEIGHT

def draw_path(target):
    pygame.draw.line(
        screen,
        CYAN,
        robot.center,
        target.center,
        2
    )

# ---------------- MAIN LOOP ----------------
running = True

while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    update_cars()

    # ---------------- PHASE LOGIC ----------------
    if phase == 1:
        target = store
    else:
        target = goal

    move_robot(target)

    # pick item
    if robot.colliderect(store) and phase == 1:
        has_item = True
        phase = 2

    # finish
    if robot.colliderect(goal) and phase == 2:
        print("Mission Complete!")
        running = False

    # ---------------- DRAW ----------------
    screen.fill(GRASS)

    pygame.draw.rect(screen, ROAD, (200, 0, 100, HEIGHT))

    pygame.draw.rect(screen, GREEN, store)
    pygame.draw.rect(screen, (0, 255, 0), goal)

    for obs in static_obstacles:
        pygame.draw.rect(screen, GRAY, obs)

    for car in cars:
        pygame.draw.rect(screen, RED, car["rect"])

    pygame.draw.rect(screen, WHITE, robot)

    # sensors (simple)
    pygame.draw.circle(screen, CYAN, robot.center, 35, 1)

    # PATH DISPLAY
    draw_path(target)

    pygame.display.update()

pygame.quit()