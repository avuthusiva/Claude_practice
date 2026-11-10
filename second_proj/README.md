# EPUB to PDF Converter

A desktop application to convert EPUB files to PDF format using Python with Tkinter GUI.

## Features
- Select EPUB file via file dialog
- Convert EPUB to PDF with one click
- Auto-generates output filename (replaces `.epub` with `.pdf`)
- Shows conversion progress and status
- Download/Save the converted PDF to any location
- Conversion log for debugging

## Requirements
- Python 3.8+
- ebooklib
- weasyprint

## Installation
```bash
pip install ebooklib weasyprint
```

## Usage
```bash
python epub_to_pdf.py
```

1. Click "Browse..." to select an EPUB file
2. Output filename is auto-generated (same name, .pdf extension)
3. Click "Convert to PDF" to start conversion
4. When complete, click "Download PDF" to save to desired location

## How it Works
1. Reads EPUB using `ebooklib`
2. Extracts HTML content from all chapters/spine items
3. Wraps content in styled HTML with CSS for print layout
4. Uses `weasyprint` to render HTML to PDF
5. Saves PDF to auto-generated path, then user can save elsewhere

## Folder Structure
```
second_proj/
├── epub_to_pdf.py    # Main application
├── BREF.md           # Project brief
└── README.md         # This file
```