"""
Notifications domain — multi-channel async delivery.

All notification delivery is async (CLAUDE.md rule 4). Request
handlers never call SMTP / SMS / WhatsApp directly — they enqueue
a Celery task in `tasks.py`.

Fallback chain (CLAUDE.md RISK-06):
    WhatsApp (T+0) → SMS (T+5min) → Email (T+15min)

Delivery failures pause the relevant SLA clock.

Models intentionally not implemented yet — scaffolding only.
"""
from django.db import models  # noqa: F401
