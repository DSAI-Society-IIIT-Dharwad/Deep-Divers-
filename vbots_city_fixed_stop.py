import pygame
import sys
import math

pygame.init()

# ---------------- SCREEN ----------------
WIDTH, HEIGHT = 500, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("VBots City - FIXED STOP SYSTEM")

clock = pygame.time.Clock()

# ---------------- COLORS ----------------
GRASS = (70, 170, 90)
ROAD = (40, 40, 40)
WHITE = (255, 255, 255)
RED = (220, 60, 60)
BLUE = (80, 150, 255)
GRAY = (120, 120, 120)
GREEN = (0, 255, 180)
CYAN = (0, 255, 255)

# ---------------- ENVIRONMENT ----------------
store = pygame.Rect(50, 400, 80, 60)
goal = pygame.Rect(420, 50, 50, 50)

# Static obstacles
obstacles = [
    pygame.Rect(150, 150, 60, 20),
    pygame.Rect(300, 300, 80, 20)
]

# Dynamic cars
cars = [
    {"rect": pygame.Rect(210, 0, 30, 18), "speed": 2.3},
    {"rect": pygame.Rect(260, 500, 30, 18), "speed": -2.6}
]

# ---------------- ROBOT ----------------
robot = pygame.Rect(60, 60, 22, 22)
speed = 2.2

phase = 1
has_item = False

# ---------------- CAR MOVEMENT ----------------
def move_cars():
    for car in cars:
        car["rect"].y += car["speed"]

        if car["rect"].y > HEIGHT:
            car["rect"].y = -20
        if car["rect"].y < -20:
            car["rect"].y = HEIGHT

# ---------------- PATH ----------------
def next_move(target):
    dx = target.centerx - robot.centerx
    dy = target.centery - robot.centery
    dist = math.hypot(dx, dy)

    if dist == 0:
        return robot

    dx /= dist
    dy /= dist

    return robot.move(dx * speed, dy * speed)

# ---------------- COLLISION ----------------
def blocked(next_rect):
    # static obstacles
    for obs in obstacles:
        if next_rect.colliderect(obs):
            return True

    # cars
    for car in cars:
        if next_rect.colliderect(car["rect"]):
            return True

    return False

# ---------------- 🔥 FIXED SENSOR (IMPORTANT) ----------------
def car_in_front():
    sensor = robot.copy()
    sensor.inflate_ip(60, 60)  # enlarged vision zone

    for car in cars:
        if sensor.colliderect(car["rect"]):
            return True

    return False

# ---------------- ROBOT MOVE ----------------
def move_robot(target):
    global robot

    # 🛑 STOP if car is detected in front
    if car_in_front():
        return

    nxt = next_move(target)

    if blocked(nxt):
        return

    robot = nxt

# ---------------- PATH DRAW ----------------
def draw_path(target):
    pygame.draw.line(screen, CYAN, robot.center, target.center, 2)

# ---------------- MAIN LOOP ----------------
running = True

while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    move_cars()

    # ---------------- PHASES ----------------
    target = store if phase == 1 else goal

    move_robot(target)

    # pick item
    if robot.colliderect(store) and phase == 1:
        has_item = True
        phase = 2

    # finish
    if robot.colliderect(goal) and phase == 2:
        print("Mission Completed!")
        running = False

    # ---------------- DRAW ----------------
    screen.fill(GRASS)

    pygame.draw.rect(screen, ROAD, (200, 0, 100, HEIGHT))

    pygame.draw.rect(screen, GREEN, store)
    pygame.draw.rect(screen, (0, 255, 0), goal)

    for obs in obstacles:
        pygame.draw.rect(screen, GRAY, obs)

    for car in cars:
        pygame.draw.rect(screen, RED, car["rect"])

    pygame.draw.rect(screen, BLUE, robot)

    # sensor visual
    pygame.draw.circle(screen, CYAN, robot.center, 30, 1)

    # path line
    draw_path(target)

    # status
    font = pygame.font.SysFont("Arial", 16)

    if car_in_front():
        status = "STOPPED (CAR AHEAD)"
    else:
        status = "MOVING"

    screen.blit(font.render(status, True, WHITE), (10, 10))

    pygame.display.update()

pygame.quit()