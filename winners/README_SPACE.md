---
title: Fraud Detection OpenEnv
emoji: 🔍
colorFrom: red
colorTo: orange
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

# Financial Fraud Detection Environment (OpenEnv)

An OpenEnv-compliant reinforcement learning environment for training AI agents to detect financial fraud through SQL-based investigation.

## 🎯 What is this?

This environment simulates a real-world fraud detection scenario where an AI agent must analyze a financial database to identify fraudulent transactions and suspicious account patterns.

## 🚀 Quick Start

### Interactive Web Interface
Use the Gradio interface above to:
1. Click "Reset Environment" to initialize
2. Enter SQL queries to investigate the database
3. View rewards and observations
4. Grade your performance on tasks

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

### Observation Space
- `sql_result`: Query results (string)
- `fraud_signals`: Binary fraud indicators (array[10])
- `step_count`: Current step (0-50)

### Reward Function
- +0.3: Valid query accessing relevant tables
- +0.5: Discovering new fraud markers
- +1.0: Task completion bonus
- -0.2: Repeated queries
- -0.4: Destructive operations

## 📈 Tasks

| Task | Difficulty | Description |
|------|-----------|-------------|
| EASY | ⭐ | Find all transactions above $10,000 in the last 30 days |
| MEDIUM | ⭐⭐ | Identify accounts with >3 failed logins AND a transaction spike |
| HARD | ⭐⭐⭐ | Reconstruct a money laundering chain across 5+ transfer hops |

## 🔧 Programmatic Usage

```python
from fraud_detection.envs.core_env import FraudEnv

env = FraudEnv()
obs, info = env.reset()

# Execute a query
obs, reward, done, truncated, info = env.step(
    "SELECT * FROM accounts WHERE failed_logins > 3;"
)

print(f"Reward: {reward}")
print(f"Result: {obs['sql_result']}")
```

## 📦 Local Installation

```bash
git clone https://huggingface.co/spaces/YOUR_USERNAME/fraud-detection-openenv
cd fraud-detection-openenv
pip install -r requirements.txt
pip install -e .
python app.py
```

## 🐳 Docker

```bash
docker build -t fraud-detection .
docker run -p 7860:7860 fraud-detection
```

## 🔗 Links

- [GitHub Repository](https://github.com/decode2211/winners)
- [OpenEnv Specification](https://github.com/openenv/openenv)
- [Full Documentation](./README.md)

## 📄 License

MIT License
