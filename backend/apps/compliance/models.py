"""
Compliance domain — consent (append-only), audit log (immutable),
DSAR, retention, candidate identity master.

Two foundational invariants (CLAUDE.md RISK-03 and RISK-07):

1. Consent records are append-only. A new consent version is a new
   row; existing rows are never updated or deleted.

2. Audit events are immutable. The `AuditEvent` base below rejects
   `save()` on an existing row and disallows `delete()` entirely.

These invariants are enforced at the model layer here so that no
ORM caller — application code or migration — can mutate audit
state. Database-level enforcement (revoking UPDATE/DELETE from the
app's DB user on these tables) is the second line of defence.

Models intentionally not implemented in full — base abstraction
provided so downstream tables inherit the invariants.
"""
from django.db import models


class ImmutableModel(models.Model):
    """
    Base class for any append-only / write-once domain table.

    Subclasses gain:
        - `save()` raises if the row already exists in the DB.
        - `delete()` is disabled.
        - There is no built-in update path through the ORM.

    DB-level enforcement is mandatory in addition to this — the
    application's DB user must lack UPDATE/DELETE privileges on
    immutable tables.
    """

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if self.pk is not None:
            raise PermissionError(
                f"{self.__class__.__name__} is immutable — "
                "existing rows cannot be modified."
            )
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        raise PermissionError(
            f"{self.__class__.__name__} is immutable — "
            "rows cannot be deleted."
        )


class AuditEvent(ImmutableModel):
    """
    Platform-wide immutable audit event.

    Every state-changing action across every portal writes one row
    here. CLAUDE.md Part 4.4 (audit isolation) and RISK-07
    (queryability at scale) inform the design.

    Fields are deliberately minimal at the scaffolding stage —
    full schema lands with the audit pipeline implementation.
    """

    class Meta:
        abstract = True  # concrete table lands with the implementation
