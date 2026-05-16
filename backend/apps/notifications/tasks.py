"""
Notification delivery tasks.

All channel sends (Email / SMS / WhatsApp) are Celery tasks.
Request handlers must use `delay()` / `apply_async()` — never call
the provider SDK inline. Enforces CLAUDE.md rule 4 (no blocking
notification sends in the request thread).
"""
