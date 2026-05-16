# reporting

**THIS DOMAIN NEVER READS FROM THE OPERATIONAL DB.**

Bounded context for analytics, dashboards, BI feeds, and scheduled
reports. Bound to the `reporting` database via the DB router in
`config/db_router.py`.

Architectural rule (CLAUDE.md Part 4.8):

> All analytics queries, dashboard data fetches, BI connector feeds,
> report generation, KPI calculations, and MIS data exports MUST read
> from the Reporting DB. Never from the operational DB.

Any query in this app that touches `default` is a build-breaking
architectural defect.

**Scope**
- Denormalised read models (case summary, daily TAT metrics,
  SLA breach events, vendor performance, etc.)
- API endpoints serving dashboard widgets and scheduled reports
- BI connector (RFP 18.5) provisioning

**Out of scope**
- The Reporting Workbench live case state — that's `apps.cases`
  served via `ops_bff` from the operational DB.
- Any write path other than the sync mechanism (log shipping / CDC).
