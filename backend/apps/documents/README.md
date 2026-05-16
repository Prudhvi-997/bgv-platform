# documents

Evidence store + multi-format document processing.

**Accepted formats** (CLAUDE.md Part 4.7.1)

| Format | Pipeline |
|---|---|
| PDF, JPG, PNG | Virus scan → OCR → fraud detection |
| DOCX, XLSX | Virus scan → LibreOffice → PDF → OCR (original preserved) |
| ZIP | Validate structure → extract → route each child |

**Limits**
- 10 MB per file
- ZIP: ≤ 50 MB extracted, ≤ 20 files, no nested ZIPs

**Invariants**
- All conversion / extraction runs in Celery — never inline.
- Originals are preserved alongside converted PDFs.
- Every document gets an audit hash (SHA-256 of content at upload)
  for tamper detection.
- Per-upload audit row written via `apps.compliance` (immutable).
