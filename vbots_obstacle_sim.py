import pygame
import sys
import math
import random

pygame.init()

# ---------------- SCREEN ----------------
WIDTH, HEIGHT = 500, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("VBots - 2 Phase + Obstacles")

clock = pygame.time.Clock()

# ---------------- COLORS ----------------
GRASS = (70, 170, 90)
ROAD = (45, 45, 45)
ROBOT = (200, 200, 210)
STORE = (210, 210, 215)
GOAL = (0, 255, 180)
OBSTACLE = (120, 120, 120)
SENSOR = (0, 255, 255)
BLACK = (0, 0, 0)

# ---------------- OBJECTS ----------------
store = pygame.Rect(40, 380, 100, 80)
goal = pygame.Rect(420, 60, 40, 40)

obstacles = [
    pygame.Rect(200, 100, 80, 20),
    pygame.Rect(320, 200, 100, 20),
    pygame.Rect(120, 250, 20, 100),
    pygame.Rect(260, 320, 120, 20)
]

# ---------------- ROBOT ----------------
x, y = 60.0, 60.0
speed = 2.5
size = 22

has_item = False
phase = 1
running = True

# ---------------- SPEECH ----------------
msg = ""

def speak(text):
    global msg
    msg = text
    print("Robot:", text)

# ---------------- HELPERS ----------------
def robot_rect():
    return pygame.Rect(int(x), int(y), size, size)

def draw_speech():
    font = pygame.font.SysFont("Arial", 14)
    img = font.render(msg, True, BLACK)
    screen.blit(img, (x, y - 20))

# ---------------- COLLISION ----------------
def check_collision(rect):
    for obs in obstacles:
        if rect.colliderect(obs):
            return True
    return False

# ---------------- MOVE ----------------
def move_robot(target):
    global x, y

    dx = target[0] - x
    dy = target[1] - y

    dist = math.hypot(dx, dy)
    if dist > 0:
        dx /= dist
        dy /= dist

    new_x = x + dx * speed
    new_y = y + dy * speed

    test_rect = pygame.Rect(int(new_x), int(new_y), size, size)

    # collision check
    if not check_collision(test_rect):
        x, y = new_x, new_y
    else:
        speak("Obstacle detected!")

# ---------------- DRAW ----------------
def draw_world():
    screen.fill(GRASS)
    pygame.draw.rect(screen, ROAD, (200, 0, 100, HEIGHT))

def draw_store():
    pygame.draw.rect(screen, STORE, store)

def draw_goal():
    pygame.draw.rect(screen, GOAL, goal)

def draw_obstacles():
    for obs in obstacles:
        pygame.draw.rect(screen, OBSTACLE, obs)

def draw_robot():
    rr = robot_rect()
    pygame.draw.rect(screen, ROBOT, rr, border_radius=5)

    # sensors
    cx, cy = rr.center
    for a in [-25, 0, 25]:
        rad = math.radians(a)
        ex = cx + math.cos(rad) * 15
        ey = cy + math.sin(rad) * 15
        pygame.draw.line(screen, SENSOR, (cx, cy), (ex, ey), 1)

    draw_speech()

# ---------------- MAIN ----------------
speak("Starting mission... Go to store")

while running:
    clock.tick(60)

    rr = robot_rect()

    # ---------------- PHASE LOGIC ----------------
    if phase == 1:
        target = store.center
    else:
        target = goal.center

    move_robot(target)

    # ---------------- PHASE 1 ----------------
    if phase == 1 and rr.colliderect(store):
        has_item = True
        phase = 2
        speak("Item picked! Going to delivery point")

    # ---------------- PHASE 2 ----------------
    if phase == 2 and rr.colliderect(goal):
        speak("Item delivered successfully!")
        speak("Mission complete")
        running = False

    # ---------------- EVENTS ----------------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # ---------------- DRAW ----------------
    draw_world()
    draw_store()
    draw_goal()
    draw_obstacles()
    draw_robot()

    pygame.display.update()

pygame.quit()