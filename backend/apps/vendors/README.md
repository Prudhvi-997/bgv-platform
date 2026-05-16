# vendors

Vendor management, assignment, and SLA tracking.

**Scope**
- Vendor orgs, capability matrix (check type × geography)
- Vendor users (Verifier / Team Lead / Manager)
- Assignment lifecycle and acknowledgement
- Vendor-track SLA (one of the three tracks in C-03)
- Subprocessor / DPA register exposed in Super Admin (RFP 22.3)
- Revalidation queue (CLAUDE.md GAP-19)

**Out of scope**
- Check execution — `apps.verification`
- Notification delivery to vendors — `apps.notifications`

**Invariants**
- DPA must be Active before vendor can receive assignments.
- Vendor session cannot reach Ops or Client BFFs.
