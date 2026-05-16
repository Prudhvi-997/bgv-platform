# nginx — per-portal reverse proxy

One config per portal. Each terminates HTTPS, serves the built React
bundle, and proxies **only** that portal's BFF path back to Django.

The boundary is enforced twice:
1. nginx — only `/api/<portal>/` is proxied; other API paths return 404.
2. BFF — the portal's permission class rejects sessions scoped to any
   other portal (CLAUDE.md Part 4.3).

The Candidate Portal lives behind a WAF (not modelled here) and is
deployed as an independent unit (CLAUDE.md RISK-01).
