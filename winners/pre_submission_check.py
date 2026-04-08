"""
Pre-submission validation script.
Checks all competition requirements before submission.
"""
import sys
import os
import subprocess
import json
from pathlib import Path


def print_header(text):
    """Print a formatted header."""
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60)


def print_check(name, passed, details=""):
    """Print a check result."""
    status = "✓ PASS" if passed else "✗ FAIL"
    print(f"{status}: {name}")
    if details:
        print(f"       {details}")
    return passed


def check_file_exists(filepath):
    """Check if a file exists."""
    return Path(filepath).exists()


def check_required_files():
    """Check that all required files exist."""
    print_header("Required Files Check")
    
    required_files = [
        "inference.py",
        "openenv.yaml",
        "Dockerfile",
        "requirements.txt",
        "setup.py",
        "README.md",
        "fraud_detection/__init__.py",
        "fraud_detection/envs/core_env.py",
        "fraud_detection/envs/engine.py",
        "fraud_detection/envs/models.py",
        "fraud_detection/tasks/tasks.py",
        "fraud_detection/db/fraud.db",
    ]
    
    all_passed = True
    for filepath in required_files:
        exists = check_file_exists(filepath)
        all_passed &= print_check(filepath, exists)
    
    return all_passed


def check_environment_variables():
    """Check that required environment variables are documented."""
    print_header("Environment Variables Check")
    
    required_vars = ["API_BASE_URL", "MODEL_NAME", "HF_TOKEN"]
    
    # Check if they're documented in README
    with open("README.md", "r", encoding="utf-8") as f:
        readme_content = f.read()
    
    all_passed = True
    for var in required_vars:
        documented = var in readme_content
        all_passed &= print_check(
            f"{var} documented",
            documented,
            "Found in README" if documented else "Not found in README"
        )
    
    return all_passed


def check_openenv_spec():
    """Check OpenEnv specification compliance."""
    print_header("OpenEnv Specification Check")
    
    # Check openenv.yaml exists and is valid
    if not check_file_exists("openenv.yaml"):
        print_check("openenv.yaml exists", False)
        return False
    
    with open("openenv.yaml", "r") as f:
        import yaml
        try:
            spec = yaml.safe_load(f)
            print_check("openenv.yaml is valid YAML", True)
        except Exception as e:
            print_check("openenv.yaml is valid YAML", False, str(e))
            return False
    
    # Check required fields
    required_fields = ["name", "version", "description", "action_space", "observation_space", "entrypoint"]
    all_passed = True
    for field in required_fields:
        exists = field in spec
        all_passed &= print_check(f"Field '{field}' present", exists)
    
    return all_passed


def check_tasks():
    """Check that tasks are properly defined."""
    print_header("Tasks Check")
    
    try:
        from fraud_detection.tasks.tasks import TASKS
        
        all_passed = True
        all_passed &= print_check("Tasks imported successfully", True)
        all_passed &= print_check(
            "At least 3 tasks defined",
            len(TASKS) >= 3,
            f"Found {len(TASKS)} tasks"
        )
        
        for task in TASKS:
            has_name = hasattr(task, 'name')
            has_description = hasattr(task, 'description')
            has_grader = hasattr(task, 'grader')
            
            all_passed &= print_check(
                f"Task {task.name if has_name else 'UNKNOWN'}",
                has_name and has_description and has_grader,
                f"name={has_name}, description={has_description}, grader={has_grader}"
            )
        
        return all_passed
    except Exception as e:
        print_check("Tasks import", False, str(e))
        return False


def check_graders():
    """Check that graders work correctly."""
    print_header("Graders Check")
    
    try:
        from fraud_detection.envs.core_env import FraudEnv
        from fraud_detection.tasks.tasks import TASKS
        
        env = FraudEnv()
        env.reset()
        env.step("SELECT * FROM accounts LIMIT 1;")
        state = env.state()
        
        all_passed = True
        for task in TASKS:
            try:
                score = task.grader(state)
                in_range = 0.0 <= score <= 1.0
                all_passed &= print_check(
                    f"Grader for {task.name}",
                    in_range,
                    f"Score: {score:.2f}"
                )
            except Exception as e:
                all_passed &= print_check(f"Grader for {task.name}", False, str(e))
        
        return all_passed
    except Exception as e:
        print_check("Graders test", False, str(e))
        return False


