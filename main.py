import argparse

from src.agents.ppo_agent import PPOAgent
from src.env import create_env
from src.evaluation.evaluator import Evaluator
from src.training.trainer import train
from src.utils.config_loader import load_config


def main():
    parser = argparse.ArgumentParser(description="DRL autonomous navigation trainer")
    parser.add_argument(
        "command",
        nargs="?",
        default="train",
        choices=["train", "evaluate"],
        help="Whether to train a policy or evaluate an existing one.",
    )
    parser.add_argument(
        "--config",
        default="configs/default.yaml",
        help="Path to the training configuration YAML file.",
    )
    parser.add_argument(
        "--model",
        default=None,
        help="Path to a trained model for evaluation. Defaults to the configured model path.",
    )
    parser.add_argument(
        "--episodes",
        type=int,
        default=10,
        help="Number of episodes to run during evaluation.",
    )
    args = parser.parse_args()

    if args.command == "train":
        train(args.config)
        return

    config = load_config(args.config)
    env = create_env(config)
    model_path = args.model or config.get("training", {}).get("model_path", "models/ppo_model")
    agent = PPOAgent(env).load(model_path)
    metrics = Evaluator(env, agent).run(episodes=args.episodes)
    Evaluator.save_report(metrics)
    print(metrics)
    env.close()


if __name__ == "__main__":
    main()
