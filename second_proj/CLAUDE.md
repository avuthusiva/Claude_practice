# CLAUDE.md

## Project
This folder holds **second_proj** — an EPUB to PDF converter web application.

## What the app does
- Accepts EPUB file upload via drag-and-drop or file picker
- Converts EPUB to PDF using ebooklib + weasyprint
- Shows conversion progress and status messages
- Provides download button for the converted PDF
- Auto-generates output filename: removes `.epub` extension, adds `.pdf`

## Safety rules
- Never delete or overwrite a file until the user explicitly confirms
- Never modify a file outside the user's explicit request
- Ask before any destructive action
- Temporary files stored in `/tmp/epub_conversions/` are cleaned up on server restart

## Honest limitation
- Desktop Tkinter version (`epub_to_pdf.py`) requires `python3-tk` system package
- Web version has 50MB upload limit
- Complex EPUBs with advanced CSS/JS may not render perfectly in PDF
- Requires `ebooklib` and `weasyprint` Python packages

## Communication
- Write all answers in plain, simple English. No fancy or showy language.
- Keep work sessions reasonably sized; avoid very long uninterrupted runs.

## Session tracking
- When starting a new session or tracking work, name/rename the session or record it using the date and time format `YYYY-MM-DD_HH-MM-SS`.

## Current state
The application is a Flask web application with the following structure:
```
second_proj/
├── app.py          # Flask web server (running on port 5001)
├── epub_to_pdf.py  # Desktop Tkinter version (requires python3-tk)
├── BREF.md         # Project brief
├── CLAUDE.md       # This file
└── README.md       # Documentation
```

Features:
- File input: drag-and-drop or click to select EPUB file
- Convert button with progress indicator
- Real-time conversion log
- Success/error status messages
- Download button appears after successful conversion
- Auto-generates output filename: `input.epub` → `input.pdf`
- Title page with book metadata
- Proper CSS for print layout (A4, margins, page breaks)

## Flask API Endpoints
- `GET /` - Main converter page
- `POST /convert` - Upload EPUB, return PDF filename
- `GET /download/<filename>` - Download converted PDF

## Dependencies
- `flask` - Web framework
- `ebooklib` - EPUB parsing
- `weasyprint` - HTML to PDF conversion

## Running the Application
```bash
cd /home/siva/Desktop/work/claude/Claude_practice/second_proj
python3 app.py
# Open http://localhost:5001
```

## User context
- Siva Vardhna Reddy, PL/SQL developer at HSBC (10 years), migrating to Data Engineering.
- Current skills: PL/SQL (professional); Python, Snowflake, DBT, Ansible (basic).