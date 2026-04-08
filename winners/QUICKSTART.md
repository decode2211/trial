# Quick Start Guide

Get up and running with the Fraud Detection OpenEnv environment in 5 minutes.

## 🚀 Installation (2 minutes)

```bash
# Clone the repository
git clone https://github.com/decode2211/winners.git
cd winners

# Install dependencies
pip install -r requirements.txt
pip install -e .
```

## 🔑 Configuration (1 minute)

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your API key
# For Groq (recommended for testing):
GROQ_API_KEY=your_groq_api_key_here
MODEL_NAME=llama-3.1-8b-instant
```

Get a free Groq API key at: https://console.groq.com/

## ✅ Verify Installation (1 minute)

```bash
# Run the test suite
python fraud_detection/test_all.py
```

Expected output:
```
============================================================
FRAUD DETECTION ENVIRONMENT TEST SUITE
============================================================
...
Total: 8/8 tests passed
🎉 All tests passed! Environment is ready for deployment.
```

## 🎮 Try It Out (1 minute)

### Option 1: Interactive Gradio Interface

```bash
python app.py
```

Then open http://localhost:7860 in your browser.

### Option 2: Run Inference Script

```bash
python inference.py
```

Expected output:
```
[START] task=EASY model=llama-3.1-8b-instant
[STEP]  step=1 action=SELECT * FROM transactions... reward=0.3 done=False
[END]   total_reward=2.4 steps=15 score=0.85
```

### Option 3: Python API

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
```

## 📊 Example Queries

### Easy Task: High-Value Transactions
```sql
SELECT * FROM transactions 
WHERE amount > 10000 
AND timestamp >= DATE('now', '-30 days');
```

### Medium Task: Suspicious Accounts
```sql
SELECT a.account_id, a.failed_logins, COUNT(t.transaction_id) as tx_count
FROM accounts a
JOIN transactions t ON a.account_id = t.source_account_id
WHERE a.failed_logins > 3
GROUP BY a.account_id
HAVING COUNT(t.transaction_id) > 10;
```

### Hard Task: Fraud Chain
```sql
SELECT * FROM transactions 
WHERE source_account_id IN ('A040', 'A041', 'A042', 'A043', 'A044')
AND dest_account_id IN ('A041', 'A042', 'A043', 'A044', 'A045')
ORDER BY timestamp;
```

## 🐳 Docker Quick Start

```bash
# Build the image
docker build -t fraud-detection .

# Run with Gradio interface
docker run -p 7860:7860 -e GROQ_API_KEY=your_key fraud-detection

# Or run inference
docker run --rm -e GROQ_API_KEY=your_key fraud-detection python inference.py
```

## 📚 Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Check [DEPLOYMENT.md](DEPLOYMENT.md) for deployment instructions
- Explore the [fraud_detection/](fraud_detection/) package
- Customize tasks in [fraud_detection/tasks/tasks.py](fraud_detection/tasks/tasks.py)
- Modify rewards in [fraud_detection/envs/engine.py](fraud_detection/envs/engine.py)

## 🆘 Troubleshooting

### Issue: "No module named 'fraud_detection'"
**Solution**: Run `pip install -e .` in the project root.

### Issue: "Database not found"
**Solution**: The database should be at `fraud_detection/db/fraud.db`. If missing, run:
```bash
python fraud_detection/db/seed.py
```

### Issue: "API key not set"
**Solution**: Ensure your `.env` file has the correct API key:
```bash
cat .env  # Check the file contents
```

### Issue: Tests fail
**Solution**: Reinstall dependencies:
```bash
pip install -r requirements.txt --force-reinstall
pip install -e .
```

## 💡 Tips

1. **Start with the EASY task** to understand the environment
2. **Use LIMIT clauses** to avoid overwhelming output
3. **Check the reward** after each query to guide your exploration
4. **Grade frequently** to track your progress
5. **Read the database schema** in the README

## 🎯 Goals

Try to achieve these scores:
- EASY: 0.90+ (should be straightforward)
- MEDIUM: 0.65+ (requires JOIN and aggregation)
- HARD: 0.70+ (needs multi-step reasoning)

Good luck! 🚀
