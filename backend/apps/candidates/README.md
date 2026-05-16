# candidates

Candidate-facing domain — invitations, OTP auth, form state.

**Scope**
- Invitation tokens, OTP issuance and verification
- Candidate session lifecycle (OTP-only, no persistent account)
- Draft form state with auto-save (CLAUDE.md RFP 11.3, 11.4, 11.10)
- Re-submission flags from ops insufficiency marks

**Out of scope**
- Identity master record — `apps.compliance` (C-05 / RFP 17.5)
- Consent capture — `apps.compliance`
- Document uploads — `apps.documents`

**Invariants**
- The candidate BFF is the only BFF that can call into this app.
- Sessions are short-lived JWTs bound to device fingerprint hash.
- All candidate data submission events are immutably audit-logged.
