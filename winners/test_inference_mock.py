"""
Mock inference test to verify the inference script structure without API calls.
"""
import sys
from fraud_detection.envs.core_env import FraudEnv
from fraud_detection.tasks.tasks import TASKS


def mock_inference():
    """Run a mock inference to test the structure."""
    print("=== Mock Inference Test ===\n")
    
    env = FraudEnv()
    
    # Predefined queries for each task
    task_queries = {
        "EASY": [
            "SELECT * FROM transactions WHERE amount > 10000 AND timestamp >= DATE('now', '-30 days');"
        ],
        "MEDIUM": [
            "SELECT a.account_id FROM accounts a JOIN transactions t ON a.account_id = t.source_account_id WHERE a.failed_logins > 3 GROUP BY a.account_id HAVING COUNT(t.transaction_id) > 10;"
        ],
        "HARD": [
            "SELECT * FROM transactions WHERE source_account_id IN ('A040', 'A041', 'A042', 'A043', 'A044') AND dest_account_id IN ('A041', 'A042', 'A043', 'A044', 'A045') ORDER BY timestamp;"
        ]
    }
    
    for task in TASKS:
        print(f"[START] task={task.name} model=mock-model")
        
        obs, info = env.reset()
        total_reward = 0.0
        step_count = 0
        
        # Use predefined queries for this task
        queries = task_queries.get(task.name, ["SELECT * FROM accounts LIMIT 1;"])
        
        for query in queries:
            obs, reward, done, truncated, info = env.step(query)
            total_reward += float(reward)
            step_count += 1
            
            print(f"[STEP]  step={step_count} action={query[:50]}... reward={reward} done={done or truncated}")
            
            if done or truncated:
                break
        
        # Grade the final state
        score = task.grader(env.state())
        print(f"[END]   total_reward={total_reward} steps={step_count} score={score}")
        print()
    
    print("=== Mock Inference Complete ===")


if __name__ == "__main__":
    try:
        mock_inference()
        print("\n✓ Inference structure is correct!")
        sys.exit(0)
    except Exception as e:
        print(f"\n✗ Inference test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
