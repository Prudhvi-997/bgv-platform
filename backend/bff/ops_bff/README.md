# ops_bff

Backend-for-Frontend for the Operations Portal.

**Layer 1 RBAC** — the `IsOpsPortalSession` permission rejects any
session whose token is not scoped to the Ops portal. This is the
primary boundary: a candidate / client / vendor token cannot reach
any URL under `/api/ops/` regardless of domain RBAC.

Domain logic is **not** implemented here. The BFF aggregates calls
into `apps.cases`, `apps.verification`, `apps.compliance`, etc.,
projects the result for the Ops UI, and returns it.
