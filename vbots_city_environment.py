import pygame
import sys
import math

pygame.init()

# ---------------- SCREEN ----------------
WIDTH, HEIGHT = 500, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("VBots City Environment (Restored)")

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
BLACK = (0, 0, 0)

# ---------------- MAP ----------------
store = pygame.Rect(50, 400, 80, 60)   # POINT A
goal = pygame.Rect(420, 50, 50, 50)    # END

# static obstacles (2)
obstacles = [
    pygame.Rect(150, 150, 60, 20),
    pygame.Rect(300, 300, 80, 20)
]

# dynamic cars (2)
cars = [
    {"rect": pygame.Rect(210, 0, 30, 18), "speed": 2.2},
    {"rect": pygame.Rect(260, 500, 30, 18), "speed": -2.5}
]

# ---------------- ROBOT ----------------
robot = pygame.Rect(60, 60, 22, 22)
speed = 2.2

phase = 1   # 1 = store, 2 = goal
has_item = False

# ---------------- HELPERS ----------------
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
    # static obstacles
    for obs in obstacles:
        if next_rect.colliderect(obs):
            return True

    # dynamic cars
    for car in cars:
        if next_rect.colliderect(car["rect"]):
            return True

    return False

def move_robot(target):
    global robot

    nxt = next_move(target)

    if blocked(nxt):
        return  # STOP robot

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

    # road
    pygame.draw.rect(screen, ROAD, (200, 0, 100, HEIGHT))

    # objects
    pygame.draw.rect(screen, GREEN, store)
    pygame.draw.rect(screen, (0, 255, 0), goal)

    for obs in obstacles:
        pygame.draw.rect(screen, GRAY, obs)

    for car in cars:
        pygame.draw.rect(screen, RED, car["rect"])

    pygame.draw.rect(screen, BLUE, robot)

    # sensor visualization (small)
    pygame.draw.circle(screen, CYAN, robot.center, 30, 1)

    # path line
    draw_path(target)

    # status
    font = pygame.font.SysFont("Arial", 16)

    status = "STOPPED" if blocked(next_move(target)) else "MOVING"
    screen.blit(font.render(status, True, WHITE), (10, 10))

    pygame.display.update()

pygame.quit()