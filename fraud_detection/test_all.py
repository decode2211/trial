"""
Comprehensive test suite for the fraud detection environment.
Tests all tasks, graders, and environment functionality.
"""
import sys
import traceback
from fraud_detection.envs.core_env import FraudEnv
from fraud_detection.tasks.tasks import TASKS, easy_task, medium_task, hard_task


def test_environment_reset():
    """Test that environment resets properly."""
    print("\n=== Testing Environment Reset ===")
    try:
        env = FraudEnv()
        obs, info = env.reset()
        
        assert obs['step_count'] == 0, "Step count should be 0 after reset"
        assert len(obs['fraud_signals']) == 10, "Should have 10 fraud signals"
        assert isinstance(obs['sql_result'], str), "SQL result should be string"
        
        print("✓ Environment reset successful")
        return True
    except Exception as e:
        print(f"✗ Environment reset failed: {e}")
        traceback.print_exc()
        return False


def test_basic_queries():
    """Test basic SQL query execution."""
    print("\n=== Testing Basic Queries ===")
    try:
        env = FraudEnv()
        env.reset()
        
        # Test valid query
        obs, reward, done, truncated, info = env.step("SELECT * FROM accounts LIMIT 5;")
        assert reward > 0, "Valid query should give positive reward"
        assert not done, "Should not be done after one step"
        print(f"✓ Valid query executed, reward: {reward}")
        
        # Test destructive query
        obs, reward, done, truncated, info = env.step("DROP TABLE accounts;")
        assert reward < 0, "Destructive query should give negative reward"
        assert "ERROR" in obs['sql_result'], "Should return error message"
        print(f"✓ Destructive query blocked, reward: {reward}")
        
        # Test repeated query
        env.reset()
        query = "SELECT * FROM accounts LIMIT 1;"
        env.step(query)
        obs, reward, done, truncated, info = env.step(query)
        assert reward <= 0, "Repeated query should not give positive reward"
        print(f"✓ Repeated query penalized, reward: {reward}")
        
        return True
    except Exception as e:
        print(f"✗ Basic query test failed: {e}")
        traceback.print_exc()
        return False


def test_easy_task():
    """Test EASY task: Find high-value transactions."""
    print("\n=== Testing EASY Task ===")
    try:
        env = FraudEnv()
        env.reset()
        
        # Execute the solution query
        query = """
        SELECT * FROM transactions 
        WHERE amount > 10000 
        AND timestamp >= DATE('now', '-30 days')
        """
        obs, reward, done, truncated, info = env.step(query)
        
        # Check grader
        state = env.state()
        score = easy_task.grader(state)
        
        print(f"Query result preview: {obs['sql_result'][:200]}...")
        print(f"Reward: {reward}")
        print(f"Score: {score}")
        
        assert score > 0.5, f"Easy task score should be > 0.5, got {score}"
        print(f"✓ EASY task passed with score: {score}")
        
        return True
    except Exception as e:
        print(f"✗ EASY task test failed: {e}")
        traceback.print_exc()
        return False


def test_medium_task():
    """Test MEDIUM task: Find suspicious accounts."""
    print("\n=== Testing MEDIUM Task ===")
    try:
        env = FraudEnv()
        env.reset()
        
        # Execute solution query
        query = """
        SELECT a.account_id, a.failed_logins, COUNT(t.transaction_id) as tx_count
        FROM accounts a
        JOIN transactions t ON a.account_id = t.source_account_id
        WHERE a.failed_logins > 3
        GROUP BY a.account_id
        HAVING COUNT(t.transaction_id) > 10
        """
        obs, reward, done, truncated, info = env.step(query)
        
        # Check grader
        state = env.state()
        score = medium_task.grader(state)
        
        print(f"Query result preview: {obs['sql_result'][:200]}...")
        print(f"Reward: {reward}")
        print(f"Score: {score}")
        
        assert score >= 0.0, f"Medium task score should be >= 0.0, got {score}"
        print(f"✓ MEDIUM task completed with score: {score}")
        
        return True
    except Exception as e:
        print(f"✗ MEDIUM task test failed: {e}")
        traceback.print_exc()
        return False


