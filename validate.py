import os
import site

scripts_dir = os.path.join(site.getuserbase(), "Scripts")
openenv_path = os.path.join(scripts_dir, "openenv")
if not os.path.exists(openenv_path) and os.path.exists(openenv_path + ".exe"):
    openenv_path += ".exe"

print(f"Running: {openenv_path} validate fraud_detection/envs/core_env.py:FraudEnv")
ret = os.system(f'"{openenv_path}" validate fraud_detection/envs/core_env.py:FraudEnv')
print("Exit code:", ret)
