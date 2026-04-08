from typing import List, Set, Any
import numpy as np
import sqlite3
import os
import re

def clamp_score(score: float) -> float:
    """Ensure score is strictly between 0 and 1 (not 0.0 or 1.0)"""
    return max(0.001, min(0.999, float(score)))

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
    # state is a dict from FraudState.model_dump()
    # Expecting about 10 transactions > 10000 
    expected = 10.0
    try:
        sql_result = state.get('sql_result', '') if isinstance(state, dict) else state.sql_result
        # If it's empty or an error
        if not sql_result or "ERROR" in sql_result:
            return clamp_score(0.0)
        
        # Count the number of dict-like structures (each row is a dict)
        # Count occurrences of 'transaction_id' which appears once per row
        count = sql_result.count("'transaction_id':")
        if count == 0:
            # Try alternative format
            count = sql_result.count('"transaction_id":')
        
        # Return fraction of expected
        score = min(count / expected, 1.0)
        return clamp_score(score)
    except:
        return clamp_score(0.0)

def medium_task_grader(state: Any) -> float:
    # Ground truth for accounts with >3 failed logins and a transaction spike: A005, A010
    truth = MEDIUM_TRUTH
    try:
        sql_result = state.get('sql_result', '') if isinstance(state, dict) else state.sql_result
        found = set()
        for line in sql_result.strip().split('\n'):
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
            return clamp_score(0.0)
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
        if precision + recall == 0:
            return clamp_score(0.0)
        f1 = 2 * (precision * recall) / (precision + recall)
        return clamp_score(f1)
    except:
        return clamp_score(0.0)

def hard_task_grader(state: Any) -> float:
    try:
        sql_result = state.get('sql_result', '') if isinstance(state, dict) else state.sql_result
        found = set(re.findall(r'A0\d{2}', sql_result))
        truth = {"A040", "A041", "A042", "A043", "A044", "A045"}
        if not found and not truth:
            return clamp_score(1.0)
        union = found | truth
        if not union:
            return clamp_score(0.0)
        score = len(found & truth) / len(union)
        return clamp_score(score)
    except Exception:
        return clamp_score(0.0)

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
