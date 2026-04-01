# OpenEnv: Real-World AI Training Environment

## 📌 Project Overview
This project is a custom **OpenEnv** environment designed for Reinforcement Learning (RL). It follows the standard `gymnasium` API (`step`, `reset`, `render`), allowing any standard AI agent to interact with a real-world simulated logic engine.

The goal is to bridge the gap between abstract RL algorithms and practical, real-world constraints.

---

## 👥 Team & Roles

| Name | Role | Responsibilities |
| :--- | :--- | :--- |
| **@Teammate1** | **The Architect** | API Integration, `gym.Env` implementation, Observation/Action space definitions. |
| **@Teammate2** | **The Engine Room** | Core simulation logic, physics/math transitions, state management. |
| **@Teammate3** | **The Validator** | Reward function design, unit testing, and baseline agent benchmarking. |

---

## 🛠️ Getting Started

### 1. Installation
Clone the repository and install the environment in editable mode:
```bash
git clone [https://github.com/YOUR_USERNAME/openenv-project.git](https://github.com/YOUR_USERNAME/openenv-project.git)
cd openenv-project
pip install -e .
