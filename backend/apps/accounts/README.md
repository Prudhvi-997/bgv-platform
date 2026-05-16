# accounts

Auth, tenant management, two-layer RBAC.

**Scope**
- Users (KPMG ops, client, vendor, super admin)
- Tenants (multi-tenant isolation — CLAUDE.md Part 4.3)
- Roles & permissions
- Session / JWT issuance
- Layer 1 RBAC primitives consumed by BFFs

**Out of scope**
- Candidate OTP authentication — lives in `apps.candidates`
  (candidates have no persistent account; OTP-only).

**Architectural invariants**
- Every multi-tenant model has `tenant_id`.
- Layer 1 (BFF) and Layer 2 (domain service) RBAC checks both fire on
  every request; one is never sufficient.
