# KCheck BGV Platform

Greenfield monorepo for the KPMG KCheck Background Verification platform.

**Architecture reference:** see [`CLAUDE.md`](./CLAUDE.md). It is the single source of
truth for portal boundaries, bounded contexts, RBAC, audit rules, and
data-residency policy. Read it before changing anything structural.

## Monorepo layout

```
backend/        Django + DRF — shared domain services and per-portal BFFs
frontend/       React apps — one per portal, shared component library
infra/          Docker, nginx, deployment configuration
docs/           Reference docs (CLAUDE.md is at repo root)
```

### Backend bounded contexts (`backend/apps/`)
- `accounts` — Auth, two-layer RBAC (BFF + domain)
- `cases` — Case lifecycle, state machine, initiation modes
- `verification` — Employment, Education, Legal, Address, KYC checks
- `candidates` — Candidate portal logic, OTP auth, form state
- `vendors` — Vendor management, assignment, SLA tracking
- `notifications` — Email / SMS / WhatsApp async delivery + retry
- `reporting` — **CQRS reporting domain — reads ONLY from the Reporting DB**
- `compliance` — Consent (append-only), audit log (immutable), DSAR, DPDP/GDPR
- `documents` — Evidence store, ZIP extraction pipeline, DOCX/XLSX → PDF

### Per-portal BFFs (`backend/bff/`)
Each BFF enforces the portal security boundary. A candidate session token
cannot call ops_bff endpoints regardless of RBAC permissions (CLAUDE.md
Part 4.3, Layer 1).

- `ops_bff` — Operations Portal
- `client_bff` — Client Portal
- `candidate_bff` — Candidate Portal (public-internet-facing — hardened)
- `vendor_bff` — Vendor Portal
- `admin_bff` — Super Admin Portal

### Frontend portals (`frontend/`)
Independently deployable React apps sharing a component library.

- `shared` — Design tokens + base components
- `ops-portal` — Desktop-first, dense queue UI
- `client-portal` — Tenant-scoped
- `candidate-portal` — PWA, mobile-first (deployed independently)
- `vendor-portal` — Queue-focused
- `admin-portal` — Config-heavy, low-traffic

## Architectural rules (enforced from day one)

1. The `reporting` app must **never** query the operational DB. The Django
   database router (`backend/config/db_router.py`) routes all `reporting`
   queries to the `reporting` connection.
2. Per-portal BFFs are the **primary** security boundary. RBAC is the
   secondary defence — both layers must be present.
3. `compliance.AuditEvent` is **append-only**. The model rejects `save()`
   for existing rows and disallows `delete()` entirely.
4. All notification delivery runs via Celery tasks. Request handlers
   never call SMTP / SMS / WhatsApp directly.
5. Document processing (ZIP extraction, DOCX/XLSX → PDF) runs in Celery
   workers — never in the request thread.
6. Every multi-tenant model carries a `tenant_id`. Cross-tenant access
   is blocked at the queryset layer.
7. The reporting DB is **read-only** to the application. Only the sync
   mechanism (log shipping / CDC) writes to it.

## Local development

```bash
cp .env.example .env
docker compose up -d operational_db reporting_db redis
# (backend / celery_worker / celery_beat once images are built)
```

Detailed service descriptions live next to each app's `README.md`.
