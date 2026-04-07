import sqlite3
import numpy as np
import datetime
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "fraud.db")

def seed():
    np.random.seed(42)
    
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    cur.execute('''
    CREATE TABLE accounts (
        account_id TEXT PRIMARY KEY,
        name TEXT,
        balance REAL,
        failed_logins INTEGER,
        created_at TEXT
    )
    ''')
    
    cur.execute('''
    CREATE TABLE transactions (
        transaction_id TEXT PRIMARY KEY,
        source_account_id TEXT,
        dest_account_id TEXT,
        amount REAL,
        type TEXT,
        timestamp TEXT,
        FOREIGN KEY(source_account_id) REFERENCES accounts(account_id),
        FOREIGN KEY(dest_account_id) REFERENCES accounts(account_id)
    )
    ''')
    
    now = datetime.datetime.now()
    
    accounts = []
    for i in range(1, 51):
        account_id = f"A{i:03d}"
        accounts.append(account_id)
        # Normal account: few failed logins
        failed_logins = np.random.randint(0, 3) 
        balance = round(np.random.uniform(100, 5000), 2)
        cur.execute('INSERT INTO accounts VALUES (?, ?, ?, ?, ?)', 
                    (account_id, f"User {i}", balance, failed_logins, (now - datetime.timedelta(days=np.random.randint(30, 365))).isoformat()))
        
    # MEDIUM task: Accounts with >3 failed logins AND a transaction spike
    # Make A005 and A010 have >3 failed logins and a spike
    cur.execute('UPDATE accounts SET failed_logins = 5 WHERE account_id IN ("A005", "A010")')
    
    transaction_id_counter = 1
    transactions = []
    
    def insert_tx(src, dest, amount, type, time_offset_days):
        nonlocal transaction_id_counter
        tx_id = f"T{transaction_id_counter:04d}"
        transaction_id_counter += 1
        tx_time = (now - datetime.timedelta(days=time_offset_days)).isoformat()
        cur.execute('INSERT INTO transactions VALUES (?, ?, ?, ?, ?, ?)',
                    (tx_id, src, dest, amount, type, tx_time))
        return tx_id

    # Normal transactions
    for _ in range(300):
        src = np.random.choice(accounts)
        dest = np.random.choice([a for a in accounts if a != src])
        amount = round(np.random.uniform(5, 500), 2)
        insert_tx(src, dest, amount, 'TRANSFER', np.random.randint(0, 100))

    # EASY task: Find all transactions above $10,000 in the last 30 days
    for _ in range(10):
        src = np.random.choice(accounts)
        dest = np.random.choice([a for a in accounts if a != src])
        amount = round(np.random.uniform(10500, 20000), 2)
        insert_tx(src, dest, amount, 'TRANSFER', np.random.randint(1, 29)) # within last 30 days
        
    # Also some above 10k but older than 30 days
    for _ in range(5):
        src = np.random.choice(accounts)
        dest = np.random.choice([a for a in accounts if a != src])
        amount = round(np.random.uniform(10500, 20000), 2)
        insert_tx(src, dest, amount, 'TRANSFER', np.random.randint(35, 100))
        
    # MEDIUM task: transaction spike for A005 and A010
    # Add many small transactions quickly for these
    for acc in ["A005", "A010"]:
        for _ in range(15):
             dest = np.random.choice([a for a in accounts if a != acc])
             amount = round(np.random.uniform(900, 999), 2)
             insert_tx(acc, dest, amount, 'TRANSFER', np.random.randint(1, 5))

    # HARD task: Reconstruct a layering fraud chain across 5 hops of transfers
    # Chain: A040 -> A041 -> A042 -> A043 -> A044 -> A045
    chain_accounts = ["A040", "A041", "A042", "A043", "A044", "A045"]
    layer_amount = 5432.10
    for i in range(len(chain_accounts) - 1):
        # same amount, sequential days (e.g., offsets 10, 9, 8, 7, 6)
        insert_tx(chain_accounts[i], chain_accounts[i+1], layer_amount, 'TRANSFER', 10 - i)
        layer_amount -= 50 # Small fee deduction at each step
        
    EXPECTED_HIGH_VALUE_RECENT = 10
    cursor = conn.cursor()
    cursor.execute("""
        SELECT COUNT(*) FROM transactions 
        WHERE amount > 10000 
        AND timestamp >= DATE('now', '-30 days')
    """)
    count = cursor.fetchone()[0]

    assert count == EXPECTED_HIGH_VALUE_RECENT, \
        f"Seed produced {count} rows, grader expects {EXPECTED_HIGH_VALUE_RECENT}"

    print(f"Seed verified: {count} high-value recent transactions found.")
    
    conn.commit()
    conn.close()

    

if __name__ == "__main__":
    seed()
