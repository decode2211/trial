from pydantic import BaseModel, Field
from typing import Dict, Any, Optional

class Observation(BaseModel):
    # The Architect will add specific fields here later based on the chosen job
    state_description: str = Field(..., description="A text summary of the current state.")
    available_actions: list[str] = Field(..., description="List of actions the agent can take right now.")
    raw_data: Optional[Dict[str, Any]] = Field(default=None, description="Any JSON data needed for context.")

class Action(BaseModel):
    # The Architect will define the exact buttons the AI can press here
    action_type: str = Field(..., description="The type of action to execute.")
    parameters: Optional[Dict[str, Any]] = Field(default=None, description="Arguments for the action.")

class Reward(BaseModel):
    # This is standard across all OpenEnv projects
    value: float = Field(..., ge=-1.0, le=1.0, description="The reward value for the current step.")
    message: str = Field(..., description="Explanation of why this reward was given (for the trace logs).")