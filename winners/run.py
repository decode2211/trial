#!/usr/bin/env python
"""
Unified runner script for the Fraud Detection OpenEnv environment.
Provides easy access to all common operations.
"""
import sys
import subprocess
import argparse


def run_tests():
    """Run the comprehensive test suite."""
    print("Running comprehensive test suite...")
    return subprocess.call([sys.executable, "fraud_detection/test_all.py"])


def run_validation():
    """Run pre-submission validation."""
    print("Running pre-submission validation...")
    return subprocess.call([sys.executable, "pre_submission_check.py"])


def run_inference():
    """Run the inference script."""
    print("Running inference script...")
    return subprocess.call([sys.executable, "inference.py"])


def run_mock_inference():
    """Run mock inference without API calls."""
    print("Running mock inference...")
    return subprocess.call([sys.executable, "test_inference_mock.py"])


def run_gradio():
    """Run the Gradio web interface."""
    print("Starting Gradio interface...")
    return subprocess.call([sys.executable, "app.py"])


def run_quick_test():
    """Run quick environment test."""
    print("Running quick test...")
    return subprocess.call([sys.executable, "test.py"])


def check_database():
    """Check database contents."""
    print("Checking database...")
    return subprocess.call([sys.executable, "check_db.py"])


def seed_database():
    """Reseed the database."""
    print("Reseeding database...")
    return subprocess.call([sys.executable, "fraud_detection/db/seed.py"])


def main():
    parser = argparse.ArgumentParser(
        description="Fraud Detection OpenEnv Runner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run.py test          # Run comprehensive tests
  python run.py validate      # Run pre-submission validation
  python run.py inference     # Run inference with LLM
  python run.py mock          # Run mock inference (no API)
  python run.py gradio        # Start Gradio interface
  python run.py quick         # Quick environment test
  python run.py db            # Check database contents
  python run.py seed          # Reseed database
        """
    )
    
    parser.add_argument(
        "command",
        choices=["test", "validate", "inference", "mock", "gradio", "quick", "db", "seed"],
        help="Command to run"
    )
    
    args = parser.parse_args()
    
    commands = {
        "test": run_tests,
        "validate": run_validation,
        "inference": run_inference,
        "mock": run_mock_inference,
        "gradio": run_gradio,
        "quick": run_quick_test,
        "db": check_database,
        "seed": seed_database,
    }
    
    exit_code = commands[args.command]()
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
