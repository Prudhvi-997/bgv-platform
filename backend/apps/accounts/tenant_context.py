"""
Per-request tenant context.

Multi-tenant isolation (CLAUDE.md RISK-02) is enforced at the ORM layer by
the `TenantManager`. To do that, the manager needs to know "which tenant
is this request for?" without the view code remembering to pass it in.

We use a `ContextVar` rather than a thread-local so the value is also
correct under Django's async views. The middleware
(`apps.accounts.middleware.TenantContextMiddleware`) pushes the tenant
from the request's JWT and clears it on response.

There are two escape hatches, both deliberately explicit:

    1. `Model.objects.unfiltered()` — return an unfiltered queryset for
       contexts that legitimately span tenants (Super Admin, cross-tenant
       audits). Every call site should be reviewed.

    2. `with unfiltered_scope(): ...` — context manager that flips the
       contextvar flag for the duration of the block. Used by management
       commands and migrations.
"""
from __future__ import annotations

import contextlib
import uuid
from contextvars import ContextVar
from typing import Iterator, Optional

_tenant_var: ContextVar[Optional[uuid.UUID]] = ContextVar(
    "kcheck_current_tenant", default=None
)
_unfiltered_var: ContextVar[bool] = ContextVar(
    "kcheck_unfiltered_mode", default=False
)


def get_current_tenant() -> Optional[uuid.UUID]:
    """Return the tenant UUID for the current request, or None."""
    return _tenant_var.get()


def set_current_tenant(tenant_id: Optional[uuid.UUID]):
    """
    Set the tenant for the current context. Returns a token that the
    middleware uses to reset the var when the request finishes.
    """
    return _tenant_var.set(tenant_id)


def reset_current_tenant(token) -> None:
    """Restore the previous tenant context value."""
    _tenant_var.reset(token)


def is_unfiltered_mode() -> bool:
    """True if the caller has opted out of tenant filtering."""
    return _unfiltered_var.get()


@contextlib.contextmanager
def tenant_scope(tenant_id: Optional[uuid.UUID]) -> Iterator[None]:
    """Context manager that pins the tenant for the enclosed block."""
    token = _tenant_var.set(tenant_id)
    try:
        yield
    finally:
        _tenant_var.reset(token)


@contextlib.contextmanager
def unfiltered_scope() -> Iterator[None]:
    """
    Context manager that disables tenant filtering for the enclosed block.

    Use sparingly: any cross-tenant access is a high-impact security
    decision (CLAUDE.md RISK-02). Acceptable cases include data
    migrations, the `seed_roles` management command, and Super Admin
    cross-tenant reports.
    """
    token = _unfiltered_var.set(True)
    try:
        yield
    finally:
        _unfiltered_var.reset(token)
