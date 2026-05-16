# notifications

Multi-channel async notification delivery.

**Scope**
- Templates per locale (CLAUDE.md Part 4.10)
- Channel routing: Email / SMS / WhatsApp
- Retry chain with delivery receipts
- Per-message audit (delivery status drives SLA pause logic)

**Architectural rules**
- Channels are invoked from Celery tasks only — never inline.
- Delivery failure events are surfaced on the Ops dashboard
  (CLAUDE.md 6.1.30 Delivery Status & Failure Management).
- SLA pause / resume on Undeliverable is automatic.
