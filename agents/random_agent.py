import gymnasium as gym
import envs  # This triggers the registration

env = gym.make("RealWorldEnv-v0")
observation, info = env.reset()

for _ in range(10):
    action = env.action_space.sample()  # Take a random action
    observation, reward, terminated, truncated, info = env.step(action)
    print(f"Action: {action}, Reward: {reward}")

    if terminated or truncated:
        observation, info = env.reset()

env.close()