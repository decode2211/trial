from typing import List, Set, Any
import numpy as np
import sqlite3
import os
import re

def _build_medium_truth() -> set:
    db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "db", "fraud.db")
    conn = sqlite3.connect(db_path)
    rows = conn.execute("""
        SELECT a.account_id FROM accounts a
        JOIN transactions t ON a.account_id = t.source_account_id
        WHERE a.failed_logins > 3
        GROUP BY a.account_id
        HAVING MAX(t.amount) > 5000
    """).fetchall()
    conn.close()
    return {r[0] for r in rows}

MEDIUM_TRUTH = _build_medium_truth()

# We define these classes to meet the requirements of ProgrammaticGrader, 
# assuming OpenEnv's standard interface if available, or providing them locally.
class ProgrammaticGrader:
    def __init__(self, check_func) -> None:
        self.check_func = check_func
        
    def __call__(self, state: Any, **kwargs) -> float:
        return float(self.check_func(state))

class Task:
    def __init__(self, name: str, description: str, grader: ProgrammaticGrader):
        self.name = name
        self.description = description
        self.grader = grader

def easy_task_grader(state: Any) -> float:
    # state is FraudState. We check sql_result.
    # Expecting about 10 transactions > 10000 
    expected = 10.0
    try:
        # Simplistic parsing of state.sql_result to count rows
        lines = state.sql_result.strip().split('\\n')
        # If it's empty or an error
        if not lines or "ERROR" in state.sql_result:
            return 0.0
        # Return fraction of expected
        return min(len(lines) / expected, 1.0)
    except:
        return 0.0

def medium_task_grader(state: Any) -> float:
    # Ground truth for accounts with >3 failed logins and a transaction spike: A005, A010
    truth = MEDIUM_TRUTH
    try:
        found = set()
        for line in state.sql_result.strip().split('\\n'):
            for acc in truth:
                if acc in line:
                    found.add(acc)
            # Or just parse out A[0-9]{3}
            import re
            matches = re.findall(r"A\d{3}", line)
            found.update(matches)
        
        # Calculate F1 score vs ground truth
        tp = len(truth.intersection(found))
        fp = len(found - truth)
        fn = len(truth - found)
        
        if tp == 0:
            return 0.0
        precision = tp / (tp + fp)
        recall = tp / (tp + fn)
        f1 = 2 * (precision * recall) / (precision + recall)
        return float(f1)
    except:
        return 0.0

def hard_task_grader(state: Any) -> float:
    try:
        found = set(re.findall(r'A0\d{2}', state.sql_result))
        truth = {"A040", "A041", "A042", "A043", "A044", "A045"}
        if not found and not truth:
            return 1.0
        union = found | truth
        if not union:
            return 0.0
        return len(found & truth) / len(union)
    except Exception:
        return 0.0

easy_task = Task(
    name="EASY",
    description="Find all transactions above $10,000 in the last 30 days",
    grader=ProgrammaticGrader(easy_task_grader)
)

medium_task = Task(
    name="MEDIUM",
    description="Identify accounts with >3 failed logins AND a transaction spike",
    grader=ProgrammaticGrader(medium_task_grader)
)

hard_task = Task(
    name="HARD",
    description="Reconstruct a layering fraud chain across 5 hops of transfers",
    grader=ProgrammaticGrader(hard_task_grader)
)

TASKS = [easy_task, medium_task, hard_task]
