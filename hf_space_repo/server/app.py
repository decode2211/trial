"""
FastAPI server for OpenEnv compliance.
Provides REST API endpoints for environment interaction.
"""
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
import sys
import os

# Add parent directory to path to import fraud_detection
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fraud_detection.envs.core_env import FraudEnv

app = FastAPI(title="Fraud Detection OpenEnv API")

# Global environment instance
env: Optional[FraudEnv] = None

class ActionRequest(BaseModel):
    action: str

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"status": "ok", "message": "Fraud Detection OpenEnv API"}

@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy"}

@app.post("/reset")
async def reset():
    """Reset the environment"""
    global env
    try:
        env = FraudEnv()
        obs, info = env.reset()
        return JSONResponse(content={"observation": obs, "info": info})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/step")
async def step(request: ActionRequest):
    """Execute a step in the environment"""
    global env
    if env is None:
        raise HTTPException(status_code=400, detail="Environment not initialized. Call /reset first.")
    
    try:
        obs, reward, done, truncated, info = env.step(request.action)
        return JSONResponse(content={
            "observation": obs,
            "reward": float(reward),
            "done": bool(done),
            "truncated": bool(truncated),
            "info": info
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/state")
async def state():
    """Get current environment state"""
    global env
    if env is None:
        raise HTTPException(status_code=400, detail="Environment not initialized. Call /reset first.")
    
    try:
        return JSONResponse(content=env.state())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)

def main():
    """Entry point for OpenEnv server command"""
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)
