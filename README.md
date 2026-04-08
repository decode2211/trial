---
title: Fraud Detection
emoji: 🔍
colorFrom: red
colorTo: blue
sdk: docker
pinned: false
tags:
  - openenv
---

# Financial Fraud Detection Environment (OpenEnv)

## 📌 Project Overview
This project provides a complete, compliant reinforcement learning environment for financial fraud detection based on the standard `gymnasium` API. It enables AI agents to interface with a simulated backend SQLite database containing `accounts` and `transactions`, aiming to detect fraudulent patterns through SQL querying. 

The environment natively integrates dense reward shaping and strict constraints, seamlessly bringing standard algorithms into a real-world, constrained setup.

---

## 📂 Project Structure

### Root Directory
- **`inference.py`**: The main execution engine. Runs a Groq-powered LLM agent (`llama-3.1-8b-instant`) interacting with the Gym environment to solve fraud detection tasks. Outputs deterministic logs (`[START]`, `[STEP]`, `[END]`).
- **`launch.py`**: Runner script that triggers `inference.py` and redirects output to `output.txt` for automated grading systems.
- **`test.py`**: A lightweight test script to verify environment resetting and basic interactions.
- **`openenv.yaml`**: Standardized environment definition outlining task metadata (difficulties, descriptions) and expected schema mapping.
- **`Dockerfile`**: Docker configuration packaging the environment and dependencies on a lightweight Python base image.
- **`requirements.txt`**: Standard dependencies list (`gymnasium`, `pydantic`, `openai`, `numpy`).
- **`setup.py`**: Standard packaging script to install the `fraud_detection` package as a local module.

### Core Modules: `fraud_detection/`
The main Python package exposing the environment logic, database mockups, and analytical tasks.

#### `fraud_detection/envs/`
- **`core_env.py`**: A `gymnasium.Env` subclass (`FraudEnv`) bridging API interactions. Manages textual SQL observation spaces, binary fraud signals, step-counts, and action processing. 
- **`engine.py`**: The core data engine (`FraudEngine`) managing direct connections to SQLite. Handles dense reward shaping rules (penalizing destructive SQL, rewarding valid tables and finding fraud indicators).

#### `fraud_detection/db/`
- **`fraud.db`**: Pre-seeded local SQLite database mapping synthetic accounts and transactional ledgers.
- **`seed.py`**: Script to dynamically regenerate or alter the initial database with seeded edge cases.

#### `fraud_detection/tasks/`
- **`tasks.py`**: Defines specific scenarios (`TASKS`) the model needs to solve, complete with grading criteria and prompt wrappers.

#### Empty Directories
- **`docs/`**: Reserved for further documentation.
- **`tests/`**: Reserved for expanded CI/CD unit testing.

---

## 🛠️ Getting Started

### 1. Installation
Clone the repository and install dependencies in an editable mode:

```bash
git clone <your-repo-url>
cd openenv-project
pip install -r requirements.txt
pip install -e .
```

### 2. Running Inference
The agent interacts with the Gym environment using standard completion models (configurable via environment variables `API_BASE_URL`, `MODEL_NAME`, `GROQ_API_KEY`, or `HF_TOKEN`).

```bash
python inference.py
```

Or run via the provided launch wrapper for direct execution and logging:
```bash
python launch.py
```

### 3. Docker Support
To run in an isolated environment simulating cloud testing:

```bash
docker build -t openenv-fraud .
docker run --rm openenv-fraud
```

---

## 👥 Team & Roles

| Name | Role | Responsibilities |
| :--- | :--- | :--- |
| **@Teammate1** | **The Architect** | API Integration, `gym.Env` implementation, Observation/Action space definitions. |
| **@Teammate2** | **The Engine Room** | Core simulation logic, `fraud.db` integration, physics/math transitions. |
| **@Teammate3** | **The Validator** | Reward function design, Groq LLM integration, baseline agent testing via `inference.py`. |
