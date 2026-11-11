# EPUB to PDF Converter — Error Log

This file collects every error encountered by this project, its root cause,
and the fix applied. Add a new entry here whenever a new error shows up,
so the history stays in one place.

---

## ERR-001 — Missing manifest item crashes EPUB read

**Date:** 2026-11-11

**Symptom:**

```
KeyError: "There is no item named 'EPUB/toc01.html' in the archive"
```

Conversion failed immediately when uploading certain EPUB files (e.g.
`sanet.st_9798341661622_Fixed.epub`).

**Root cause:**

The EPUB's OPF manifest declares `EPUB/toc01.html`, but that file is not
actually present in the zip archive (the book ships `EPUB/toc.ncx`
instead). ebooklib reads the manifest eagerly and raises `KeyError` on
the first missing entry, aborting the whole read before any content is
extracted.

**Fix:**

Added `epub_reader.py`, a wrapper around `ebooklib`'s reader. When a
manifest item is missing from the archive, it returns a minimal valid
XHTML document (an empty `<nav>` with an `<ol>`) instead of raising, so
the TOC parser stays happy and the rest of the book loads normally.

Both apps now call `read_epub(...)` instead of `epub.read_epub(...)`:

- `app.py` (Flask web app)
- `epub_to_pdf.py` (Tkinter desktop app)

**Status:** Fixed and verified. The same EPUB now converts to a 1.3 MB PDF.

---

## ERR-002 — Empty replacement content breaks the nav parser

**Date:** 2026-11-11

**Symptom:**

```
lxml.etree.ParserError: Document is empty
```

Appeared while debugging ERR-001, when the workaround returned empty bytes
for the missing item.

**Root cause:**

ebooklib passes the missing item's content to its HTML/TOC parser. Empty
bytes are not valid XML, so lxml rejects them.

**Fix:**

Return well-formed XHTML (see `epub_reader.py`) instead of empty bytes.

**Status:** Fixed (was an intermediate step in the ERR-001 fix).

---

## ERR-003 — Nav replacement without a `<nav>` element breaks TOC parsing

**Date:** 2026-11-11

**Symptom:**

```
AttributeError: 'NoneType' object has no attribute 'iterchildren'
```

Appeared while debugging ERR-001, when the workaround returned a `<head>`
only, with no `<nav>` element.

**Root cause:**

ebooklib's TOC parser looks for a `<nav>` element and calls methods on
it. With no `<nav>` present, the lookup returns `None` and the code crashes.

**Fix:**

The replacement XHTML includes `<nav id="toc" epub:type="toc"><ol></ol></nav>`.

**Status:** Fixed (was an intermediate step in the ERR-001 fix).

---

## ERR-004 — Invalid escape sequence in embedded JS regex (latent)

**Date:** 2026-11-11

**Symptom:**

```
SyntaxWarning: "\." is an invalid escape sequence. Such sequences will not
work in the future. Did you mean "\\."?
```

Printed at startup from `app.py` line 263.

**Root cause:**

The HTML template contains a JavaScript regex literal written inside a
Python string: `file.name.replace(/\.epub$/i, '.pdf')`. Python treats
`\.` as an escape sequence, which is deprecated and will become a
`SyntaxError` in a future Python version.

**Fix:**

Not yet applied. Currently harmless, but should be fixed by writing the
regex with a raw string or escaping the backslash. See `app.py:263`.

**Status:** Open / latent. Low priority today, but will break in a future
Python release.

---

## How to add a new error

1. Copy the section format above.
2. Assign the next ERR-NNN number.
3. Fill in Date, Symptom, Root cause, Fix, Status.
4. If the fix changes code, note the file and line.