# Dockerfiles

Two backend images:

- `Dockerfile.backend` — Django runserver / WSGI host. No LibreOffice.
- `Dockerfile.celery`  — Celery worker. Includes LibreOffice for the
  DOCX / XLSX → PDF conversion pipeline (CLAUDE.md Part 4.7.3).

The web image deliberately does not ship LibreOffice — only Celery
workers should be able to invoke heavy document conversion. This
keeps the request thread guaranteed-non-blocking on conversion work
(CLAUDE.md rule 5).
