"""
Document processing Celery tasks.

All conversion and extraction work runs here. Request handlers
schedule tasks and return immediately with a job ID
(CLAUDE.md rule 5).
"""
