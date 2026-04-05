import pygame
import sys
import math
import random

# OPTIONAL VOICE (uncomment if you want real speech)
# import pyttsx3
# engine = pyttsx3.init()

pygame.init()

# ---------------- SCREEN ----------------
WIDTH, HEIGHT = 500, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("VBots - Talking Robot AI")

clock = pygame.time.Clock()

# ---------------- COLORS ----------------
GRASS = (70, 170, 90)
ROAD = (45, 45, 45)
STORE = (210, 210, 215)
GOAL_COLOR = (0, 255, 180)
ROBOT = (200, 200, 210)
SENSOR = (0, 255, 255)
BLACK = (0, 0, 0)

# ---------------- POSITIONS ----------------
store_x, store_y = 40, 380
goal = (430, 60)

# ---------------- ROBOT ----------------
x, y = 60.0, 60.0
speed = 2.5
ROBOT_SIZE = 22

has_item = False
phase = 1  # 1 = pickup, 2 = delivery
running = True

# ---------------- SPEECH SYSTEM ----------------
current_speech = ""

def speak(text):
    global current_speech
    current_speech = text
    print("Robot:", text)

    # OPTIONAL VOICE
    # engine.say(text)
    # engine.runAndWait()

def draw_speech():
    if current_speech:
        font = pygame.font.SysFont("Arial", 14)
        img = font.render(current_speech, True, BLACK)
        screen.blit(img, (x, y - 25))

# ---------------- HELPERS ----------------
def robot_rect():
    return pygame.Rect(int(x), int(y), ROBOT_SIZE, ROBOT_SIZE)

def store_rect():
    return pygame.Rect(store_x, store_y, 120, 90)

def goal_rect():
    return pygame.Rect(goal[0]-15, goal[1]-15, 30, 30)

# ---------------- MOVE ----------------
def move_robot(target):
    global x, y

    dx = target[0] - x
    dy = target[1] - y

    dist = math.hypot(dx, dy)
    if dist > 0:
        dx /= dist
        dy /= dist

    x += dx * speed
    y += dy * speed

# ---------------- DRAW ----------------
def draw_world():
    screen.fill(GRASS)
    pygame.draw.rect(screen, ROAD, (200, 0, 100, HEIGHT))

def draw_store():
    pygame.draw.rect(screen, STORE, (store_x, store_y, 120, 90))

def draw_goal():
    pygame.draw.circle(screen, GOAL_COLOR, goal, 16)

def draw_robot():
    rr = robot_rect()
    pygame.draw.rect(screen, ROBOT, rr, border_radius=5)

    # sensors
    sx, sy = rr.center
    for a in [-20, 0, 20]:
        rad = math.radians(a)
        ex = sx + math.cos(rad) * 15
        ey = sy + math.sin(rad) * 15
        pygame.draw.line(screen, SENSOR, (sx, sy), (ex, ey), 1)

    draw_speech()

# ---------------- MAIN LOOP ----------------
speak("System starting... Going to store")

while running:
    clock.tick(60)

    rr = robot_rect()

    # ---------------- PHASE LOGIC ----------------
    if phase == 1:
        target = (store_x + 60, store_y + 45)
    else:
        target = goal

    move_robot(target)

    # ---------------- PHASE 1 ----------------
    if phase == 1 and rr.colliderect(store_rect()):
        has_item = True
        phase = 2
        speak("Item collected! Moving to delivery point")

    # ---------------- PHASE 2 ----------------
    if phase == 2 and rr.colliderect(goal_rect()):
        speak("Item delivered successfully!")
        speak("Mission complete. Shutting down simulation.")
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
    draw_robot()

    pygame.display.update()

pygame.quit()