def test_hard_task():
    """Test HARD task: Reconstruct fraud chain."""
    print("\n=== Testing HARD Task ===")
    try:
        env = FraudEnv()
        env.reset()
        
        # Execute solution query
        query = """
        SELECT * FROM transactions 
        WHERE source_account_id IN ('A040', 'A041', 'A042', 'A043', 'A044')
        AND dest_account_id IN ('A041', 'A042', 'A043', 'A044', 'A045')
        ORDER BY timestamp
        """
        obs, reward, done, truncated, info = env.step(query)
        
        # Check grader
        state = env.state()
        score = hard_task.grader(state)
        
        print(f"Query result preview: {obs['sql_result'][:200]}...")
        print(f"Reward: {reward}")
        print(f"Score: {score}")
        
        assert score >= 0.0, f"Hard task score should be >= 0.0, got {score}"
        print(f"✓ HARD task completed with score: {score}")
        
        return True
    except Exception as e:
        print(f"✗ HARD task test failed: {e}")
        traceback.print_exc()
        return False


def test_reward_bounds():
    """Test that rewards are properly bounded."""
    print("\n=== Testing Reward Bounds ===")
    try:
        env = FraudEnv()
        env.reset()
        
        queries = [
            "SELECT * FROM accounts LIMIT 1;",
            "SELECT * FROM transactions LIMIT 1;",
            "DROP TABLE accounts;",
            "SELECT * FROM accounts WHERE account_id = 'A005';",
        ]
        
        for query in queries:
            obs, reward, done, truncated, info = env.step(query)
            assert -1.0 <= reward <= 1.0, f"Reward {reward} out of bounds [-1.0, 1.0]"
        
        print("✓ All rewards within bounds [-1.0, 1.0]")
        return True
    except Exception as e:
        print(f"✗ Reward bounds test failed: {e}")
        traceback.print_exc()
        return False


def test_episode_termination():
    """Test episode termination conditions."""
    print("\n=== Testing Episode Termination ===")
    try:
        env = FraudEnv()
        env.reset()
        
        # Test max steps truncation
        for i in range(51):
            obs, reward, done, truncated, info = env.step("SELECT 1;")
            if truncated:
                print(f"✓ Episode truncated at step {i+1}")
                break
        
        assert truncated, "Episode should truncate at max steps"
        
        return True
    except Exception as e:
        print(f"✗ Episode termination test failed: {e}")
        traceback.print_exc()
        return False


def test_state_method():
    """Test that state() method returns proper dict."""
    print("\n=== Testing state() Method ===")
    try:
        env = FraudEnv()
        env.reset()
        env.step("SELECT * FROM accounts LIMIT 1;")
        
        state = env.state()
        
        assert isinstance(state, dict), "state() should return dict"
        assert 'step_count' in state, "state should have step_count"
        assert 'sql_result' in state, "state should have sql_result"
        assert 'query_history' in state, "state should have query_history"
        
        print(f"✓ state() returns valid dict with keys: {list(state.keys())}")
        return True
    except Exception as e:
        print(f"✗ state() method test failed: {e}")
        traceback.print_exc()
        return False


def run_all_tests():
    """Run all tests and report results."""
    print("\n" + "="*60)
    print("FRAUD DETECTION ENVIRONMENT TEST SUITE")
    print("="*60)
    
    tests = [
        ("Environment Reset", test_environment_reset),
        ("Basic Queries", test_basic_queries),
        ("EASY Task", test_easy_task),
        ("MEDIUM Task", test_medium_task),
        ("HARD Task", test_hard_task),
        ("Reward Bounds", test_reward_bounds),
        ("Episode Termination", test_episode_termination),
        ("State Method", test_state_method),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n✗ {name} crashed: {e}")
            traceback.print_exc()
            results.append((name, False))
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Environment is ready for deployment.")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Please review.")
        return 1


if __name__ == "__main__":
    exit_code = run_all_tests()
    sys.exit(exit_code)
