import pygame
import sys
import math

pygame.init()

# ---------------- SCREEN ----------------
WIDTH, HEIGHT = 500, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("VBots Directional Sensor Stop Fix")

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

obstacles = [
    pygame.Rect(150, 150, 60, 20),
    pygame.Rect(300, 300, 80, 20)
]

cars = [
    {"rect": pygame.Rect(210, 0, 30, 18), "speed": 2.3},
    {"rect": pygame.Rect(260, 500, 30, 18), "speed": -2.6}
]

# ---------------- ROBOT ----------------
robot = pygame.Rect(60, 60, 22, 22)
speed = 2.2

phase = 1

# ---------------- CAR MOVEMENT ----------------
def move_cars():
    for car in cars:
        car["rect"].y += car["speed"]
        if car["rect"].y > HEIGHT:
            car["rect"].y = -20
        if car["rect"].y < -20:
            car["rect"].y = HEIGHT

# ---------------- NEXT MOVE ----------------
def next_move(target):
    dx = target.centerx - robot.centerx
    dy = target.centery - robot.centery
    dist = math.hypot(dx, dy)

    if dist == 0:
        return robot

    dx /= dist
    dy /= dist

    return robot.move(dx * speed, dy * speed)

# ---------------- BLOCKING ----------------
def blocked(next_rect):
    for obs in obstacles:
        if next_rect.colliderect(obs):
            return True
    for car in cars:
        if next_rect.colliderect(car["rect"]):
            return True
    return False

# ---------------- 🔥 FIXED DIRECTIONAL SENSOR ----------------
def car_in_front(target):
    # direction vector
    dx = target.centerx - robot.centerx
    dy = target.centery - robot.centery
    dist = math.hypot(dx, dy)

    if dist == 0:
        return False

    dx /= dist
    dy /= dist

    # look-ahead point (forward beam)
    look_x = robot.centerx + dx * 60
    look_y = robot.centery + dy * 60

    sensor = pygame.Rect(look_x - 10, look_y - 10, 20, 20)

    for car in cars:
        if sensor.colliderect(car["rect"]):
            return True

    return False

# ---------------- MOVE ROBOT ----------------
def move_robot(target):
    global robot

    # 🛑 STOP ONLY if car is directly in FRONT direction
    if car_in_front(target):
        return

    nxt = next_move(target)

    if blocked(nxt):
        return

    robot = nxt

# ---------------- DRAW PATH ----------------
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

    target = store if phase == 1 else goal

    move_robot(target)

    if robot.colliderect(store) and phase == 1:
        phase = 2

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

    pygame.draw.circle(screen, CYAN, robot.center, 25, 1)

    draw_path(target)

    # status
    font = pygame.font.SysFont("Arial", 16)

    if car_in_front(target):
        status = "STOPPED (CAR IN FRONT)"
    else:
        status = "MOVING"

    screen.blit(font.render(status, True, WHITE), (10, 10))

    pygame.display.update()

pygame.quit()