#!/usr/bin/env python3
"""
Robust EPUB reader that tolerates malformed archives.

Some EPUBs declare files in their OPF manifest that are not actually
present in the archive (for example ``EPUB/toc01.html``). ebooklib's
default reader raises ``KeyError`` when it tries to load such items,
which breaks the whole conversion. This module wraps the reader so
missing manifest entries are skipped instead of failing.

It returns a minimal, valid XHTML document for any missing item, so
downstream code (e.g. the nav/TOC parser) still receives well-formed
input.
"""

import ebooklib
from ebooklib import epub
from ebooklib.reader import EpubReader

# Minimal valid XHTML returned for any manifest item that is missing
# from the archive. The empty <nav> with an <ol> keeps ebooklib's TOC
# parser happy without inventing any content.
_MISSING_ITEM_CONTENT = (
    b'<?xml version="1.0" encoding="UTF-8"?>'
    b'<html xmlns="http://www.w3.org/1999/xhtml">'
    b'<head><title>missing</title></head>'
    b'<body><nav id="toc" epub:type="toc"><ol></ol></nav></body>'
    b'</html>'
)


def read_epub(path):
    """Read an EPUB file, skipping manifest entries missing from the archive.

    Mirrors ``ebooklib.epub.read_epub`` but never raises ``KeyError`` for
    a manifest item that is not present in the zip.
    """
    original_read_file = EpubReader.read_file

    def _read_file_safe(self, name):
        try:
            return original_read_file(self, name)
        except KeyError:
            # The OPF manifest references a file that is not in the archive.
            # Skip it instead of aborting the whole read.
            return _MISSING_ITEM_CONTENT

    EpubReader.read_file = _read_file_safe
    try:
        return epub.read_epub(path)
    finally:
        EpubReader.read_file = original_read_file