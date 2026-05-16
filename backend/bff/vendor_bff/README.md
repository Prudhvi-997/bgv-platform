# vendor_bff

Backend-for-Frontend for the Vendor Portal.

**Layer 1 RBAC** — `IsVendorPortalSession` rejects any session whose
token is not scoped to this portal. This is the primary boundary: a
session from any other portal cannot reach URLs under this BFF
regardless of domain RBAC (CLAUDE.md Part 4.3).

Domain logic is **not** implemented here. The BFF aggregates calls
into the `apps.*` services, projects the result for this portal's UI,
and returns it.
