"""
Cases domain — case records, state machine, initiation modes.

State transitions are persisted (CLAUDE.md RISK-11): every transition
is a single DB transaction that updates case status and writes an
audit event. State machines do not live only in application memory.

Initiation modes (CLAUDE.md Part 5.2, C-01):
    - candidate_portal        (F1, default)
    - client_direct_entry     (F2, non-candidate, client HR enters data)
    - client_bulk_prefilled   (F3, bulk pre-filled upload)
    - ops_manual              (F4, ops staff manual entry)
    - hrms_auto_push          (F5, HRMS/ATS API push)

Models intentionally not implemented yet — scaffolding only.
"""
from django.db import models  # noqa: F401
