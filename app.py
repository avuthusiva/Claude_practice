"""
app.py - Flask backend server for the File Inspector application.

Provides:
- REST API endpoint for uploading file metadata to DuckDB
- DuckDB database management (table creation, log insertion)
- Query/read functionality for the file_logs table

The HTML frontend (index.html) sends file metadata to the /upload endpoint,
which inserts a row into the file_logs table in the DuckDB database.
"""

import os
import json
from datetime import datetime
from flask import Flask, request, jsonify
import duckdb

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "first_project", "file_insect.duckdb")

# Ensure the database directory exists
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

app = Flask(__name__, template_folder=BASE_DIR, static_folder=BASE_DIR)

# ---------------------------------------------------------------------------
# Database management
# ---------------------------------------------------------------------------
def get_connection():
    """Open a connection to the DuckDB database file."""
    return duckdb.connect(DB_PATH)


def init_db():
    """Create the file_logs table if it does not already exist."""
    conn = get_connection()
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


def insert_log(file_name, file_size, mime_type, last_modified,
               format_type, file_extension, word_count=0, character_count=0):
    """Insert a single file log row into the file_logs table."""
    conn = get_connection()
    # DuckDB INTEGER PRIMARY KEY needs a value; auto-generate if omitted by using a sequence
    # We'll omit the id column and let DuckDB assign the rowid implicitly
    conn.execute("""
        INSERT INTO file_logs
            (file_name, file_size, mime_type, last_modified,
             format_type, file_extension, word_count, character_count)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (file_name, file_size, mime_type, last_modified,
          format_type, file_extension, word_count, character_count))
    conn.close()


def read_logs(limit=100):
    """Read the most recent file log entries."""
    conn = get_connection()
    # Order by upload_timestamp instead of id
    rows = conn.execute(
        "SELECT * FROM file_logs ORDER BY upload_timestamp DESC LIMIT ?", (limit,)
    ).fetchall()
    cols = [desc[0] for desc in conn.execute(
        "DESCRIBE file_logs"
    ).fetchall()]
    conn.close()
    return [dict(zip(cols, row)) for row in rows]


# Initialize the database on startup
init_db()

# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------
@app.route("/")
def index():
    """Serve the main HTML page."""
    return app.send_static_file("index.html")


@app.route("/dashboard")
def dashboard():
    """Serve the database dashboard page."""
    return app.send_static_file("dashboard.html")


@app.route("/logs_view")
def logs_view():
    """Serve the raw JSON logs view page."""
    return app.send_static_file("logs.html")


@app.route("/upload", methods=["POST"])
def upload():
    """
    Receive file metadata from the frontend and store it in DuckDB.

    Expected JSON body:
        file_name       (str)   - original file name
        file_size       (int)   - file size in bytes
        mime_type       (str)   - MIME / file type
        last_modified   (str)   - ISO timestamp of last modified
        format_type     (str)   - human-readable format label
        file_extension  (str)   - file extension (e.g. "txt", "pdf")
        word_count      (int)   - optional, default 0
        character_count (int)   - optional, default 0
    """
    try:
        data = request.get_json(force=True)
    except Exception:
        return jsonify({"status": "error", "message": "Invalid JSON body"}), 400

    file_name       = data.get("file_name", "")
    file_size       = data.get("file_size", 0)
    mime_type       = data.get("mime_type", "")
    last_modified   = data.get("last_modified", "")
    format_type     = data.get("format_type", "")
    file_extension  = data.get("file_extension", "")
    word_count      = data.get("word_count", 0)
    character_count = data.get("character_count", 0)

    try:
        insert_log(file_name, file_size, mime_type, last_modified,
                   format_type, file_extension, word_count, character_count)
        return jsonify({
            "status": "success",
            "message": f"File '{file_name}' uploaded to database successfully."
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/logs", methods=["GET"])
def logs():
    """Return recent file log entries as JSON."""
    limit = request.args.get("limit", 100, type=int)
    rows = read_logs(limit=limit)
    return jsonify({"status": "success", "count": len(rows), "logs": rows})


@app.route("/health", methods=["GET"])
def health():
    """Simple health-check endpoint."""
    return jsonify({"status": "ok", "db_path": DB_PATH})


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print(f"DuckDB database: {DB_PATH}")
    print("Serving index.html at http://localhost:5000")
    app.run(host="127.0.0.1", port=5000, debug=True)