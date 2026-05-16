"""
Vendors domain — vendor organisations, users, assignments, SLA.

Desk vendors and field agents share this domain. Field agents access
the Field Agent App via the same vendor auth surface but with a
distinct mobile session profile (CLAUDE.md Part 5.6).

Subprocessor registry (RFP 22.3) — vendors with DPA status — also
lives here.

Models intentionally not implemented yet — scaffolding only.
"""
from django.db import models  # noqa: F401
