# @kcheck/shared

Design tokens + base React components consumed by every portal.

**Versioning matters.** A change in this package propagates to all
five portals. Breaking changes require coordinated rollout across:

- ops-portal
- client-portal
- candidate-portal (public-facing — extra care)
- vendor-portal
- admin-portal

Keep the public surface lean. If a component is portal-specific,
it belongs in that portal — not here.
