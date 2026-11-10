# CLAUDE.md

## Project
**File Inspector** — a web application that inspects files and reports contents and metadata, including database logging.

## What the app does
- Reads a file selected by the user (upload or drag-drop).
- Calculates: number of lines, words, and characters.
- Fetches and displays file properties: name, size, last modified date, MIME / file type, and format type.
- Persistence: theme preference saved to localStorage.
- Reports OS permission bits as "not available" (Browser limitation).
- Database Logging: Logs metadata to a DuckDB database using a Flask backend.

## Safety rules
- Never delete or overwrite a file without explicit user confirmation.
- Never modify a file outside the user's explicit request.
- Ask before any destructive action.

## Honest limitation
- Browser JavaScript cannot read OS permission bits (read/write/execute) from disk for security reasons.

## Communication
- Use plain, simple English.
- Keep work sessions reasonably sized; avoid very long uninterrupted runs.

## Session tracking
- Name/rename the session or record work using the date and time format `YYYY-MM-DD_HH-MM-SS`.

## Technical Stack
- Frontend: HTML/CSS/JavaScript (client-side)
- Backend: Flask
- Database: DuckDB
- Persistence: localStorage

## Current state
- File input: click/drag-and-drop.
- Calculations: lines, words, characters.
- Properties: name, size, modified date, MIME/type, format badge.
- Download: as plain text report with `_report` suffix.
- Supported Formats: .txt, .pdf, .html, .md, .docx.
- Theme: persistent dark/light mode toggle.
- Database: logs stored via Flask API to `first_project/file_insect.duckdb`.

## User context
- Siva Vardhna Reddy, PL/SQL developer at HSBC (10 years), transitioning to Data Engineering.
- Skills: PL/SQL (professional); Python, Snowflake, DBT, Ansible (basic).
