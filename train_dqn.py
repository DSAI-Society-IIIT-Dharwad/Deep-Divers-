from vbots_dqn_env import VBotsEnv
from dqn_agent import DQNAgent
import numpy as np

env = VBotsEnv()

state_size = 7
action_size = 4

agent = DQNAgent(state_size, action_size)

EPISODES = 500

for e in range(EPISODES):
    state = env.reset()
    total_reward = 0

    for time in range(500):
        action = agent.act(state)
        next_state, reward, done = env.step(action)

        agent.remember(state, action, reward, next_state, done)
        state = next_state
        total_reward += reward

        if done:
            break

    agent.replay()

    print(f"Episode {e+1} | Reward: {total_reward:.2f} | Epsilon: {agent.epsilon:.3f}")