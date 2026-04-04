from src.evaluation.metrics import compute_navigation_metrics


def test_compute_navigation_metrics():
    metrics = compute_navigation_metrics(
        [
            {"reward": 10.0, "steps": 25, "collision": False, "success": True},
            {"reward": -5.0, "steps": 50, "collision": True, "success": False},
        ]
    )

    assert metrics["episodes"] == 2
    assert metrics["success_rate"] == 0.5
    assert metrics["collision_rate"] == 0.5
    assert metrics["avg_steps_to_goal"] == 25.0
    assert metrics["avg_episode_reward"] == 2.5
