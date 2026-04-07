import sys
import os

print("--- Running seed.py ---")
os.system(f"{sys.executable} db/seed.py")

print("\n--- Testing tasks.py ---")
from tasks.tasks import MEDIUM_TRUTH
print('Medium truth:', MEDIUM_TRUTH)

print("\n--- Testing engine.py / core_env.py ---")
from envs.core_env import FraudEnv
import collections

Action = collections.namedtuple('Action', ['sql'])

env = FraudEnv()
obs, info = env.reset()
print('reset OK')
obs2, r, term, trunc, info2 = env.step(Action(sql='SELECT * FROM accounts LIMIT 5'))
print('step reward:', r)
s = env.state()
print('state type:', type(s))
