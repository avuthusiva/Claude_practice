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
- Runs purely in the browser (client-side), no backend
- Properties to show: file name and size, last modified date, MIME / file type, OS permission bits
- Output: show the report on the page and download it as a file

## Honest limitation
A browser cannot read the OS permission bits (read/write/execute) of a file on disk.
The app will show the permission bits as "not available" and explain why.
If real permission bits are needed later, a small backend is required.

## Current state
The app is built as a single HTML file: `first_project/index.html`
- File input: click to select or drag-and-drop.
- Calculations: lines, words, characters.
- Properties shown: file name, size, last modified date, MIME / file type.
- OS permission bits: shown as "not available" with an explanation.
- Output: shown on the page, and downloadable as a plain text file.
- Download naming: the original file extension is removed and "_report" is added before ".txt".
- Supported Formats: Only .txt, .pdf, and .html are allowed; others trigger a format error.
- Theme: Includes a dark/light mode toggle (defaults to dark mode).

## Database and Logs
- DuckDB database created: `first_project/file_insect.duckdb`
- Tables created: `file_logs` to store file details, metadata, and timestamps.
- Python script `db_manager.py` initialized to manage table creation and insert logs.
- Python script `read_db.py` created to query and read data from the `file_logs` table.