#!/usr/bin/env python3
"""
EPUB to PDF Converter
A simple desktop application to convert EPUB files to PDF format.

Features:
- Select EPUB file via file dialog
- Convert button to start conversion
- Progress/status messages
- Download/Save button for the converted PDF
- Auto-generates output filename (replaces .epub with .pdf)
"""

import os
import sys
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pathlib import Path

try:
    from ebooklib import epub
    from weasyprint import HTML, CSS
    from weasyprint.text.fonts import FontConfiguration
except ImportError as e:
    print(f"Missing dependencies: {e}")
    print("Please install: pip install ebooklib weasyprint")
    sys.exit(1)

# Robust reader: skips manifest entries that are missing from the archive
# (some EPUBs reference files like EPUB/toc01.html that are not present).
from epub_reader import read_epub


class EpubToPdfConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("EPUB to PDF Converter")
        self.root.geometry("600x450")
        self.root.resizable(False, False)

        # Variables
        self.input_file = None
        self.output_file = None
        self.conversion_thread = None

        self.setup_ui()

    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Title
        title_label = ttk.Label(main_frame, text="EPUB to PDF Converter",
                                font=("Helvetica", 18, "bold"))
        title_label.pack(pady=(0, 20))

        # File selection section
        file_frame = ttk.LabelFrame(main_frame, text="Select EPUB File", padding="15")
        file_frame.pack(fill=tk.X, pady=(0, 15))

        self.file_path_var = tk.StringVar()
        self.file_entry = ttk.Entry(file_frame, textvariable=self.file_path_var,
                                     state="readonly", width=50)
        self.file_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))

        browse_btn = ttk.Button(file_frame, text="Browse...", command=self.browse_file)
        browse_btn.pack(side=tk.RIGHT)

        # Output file section
        output_frame = ttk.LabelFrame(main_frame, text="Output PDF File", padding="15")
        output_frame.pack(fill=tk.X, pady=(0, 15))

        self.output_path_var = tk.StringVar()
        self.output_entry = ttk.Entry(output_frame, textvariable=self.output_path_var,
                                       state="readonly", width=50)
        self.output_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))

        # Convert button
        self.convert_btn = ttk.Button(main_frame, text="Convert to PDF",
                                       command=self.start_conversion,
                                       style="Accent.TButton")
        self.convert_btn.pack(pady=10, ipadx=20, ipady=5)

        # Progress bar
        self.progress = ttk.Progressbar(main_frame, mode="indeterminate")
        self.progress.pack(fill=tk.X, pady=(0, 10))

        # Status label
        self.status_var = tk.StringVar(value="Ready")
        self.status_label = ttk.Label(main_frame, textvariable=self.status_var,
                                       font=("Helvetica", 10), foreground="gray")
        self.status_label.pack(pady=(0, 10))

        # Download button (initially hidden)
        self.download_btn = ttk.Button(main_frame, text="Download PDF",
                                        command=self.download_pdf, state="disabled")
        self.download_btn.pack(pady=5, ipadx=20, ipady=5)

        # Log area
        log_frame = ttk.LabelFrame(main_frame, text="Conversion Log", padding="10")
        log_frame.pack(fill=tk.BOTH, expand=True)

        self.log_text = tk.Text(log_frame, height=8, wrap=tk.WORD, state="disabled")
        scrollbar = ttk.Scrollbar(log_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=scrollbar.set)
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def browse_file(self):
        file_path = filedialog.askopenfilename(
            title="Select EPUB File",
            filetypes=[("EPUB Files", "*.epub"), ("All Files", "*.*")]
        )
        if file_path:
            self.input_file = file_path
            self.file_path_var.set(file_path)

            # Auto-generate output filename
            input_path = Path(file_path)
            output_path = input_path.with_suffix(".pdf")
            self.output_file = str(output_path)
            self.output_path_var.set(str(output_path))

            self.log(f"Selected: {input_path.name}")
            self.status_var.set("Ready to convert")
            self.convert_btn.config(state="normal")
            self.download_btn.config(state="disabled")

    def log(self, message):
        self.log_text.config(state="normal")
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
        self.log_text.config(state="disabled")

    def start_conversion(self):
        if not self.input_file:
            messagebox.showwarning("Warning", "Please select an EPUB file first.")
            return

        # Disable UI during conversion
        self.convert_btn.config(state="disabled")
        self.download_btn.config(state="disabled")
        self.progress.start(10)
        self.status_var.set("Converting...")
        self.log_text.config(state="normal")
        self.log_text.delete(1.0, tk.END)
        self.log_text.config(state="disabled")

        # Run conversion in background thread
        self.conversion_thread = threading.Thread(target=self.convert_epub_to_pdf)
        self.conversion_thread.daemon = True
        self.conversion_thread.start()

    def convert_epub_to_pdf(self):
        try:
            self.log(f"Reading EPUB: {Path(self.input_file).name}")

            # Read EPUB (tolerant of manifest entries missing from the archive)
            book = read_epub(self.input_file)

            # Extract HTML content from all chapters
            html_content = []

            # Get metadata for title
            title = book.get_metadata('DC', 'title')
            book_title = title[0][0] if title else "Converted Book"
            self.log(f"Book title: {book_title}")

            # Process each item in the book
            spine_items = book.get_items_of_type(epub.ITEM_DOCUMENT)
            chapter_count = 0

            for item in spine_items:
                if item.get_type() == epub.ITEM_DOCUMENT:
                    chapter_count += 1
                    content = item.get_content().decode('utf-8')
                    # Wrap content in a div for better styling
                    html_content.append(f'<div class="chapter">{content}</div>')
                    self.log(f"Processed chapter {chapter_count}")

            # Create complete HTML document
            full_html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>{book_title}</title>
    <style>
        @page {{
            margin: 2.5cm;
            size: A4;
        }}
        body {{
            font-family: "DejaVu Serif", "Times New Roman", serif;
            font-size: 12pt;
            line-height: 1.6;
            color: #333;
        }}
        .chapter {{
            page-break-before: always;
            margin-bottom: 2em;
        }}
        .chapter:first-child {{
            page-break-before: avoid;
        }}
        h1, h2, h3, h4, h5, h6 {{
            color: #2c3e50;
            page-break-after: avoid;
        }}
        p {{
            margin: 0.5em 0;
            text-align: justify;
        }}
        img {{
            max-width: 100%;
            height: auto;
            page-break-inside: avoid;
        }}
        .title-page {{
            text-align: center;
            page-break-after: always;
            padding-top: 20%;
        }}
        .title-page h1 {{
            font-size: 28pt;
            margin-bottom: 0.5em;
        }}
        .title-page .author {{
            font-size: 14pt;
            color: #666;
        }}
    </style>
