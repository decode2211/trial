# How to Run the Fraud Detection OpenEnv Environment

This guide provides step-by-step instructions for running the environment in various ways.

## 🚀 Quick Start (5 minutes)

### 1. Install Dependencies

```bash
pip install -r requirements.txt
pip install -e .
```

### 2. Configure API Key

Create a `.env` file:
```bash
cp .env.example .env
```

Edit `.env` and add your API key:
```env
GROQ_API_KEY=your_groq_api_key_here
MODEL_NAME=llama-3.1-8b-instant
```

Get a free Groq API key at: https://console.groq.com/

### 3. Run Tests

```bash
python run.py test
```

Expected output:
```
Total: 8/8 tests passed
🎉 All tests passed!
```

### 4. Run Inference

```bash
python run.py inference
```

## 📋 All Available Commands

### Using the run.py Script

```bash
# Run comprehensive test suite
python run.py test

# Run pre-submission validation
python run.py validate

# Run inference with LLM
python run.py inference

# Run mock inference (no API key needed)
python run.py mock

# Start Gradio web interface
python run.py gradio

# Quick environment test
python run.py quick

# Check database contents
python run.py db

# Reseed database
python run.py seed
```

### Direct Script Execution

```bash
# Test suite
python fraud_detection/test_all.py

# Validation
python pre_submission_check.py

# Inference
python inference.py

# Mock inference
python test_inference_mock.py

# Gradio interface
python app.py

# Quick test
python test.py

# Database check
python check_db.py

# Database seeding
python fraud_detection/db/seed.py
```

## 🐳 Docker Commands

### Build the Image

```bash
docker build -t fraud-detection-env .
```

### Run Gradio Interface

```bash
docker run -p 7860:7860 \
  -e GROQ_API_KEY=your_key_here \
  fraud-detection-env
```

Then open http://localhost:7860

### Run Inference

```bash
docker run --rm \
  -e GROQ_API_KEY=your_key_here \
  fraud-detection-env \
  python inference.py
```

### Run Tests

```bash
docker run --rm fraud-detection-env python fraud_detection/test_all.py
```

### Run Validation

```bash
docker run --rm fraud-detection-env python pre_submission_check.py
```

### Interactive Shell

```bash
docker run -it --rm fraud-detection-env /bin/bash
```

## 🎮 Interactive Usage

### Gradio Web Interface

1. Start the interface:
```bash
python app.py
```

2. Open http://localhost:7860 in your browser

3. Click "Reset Environment"

4. Enter SQL queries like:
```sql
SELECT * FROM accounts WHERE failed_logins > 3;
```

5. Click "Execute Query" to see results and rewards

6. Select a task and click "Grade Current State" to see your score

### Python API

```python
from fraud_detection.envs.core_env import FraudEnv

# Create environment
env = FraudEnv()

# Reset
obs, info = env.reset()
print(f"Initial observation: {obs}")

# Execute queries
queries = [
    "SELECT * FROM accounts LIMIT 5;",
    "SELECT * FROM transactions WHERE amount > 10000;",
    "SELECT * FROM accounts WHERE failed_logins > 3;"
]

for query in queries:
    obs, reward, done, truncated, info = env.step(query)
    print(f"\nQuery: {query}")
    print(f"Reward: {reward}")
    print(f"Result preview: {obs['sql_result'][:100]}...")
    
    if done or truncated:
        break

# Get final state
state = env.state()
print(f"\nFinal state: {state}")
```

### With Task Grading

```python
from fraud_detection.envs.core_env import FraudEnv
from fraud_detection.tasks.tasks import TASKS

env = FraudEnv()

for task in TASKS:
    print(f"\n=== Task: {task.name} ===")
    print(f"Description: {task.description}")
    
    env.reset()
    
    # Your solution query here
    query = "SELECT * FROM transactions WHERE amount > 10000;"
    obs, reward, done, truncated, info = env.step(query)
    
    # Grade the result
    score = task.grader(env.state())
    print(f"Score: {score:.2f}")
```

## 🧪 Testing Scenarios

### Test Individual Tasks

```python
from fraud_detection.envs.core_env import FraudEnv
from fraud_detection.tasks.tasks import easy_task, medium_task, hard_task

env = FraudEnv()

# Test EASY task
env.reset()
env.step("SELECT * FROM transactions WHERE amount > 10000 AND timestamp >= DATE('now', '-30 days');")
print(f"EASY score: {easy_task.grader(env.state())}")

# Test MEDIUM task
env.reset()
env.step("SELECT a.account_id FROM accounts a JOIN transactions t ON a.account_id = t.source_account_id WHERE a.failed_logins > 3 GROUP BY a.account_id HAVING COUNT(t.transaction_id) > 10;")
print(f"MEDIUM score: {medium_task.grader(env.state())}")

# Test HARD task
env.reset()
env.step("SELECT * FROM transactions WHERE source_account_id IN ('A040', 'A041', 'A042', 'A043', 'A044') AND dest_account_id IN ('A041', 'A042', 'A043', 'A044', 'A045') ORDER BY timestamp;")
print(f"HARD score: {hard_task.grader(env.state())}")
```

