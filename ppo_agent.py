from pathlib import Path

from stable_baselines3 import PPO

from src.agents.base_agent import BaseAgent


class PPOAgent(BaseAgent):
    def __init__(self, env, policy="MlpPolicy", verbose=1, **kwargs):
        self.model = PPO(policy, env, verbose=verbose, **kwargs)

    def train(self, steps, callback=None):
        self.model.learn(total_timesteps=steps, callback=callback)

    def save(self, path="models/ppo_model"):
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        self.model.save(path)

    def load(self, path):
        self.model = PPO.load(path)
        return self

    def predict(self, obs, deterministic=True):
        action, _ = self.model.predict(obs, deterministic=deterministic)
        return action
