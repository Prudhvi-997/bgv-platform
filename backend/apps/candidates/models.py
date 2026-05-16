"""
Candidates domain — candidate-side state.

Candidates have no persistent account. Authentication is OTP-only
(WhatsApp / SMS / Email) per invitation. Session state, draft form
data, and re-submission flags live here.

Identity master records (cross-case consolidation) live in
`apps.compliance` (CLAUDE.md C-05) — not here.

Models intentionally not implemented yet — scaffolding only.
"""
from django.db import models  # noqa: F401
