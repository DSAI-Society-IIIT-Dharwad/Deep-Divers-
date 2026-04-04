from pathlib import Path

try:
    from stable_baselines3.common.callbacks import BaseCallback
except ImportError:  # pragma: no cover - handled at runtime when SB3 is missing
    BaseCallback = object


class TrainingRewardCallback(BaseCallback):
    def __init__(self, log_every=1000, save_path=None, verbose=0):
        super().__init__(verbose=verbose)
        self.log_every = int(log_every)
        self.save_path = save_path
        self.episode_rewards = []

    def _on_step(self):
        if self.locals.get("dones") is not None:
            rewards = self.locals.get("rewards", [])
            dones = self.locals.get("dones", [])
            for reward, done in zip(rewards, dones):
                if done:
                    self.episode_rewards.append(float(reward))

        if self.n_calls % self.log_every == 0:
            print(f"Training step {self.n_calls}")
            if self.save_path:
                Path(self.save_path).parent.mkdir(parents=True, exist_ok=True)
                self.model.save(self.save_path)

        return True
