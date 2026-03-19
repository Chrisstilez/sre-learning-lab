import psycopg2
import sys
from datetime import datetime

# Connection details match our Secret
DB_CONFIG = {
    "host": "postgres-0.postgres.database.svc.cluster.local",
    "database": "sre_lab",
    "user": "admin",
    "password": "pgpass123",
    "port": 5432
}

def connect():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        conn.autocommit = True
        return conn
    except Exception as e:
        print(f"Connection failed: {e}")
        sys.exit(1)

def setup_table(conn):
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS visits (
            id SERIAL PRIMARY KEY,
            visitor_name TEXT NOT NULL,
            message TEXT,
            visited_at TIMESTAMP DEFAULT NOW()
        )
    """)
    print("Table 'visits' ready.")

def add_visit(conn, name, message):
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO visits (visitor_name, message) VALUES (%s, %s) RETURNING id",
        (name, message)
    )
    row_id = cursor.fetchone()[0]
    print(f"Added visit #{row_id}: {name} - {message}")

def show_visits(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT id, visitor_name, message, visited_at FROM visits ORDER BY id")
    rows = cursor.fetchall()
    if not rows:
        print("No visits yet.")
        return
    print(f"\n{'ID':<5} {'Name':<15} {'Message':<30} {'Time'}")
    print("-" * 75)
    for row in rows:
        print(f"{row[0]:<5} {row[1]:<15} {row[2]:<30} {row[3]}")
    print(f"\nTotal visits: {len(rows)}")

def count_visits(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM visits")
    count = cursor.fetchone()[0]
    print(f"Total visits: {count}")

if __name__ == "__main__":
    conn = connect()
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python db_client.py setup          - Create table")
        print("  python db_client.py add NAME MSG   - Add a visit")
        print("  python db_client.py show            - Show all visits")
        print("  python db_client.py count           - Count visits")
        sys.exit(0)
    
    command = sys.argv[1]
    
    if command == "setup":
        setup_table(conn)
    elif command == "add":
        name = sys.argv[2] if len(sys.argv) > 2 else "anonymous"
        message = sys.argv[3] if len(sys.argv) > 3 else "was here"
        add_visit(conn, name, message)
    elif command == "show":
        show_visits(conn)
    elif command == "count":
        count_visits(conn)
    else:
        print(f"Unknown command: {command}")
    
    conn.close()
