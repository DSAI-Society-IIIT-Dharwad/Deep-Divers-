import pygame
import sys
import math
import random

pygame.init()

# ---------------- SCREEN ----------------
WIDTH, HEIGHT = 500, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("VBots - City Simulation")

clock = pygame.time.Clock()

# ---------------- COLORS ----------------
GRASS = (70, 170, 90)
ROAD = (40, 40, 40)
LANE = (220, 220, 220)

ROBOT = (200, 200, 210)
STORE = (210, 210, 215)
GOAL = (0, 255, 180)

OBSTACLE = (120, 120, 120)
CAR1 = (220, 60, 60)
CAR2 = (60, 120, 255)

SENSOR = (0, 255, 255)
BLACK = (0, 0, 0)

# ---------------- MAP ----------------
road = pygame.Rect(200, 0, 100, HEIGHT)

store = pygame.Rect(40, 380, 100, 80)
goal = pygame.Rect(420, 60, 40, 40)

obstacles = [
    pygame.Rect(120, 120, 60, 20),
    pygame.Rect(260, 220, 90, 20),
    pygame.Rect(80, 260, 20, 80),
    pygame.Rect(300, 340, 100, 20)
]

# ---------------- VEHICLES ----------------
cars = [
    {"x": 210, "y": 50, "v": 2.5, "c": CAR1},
    {"x": 260, "y": 300, "v": -2.2, "c": CAR2}
]

# ---------------- ROBOT ----------------
x, y = 60.0, 60.0
size = 22
speed = 2.4

phase = 1
has_item = False
running = True

msg = ""

# ---------------- SPEECH ----------------
def speak(text):
    global msg
    msg = text
    print("Robot:", text)

# ---------------- HELPERS ----------------
def robot_rect():
    return pygame.Rect(int(x), int(y), size, size)

def car_rect(c):
    return pygame.Rect(c["x"], c["y"], 30, 18)

def draw_speech():
    font = pygame.font.SysFont("Arial", 14)
    img = font.render(msg, True, BLACK)
    screen.blit(img, (x, y - 25))

# ---------------- COLLISION ----------------
def hit_obstacle(r):
    for o in obstacles:
        if r.colliderect(o):
            return True
    return False

def hit_car(r):
    for c in cars:
        if r.colliderect(car_rect(c)):
            return True
    return False

# ---------------- MOVE ----------------
def move_robot(target):
    global x, y, phase

    dx = target[0] - x
    dy = target[1] - y

    dist = math.hypot(dx, dy)
    if dist > 0:
        dx /= dist
        dy /= dist

    new_x = x + dx * speed
    new_y = y + dy * speed

    test = pygame.Rect(int(new_x), int(new_y), size, size)

    # obstacle collision → CHANGE PHASE
    if hit_obstacle(test):
        speak("Obstacle hit! Switching phase!")
        phase = 2
        return

    # car collision → reset
    if hit_car(test):
        speak("Car collision! Reset!")
        x, y = 60, 60
        return

    x, y = new_x, new_y

# ---------------- CARS ----------------
def move_cars():
    for c in cars:
        c["y"] += c["v"]
        if c["y"] > HEIGHT:
            c["y"] = -20
        if c["y"] < -20:
            c["y"] = HEIGHT

# ---------------- DRAW ----------------
def draw_world():
    screen.fill(GRASS)
    pygame.draw.rect(screen, ROAD, road)

    # lane markings
    for i in range(0, HEIGHT, 30):
        pygame.draw.rect(screen, LANE, (250, i, 5, 15))

def draw_store():
    pygame.draw.rect(screen, STORE, store)

def draw_goal():
    pygame.draw.rect(screen, GOAL, goal)

def draw_obstacles():
    for o in obstacles:
        pygame.draw.rect(screen, OBSTACLE, o)

def draw_cars():
    for c in cars:
        pygame.draw.rect(screen, c["c"], car_rect(c))

def draw_robot():
    r = robot_rect()
    pygame.draw.rect(screen, ROBOT, r, border_radius=5)

    cx, cy = r.center
    for a in [-25, 0, 25]:
        rad = math.radians(a)
        ex = cx + math.cos(rad) * 15
        ey = cy + math.sin(rad) * 15
        pygame.draw.line(screen, SENSOR, (cx, cy), (ex, ey), 1)

    draw_speech()

# ---------------- MAIN ----------------
speak("Mission start")

while running:
    clock.tick(60)

    move_cars()
    rr = robot_rect()

    # ---------------- PHASE LOGIC ----------------
    if phase == 1:
        target = store.center
    else:
        target = goal.center

    move_robot(target)

    # pickup
    if rr.colliderect(store) and phase == 1:
        has_item = True
        phase = 2
        speak("Item picked! Going to goal")

    # delivery
    if rr.colliderect(goal) and phase == 2:
        speak("Delivered successfully!")
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
    draw_cars()
    draw_robot()

    pygame.display.update()

pygame.quit()