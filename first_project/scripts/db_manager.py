"""
db_manager.py - Database management utilities for the File Inspector app.

Provides functions to:
- Create the DuckDB database file and the file_logs table
- Insert file log entries
- Manage the database lifecycle

Usage:
    python scripts/db_manager.py          # creates the database and table
"""

import os
import duckdb

# Database path - in data folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)
DB_PATH = os.path.join(PROJECT_ROOT, "data", "file_insect.duckdb")


def get_db_path():
    """Return the absolute path to the DuckDB database file."""
    return DB_PATH


def create_database():
    """
    Create the DuckDB database file and the file_logs table.
    """
    conn = duckdb.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS file_logs (
            file_name       VARCHAR,
            file_size       BIGINT,
            mime_type       VARCHAR,
            last_modified   VARCHAR,
            format_type     VARCHAR,
            file_extension  VARCHAR,
            word_count      BIGINT,
            character_count BIGINT,
            upload_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.close()
    print(f"Database created/verified at: {DB_PATH}")


def insert_log(file_name, file_size, mime_type, last_modified,
               format_type, file_extension, word_count=0, character_count=0):
    """
    Insert a single file log entry into the file_logs table.

    Args:
        file_name       (str)   - original file name
        file_size       (int)   - file size in bytes
        mime_type       (str)   - MIME / file type
        last_modified   (str)   - last modified timestamp (ISO string)
        format_type     (str)   - human-readable format label
        file_extension  (str)   - file extension (e.g. "txt")
        word_count      (int)   - word count, default 0
        character_count (int)   - character count, default 0
    """
    conn = duckdb.connect(DB_PATH)
    conn.execute("""
        INSERT INTO file_logs
            (file_name, file_size, mime_type, last_modified,
             format_type, file_extension, word_count, character_count)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (file_name, file_size, mime_type, last_modified,
          format_type, file_extension, word_count, character_count))
    conn.close()


def get_table_schema():
    """Return the column names and types of the file_logs table."""
    conn = duckdb.connect(DB_PATH)
    rows = conn.execute("DESCRIBE file_logs").fetchall()
    conn.close()
    return rows


def get_row_count():
    """Return the total number of rows in the file_logs table."""
    conn = duckdb.connect(DB_PATH)
    count = conn.execute("SELECT COUNT(*) FROM file_logs").fetchone()[0]
    conn.close()
    return count


if __name__ == "__main__":
    create_database()
    print("Table schema:")
    for col in get_table_schema():
        print(f"  {col}")
    print(f"Total rows: {get_row_count()}")