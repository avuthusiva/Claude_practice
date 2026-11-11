#!/usr/bin/env python3
"""
EPUB to PDF Converter - Web Application
Flask backend with HTML frontend for converting EPUB files to PDF.
"""

import os
import threading
from pathlib import Path
from flask import Flask, request, jsonify, send_file, render_template_string
from werkzeug.utils import secure_filename

try:
    import ebooklib
    from ebooklib import epub
    from weasyprint import HTML, CSS
    from weasyprint.text.fonts import FontConfiguration
except ImportError as e:
    print(f"Missing dependencies: {e}")
    print("Please install: pip install ebooklib weasyprint")
    exit(1)

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max upload
app.config['UPLOAD_FOLDER'] = '/tmp/epub_conversions'

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Store conversion status
conversion_status = {}

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>EPUB to PDF Converter</title>
    <style>
        :root {
            --primary: #3182ce;
            --primary-hover: #2b6cb0;
            --success: #38a169;
            --success-hover: #2f855a;
            --bg: #f7fafc;
            --card: #ffffff;
            --text: #2d3748;
            --text-light: #718096;
            --border: #e2e8f0;
            --error: #e53e3e;
        }
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background: var(--bg);
            color: var(--text);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            padding: 40px 20px;
        }
        .container {
            background: var(--card);
            border-radius: 16px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.08);
            padding: 40px;
            width: 100%;
            max-width: 560px;
        }
        h1 {
            font-size: 28px;
            font-weight: 700;
            text-align: center;
            margin-bottom: 8px;
            color: var(--text);
        }
        .subtitle {
            text-align: center;
            color: var(--text-light);
            margin-bottom: 32px;
        }
        .drop-zone {
            border: 2px dashed var(--border);
            border-radius: 12px;
            padding: 40px 20px;
            text-align: center;
            cursor: pointer;
            transition: all 0.2s;
            background: #fafafa;
        }
        .drop-zone:hover, .drop-zone.drag-over {
            border-color: var(--primary);
            background: #ebf8ff;
        }
        .drop-zone p { margin: 8px 0; }
        .drop-zone .icon { font-size: 48px; }
        .file-info {
            background: #ebf8ff;
            border: 1px solid var(--primary);
            border-radius: 8px;
            padding: 16px;
            margin-top: 16px;
            display: none;
            align-items: center;
            justify-content: space-between;
        }
        .file-info.visible { display: flex; }
        .file-info .name { font-weight: 500; }
        .file-info .size { color: var(--text-light); font-size: 14px; }
        .btn {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
            padding: 14px 28px;
            border-radius: 8px;
            font-size: 16px;
            font-weight: 600;
            border: none;
            cursor: pointer;
            transition: all 0.2s;
            width: 100%;
        }
        .btn:disabled { opacity: 0.6; cursor: not-allowed; }
        .btn-primary {
            background: var(--primary);
            color: white;
        }
        .btn-primary:hover:not(:disabled) { background: var(--primary-hover); }
        .btn-success {
            background: var(--success);
            color: white;
            display: none;
        }
        .btn-success.visible { display: inline-flex; }
        .btn-success:hover:not(:disabled) { background: var(--success-hover); }
        .progress-container {
            margin: 24px 0;
            display: none;
        }
        .progress-container.visible { display: block; }
        .progress-bar {
            height: 8px;
            background: var(--border);
            border-radius: 4px;
            overflow: hidden;
        }
        .progress-fill {
            height: 100%;
            background: var(--primary);
            width: 0%;
            transition: width 0.3s;
            border-radius: 4px;
        }
        .progress-fill.indeterminate {
            animation: progress-pulse 1.5s infinite;
        }
        @keyframes progress-pulse {
            0% { width: 0%; margin-left: 0%; }
            50% { width: 50%; margin-left: 0%; }
            100% { width: 0%; margin-left: 100%; }
        }
        .status {
            text-align: center;
            font-size: 14px;
            color: var(--text-light);
            min-height: 24px;
            margin-top: 8px;
        }
        .status.success { color: var(--success); }
        .status.error { color: var(--error); }
        .log-area {
            background: #1a202c;
            color: #e2e8f0;
            border-radius: 8px;
            padding: 16px;
            font-family: monospace;
            font-size: 13px;
            max-height: 200px;
            overflow-y: auto;
            display: none;
        }
        .log-area.visible { display: block; }
        .log-line { margin: 4px 0; white-space: pre-wrap; }
        .log-line.success { color: #68d391; }
        .log-line.error { color: #fc8181; }
    </style>
</head>
<body>
    <div class="container">
        <h1>EPUB to PDF Converter</h1>
        <p class="subtitle">Convert your EPUB files to PDF format</p>

        <div class="drop-zone" id="dropZone">
            <div class="icon">📖</div>
            <p>Drag & drop an EPUB file here</p>
            <p style="font-size: 14px; color: var(--text-light);">or click to browse</p>
            <input type="file" id="fileInput" accept=".epub" style="display: none;">
        </div>

        <div class="file-info" id="fileInfo">
            <div>
                <div class="name" id="fileName"></div>
                <div class="size" id="fileSize"></div>
            </div>
        </div>

        <button class="btn btn-primary" id="convertBtn" disabled>Convert to PDF</button>

        <div class="progress-container" id="progressContainer">
            <div class="progress-bar">
                <div class="progress-fill indeterminate" id="progressFill"></div>
            </div>
            <div class="status" id="statusText">Ready</div>
        </div>

        <button class="btn btn-success" id="downloadBtn" disabled>Download PDF</button>

        <div class="log-area" id="logArea"></div>
    </div>

    <script>
        const dropZone = document.getElementById('dropZone');
        const fileInput = document.getElementById('fileInput');
        const fileInfo = document.getElementById('fileInfo');
        const fileName = document.getElementById('fileName');
        const fileSize = document.getElementById('fileSize');
        const convertBtn = document.getElementById('convertBtn');
        const progressContainer = document.getElementById('progressContainer');
        const progressFill = document.getElementById('progressFill');
        const statusText = document.getElementById('statusText');
        const downloadBtn = document.getElementById('downloadBtn');
        const logArea = document.getElementById('logArea');

        let selectedFile = null;
        let outputFilename = '';

        // Drag and drop
        dropZone.addEventListener('click', () => fileInput.click());
        dropZone.addEventListener('dragover', (e) => {
            e.preventDefault();
            dropZone.classList.add('drag-over');
        });
        dropZone.addEventListener('dragleave', () => dropZone.classList.remove('drag-over'));
        dropZone.addEventListener('drop', (e) => {
            e.preventDefault();
            dropZone.classList.remove('drag-over');
            if (e.dataTransfer.files.length) handleFile(e.dataTransfer.files[0]);
        });
        fileInput.addEventListener('change', (e) => {
            if (e.target.files.length) handleFile(e.target.files[0]);
        });

        function handleFile(file) {
            if (!file.name.toLowerCase().endsWith('.epub')) {
                alert('Please select an EPUB file.');
                return;
            }
            selectedFile = file;
            outputFilename = file.name.replace(/\.epub$/i, '.pdf');
            fileName.textContent = file.name;
            fileSize.textContent = `${(file.size / 1024 / 1024).toFixed(2)} MB`;
            fileInfo.classList.add('visible');
            convertBtn.disabled = false;
            downloadBtn.classList.remove('visible');
            logArea.classList.remove('visible');
        }

        function log(message, type = '') {
            logArea.classList.add('visible');
            const line = document.createElement('div');
            line.className = `log-line ${type}`;
            line.textContent = message;
            logArea.appendChild(line);
            logArea.scrollTop = logArea.scrollHeight;
        }

        async function convert() {
            if (!selectedFile) return;

            convertBtn.disabled = true;
            progressContainer.classList.add('visible');
            progressFill.classList.add('indeterminate');
            statusText.textContent = 'Uploading and converting...';
            statusText.className = 'status';
            logArea.innerHTML = '';
            logArea.classList.add('visible');
            downloadBtn.classList.remove('visible');

            const formData = new FormData();
            formData.append('file', selectedFile);

            log('Uploading EPUB file...');
            try {
                const response = await fetch('/convert', {
                    method: 'POST',
                    body: formData
                });

                const result = await response.json();

                if (result.status === 'success') {
                    log('✓ Conversion completed!', 'success');
                    statusText.textContent = 'Conversion completed!';
                    statusText.className = 'status success';
                    progressFill.classList.remove('indeterminate');
                    progressFill.style.width = '100%';
                    downloadBtn.classList.add('visible');
                    downloadBtn.disabled = false;
                    downloadBtn.onclick = () => {
                        window.location.href = `/download/${result.filename}`;
                    };
                } else {
                    throw new Error(result.message || 'Conversion failed');
                }
            } catch (err) {
                log(`✗ Error: ${err.message}`, 'error');
                statusText.textContent = `Error: ${err.message}`;
                statusText.className = 'status error';
                progressFill.classList.remove('indeterminate');
                progressFill.style.width = '0%';
            } finally {
                convertBtn.disabled = false;
            }
        }

        convertBtn.addEventListener('click', convert);
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return HTML_TEMPLATE

@app.route('/convert', methods=['POST'])
def convert():
    if 'file' not in request.files:
        return jsonify({'status': 'error', 'message': 'No file uploaded'}), 400

    file = request.files['file']
    if file.filename == '' or not file.filename.lower().endswith('.epub'):
        return jsonify({'status': 'error', 'message': 'Invalid file. Please upload an EPUB file.'}), 400

    # Secure filename
    original_filename = secure_filename(file.filename)
    output_filename = Path(original_filename).with_suffix('.pdf').name

    # Save input file
    input_path = os.path.join(app.config['UPLOAD_FOLDER'], original_filename)
    file.save(input_path)

    output_path = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)

    try:
        # Read EPUB
        book = epub.read_epub(input_path)

        # Get metadata
        title_meta = book.get_metadata('DC', 'title')
        book_title = title_meta[0][0] if title_meta else "Converted Book"

        # Extract content from spine
        html_parts = []
        for item in book.get_items_of_type(ebooklib.ITEM_DOCUMENT):
            content = item.get_content().decode('utf-8')
            html_parts.append(f'<div class="chapter">{content}</div>')

        # Build HTML
        full_html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>{book_title}</title>
    <style>
        @page {{ margin: 2.5cm; size: A4; }}
        body {{ font-family: "DejaVu Serif", "Times New Roman", serif; font-size: 12pt; line-height: 1.6; color: #333; }}
        .chapter {{ page-break-before: always; margin-bottom: 2em; }}
        .chapter:first-child {{ page-break-before: avoid; }}
        h1, h2, h3, h4, h5, h6 {{ color: #2c3e50; page-break-after: avoid; }}
        p {{ margin: 0.5em 0; text-align: justify; }}
        img {{ max-width: 100%; height: auto; page-break-inside: avoid; }}
        .title-page {{ text-align: center; page-break-after: always; padding-top: 20%; }}
        .title-page h1 {{ font-size: 28pt; margin-bottom: 0.5em; }}
        .title-page .author {{ font-size: 14pt; color: #666; }}
    </style>
</head>
<body>
    <div class="title-page">
        <h1>{book_title}</h1>
        <div class="author">Converted from EPUB</div>
    </div>
    {''.join(html_parts)}
</body>
</html>
"""

        # Generate PDF
        font_config = FontConfiguration()
        html_doc = HTML(string=full_html)
        html_doc.write_pdf(output_path, font_config=font_config)

        return jsonify({
            'status': 'success',
            'message': 'Conversion completed',
            'filename': output_filename
        })

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/download/<filename>')
def download(filename):
    path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(filename))
    if not os.path.exists(path):
        return "File not found", 404
    return send_file(path, as_attachment=True, download_name=filename)

if __name__ == '__main__':
    print("Starting EPUB to PDF Converter on http://localhost:5001")
    app.run(host='127.0.0.1', port=5001, debug=True)