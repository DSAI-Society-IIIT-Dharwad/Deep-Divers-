import pygame
import sys
import math

pygame.init()

# ---------------- SCREEN ----------------
WIDTH, HEIGHT = 600, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("VBots Fixed Front Obstacle Detection")

clock = pygame.time.Clock()

# ---------------- COLORS ----------------
GRASS = (80, 180, 90)
ROAD = (50, 50, 50)
WHITE = (255, 255, 255)
RED = (220, 70, 70)
BLUE = (80, 140, 255)
GRAY = (120, 120, 120)
GREEN = (0, 255, 140)
CYAN = (0, 255, 255)
YELLOW = (255, 220, 80)

# ---------------- ENVIRONMENT ----------------
store = pygame.Rect(60, 420, 80, 60)
goal = pygame.Rect(520, 40, 60, 60)

obstacles = [
    pygame.Rect(250, 200, 80, 25),
    pygame.Rect(380, 350, 90, 25)
]

cars = [
    {"rect": pygame.Rect(300, 0, 35, 20), "speed": 2.5},
    {"rect": pygame.Rect(350, 500, 35, 20), "speed": -2.2}
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

# ---------------- PATH TARGET ----------------
def get_target():
    if phase == 1:
        return store
    else:
        return goal

# ---------------- MOVE ROBOT ----------------
def move_towards(target):
    dx = target.centerx - robot.centerx
    dy = target.centery - robot.centery
    dist = math.hypot(dx, dy)

    if dist == 0:
        return robot

    dx /= dist
    dy /= dist

    return robot.move(dx * speed, dy * speed)

# ---------------- COLLISION CHECK ----------------
def blocked(rect):
    for obs in obstacles:
        if rect.colliderect(obs):
            return True
    return False

# ---------------- 🔥 FIXED FRONT SENSOR (REAL RAY) ----------------
def car_in_front(target):
    dx = target.centerx - robot.centerx
    dy = target.centery - robot.centery
    dist = math.hypot(dx, dy)

    if dist == 0:
        return False

    dx /= dist
    dy /= dist

    # 🔥 strict forward ray
    for step in range(15, 100, 10):
        x = int(robot.centerx + dx * step)
        y = int(robot.centery + dy * step)

        ray = pygame.Rect(x, y, 5, 5)

        for car in cars:
            if ray.colliderect(car["rect"]):
                return True

    return False

# ---------------- ROBOT LOGIC ----------------
def update_robot(target):
    global robot

    # STOP ONLY if car is directly in front path
    if car_in_front(target):
        return

    nxt = move_towards(target)

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

    target = get_target()

    update_robot(target)

    # ---------------- PHASE LOGIC ----------------
    if robot.colliderect(store) and phase == 1:
        has_item = True
        phase = 2

    if robot.colliderect(goal) and phase == 2 and has_item:
        print("✅ Mission Completed!")
        running = False

    # ---------------- DRAW ----------------
    screen.fill(GRASS)

    # road
    pygame.draw.rect(screen, ROAD, (250, 0, 120, HEIGHT))

    # store + goal
    pygame.draw.rect(screen, GREEN, store)
    pygame.draw.rect(screen, YELLOW, goal)

    # obstacles
    for obs in obstacles:
        pygame.draw.rect(screen, GRAY, obs)

    # cars
    for car in cars:
        pygame.draw.rect(screen, RED, car["rect"])

    # robot
    pygame.draw.rect(screen, BLUE, robot)

    # path
    draw_path(target)

    # sensor visualization (small)
    pygame.draw.circle(screen, CYAN, robot.center, 30, 1)

    # status text
    font = pygame.font.SysFont("Arial", 16)

    if car_in_front(target):
        status = "STOPPED: CAR IN FRONT"
    else:
        status = "MOVING"

    screen.blit(font.render(status, True, WHITE), (10, 10))
    screen.blit(font.render(f"Phase: {phase}", True, WHITE), (10, 30))

    pygame.display.update()

pygame.quit()