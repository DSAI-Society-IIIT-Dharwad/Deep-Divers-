import numpy as np


def summarize_episode_rewards(episode_rewards):
    values = np.asarray(episode_rewards, dtype=np.float32)
    if values.size == 0:
        return {"mean_reward": 0.0, "max_reward": 0.0, "min_reward": 0.0}

    return {
        "mean_reward": float(np.mean(values)),
        "max_reward": float(np.max(values)),
        "min_reward": float(np.min(values)),
    }


def compute_navigation_metrics(episodes):
    if not episodes:
        return {
            "episodes": 0,
            "success_rate": 0.0,
            "collision_rate": 0.0,
            "avg_steps_to_goal": 0.0,
            "avg_episode_reward": 0.0,
        }

    rewards = [episode["reward"] for episode in episodes]
    successes = [episode["success"] for episode in episodes]
    collisions = [episode["collision"] for episode in episodes]
    successful_steps = [episode["steps"] for episode in episodes if episode["success"]]

    return {
        "episodes": len(episodes),
        "success_rate": float(np.mean(successes)),
        "collision_rate": float(np.mean(collisions)),
        "avg_steps_to_goal": float(np.mean(successful_steps)) if successful_steps else 0.0,
        "avg_episode_reward": float(np.mean(rewards)),
        **summarize_episode_rewards(rewards),
    }
