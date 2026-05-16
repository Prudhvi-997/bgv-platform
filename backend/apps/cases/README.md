# cases

Case lifecycle and state machine — the core operational entity.

**Scope**
- Case records with `tenant_id`, `initiation_mode`, `package`, status
- 24-state state machine (CLAUDE.md GAP-9)
- Three-track SLA timers (Client / Internal / Vendor — CLAUDE.md C-03)
- Case workbench domain operations consumed by `ops_bff`

**Out of scope**
- Check execution — lives in `apps.verification`
- Candidate-facing form state — lives in `apps.candidates`
- Documents — lives in `apps.documents`

**Invariants**
- Every state transition: single DB txn = (status update + audit event).
- Optimistic locking via `version` field prevents concurrent transitions.
- Custom fields per tenant flow through `apps.cases` (CLAUDE.md C-08).
