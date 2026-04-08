import sqlite3
import datetime

conn = sqlite3.connect('fraud_detection/db/fraud.db')
cursor = conn.cursor()

# Check easy task
cursor.execute("""
    SELECT COUNT(*) FROM transactions 
    WHERE amount > 10000 
    AND timestamp >= DATE('now', '-30 days')
""")
count = cursor.fetchone()[0]
print(f"Easy task: {count} transactions > 10000 in last 30 days")

# Check medium task
cursor.execute("""
    SELECT a.account_id, a.failed_logins, COUNT(t.transaction_id) as tx_count
    FROM accounts a
    JOIN transactions t ON a.account_id = t.source_account_id
    WHERE a.failed_logins > 3
    GROUP BY a.account_id
    HAVING COUNT(t.transaction_id) > 10
""")
rows = cursor.fetchall()
print(f"Medium task: {len(rows)} accounts with >3 failed logins and >10 transactions")
for row in rows:
    print(f"  {row}")

# Check hard task
cursor.execute("""
    SELECT * FROM transactions 
    WHERE source_account_id IN ('A040', 'A041', 'A042', 'A043', 'A044')
    AND dest_account_id IN ('A041', 'A042', 'A043', 'A044', 'A045')
    ORDER BY timestamp
""")
rows = cursor.fetchall()
print(f"Hard task: {len(rows)} transactions in the chain")

conn.close()
