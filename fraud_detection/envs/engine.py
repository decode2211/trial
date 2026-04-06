import sqlite3
import os
import re
from typing import List, Tuple, Dict, Any, Optional
from pydantic import BaseModel, ConfigDict
import numpy as np

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "db", "fraud.db")

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
    model_config = ConfigDict(extra="allow")
    step_count: int
    sql_result: str
    query_history: List[str]
    fraud_signals: List[int]
    
class FraudEngine:
    def __init__(self):
        self.conn = None
        self.state: FraudState = None
        
    def reset(self) -> FraudState:
        np.random.seed(42)
        if self.conn:
            self.conn.close()
        self.conn = sqlite3.connect(DB_PATH)
        
        self.state = FraudState(
            step_count=0,
            sql_result="Welcome to AntiGravity DB. Tables: accounts, transactions.",
            query_history=[],
            fraud_signals=[0] * 10
        )
        return self.state
        
    def step(self, action: str) -> Tuple[Dict[str, Any], float, bool, Dict[str, Any]]:
        self.state.step_count += 1
        reward = 0.0
        done = False
        info = {}
        action_upper = action.upper()
        
        # Dense reward shaping
        
        # -0.4 destructive SQL (DROP/DELETE/TRUNCATE)
        if any(bad_word in action_upper for bad_word in ["DROP", "DELETE", "TRUNCATE"]):
            reward -= 0.4
            self.state.sql_result = "ERROR: Destructive operations prohibited."
            return self._get_obs(), reward, done, info
            
        # -0.2 repeated identical query (loop detection)
        if action in self.state.query_history:
            reward -= 0.2
        else:
            self.state.query_history.append(action)
            
        # +0.3 querying correct table
        if "ACCOUNTS" in action_upper or "TRANSACTIONS" in action_upper:
            reward += 0.3
            
        try:
            cursor = self.conn.cursor()
            cursor.execute(action)
            rows = cursor.fetchall()
            
            # Simple conversion of results to string
            if not rows:
                self.state.sql_result = "No results found."
            else:
                # Truncate at 100 rows to avoid blowing up text size
                truncated = rows[:100]
                self.state.sql_result = "\\n".join([str(row) for row in truncated])
            
            # +0.5 true-positive fraud signal
            # We approximate this by seeing if the result contains known fraud indicators
            # For our seed DB: A005, A010, A040..A045 or high amounts like >10000
            result_str = self.state.sql_result
            if "A005" in result_str or "A010" in result_str or "A045" in result_str:
                reward += 0.5
                self.state.fraud_signals[0] = 1 # Mark some signal active
            
            if done:
                reward += 1.0 # terminal bonus
                
        except sqlite3.Error as e:
            self.state.sql_result = f"SQL ERROR: {e}"
            info["error"] = str(e)
            
        return self._get_obs(), reward, done, info
        
    def _get_obs(self) -> Dict[str, Any]:
        # Return observation suitable for core_env
        return {
            "sql_result": self.state.sql_result[:1000], # Keep length in check
            "fraud_signals": np.array(self.state.fraud_signals, dtype=np.int8),
            "step_count": self.state.step_count
        }
