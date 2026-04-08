import traceback
try:
    from fraud_detection.envs.core_env import FraudEnv
    env = FraudEnv(render_mode="human")
    obs, info = env.reset()
    print("Reset successful")
    
    actions = [
        "SELECT * FROM accounts LIMIT 5;",
    ]
    
    for act in actions:
        print(f"Taking action: {act}")
        obs, reward, done, truncated, info = env.step(act)
        print(f"Reward: {reward}")
    
    print("Done testing.")
except Exception as e:
    traceback.print_exc()
