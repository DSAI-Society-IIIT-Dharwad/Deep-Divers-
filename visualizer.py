import pygame
import numpy as np
import math

SCALE = 120


# 🌍 ENVIRONMENT (beautiful + stable)
def draw_environment(screen, w, h):
    # sky
    screen.fill((135, 206, 235))

    # grass
    pygame.draw.rect(screen, (34, 139, 34), (0, h//2, w, h//2))

    # road
    pygame.draw.rect(screen, (40, 40, 40), (0, h//2 - 50, w, 100))

    # road markings
    for i in range(0, w, 80):
        pygame.draw.rect(screen, (255, 255, 255), (i, h//2 - 5, 40, 10))

    # trees 🌳
    for i in range(50, w, 200):
        pygame.draw.rect(screen, (101, 67, 33), (i, h//2 - 120, 10, 40))
        pygame.draw.circle(screen, (34, 139, 34), (i+5, h//2 - 130), 25)

    # sun ☀️ (fixed, not moving)
    pygame.draw.circle(screen, (255, 223, 0), (w-80, 80), 40)


# 🤖 ROBOT (silver realistic)
def draw_robot(screen, pos, theta):
    x, y = int(pos[0]), int(pos[1])

    # shadow
    pygame.draw.ellipse(screen, (50, 50, 50), (x-30, y+10, 60, 20))

    # body
    pygame.draw.rect(screen, (200, 200, 210), (x-25, y-15, 50, 30), border_radius=8)
    pygame.draw.rect(screen, (160, 160, 170), (x-20, y-10, 40, 20), border_radius=6)

    # wheels
    pygame.draw.rect(screen, (20, 20, 20), (x-28, y-18, 8, 36))
    pygame.draw.rect(screen, (20, 20, 20), (x+20, y-18, 8, 36))

    # sensor
    fx = x + 25 * math.cos(theta)
    fy = y + 25 * math.sin(theta)
    pygame.draw.circle(screen, (0, 255, 255), (int(fx), int(fy)), 7)

    # direction line
    pygame.draw.line(
        screen,
        (255, 255, 255),
        (x, y),
        (x + 35 * math.cos(theta), y + 35 * math.sin(theta)),
        3
    )


# 🚧 OBSTACLES (cars + poles)
def draw_obstacle(screen, pos, i):
    x, y = int(pos[0]), int(pos[1])

    if i % 2 == 0:
        # car
        pygame.draw.rect(screen, (0, 0, 180), (x-25, y-12, 50, 25), border_radius=6)
        pygame.draw.circle(screen, (0, 0, 0), (x-15, y+13), 5)
        pygame.draw.circle(screen, (0, 0, 0), (x+15, y+13), 5)
    else:
        # electric pole
        pygame.draw.rect(screen, (120, 120, 120), (x-5, y-40, 10, 80))
def draw_status(screen, env, font):
    # check nearest obstacle
    min_dist = min([np.linalg.norm(env.position - o) for o in env.obstacles])

    if min_dist < 1.5:
        text = font.render("⚠️ DANGER!", True, (255, 0, 0))
        screen.blit(text, (20, 20))

    if env._check_collision():
        text = font.render("💥 COLLISION!", True, (255, 50, 50))
        screen.blit(text, (20, 60))

# 🚀 MAIN VISUAL LOOP
def run_visual(env, model):
    pygame.init()
    font = pygame.font.SysFont("Arial", 28)
    WIDTH, HEIGHT = 1000, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Robot Simulation")

    clock = pygame.time.Clock()

    obs, _ = env.reset()

    running = True

    while running:
        # 🌍 background
        draw_environment(screen, WIDTH, HEIGHT)

        # ❌ exit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # 🤖 AI action
        action, _ = model.predict(obs, deterministic=True)
        obs, reward, done, _, _ = env.step(action)

        # 🎯 goal
        goal = env.goal * SCALE
        pygame.draw.circle(screen, (0, 200, 0), goal.astype(int), 12)

        # 🚧 obstacles
        for i, o in enumerate(env.obstacles):
            draw_obstacle(screen, o * SCALE, i)

        # 🤖 robot
        robot = env.position * SCALE
        draw_robot(screen, robot, env.theta)
        draw_status(screen, env, font)
        pygame.display.flip()
        clock.tick(15)  # realistic speed

        # 🔁 reset after finish
        if done:
            obs, _ = env.reset()

    pygame.quit()
    def run_visual(env, model):
     import pygame
    pygame.init()

    WIDTH, HEIGHT = 1000, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Robot Simulation")

    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 28)

    obs, _ = env.reset()
    done = False

    running = True

    while running:
        draw_environment(screen, WIDTH, HEIGHT)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and done:
                    obs, _ = env.reset()
                    done = False

        if not done:
            action, _ = model.predict(obs, deterministic=True)
            obs, reward, done, _, _ = env.step(action)

        goal = env.goal * SCALE
        pygame.draw.circle(screen, (0, 200, 0), goal.astype(int), 12)

        for i, o in enumerate(env.obstacles):
            draw_obstacle(screen, o * SCALE, i)

        robot = env.position * SCALE
        draw_robot(screen, robot, env.theta)

        if done:
            if env._check_collision():
                text = font.render("💥 COLLISION! Press ENTER", True, (255, 0, 0))
            else:
                text = font.render("🎯 GOAL REACHED! Press ENTER", True, (0, 200, 0))

            screen.blit(text, (20, 20))

        pygame.display.flip()
        clock.tick(15)

    pygame.quit()