</head>
<body>
    <div class="title-page">
        <h1>{book_title}</h1>
        <div class="author">Converted from EPUB</div>
    </div>
    {''.join(html_content)}
</body>
</html>
"""

            self.log(f"Generating PDF: {Path(self.output_file).name}")

            # Generate PDF
            font_config = FontConfiguration()
            html_doc = HTML(string=full_html)
            html_doc.write_pdf(self.output_file, font_config=font_config)

            self.log("✓ Conversion completed successfully!")

            # Update UI on main thread
            self.root.after(0, self.conversion_complete)

        except Exception as e:
            error_msg = f"Conversion failed: {str(e)}"
            self.log(f"✗ {error_msg}")
            self.root.after(0, lambda: self.conversion_error(error_msg))

    def conversion_complete(self):
        self.progress.stop()
        self.status_var.set("Conversion completed!")
        self.convert_btn.config(state="normal")
        self.download_btn.config(state="normal")
        messagebox.showinfo("Success", f"PDF created successfully!\nSaved to: {self.output_file}")

    def conversion_error(self, error_msg):
        self.progress.stop()
        self.status_var.set("Conversion failed")
        self.convert_btn.config(state="normal")
        messagebox.showerror("Error", error_msg)

    def download_pdf(self):
        if not self.output_file or not os.path.exists(self.output_file):
            messagebox.showwarning("Warning", "PDF file not found.")
            return

        save_path = filedialog.asksaveasfilename(
            title="Save PDF As",
            defaultextension=".pdf",
            initialfile=Path(self.output_file).name,
            filetypes=[("PDF Files", "*.pdf"), ("All Files", "*.*")]
        )

        if save_path:
            try:
                import shutil
                shutil.copy2(self.output_file, save_path)
                self.log(f"PDF saved to: {save_path}")
                messagebox.showinfo("Success", f"PDF saved to:\n{save_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save: {str(e)}")


def main():
    root = tk.Tk()

    # Style configuration
    style = ttk.Style()
    style.configure("Accent.TButton", font=("Helvetica", 11, "bold"))

    app = EpubToPdfConverter(root)
    root.mainloop()


if __name__ == "__main__":
    main()