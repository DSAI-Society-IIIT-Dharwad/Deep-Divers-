from src.env import create_env
from stable_baselines3 import PPO

def train():
    env = create_env()

    model = PPO("MlpPolicy", env, verbose=1)

    print("Training started...")
    model.learn(total_timesteps=200000)

    model.save("models/ppo_model")

    print("Training done!")
    env.close()