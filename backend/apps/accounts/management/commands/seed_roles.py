"""
seed_roles — idempotently provision the platform's built-in roles.

Run on a freshly migrated database (or any time the role catalog
changes). Existing rows are updated, not duplicated.

The role catalog mirrors the spec for the accounts implementation
and CLAUDE.md Part 5.1 (per-portal role definitions).
"""
from __future__ import annotations

from django.core.management.base import BaseCommand

from apps.accounts.models import Role
from apps.accounts.tenant_context import unfiltered_scope


BUILT_IN_ROLES = [
    # Ops Portal
    {
        "name": "ops_reviewer",
        "portal": "ops",
        "permissions": [
            "cases.view",
            "cases.update",
            "verification.view",
            "verification.update",
        ],
    },
    {
        "name": "ops_lead",
        "portal": "ops",
        "permissions": [
            "cases.view",
            "cases.update",
            "cases.assign",
            "verification.view",
            "verification.update",
            "vendors.view",
        ],
    },
    {
        "name": "adjudicator",
        "portal": "ops",
        "permissions": [
            "cases.view",
            "cases.adjudicate",
            "verification.view",
        ],
    },
    {
        "name": "qc_reviewer",
        "portal": "ops",
        "permissions": [
            "cases.view",
            "verification.view",
            "verification.qc_review",
        ],
    },

    # Client Portal
    {
        "name": "client_viewer",
        "portal": "client",
        "permissions": ["cases.view_own_tenant"],
    },
    {
        "name": "client_initiator",
        "portal": "client",
        "permissions": [
            "cases.view_own_tenant",
            "cases.initiate",
        ],
    },
    {
        "name": "client_admin",
        "portal": "client",
        "permissions": [
            "cases.view_own_tenant",
            "cases.initiate",
            "cases.manage_users",
        ],
    },

    # Vendor Portal
    {
        "name": "vendor_verifier",
        "portal": "vendor",
        "permissions": [
            "verification.view_assigned",
            "verification.submit",
        ],
    },
    {
        "name": "vendor_lead",
        "portal": "vendor",
        "permissions": [
            "verification.view_assigned",
            "verification.submit",
            "verification.review",
        ],
    },

    # Super Admin Portal
    {
        "name": "platform_admin",
        "portal": "admin",
        "permissions": ["*"],
    },
    {
        "name": "privacy_officer",
        "portal": "admin",
        "permissions": [
            "compliance.view",
            "compliance.manage",
            "dsar.manage",
        ],
    },

    # Candidate Portal
    {
        "name": "candidate",
        "portal": "candidate",
        "permissions": [
            "candidate.view_own",
            "candidate.submit",
        ],
    },
]


class Command(BaseCommand):
    help = "Idempotently seed the built-in role catalog."

    def handle(self, *args, **options):
        created, updated = 0, 0
        # Role rows are global (no tenant) but the manager is non-tenant
        # too — `unfiltered_scope` is a belt-and-braces guard against
        # future refactors that flip a model onto the TenantManager.
        with unfiltered_scope():
            for spec in BUILT_IN_ROLES:
                obj, was_created = Role.objects.update_or_create(
                    name=spec["name"],
                    portal=spec["portal"],
                    defaults={"permissions": spec["permissions"]},
                )
                if was_created:
                    created += 1
                else:
                    updated += 1
        self.stdout.write(
            self.style.SUCCESS(
                f"Roles seeded — created: {created}, updated: {updated}, "
                f"total in catalog: {len(BUILT_IN_ROLES)}."
            )
        )
