import gymnasium as gym
from gymnasium import spaces
import numpy as np

class RealWorldEnv(gym.Env):
    def __init__(self):
        super(RealWorldEnv, self).__init__()
        # Define action and observation space
        # Example: 0 = Stay, 1 = Move
        self.action_space = spaces.Discrete(2)
        # Example: A 1D sensor reading
        self.observation_space = spaces.Box(low=0, high=100, shape=(1,), dtype=np.float32)

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        # Reset the engine state
        state = np.array([50.0], dtype=np.float32)
        return state, {}

    def step(self, action):
        # 1. Update Engine logic
        # 2. Calculate Reward
        # 3. Check if done
        observation = np.array([50.0], dtype=np.float32)
        reward = 1.0
        terminated = False
        truncated = False
        return observation, reward, terminated, truncated, {}