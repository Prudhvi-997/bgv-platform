# KCheck frontend

Five React portals plus a shared component library. Each portal is
independently deployable (CLAUDE.md Part 4.1, RISK-01).

## Portals

| Portal | Path | Deployment profile |
|---|---|---|
| Operations | `ops-portal/` | Internal VPN-gated, dense desktop UI |
| Client | `client-portal/` | Tenant-scoped, peak 700 concurrent (CLAUDE.md C-04) |
| Candidate | `candidate-portal/` | Public internet, mobile-first PWA, WAF-fronted |
| Vendor | `vendor-portal/` | External, IP-restricted, queue-focused |
| Super Admin | `admin-portal/` | Internal, low-traffic, configuration-heavy |
| Shared | `shared/` | Component library + design tokens |

**Each portal talks only to its own BFF** under `/api/<portal>/`. The
candidate portal does not import ops portal code, route definitions, or
secrets. Independent build pipelines are mandatory for the candidate
portal (CLAUDE.md RISK-01).

## Workspace

This is a Yarn / npm workspaces monorepo. Per-portal commands run
from each portal's directory.
