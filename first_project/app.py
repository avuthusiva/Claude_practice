from flask import Flask, request, jsonify, send_from_directory
import duckdb
import os
from datetime import datetime

app = Flask(__name__)
DB_PATH = "/home/siva/Desktop/work/claude/first_project/file_insect.duckdb"

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/upload', methods=['POST'])
def upload_to_db():
    try:
        data = request.json
        file_name = data.get('file_name')
        file_size = data.get('file_size')
        mime_type = data.get('mime_type')
        last_modified = data.get('last_modified')

        con = duckdb.connect(DB_PATH)
        con.execute("""
            INSERT INTO file_logs (file_name, file_size, mime_type, last_modified, processed_at)
            VALUES (?, ?, ?, ?, ?)
        """, (file_name, file_size, mime_type, last_modified, datetime.now()))
        con.close()

        return jsonify({"status": "success", "message": f"Logged {file_name} to database."})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(port=5000, debug=True)
