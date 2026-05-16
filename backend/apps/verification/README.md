# verification

Check execution domain — one check record per verification within a case.

**Scope**
- Per-check status, outcome, evidence references, SLA timers
- Integrations with external sources (EPFO, NSDL, DigiLocker, court DBs)
- AI signals attached to checks (face match, fraud flags, etc.)
- Site visit sub-component (CLAUDE.md GAP-3)

**Out of scope**
- Vendor assignment routing — lives in `apps.vendors`
- Document files themselves — lives in `apps.documents`

**Invariants**
- Check outcomes can be declared only after consent is valid for the
  applicable purpose (validated via `apps.compliance`).
- AI signals never auto-decide adverse outcomes — human review gate
  is mandatory (CLAUDE.md RISK-08).
