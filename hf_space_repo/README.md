---
title: Fraud Detection OpenEnv
emoji: 🔍
colorFrom: red
colorTo: yellow
sdk: docker
app_port: 7860
pinned: false
tags:
  - openenv
  - reinforcement-learning
  - fraud-detection
  - gymnasium
  - sql
---

# 🔍 Financial Fraud Detection Environment (OpenEnv)

An OpenEnv-compliant reinforcement learning environment for training AI agents to detect financial fraud through SQL-based investigation.

## 🎯 What is this?

This environment simulates a real-world fraud detection scenario where an AI agent must analyze a financial database to identify fraudulent transactions and suspicious account patterns. It's designed for:

- Training reinforcement learning agents
- Evaluating LLM reasoning capabilities
- Testing SQL-based investigation strategies
- Benchmarking fraud detection approaches

## 🚀 Quick Start

### Interactive Web Interface
Use the Gradio interface above to:
1. Click **"Reset Environment"** to initialize
2. Enter SQL queries to investigate the database
3. View rewards and observations
4. Grade your performance on tasks

### Available Tables
- **accounts**: Account information (account_id, name, balance, failed_logins, created_at)
- **transactions**: Transaction records (transaction_id, source_account_id, dest_account_id, amount, type, timestamp)

### Example Queries

**EASY Task** - Find high-value transactions:
```sql
SELECT * FROM transactions 
WHERE amount > 10000 
AND timestamp >= DATE('now', '-30 days');
```

**MEDIUM Task** - Find suspicious accounts:
```sql
SELECT a.account_id, a.failed_logins, COUNT(t.transaction_id) as tx_count
FROM accounts a
JOIN transactions t ON a.account_id = t.source_account_id
WHERE a.failed_logins > 3
GROUP BY a.account_id
HAVING COUNT(t.transaction_id) > 10;
```

**HARD Task** - Reconstruct fraud chain:
```sql
SELECT * FROM transactions 
WHERE source_account_id IN ('A040', 'A041', 'A042', 'A043', 'A044')
AND dest_account_id IN ('A041', 'A042', 'A043', 'A044', 'A045')
ORDER BY timestamp;
```

## 📊 Environment Details

### Action Space
- **Type**: Text (SQL queries)
- **Constraints**: Max 500 characters, SELECT only
- **Description**: Raw SQL SELECT queries targeting the SQLite database

### Observation Space
- `sql_result`: Query results (string, max 1000 chars)
- `fraud_signals`: Binary fraud indicators (array[10])
- `step_count`: Current step number (0-50)

### Reward Function
Dense reward shaping with partial progress signals:
- **+0.3**: Valid query accessing relevant tables
- **+0.5**: Discovering new fraud markers (accounts A005, A010, A045)
- **+1.0**: Task completion bonus
- **-0.2**: Repeated queries (inefficiency penalty)
- **-0.4**: Destructive operations (DROP, DELETE, TRUNCATE)
- **Bounded**: All rewards clipped to [-1.0, 1.0]

## 📈 Tasks

| Task | Difficulty | Description | Expected Score |
|------|-----------|-------------|----------------|
| EASY | ⭐ | Find all transactions above $10,000 in the last 30 days | 0.85-0.95 |
| MEDIUM | ⭐⭐ | Identify accounts with >3 failed logins AND a transaction spike | 0.60-0.75 |
| HARD | ⭐⭐⭐ | Reconstruct a money laundering chain across 5+ transfer hops | 0.40-0.60 |

## 🔧 Programmatic Usage

```python
from fraud_detection.envs.core_env import FraudEnv

# Create environment
env = FraudEnv()
obs, info = env.reset()

# Execute a query
obs, reward, done, truncated, info = env.step(
    "SELECT * FROM accounts WHERE failed_logins > 3;"
)

print(f"Reward: {reward}")
print(f"Result: {obs['sql_result']}")

# Grade performance
from fraud_detection.tasks.tasks import TASKS
for task in TASKS:
    score = task.grader(env.state())
    print(f"{task.name}: {score:.2f}")
```

## 📦 Local Installation

```bash
# Clone the repository
git clone https://huggingface.co/spaces/adeline2211/winners
cd winners

# Install dependencies
pip install -r requirements.txt
pip install -e .

# Run the Gradio interface
python app.py
```

## 🐳 Docker

```bash
# Build the image
docker build -t fraud-detection .

# Run the container
docker run -p 7860:7860 fraud-detection
```

Then open http://localhost:7860

## 🎓 OpenEnv Compliance

This environment fully implements the OpenEnv specification:
- ✅ Typed Pydantic models (Observation, Action, Reward)
- ✅ Standard gymnasium.Env interface
- ✅ `step()`, `reset()`, `state()` methods
- ✅ `openenv.yaml` metadata file
- ✅ Programmatic graders with 0.0-1.0 scores
- ✅ Validated with `openenv validate`

## 🏆 Competition Features

- **Real-world utility**: Models actual fraud detection workflows
- **Progressive difficulty**: Three well-defined tasks
- **Dense rewards**: Partial progress signals guide learning
- **Deterministic grading**: Reproducible evaluation
- **Production-ready**: Docker, tests, comprehensive docs

## 🔗 Links

- [GitHub Repository](https://github.com/decode2211/winners)
- [OpenEnv Specification](https://github.com/openenv/openenv)
- [Gymnasium Documentation](https://gymnasium.farama.org/)

## 📄 License

MIT License

---

Built for the OpenEnv competition. Trains AI agents to detect financial fraud through SQL-based investigation of transaction patterns and account behaviors.
