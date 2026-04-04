import json
from pathlib import Path

from src.evaluation.metrics import compute_navigation_metrics


class Evaluator:
    def __init__(self, env, agent):
        self.env = env
        self.agent = agent

    def run(self, episodes=10, deterministic=True):
        history = []

        for _ in range(episodes):
            obs, _ = self.env.reset()
            terminated = False
            truncated = False
            episode_reward = 0.0
            step_count = 0
            collision = False
            success = False

            while not (terminated or truncated):
                action = self.agent.predict(obs, deterministic=deterministic)
                obs, reward, terminated, truncated, _ = self.env.step(action)
                episode_reward += reward
                step_count += 1

                collision = bool(obs[11] > 0.5)
                success = bool(terminated and not collision and obs[5] < 0.8)

            history.append(
                {
                    "reward": float(episode_reward),
                    "steps": step_count,
                    "collision": collision,
                    "success": success,
                }
            )

        return compute_navigation_metrics(history)

    @staticmethod
    def save_report(metrics, output_path="logs/evaluation.json"):
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(metrics, indent=2), encoding="utf-8")
