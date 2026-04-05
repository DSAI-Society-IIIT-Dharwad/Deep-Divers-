import pygame
import sys
import time

pygame.init()

# ---------------- SCREEN ----------------
WIDTH, HEIGHT = 500, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("VBots Grid Stop & Resume")

clock = pygame.time.Clock()

# ---------------- GRID SIZE ----------------
CELL = 200

def to_px(pos):
    x, y = pos
    return x * CELL + 100, y * CELL + 100

# ---------------- POINTS ----------------
start = (0, 0)   # 00
goal = (0, 2)    # 02

robot_pos = [0, 0]

# ---------------- CAR (dynamic obstacle) ----------------
car_active = True
car_pos = pygame.Rect(100, 300, 60, 30)

# ---------------- COLORS ----------------
GREEN = (0, 255, 0)
RED = (220, 60, 60)
WHITE = (255, 255, 255)
BLUE = (80, 150, 255)
GRAY = (120, 120, 120)
BLACK = (0, 0, 0)

# ---------------- MOVE CONTROL ----------------
paused = False
step_delay = 0.6
last_move_time = time.time()

def car_in_front():
    """Check if car blocks middle path"""
    rx, ry = to_px(robot_pos)
    robot_rect = pygame.Rect(rx, ry, 30, 30)
    return robot_rect.colliderect(car_pos)

def move_robot():
    global robot_pos

    if robot_pos == list(goal):
        return

    # MOVE DOWN TOWARDS (0,2)
    next_pos = [robot_pos[0], robot_pos[1] + 1]

    # TEMP POSITION CHECK
    old = robot_pos[:]
    robot_pos[:] = next_pos

    if car_in_front():
        robot_pos[:] = old
        return False

    return True

# ---------------- MAIN LOOP ----------------
running = True

while running:
    clock.tick(60)
    screen.fill(GRAY)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # ---------------- CAR LOGIC ----------------
    # Car appears in middle then moves away
    if car_active:
        car_pos.x += 1
        if car_pos.x > 500:
            car_active = False  # car gone

    # ---------------- ROBOT LOGIC ----------------
    if time.time() - last_move_time > step_delay:
        if car_in_front():
            paused = True
        else:
            paused = False
            moved = move_robot()
        last_move_time = time.time()

    # ---------------- DRAW GRID ----------------
    for i in range(3):
        for j in range(3):
            x, y = i * CELL + 100, j * CELL + 100
            pygame.draw.rect(screen, WHITE, (x, y, CELL - 20, CELL - 20), 2)

    # ---------------- DRAW START & GOAL ----------------
    sx, sy = to_px(start)
    gx, gy = to_px(goal)

    pygame.draw.rect(screen, GREEN, (sx, sy, 30, 30))
    pygame.draw.rect(screen, RED, (gx, gy, 30, 30))

    # ---------------- DRAW ROBOT ----------------
    rx, ry = to_px(robot_pos)
    pygame.draw.rect(screen, BLUE, (rx, ry, 30, 30))

    # ---------------- DRAW CAR ----------------
    if car_active:
        pygame.draw.rect(screen, BLACK, car_pos)

    # ---------------- STATUS TEXT ----------------
    font = pygame.font.SysFont("Arial", 18)

    if paused:
        text = font.render("Robot STOPPED: Car ahead", True, RED)
    else:
        text = font.render("Robot MOVING", True, GREEN)

    screen.blit(text, (20, 20))

    pygame.display.update()

pygame.quit()