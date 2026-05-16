"""
Reporting domain — CQRS read side.

This app is routed exclusively to the `reporting` database
(see `config/db_router.py`). It NEVER queries the operational DB.

The Reporting DB is populated by an out-of-band sync mechanism
(CLAUDE.md Part 4.8.3):
    Phase 1 — SQL Server log shipping (or MySQL replica + CDC)
    Phase 2 — Debezium / managed CDC into the Reporting DB
    Phase 3 — Cloud-native managed CDC (DMS)

Read models here are denormalised and pre-aggregated. PII is
anonymised at the schema level — hash tokens + last-4 only.

Models intentionally not implemented yet — scaffolding only.
"""
from django.db import models  # noqa: F401
