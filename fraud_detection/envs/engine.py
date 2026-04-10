import sqlite3
import os
import re
from typing import List, Tuple, Dict, Any, Optional, Set
from pydantic import BaseModel, ConfigDict
import numpy as np

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "db", "fraud.db")

REWARD_CLIP = (-1.0, 1.0)

class Transaction(BaseModel):
    model_config = ConfigDict(extra="allow")
    transaction_id: str
    source_account_id: str
    dest_account_id: str
    amount: float
    type: str
    timestamp: str

class Account(BaseModel):
    model_config = ConfigDict(extra="allow")
    account_id: str
    name: str
    balance: float
    failed_logins: int
    created_at: str

class FraudSignal(BaseModel):
    model_config = ConfigDict(extra="allow")
    type: str
    confidence: float

class FraudState(BaseModel):
    model_config = ConfigDict(extra="allow", arbitrary_types_allowed=True)
    step_count: int
    sql_result: str
    query_history: List[str]
    fraud_signals: List[int]
    discovered_markers: Set[str] = set()
    
class FraudEngine:
    def __init__(self):
        self.conn = None
        self.state: FraudState = None
        self.max_steps = 50
        
    def reset(self) -> FraudState:
        np.random.seed(42)
        if self.conn:
            self.conn.close()
        self.conn = sqlite3.connect(DB_PATH)
        self.conn.row_factory = sqlite3.Row
        
        self.state = FraudState(
            step_count=0,
            sql_result="Welcome to AntiGravity DB. Tables: accounts, transactions.",
            query_history=[],
            fraud_signals=[0] * 10,
            discovered_markers=set()
        )
        return self.state
        
    def _task_complete(self) -> bool:
        return all(
            marker in self.state.discovered_markers
            for marker in ["A005", "A010", "A045"]
        )
        
    def step(self, action: str) -> Tuple[Dict[str, Any], float, bool, bool, Dict[str, Any]]:
        self.state.step_count += 1
        info = {}
        action_upper = action.upper()
        result_rows = []
        
        is_destructive = any(kw in action_upper for kw in ["DROP", "DELETE", "TRUNCATE"])
        is_loop = action in self.state.query_history
        
        if is_destructive:
            self.state.sql_result = "ERROR: Destructive operations prohibited."
        elif is_loop:
            pass
        else:
            try:
                cursor = self.conn.cursor()
                cursor.execute(action)
                rows = cursor.fetchall()
                if not rows:
                    self.state.sql_result = "No results found."
                else:
                    result_rows = [dict(r) for r in rows]
                    truncated = result_rows[:100]
                    self.state.sql_result = "\\n".join([str(r) for r in truncated])
            except sqlite3.Error as e:
                self.state.sql_result = f"SQL ERROR: {e}"
                info["error"] = str(e)
                
        reward = self._compute_reward(action, result_rows)
        
        if not is_destructive and not is_loop:
            self.state.query_history.append(action)
            
        terminated = self._task_complete()
        truncated = self.state.step_count >= self.max_steps
        
        if terminated:
            reward += 1.0
            
        return self._get_obs(), reward, terminated, truncated, info

    def _compute_reward(self, action: str, result_rows: list) -> float:
        action_upper = action.upper()

        if any(kw in action_upper for kw in ["DROP", "DELETE", "TRUNCATE"]):
            return -0.4

        if action in self.state.query_history:
            return -0.2

        reward = 0.0

        if any(t in action_upper for t in ["ACCOUNTS", "TRANSACTIONS"]):
            reward += 0.3

        discovered = {
            row["account_id"] for row in result_rows 
            if "account_id" in row
        }
        new_finds = discovered & {"A005", "A010", "A045"} - self.state.discovered_markers
        if new_finds:
            self.state.discovered_markers.update(new_finds)
            reward += 0.5

        return max(REWARD_CLIP[0], min(REWARD_CLIP[1], reward))
        
    def _get_obs(self) -> Dict[str, Any]:
        # Return observation suitable for core_env
        # Convert NumPy types to native Python types for JSON serialization
        fraud_signals = self.state.fraud_signals
        if hasattr(fraud_signals, 'tolist'):
            fraud_signals = fraud_signals.tolist()
        else:
            fraud_signals = [int(x) for x in fraud_signals]
        return {
            "sql_result": self.state.sql_result[:1000],
            "fraud_signals": fraud_signals,
            "step_count": int(self.state.step_count)
        }
