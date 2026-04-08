import gymnasium as gym
from gymnasium import spaces
import numpy as np
from typing import Optional, Tuple, Dict, Any
from .engine import FraudEngine, FraudState
from .models import Observation, Action, Reward

class FraudEnv(gym.Env):
    metadata = {"render_modes": ["human"]}
    
    def __init__(self, render_mode: Optional[str] = None):
        super().__init__()
        self.render_mode = render_mode
        self.engine = FraudEngine()
        
        # Max length for text to avoid infinite.
        self.observation_space = spaces.Dict(
            {
                "sql_result": spaces.Text(max_length=1000),
                "fraud_signals": spaces.MultiBinary(10),
                "step_count": spaces.Discrete(50)
            }
        )
        self.action_space = spaces.Text(max_length=500)
        
    def reset(self, seed: Optional[int] = None, options: Optional[Dict[str, Any]] = None) -> Tuple[Dict[str, Any], dict]:
        super().reset(seed=seed)
        self.engine.reset()
        if self.render_mode == "human":
            self.render()
        obs = {"sql_result": "", "fraud_signals": [0]*10, "step_count": 0}
        return obs, {}
        
    def step(self, action: Action) -> Tuple[Dict[str, Any], float, bool, bool, dict]:
        sql = action.sql if isinstance(action, Action) else action
        obs_dict, reward, terminated, truncated, info = self.engine.step(sql)
        
        if self.render_mode == "human":
            self.render()
            
        return obs_dict, reward, terminated, truncated, info
        
    def state(self) -> dict:
        # Expected by constraints
        return self.engine.state.model_dump()
        
    def render(self):
        if self.render_mode == "human":
            st = self.engine.state
            print(f"--- FraudState Summary ---")
            print(f"Step: {st.step_count}")
            print(f"Result length: {len(st.sql_result)}")
            print(f"Fraud Signals: {st.fraud_signals}")
            print("--------------------------")

if __name__ == "__main__":
    env = FraudEnv(render_mode="human")
    obs, info = env.reset()
    
    actions = [
        "SELECT * FROM accounts LIMIT 5;",
        "SELECT amount FROM transactions WHERE amount > 10000 LIMIT 5;",
        "SELECT * FROM accounts WHERE failed_logins > 3 LIMIT 5;"
    ]
    
    for act in actions:
        print(f"Taking action: {act}")
        obs, reward, done, truncated, info = env.step(act)
        print(f"Reward: {reward}")
        print(f"Observation sql_result preview: {obs['sql_result'][:50]}...")
        if done or truncated:
            break
