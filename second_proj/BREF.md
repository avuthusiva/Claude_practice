# EPUB to PDF Converter

## Goal
Create an application that converts EPUB files to PDF format.

## Requirements
1. Read the EPUB file when file path is given
2. Provide a "Convert" button to start conversion
2. Show message when conversion is completed
3. Provide a "Download" button for the converted PDF file
4. File name: take the EPUB file name, remove `.epub` extension, add `.pdf` extension

## Application Type
Flask web application with HTML/JavaScript frontend (port 5001)

## Architecture
- **Backend**: Flask server (`app.py`) - handles file upload, EPUB parsing, PDF generation
- **Frontend**: Single-page HTML with drag-and-drop, progress indicator, download button
- **Conversion Engine**: 
  - `ebooklib` for EPUB reading and content extraction
  - `weasyprint` for HTML-to-PDF rendering
- **File Handling**: Temporary storage in `/tmp/epub_conversions/`

## Current State
The application is built and running as a Flask web app:
- **Main app**: `app.py` - Flask server with embedded HTML template
- **Desktop version**: `epub_to_pdf.py` - Tkinter GUI (requires `python3-tk` system package)
- **Documentation**: `README.md`

## Features Implemented
- Drag & drop or click to select EPUB file
- Convert button with progress indicator
- Real-time conversion log
- Success/error status messages
- Download button appears after successful conversion
- Auto-generates output filename: `input.epub` → `input.pdf`
- Title page with book metadata
- Proper CSS for print layout (A4, margins, page breaks)

## API Endpoints
- `GET /` - Main converter page
- `POST /convert` - Upload EPUB, return PDF filename
- `GET /download/<filename>` - Download converted PDF

## Dependencies
- `ebooklib` - EPUB parsing
- `weasyprint` - HTML to PDF conversion
- `flask` - Web framework

## Honest Limitation
The desktop Tkinter version (`epub_to_pdf.py`) requires `python3-tk` system package which may not be available in all environments. The Flask web version works without GUI dependencies.