def check_reward_bounds():
    """Check that rewards are properly bounded."""
    print_header("Reward Bounds Check")
    
    try:
        from fraud_detection.envs.core_env import FraudEnv
        
        env = FraudEnv()
        env.reset()
        
        test_queries = [
            "SELECT * FROM accounts LIMIT 1;",
            "SELECT * FROM transactions LIMIT 1;",
            "DROP TABLE accounts;",
            "SELECT * FROM accounts WHERE account_id = 'A005';",
        ]
        
        all_passed = True
        for query in test_queries:
            obs, reward, done, truncated, info = env.step(query)
            in_bounds = -1.0 <= reward <= 1.0
            all_passed &= print_check(
                f"Reward for '{query[:30]}...'",
                in_bounds,
                f"Reward: {reward:.2f}"
            )
        
        return all_passed
    except Exception as e:
        print_check("Reward bounds test", False, str(e))
        return False


def check_inference_script():
    """Check that inference.py has correct structure."""
    print_header("Inference Script Check")
    
    if not check_file_exists("inference.py"):
        print_check("inference.py exists", False)
        return False
    
    with open("inference.py", "r") as f:
        content = f.read()
    
    all_passed = True
    
    # Check for required imports
    all_passed &= print_check("Imports openai", "import openai" in content or "from openai" in content)
    all_passed &= print_check("Imports FraudEnv", "FraudEnv" in content)
    all_passed &= print_check("Imports TASKS", "TASKS" in content)
    
    # Check for required log format
    all_passed &= print_check("Has [START] log", "[START]" in content)
    all_passed &= print_check("Has [STEP] log", "[STEP]" in content)
    all_passed &= print_check("Has [END] log", "[END]" in content)
    
    # Check for environment variable usage
    all_passed &= print_check("Uses API_BASE_URL", "API_BASE_URL" in content)
    all_passed &= print_check("Uses MODEL_NAME", "MODEL_NAME" in content)
    
    return all_passed


def check_dockerfile():
    """Check that Dockerfile is properly configured."""
    print_header("Dockerfile Check")
    
    if not check_file_exists("Dockerfile"):
        print_check("Dockerfile exists", False)
        return False
    
    with open("Dockerfile", "r") as f:
        content = f.read()
    
    all_passed = True
    all_passed &= print_check("Has FROM instruction", "FROM" in content)
    all_passed &= print_check("Installs requirements", "requirements.txt" in content)
    all_passed &= print_check("Installs package", "pip install -e" in content or "pip install ." in content)
    all_passed &= print_check("Has CMD instruction", "CMD" in content)
    
    return all_passed


def check_documentation():
    """Check that documentation is comprehensive."""
    print_header("Documentation Check")
    
    if not check_file_exists("README.md"):
        print_check("README.md exists", False)
        return False
    
    with open("README.md", "r", encoding="utf-8") as f:
        content = f.read()
    
    all_passed = True
    
    required_sections = [
        ("Environment description", "Environment" in content or "Overview" in content),
        ("Action space", "Action Space" in content or "action_space" in content),
        ("Observation space", "Observation Space" in content or "observation_space" in content),
        ("Task descriptions", "Task" in content or "EASY" in content),
        ("Setup instructions", "Installation" in content or "Setup" in content or "Getting Started" in content),
        ("Usage instructions", "Usage" in content or "Running" in content),
    ]
    
    for section_name, check in required_sections:
        all_passed &= print_check(section_name, check)
    
    return all_passed


def run_all_checks():
    """Run all validation checks."""
    print("\n" + "="*60)
    print("  PRE-SUBMISSION VALIDATION")
    print("="*60)
    
    checks = [
        ("Required Files", check_required_files),
        ("Environment Variables", check_environment_variables),
        ("OpenEnv Specification", check_openenv_spec),
        ("Tasks", check_tasks),
        ("Graders", check_graders),
        ("Reward Bounds", check_reward_bounds),
        ("Inference Script", check_inference_script),
        ("Dockerfile", check_dockerfile),
        ("Documentation", check_documentation),
    ]
    
    results = []
    for name, check_func in checks:
        try:
            passed = check_func()
            results.append((name, passed))
        except Exception as e:
            print(f"\n✗ {name} check crashed: {e}")
            import traceback
            traceback.print_exc()
            results.append((name, False))
    
    # Summary
    print_header("VALIDATION SUMMARY")
    
    passed_count = sum(1 for _, passed in results if passed)
    total_count = len(results)
    
    for name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status}: {name}")
    
    print(f"\nTotal: {passed_count}/{total_count} checks passed")
    
    if passed_count == total_count:
        print("\n🎉 All validation checks passed!")
        print("Your environment is ready for submission.")
        return 0
    else:
        print(f"\n⚠️  {total_count - passed_count} check(s) failed.")
        print("Please fix the issues before submitting.")
        return 1


if __name__ == "__main__":
    try:
        exit_code = run_all_checks()
        sys.exit(exit_code)
    except Exception as e:
        print(f"\n✗ Validation crashed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
