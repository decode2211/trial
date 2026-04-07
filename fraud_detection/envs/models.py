from pydantic import BaseModel
from typing import List

class Observation(BaseModel):
    sql_result: str
    fraud_signals: List[int]
    step_count: int

class Action(BaseModel):
    sql: str

class Reward(BaseModel):
    value: float
    reason: str
