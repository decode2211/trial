"""
Hugging Face Space entry point for the Fraud Detection OpenEnv environment.
Provides a simple web interface to interact with the environment.
"""
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import gradio as gr
from fraud_detection.envs.core_env import FraudEnv
from fraud_detection.tasks.tasks import TASKS
import json

# Create FastAPI app for OpenEnv compliance
fastapi_app = FastAPI()

# Global environment for API endpoints
api_env = None

class ResetResponse(BaseModel):
    observation: dict
    info: dict

class StepRequest(BaseModel):
    action: str

class StepResponse(BaseModel):
    observation: dict
    reward: float
    done: bool
    truncated: bool
    info: dict

@fastapi_app.post("/reset")
async def api_reset():
    """OpenEnv-compliant reset endpoint"""
    global api_env
    api_env = FraudEnv()
    obs, info = api_env.reset()
    return JSONResponse(content={"observation": obs, "info": info})

@fastapi_app.post("/step")
async def api_step(request: StepRequest):
    """OpenEnv-compliant step endpoint"""
    global api_env
    if api_env is None:
        return JSONResponse(content={"error": "Environment not initialized. Call /reset first."}, status_code=400)
    
    obs, reward, done, truncated, info = api_env.step(request.action)
    return JSONResponse(content={
        "observation": obs,
        "reward": float(reward),
        "done": bool(done),
        "truncated": bool(truncated),
        "info": info
    })

@fastapi_app.get("/state")
async def api_state():
    """OpenEnv-compliant state endpoint"""
    global api_env
    if api_env is None:
        return JSONResponse(content={"error": "Environment not initialized. Call /reset first."}, status_code=400)
    
    return JSONResponse(content=api_env.state())

@fastapi_app.get("/")
async def root():
    """Health check endpoint"""
    return JSONResponse(content={"status": "ok", "message": "Fraud Detection OpenEnv API"})


def create_environment():
    """Create and return a new environment instance."""
    return FraudEnv()


def reset_environment():
    """Reset the environment and return initial observation."""
    global env
    env = create_environment()
    obs, info = env.reset()
    return format_observation(obs), "Environment reset successfully!"


def step_environment(sql_query):
    """Execute a step in the environment."""
    global env
    if env is None:
        return "Error: Environment not initialized. Please reset first.", ""
    
    try:
        obs, reward, done, truncated, info = env.step(sql_query)
        
        result = f"**Reward:** {reward:.2f}\n\n"
        result += f"**Done:** {done or truncated}\n\n"
        result += f"**Observation:**\n{format_observation(obs)}"
        
        if done or truncated:
            result += "\n\n**Episode finished!**"
        
        return result, format_observation(obs)
    except Exception as e:
        return f"Error: {str(e)}", ""


def format_observation(obs):
    """Format observation for display."""
    if isinstance(obs, dict):
        return json.dumps(obs, indent=2)
    return str(obs)


def get_task_info(task_name):
    """Get information about a specific task."""
    for task in TASKS:
        if task.name == task_name:
            return f"**Task:** {task.name}\n\n**Description:** {task.description}"
    return "Task not found"


def grade_current_state(task_name):
    """Grade the current state for a specific task."""
    global env
    if env is None:
        return "Error: Environment not initialized. Please reset first."
    
    for task in TASKS:
        if task.name == task_name:
            state = env.state()
            score = task.grader(state)
            return f"**Task:** {task.name}\n**Score:** {score:.2f}"
    
    return "Task not found"


# Global environment instance
env = None

# Create Gradio interface
with gr.Blocks(title="Fraud Detection OpenEnv") as demo:
    gr.Markdown("""
    # 🔍 Financial Fraud Detection Environment
    
    This is an OpenEnv-compliant environment for training AI agents to detect financial fraud.
    
    ## How to use:
    1. Click **Reset Environment** to initialize
    2. Enter SQL queries to investigate the database
    3. View rewards and observations
    4. Grade your performance on specific tasks
    
    ## Available Tables:
    - `accounts`: Account information (account_id, name, balance, failed_logins, created_at)
    - `transactions`: Transaction records (transaction_id, source_account_id, dest_account_id, amount, type, timestamp)
    """)
    
    with gr.Row():
        with gr.Column():
            gr.Markdown("### Environment Control")
            reset_btn = gr.Button("Reset Environment", variant="primary")
            reset_output = gr.Textbox(label="Reset Status", lines=2)
            
            gr.Markdown("### Execute SQL Query")
            sql_input = gr.Textbox(
                label="SQL Query",
                placeholder="SELECT * FROM accounts LIMIT 5;",
                lines=3
            )
            step_btn = gr.Button("Execute Query", variant="primary")
            step_output = gr.Textbox(label="Result", lines=10)
            
        with gr.Column():
            gr.Markdown("### Current Observation")
            obs_output = gr.Textbox(label="Observation", lines=10)
            
            gr.Markdown("### Task Grading")
            task_selector = gr.Dropdown(
                choices=["EASY", "MEDIUM", "HARD"],
                label="Select Task",
                value="EASY"
            )
            task_info_btn = gr.Button("Show Task Info")
            task_info_output = gr.Textbox(label="Task Information", lines=4)
            
            grade_btn = gr.Button("Grade Current State")
            grade_output = gr.Textbox(label="Grade", lines=3)
    
    gr.Markdown("""
    ### Tasks:
    - **EASY**: Find all transactions above $10,000 in the last 30 days
    - **MEDIUM**: Identify accounts with >3 failed logins AND a transaction spike
    - **HARD**: Reconstruct a layering fraud chain across 5 hops of transfers
    """)
    
    # Connect buttons to functions
    reset_btn.click(reset_environment, outputs=[obs_output, reset_output])
    step_btn.click(step_environment, inputs=[sql_input], outputs=[step_output, obs_output])
    task_info_btn.click(get_task_info, inputs=[task_selector], outputs=[task_info_output])
    grade_btn.click(grade_current_state, inputs=[task_selector], outputs=[grade_output])

# Launch the app
if __name__ == "__main__":
    # Mount Gradio on FastAPI
    app = gr.mount_gradio_app(fastapi_app, demo, path="/gradio")
    
    # Run with uvicorn
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)
