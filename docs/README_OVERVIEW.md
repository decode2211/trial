# Project README Overview

A summary of all README files found across this project.

---

## 1. `README.md` (Root)

The main project README for the Financial Fraud Detection Environment (OpenEnv). It covers the full project structure, explaining each file and module in the root directory and the `fraud_detection/` package. It walks through the core components: the gymnasium-based `FraudEnv`, the `FraudEngine` SQLite data layer, the pre-seeded `fraud.db`, task definitions, and the Groq-powered LLM inference agent. It also includes setup instructions (local install, running inference, Docker), and a team roles table describing the responsibilities of each contributor (Architect, Engine Room, Validator).

---

## 2. `hf_space_repo/README.md`

The README for the Hugging Face Space deployment of the project. It provides a user-facing description of the environment intended for the HF Spaces platform. It explains the interactive Gradio web interface, available database tables (`accounts`, `transactions`), example SQL queries for each difficulty level (EASY, MEDIUM, HARD), the full reward function breakdown, and task scoring expectations. It also covers programmatic usage via the `FraudEnv` API, local installation steps, Docker usage, and OpenEnv compliance checklist. Includes links to the GitHub repo and OpenEnv specification.

---

## 3. `winners/README.md`

A concise README targeting the winning submission version of the project, also formatted for Hugging Face Spaces. It summarizes the environment's purpose, the Gradio interface workflow, example SQL queries for all three task difficulties, action/observation space specs, the reward function, and task descriptions. Includes local install and Docker instructions, and links to the GitHub repo and OpenEnv spec. This is a streamlined version of the full HF Space README.

---

## 4. `winners/README_HF.md`

A Hugging Face-specific README variant within the `winners/` folder. It focuses on the environment's design for training RL agents and evaluating LLM reasoning. Covers the action/observation spaces, reward function, and all three tasks (EASY, MEDIUM, HARD) with plain-text descriptions rather than SQL examples. Notably includes a baseline performance table showing expected scores per task difficulty. Also covers programmatic access, inference runner usage with `GROQ_API_KEY`, installation, and Docker setup.

---

## 5. `winners/README_SPACE.md`

Another Hugging Face Space-oriented README in the `winners/` folder, nearly identical in structure to `winners/README.md`. It describes the interactive Gradio interface, provides the same three example SQL queries, documents the action/observation spaces and reward function, and lists the three tasks in a table. Includes local install, Docker instructions, and links. This file appears to be a deployment-ready copy intended for direct use as the Space's README.

---

*This file was auto-generated to provide a single reference point for all README documentation in the project.*
