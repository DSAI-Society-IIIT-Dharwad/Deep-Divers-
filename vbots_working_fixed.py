import pygame
import sys
import math

pygame.init()

WIDTH, HEIGHT = 600, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("VBots Stable Movement Fix")

clock = pygame.time.Clock()

# ---------------- COLORS ----------------
GRASS = (80, 180, 90)
ROAD = (50, 50, 50)
WHITE = (255, 255, 255)
RED = (220, 70, 70)
BLUE = (80, 140, 255)
GRAY = (120, 120, 120)
GREEN = (0, 255, 140)
YELLOW = (255, 220, 80)
CYAN = (0, 255, 255)

# ---------------- ENV ----------------
store = pygame.Rect(60, 420, 80, 60)
goal = pygame.Rect(520, 40, 60, 60)

obstacles = [
    pygame.Rect(250, 200, 80, 25),
    pygame.Rect(380, 350, 90, 25)
]

cars = [
    {"rect": pygame.Rect(300, 0, 35, 20), "speed": 2.2},
    {"rect": pygame.Rect(350, 500, 35, 20), "speed": -2.0}
]

# ---------------- ROBOT ----------------
robot = pygame.Rect(80, 80, 22, 22)
speed = 2.3

phase = 1
has_item = False

# ---------------- MOVE CARS ----------------
def move_cars():
    for car in cars:
        car["rect"].y += car["speed"]
        if car["rect"].y > HEIGHT:
            car["rect"].y = -30
        if car["rect"].y < -30:
            car["rect"].y = HEIGHT

# ---------------- TARGET ----------------
def target_point():
    return store if phase == 1 else goal

# ---------------- MOVE ROBOT ----------------
def move_robot(target):
    dx = target.centerx - robot.centerx
    dy = target.centery - robot.centery
    dist = math.hypot(dx, dy)

    if dist == 0:
        return robot

    dx /= dist
    dy /= dist

    return robot.move(dx * speed, dy * speed)

# ---------------- COLLISION ----------------
def blocked(rect):
    for obs in obstacles:
        if rect.colliderect(obs):
            return True
    return False

# ---------------- 🔥 FIXED SENSOR (IMPORTANT) ----------------
def car_in_front(target):
    dx = target.centerx - robot.centerx
    dy = target.centery - robot.centery
    dist = math.hypot(dx, dy)

    if dist == 0:
        return False

    dx /= dist
    dy /= dist

    # ONLY CHECK VERY NEAR FORWARD LINE
    for step in range(10, 70, 10):
        x = int(robot.centerx + dx * step)
        y = int(robot.centery + dy * step)

        point = pygame.Rect(x, y, 6, 6)

        for car in cars:
            # extra safety: ensure car is roughly in direction
            if point.colliderect(car["rect"]):
                return True

    return False

# ---------------- UPDATE ----------------
def update_robot(target):
    global robot

    # DEBUG: uncomment to test if sensor is always true
    # print(car_in_front(target))

    if car_in_front(target):
        return  # STOP only if truly in front

    nxt = move_robot(target)

    if not blocked(nxt):
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

    target = target_point()

    update_robot(target)

    # ---------------- PHASE LOGIC ----------------
    if robot.colliderect(store) and phase == 1:
        has_item = True
        phase = 2

    if robot.colliderect(goal) and phase == 2 and has_item:
        print("MISSION COMPLETE")
        running = False

    # ---------------- DRAW ----------------
    screen.fill(GRASS)

    pygame.draw.rect(screen, ROAD, (250, 0, 120, HEIGHT))

    pygame.draw.rect(screen, GREEN, store)
    pygame.draw.rect(screen, YELLOW, goal)

    for obs in obstacles:
        pygame.draw.rect(screen, GRAY, obs)

    for car in cars:
        pygame.draw.rect(screen, RED, car["rect"])

    pygame.draw.rect(screen, BLUE, robot)

    draw_path(target)

    pygame.draw.circle(screen, CYAN, robot.center, 25, 1)

    font = pygame.font.SysFont("Arial", 16)

    status = "STOPPED" if car_in_front(target) else "MOVING"

    screen.blit(font.render(status, True, WHITE), (10, 10))
    screen.blit(font.render(f"Phase: {phase}", True, WHITE), (10, 30))

    pygame.display.update()

pygame.quit()