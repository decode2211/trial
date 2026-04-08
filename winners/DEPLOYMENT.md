# Deployment Guide

This guide covers deploying the Fraud Detection OpenEnv environment to Hugging Face Spaces and running it locally.

## 📋 Pre-Deployment Checklist

Before deploying, ensure all requirements are met:

- [x] Environment implements full OpenEnv spec
- [x] 3+ tasks with programmatic graders (EASY, MEDIUM, HARD)
- [x] Rewards bounded to [0.0, 1.0] range
- [x] Dockerfile builds successfully
- [x] inference.py runs without errors
- [x] Structured logs ([START], [STEP], [END])
- [x] Runtime < 20 minutes
- [x] Compatible with 2 vCPU, 8GB RAM

## 🚀 Deploying to Hugging Face Spaces

### Step 1: Create a Hugging Face Space

1. Go to https://huggingface.co/spaces
2. Click "Create new Space"
3. Fill in the details:
   - **Name**: `fraud-detection-openenv` (or your preferred name)
   - **License**: MIT
   - **SDK**: Docker
   - **Hardware**: CPU basic (free tier works)
4. Add the `openenv` tag in Space settings

### Step 2: Configure Secrets

In your Space settings, add the following secrets:

```
GROQ_API_KEY=your_groq_api_key_here
MODEL_NAME=llama-3.1-8b-instant
```

Or for OpenAI:
```
OPENAI_API_KEY=your_openai_api_key_here
MODEL_NAME=gpt-4o-mini
```

Or for custom API:
```
API_BASE_URL=https://your-api-endpoint.com/v1
MODEL_NAME=your-model-name
HF_TOKEN=your_token_here
```

### Step 3: Push Code to Space

```bash
# Clone your Space repository
git clone https://huggingface.co/spaces/YOUR_USERNAME/fraud-detection-openenv
cd fraud-detection-openenv

# Copy all files from this project
cp -r /path/to/winners/* .

# Rename README_HF.md to README.md for Space
mv README_HF.md README.md

# Commit and push
git add .
git commit -m "Initial deployment"
git push
```

### Step 4: Verify Deployment

1. Wait for the Space to build (5-10 minutes)
2. Check the build logs for errors
3. Once running, test the Gradio interface
4. Verify the environment responds to queries

### Step 5: Test API Endpoint

```bash
# Test reset endpoint
curl -X POST https://YOUR_USERNAME-fraud-detection-openenv.hf.space/reset

# Test step endpoint
curl -X POST https://YOUR_USERNAME-fraud-detection-openenv.hf.space/step \
  -H "Content-Type: application/json" \
  -d '{"action": "SELECT * FROM accounts LIMIT 5;"}'
```

## 🐳 Local Docker Deployment

### Build the Docker Image

```bash
docker build -t fraud-detection-env .
```

### Run with Gradio Interface

```bash
docker run -p 7860:7860 \
  -e GROQ_API_KEY=your_key_here \
  fraud-detection-env
```

Then open http://localhost:7860 in your browser.

### Run Inference Script

```bash
docker run --rm \
  -e GROQ_API_KEY=your_key_here \
  fraud-detection-env \
  python inference.py
```

### Run with Custom Command

```bash
docker run --rm \
  -e GROQ_API_KEY=your_key_here \
  fraud-detection-env \
  python fraud_detection/test_all.py
```

## 🧪 Local Development Setup

### Install Dependencies

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -e .
```

### Configure Environment

```bash
# Copy example env file
cp .env.example .env

# Edit .env with your API keys
nano .env  # or use your preferred editor
```

### Run Tests

```bash
# Run comprehensive test suite
python fraud_detection/test_all.py

# Run quick environment test
python test.py

# Run mock inference test
python test_inference_mock.py

# Validate OpenEnv compliance
python validate.py
```

### Run Inference

```bash
# Run with your API key
python inference.py

# Or use launch wrapper
python launch.py
```

### Run Gradio Interface

```bash
python app.py
```

## 📊 Monitoring and Debugging

### Check Logs

For Hugging Face Spaces:
1. Go to your Space page
2. Click on "Logs" tab
3. Monitor real-time output

For Docker:
```bash
# View logs
docker logs <container_id>

