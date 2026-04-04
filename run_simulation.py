from stable_baselines3 import PPO
from src.env.robot_env import RobotEnv
from src.evaluation.visualizer import run_visual

env = RobotEnv()
model = PPO.load("models/ppo_model")

# Phase 1
env.set_phase(1)
print("Phase 1: Collision")
run_visual(env, model)

input("Press ENTER for Phase 2...")

# Phase 2
env.set_phase(2)
print("Phase 2: Goal")
run_visual(env, model)