"""
read_db.py - Read and query utilities for the File Inspector DuckDB database.

Provides functions to:
- Connect to the DuckDB database (read-only or read-write)
- Query all file logs with pagination
- Filter logs by extension or format type
- Calculate aggregate summary statistics (total files, size, words, characters)
- Output a formatted text report

Usage:
    python read_db.py
"""

import os
import duckdb

# Database path relative to this script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "first_project", "file_insect.duckdb")


def get_connection():
    """Open a connection to the DuckDB database."""
    if not os.path.exists(DB_PATH):
        raise FileNotFoundError(f"Database not found at {DB_PATH}. Run db_manager.py first.")
    return duckdb.connect(DB_PATH, read_only=True)


def read_all_logs(limit=100, offset=0):
    """
    Read file log entries from the database with limit and offset.

    Returns:
        List of dictionaries representing each row.
    """
    try:
        conn = get_connection()
        rows = conn.execute(
            "SELECT * FROM file_logs ORDER BY upload_timestamp DESC LIMIT ? OFFSET ?",
            (limit, offset)
        ).fetchall()
        cols = [desc[0] for desc in conn.execute("DESCRIBE file_logs").fetchall()]
        conn.close()
        return [dict(zip(cols, row)) for row in rows]
    except Exception as e:
        print(f"Error reading logs: {e}")
        return []


def read_logs_by_extension(file_extension, limit=100):
    """Read logs filtered by file extension (e.g., 'txt', 'pdf', 'md')."""
    try:
        conn = get_connection()
        rows = conn.execute(
            "SELECT * FROM file_logs WHERE file_extension = ? ORDER BY upload_timestamp DESC LIMIT ?",
            (file_extension, limit)
        ).fetchall()
        cols = [desc[0] for desc in conn.execute("DESCRIBE file_logs").fetchall()]
        conn.close()
        return [dict(zip(cols, row)) for row in rows]
    except Exception as e:
        print(f"Error reading logs by extension: {e}")
        return []


def get_summary_stats():
    """
    Calculate summary statistics across all logged files.

    Returns:
        Dictionary containing total files, total size, total words, total characters, and breakdown by extension.
    """
    try:
        conn = get_connection()
        stats = conn.execute("""
            SELECT
                COUNT(*) AS total_files,
                COALESCE(SUM(file_size), 0) AS total_size,
                COALESCE(SUM(word_count), 0) AS total_words,
                COALESCE(SUM(character_count), 0) AS total_characters
            FROM file_logs
        """).fetchone()

        by_ext = conn.execute("""
            SELECT file_extension, COUNT(*) AS count
            FROM file_logs
            GROUP BY file_extension
            ORDER BY count DESC
        """).fetchall()
        conn.close()

        return {
            "total_files": stats[0],
            "total_size": stats[1],
            "total_words": stats[2],
            "total_characters": stats[3],
            "by_extension": {ext: count for ext, count in by_ext}
        }
    except Exception as e:
        print(f"Error getting summary stats: {e}")
        return {
            "total_files": 0,
            "total_size": 0,
            "total_words": 0,
            "total_characters": 0,
            "by_extension": {}
        }


if __name__ == "__main__":
    print("=== File Inspector Database Report ===")
    print(f"Database Path: {DB_PATH}\n")

    summary = get_summary_stats()
    print("Summary Statistics:")
    print(f"  Total Files Logged:    {summary['total_files']}")
    print(f"  Total Size:            {summary['total_size']} bytes")
    print(f"  Total Words:           {summary['total_words']}")
    print(f"  Total Characters:      {summary['total_characters']}")
    print(f"  Files by Extension:    {summary['by_extension']}\n")

    print("=== Recent File Logs ===")
    logs = read_all_logs(limit=10)
    if not logs:
        print("  No logs found in database.")
    else:
        for i, log in enumerate(logs, 1):
            print(f"  {i}. {log['file_name']} | Type: {log['format_type']} | Size: {log['file_size']} bytes | Uploaded: {log['upload_timestamp']}")
