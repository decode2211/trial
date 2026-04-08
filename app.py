from fastapi import FastAPI
from pydantic import BaseModel
from typing import Any, Dict
from fraud_detection.envs.core_env import FraudEnv

app = FastAPI()
env = FraudEnv()

class ActionRequest(BaseModel):
    sql: str

@app.get("/reset")
def reset():
    obs, info = env.reset()
    return {"observation": obs, "info": info}

@app.post("/step")
def step(action: ActionRequest):
    obs, reward, terminated, truncated, info = env.step(action.sql)
    return {
        "observation": obs,
        "reward": reward,
        "terminated": terminated,
        "truncated": truncated,
        "info": info
    }

@app.get("/state")
def state():
    return env.state()

@app.get("/health")
def health():
    return {"status": "ok"}