---
title: Fraud Detection OpenEnv
emoji: 🔍
colorFrom: red
colorTo: orange
sdk: docker
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

This environment simulates a real-world fraud detection scenario where an AI agent must analyze a financial database to identify fraudulent transactions and suspicious account patterns. It's designed for:

- Training reinforcement learning agents
- Evaluating LLM reasoning capabilities
- Testing SQL-based investigation strategies
- Benchmarking fraud detection approaches

## 🏗️ Environment Details

### Action Space
- **Type**: Text (SQL queries)
- **Description**: SELECT queries against accounts and transactions tables
- **Constraints**: Max 500 characters, no destructive operations

### Observation Space
- `sql_result`: Query results (string, max 1000 chars)
- `fraud_signals`: Binary fraud indicators (array[10])
- `step_count`: Current step (0-50)

### Reward Function
- +0.3: Valid query accessing relevant tables
- +0.5: Discovering new fraud markers
- +1.0: Task completion bonus
- -0.2: Repeated queries
- -0.4: Destructive operations

## 📊 Tasks

### EASY: High-Value Transactions
Find all transactions above $10,000 in the last 30 days.

### MEDIUM: Suspicious Accounts
Identify accounts with >3 failed logins AND a transaction spike.

### HARD: Fraud Chain Reconstruction
Reconstruct a money laundering chain across 5+ transfer hops.

## 🚀 Usage

### Interactive Web Interface
Use the Gradio interface above to:
1. Reset the environment
2. Execute SQL queries
3. View rewards and observations
4. Grade your performance

### Programmatic Access

```python
from fraud_detection.envs.core_env import FraudEnv

env = FraudEnv()
obs, info = env.reset()

# Execute a query
obs, reward, done, truncated, info = env.step(
    "SELECT * FROM accounts WHERE failed_logins > 3;"
)
```

### Running Inference

```bash
# Set your API key
export GROQ_API_KEY=your_key_here

# Run the baseline agent
python inference.py
```

## 📦 Installation

```bash
git clone https://huggingface.co/spaces/YOUR_USERNAME/fraud-detection
cd fraud-detection
pip install -r requirements.txt
pip install -e .
```

## 🐳 Docker

```bash
docker build -t fraud-detection .
docker run -p 7860:7860 fraud-detection
```

## 📈 Baseline Performance

| Task | Difficulty | Baseline Score |
|------|-----------|----------------|
| EASY | ⭐ | 0.90 |
| MEDIUM | ⭐⭐ | 0.65 |
| HARD | ⭐⭐⭐ | 0.42 |

## 🔗 Links

- [GitHub Repository](https://github.com/decode2211/winners)
- [OpenEnv Specification](https://github.com/openenv/openenv)
- [Documentation](./README.md)

## 📄 License

MIT License
