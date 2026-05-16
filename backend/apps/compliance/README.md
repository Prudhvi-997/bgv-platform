# compliance

Consent, audit log, DSAR, retention, candidate identity master.

**The most architecturally sensitive domain in the platform.**

**Scope**
- Consent capture, versioning, withdrawal (CLAUDE.md RFP 15.1)
- Immutable audit event log (CLAUDE.md RISK-07)
- DSAR / right-to-correction / right-to-erasure workflows
- Retention policy & purge schedule
- Candidate identity master record (CLAUDE.md C-05 / RFP 17.5)
- Data catalog / lineage / masking matrix (C-05)

**Invariants — non-negotiable**
1. `ImmutableModel` and any subclass (including `AuditEvent`)
   rejects mutation through the ORM. Migrations that ALTER these
   tables must be reviewed by the Compliance Architect.
2. The DB user used by the application must lack UPDATE/DELETE
   privileges on `consent_*` and `audit_*` tables. Application-layer
   enforcement is the second line of defence; DB-level is the first.
3. Consent receipts are written to immutable object storage (S3
   Object Lock / Azure Blob Immutability) at signature time. The
   DB row is the index; the receipt PDF is the artefact.
