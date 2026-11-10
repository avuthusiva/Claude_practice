# CLAUDE.md

## Project
This folder holds **first_project** — a web application that inspects a file and reports its contents and metadata.

## What the app does
- Reads a file selected by the user (upload or drag-drop).
- Calculates: number of lines, number of words, number of characters.
- Fetches and displays file properties: name, size, last modified date, MIME / file type.
- Reports OS permission bits as not available (see limitation below).
- Built with HTML, client-side only, no backend.

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
The app is built as a single HTML file: `first_project/index.html`
- File input: click to select or drag-and-drop.
- Calculations: lines, words, characters.
- Properties shown: file name, size, last modified date, MIME / file type.
- Output: shown on the page, and downloadable as a plain text file.
- Download naming: the original file extension is removed and "_report" is added before ".txt".
- Supported Formats: Only .txt, .pdf, .html are allowed; others trigger a format error.
- Theme: Includes a dark/light mode toggle (defaults to dark mode).

## Database and Logs
- DuckDB database: `first_project/file_insect.duckdb`
- Table: `file_logs` (stores file_name, file_size, mime_type, last_modified, processed_at)
- Python scripts: `db_manager.py` (create table, insert logs) and `read_db.py` (query logs)
- Upload button: sends file data to Flask server at `/upload` endpoint

## User context
- Siva Vardhna Reddy, PL/SQL developer at HSBC (10 years), migrating to Data Engineering.
- Current skills: PL/SQL (professional); Python, Snowflake, DBT, Ansible (basic).