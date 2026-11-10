# CLAUDE.md

## Project
This folder holds **first_project** — a web application that inspects a file and reports its contents and metadata.

## What the app does
- Reads a file selected by the user (upload or drag-drop).
- Calculates: number of lines, number of words, number of characters.
- Fetches and displays file properties: name, size, last modified date, MIME / file type.
- Reports OS permission bits as not available (see limitation below).
- Built with Flask backend server and HTML frontend.

## Safety rules
- Never delete or overwrite a file until the user explicitly confirms.
- Never modify a file outside the user's explicit request.
- Ask before any destructive action.

## Honest limitation
Browser JavaScript cannot read the OS permission bits of a file on disk.
The app shows permission bits as "not available" with an explanation.
To read real permission bits, a small backend is needed.

## Communication
- Write all answers in plain, simple English. No fancy or showy language.
- Keep work sessions reasonably sized; avoid very long uninterrupted runs.

## Session tracking
- When starting a new session or tracking work, name/rename the session or record it using the date and time format `YYYY-MM-DD_HH-MM-SS`.

## Current state
The app is a Flask web application with the following folder structure:
```
first_project/
├── api/
│   └── app.py                 # Flask backend server
├── data/
│   └── file_insect.duckdb     # DuckDB database
├── docs/
│   ├── BREF.md
│   ├── CLAUDE.md
│   └── README.md
├── scripts/
│   ├── db_manager.py          # Database table creation & log insertion
│   └── read_db.py             # Query & report utilities
├── templates/
│   ├── index.html             # Main file inspector
│   ├── dashboard.html         # Stats dashboard
│   └── logs.html              # Raw JSON logs view
├── .venv/                     # Python virtual environment
├── .python-version
├── pyproject.toml
└── uv.lock
```

Features:
- File input: click to select or drag-and-drop.
- Calculations: lines, words, characters.
- Properties shown: file name, size, last modified date, MIME / file type.
- Format support: .txt, .pdf, .html, .md, .docx
- OS permission bits: shown as "not available" with an explanation.
- Output: shown on the page, and downloadable as a plain text file.
- Download naming: the original file extension is removed and "_report" is added before ".txt".
- Theme: Includes a dark/light mode toggle (defaults to dark mode) with persistent preference saved to localStorage.
- Copy to clipboard: Report text can be copied to clipboard from the download modal.
- Format badge: File type displayed as badge (e.g., "Text (.txt)", "PDF (.pdf)", "Markdown (.md)", "Word (.docx)").
- Database upload: Sends file metadata to Flask server at `/upload` endpoint.

## Flask API Endpoints
- `GET /` - Main file inspector page (templates/index.html)
- `GET /dashboard` - Stats dashboard (templates/dashboard.html)
- `GET /logs_view` - Raw JSON logs viewer (templates/logs.html)
- `POST /upload` - Store file metadata in DuckDB
- `GET /logs` - Retrieve file logs as JSON
- `GET /health` - Health check endpoint

## Database and Logs
- DuckDB database: `data/file_insect.duckdb`
- Table: `file_logs` stores file_name, file_size, mime_type, last_modified, format_type, file_extension, word_count, character_count, upload_timestamp
- Python scripts: `scripts/db_manager.py` (create table, insert logs) and `scripts/read_db.py` (query logs)
- Flask server `api/app.py` provides API endpoints

## User context
- Siva Vardhna Reddy, PL/SQL developer at HSBC (10 years), migrating to Data Engineering.
- Current skills: PL/SQL (professional); Python, Snowflake, DBT, Ansible (basic).