# Follow logs
docker logs -f <container_id>
```

### Common Issues

#### Issue: Docker build fails
**Solution**: Ensure you have enough disk space and Docker is up to date.

```bash
docker system prune -a
docker pull python:3.10-slim
```

#### Issue: API key not working
**Solution**: Verify the key is set correctly in environment variables.

```bash
# Check if key is set
echo $GROQ_API_KEY

# Test API connection
curl https://api.groq.com/openai/v1/models \
  -H "Authorization: Bearer $GROQ_API_KEY"
```

#### Issue: Database not found
**Solution**: Ensure the database is included in the Docker image.

```bash
# Check if database exists
docker run --rm fraud-detection-env ls -la fraud_detection/db/
```

#### Issue: Inference timeout
**Solution**: Reduce max_steps or use a faster model.

```python
# In core_env.py, reduce max_steps
self.max_steps = 30  # Instead of 50
```

## 🔧 Configuration Options

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `API_BASE_URL` | LLM API endpoint | Auto-detected |
| `MODEL_NAME` | Model identifier | `llama-3.1-8b-instant` |
| `GROQ_API_KEY` | Groq API key | None |
| `OPENAI_API_KEY` | OpenAI API key | None |
| `HF_TOKEN` | Hugging Face token | None |
| `GRADIO_SERVER_NAME` | Gradio server host | `0.0.0.0` |
| `GRADIO_SERVER_PORT` | Gradio server port | `7860` |

### Dockerfile Customization

To use a different Python version:
```dockerfile
FROM python:3.11-slim
```

To add more dependencies:
```dockerfile
RUN pip install --no-cache-dir additional-package
```

To change the default command:
```dockerfile
CMD ["python", "your_script.py"]
```

## 📈 Performance Optimization

### Reduce Docker Image Size

```dockerfile
# Use multi-stage build
FROM python:3.10-slim as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user -r requirements.txt

FROM python:3.10-slim
COPY --from=builder /root/.local /root/.local
COPY . /app
WORKDIR /app
```

### Speed Up Inference

1. Use a faster model (e.g., `llama-3.1-8b-instant` instead of `gpt-4`)
2. Reduce `max_tokens` in inference.py
3. Set `temperature=0.0` for deterministic results
4. Cache API responses for repeated queries

### Optimize Database Queries

The database is small (50 accounts, 300+ transactions), so performance should be good. For larger databases:

1. Add indexes:
```sql
CREATE INDEX idx_amount ON transactions(amount);
CREATE INDEX idx_timestamp ON transactions(timestamp);
```

2. Use query limits:
```sql
SELECT * FROM transactions LIMIT 100;
```

## 🎯 Competition Submission

### Required Files

Ensure these files are present:
- `inference.py` - Main inference script
- `openenv.yaml` - Environment specification
- `Dockerfile` - Container configuration
- `requirements.txt` - Python dependencies
- `setup.py` - Package installation
- `README.md` - Documentation
- `fraud_detection/` - Main package

### Validation

Run the pre-submission validation:
```bash
python validate.py
```

Expected output:
```
Running: openenv validate fraud_detection/envs/core_env.py:FraudEnv
✓ Environment is OpenEnv compliant
Exit code: 0
```

### Log Format Verification

Ensure logs match the required format:
```
[START] task=EASY model=llama-3.1-8b-instant
[STEP]  step=1 action=SELECT ... reward=0.3 done=False
[END]   total_reward=2.4 steps=15 score=0.85
```

### Final Checklist

- [ ] All tests pass (`python fraud_detection/test_all.py`)
- [ ] Docker builds successfully (`docker build -t test .`)
- [ ] Inference runs without errors (`python inference.py`)
- [ ] Logs follow exact format
- [ ] Runtime < 20 minutes
- [ ] HF Space deploys and responds
- [ ] README is comprehensive
- [ ] All required variables documented

## 🆘 Support

If you encounter issues:

1. Check the [GitHub Issues](https://github.com/decode2211/winners/issues)
2. Review [OpenEnv Documentation](https://github.com/openenv/openenv)
3. Consult [Gymnasium Docs](https://gymnasium.farama.org/)
4. Ask in the competition Discord/forum

## 📝 License

MIT License - see LICENSE file for details.
