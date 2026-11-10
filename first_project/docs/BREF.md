# Word calculation and file properties

## Goal
1. Need to read the file and calculate the number of lines, words and characters inside it
2. Need to fetch all the properties of the file

## Application
Need to use HTML

## Caution
Need to check which permissions are present on that file

## Constraint
Do not remove the file until the user confirms

## Architecture decision (from your answers)
- File input: file upload / drag-drop
- Runs with Flask backend server (Python)
- Properties to show: file name and size, last modified date, MIME / file type, OS permission bits
- Output: show the report on the page and download it as a file

## Honest limitation
A browser cannot read the OS permission bits (read/write/execute) of a file on disk.
The app shows the permission bits as "not available" and explains why.

## Current state
The app is built as a Flask web application with the following folder structure:
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

## Database and Logs
- DuckDB database: `data/file_insect.duckdb`
- Table: `file_logs` stores file details, metadata, and timestamps.
- Python script `scripts/db_manager.py` manages table creation and inserts logs.
- Python script `scripts/read_db.py` queries and reads data from the `file_logs` table.
- Flask server (`api/app.py`) serves the app and provides API endpoints:
  - `/` - Main file inspector page
  - `/dashboard` - Stats dashboard
  - `/logs_view` - Raw JSON logs viewer
  - `/upload` - POST endpoint to store file metadata
  - `/logs` - GET endpoint to retrieve logs as JSON
  - `/health` - Health check endpoint