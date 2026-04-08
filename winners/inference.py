import os
from dotenv import load_dotenv

load_dotenv()
import sys
import time
import openai
from fraud_detection.envs.core_env import FraudEnv
from fraud_detection.tasks.tasks import TASKS

def run_inference():
    start_time = time.time()
    
    groq_key = os.getenv("GROQ_API_KEY")
    openai_key = os.getenv("OPENAI_API_KEY")
    
    if "API_BASE_URL" in os.environ:
        api_base_url = os.environ["API_BASE_URL"]
        model_name = os.environ.get("MODEL_NAME", "llama-3.1-8b-instant")
        token = groq_key or openai_key or os.getenv("HF_TOKEN", "dummy_token")
    elif groq_key:
        api_base_url = "https://api.groq.com/openai/v1"
        model_name = os.getenv("MODEL_NAME", "llama-3.1-8b-instant")
        token = groq_key
    elif openai_key:
        api_base_url = "https://api.openai.com/v1"
        model_name = os.getenv("MODEL_NAME", "gpt-4o-mini")
        token = openai_key
    else:
        api_base_url = "https://api.groq.com/openai/v1"
        model_name = os.getenv("MODEL_NAME", "llama-3.1-8b-instant")
        token = os.getenv("HF_TOKEN", "dummy_token")
    
    def check_timeout():
        if time.time() - start_time > 1200:
            print("Timeout exceeded 1200s.")
            sys.exit(1)

    client = openai.OpenAI(base_url=api_base_url, api_key=token, max_retries=0)
    
    env = FraudEnv()

    for task in TASKS:
        check_timeout()
        print(f"[START] task={task.name} model={model_name}")
        
        obs, info = env.reset()
        done = False
        truncated = False
        total_reward = 0.0
        step_count = 0
        
        messages = [
            {"role": "system", "content": "You are a SQL agent analyzing a SQLite database for financial fraud. Tables are 'accounts' and 'transactions'. Output exactly one SQL query to execute. If you have the final answer in your previous observation, output exactly 'STOP'. Do not include markdown like ```sql or explanations."}
        ]
        
        while not (done or truncated) and step_count < 50:
            check_timeout()
            
            obs_str = f"Task: {task.description}\\n"
            obs_str += f"SQL Result:\\n{obs['sql_result']}\\n"
            obs_str += f"Fraud Signals: {obs['fraud_signals'].tolist()}\\n"
            obs_str += f"Observation Step: {obs['step_count']}"
            
            messages.append({"role": "user", "content": obs_str})
            
            try:
                response = client.chat.completions.create(
                    model=model_name,
                    messages=messages,
                    max_tokens=150,
                    temperature=0.0
                )
                action = response.choices[0].message.content.strip()
                if action.startswith("```sql"):
                    action = action[6:]
                if action.startswith("```"):
                    action = action[3:]
                if action.endswith("```"):
                    action = action[:-3]
                action = action.strip()
            except Exception as e:
                print(f"API Error: {e}")
                action = "SELECT * FROM accounts LIMIT 1;"

            if action == "STOP":
                break

            obs, reward, done, truncated, info = env.step(action)
            messages.append({"role": "assistant", "content": action})
            
            total_reward += float(reward)
            step_count += 1
            
            # The exact requested log format
            print(f"[STEP]  step={step_count} action={action} reward={reward} done={done or truncated}")
            
        score = task.grader(env.state())
        print(f"[END]   total_reward={total_reward} steps={step_count} score={score}")

if __name__ == "__main__":
    run_inference()
