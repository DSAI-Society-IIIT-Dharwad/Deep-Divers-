from src.env.factory import create_env
from src.env.robot_env import RobotEnv


def test_create_mock_env():
    config = {
        "environment": {
            "name": "mock",
            "params": {
                "goal": [4.0, 4.0],
                "world_size": 5.0,
                "max_steps": 50,
            },
        }
    }

    env = create_env(config)
    assert isinstance(env, RobotEnv)
    assert env.world_size == 5.0
    assert env.max_steps == 50
    env.close()
