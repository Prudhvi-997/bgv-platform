"""
Accounts domain — users, tenants, roles, sessions.

Two-layer RBAC (CLAUDE.md Part 4.3):
    Layer 1 — Portal access control, enforced by BFF middleware.
    Layer 2 — Feature access control, enforced by domain services.

Models intentionally not implemented yet — scaffolding only.
"""
from django.db import models  # noqa: F401
