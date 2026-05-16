"""
Documents domain — evidence store + processing pipeline.

Accepted formats (CLAUDE.md Part 4.7.1):
    PDF, DOCX, XLSX, JPG, PNG, ZIP

Processing pipelines (CLAUDE.md Part 4.7.2 / 4.7.3):
    - DOCX/XLSX → server-side LibreOffice conversion to PDF
    - ZIP → extract, validate (no nested zips, ≤20 files, ≤50MB),
      route each child through its format pipeline
    - All uploads → virus scan, OCR, fraud detection

All processing runs as Celery tasks in `tasks.py`. The request
thread never blocks on conversion or extraction (CLAUDE.md rule 5).

Models intentionally not implemented yet — scaffolding only.
"""
from django.db import models  # noqa: F401