### Test Reward Function

```python
from fraud_detection.envs.core_env import FraudEnv

env = FraudEnv()
env.reset()

test_cases = [
    ("Valid query", "SELECT * FROM accounts LIMIT 1;"),
    ("Destructive query", "DROP TABLE accounts;"),
    ("Repeated query", "SELECT * FROM accounts LIMIT 1;"),
    ("Fraud marker discovery", "SELECT * FROM accounts WHERE account_id = 'A005';"),
]

for name, query in test_cases:
    obs, reward, done, truncated, info = env.step(query)
    print(f"{name}: reward = {reward}")
```

## 🔍 Debugging

### Check Environment State

```python
from fraud_detection.envs.core_env import FraudEnv

env = FraudEnv(render_mode="human")
env.reset()
env.step("SELECT * FROM accounts LIMIT 5;")
```

Output:
```
--- FraudState Summary ---
Step: 1
Result length: 627
Fraud Signals: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
--------------------------
```

### Inspect Database

```bash
python check_db.py
```

Or use SQLite directly:
```bash
sqlite3 fraud_detection/db/fraud.db
```

```sql
-- Check tables
.tables

-- Check accounts
SELECT * FROM accounts LIMIT 5;

-- Check transactions
SELECT * FROM transactions LIMIT 5;

-- Check high-value transactions
SELECT COUNT(*) FROM transactions WHERE amount > 10000;
```

### View Logs

For inference:
```bash
python inference.py 2>&1 | tee output.log
```

For Docker:
```bash
docker logs <container_id>
```

## 🎯 Example Workflows

### Workflow 1: Development Testing

```bash
# 1. Make changes to code
vim fraud_detection/envs/engine.py

# 2. Run quick test
python run.py quick

# 3. Run full test suite
python run.py test

# 4. Run validation
python run.py validate
```

### Workflow 2: Task Development

```bash
# 1. Modify tasks
vim fraud_detection/tasks/tasks.py

# 2. Test with mock inference
python run.py mock

# 3. Check database
python run.py db

# 4. Run full tests
python run.py test
```

### Workflow 3: Deployment Preparation

```bash
# 1. Run all tests
python run.py test

# 2. Run validation
python run.py validate

# 3. Build Docker image
docker build -t fraud-detection-env .

# 4. Test Docker image
docker run --rm fraud-detection-env python fraud_detection/test_all.py

# 5. Test inference in Docker
docker run --rm -e GROQ_API_KEY=$GROQ_API_KEY fraud-detection-env python inference.py
```

## 🚨 Troubleshooting

### Issue: Module not found

```bash
# Solution: Reinstall package
pip install -e .
```

### Issue: Database not found

```bash
# Solution: Check database exists
ls -la fraud_detection/db/fraud.db

# If missing, reseed
python run.py seed
```

### Issue: API key error

```bash
# Solution: Check environment variable
echo $GROQ_API_KEY

# Or check .env file
cat .env
```

### Issue: Tests fail

```bash
# Solution: Clean and reinstall
pip uninstall fraud_detection -y
pip install -e .
python run.py test
```

### Issue: Docker build fails

```bash
# Solution: Clean Docker cache
docker system prune -a
docker build --no-cache -t fraud-detection-env .
```

## 📊 Performance Monitoring

### Measure Inference Time

```bash
time python inference.py
```

### Monitor Resource Usage

```bash
# CPU and memory
docker stats

# Or with Python
python -c "import psutil; print(f'CPU: {psutil.cpu_percent()}%, Memory: {psutil.virtual_memory().percent}%')"
```

## 🎓 Learning Path

1. **Start here**: Run `python run.py quick` to verify setup
2. **Explore**: Use Gradio interface (`python run.py gradio`)
3. **Understand**: Read the code in `fraud_detection/envs/`
4. **Experiment**: Try different SQL queries
5. **Challenge**: Solve all three tasks
6. **Extend**: Add new tasks or fraud patterns
7. **Deploy**: Build Docker and deploy to HF Spaces

## 📚 Additional Resources

- [README.md](README.md) - Full documentation
- [QUICKSTART.md](QUICKSTART.md) - Quick start guide
- [DEPLOYMENT.md](DEPLOYMENT.md) - Deployment instructions
- [SUBMISSION_SUMMARY.md](SUBMISSION_SUMMARY.md) - Competition summary

## 🆘 Getting Help

If you encounter issues:
1. Check this guide
2. Review error messages carefully
3. Run validation: `python run.py validate`
4. Check GitHub issues
5. Review OpenEnv documentation

Good luck! 🚀
