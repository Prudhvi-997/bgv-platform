"""
Celery application.

All notification delivery and document processing run as Celery tasks
(CLAUDE.md rule 4 & 5). Request handlers schedule work here; they never
block on SMTP / SMS / WhatsApp / LibreOffice / OCR.
"""
import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.dev")

app = Celery("kcheck")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
