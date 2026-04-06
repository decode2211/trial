from typing import List, Set, Any
import numpy as np

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
    truth = {"A005", "A010"}
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
    # Ground truth layering chain: A040 -> A041 -> A042 -> A043 -> A044 -> A045
    truth = {"A040", "A041", "A042", "A043", "A044", "A045"}
    try:
        found = set()
        import re
        for line in state.sql_result.strip().split('\\n'):
            matches = re.findall(r"A\d{3}", line)
            found.update(matches)
            
        intersection = len(truth.intersection(found))
        union = len(truth.union(found))
        
        if union == 0:
            return 0.0
        # Jaccard similarity
        return float(intersection / union)
    except:
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
