import pygame
import sys
import math

pygame.init()

# ---------------- SCREEN ----------------
WIDTH, HEIGHT = 500, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("VBots City + Grid + Smart Stop")

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

# ---------------- GRID ----------------
GRID_SIZE = 50

def draw_grid():
    for x in range(0, WIDTH, GRID_SIZE):
        pygame.draw.line(screen, (200, 200, 200), (x, 0), (x, HEIGHT), 1)
    for y in range(0, HEIGHT, GRID_SIZE):
        pygame.draw.line(screen, (200, 200, 200), (0, y), (WIDTH, y), 1)

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
has_item = False

# ---------------- MOVEMENT ----------------
def move_cars():
    for car in cars:
        car["rect"].y += car["speed"]

        if car["rect"].y > HEIGHT:
            car["rect"].y = -20
        if car["rect"].y < -20:
            car["rect"].y = HEIGHT

def next_move(target):
    dx = target.centerx - robot.centerx
    dy = target.centery - robot.centery
    dist = math.hypot(dx, dy)

    if dist == 0:
        return robot

    dx /= dist
    dy /= dist

    return robot.move(dx * speed, dy * speed)

def blocked(next_rect):
    for obs in obstacles:
        if next_rect.colliderect(obs):
            return True
    for car in cars:
        if next_rect.colliderect(car["rect"]):
            return True
    return False

def car_in_front():
    sensor = robot.copy()
    sensor.inflate_ip(60, 60)

    for car in cars:
        if sensor.colliderect(car["rect"]):
            return True
    return False

def move_robot(target):
    global robot

    if car_in_front():
        return

    nxt = next_move(target)

    if blocked(nxt):
        return

    robot = nxt

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

    # ---------------- PHASE ----------------
    target = store if phase == 1 else goal

    move_robot(target)

    if robot.colliderect(store) and phase == 1:
        has_item = True
        phase = 2

    if robot.colliderect(goal) and phase == 2:
        print("Mission Completed!")
        running = False

    # ---------------- DRAW ----------------
    screen.fill(GRASS)

    draw_grid()  # 🟦 GRID ADDED

    pygame.draw.rect(screen, ROAD, (200, 0, 100, HEIGHT))

    pygame.draw.rect(screen, GREEN, store)
    pygame.draw.rect(screen, (0, 255, 0), goal)

    for obs in obstacles:
        pygame.draw.rect(screen, GRAY, obs)

    for car in cars:
        pygame.draw.rect(screen, RED, car["rect"])

    pygame.draw.rect(screen, BLUE, robot)

    pygame.draw.circle(screen, CYAN, robot.center, 30, 1)

    draw_path(target)

    font = pygame.font.SysFont("Arial", 16)
    status = "STOPPED (CAR AHEAD)" if car_in_front() else "MOVING"
    screen.blit(font.render(status, True, WHITE), (10, 10))

    pygame.display.update()

pygame.quit()