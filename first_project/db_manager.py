import duckdb
import os
from datetime import datetime

# Database path
db_path = "/home/siva/Desktop/work/claude/first_project/file_insect.duckdb"

def init_db():
    con = duckdb.connect(db_path)
    con.execute("""
        CREATE TABLE IF NOT EXISTS file_logs (
            id INTEGER PRIMARY KEY,
            file_name VARCHAR,
            file_size BIGINT,
            mime_type VARCHAR,
            last_modified TIMESTAMP,
            processed_at TIMESTAMP
        )
    """)
    con.close()

def log_file(file_name, file_size, mime_type, last_modified):
    con = duckdb.connect(db_path)
    con.execute("""
        INSERT INTO file_logs (file_name, file_size, mime_type, last_modified, processed_at)
        VALUES (?, ?, ?, ?, ?)
    """, (file_name, file_size, mime_type, last_modified, datetime.now()))
    con.close()

if __name__ == "__main__":
    init_db()
    print("Database and table initialized.")
