# KCheck BGV Platform — Enterprise Product Architecture Review
## Complete Solution Architecture, Portal IA, Traceability Matrix & Implementation Blueprint

**Document Classification:** Confidential — Architecture Review  
**Platform:** KCheck Background Verification Platform — Modernization  
**Client:** KPMG India  
**Governing Source:** BGV_RFP_24_Apr_26.xlsx  
**Workflow Reference:** KCheck_Complete_Workflow_Reference_v2_Gap_Closed_Full_Aligned.docx  
**Prepared By:** Enterprise Architecture Review  
**Version:** 1.0

---

# TABLE OF CONTENTS

1. Part 1 — Architecture Review: Portal Structure Analysis
2. Part 2 — Portal Decision Matrix
3. Part 3 — Final Recommended Product Structure
4. Part 4 — Enterprise Product Architecture Strategy
5. Part 5 — Complete Portal Information Architecture
6. Part 6 — Page Design Depth
7. Part 7 — Domain Boundary Analysis
8. Part 8 — Critical Architectural Risks
9. Part 9 — RFP Requirement Traceability Mapping

---

# PART 1 — ARCHITECTURE REVIEW: PORTAL STRUCTURE ANALYSIS

## 1.1 Proposed Architecture Under Review

The proposed architecture defines five portals:

1. Super Admin Portal
2. Client Portal
3. Vendor Portal
4. Candidate Portal
5. Operations Portal

## 1.2 Architectural Evaluation Framework

Before evaluating correctness, we must establish what drives portal boundaries in an enterprise BGV platform. A portal boundary is justified when **at least three** of the following conditions are true:

- **Security boundary**: The actor must not see another actor's data, workflow state, or system internals
- **Workflow boundary**: The actor owns a distinct workflow phase that has no overlap with other portals
- **SLA ownership boundary**: The actor is independently accountable for time-bound outcomes
- **Compliance boundary**: The actor's data handling is governed by a distinct legal obligation
- **UX boundary**: The actor's task model is fundamentally different (mobile-first vs. desktop ops vs. guest access)
- **Trust boundary**: The actor is external (third-party) vs. internal (KPMG employee)
- **Audit boundary**: The actor's actions must be separately logged for regulatory accountability

## 1.3 Critical Analysis: Are 5 Portals Correct?

### VERDICT: 5 portals are **necessary but incompletely defined**.

The 5 proposed portals are architecturally justified. However, the architecture has two problems:

**Problem 1 — Missing boundary portals**: Several external actors (Employer, University, Field Agent) currently fall into no portal or are incorrectly assumed to be absorbed into the Vendor Portal. This creates compliance and workflow risks.

**Problem 2 — Super Admin is conflated**: The Super Admin Portal conflates KPMG platform governance with client-specific configuration. These are distinct operational concerns with different access security requirements.

### Deep Analysis of Each Proposed Portal

#### Portal 1: Super Admin Portal — Analysis

**What it must cover:**
- Platform-level configuration (not client-level)
- Tenant provisioning, onboarding new client organizations
- Global rule engine configuration
- AI model governance, threshold management
- System health, audit log access, incident management
- Cross-tenant analytics (anonymized)
- License/billing module management

**Critical challenge:** The RFP (Section 12 — Admin) defines two distinct administrative concerns:
- **Platform admin** (KPMG internal IT/ops governance) — creates tenants, manages global policies
- **Client admin** (client-side HR/IT admins) — configures packages, forms, users within their tenant

These are currently conflated in the Super Admin concept. A client admin logging into the same portal as KPMG's platform admin creates a **tenant isolation risk** (RFP 14.10 — Tenant Isolation). They must be separated at the UX layer, even if backed by the same RBAC system.

**Verdict:** Super Admin Portal is justified but must be strictly scoped to KPMG-internal platform governance only. Client-side admin functions must live inside the Client Portal under an elevated "Client Admin" role.

#### Portal 2: Client Portal — Analysis

**What it must cover:**
- Case initiation and bulk upload (RFP 10.1, 10.15)
- Candidate invitation management
- Real-time case status tracking (RFP 12, 18)
- Report download and adjudication review
- Client-specific package configuration (RFP 12.1, 12.2)
- Billing and invoice visibility (RFP 22, 18.10)
- User management within their tenant
- ATS/HRIS integration configuration (RFP 13.1)
- Color-code matrix configuration (RFP 12.11)
- SLA monitoring for their cases (RFP 10.5, 18.1)

**Security boundary:** Clients must never see another client's data, cases, or configurations. This is a hard multi-tenancy boundary enforced at both data and UI layers.

**Workflow boundary:** Clients own the initiation phase, receive outputs, and in some workflows participate in adjudication approval. This is a distinct workflow role.

**Compliance boundary:** Clients are data controllers under DPDP/GDPR for their employees. Their consent management, data access, and retention configuration is legally separate from KPMG's processor role.

**Verdict:** Client Portal is fully justified. It should include a Client Admin sub-role for configuration, distinct from a Client Viewer/Initiator role.

#### Portal 3: Vendor Portal — Analysis

**What it must cover:**
- Assignment intake and acknowledgment (RFP 4, 6, 7)
- Evidence submission and verification updates
- SLA tracking against vendor commitments
- Vendor-specific case queue management
- Communication with KPMG ops
- Vendor performance scorecard visibility (RFP 19, 21)

**Critical challenge:** The Vendor Portal concept is currently too broad. The RFP distinguishes between:
- **Verification vendors** (third-party BGV agencies doing physical/court/employment checks)
- **Technology subprocessors** (AI vendors, database providers — no UI needed, API only)
- **Field agents** doing physical address verification (mobile-first, GPS-tracked workflows)

Field agents doing physical address verification (RFP 7.2, 7.3 — GPS-timestamped evidence, neighbor verification) cannot use a desktop web portal. They need a **mobile-first field agent app** with offline capability, GPS capture, photo upload, and signature capture. Forcing them into a desktop vendor portal creates an operational failure.

**Verdict:** Vendor Portal is justified for desk-based vendors. Field agents require a separate mobile app or a mobile-optimized lightweight module branched from the Vendor Portal.

#### Portal 4: Candidate Portal — Analysis

**What it must cover:**
- OTP-based authentication (no persistent account)
- Dynamic form fill (personal, employment, education, identity)
- Document upload with quality feedback
- Biometric/liveness capture
- Consent and e-signature
- Real-time status tracking
- Re-submission on insufficiency
- Dispute initiation
- Support channel access
- WhatsApp deep-link compatibility (RFP 11.13)

**Security boundary:** Candidates are external, untrusted actors. They have zero visibility into KPMG operations, vendor activity, or other candidates. This is the hardest security boundary in the system.

**UX boundary:** Candidates are mobile-first, one-time users with no institutional knowledge of BGV. The UX must be guided, simple, and error-tolerant — completely unlike the dense operational UI of the Ops Portal.

**Compliance boundary:** Candidate consent, data rights (access, correction, erasure under DPDP/GDPR — RFP 15.6, 15.7, 15.8), and FCRA-style disclosures (RFP 16.1) apply exclusively to this interface.

**Trust boundary:** Candidates are the primary fraud attack surface — biometric spoofing, document fraud, synthetic identity. AI fraud controls are concentrated here.

**Verdict:** Candidate Portal is fully justified and must remain physically separate from all other portals. It must be independently deployable, independently scalable (600–700 daily users), and hardened against public internet threats.

#### Portal 5: Operations Portal — Analysis

**What it must cover:**
- Case queue management (RFP 10.13)
- Verification execution across all check types
- Adjudication workbench (RFP 10.9)
- QA/QC workflow (RFP 10.14)
- Insufficiency management and candidate remarks
- SLA monitoring and breach escalation (RFP 10.5, 21.5)
- Vendor assignment and coordination (RFP 10.19)
- Report generation and sign-off
- Dispute management (RFP 10.10)
- AI reviewer assist panel (RFP 2.15)
- Fraud intelligence dashboard (RFP 2.24)

**Security boundary:** Ops users are internal KPMG staff. They see the complete case file including sensitive PII, verification outcomes, AI flags, and vendor responses. No external actor should ever access this portal.

**Workflow boundary:** Ops owns the core verification execution phase — the longest and most complex phase in the BGV lifecycle.

**SLA ownership:** Ops is accountable for verification TAT, insufficiency resolution time, QC turnaround, and report delivery SLAs.

**Verdict:** Operations Portal is fully justified. It is the most complex portal and should not be merged with any other.

## 1.4 Missing Portal Boundaries

The following actors are NOT adequately addressed in the 5-portal model and require explicit architectural decisions:

### Employer Verification Interface
When KPMG sends employment verification requests to former employers, the current model assumes email/offline communication. The RFP explicitly calls for "digital employer outreach, configurable digital outreach templates, and secure employer response channel" (RFP 4.1, 4.2). This requires a **lightweight secure response interface** — not a full portal, but a tokenized web form that employers access via a one-time link to confirm employment details. This is architecturally distinct from the Vendor Portal.

### University/Board Verification Interface
Similar to employer outreach — RFP 5.1 (University/board direct verification) implies a structured digital response mechanism. Currently assumed to be email-only. A lightweight verification response form is needed.

### Field Agent Mobile App
RFP 7.2, 7.3 — GPS-timestamped physical evidence, photo authenticity checks, neighbor verification workflow. Desktop vendor portal is architecturally inappropriate. A PWA or native mobile app is required.

### Auditor/Legal Read-Only Access
RFP 12.9 (Audit views), 18.3 (Audit packs), 15.10 (DPIA support) — regulators or internal legal/risk teams may need read-only access to audit evidence, consent logs, and adjudication records. This is a compliance-critical boundary that must not share the main Ops Portal interface.

---

# PART 2 — PORTAL DECISION MATRIX

## 2.1 Core 5 Portals

| Portal | Decision | Justification | RFP References | Risks if Merged |
|---|---|---|---|---|
| **Super Admin Portal** | KEEP — but restrict scope to KPMG platform governance only | Platform tenant management, global rule engine, AI model governance, system health, cross-tenant audit. Distinct from client admin functions. | RFP 12.1–12.12, 14.10, 19.1–19.11, 21.1–21.7 | Merging with Ops Portal creates tenant isolation breach. Client admins must never reach platform-level config. |
| **Client Portal** | KEEP — expand to include Client Admin role | Clients are data controllers, own case initiation, receive outputs. Multi-tenancy demands hard data segregation. Client Admin sub-role handles package config, users, billing visibility. | RFP 10.1, 11.1–11.14, 12.1–12.12, 13.1–13.10, 18.1–18.10, 22.1–22.6 | Merging with Ops Portal exposes internal verification operations to clients — catastrophic compliance and confidentiality failure. |
| **Vendor Portal** | KEEP — split into Desk Vendor Portal + Field Agent Mobile App | Desk vendors and field agents have irreconcilably different UX needs. Field agents are GPS-tracked, mobile-first, offline-capable. Desk vendors are desktop, queue-based. | RFP 4.1–4.15, 6.1–6.8, 7.1–7.6, 10.19 | Merging field agents into desk portal = GPS/photo workflow failure, 0% field adoption, physical verification breakdown. |
| **Candidate Portal** | KEEP — highest priority, independent deployment | External untrusted actor, fraud attack surface, mobile-first, consent/compliance owner, independently scalable. Never merge. | RFP 11.1–11.14, 15.1–15.11, 2.1–2.24, 3.1–3.10 | Any merge exposes operations to public internet attack surface. GDPR consent isolation requirement violated. |
| **Operations Portal** | KEEP — highest complexity, internal only | Core verification execution, adjudication, QA/QC, SLA governance, AI-assisted review. Internal KPMG staff only. Most feature-rich portal. | RFP 10.1–10.19, 2.1–2.24, 18.1–18.10, 21.1–21.7 | Merging with Client Portal exposes verification internals, vendor identities, adjudication notes to clients — legally and operationally unacceptable. |

## 2.2 Additional Actors — Portal Decisions

| Actor/Portal | Decision | Justification | RFP References | Risk if Not Addressed |
|---|---|---|---|---|
| **Employer Portal** | LIGHTWEIGHT EXTERNAL MODULE — tokenized one-time-link web form | RFP explicitly requires "secure employer response channel" and "structured employer response forms." Not a full portal — employers are occasional, untrusted, one-task actors. | RFP 4.1, 4.2, 4.14 | Without it: employment verification remains email/offline. TAT increases 3–5 days. RFP 4.1 requirement unmet. |
| **Referee Portal** | LIGHTWEIGHT EXTERNAL MODULE — same tokenized model as Employer | Reference checks (RFP 4.12) require structured questionnaire responses from referees. One-time access via secure link. | RFP 4.12, 4.13 | Without it: unstructured phone/email references, no audit trail, no structured data capture. |
| **University/Board Interface** | LIGHTWEIGHT EXTERNAL MODULE — structured digital response form | RFP 5.1 (direct university verification) implies digital workflow. Universities are batch-respondents, not persistent users. | RFP 5.1, 5.2, 5.5 | Without it: manual email verification, 7–10 day TAT per check, high error rate. |
| **Risk/Legal Portal** | RBAC MODULE inside Ops Portal — "Risk/Legal" role | Risk and legal reviewers work within the same case lifecycle as ops. They need elevated read access to adjudication notes, consent logs, waiver approvals, DPIA records. Not a separate portal — RBAC with restricted write permissions suffices. | RFP 1.4, 6.4–6.8, 15.10, 16.1–16.2 | Creating separate portal duplicates case data views. RBAC module is sufficient and avoids fragmentation. |
| **Auditor Portal** | LIGHTWEIGHT READ-ONLY MODULE — separate URL, separate session | Regulators and external auditors need access to audit packs (RFP 18.3), consent logs, adjudication records. Must be physically separate from Ops Portal — different URL, read-only, session-time-limited, IP-restricted. | RFP 12.9, 18.3, 15.10, 16.2 | Without it: audit evidence must be manually exported and shared — unacceptable for a GDPR/DPDP-compliant platform. |
| **Field Agent App** | SEPARATE MOBILE APP (PWA or native) | GPS capture, photo with timestamp, neighbor verification, offline capability, signature capture. Architecturally impossible on desktop portal. | RFP 7.2, 7.3, 7.4, 7.5, 7.6 | Without it: physical address verification cannot meet RFP 7.2–7.3 GPS/timestamp requirements. Entire address verification module fails. |
| **Investigator Portal** | RBAC MODULE inside Ops Portal — "Senior Investigator" role | Investigators handle complex fraud cases, entity graph analysis, and deep discrepancy investigation. They work within the case lifecycle — elevated access to AI fraud signals, entity graphs, sanction results. RBAC inside Ops Portal is sufficient. | RFP 2.9–2.24, 6.1–6.8 | Separate portal creates case data duplication and fragmented workflow. |

---

# PART 3 — FINAL RECOMMENDED PRODUCT STRUCTURE

## 3.1 Complete Recommended Architecture

| Component | Type | Recommendation | Reason |
|---|---|---|---|
| **Super Admin Portal** | Full Portal — Internal | KEEP — KPMG platform governance only | Tenant provisioning, global rule engine, AI model governance, system health, cross-tenant audit. Distinct security perimeter from all other portals. |
| **Client Portal** | Full Portal — External (Tenant-Scoped) | KEEP — add Client Admin role | Multi-tenant, data controller boundary, case initiation, report receipt, billing visibility, ATS integration config. |
| **Operations Portal** | Full Portal — Internal | KEEP — highest priority build | Core verification engine, adjudication workbench, QA/QC, SLA governance, AI reviewer assist. Internal KPMG staff. |
| **Candidate Portal** | Full Portal — External (Public) | KEEP — independent deployment, independent scaling | Public-internet-facing, fraud attack surface, mobile-first, consent-owner, GDPR/DPDP compliance surface. |
| **Vendor Portal (Desk)** | Full Portal — External (Vendor-Scoped) | KEEP — desk-based verification vendors | Assignment management, evidence submission, SLA tracking, vendor scorecard. Secure but not public-internet hardened. |
| **Field Agent App** | Mobile App (PWA or native) | ADD — not currently in proposed architecture | GPS-tracked physical verification, photo evidence, offline sync, neighbor verification. Architecturally incompatible with desktop portal. |
| **Employer Response Module** | Lightweight External Access Module | ADD — tokenized web form | One-time-link structured employment confirmation. No persistent account. Read candidate-submitted data, respond via form. |
| **Referee Response Module** | Lightweight External Access Module | ADD — tokenized web form | One-time-link structured reference questionnaire. Same architecture as Employer module. |
| **University Response Module** | Lightweight External Access Module | ADD — tokenized web form | One-time-link structured academic verification response. Batch-capable for large institutions. |
| **Auditor Read-Only Module** | Lightweight Restricted Module — separate URL | ADD — compliance requirement | IP-restricted, session-time-limited, read-only access to audit packs, consent logs, adjudication records for regulators/external auditors. |
| **Risk/Legal Role** | RBAC Module inside Ops Portal | DEFINE explicitly within Ops Portal | Elevated read access + waiver/adjudication approval permissions. Not a separate portal. |
| **Investigator Role** | RBAC Module inside Ops Portal | DEFINE explicitly within Ops Portal | Deep fraud investigation access, entity graph, AI signals. Elevated Ops Portal role. |
| **Client Admin Role** | RBAC Module inside Client Portal | DEFINE explicitly within Client Portal | Package configurator, user management, form builder, holiday list, color-code matrix. Elevated Client Portal role. |
| **QA/QC Reviewer Role** | RBAC Module inside Ops Portal | DEFINE explicitly | Second-level QC sampling, error tagging, feedback loops. Restricted write access — cannot override first reviewer. |

---

# PART 4 — ENTERPRISE PRODUCT ARCHITECTURE STRATEGY

## 4.1 Architecture Decision

### Recommended Strategy: **Shared Backend, Domain-Driven Bounded Contexts, Multi-Shell Frontend**

This is not a microfrontend-first architecture, nor a monolith. It is a **domain-driven platform with role-shell frontends sharing a single API platform**.

### Why Not Single Frontend with RBAC?

A single frontend with route-based RBAC fails for KCheck because:

1. **Security surface**: The Candidate Portal is public-internet-facing and must be independently deployable and scalable. Packaging it with the internal Ops Portal in a single deployable unit is a security anti-pattern.

2. **UX incompatibility**: Candidate UX is mobile-first, wizard-driven, single-task. Ops UX is dense, multi-panel, queue-based, desktop-heavy. Sharing a component library is fine; sharing a deployed frontend is not.

3. **Scaling independence**: Candidate Portal handles 600–700 simultaneous sessions during peak. Ops Portal handles ~150–200 concurrent internal users. These have fundamentally different scaling profiles and CDN/caching requirements.

4. **Audit isolation**: Candidate Portal actions (consent capture, form submission) must be independently auditable as the primary GDPR/DPDP evidence surface. Coupling it to the ops codebase risks audit contamination.

### Why Not Full Microfrontend?

Full microfrontend (independent build, deploy, runtime per feature) introduces:

1. **Excessive operational overhead** for a team modernizing from ASP.NET Web Forms — the complexity jump is too large.
2. **Shared state management complexity** across module federation boundaries — problematic for case-context that spans multiple workflow phases.
3. **Performance regression** from runtime module loading — unacceptable for the Candidate Portal on mobile networks.

### Recommended Architecture Pattern

```
┌─────────────────────────────────────────────────────────────────┐
│                    API GATEWAY / BFF LAYER                       │
│         (Per-portal Backend-for-Frontend APIs)                   │
└──────────────┬──────────────┬──────────────┬────────────────────┘
               │              │              │
    ┌──────────▼──┐  ┌────────▼──┐  ┌───────▼──────────┐
    │  Domain     │  │  Domain   │  │  Domain          │
    │  Services   │  │  Services │  │  Services        │
    │  (Case,     │  │  (Verify, │  │  (Consent,       │
    │  Workflow,  │  │  Vendor,  │  │  Compliance,     │
    │  Notif.)    │  │  QC)      │  │  Audit)          │
    └─────────────┘  └───────────┘  └──────────────────┘
```

**Shared Backend:**
- Single domain service layer with bounded contexts (Case Management, Verification, Consent/Compliance, Vendor Orchestration, Notification, **Reporting** ← owns all analytics, dashboards, BI feeds, and report generation — served from dedicated Reporting DB, never the operational DB [C-09], AI/ML Integration, Audit)
- REST + Event-driven internal communication
- One database per domain context (not per portal)

**Multiple Frontend Shells:**
- Candidate Portal — independent deployment, React PWA, mobile-optimized
- Ops Portal — internal deployment, React desktop-first, dense UI
- Client Portal — tenant-scoped, React, moderate complexity
- Vendor Portal — external deployment, React, queue-focused
- Super Admin Portal — internal, React, low-traffic, configuration-heavy
- Field Agent App — React Native PWA, offline-capable, GPS-enabled

**Per-Portal BFF (Backend-for-Frontend):**
- Each portal has its own API gateway layer that aggregates domain service calls
- The BFF layer enforces the security boundary — a candidate BFF never exposes ops-internal APIs
- This is the primary enforcement mechanism for portal data isolation, not just RBAC

## 4.2 Maintainability Implications

| Concern | Implication |
|---|---|
| Shared component library | All portals share a design system and base component library. Changes to shared components propagate everywhere — requires versioning. |
| Domain service independence | Each domain service (Case, Verify, Consent, etc.) can be evolved independently. Adding a new check type doesn't require changes to the Candidate Portal. |
| Frontend shell independence | Candidate Portal can be deployed independently without touching Ops Portal. Critical for security patching of the public-facing surface. |
| BFF layer evolution | Each portal's BFF evolves with that portal's needs. The Client Portal BFF can add new aggregation endpoints without affecting the Ops BFF. |

## 4.3 RBAC Implications

The RBAC model must operate at two layers:

**Layer 1 — Portal Access Control (BFF level):** Which portal can a session token access? Enforced by the BFF. A vendor session token cannot call Ops BFF APIs regardless of RBAC permissions.

**Layer 2 — Feature Access Control (Domain service level):** Within a portal, which features/data can a user access? Enforced by domain services. A Client Viewer cannot call case-adjudication APIs even if they somehow bypass the BFF.

This two-layer RBAC is essential for RFP 12.7 (Role-based access control), 14.10 (Tenant isolation), and compliance with DPDP/GDPR data minimization (RFP 15.4).

## 4.4 Audit Implications

Every portal action flows through a common audit event bus. The audit log is:

- Immutable (write-once) — RFP 14.12
- Correlated by Case ID, User ID, Session ID, Timestamp
- Portal-tagged (which portal originated the action)
- Stored in a separate audit database, never the operational DB

The separation of portal BFFs means each portal's API calls are independently tagged, making it possible to produce "candidate-only audit pack" or "ops-only audit trail" for regulatory purposes (RFP 18.3).

## 4.5 Deployment Implications

| Portal | Deployment Model | Scaling Strategy |
|---|---|---|
| Candidate Portal | Public cloud, CDN-fronted, auto-scaling | Horizontal pod autoscaling on form-submission and document-upload endpoints |
| Ops Portal | Internal cloud/VPN-gated, fixed capacity | Vertical scaling with read replicas for queue views |
| Client Portal | Public cloud, tenant-isolated, CDN-fronted, auto-scaling | **Peak concurrent: 700 sessions (PPTX baseline — same order of magnitude as Candidate Portal). [C-04 \| RFP 21.1, 21.6]** Endpoint-specific scaling required: (1) **Case list / status queries** — served exclusively from reporting read replica; never hits primary operational DB. (2) **Report downloads** — CDN-cached pre-generated PDFs; large bulk-ZIP downloads served from dedicated file-serving nodes, isolated from API nodes. (3) **Bulk upload processing** — async job queue with separate worker pool; file validation and case creation are background jobs, never blocking API response. Tenant-based rate limiting applied per client org to prevent one large tenant saturating shared infrastructure. **Load test target (RFP 21.6): sustain 700 concurrent sessions with p95 < 2s on case-list and status endpoints.** |
| Vendor Portal | Public cloud, IP-restricted by vendor registration | Moderate scaling; batch assignment endpoints |
| Super Admin Portal | Internal VPN-only, low-traffic | Minimal scaling; admin operations are low-volume |
| Field Agent App | Progressive Web App, offline-capable, sync-on-connect | Edge caching; offline queue with sync on connectivity restore |

## 4.6 Scaling Implications

The dominant scaling concern is the Candidate Portal (600–700 daily users with document upload and AI OCR processing). The architecture must ensure:

1. Document upload endpoints scale independently from form-submission endpoints
2. AI processing (OCR, liveness, biometric match) is asynchronous — never blocks candidate form submission
3. The Operations Portal queue view (150–200 concurrent ops users) is served from a read replica, never the primary write database
4. Notification delivery (email + SMS + WhatsApp) is fully async, failure-tolerant with retry queues
5. **The Client Portal is a second high-concurrency surface and must not be treated as low-traffic. [C-04 | RFP 21.1, 21.6 | Legacy: PPTX "Clients: 1000+ Credentials (700)"]** Peak concurrent sessions reach 700 — comparable in raw concurrency to the Candidate Portal's daily unique user count. Three Client Portal endpoints carry disproportionate load and require independent scaling treatment:
   - **Case list / status queries:** Hundreds of concurrent users refreshing case status during active hiring drives. Must be served from the reporting read replica with aggressive query result caching (TTL: 30–60 seconds). A cache miss at 700 concurrent users hitting the primary DB is a direct availability risk.
   - **Report downloads:** Bulk ZIP downloads (50–200 BGV reports per export) generate large file transfers. Pre-generate report ZIPs asynchronously and serve via CDN or object storage pre-signed URLs — never stream directly from the application server.
   - **Bulk upload processing:** Excel validation and case creation for 500-row uploads is compute-intensive. Route to a background job queue (separate worker pool from API servers). Upload endpoint returns a job ID immediately; client polls for completion status. Never process synchronously in the request thread.
   - **Load test target (RFP 21.6):** Validate Client Portal sustains 700 concurrent sessions with p95 response time < 2s on case-list, status, and report-inbox endpoints under peak load.

---

## 4.7 Platform-Wide Document Format Policy

> **C-02 | RFP 11.5, 10.16 | Legacy source: PPTX "Doc Types Supported: PDF, XL, Word, JPG, PNG and Zip"**
> This section is the single source of truth for accepted document formats across ALL portals
> and ALL upload surfaces (Candidate Portal, Ops Portal, Client Portal, Vendor Portal, Field Agent App).
> All page-level format references in Parts 5 and 6 derive from this table.

### 4.7.1 Accepted Formats Table

| Format | Extensions | Use Cases in BGV | Max Size | Special Handling |
|---|---|---|---|---|
| **PDF** | `.pdf` | Primary format — all documents | 10 MB | In-browser preview, OCR, fraud detection |
| **Image** | `.jpg`, `.jpeg`, `.png` | ID documents, address proofs, photos, field agent evidence | 10 MB (auto-compressed to <3 MB on mobile before upload) | Quality score, OCR, presentation attack detection |
| **Word** | `.docx` | Experience letters, offer letters, relieving letters, declarations (from employers, universities) | 10 MB | Virus scan → server-side convert to PDF → OCR on converted PDF. Original file preserved in evidence store alongside converted PDF. |
| **Excel** | `.xlsx`, `.xls` | Payslips, salary statements, HRMS exports, bank statements | 10 MB | Virus scan → server-side convert to PDF → optional structured data extraction. Original file preserved alongside converted PDF. |
| **ZIP** | `.zip` | Bundled university responses, bundled employer document packs, multi-document submissions | 50 MB extracted (max 20 files per ZIP, no nested ZIPs) | Full extraction pipeline — see 4.7.2. |

### 4.7.2 ZIP Extraction Pipeline

ZIP is a container, not a document. Every ZIP must go through a dedicated extraction pipeline before its contents can be reviewed:

```
ZIP file received (any upload surface)
        │
        ▼
[1] Structure validation
    ├── Contains nested ZIP? → REJECT immediately
    │   Error: "Nested ZIP files are not supported. Extract and re-upload."
    ├── Extracted file count > 20? → REJECT
    │   Error: "ZIP contains [N] files. Maximum is 20 files per ZIP."
    └── Extracted total size > 50 MB? → REJECT
        Error: "Extracted content is [N] MB. Maximum is 50 MB per ZIP."
        │
        ▼
[2] Virus scan
    ├── Scan entire ZIP archive
    ├── Scan each extracted file individually
    └── Any infection → QUARANTINE entire ZIP, reject, notify ops
        │
        ▼
[3] Extract all files
        │
        ▼
[4] Per-file format routing
    ├── PDF → standard PDF pipeline (preview + OCR + fraud detection)
    ├── JPG / PNG → image pipeline (quality + OCR)
    ├── DOCX → Word pipeline (convert to PDF + OCR)
    ├── XLSX → Excel pipeline (convert to PDF + data extract)
    └── Any other format → log as "unsupported format in ZIP", skip,
        notify ops: "ZIP contained [N] unsupported files (e.g. .exe, .mp4)"
        │
        ▼
[5] Evidence Store records created
    Parent record: ZipPackage — filename, total files, extraction status, upload_source
    Child records: one per extracted file — linked to parent ZIP via parent_zip_id
    Each child record processed independently (OCR, fraud detection, quality score)
        │
        ▼
[6] UI presentation
    Document Table shows ZIP parent row with [View Extracted Files] action
    Expanding shows child rows — each with individual [View] / format-specific actions
```

### 4.7.3 Word and Excel Processing Pipeline

```
DOCX / XLSX file received
        │
        ▼
[1] Virus scan (Word macros and Excel macros are primary malware vectors)
    Infection detected → QUARANTINE, reject, notify ops
        │
        ▼
[2] Server-side PDF conversion
    Tool: LibreOffice (headless) — handles both DOCX and XLSX
    DOCX → PDF (preserves formatting, headers, signatures)
    XLSX → PDF (each sheet becomes a page; multi-sheet handled)
    Conversion failure → flag document: "Conversion failed — download original for review"
        │
        ▼
[3] OCR on converted PDF
    (Same OCR pipeline as native PDF — extracts text, identifies fields)
    XLSX: optional structured data extraction (company name, salary figures, dates)
        │
        ▼
[4] Evidence Store
    original_file_path: stores .docx / .xlsx (never deleted)
    converted_pdf_path: stores generated PDF (for viewing)
    Both paths present → viewer uses converted_pdf_path for display
        │
        ▼
[5] UI actions available
    [View as PDF] → opens converted PDF in inline viewer
    [Download Original] → downloads the original .docx / .xlsx
```

### 4.7.4 Evidence Store Document Record Schema

Every document — regardless of format or upload surface — creates one record with this structure:

```
{
  id:                   uuid,
  case_id:              uuid,
  check_id:             uuid (nullable — null if case-level doc),
  original_format:      enum(pdf, docx, xlsx, jpg, png, zip, zip_child),
  original_file_path:   string (always populated — original preserved),
  converted_pdf_path:   string (populated for docx, xlsx; same as original for pdf),
  parent_zip_id:        uuid (null unless this is a ZIP-extracted child),
  upload_source:        enum(candidate, ops, vendor, employer, university, field_agent, client_hr),
  initiation_mode:      string (mirrors case initiation_mode — for traceability),
  ai_quality_score:     float (0–1, null for xlsx/zip),
  fraud_flag:           boolean,
  fraud_flag_reasons:   string[] (populated if fraud_flag = true),
  ocr_extracted:        json (field-value pairs),
  upload_timestamp:     datetime,
  uploader_id:          uuid,
  audit_hash:           string (SHA-256 of file content at time of upload — tamper detection)
}
```

### 4.7.5 Format-Specific Actions in UI (All Portals)

| Format | Viewer Action | Secondary Action | Notes |
|---|---|---|---|
| PDF | [View] → inline PDF viewer | — | Multi-page, zoom/pan/rotate, OCR overlay |
| JPG / PNG | [View] → image viewer | — | Zoom/pan, fraud overlay |
| DOCX | [View as PDF] → converted PDF viewer | [Download Original] | Clearly labelled "Converted PDF — original Word file available to download" |
| XLSX | [View as PDF] → converted PDF viewer | [Download Original] | Clearly labelled "Converted PDF — original Excel file available to download" |
| ZIP (parent) | [View Extracted Files] → expands to child list | [Download ZIP] | Child rows each have their own format-specific actions |
| ZIP (child) | Per-child format action (same as above table) | — | Child row shows: "Extracted from: [zip filename]" |

---
---

## 4.8 Reporting Architecture Decision

> **C-09 | RFP 18.1, 18.5, 18.6, 18.7, 21.4**
> **Legacy source: MOM "Separate reporting DB — synced every ~1 minute — avoids production DB access"**
> **PPTX: "MIS Database (Realtime Sync) — ETL Tool, Native Database Application, Log Shipping"**
>
> This is a named, binding architectural decision. All analytics, dashboards, BI feeds, and report
> generation MUST use the Reporting DB. Direct queries to the operational database for any
> reporting or analytics purpose are a build-breaking architectural defect.

### 4.8.1 What the Reporting Domain Owns

The Reporting Domain is a first-class bounded context. It owns:

| Owned | NOT Owned |
|---|---|
| Pre-aggregated read models for all dashboards | Live case state (Case Management domain) |
| Denormalised case summaries for fast list queries | Audit events (Audit Domain) |
| Historical time-series for trend analysis | Document content (Evidence Store) |
| KPI/KRI computed metrics (RFP 18.6) | Active candidate form state (Candidate Domain) |
| BI-queryable anonymised schemas | Real-time case write operations |
| API usage analytics data (RFP 18.8) | |
| Scheduled report generation outputs | |

### 4.8.2 The Isolation Rule (Binding on All Developers)

```
THE RULE:

All analytics queries, dashboard data fetches, BI connector feeds,
report generation, KPI calculations, and MIS data exports
MUST read from the Reporting DB. Never from the operational DB.

The only exception: a user viewing their own ACTIVE real-time state
(candidate viewing live form, ops on live case workbench) reads from
the operational DB for real-time accuracy. Everything else — analytics,
history, trends, dashboards, reports — goes through the Reporting DB.
```

### 4.8.3 Sync Mechanism — Per Deployment Phase

```
PHASE 1 — On-Prem (SQL Server):
  Mechanism:  SQL Server Log Shipping (native — matches legacy PPTX pattern)
  Lag target: < 60 seconds
  Monitoring: Log shipping job status in Super Admin > System Health

PHASE 2 — Hybrid (containerised):
  Mechanism:  CDC (Change Data Capture) via Debezium or cloud-native equivalent
  Transport:  Message queue (Kafka / Azure Service Bus)
  Lag target: < 30 seconds

PHASE 3 — Cloud-Native:
  Mechanism:  Managed CDC (Azure DMS / AWS DMS)
  BI mode:    Power BI Premium DirectQuery supported
  Lag target: < 15 seconds
```

### 4.8.3A CDC Pipeline Detail — Phases 2 and 3 [C-14 | RFP 21.4]

> This sub-section specifies the CDC pipeline for Phases 2 and 3 in coding-ready detail.
> Phase 1 (SQL Server log shipping) is operationally straightforward and fully specified
> by the SQL Server native documentation — no additional detail needed here.

**Tables on the CDC Watch List**

CDC does not replicate every table. Only case-data tables producing analytics-relevant events
are watched. Security, session, and transient tables are explicitly excluded:

```
WATCHED (operational DB → Reporting DB):
  ✅ cases               Case status, outcome, SLA state, initiation_mode
  ✅ checks              Per-check status, assigned user/vendor, completed timestamp
  ✅ sla_events          Breach events, pause/resume, amber/red threshold crossings
  ✅ evidence            Document uploads, AI quality scores, fraud flags
  ✅ communications      Outreach events, channel, delivery status
  ✅ adjudications       Outcome declarations, rationale hash, waiver decisions
  ✅ vendor_assignments  Vendor assigned, response received, vendor SLA events
  ✅ audit_events        Aggregated audit volume only (for compliance dashboards)
  ✅ custom_attributes   Client custom field values per case (C-08 fields)

NOT WATCHED (excluded from CDC):
  ❌ sessions            Transient authentication state — not needed in Reporting DB
  ❌ otp_codes           Security — never replicated anywhere
  ❌ consent_raw         Raw PII — consent statistics replicated but not raw records
  ❌ temp_processing     Internal processing state — not analytical
  ❌ feature_flags       Configuration — not analytical
```

**Event Types and Handling**

```
INSERT event:
  Trigger: New case created, new check record, new evidence uploaded, etc.
  Action:  Stream processor creates new row in relevant Reporting DB read model(s).

UPDATE event:
  Trigger: Case status changes, check completed, adjudication declared, etc.
  Action:  Stream processor updates existing row in Reporting DB read model(s).
           Multiple read models may be affected by a single UPDATE.
           e.g., a case status change to "Complete" updates:
             → case_summary_view (status field)
             → daily_tat_metrics (records TAT if newly completed)
             → sla_breach_events (if completion was after breach)
             → client_pipeline_summary (case count by status)

SOFT-DELETE event:
  Trigger: Record marked deleted_at (never hard-deleted in operational DB).
  Action:  Stream processor marks row inactive in Reporting DB (NOT deleted).
           Inactive rows are preserved for historical analytics.
           Dashboards filter out inactive rows unless explicitly showing history.

SCHEMA CHANGE event:
  Trigger: A new custom field registered (C-08 Custom Field Registry).
  Action:  Stream processor dynamically adds the custom_attribute to
           the case_summary_view and exports schema. No code change needed.
```

**Stream Processor Responsibilities**

The stream processor is NOT a simple data replication job. It transforms operational
events into denormalised Reporting DB read models:

```
FOR EACH CDC EVENT CONSUMED FROM QUEUE:

1. IDENTIFY AFFECTED READ MODELS
   One operational event may update multiple read models simultaneously.
   The processor maintains a mapping: table + event_type → [read_model_list]

2. APPLY DENORMALISATION
   Join related tables as needed to produce the full read model row.
   The Reporting DB schema is denormalised — not a copy of the operational schema.
   e.g., case_summary_view needs: case fields + check outcomes + client name +
         package name + SLA state — joined from 5+ operational tables.
   The processor resolves joins using data from the event + lookups to Reporting DB.

3. APPLY PII ANONYMISATION
   Before writing to Reporting DB:
     Raw Aadhaar → SHA-256 hash token + last-4 display
     Raw PAN → SHA-256 hash token + last-4 display
     Raw mobile → SHA-256 hash token + last-4 display
     Raw email → SHA-256 hash token (no display version)
   Hash tokens are consistent (same input → same hash) enabling joins across events.
   Hash salt: per-tenant salt stored in Super Admin config (not in Reporting DB).

4. WRITE TO REPORTING DB
   Upsert (INSERT or UPDATE) the affected read model rows.
   All writes are idempotent — re-processing the same event produces same result.
   Idempotency key: operational_record_id + event_sequence_number.

5. ACKNOWLEDGE MESSAGE IN QUEUE
   ONLY after successful write to Reporting DB.
   If write fails → message remains in queue → retry after configurable delay.
   This guarantees at-least-once delivery with no data loss.
```

**Error Handling and Lag Monitoring**

```
NORMAL OPERATION:
  CDC event → queue → processor → Reporting DB
  Phase 2 lag: < 30 seconds end-to-end

LAG SPIKE (burst write scenario):
  Cause:   500 bulk cases created at once (Client Portal bulk pre-filled upload)
  Effect:  Queue depth spikes → processor backlog → Reporting DB lag increases
  Alert:   Queue depth > 1000 messages → Super Admin System Health alert
  Impact:  Dashboard banner: "Analytics data may be slightly delayed" (amber — per 4.8.7)
  Recovery: Processor auto-scales (containerised) or catches up as burst subsides.
            No data loss — queue acts as durable buffer throughout.

PROCESSOR FAILURE:
  Cause:   Stream processor crashes or becomes unreachable
  Effect:  Messages accumulate in queue (durable — not lost)
  Alert:   "Reporting DB sync processor unhealthy — [N] events pending" → Super Admin
  Recovery: Processor restarts, re-reads from last committed queue offset.
             All pending events processed in order. No gaps.

REPORTING DB UNAVAILABLE:
  Cause:   Reporting DB maintenance window or failure
  Effect:  Processor holds messages in queue (dead letter queue after N retries)
  Alert:   "Reporting DB write failures — [N] events in dead letter queue"
  Recovery: Once DB available, dead letter queue re-processed.

SCHEMA MISMATCH:
  Cause:   New column added to operational DB not yet reflected in Reporting DB
  Effect:  Processor logs schema mismatch warning, skips unknown fields
  Alert:   "Schema drift detected — [table].[column] not in Reporting DB"
  Recovery: Manual: update Reporting DB schema → processor re-processes affected events.
```

**Monitoring in Super Admin > System Health**

The following CDC metrics are surfaced in the Super Admin System Health dashboard
(tied to RFP 21.4 — Metrics & tracing):

```
REPORTING SYNC HEALTH
  Queue depth:        [N] messages pending
  Lag (current):      [N] seconds (Phase 2 target: < 30s)
  Processor status:   ✅ Running / ❌ Stopped / ⚠️ Behind
  Events processed:   [N] in last hour
  Failed writes:      [N] in last hour (with [View Dead Letter Queue] link)
  Last successful sync: [timestamp]
  Schema drift alerts: [N] unresolved
```

### 4.8.4 Reporting DB Schema Principles

```
1. DENORMALISED READ MODELS — not a copy of operational schema.
   Pre-joined, pre-aggregated views designed for analytics.
   e.g., case_summary_view (one row per case, all outcomes pre-joined)
         daily_tat_metrics (avg TAT per client/check/date pre-computed)
         sla_breach_events (materialised breach records with root cause)

2. PII ANONYMISED AT SCHEMA LEVEL
   Raw Aadhaar, PAN, mobile, email are NOT in the Reporting DB.
   Replaced with: hashed tokens (for joins) + truncated last-4 (for display).
   BI tools connecting to Reporting DB cannot access raw PII.

3. TENANT ISOLATION via SCHEMA-LEVEL VIEWS
   Each client tenant has a scoped view — BI credentials are per-tenant.
   Cross-tenant views available to Super Admin credentials only.

4. READ-ONLY at application level — only sync mechanism writes to it.
   Application service accounts have SELECT-only permissions.

5. INDEX OPTIMISED FOR ANALYTICS (GROUP BY, range scans, aggregations)
   Columnstore indexes and materialised views for frequent aggregations.
```

### 4.8.5 Pages That MUST Use Reporting DB

| Page | Data Read | Lag Acceptable |
|---|---|---|
| 6.1.2 Ops Dashboard | Pipeline counts, SLA status summary | Yes — 60s |
| 6.1.4 Master Case Registry | Case list (filtered, paginated) | Yes |
| 6.1.25 Standard Reports Library | All pre-built reports | Yes |
| 6.1.26 MIS / Analytics Dashboard | All trend charts, KPI strip | Yes |
| 6.1.27 SLA Policy Editor (impact preview) | "This change affects [N] cases" | Yes |
| 6.1.40 Live SLA Dashboard | Breach trend, urgency distribution | Yes |
| 6.2.4 Client Dashboard | Client pipeline, status summary | Yes |
| 6.2.5 Client Report Inbox | Report list, download history | Yes |
| Client Analytics Dashboard | Client TAT trends | Yes |
| 6.5.14 Integration Registry API Usage Log | API call counts, latency, errors | Yes |
| Fraud Intelligence Dashboard (H-1) | Fraud signal trends | Yes |
| BI connector (Power BI / Tableau) | ALL BI queries | Yes |
| Scheduled reports | Report data at generation time | Yes |

Pages that MUST use operational DB (real-time state, lag not acceptable):

| Page | Reason |
|---|---|
| 6.1.39 Case Workbench | Live case state |
| 6.3.1–6.3.10 Candidate forms | Live candidate submission |
| 6.4.1–6.4.6 Vendor task queue | Real-time vendor assignment |
| Consent capture | Real-time compliance critical |

### 4.8.6 BI Connector Design (RFP 18.5)

```
OPTION A — Database Connector (Phase 2/3 recommended):
  Connection:  JDBC / ODBC read-only → Reporting DB
  Credentials: Tenant-scoped service account (SELECT-only, scoped view)
  Power BI:    Import (scheduled refresh) OR DirectQuery (Phase 3)
  Tableau:     Live connection or extract
  Schema:      Anonymised denormalised views — no raw PII
  RLS:         Tenant-scoped database views enforce row-level security
  Config:      6.5.14 Integration Registry > BI Connectors

OPTION B — REST API Connector (Phase 1 / on-prem):
  Connection:  HTTPS GET /v1/analytics/... endpoints
  Auth:        OAuth 2.0 client credentials (machine-to-machine)
  Rate limit:  60 requests/minute per tenant
  Power BI:    Custom connector via Web.Contents()
  Tableau:     Web Data Connector (WDC)
  RBAC:        Enforced at API layer — not DB layer
  Config:      6.5.14 Integration Registry > BI Connectors

Both options:
  → Reporting DB only — never operational DB
  → Per-tenant data scoping enforced
  → No raw PII in returned data
  → All BI queries logged: tenant + timestamp + query type
```

### 4.8.7 Data Freshness Communication

Every dashboard and report page shows:
- "Data as of [timestamp] — refreshes every 60 seconds"
- [Manual Refresh] button (re-reads Reporting DB — does not bypass it)

Lag alerting (displayed as page banner):
- Lag > 5 min: Amber — "Analytics data may be slightly delayed"
- Lag > 15 min: Red — "Analytics data significantly delayed — contact support"
- Lag monitored in Super Admin > System Health



## 4.10 Multilingual Scope Boundary

> **C-10 | RFP 11.9, 23.4**
> **Legacy source: MOM "UI labels only — ~8 languages. Data remains in English. No full translation engine."**
> **PPTX: "Label is multilingual (Labels 6 Languages) EU, US, ME, APC"**
>
> This is a named, binding architectural decision. It defines precisely what is translated,
> what stays in English, which languages are supported, and what RTL layout requires.
> All developers building any portal page must check this section before deciding
> whether a content element needs i18n treatment.

### 4.10.1 IN SCOPE — Translated per Language Selection

The following content types are translated and served from the i18n string registry:

| Content Type | Examples | Portal(s) |
|---|---|---|
| UI navigation labels | "Dashboard", "My Cases", "Upload Documents", "Settings" | Candidate |
| Form field labels | "Company Name", "Date of Birth", "Degree", "Upload Aadhaar" | Candidate |
| Placeholder text | "e.g., DD/MM/YYYY", "Select one...", "Start typing..." | Candidate |
| Instructional / help text | "Please upload a clear photo of your Aadhaar", "Why is this needed?" | Candidate |
| Error and validation messages | "This field is required", "File exceeds 10 MB limit", "Invalid date format" | Candidate |
| Consent notice body | Full DPDP/GDPR consent text — legally required in candidate's language | Candidate |
| Pre-adverse notice | Legal notice sent to candidate before adverse action | Candidate (delivered) |
| Adverse action notice | Final adverse action notice | Candidate (delivered) |
| Email / SMS / WhatsApp templates | "Your BGV has been initiated by [company]", insufficiency notices | All portals (outbound) |
| Candidate portal status messages | "Your form has been submitted", "Document quality: Good" | Candidate |
| Document upload guidance | "Accepted formats: PDF, Word, JPG, PNG, ZIP. Max 10 MB." | Candidate |
| Help and FAQ content | "What is background verification?", "How long does it take?" | Candidate |
| System alerts shown to candidate | "Your session will expire in 5 minutes" | Candidate |
| Tooltip content | Form field tooltips explaining what information is needed | Candidate |

### 4.10.2 OUT OF SCOPE — English Only (Regardless of UI Language)

The following content types are NEVER translated. They are stored and delivered in English always:

| Content Type | Reason |
|---|---|
| Candidate-entered data | Employer names, college names, job titles, addresses — proper nouns. Must be in English for ops processing and report generation. A candidate using Hindi UI still types company names in English. |
| Employer / University / Referee responses | External party text. Employers respond in English. |
| Verification findings | "Employment confirmed: 2016–2022 at TCS" — ops writes in English. |
| Adjudication notes | Internal KPMG documentation — English only. |
| AI signal descriptions | Technical model output — English only. |
| BGV reports delivered to clients | Reports are business documents — always English. |
| Ops Portal (all content) | Internal KPMG tool — English only. Ops reviewers work in English. |
| Vendor Portal (all content) | Vendor-facing tool — English only. |
| Super Admin Portal (all content) | Platform admin — English only. |
| Field Agent App (all content) | KPMG internal agents — English only. |
| Employer / University / Referee response forms | External stakeholder forms — English only. |
| Audit logs and compliance exports | Compliance records — English only, immutable. |
| API responses (data fields) | All API data payloads — English only. |

### 4.10.3 Locale-Specific Formats (RFP 23.4) — Applies Even When Data Is English

Even for content not translated, locale-specific formatting applies per the candidate's selected language/locale:

| Format Type | English (en-IN) | Hindi (hi-IN) | Arabic (ar-AE) | Example Field |
|---|---|---|---|---|
| Date display | 14 Jan 1992 | 14 जनवरी 1992 | ١٤ يناير ١٩٩٢ | Date of birth display |
| Date input | DD/MM/YYYY | DD/MM/YYYY | DD/MM/YYYY | Date picker (format hint) |
| Number format | 1,00,000 (Indian) | 1,00,000 | ١٠٠٬٠٠٠ | Salary field |
| Currency | ₹ (INR) | ₹ (INR) | د.إ (AED) | Compensation display |
| Address field order | Street → City → State → PIN | Same | Same | Address form |
| Phone format | +91 XXXXX XXXXX | Same | +971 XX XXX XXXX | Mobile field |
| Numeral system | Western Arabic (0–9) | Western Arabic (0–9) | May use Arabic-Indic (٠١٢٣) | Displayed numbers |

**RFP 23.4 implementation:** The i18n framework handles date/number formatting via locale-aware formatters (e.g., `Intl.DateTimeFormat`, `Intl.NumberFormat`). No separate translation needed — same data, different format rendering.

### 4.10.4 Supported Languages

Based on PPTX ("6 Languages, EU, US, ME, APC") and MOM ("~8 languages"):

| # | Language | Locale Code | Script | Direction | Region | Notes |
|---|---|---|---|---|---|---|
| 1 | English | en-IN / en-GB / en-US | Latin | LTR | EU, US, APC | Primary — all regions, default locale |
| 2 | Hindi | hi-IN | Devanagari | LTR | APC (India) | Largest candidate language India |
| 3 | Tamil | ta-IN | Tamil | LTR | APC (India, Sri Lanka) | Major South India hiring region |
| 4 | Telugu | te-IN | Telugu | LTR | APC (India) | Major South India hiring region |
| 5 | Kannada | kn-IN | Kannada | LTR | APC (India) | Karnataka / Bangalore-based candidates |
| 6 | **Arabic** | ar-AE | Arabic | **RTL** | ME (Middle East) | **Requires RTL layout — see 4.10.5** |
| 7 | French | fr-FR | Latin | LTR | EU | European client candidates |
| 8 | German | de-DE | Latin | LTR | EU | European client candidates |

Minimum viable: Languages 1–6 (covers all 4 PPTX regions). Languages 7–8 are Phase 2 additions.

Default locale: `en-IN`. Auto-detected from device locale on first visit. User-selectable at any time via persistent language selector. Selection stored in session (not candidate account — no persistent login).

### 4.10.5 RTL Layout Requirement (Arabic)

When a candidate selects Arabic (`ar-AE`), the Candidate Portal switches to RTL layout. This is a layout-level change, not just a text direction change:

```
RTL LAYOUT REQUIREMENTS:

1. HTML direction attribute:
   <html dir="rtl" lang="ar">
   Applied at the root — affects entire page layout.

2. CSS mirroring:
   All margin-left → margin-right (and vice versa)
   All padding-left → padding-right (and vice versa)
   Float: left → float: right (and vice versa)
   Use CSS logical properties where possible:
     margin-inline-start instead of margin-left
     padding-inline-end instead of padding-right

3. Layout mirroring:
   Progress wizard: step numbers flow right-to-left
   Form sections: labels align right
   Navigation: back button appears on right side
   Icons: directional icons (→, ←, >, <) must be flipped
     Non-directional icons (camera, upload, check) do NOT flip

4. Text alignment:
   All text: text-align: right (in RTL context, this is the start edge)
   Numbers and dates: remain LTR within RTL context (bidi algorithm handles)

5. Font loading:
   Arabic requires an Arabic font (e.g., Cairo, Noto Naskh Arabic)
   Loaded only when ar-AE locale is active (not in default bundle)

6. Input fields:
   direction: rtl on text inputs when Arabic locale active
   Placeholder text renders RTL
   User-typed text renders RTL

7. Scroll position:
   RTL pages scroll from right origin (handled by browser — no code change needed)

8. Testing:
   All Candidate Portal pages require RTL QA pass for Arabic locale
   Focus: layout breakage, icon mirroring, text overflow in RTL context

SCOPE OF RTL: Candidate Portal ONLY.
Ops, Vendor, Client, Super Admin portals are English-only — no RTL required.
```

### 4.10.6 i18n Implementation Pattern

```
ARCHITECTURE:

1. String registry:
   All translatable strings stored as key-value pairs per locale:
   e.g., "form.employment.company_name.label": "Company Name" (en)
         "form.employment.company_name.label": "कंपनी का नाम" (hi)
   Stored server-side and served via: GET /v1/i18n/{locale}/strings
   Cached aggressively client-side (TTL: 24h — strings rarely change)

2. Missing translation fallback:
   If a string is missing in the selected locale → fall back to en-IN.
   Never show a key name (e.g., "form.employment.company_name.label") to a user.

3. Dynamic content:
   Translated strings may contain interpolation tokens:
   "Your form was submitted by {candidate_name} on {submission_date}"
   Tokens are replaced after the string is loaded — token names are NEVER translated.

4. Locale switching:
   Language selector change → reload string registry for new locale → re-render page.
   Candidate-entered data in form fields is preserved across locale switches.
   (Candidate switches from English to Hindi mid-form — their typed data stays.)

5. RTL toggle:
   On locale switch to ar-AE → set document dir="rtl" → apply RTL CSS class to root.
   On switch away from ar-AE → remove dir attribute → remove RTL CSS class.

6. Email / SMS / WhatsApp:
   Templates stored per locale in the Communication Template Manager (6.1.24).
   Notification service selects template matching candidate's last-selected locale.
   If no template in candidate's locale → fall back to en-IN template.
   Arabic email templates must be delivered as UTF-8 with RTL email client hints.
```



## 4.11 SOAP→REST Migration Bridge

> **C-12 | RFP 13.1 (ATS/HRIS connectors), 13.2 (API-first coverage)**
> **Legacy source: MOM "Integration Capability: SOAP-based APIs available. Used by HRMS/SAP (limited cases). Not widely adopted."**
>
> This is a named, time-bounded architectural decision.
> The new KCheck platform is REST-only. However, a small number of existing KPMG clients
> (HRMS/SAP systems) currently call the legacy KCheck SOAP APIs. This bridge ensures
> those clients do not break on go-live day and have a managed 12-month migration window
> to move to REST. After 12 months, the adapter is decommissioned.

### 4.11.1 Decision

A **SOAP→REST adapter** is activated at go-live as a translation layer at the API gateway.
It is NOT application code — it is an API gateway transformation rule (Nginx, Kong, AWS API
Gateway, or equivalent). It accepts legacy SOAP requests, transforms them to REST JSON calls
on the new KCheck API, and returns SOAP XML responses. Legacy clients make zero changes.

This is a **migration scaffold**, not a permanent platform feature. It exposes only the
three operations that existed in the legacy SOAP API. No new KCheck capabilities
(AI signals, three-track SLA, custom fields, HRMS auto-push) are accessible via SOAP.

### 4.11.2 Scope — Three SOAP Operations Only

| Legacy SOAP Operation | What It Does | Maps To New REST Endpoint |
|---|---|---|
| `InitiateBGV` | Create a new BGV case | `POST /v1/cases` |
| `GetBGVStatus` | Check status of a case by client reference | `GET /v1/cases?ref={client_ref}` |
| `GetBGVResult` | Retrieve final adjudication outcome | `GET /v1/cases/{id}/result` |

No other SOAP operations are supported. If a client's SOAP call does not match these three,
the adapter returns SOAP Fault: "Operation not supported in migration bridge. Use REST API."

### 4.11.3 Authentication

SOAP clients authenticate using OAuth 2.0 client credentials — the same as REST API callers.
On migration bridge activation, existing SOAP clients are issued client_id + client_secret.
These credentials are included in the SOAP request header (not the SOAP body).
The adapter validates credentials before making the REST call.

### 4.11.4 Sunset Timeline

```
DAY 0 — GO-LIVE:
  Adapter activated. SOAP endpoint live.
  All known SOAP clients notified:
    "New REST API available. SOAP decommissions in 12 months.
     REST documentation: [link]. Sandbox: [link]."

MONTH 3:
  First migration progress check. KPMG contacts any client
  still using SOAP > 100 calls/day.

MONTH 9 (90-day warning):
  Automated notification to all active SOAP callers:
    "SOAP endpoint decommissions in 90 days. Action required."

MONTH 11 (30-day warning):
  Final automated warning. KPMG account managers contact
  any non-migrated clients directly.

MONTH 12 — SUNSET:
  SOAP adapter decommissioned.
  SOAP endpoint returns HTTP 410 Gone:
    "SOAP API has been decommissioned. Please use the REST API.
     Migration guide: [link]"
  All clients must now use REST.
```

### 4.11.5 Monitoring

SOAP adapter usage is tracked in 6.5.14 Integration Registry (Section 6D):
- Per-client SOAP call volume (daily/weekly trend)
- Migration status per client (Not started / In progress / Complete)
- Days until sunset countdown
- Automated notification send log

When a client's SOAP call volume drops to zero and stays at zero for 7+ days,
their migration is marked Complete. Account manager is notified to confirm.


---
---

# PART 5 — COMPLETE PORTAL INFORMATION ARCHITECTURE (EXPANDED)

> Every portal. Every menu. Every submenu. Every page. Every functionality. Every UI component.
> Grounded in RFP BGV_RFP_24_Apr_26.xlsx and Workflow Reference v2.

---

## 5.1 OPERATIONS PORTAL — Full Expanded IA

```
OPERATIONS PORTAL
│
├── 1. DASHBOARD
│   ├── 1.1 My Queue
│   │   └── Page: Personal Work Queue
│   │       Purpose: Personal assigned-case view for every ops reviewer
│   │       Workflows: Case pickup, SLA monitoring, priority triage, quick action
│   │       Components:
│   │         - Queue grid (Case ID, Candidate, Client, Check type, Status, SLA countdown, Risk score, Last action)
│   │         - SLA countdown column (color-coded: Green > 50%, Amber 20–50%, Red < 20%)
│   │         - Risk score badge (Low/Medium/High/Critical)
│   │         - AI-generated case summary cards (collapsed by default, expand on hover)
│   │         - Quick-action buttons per row: [Open] [Mark Insufficient] [Assign Vendor] [Escalate]
│   │         - Bulk action toolbar: Bulk assign, Bulk remind, Bulk export
│   │         - Filter bar: Check type, Client, SLA status, Risk level, Date range
│   │         - Sort controls: SLA ascending (default), Risk descending, Creation date
│   │         - "Cases requiring action today" banner (count + urgency)
│   │         - Auto-refresh toggle (30-second interval)
│   │
│   ├── 1.2 Operations Command Center
│   │   └── Page: Live Ops Overview Dashboard
│   │       Purpose: Real-time visibility across all operations for team leads and managers
│   │       Workflows: Pipeline monitoring, SLA governance, resource allocation, fraud monitoring
│   │       Components:
│   │         - Pipeline stage funnel chart (cases by lifecycle stage)
│   │         - SLA heatmap (check types on Y-axis, clients on X-axis, color = breach rate)
│   │         - Live counter cards: [Active Cases] [Pending Candidate] [Pending Vendor] [In QC] [Awaiting Adjudication]
│   │         - "Breach Risk" ticker (cases predicted to breach in next 4 hours)
│   │         - Vendor SLA compliance scoreboard (top/bottom 5 vendors by TAT)
│   │         - Notification failure counter (last 24h, with drill-in)
│   │         - AI fraud flag count (today, with severity breakdown)
│   │         - Case volume trend chart (7-day rolling, by check type)
│   │         - Team capacity widget (reviewers online, avg queue depth per reviewer)
│   │         - Escalation ticker (active escalations count + overdue escalations)
│   │         - Quick-escalate button from dashboard
│   │
│   ├── 1.3 Team Dashboard (Team Lead view)
│   │   └── Page: Team Performance Monitor
│   │       Purpose: Team lead visibility of reviewer productivity and queue distribution
│   │       Components:
│   │         - Reviewer capacity table (name, active cases, completed today, avg TAT)
│   │         - Queue rebalance action (drag-and-drop case reassignment)
│   │         - QC error rate per reviewer (this week/month)
│   │         - Insufficiency rate per reviewer
│   │         - SLA breach responsibility tracker (which reviewer's cases breached)
│   │
│   └── 1.4 My Analytics
│       └── Page: Personal Productivity Dashboard
│           Purpose: Individual reviewer's own performance visibility
│           Components:
│             - Cases resolved (today / week / month) bar chart
│             - Avg handling time per check type (line trend)
│             - Insufficiency rate (my cases) vs team average
│             - QC feedback received (errors flagged by QC on my cases)
│             - Discrepancy detection rate (how often I found discrepancies)
│             - SLA compliance rate (my cases)
│
├── 2. CASE MANAGEMENT
│   ├── 2.1 All Cases
│   │   └── Page: Master Case Registry
│   │       Purpose: Global case list with advanced search, filter, and bulk operations
│   │       Components:
│   │         - Mega-table: Case ID | Candidate Name | Client | Package | Country | Status | SLA Remaining | Risk Score | Assigned Reviewer | Assigned Vendor | Created | Last Updated | Outcome Color
│   │         - Column selector (show/hide columns)
│   │         - Advanced filter panel: Client (multi-select), Check type, Status (multi-select), SLA breach risk, Date range (created/updated), Country, Assignee, Outcome color, AI flag presence
│   │         - Saved filter presets (per-user)
│   │         - Global search bar (Case ID, Candidate name, PAN hash, Email, Requisition ref)
│   │         - Bulk actions toolbar: [Assign to Me] [Assign to Reviewer] [Assign to Vendor] [Send Reminder] [Export] [Mark for QC] [Escalate]
│   │         - Row-level quick preview drawer (open without full navigation)
│   │         - Export: CSV / Excel (redacted per role, full for Super Admin)
│   │         - Pagination controls + items-per-page selector
│   │         - Color-coded status badges per RFP 10.17 (Green/Amber/Yellow/Red)
│   │         - SLA countdown column (live countdown)
│   │         - Duplicate candidate alert icon (if candidate exists in another case)
│   │
│   ├── 2.2 Case Detail — CORE WORKBENCH
│   │   └── Page: Single Case Verification Workbench
│   │       Purpose: Central workspace for all verification execution, adjudication, QC, compliance, and communication on one case
│   │       Layout: 3-panel (Left nav | Center workspace | Right context panel)
│   │       ──────────────────────────────────────────────────
│   │       TOP BAR (Persistent):
│   │         - Case ID | Candidate name | Client name | Package | Overall Status badge
│   │         - SLA master countdown (overall case deadline)
│   │         - AI Risk Score badge (color-coded, clickable for breakdown)
│   │         - Action buttons: [Escalate] [Flag Urgent] [Close Case] [Generate Report]
│   │         - Breadcrumb: Cases > [Case ID]
│   │       ──────────────────────────────────────────────────
│   │       LEFT PANEL (Check Navigator):
│   │         - Check type list (Employment 1, Employment 2, Education 1, KYC, Legal, Address, Financial)
│   │         - Per-check status icon (Not Started / In Progress / Pending Candidate / Pending Vendor / Completed / Discrepancy / Failed)
│   │         - Per-check SLA mini-countdown
│   │         - Per-check AI flag indicator (red dot if AI flagged)
│   │         - Click to navigate to that check's workspace
│   │       ──────────────────────────────────────────────────
│   │       CENTER PANEL (Active Check Workspace):
│   │         Active check's full verification interface (see 3. Verification Execution below)
│   │       ──────────────────────────────────────────────────
│   │       RIGHT PANEL (Context Panel — collapsible):
│   │         Tab 1: Activity Timeline
│   │           - Chronological event log (every state change, action, communication)
│   │           - Actor label (Ops/Candidate/Client/System) + portal tag
│   │           - Timestamp (absolute + relative)
│   │           - Tamper-evident hash indicator per event
│   │         Tab 2: Communications
│   │           - All messages sent/received (candidate, employer, university, vendor)
│   │           - Channel icon (Email/SMS/WhatsApp)
│   │           - Delivery status (Sent / Delivered / Opened / Failed)
│   │           - [Compose New] button
│   │         Tab 3: Documents
│   │           - All documents uploaded (candidate + ops-added evidence)
│   │           - Document type, upload date, uploader
│   │           - [View] [Download] [Mark Insufficient]
│   │         Tab 4: AI Signals
│   │           - All AI-generated signals across all checks
│   │           - Flag type, confidence, check association, model version
│   │           - [Override] button (requires senior role + mandatory note)
│   │         Tab 5: Audit Log
│   │           - Full case audit trail with export
│   │       ──────────────────────────────────────────────────
│   │       BANNERS (context-aware, top of center panel):
│   │         - SLA Breach Imminent (orange) — "SLA breaches in 2h — escalate or complete"
│   │         - AI High-Risk Flag (red) — "High-confidence fraud signal — senior review required"
│   │         - Consent Invalid (red) — "Candidate consent expired — cannot proceed"
│   │         - Major Discrepancy (amber) — "Major discrepancy in Employment — adjudication required"
│   │         - Vendor Overdue (orange) — "Vendor has not responded — SLA at risk"
│   │         - Notification Failure (yellow) — "Candidate unreachable — SLA paused"
│   │         - Waiver Pending (blue) — "Waiver approval pending with Risk/Legal"
│   │
│   ├── 2.3 Pending Insufficiency Queue
│   │   └── Page: Insufficiency Management Queue
│   │       Purpose: Track all cases where candidate action is pending; manage re-submission SLA
│   │       Components:
│   │         - Queue table: Case ID | Candidate | Insufficient Fields (count) | Remarks sent | Days waiting | Re-submission status | SLA impact
│   │         - "Days waiting" column (SLA clock from insufficiency marked date)
│   │         - Re-submission status badge: Awaiting / Received / Reviewed
│   │         - Filter: Client, Days waiting (> 3, > 7, > 14), Re-submission status
│   │         - Escalation banner for cases waiting > configured threshold
│   │         - Bulk send reminder action (WhatsApp + SMS + Email)
│   │         - View remarks sent per case (drawer)
│   │         - Mark as "Candidate Unresponsive" action (triggers SLA closure + client notification)
│   │
│   ├── 2.4 QA / QC Review Queue
│   │   └── Page: QC Sampling Queue
│   │       Purpose: Second-level quality control review of completed verifications
│   │       Components:
│   │         - QC queue table: Case ID | Check type | Original Reviewer | QC Reviewer | Sampling reason | Status
│   │         - Sampling reason (Random sample / Risk-triggered / Client-requested / New reviewer)
│   │         - QC Review interface (side-by-side: original reviewer's outcome vs evidence)
│   │         - Error tagging: Error type selector (Data accuracy / Process deviation / Evidence quality / Adjudication error) + mandatory description
│   │         - QC outcome: Pass / Fail (with reason)
│   │         - Fail → routes back to original reviewer with feedback note
│   │         - QC metrics widget (pass rate, top error types, reviewer accuracy trend)
│   │         - QC feedback history per reviewer (for performance tracking)
│   │
│   ├── 2.5 Escalation Queue
│   │   └── Page: Active Escalations Manager
│   │       Purpose: Manage all auto-triggered and manually escalated cases
│   │       Components:
│   │         - Escalation table: Case ID | Escalation reason | Escalation type (Auto/Manual) | Escalated to | Time in escalation | Resolution status
│   │         - Escalation reason categories: SLA Breach Risk / AI Fraud Flag / Major Discrepancy / Client Request / Legal/Compliance / Vendor Failure
│   │         - Resolution panel (drawer): Enter resolution, close escalation, notify originator
│   │         - Escalation SLA indicator (how long in escalation vs target)
│   │         - Escalation trend chart (last 30 days, by reason type)
│   │
│   ├── 2.6 Dispute Queue
│   │   └── Page: Candidate Dispute Workbench
│   │       Purpose: Handle DPDP/GDPR-mandated candidate dispute resolution
│   │       Components:
│   │         - Dispute intake table: Dispute ID | Case ID | Candidate | Dispute type | Filed date | DPDP deadline | Status | Assigned to
│   │         - DPDP response deadline countdown (30-day clock from filing)
│   │         - Dispute type: Data Accuracy / Process / Outcome / DSAR (access/erasure/correction)
│   │         - Investigation workspace: View original case data, disputed claim, candidate evidence
│   │         - Resolution panel: Outcome (Upheld/Partially Upheld/Rejected) + resolution note + evidence
│   │         - Candidate notification trigger (automated on resolution)
│   │         - Escalation to Risk/Legal (one-click for complex disputes)
│   │         - Grievance redressal log (DPDP-mandated audit record)
│   │
│   ├── 2.7 Global Search
│   │   └── Page: Cross-Case Search
│   │       Purpose: Find any case, candidate, employer, or document across the system
│   │       Components:
│   │         - Universal search bar (Case ID, Candidate name, PAN hash, Email, Phone, Employer name, Requisition ref)
│   │         - Entity type filter: Cases / Candidates / Employers / Documents
│   │         - Date range filter
│   │         - Results grouped by entity type
│   │         - Recent searches history
│   │         - Saved search bookmarks
│   │
│   └── 2.8 Ops-Initiated Case Creation  [NEW — C-01 | RFP 10.1, 13.1]
│       └── Page: Manual Case Entry Workbench
│           Purpose: KPMG ops staff creates a BGV case by entering candidate data received
│                    from client via email or Excel — bypassing candidate portal entirely.
│                    Covers the "Email" path of the legacy 50% manual entry flow (PPTX).
│                    RFP 10.1 ("Request" step precedes "invite" — invite is not mandatory).
│                    RFP 13.1 (hybrid integration to reduce manual data entry).
│           Actors: Ops Reviewer, Senior Reviewer, Team Lead
│           Trigger: Client emails Excel / sends data offline / phone-provided candidate details
│           Entry Modes:
│             MODE A — Excel Import (preferred):
│               - Ops uploads client-provided Excel file
│               - System auto-maps columns to KCheck case fields using column-name matching
│               - Ops reviews auto-populated fields, corrects any mismatches
│               - Remaining unmapped fields shown as blank — ops fills manually
│             MODE B — Manual Field Entry:
│               - Ops types each field directly (reading from client email or document)
│               - Same field set as candidate portal form
│               - Used for single-candidate entries from email or phone
│           Components:
│             - Mode selector toggle at top: [Excel Import] [Manual Entry]
│             - Full candidate data form — all sections:
│                 Personal: Full name, DOB, gender, personal email, mobile, current address, nationality
│                 Employment: Per employer — company, designation, from/to dates, supervisor name/contact, reason for leaving
│                 Education: Per qualification — institution, degree, year, roll number
│                 Identity: Aadhaar, PAN, Passport, DL (fields driven by selected package)
│             - Document upload panel:
│                 Ops uploads documents on behalf of candidate
│                 (employer-provided, client-provided, candidate's joining kit)
│                 Accepted formats: PDF, Word, Excel, JPG, PNG, ZIP (per C-02)
│             - Audit / Consent fields (mandatory before submit):
│                 "Data Source" selector: Email / Excel / Phone / Courier / Other
│                 "Consent Reference" free-text: ops records evidence of candidate consent
│                   Example: "Client email dated 14-May-2026 from Priya Sharma (HR).
│                             Candidate consent declared by client. Ref: HR-BGV-2026-0441"
│                 This creates the audit trail for offline consent (DPDP/GDPR)
│             - Package selector: which BGV package applies to this case
│             - Client selector: which client tenant this case belongs to
│             - [Preview & Submit] button → full data review modal before creating case
│             - On submit:
│                 Case created: initiation_mode = ops_manual
│                 Case status: "In Verification" (no "Pending Candidate" step)
│                 Audit event logged: ops user, data source, consent reference, timestamp
│                 All verification steps proceed identically from this point
│           Alerts:
│             - "No candidate email provided — candidate will not receive any notifications"
│             - "Consent reference is mandatory — this is the audit record for offline consent"
│             - "Excel column [X] could not be mapped — please fill field manually"
│
├── 3. VERIFICATION EXECUTION
│   ├── 3.1 Employment Verification
│   │   └── Page: Employment Check Workspace
│   │       Purpose: Execute all employment verification checks per RFP Section 4
│   │       Components:
│   │         - Employment history display panel (candidate-submitted: company, designation, dates, supervisor, reason for leaving)
│   │         - EPFO/UAN verification panel: UAN number, UAN-pulled employment history, reconciliation diff with candidate-submitted
│   │         - EPFO discrepancy highlighter (date mismatch, employer name mismatch, designation absent in UAN)
│   │         - Dual employment detector panel: AI-flagged overlapping tenures with evidence links
│   │         - ITR/Payroll document panel: Uploaded documents, AI-extracted figures, authenticity check result
│   │         - Experience letter fraud detection: Font analysis result, metadata edit indicator, template match score
│   │         - Employer outreach section:
│   │             * Outreach status per employer (Not Sent / Sent / Opened / Responded / Overdue)
│   │             * Send outreach button (generates tokenized employer link)
│   │             * Employer response viewer (structured: confirmed dates, designation, rehire status, separation reason)
│   │             * Manual entry fallback (for phone-verified employers)
│   │         - Reference check section (if package includes):
│   │             * Reference contact details
│   │             * Outreach status
│   │             * Structured questionnaire response viewer
│   │         - Employment gap analysis widget: Timeline visual showing all tenures and gaps, AI-generated gap explanation (if candidate provided)
│   │         - Tenure reconciliation panel: Side-by-side comparison (Candidate claim | UAN record | Employer confirmed) with highlight on mismatches
│   │         - Check outcome section:
│   │             * Outcome selector: Verified / Minor Discrepancy / Major Discrepancy / Unable to Verify
│   │             * Discrepancy description (mandatory if non-Verified)
│   │             * Evidence attachment
│   │             * Notes to adjudicator
│   │             * [Mark Insufficient] button (opens field-level remarks drawer)
│   │             * [Submit Check] button
│   │         - SLA widget: Check-specific deadline countdown
│   │         - Vendor assignment drawer (if routing to external employment verifier)
│   │
│   ├── 3.2 Education Verification
│   │   └── Page: Education Check Workspace
│   │       Purpose: Verify academic credentials per RFP Section 5
│   │       Components:
│   │         - Education history display (candidate-submitted: degree, institution, board/university, year, percentage/CGPA)
│   │         - DigiLocker fetch result panel: Fetched certificate details, comparison with candidate-submitted, match/mismatch highlight
│   │         - Institution recognition panel: Accreditation status (UGC/AICTE/State Board), fake university database check result, recognition status badge
│   │         - Degree fraud detection widget: AI flags (document template forgery, incorrect year format, suspicious font), confidence score, evidence overlays
│   │         - Course duration validator: Expected duration for degree type vs claimed dates, anomaly flag
│   │         - Name change evidence panel: Affidavit upload if name on certificate differs from current name
│   │         - University outreach section:
│   │             * Outreach status (Not Sent / Sent / Responded)
│   │             * Tokenized university response link
│   │             * Structured response viewer (enrollment confirmed, degree conferred, year of passing, percentage)
│   │         - Duplicate certificate detector (same roll number / registration number in other cases)
│   │         - Check outcome section (same structure as Employment)
│   │         - Vendor assignment drawer (for physical university verification)
│   │
│   ├── 3.3 Identity / KYC Verification
│   │   └── Page: KYC Verification Workspace
│   │       Purpose: Verify candidate identity documents and biometrics per RFP Sections 3, 2.1–2.8
│   │       Components:
│   │         - Document gallery: All uploaded ID documents (Aadhaar, PAN, Passport, DL, Voter ID)
│   │         - Per-document verification result panel:
│   │             * Aadhaar: OTP-based API verification result, masked display, data match
│   │             * PAN: NSDL API result, name-DOB match
│   │             * Passport: MRZ validation result, expiry check, country authority check (ICAO)
│   │             * DL: RC/DL API result (where available), expiry, endorsements
│   │         - OCR extraction panel: AI-extracted fields vs candidate-entered fields, field-level diff
│   │         - Biometric panel:
│   │             * Face match result: Selfie vs ID photo composite view, match score (0–100%), confidence category
│   │             * Liveness result: Active/Passive challenge completed, liveness score, deepfake flag (if applicable)
│   │             * Attempt history: How many liveness attempts, failure reasons
│   │         - Document fraud detection overlay: Presentation attack indicators, font anomalies, metadata tampering, photoshop detection markers
│   │         - Device/geo risk panel: Device type, OS, IP country, VPN/proxy detection, geo-distance from declared address
│   │         - MRZ/barcode validation panel (Passport/DL)
│   │         - Cross-document consistency check: DOB match across all documents, name match, address consistency
│   │         - Check outcome section + override panel (senior role required)
│   │         - Biometric consent validity check (before processing biometric data)
│   │
│   ├── 3.4 Legal / Criminal Verification
│   │   └── Page: Legal Check Workspace
│   │       Purpose: Execute court record and watchlist checks per RFP Section 6
│   │       Components:
│   │         - Search scope configuration: District courts (list), High Courts (list), Supreme Court, SFIO, SEBI, RBI
│   │         - Court record search results panel: Source database, case number, case type, petitioner/respondent, status (Disposed/Pending/Convicted), date
│   │         - Identity resolution panel: Match confidence (same name, DOB, address confirmation), identity disambiguation notes
│   │         - Global watchlist/sanctions screening result: OFAC, UN, EU, domestic lists, PEP classification (RFP 6.5)
│   │         - Ongoing investigation flag: Differentiate between pending charge (risk) vs disposed case (different severity)
│   │         - Adjudication matrix panel: Auto-recommendation based on case type + role-specific policy (configurable)
│   │         - Jurisdiction coverage indicator: Which courts were searched, which are not reachable digitally
│   │         - Role-based check depth indicator: Executive package searches more courts than standard
│   │         - Check outcome section (with mandatory notes for any hit)
│   │
│   ├── 3.5 Address Verification
│   │   └── Page: Address Verification Workspace
│   │       Purpose: Verify candidate residential address per RFP Section 7
│   │       Components:
│   │         - Digital verification panel:
│   │             * Geo-coordinate validation (declared address mapped, plausibility check)
│   │             * Map view with address pin
│   │             * Distance from centroid check
│   │             * Utility/telecom database check result (where permissible)
│   │         - Field visit management section:
│   │             * Assign field agent (from registered agent pool by geography)
│   │             * Visit assignment status (Assigned / Acknowledged / In Transit / Evidence Submitted)
│   │             * Agent name, contact, ETA
│   │         - GPS-tagged evidence viewer:
│   │             * Photo gallery with GPS coordinates, timestamp, accuracy radius
│   │             * Map pin matching photo location to declared address
│   │             * Photo authenticity flag (AI: inconsistent metadata, teleported location)
│   │         - Neighbor verification notes viewer
│   │         - Remote video verification section (for remote-friendly packages):
│   │             * Scheduler (candidate + agent time slot)
│   │             * Video session status
│   │             * Video evidence record (if captured)
│   │         - Address reconciliation widget: Declared address vs GPS-verified address vs postal database address — 3-way diff
│   │         - Check outcome section
│   │
│   ├── 3.6 Financial Verification
│   │   └── Page: Financial Check Workspace
│   │       Purpose: Execute financial background checks per RFP Section 8
│   │       Components:
│   │         - Credit bureau result panel (CIBIL/Experian — where client has permissible purpose)
│   │         - Bankruptcy/insolvency check: MCA, DRT, NCLT search results
│   │         - AML/KYC screening: Transaction pattern flags (where applicable)
│   │         - Purpose limitation display: Explicitly shows legal basis for financial check
│   │         - Consent verification panel: Confirms financial check consent separately obtained
│   │         - Outcome: Clear / Adverse Finding / Unable to Verify (with mandatory notes for adverse)
│   │
│   └── 3.7 Reference Check Workspace
│       └── Page: Reference Check Workspace
│           Purpose: Manage structured reference verification per RFP 4.12–4.13
│           Components:
│             - Reference contacts list (submitted by candidate)
│             - Outreach status per reference
│             - Reference questionnaire response viewer (structured form responses)
│             - Referee credibility check (employment of referee cross-verified)
│             - Notes and outcome section
│
├── 4. ADJUDICATION
│   ├── 4.1 Adjudication Queue
│   │   └── Page: Cases Pending Final Adjudication
│   │       Purpose: All cases where verification complete, awaiting adjudicator decision
│   │       Components:
│   │         - Queue table: Case ID | Candidate | Client | Package | Checks complete | Discrepancy count (by severity) | AI risk score | SLA to report delivery | Assigned adjudicator
│   │         - Filter: Client, Discrepancy severity, SLA urgency, Adjudicator
│   │         - Priority sort: Most urgent first (SLA + severity composite)
│   │         - AI reviewer assist summary card (per row, expandable)
│   │         - Escalated cases section (separate from standard queue)
│   │         - Bulk assign adjudicator action
│   │
│   ├── 4.2 Adjudication Workbench
│   │   └── Page: Final Decision Interface
│   │       Purpose: Complete case review for final adjudication decision per RFP 10.9
│   │       Components:
│   │         - Full case summary view (all checks, all outcomes, all discrepancies)
│   │         - AI-generated adjudication summary: "Summary of findings: [auto-text]. Key discrepancies: [list]. Risk factors: [list]. Suggested outcome: [suggestion]."
│   │         - Discrepancy table: Type | Severity | Source check | AI-detected vs manual | Resolution options
│   │         - Outcome selector: Clear / Minor Discrepancy / Major Discrepancy / Unable to Verify / Failed
│   │         - Outcome notes field (mandatory for non-Clear)
│   │         - Evidence attachment panel
│   │         - Pre-adverse notice trigger: If outcome = Failed or Major Discrepancy, prompt to generate pre-adverse notice
│   │         - Pre-adverse notice preview modal (RFP 10.11): Candidate name, findings summary, rights explanation, waiting period
│   │         - Adverse action notice generator (after waiting period)
│   │         - Waiver request trigger (routes to approval chain)
│   │         - Report template selector (client-specific templates)
│   │         - Adjudicator identity confirmation (name + timestamp captured in audit)
│   │         - Confirm decision button (modal with legal confirmation text)
│   │
│   ├── 4.3 Waiver Management
│   │   └── Page: Waiver Request Approval Workflow
│   │       Purpose: Process client/ops-requested waivers for cases with discrepancies per RFP 10.7
│   │       Components:
│   │         - Waiver request table: Request ID | Case ID | Discrepancy being waived | Requester | Approval tier required | Status | Days pending
│   │         - Waiver request detail drawer: Discrepancy details, waiver justification, supporting evidence, requestor notes
│   │         - Approval routing display (who needs to approve: Ops Lead / Risk / Legal / Client sign-off)
│   │         - Approval action panel: [Approve] [Reject] [Request More Info] + mandatory notes
│   │         - Approval chain history (each approver's decision with timestamp)
│   │         - Waiver history per candidate (recurrence check — repeated waivers flagged)
│   │         - Waiver audit export
│   │
│   └── 4.4 Report Generation
│       └── Page: BGV Report Builder and Delivery
│           Purpose: Generate, review, approve, and deliver final BGV reports per RFP 18
│           Components:
│             - Client-specific template selector
│             - Report preview panel (live render with candidate data)
│             - Section inclusion/exclusion toggles (per client configuration)
│             - Color-code outcome tagging (per client's color matrix configuration — RFP 12.11)
│             - Reviewer sign-off panel (reviewer name + date stamp)
│             - QC approval step (if QC required for this package)
│             - Report delivery: Auto-push to client portal + notification
│             - Delivery confirmation log
│             - Report version history (if re-issued)
│             - Redaction control (mark fields for redaction before delivery — per client agreement)
│
├── 5. VENDOR MANAGEMENT (Ops-side)
│   ├── 5.1 Vendor Assignment Console
│   │   └── Page: Case-to-Vendor Routing Interface
│   │       Purpose: Assign check items to appropriate vendors per geography and capability
│   │       Components:
│   │         - Unassigned items queue (check type, geography, SLA)
│   │         - Vendor capability matrix table (vendor, check types supported, geographies covered, SLA commitment)
│   │         - Vendor current workload indicator (active assignments, capacity %)
│   │         - AI-suggested vendor (best match: capability + geography + availability + SLA history)
│   │         - Manual override option
│   │         - Bulk assignment interface (assign 20 cases to same vendor in one action)
│   │         - Assignment confirmation drawer (case + vendor + expected TAT)
│   │         - Assignment history log per case
│   │
│   ├── 5.2 Vendor Performance Dashboard
│   │   └── Page: Vendor Scorecard & Analytics
│   │       Purpose: Monitor vendor quality, SLA compliance, and reliability per RFP 21
│   │       Components:
│   │         - Vendor performance table: Vendor name | Check type | Avg TAT | SLA compliance % | QC error rate | Response rate | Active assignments
│   │         - Vendor comparison chart (side-by-side bar chart for top metrics)
│   │         - Vendor drill-in: Individual vendor scorecard with trend charts
│   │         - SLA breach count by vendor (last 30/90 days)
│   │         - Quality score (QC error rate on submissions from this vendor)
│   │         - Vendor performance alert (auto-flag if vendor drops below threshold)
│   │         - Export scorecard (PDF for vendor review meetings)
│   │
│   ├── 5.3 Vendor Onboarding
│   │   └── Page: New Vendor Setup Workflow
│   │       Purpose: Onboard new verification vendors with capability configuration
│   │       Components:
│   │         - Multi-step onboarding wizard: Details > Capabilities > SLA > Users > Documents > Activate
│   │         - Vendor type selector (BGV agency / Court search firm / Address verifier / Reference checker)
│   │         - Capability matrix configurator (check types, geographies)
│   │         - SLA agreement capture (per check type, per geography)
│   │         - Vendor user account creation
│   │         - Contract and DPA document upload (DPDP/GDPR subprocessor agreement — RFP 22.3)
│   │         - Activation gate (requires contract + DPA uploaded)
│   │
│   └── 5.4 Vendor Communication Log
│       └── Page: Ops-Vendor Communication Center
│           Purpose: Track all structured and unstructured communication with vendors
│           Components:
│             - Communication log table (per vendor, per case)
│             - Message compose (assignment notes, clarification requests)
│             - Template-based standard messages
│             - Delivery and read status
│
├── 6. REPORTING & ANALYTICS
│   ├── 6.1 Report Generation Queue
│   │   └── Page: Reports Pending Generation
│   │       Purpose: Cases where adjudication complete, reports pending creation
│   │       Components: Queue table, template selector, generate action, bulk generate
│   │
│   ├── 6.2 Report Archive
│   │   └── Page: All Issued Reports
│   │       Purpose: Search and access all previously generated BGV reports
│   │       Components:
│   │         - Report archive table (Case ID, Candidate, Client, Issue date, Version, Template used)
│   │         - Search and filter (client, date range, outcome, template)
│   │         - View / Download per report
│   │         - Re-issue report (version increment, reason capture)
│   │         - Report access log (who downloaded, when — for audit)
│   │
│   ├── 6.3 Operational Reports Library
│   │   └── Page: Standard Report Catalog
│   │       Purpose: Pre-built operational reports for MIS, client reporting, and compliance.
│   │               Reports are primarily used as SCHEDULED DELIVERIES (recipients receive
│   │               reports in their inbox automatically). On-demand preview/download is
│   │               secondary — for ad-hoc investigation. [C-13 | RFP 18.1, 18.6]
│   │       Report List (minimum 10–15 per RFP 18.6 KPI/KRI library):
│   │         - Cases Initiated (daily/weekly/monthly, by client, by check type)
│   │         - Cases Completed (TAT analysis)
│   │         - SLA Compliance Report (by client, by vendor, by check type)
│   │         - Discrepancy Frequency Report (by type, by check, by client)
│   │         - Vendor Performance Report
│   │         - Insufficiency Rate Report (by check type, by client)
│   │         - QC Error Report (by reviewer, by check type)
│   │         - Fraud Flag Summary Report
│   │         - Escalation Summary Report
│   │         - Candidate Completion Rate Report
│   │         - Waiver Report (by client, by discrepancy type)
│   │         - Data Subject Request Summary (DPDP compliance)
│   │         - Consent Audit Report
│   │         - Notification Delivery Report (channel-wise)
│   │       Components per report (PRIMARY first):
│   │         PRIMARY: [Schedule Delivery] — set up recurring delivery to recipients
│   │           - Frequency: Daily / Weekly / Monthly / Custom
│   │           - Day and time selector
│   │           - Recipients: email distribution list
│   │           - Format: PDF / Excel / Both
│   │           - [Send Test Now] — one-time delivery for validation before schedule goes live
│   │         SECONDARY: [Run Now] — on-demand preview and download
│   │           - Parameter selector (date range, client, check type)
│   │           - In-portal preview (tabular + charts)
│   │           - Export: PDF / Excel / CSV
│   │
│   └── 6.4 MIS / Analytics Dashboard
│       └── Page: Advanced MIS & BI Dashboard
│           Purpose: Strategic analytics for operations leadership per RFP 18, 21
│           Components:
│             - KPI summary strip: [Total Cases MTD] [Cases Completed] [SLA Compliance %] [Avg TAT] [Discrepancy Rate] [Fraud Flag Rate]
│             - Pipeline funnel by stage
│             - TAT analytics: Heatmap (client vs check type), trend over time, p90/p95 TAT
│             - SLA breach trend and root cause analysis
│             - Discrepancy type frequency (top 10 discrepancy types)
│             - Vendor performance trends
│             - Fraud flag trend (AI flags raised, confirmed, false positive rate)
│             - AI accuracy metrics (where ground truth available)
│             - BI export connector (Power BI / Tableau data feed)
│             - Date range selector, client filter, check type filter
│
├── 7. SLA & ESCALATION MANAGEMENT
│   ├── 7.1 Live SLA Monitor
│   │   └── Page: Real-Time SLA Health Dashboard
│   │       Purpose: Continuous SLA tracking and breach prevention per RFP 10.5, 21
│   │       Components:
│   │         - SLA health distribution: Count of cases by health tier (Green/Amber/Red/Breached)
│   │         - Live SLA countdown table (all in-progress cases with countdown, sortable by urgency)
│   │         - AI-predicted breach alerts widget: "These 12 cases are likely to breach in 4 hours based on current velocity"
│   │         - SLA pause log: Cases where SLA is paused (notification failure/candidate unresponsive) with resume conditions
│   │         - Per-check SLA breakdown: Which check type is the most common breach contributor
│   │         - Client-specific SLA tier display (different clients may have different SLA agreements)
│   │         - Auto-escalation trigger log (which rules fired today)
│   │
│   ├── 7.2 SLA Configuration (Ops Admin)
│   │   └── Page: SLA Policy Editor
│   │       Purpose: Configure three-track SLA (Client / Internal / Vendor) thresholds,
│   │                escalation rules, and auto-actions per check type [C-03 | RFP 1.7]
│   │       Components:
│   │         - Three-track SLA policy table per check type:
│   │             Client SLA (days) | Internal SLA (days) | Vendor SLA (days) |
│   │             Amber threshold (%) | Red threshold (%) | [Reset to Default]
│   │         - Default Template row values pre-loaded (KPMG baseline — per C-03)
│   │         - [Reset to Default] action per row — restores KPMG baseline values
│   │         - Escalation matrix configurator (at what % of SLA remaining → who gets notified)
│   │         - Auto-escalation rules (trigger conditions, notification targets)
│   │         - SLA pause conditions (when to pause, auto-resume conditions)
│   │         - SLA penalty calculation rules (ties to billing module — RFP 22.2)
│   │         - Version history + rollback for SLA policies
│   │
│   └── 7.3 Escalation Resolution Log
│       └── Page: Historical Escalation Analytics
│           Components:
│             - Escalation count trend (by type, by client, by week)
│             - Avg time to resolve escalations
│             - Top escalation causes
│             - Escalation recurrence by case/client
│
├── 8. COMMUNICATIONS CENTER
│   ├── 8.1 Compose & Send
│   │   └── Page: Multi-Channel Communication Interface
│   │       Purpose: Send structured communications to any stakeholder per RFP 11.7, 11.13
│   │       Components:
│   │         - Recipient selector: Candidate / Employer / University / Vendor / Client
│   │         - Channel selector: Email / SMS / WhatsApp
│   │         - Template selector (purpose-specific templates: invitation, reminder, insufficient, completion, adverse notice)
│   │         - Template preview with populated variables (candidate name, case ID, deadline, link)
│   │         - Personalization override (edit template for this send)
│   │         - Send immediately / Schedule for specific time
│   │         - Multi-language template selection (RFP 19.6 — 6–8 languages)
│   │         - Delivery confirmation
│   │
│   ├── 8.2 Notification Delivery Monitor
│   │   └── Page: Delivery Status & Failure Management
│   │       Purpose: Detect and remediate notification delivery failures — critical for SLA
│   │       Components:
│   │         - Failed delivery table: Case ID | Recipient | Channel | Failure reason | Attempts | Last attempt time
│   │         - Failure reason categorization: Invalid number / WhatsApp not registered / Email bounced / Spam blocked
│   │         - Channel fallback status (WhatsApp failed → SMS attempted → Email attempted)
│   │         - Manual re-send button per row
│   │         - SLA impact indicator (cases with SLA paused due to delivery failure)
│   │         - Bulk re-send action
│   │         - Failure trend chart (daily failure rate by channel)
│   │
│   └── 8.3 Template Manager
│       └── Page: Communication Template Library
│           Components:
│             - Template catalog (type, channel, language, version)
│             - Template editor (rich text with variable tokens)
│             - Variable tokens reference panel
│             - Multi-language versions per template
│             - Preview and test send
│             - Approval workflow for new/changed templates
│             - Version history + rollback
│
├── 9. COMPLIANCE & AUDIT
│   ├── 9.1 Consent Management
│   │   └── Page: Consent Record Viewer and Audit
│   │       Purpose: Provide complete consent audit trail for DPDP/GDPR compliance per RFP 15.1–15.3
│   │       Components:
│   │         - Consent registry table: Case ID | Candidate | Consent version | Signed timestamp | IP address | Device fingerprint | Purpose scope | Withdrawal status
│   │         - Consent document viewer (exact consent text candidate agreed to, with version)
│   │         - E-signature verification display
│   │         - Consent withdrawal log (if candidate withdrew consent)
│   │         - Consent validity indicator (expired / active / withdrawn)
│   │         - DPDP/GDPR compliance status per case
│   │         - Export consent pack (per case, for regulatory submission)
│   │
│   ├── 9.2 Audit Trail Viewer
│   │   └── Page: Immutable Case Audit Log
│   │       Purpose: Complete, tamper-evident record of every action on every case per RFP 14.12
│   │       Components:
│   │         - Event log table: Event ID | Case ID | Timestamp | Actor | Actor role | Portal | Action type | Affected data field | Before value (redacted) | After value (redacted) | Event hash
│   │         - Filter: Case ID / Actor / Action type / Portal / Date range
│   │         - Hash chain verification button (verifies log integrity)
│   │         - Export audit pack: Per-case PDF + JSON with hash manifest
│   │         - Long-term archive access (cold storage query for cases > 12 months)
│   │
│   ├── 9.3 DSAR Management
│   │   └── Page: Data Subject Access Request Tracker
│   │       Purpose: Manage DPDP/GDPR data subject rights requests per RFP 15.6–15.9
│   │       Components:
│   │         - DSAR intake table: Request ID | Candidate | Request type (Access/Correction/Erasure/Portability) | Filed date | Legal deadline | Status | Assigned to
│   │         - Legal deadline countdown (30-day GDPR / DPDP response clock)
│   │         - Investigation workspace: Pull all data held for this candidate
│   │         - Response generation: Data export package (Access) / Correction log / Erasure confirmation
│   │         - Erasure impact check: Is this candidate's data needed for pending verification? (Legal hold flag)
│   │         - Response delivery confirmation
│   │         - DSAR registry export (for DPA reporting)
│   │
│   └── 9.4 Data Retention Manager
│       └── Page: Retention Policy Monitor
│           Purpose: Enforce configurable data retention and automated purge per RFP 15.5
│           Components:
│             - Retention policy table (per check type, per country, per client)
│             - Cases approaching retention expiry (scheduled for deletion)
│             - Pending deletion queue (review before purge)
│             - Purge execution log (what was deleted, when, by what rule)
│             - Legal hold registry (cases exempt from deletion due to dispute/litigation)
│
├── 10. SETTINGS (Operations-level)
│   ├── 10.1 Team Management
│   │   └── Page: Ops User Administration
│   │       Components:
│   │         - User list: Name | Role | Active cases | Last login | Status
│   │         - Add user wizard (name, email, role assignment, client access scope)
│   │         - Role selector: Reviewer / Senior Reviewer / QC Reviewer / Adjudicator / Team Lead / Compliance / Investigator
│   │         - Temporary delegation (delegated access with expiry date — RFP 12.8)
│   │         - Workload rebalancing (manual reassignment)
│   │         - User deactivation (with open case reassignment workflow)
│   │
│   ├── 10.2 Check Configuration
│   │   └── Page: Verification Check Settings
│   │       Components:
│   │         - Check type registry (all supported check types, enabled/disabled)
│   │         - Per-check configuration (vendor routing rules, auto-assign logic, SLA defaults)
│   │         - Check depth by role type (Senior Executive vs Standard check differences)
│   │         - Country-specific check availability matrix
│   │
│   └── 10.3 Notification Configuration
│       └── Page: Notification Rules and Escalation Config
│           Components:
│             - Notification rules table (event → channel → recipient → template)
│             - Escalation ladder configuration (SLA % → notification target)
│             - Out-of-hours rule (after-hours escalations go to on-call)
│             - Notification throttle settings (max reminders per candidate per day)
│             - Test notification sender
```

---

## 5.2 CLIENT PORTAL — Full Expanded IA

```
CLIENT PORTAL
│
├── 1. DASHBOARD
│   └── Page: Client Overview Dashboard
│       Purpose: Client's primary landing page — status visibility across their entire BGV program
│       Components:
│         - KPI strip: [Active Cases] [Cases Completed This Month] [Pending Candidate Action] [Reports Ready] [Avg TAT (days)] [SLA Compliance %]
│         - Status distribution donut chart (In Progress / Pending Candidate / Completed / On Hold)
│         - Outcome color distribution (Green / Amber / Yellow / Red — per client's matrix)
│         - "Action Required" panel: Candidates who have not submitted, reports requiring client adjudication approval, disputes pending client response
│         - Recent reports (last 10 completed — quick download buttons)
│         - Monthly volume trend chart
│         - Business unit breakdown (if client uses BU segregation)
│         - SLA compliance sparkline (last 12 weeks)
│         - Notification: System announcements from KPMG
│
├── 2. CASE MANAGEMENT
│   ├── 2.1 Initiate New Case
│   │   └── Page: Single Case Initiation Wizard
│   │       Purpose: Create individual BGV case per RFP 10.1, 10.2
│   │       RFP: 10.1 (end-to-end lifecycle — "invite" step is not mandatory), 10.2, 13.1
│   │       Workflow (Standard): Package selection → Initiation mode → Candidate details → Duplicate check → Invite send
│   │       Workflow (Non-Candidate): Package selection → Initiation mode → Full data entry → Consent declaration → Submit
│   │       Components:
│   │         Step 1 — Package Selection:
│   │           - Package tiles (Basic / Standard / Executive / Custom — client-configured packages shown)
│   │           - Package comparison drawer (what checks are included in each)
│   │           - Role/designation field (drives package recommendation)
│   │         Step 1B — Initiation Mode Selection [NEW — C-01 | RFP 10.1, 13.1]:
│   │           - "Invite Candidate" (default) — candidate fills their own data via portal
│   │           - "Enter Data Directly" — client HR fills all candidate data now, no invitation sent
│   │             Displayed note: "Use this when you have all candidate details and the
│   │             candidate will not be contacted via the portal."
│   │         Step 2 — Candidate Details:
│   │           IF "Invite Candidate" mode (existing flow):
│   │             - Candidate full name, personal email, mobile number
│   │             - Requisition reference / Job ID (internal tracking — RFP 10.2)
│   │             - Business unit selector, hiring manager name, country
│   │             - Consent language preference
│   │           IF "Enter Data Directly" mode (non-candidate — NEW):
│   │             - Full candidate data form (all sections):
│   │                 Personal: name, DOB, gender, email, mobile, address, nationality
│   │                 Employment: all employer records (company, designation, dates, supervisor)
│   │                 Education: all qualifications (institution, degree, year, roll number)
│   │                 Identity: Aadhaar, PAN, Passport (per package requirements)
│   │             - Document upload: client HR uploads documents on candidate's behalf
│   │         Step 3 — Duplicate Check:
│   │           - Real-time duplicate detection alert: "This candidate was verified in [previous case] on [date] for [package]. Outcome: [color]."
│   │           - Options: Use previous report / Initiate fresh verification / Cancel
│   │         Step 4 — Review & Confirm:
│   │           IF "Invite Candidate": Summary card + [Confirm & Send Invitation] button
│   │           IF "Enter Data Directly" [NEW]:
│   │             - Consent Declaration (mandatory before submit):
│   │               "I confirm [candidate name] has provided consent for KPMG to conduct
│   │                background verification. I am authorised to submit this data."
│   │             - [Confirm & Submit to KPMG] button (no invitation sent)
│   │         Step 5 — Confirmation:
│   │           - Case ID generated
│   │           IF "Invite Candidate": Invitation delivery status (Email/SMS/WhatsApp)
│   │           IF "Enter Data Directly": "Case submitted to KPMG ops — no candidate invitation sent"
│   │             initiation_mode: client_direct_entry logged in audit
│   │           - [Go to Case] button
│   │
│   ├── 2.2 Bulk Case Upload
│   │   └── Page: Bulk Case Initiation Interface
│   │       Purpose: Upload multiple candidates from Excel per RFP 10.15
│   │       RFP: 10.15 (bulk invite, bulk operations), 13.1 (pre-filled candidate details)
│   │       Two modes via tabs [NEW — C-01]:
│   │       ─────────────────────────────────────────────────────────────────
│   │       TAB 1 — Bulk Invite (existing standard flow):
│   │         Purpose: Upload candidate list, system sends invitations to each candidate
│   │         Components:
│   │         - Excel template download (columns: name, email, mobile, package, BU, country)
│   │         - File upload dropzone (drag-and-drop)
│   │         - Validation engine:
│   │             * Format check (column headers match template)
│   │             * Required field validation (name, email/mobile mandatory)
│   │             * Package name validation (must match configured packages)
│   │             * Duplicate detection (highlight rows where candidate already exists)
│   │             * Error summary: "18 rows valid, 3 rows with errors"
│   │         - Row-level error display (error icon per cell, hover for message)
│   │         - Fix and re-upload flow (download errors-only file, correct, re-upload)
│   │         - Preview table: All valid rows with parsed values
│   │         - Confirm & Create button → invitations sent to all candidates
│   │         - Bulk status results: Created / Duplicate (skipped) / Failed — with Case IDs
│   │         - Download results summary (Excel)
│   │       ─────────────────────────────────────────────────────────────────
│   │       TAB 2 — Bulk Pre-filled Data (non-candidate — NEW — C-01 | RFP 10.15, 13.1):
│   │         Purpose: Upload complete candidate data for multiple candidates — no
│   │                  invitations sent. Client HR has all data and submits directly.
│   │                  Covers legacy "50% manual entry via Excel" (PPTX).
│   │         Components:
│   │         - Excel template download (extended columns: all personal, employment,
│   │             education, identity fields + ConsentObtained column)
│   │         - ConsentObtained column: must be "Yes" for every row — system blocks
│   │             submission if any row has "No" or blank
│   │         - File upload dropzone
│   │         - Validation engine (same format/required/duplicate checks as Tab 1)
│   │         - Consent declaration banner (displayed before confirm):
│   │             "By submitting, you confirm all candidates in this file have provided
│   │              consent for KPMG to conduct background verification on their behalf."
│   │         - [Confirm & Submit to KPMG] button (no invitations triggered)
│   │         - On submit: cases created with initiation_mode = client_bulk_prefilled
│   │         - All cases: status = "Submitted to KPMG Ops" (no "Pending Candidate" step)
│   │         - Bulk status results: Created / Skipped / Failed — with Case IDs
│   │         - Document upload (post-creation): upload ZIP of documents per candidate
│   │             System matches documents to cases by candidate name/email
│   │
│   ├── 2.3 All Cases
│   │   └── Page: Client Case List
│   │       Purpose: View and manage all cases initiated by this client
│   │       Components:
│   │         - Case table: Case ID | Candidate Name | Package | Business Unit | Country | Status | Outcome Color | SLA Status | Candidate Submission | Report Available | Created Date
│   │         - Status badge: Not Started / Pending Candidate / In Verification / Pending Client Review / Completed / On Hold
│   │         - Outcome color badge (post-completion): Green / Amber / Yellow / Red
│   │         - SLA status: On Track / At Risk / Breached
│   │         - Filter: Status, Package, Business Unit, Country, Date range, Outcome color, SLA status
│   │         - Search: Candidate name, email, Requisition ref, Case ID
│   │         - Export (Excel/CSV — client-permitted fields only)
│   │         - Bulk re-invite (for candidates who have not submitted)
│   │         - Bulk export reports (download all ready reports as ZIP)
│   │         - Row click → Case Detail (client view)
│   │
│   ├── 2.4 Case Detail (Client View)
│   │   └── Page: Case Status View — Client Perspective
│   │       Purpose: Client-facing case status with appropriate information filtering
│   │       (No ops internals, no vendor details, no intermediate AI flags shown)
│   │       Components:
│   │         - Case header: Case ID | Candidate | Package | Status | Overall Outcome color (post-adjudication)
│   │         - Check status timeline: Visual per-check progress (Not Started / In Progress / Completed / Awaiting Candidate)
│   │         - "Pending Candidate Action" alert banner (if candidate has not submitted)
│   │         - "Ready for Your Review" banner (if client adjudication approval required)
│   │         - Expected completion estimate (shown as date range)
│   │         - Per-check summary (when completed): Verified / Discrepancy found / Unable to Verify — no internal notes visible
│   │         - Report section: Download button when available; version history
│   │         - Discrepancy summary: Only adjudicated discrepancies shared with client (type + severity + resolution)
│   │         - Communication history: Only client-visible messages (not ops internal notes)
│   │         - Dispute initiation button
│   │         - Re-invite candidate button (if candidate not yet submitted)
│   │         - Close / On-Hold request button
│   │
│   └── 2.5 Pending My Action
│       └── Page: Client Action Required Queue
│           Purpose: Cases requiring client's response (adjudication approval, dispute response, waiver confirmation)
│           Components:
│             - Queue table: Case ID | Action type | Since | Deadline (if SLA applies)
│             - Action types: Client Adjudication Approval / Waiver Confirmation / Dispute Response
│             - Action-specific panel per item
│             - SLA countdown where client response has deadline
│
├── 3. REPORTS
│   ├── 3.1 Report Inbox
│   │   └── Page: Reports Ready for Download
│   │       Components:
│   │         - Report inbox table: Case ID | Candidate | Package | Report date | Outcome color | Version | [Download]
│   │         - New reports badge (unviewed reports highlighted)
│   │         - Report preview panel (open in-browser PDF viewer)
│   │         - Bulk download (select all / by date range / by outcome)
│   │         - Report expiry notice (if retention policy applies)
│   │         - Download activity log (who on client team downloaded, when)
│   │
│   ├── 3.2 Report Archive
│   │   └── Page: Full Historical Report Library
│   │       Components:
│   │         - Full archive searchable by candidate, date, package, outcome
│   │         - Re-issued report indicator (version > 1)
│   │         - Compare versions (for re-issued reports)
│   │
│   └── 3.3 Report Analytics
│       └── Page: Client-Specific Outcome Analytics
│           Components:
│             - Outcome distribution chart (Green/Amber/Yellow/Red breakdown, current month vs last 6 months)
│             - Discrepancy type frequency (what types of discrepancies appear most in their hires)
│             - TAT trend (avg verification time for their cases)
│             - Package performance comparison
│             - Business unit comparison
│             - Export to Excel
│
├── 4. CONFIGURATION (Client Admin Role)
│   ├── 4.1 Package Manager
│   │   └── Page: Screening Package Configuration
│   │       Purpose: Client defines their own screening packages per RFP 12.1–12.4
│   │       Components:
│   │         - Package list (client's configured packages)
│   │         - [Create Package] wizard:
│   │             * Package name and description
│   │             * Check type selector (multi-select from enabled checks)
│   │             * Per-check configuration (depth: standard/enhanced/comprehensive)
│   │             * Role/level association (this package defaults for which job roles)
│   │             * Country applicability (which countries this package applies to)
│   │             * Estimated TAT (calculated based on check mix)
│   │             * Cost preview (if pricing configured)
│   │         - Package activation / deactivation
│   │         - Package audit history (who changed what, when)
│   │         - Duplicate package (clone and modify)
│   │
│   ├── 4.2 User Management
│   │   └── Page: Client User Administration
│   │       Components:
│   │         - User table: Name | Email | Role | Business Unit | Last Login | Status
│   │         - [Add User] form: Name, email, role (Initiator/Viewer/Admin), business unit
│   │         - Role description tooltip (what each role can do)
│   │         - Business unit data segregation (Viewer in BU-A cannot see BU-B cases)
│   │         - Temporary access with expiry date
│   │         - SSO/SAML configuration (for enterprise client SSO integration — RFP 13.3)
│   │         - Deactivate user (with open case notification)
│   │
│   ├── 4.3 Form Builder
│   │   └── Page: Custom Form Configuration
│   │       Purpose: Customize consent forms, employer forms, reference questionnaires per RFP 12.5
│   │       Components:
│   │         - Form type selector: Candidate Consent / Employer Verification / Reference Questionnaire / Candidate Declaration
│   │         - Drag-and-drop field builder
│   │         - Field types: Text / Dropdown / Date / Checkbox / File Upload / Signature
│   │         - Mandatory/Optional toggle per field
│   │         - Conditional field logic (show field X only if field Y = Z)
│   │         - Multi-language versions per form
│   │         - Form preview (desktop + mobile)
│   │         - Form version history + rollback
│   │         - Publish / Draft status
│   │
│   ├── 4.4 Color Code Matrix
│   │   └── Page: Outcome Color Configuration
│   │       Purpose: Define what each outcome color means for this client per RFP 12.11, 18.9
│   │       Components:
│   │         - Color matrix table: Scenario / Discrepancy combination → Color assignment
│   │         - Pre-built color schemes (Conservative / Standard / Flexible)
│   │         - Custom scenario builder (IF discrepancy type = X AND severity = Y THEN color = Z)
│   │         - Color meaning descriptions (what each color means for their hiring policy)
│   │         - Preview: How sample case outcomes would appear with this matrix
│   │         - Audit history of color matrix changes
│   │
│   ├── 4.5 Holiday List Manager
│   │   └── Page: Holiday Configuration for TAT/SLA Calculation
│   │       Components:
│   │         - Holiday list by country/state
│   │         - Import from Excel
│   │         - Add/edit/delete individual holidays
│   │         - Preview: SLA impact example (how a holiday affects TAT for a standard package)
│   │
│   ├── 4.6 Branding Configuration
│   │   └── Page: Candidate Portal White-Label Settings
│   │       Components:
│   │         - Logo upload (dimensions + format guide)
│   │         - Primary color picker (for candidate portal button/header color)
│   │         - Custom domain configuration (verification.clientdomain.com)
│   │         - Welcome message editor (multilingual)
│   │         - Completion message editor
│   │         - Support contact configuration (which phone/email candidates call for help)
│   │         - Preview (live candidate portal preview with branding applied)
│   │
│   ├── 4.7 Integration Settings
│   │   └── Page: ATS/HRIS Integration Configuration
│   │       Purpose: Connect ATS/HRIS for auto-initiation per RFP 13.1–13.3
│   │       Components:
│   │         - Connector catalog: Workday / SAP SuccessFactors / Oracle HCM / Darwinbox / Keka / Generic REST API
│   │         - Connection wizard:
│   │             * Authentication method (OAuth / API Key / Webhook secret)
│   │             * Credential entry and secure storage
│   │             * Field mapping table (ATS field → KCheck field)
│   │             * Trigger event configuration (which ATS event initiates BGV: Offer Accepted / Pre-Join / Other)
│   │         - Sandbox test mode (test connection with mock data)
│   │         - Integration health monitor (last sync, errors, latency)
│   │         - Webhook configuration (KCheck → ATS: send case status updates, report availability)
│   │         - Event log (all sync events with status)
│   │
│   ├── 4.8 Adjudication Policy
│   │   └── Page: Client Adjudication Rules
│   │       Purpose: Configure client-specific adjudication rules and approval requirements per RFP 10.9
│   │       Components:
│   │         - Auto-approve threshold (which outcomes auto-approve without client sign-off)
│   │         - Client sign-off requirement (which outcome types require explicit client approval before report release)
│   │         - Pre-adverse notice settings (waiting period duration, delivery method)
│   │         - Waiver policy (which types of waivers client pre-authorizes)
│   │
│   └── 4.9 Custom Field Registry  [NEW — C-08 | RFP 12.3]
│       └── Page: Custom Data Field Management
│           Purpose: Register client-specific data fields that extend the standard case data
│                    model — beyond form presentation into searchable, exportable, API-queryable
│                    case attributes scoped per client / BU / country.
│           RFP: 12.3 | Actor: Client Admin
│           Components:
│             - Custom field registry table:
│                 Field Key (API) | Display Label | Data Type | Scope | Required | Searchable | Exportable | Status
│             - [Add Custom Field] wizard:
│                 Field key (alphanumeric, no spaces, immutable once saved)
│                 Display label (shown in UI — editable)
│                 Data type: Text / Number / Date / Dropdown / Boolean / Multi-select
│                 For Dropdown/Multi-select: option values list
│                 Scope: Client-wide / Specific BU / Specific country (or combinations)
│                 Required / Optional / Conditional
│                 Searchable in All Cases: Yes / No
│                 Exportable in bulk export and reports: Yes / No
│                 Visible in: Candidate form / Ops portal / Client portal / All
│             - Max 50 custom fields per client tenant
│             - Deactivate field (hides from new cases — historical data preserved)
│             - Fields automatically appear in Form Builder palette after registration
│
├── 5. BILLING & INVOICING
│   └── Page: Client Billing Dashboard
│       Purpose: Invoice visibility and financial management per RFP 22.1
│       Components:
│         - Invoice list: Invoice date | Period | Check count | Amount | Status (Paid/Unpaid/Disputed) | Download
│         - Current month usage tracker: Checks initiated, volume slab, cost-to-date
│         - Per-check cost breakdown (what each check type costs)
│         - Volume slab progress bar (approaching next tier indicator)
│         - Add-on charge breakdown (rush processing, additional checks, re-verifications)
│         - Invoice dispute button (opens dispute form sent to KPMG billing)
│         - Payment history
│         - Cost center / PO number assignment per invoice
│
└── 6. ANALYTICS & INSIGHTS
    └── Page: Client BGV Analytics Dashboard
        Purpose: Strategic insights for HR leadership and hiring managers per RFP 18.10
        Components:
          - Time period selector (MTD / QTD / YTD / Custom)
          - Volume by business unit (horizontal bar chart)
          - Package utilization breakdown (which packages used most)
          - Outcome distribution trend (monthly — is discrepancy rate increasing?)
          - TAT trend by package
          - Discrepancy type frequency (what types of issues found in their candidate pool)
          - Top discrepancy-contributing check types
          - Candidate completion rate (what % complete form within 48h)
          - Geography distribution (India / Global breakdown if applicable)
          - Export to Excel / PowerPoint-ready charts

├── 7. COMPLIANCE  [NEW — C-11 | RFP 22.4]
│   └── 7.1 Audit Evidence Request
│       └── Page: Client Audit Evidence Request
│           Purpose: Formal channel for client to exercise contractual right to audit
│                    KPMG's verification controls and evidence for their candidates.
│                    RFP 22.4: "Customer right to audit vendor controls and evidence."
│                    Distinct from the standard BGV report — this is a formal audit mechanism.
│           RFP: 22.4 | Actor: Client Admin
│           Components:
│             - [Raise Audit Request] wizard:
│                 Request type:
│                   • Per-case evidence audit (select specific case IDs)
│                   • Process controls evidence (KPMG verification methodology)
│                   • Compliance documentation (DPA, subprocessor list, certifications)
│                   • Combined (any/all of the above)
│                 Scope: Case ID selector (multi) OR date range OR "all cases"
│                 Purpose / reason: free text (contractual audit / regulatory inspection /
│                                   dispute resolution / annual vendor review)
│                 Preferred format: PDF pack / In-portal view / Both
│             - Request status tracker:
│                 Request ID | Type | Submitted | Status | KPMG Owner | Evidence Ready date
│                 Status values: Submitted → In Review → Evidence Preparation →
│                                Ready for Download → Downloaded → Closed
│             - Evidence download section:
│                 Secure download link (time-limited: 72 hours)
│                 Download log (who downloaded, when)
│             - ITSM integration: auto-creates ServiceNow Service Request (via C-06)
│             - Request history: All past audit requests and their responses
```

---

## 5.3 CANDIDATE PORTAL — Full Expanded IA

```
CANDIDATE PORTAL
│
├── 1. ENTRY & AUTHENTICATION
│   ├── 1.1 Invitation Landing Page
│   │   └── Page: Welcome Landing (from invitation link)
│   │       Components:
│   │         - Client-branded header (logo, welcome message — white-labeled)
│   │         - Explanation: "Your employer [Client Name] has initiated a background verification"
│   │         - What to expect (timeline, steps, estimated time to complete)
│   │         - Mobile-optimized layout (client's majority users are mobile)
│   │         - Language selector (multilingual — RFP 19.6)
│   │         - [Begin Verification] button
│   │
│   └── 1.2 OTP Authentication
│       └── Page: Identity Verification & Session Start
│           Components:
│             - Mobile number display (masked — pre-filled from invitation)
│             - [Send OTP] button (WhatsApp first, SMS fallback)
│             - OTP entry field (6-digit, auto-advance)
│             - Resend OTP (with 30-second cooldown)
│             - Use email instead option (fallback)
│             - Session creation on successful OTP
│             - Device fingerprint capture (background, for fraud detection)
│             - Geo-location request (consent-disclosed, background capture)
│
├── 2. CONSENT & DISCLOSURE
│   └── 2.1 Consent Capture
│       └── Page: Privacy Notice & Consent
│           Purpose: DPDP/GDPR-compliant consent capture — primary compliance page
│           Components:
│             - Client-branded header
│             - Consent notice body (scrollable, full text required):
│                 * Data controller identity (KPMG + client)
│                 * Categories of personal data collected
│                 * Specific purposes for each data category
│                 * Third parties / subprocessors (obfuscated as "verification agencies")
│                 * Data retention periods (per check type)
│                 * Candidate rights: access, correction, erasure, restriction, portability, object
│                 * Grievance officer contact
│                 * Right to withdraw consent (with consequence disclosed)
│             - "I have read and understood" scroll confirmation (scrolled to bottom detection)
│             - FCRA-style disclosure section (jurisdiction-applicable — separate section)
│             - Relationship/directorship disclosure (if package requires)
│             - Financial check consent (separate explicit consent if package includes credit check)
│             - E-signature capture options:
│                 * On-screen drawn signature (canvas)
│                 * Type-to-sign (name typed as signature)
│                 * DocuSign redirect (for enterprise-grade e-sign)
│             - Timestamp and session metadata captured at signature
│             - Consent receipt screen: "Your consent has been recorded. Download receipt."
│             - [Download Consent Receipt PDF] button
│             - [Proceed to Verification Form] button (disabled until signature complete)
│
├── 3. VERIFICATION FORM (Dynamic Multi-Step Wizard)
│   ├── 3.1 Progress Tracker
│   │   └── Component: Persistent progress bar (step indicator at top)
│   │       - Step names visible: Personal → Employment → Education → Identity → Documents → Review → Submit
│   │       - Completed steps shown in green with checkmark
│   │       - Auto-save indicator ("Saved" on every field blur)
│   │       - Resume capability (OTP re-auth shows "Continue where you left off")
│   │
│   ├── 3.2 Personal Details
│   │   └── Page: Personal Information Form
│   │       Components:
│   │         - Full legal name (as per ID — cannot differ from ID documents)
│   │         - Date of birth (date picker with age validation)
│   │         - Gender (optional, package-dependent)
│   │         - Nationality (dropdown — triggers country-specific form sections)
│   │         - PAN number (masked input, format validation)
│   │         - Aadhaar number (masked input, format validation, optional consent toggle for Aadhaar use)
│   │         - Current address (address lookup with auto-complete, manual entry fallback)
│   │         - Permanent address (checkbox: "Same as current" or separate entry)
│   │         - Mobile number (pre-filled from invitation, editable)
│   │         - Alternate email
│   │         - Relationship/directorship declarations (conditional — if package requires):
│   │             * Are you related to any KPMG employee? (Yes/No)
│   │             * Do you hold directorships? (Yes/No → if Yes, list them)
│   │         - Field tooltips (info icon next to each sensitive field — configurable text)
│   │         - Real-time inline validation (format errors shown immediately)
│   │         - [Save & Continue] button
│   │
│   ├── 3.3 Employment History
│   │   └── Page: Employment Entry Form
│   │       Components (per employment entry — repeating section):
│   │         - Employer/Company name (with auto-suggest from known company database)
│   │         - Designation / Job title
│   │         - Employment type (Full-time / Part-time / Contract / Internship)
│   │         - Start date / End date (date pickers — end date = "Currently working here" toggle)
│   │         - Location (city, country)
│   │         - HR/Manager contact name and email/mobile (for verification outreach)
│   │         - Reason for leaving (dropdown + free text)
│   │         - Supervisor name (optional)
│   │         - [Add Another Employer] button
│   │         - [Remove] button per entry
│   │         Smart Validation:
│   │           - Employment gap detection: "We noticed a gap from [date] to [date]. Please explain or add any self-employment, study, or break." → Expandable gap explanation field
│   │           - Dual employment warning: "These two employments overlap. Please verify your dates."
│   │           - Date validation: Cannot have future start dates
│   │         Resubmission Mode:
│   │           - Approved fields shown read-only with lock icon
│   │           - Only ops-flagged fields editable
│   │           - Insufficient remark displayed above flagged field: "Please provide the correct end date for this employer."
│   │
│   ├── 3.4 Education History
│   │   └── Page: Education Entry Form
│   │       Components (per education entry — repeating):
│   │         - Highest qualification type (Bachelor's / Master's / Diploma / 10th / 12th / Doctorate / Professional)
│   │         - Institution name
│   │         - University / Board (for 10th/12th) — dropdown with known institutions
│   │         - Year of enrollment / Year of passing
│   │         - Percentage / CGPA
│   │         - Course/stream (Engineering / Commerce / Arts etc.)
│   │         - DigiLocker fetch option: [Fetch from DigiLocker] button → OAuth to DigiLocker, auto-populates fields from fetched certificate
│   │         - Name mismatch handling: If certificate name differs from profile name → prompt for name change affidavit upload
│   │         - [Add Another Qualification] button
│   │         Smart Validation:
│   │           - Course duration check: "A 4-year engineering degree cannot start in 2018 and end in 2019."
│   │           - Year logic: Graduation year must be > enrollment year
│   │
│   ├── 3.5 Other Check-Specific Sections (Dynamic — shown per package)
│   │   ├── Address Confirmation: Current address confirmation with geocoding
│   │   ├── References: Add reference contacts (name, designation, relationship, mobile/email) — shown if reference check package
│   │   ├── Financial Declarations: Consent for credit check (separate explicit consent)
│   │   └── Legal Declarations: "Have you ever been convicted of a criminal offense?" (Yes/No with details)
│   │
│   ├── 3.6 Document Upload
│   │   └── Page: Document Submission Center
│   │       Purpose: Upload all required supporting documents per RFP 11.5
│   │       Components:
│   │         - Document checklist (required documents based on package — dynamic):
│   │             * Government ID (Aadhaar / PAN / Passport / DL — at least one required)
│   │             * Current address proof
│   │             * Employment documents (offer letter, relieving letter, payslips — per employer)
│   │             * Education certificates (per degree)
│   │             * Additional as per check flags
│   │         - Per-document upload widget:
│   │             * Drag-and-drop or [Upload] button
│   │             * Camera capture option (mobile) with scan guide overlay
│   │             * File type guidance: PDF / DOCX (Word) / XLSX (Excel) / JPG / PNG / ZIP
│   │               Max 10 MB per file; ZIP max 50 MB extracted, max 20 files inside
│   │               Word and Excel are converted to PDF for secure viewing — original preserved
│   │               ZIP files are extracted and each document quality-checked individually
│   │             * Real-time quality feedback (AI-powered):
│   │                 - "Image is blurry — please retake"
│   │                 - "Glare detected — reposition document"
│   │                 - "Document appears cropped — ensure all corners visible"
│   │                 - "Quality: Good / Fair / Poor" indicator
│   │             * OCR extraction preview: "We extracted: Name: [X], DOB: [Y]. Does this match?"
│   │             * Upload progress bar
│   │             * Re-upload / Replace button
│   │         - Overall checklist status: "4 of 6 documents uploaded. Missing: [list]"
│   │         - [Skip for now] option for optional documents (with reminder that it may delay verification)
│   │
│   ├── 3.7 Biometric Capture (Conditional)
│   │   └── Page: Identity Verification — Liveness & Face Match
│   │       Purpose: Biometric identity verification per RFP 2.1–2.4
│   │       Components:
│   │         - Camera access request screen (explains why camera needed, consent reminder)
│   │         - Biometric consent confirmation (separate explicit step — special category data)
│   │         - Liveness type (from package config):
│   │             Active: Step-by-step challenge (blink, turn left, turn right — animated guide)
│   │             Passive: Single selfie with quality check
│   │         - Camera viewfinder with face alignment guide (oval overlay)
│   │         - Result screen:
│   │             Success: "Identity verified. Face matched with your ID documents."
│   │             Retry: "Unable to verify. Please ensure good lighting and remove glasses." (up to 3 attempts)
│   │             Escalate: "Verification could not be completed automatically. A manual review will be performed." (after 3 failed attempts)
│   │         - Privacy assurance message (biometric data not stored, only match score retained)
│   │         - [Skip if not mandatory] (rare — depends on package)
│   │
│   └── 3.8 Review & Submit
│       └── Page: Final Submission Review
│           Components:
│             - Full summary of all submitted information (sections collapsible)
│             - Document upload status per document
│             - Edit links per section (back navigation with state preserved)
│             - Completeness indicator: "All required information submitted" vs "Missing items: [list]"
│             - Declaration statement (checkbox): "I declare that all information provided is true and accurate to the best of my knowledge."
│             - [Submit Application] button (disabled until completeness = 100% for mandatory items)
│             - Submission confirmation screen:
│                 * Success message (client-branded)
│                 * Case reference number
│                 * "What happens next" timeline
│                 * Estimated completion date
│                 * Status check link
│
├── 4. STATUS TRACKING
│   └── Page: My Application Status
│       Components:
│         - Overall progress indicator (stages: Submitted → Verification In Progress → Completed)
│         - Per-check status tracker (visual timeline):
│             * Employment check: In Progress / Awaiting Employer Response / Completed
│             * Education check: In Progress / Completed
│             * KYC: Completed
│             (No ops-internal details exposed — only high-level status)
│         - "Action Required" alert banner:
│             * "KPMG requires additional information for your employment at [Company]. Click to provide."
│         - Expected completion date estimate
│         - [Re-enter information] button (when insufficient notification received)
│         - [Contact Support] button
│         - Download consent receipt button
│
├── 5. RE-SUBMISSION (Triggered by Insufficiency)
│   └── Page: Additional Information Required
│       Components:
│         - Banner: "Some information needs to be updated. Please review the highlighted fields."
│         - KPMG's remarks per flagged field (field-level, specific: "Please provide a correct end date for ABC Corp.")
│         - Form with ONLY flagged fields editable (all other fields locked/read-only)
│         - Document re-upload for specific documents flagged insufficient
│         - Character counter on text fields
│         - [Submit Updated Information] button
│         - Confirmation screen + updated status
│
├── 6. DISPUTE
│   └── Page: Raise a Concern
│       Components:
│         - Dispute type selector:
│             * "My information is inaccurate in the verification"
│             * "I believe there is a process error"
│             * "I disagree with the outcome/findings"
│             * "I want to access my data" (DSAR — access request)
│             * "I want my data deleted" (DSAR — erasure request)
│             * "I want to correct my data" (DSAR — correction request)
│         - Description text area
│         - Supporting evidence upload
│         - Contact preference for response (email / mobile)
│         - [Submit] button
│         - Dispute status tracker (submitted / under review / resolved)
│         - Resolution notification
│
└── 7. SUPPORT
    └── Page: Help & Support
        Components:
          - In-portal chat widget (bot + live agent fallback)
          - FAQ accordion (multilingual, organized by stage of process)
          - [Email Support] form
          - Toll-free helpline (country-specific)
          - WhatsApp support deeplink
          - Session info display (Case reference for when calling support)
          - Estimated response time display
```

---

## 5.4 VENDOR PORTAL (DESK) — Full Expanded IA

```
VENDOR PORTAL (DESK VENDORS)
│
├── 1. DASHBOARD
│   └── Page: Vendor Operations Dashboard
│       Components:
│         - KPI strip: [New Assignments] [In Progress] [Completed Today] [SLA At Risk] [Overdue]
│         - Assignment status distribution (donut chart)
│         - SLA countdown list (top 10 cases closest to breach)
│         - My performance scorecard (TAT compliance %, quality score)
│         - Notification center (new assignments, reminders, QC feedback)
│         - [Acknowledge All New] quick action button
│
├── 2. CASE QUEUE
│   ├── 2.1 New Assignments
│   │   └── Page: Assignment Inbox
│   │       Components:
│   │         - Assignment table: Case ID | Check type | Geography | SLA deadline | Documents available | Assignment date
│   │         - [Acknowledge] button per row (marks as accepted, starts vendor SLA clock)
│   │         - [Decline] button (with reason — routes back to KPMG for reassignment)
│   │         - Bulk acknowledge action
│   │         - Case documents panel: Candidate-submitted documents relevant to this specific check (not full case)
│   │         - Assignment instructions from KPMG ops (if any notes attached)
│   │         - SLA deadline display (date + countdown)
│   │
│   ├── 2.2 In Progress
│   │   └── Page: Active Assignment Workspace
│   │       Components:
│   │         - Active cases table with SLA indicators
│   │         - Case evidence submission interface per case:
│   │             * Check-type-specific structured form (Employment: confirmation dates / Education: enrollment confirmed / Legal: case records)
│   │             * Evidence file upload (findings report, supporting documents)
│   │             * Outcome declaration: Verified / Discrepancy Found / Unable to Verify / Partial
│   │             * Notes to KPMG ops (free text)
│   │             * [Submit Evidence] button
│   │         - Status update capability: Move to "In Progress" / "Awaiting Response" / "Completed"
│   │         - SLA breach alert banner (when approaching deadline)
│   │
│   └── 2.3 Completed Assignments
│       └── Page: Completed Case Archive
│           Components:
│             - Completed cases with submission date and outcome
│             - QC feedback received per case (if KPMG QC flagged an error)
│             - [View Submission] for each (read-only after submission)
│             - Performance trend (last 30 days acceptance/TAT metrics)
│
├── 3. SLA TRACKER
│   └── Page: My SLA Health Dashboard
│       Components:
│         - All active assignments with SLA status
│         - Color-coded SLA health (Green/Amber/Red)
│         - Cases at breach risk highlighted
│         - SLA compliance rate (last 30/90 days)
│         - Historical SLA breach record
│         - SLA extension request form (with reason — routes to KPMG for approval)
│
├── 4. COMMUNICATIONS
│   └── Page: KPMG Communication Channel
│       Components:
│         - Message thread per case (with KPMG ops)
│         - Standard message templates (clarification request, extension request, unable to verify notice)
│         - Attachment capability
│         - Message history and read receipts
│
└── 5. PROFILE & SETTINGS
    ├── 5.1 My Organization Profile
    │   └── Page: Vendor Account Details
    │       Components:
    │         - Organization details (name, address, GSTN, PAN)
    │         - Coverage configuration (check types supported, geographies)
    │         - Bank details (for payment — masked)
    │         - DPA/contract document upload
    │
    └── 5.2 User Management (Vendor-side)
        └── Page: My Team
            Components:
              - Add/manage vendor-side users
              - Role: Verifier / Team Lead / Manager
              - Case visibility scope per user
```

---

## 5.5 SUPER ADMIN PORTAL — Full Expanded IA

```
SUPER ADMIN PORTAL
│
├── 1. PLATFORM OVERVIEW DASHBOARD
│   └── Page: KPMG Platform Command Center
│       Components:
│         - Platform KPIs: [Active Tenants] [Total Cases Today] [System Uptime] [API Error Rate] [Avg Response Time]
│         - Tenant health map (grid of tenants with status)
│         - System health panel: API gateway status, domain service status, queue depths, DB performance
│         - AI service health: OCR accuracy (today), face match accuracy, liveness pass rate, fraud flag rate
│         - Security alert panel: Failed logins, unusual activity, geo-anomalies
│         - Active incidents (if any — with severity)
│         - Notification delivery platform health (channel-wise success rate across all tenants)
│         - Data residency compliance indicator (green if all tenants within policy)
│
├── 2. TENANT MANAGEMENT
│   ├── 2.1 All Tenants
│   │   └── Page: Client Organization Registry
│   │       Components:
│   │         - Tenant list: Org name | Type | Status | Active cases | Contract start/end | Primary contact | Data residency region
│   │         - Status: Active / Trial / Suspended / Offboarded
│   │         - [Provision New Tenant] button
│   │         - Tenant drill-in: Full configuration + usage stats
│   │         - Suspend tenant action (with data freeze)
│   │         - Offboarding workflow (data export + deletion schedule)
│   │
│   ├── 2.2 Tenant Onboarding
│   │   └── Page: New Tenant Provisioning Wizard
│   │       Steps:
│   │         1. Organization details (name, type, primary contact, contract dates)
│   │         2. Data residency selection (India / EU / US / Multi-region)
│   │         3. Country/jurisdiction scope (which countries this tenant operates in)
│   │         4. Check types enabled for this tenant
│   │         5. AI features enabled (face match, fraud detection, auto-decisioning)
│   │         6. Branding seed (logo, domain prefix)
│   │         7. Default SLA templates
│   │         8. Initial admin user creation
│   │         9. Activation
│   │
│   └── 2.3 Tenant Configuration
│       └── Page: Per-Tenant Deep Configuration
│           Components:
│             - All tenant settings (editable from Super Admin)
│             - Feature flag overrides per tenant
│             - Data residency setting change (with migration trigger)
│             - Enabled check types
│             - AI confidence threshold overrides
│             - Contract details and renewal alerts
│
├── 3. RULE ENGINE
│   └── Page: Global Platform Rule Configuration
│       Components:
│         - Auto-routing rules editor (case assignment logic — configurable IF/THEN)
│         - Auto-decisioning threshold configuration (Clear threshold, auto-escalate threshold)
│         - Escalation matrix templates (for new tenants)
│         - SLA policy templates (default SLA tiers)
│         - Risk scoring rule configuration (weights for composite risk score components)
│         - Rule version history + rollback
│         - Rule simulation (test rule change with historical cases before deployment)
│
├── 4. AI GOVERNANCE
│   ├── 4.1 Model Registry
│   │   └── Page: AI Model Version Management
│   │       Components:
│   │         - Model catalog: OCR, Face Match, Liveness, Deepfake Detector, Fraud Scorer, Document Authenticator
│   │         - Per-model: Current version, accuracy metrics, deployment date, previous version
│   │         - Model health indicators: Drift score, accuracy degradation alert
│   │         - Rollback to previous version capability
│   │         - Model changelog (what changed between versions)
│   │
│   ├── 4.2 Threshold Configuration
│   │   └── Page: AI Decision Threshold Management
│   │       Components:
│   │         - Per-model confidence thresholds (auto-pass / review-required / auto-fail)
│   │         - Per-tenant threshold overrides
│   │         - Impact simulation (changing threshold X would affect Y% of cases)
│   │         - Threshold change audit log
│   │
│   ├── 4.3 Bias & Fairness Monitor
│   │   └── Page: AI Bias and Subgroup Performance Dashboard
│   │       Purpose: RFP 2.17 — Monitor for demographic bias in AI decisions
│   │       Components:
│   │         - Subgroup performance table (demographic dimension — where data available)
│   │         - Disparity alert (if one group has significantly higher AI rejection rate)
│   │         - False positive/negative rate by subgroup
│   │         - Bias investigation trigger (escalate to AI team)
│   │         - Fairness audit export
│   │
│   └── 4.4 AI Explainability Audit
│       └── Page: AI Decision Reason Code Quality Review
│           Components:
│             - Sample of AI decisions with reason codes
│             - Human review: Is the reason code accurate and explainable?
│             - Reason code accuracy rate
│             - Flag unexplainable decisions for model team
│
├── 5. SECURITY & COMPLIANCE
│   ├── 5.1 Platform Audit Log
│   │   └── Page: Cross-Tenant Platform Audit
│   │       Components:
│   │         - Platform-level events (tenant provisioning, admin actions, config changes)
│   │         - Security events (failed logins, unusual access patterns, admin escalations)
│   │         - Filter by event type, actor, tenant, date range
│   │         - Export for external audit
│   │
│   ├── 5.2 Incident Management
│   │   └── Page: Security Incident Response Center
│   │       Components:
│   │         - Incident registry (active + historical)
│   │         - Severity classifier (P1/P2/P3/P4)
│   │         - Breach notification workflow:
│   │             * Breach detected → affected tenant identification
│   │             * Country-specific DPA notification deadline (GDPR: 72h, DPDP: 72h)
│   │             * Notification draft generator
│   │             * Notification delivery log
│   │         - IR playbook steps (per incident type)
│   │         - Post-incident review (lessons learned)
│   │         - CISO escalation trigger
│   │
│   ├── 5.3 Data Residency Compliance Monitor
│   │   └── Page: Data Residency & Transfer Tracker
│   │       Components:
│   │         - Per-tenant data location map (visual world map with data location pins)
│   │         - Cross-border transfer log (when data crossed jurisdictions, legal basis)
│   │         - SCC/adequacy framework status per transfer corridor
│   │         - Residency policy breach alert (if data detected outside mandated region)
│   │         - Export residency compliance report for DPA submission
│   │
│   └── 5.4 Penetration Test & Vulnerability Tracker
│       └── Page: Security Assurance Dashboard
│           Components:
│             - Last pen test date and scope
│             - Open vulnerability tracker (critical/high/medium/low)
│             - Remediation status and target dates
│             - CVE watch for platform dependencies
│             - Compliance certification status (ISO 27001, SOC 2)
│
├── 6. INTEGRATION REGISTRY
│   └── Page: Platform-Wide API & Connector Management
│       Components:
│         - All active integrations (ATS connectors, AI vendor APIs, government DB APIs, notification providers)
│         - Per-integration health: Status, last success, error rate, latency
│         - API credential rotation log
│         - Subprocessor registry (DPDP/GDPR required — list of all third parties processing data — RFP 22.3)
│         - DPA status per subprocessor
│         - Integration addition workflow (new vendor API onboarding)
│
├── 7. BILLING CONFIGURATION
│   └── Page: Platform Pricing & Billing Setup
│       Components:
│         - Per-tenant pricing table (per check type)
│         - Volume slab configuration (per tenant)
│         - Invoice generation schedule (monthly/quarterly)
│         - SLA penalty calculation rules
│         - Invoice generation trigger (manual or scheduled)
│         - Revenue analytics (platform-level, per tenant summary)
│
└── 8. BUILD & RELEASE MANAGEMENT
    └── Page: Platform Release & Feature Management
        Components:
          - Environment status panel (Dev / UAT / Prod — green/red)
          - Active feature flags (per environment, per tenant)
          - Feature flag toggle (enable feature for specific tenant only — canary)
          - Recent deployments log (version, deploy date, deployer)
          - Rollback trigger (one-click rollback to previous version)
          - Maintenance mode toggle (per portal, with user-facing message editor)
          - CI/CD pipeline status widget
```

---

## 5.6 FIELD AGENT MOBILE APP — Full Expanded IA

```
FIELD AGENT APP (PWA / Mobile-native)
│
├── 1. AUTHENTICATION
│   └── Page: Agent Login
│       Components:
│         - Username + OTP (or biometric login on supported devices)
│         - Offline mode indicator ("You are offline — previously assigned cases available")
│         - App version display (for support)
│
├── 2. MY ASSIGNMENTS (TODAY)
│   └── Page: Today's Assignment List
│       Components:
│         - Assignment cards: Case ID (anonymized reference) | Check type | Address | SLA deadline
│         - Priority indicator (SLA urgency)
│         - [Navigate] button (opens native maps with address)
│         - [View Details] button (candidate address details, contact instructions)
│         - Offline sync status ("3 pending submissions to sync")
│         - [Sync Now] button
│
├── 3. EVIDENCE CAPTURE (On-site)
│   └── Page: On-Site Verification Interface
│       Purpose: GPS-timestamped evidence capture per RFP 7.2–7.6
│       Components:
│         - GPS capture: Auto-capture on page load (lat/long/accuracy/timestamp)
│         - GPS status indicator: "Location acquired: [coords], Accuracy: ±10m"
│         - GPS anomaly warning: If current location is > 2km from declared address → yellow warning
│         - Photo capture:
│             * Camera viewfinder with overlay guide
│             * GPS metadata auto-embedded in photo
│             * Timestamp auto-embedded
│             * Anti-spoofing: Screenshots/gallery photos blocked; camera-only allowed
│             * Photo quality check (blur, insufficient lighting warning)
│             * Multiple photos (front of building, address plate, interior — as instructed)
│         - Structured verification checklist:
│             * "Address board/nameplate visible?" (Yes/No/Not applicable)
│             * "Candidate/Resident present at address?" (Yes/No)
│             * "Documents sighted?" (Yes/No)
│             * "Neighbor verification done?" (Yes/No → free text for neighbor statement)
│         - Digital signature capture (resident/neighbor signature where applicable)
│         - Notes field (additional observations)
│         - Outcome declaration: Address Confirmed / Address Not Confirmed / Unable to Verify / Partial
│         - [Submit] (online) OR [Save for sync] (offline queue)
│         - Tamper-detection: Submission metadata includes app integrity attestation
│
├── 4. OFFLINE QUEUE
│   └── Page: Pending Sync Queue
│       Components:
│         - List of submissions waiting to sync
│         - Upload progress on reconnection
│         - Sync conflict alert (if case was reassigned while offline)
│         - Clear completed syncs
│
└── 5. MY PERFORMANCE
    └── Page: Agent Dashboard
        Components:
          - Cases completed today/week
          - SLA compliance rate (this month)
          - Pending sync count
          - Feedback from QC (if any submissions flagged)
          - Contact KPMG ops (support line)
```

---

## 5.7 LIGHTWEIGHT EXTERNAL MODULES

### Employer Response Module
```
EMPLOYER RESPONSE MODULE (Tokenized Web Form)
│
├── Landing Page (from one-time link)
│   Components:
│     - KPMG branding
│     - Explanation: "You are being contacted to verify employment of [Candidate name] who has listed you as a former employer."
│     - Data protection notice (how this data is used, DPDP/GDPR)
│     - Identity confirmation: "Are you authorized to respond on behalf of [Company]?"
│     - [Proceed to Verification Form] button
│
├── Employment Verification Form
│   Components:
│     - Pre-filled candidate data (name, designation, dates as claimed)
│     - Fields to confirm or correct:
│         * Employment dates (Start date / End date — or "Still employed")
│         * Designation / Job title at joining, at leaving
│         * Department / Function
│         * Reason for leaving (dropdown + optional notes)
│         * Eligible for rehire? (Yes / No / With conditions)
│         * "Any concerns you wish to note?" (optional free text)
│     - Declaration checkbox (authorized to provide this information)
│     - [Submit Response] button
│     - Confirmation screen with submission reference
│
└── Already Responded Page
    - If link re-used: "This verification has already been completed. Thank you."
```

### University/Board Response Module
```
UNIVERSITY RESPONSE MODULE (Tokenized Web Form)
│
├── Landing Page
│   - Institution name confirmation
│   - Data protection notice
│
├── Academic Verification Form
│   Components:
│     - Pre-filled: Candidate name, degree claimed, year claimed, percentage claimed
│     - Fields to confirm or correct:
│         * Enrollment confirmed? (Yes/No)
│         * Degree conferred? (Yes/No)
│         * Year of passing (actual)
│         * Percentage/Grade (actual — or "Unable to disclose" option)
│         * Course/Program name
│         * Roll number / Registration number
│     - Batch response option: "If you need to respond for multiple students from your institution, please use our batch upload template."
│     - [Submit] button
│
└── Confirmation Screen
```

### Referee Response Module
```
REFEREE RESPONSE MODULE (Tokenized Web Form)
│
├── Landing Page
│   - Explanation: "You are listed as a professional reference for [Candidate name]."
│
├── Reference Questionnaire (Client-configured)
│   Components:
│     - Pre-filled: Candidate name, company, designation, relationship to referee
│     - Configurable questions (from client's form builder):
│         * "How long have you known this candidate professionally?"
│         * "Please rate their performance in the role." (1–5 scale)
│         * "Key strengths?" (free text)
│         * "Any areas for development?" (free text)
│         * "Would you recommend them for a similar role?" (Yes/No/With reservations)
│         * "Any concerns you wish to note?" (optional)
│     - Declaration checkbox
│     - [Submit] button
│
└── Confirmation Screen
```

### Auditor Read-Only Module
```
AUDITOR READ-ONLY MODULE (IP-restricted, session-limited)
│
├── Authentication
│   - KPMG-issued auditor credentials (OTP-based, time-limited)
│   - IP restriction enforced (auditor's declared IP range)
│   - Session timeout: 4 hours
│
├── Audit Pack Access
│   Components:
│     - Scope selector: Which cases / which time period to audit
│     - Case list (read-only, no action buttons)
│     - Consent records viewer (per case)
│     - Adjudication log viewer (per case)
│     - Communication log viewer (per case)
│     - Audit event trail viewer
│     - AI decision log (model version, reason codes — per case)
│
└── Export
    - Export audit pack per case (PDF + JSON with hash manifest)
    - Bulk export for date range
    - Download log (auditor's access and downloads logged)
```

---
# PART 6 — PAGE DESIGN DEPTH

## 6.1 OPERATIONS PORTAL — Detailed Page Designs (Part A: Queue & Management Pages)


---

## 6.1 OPERATIONS PORTAL

---

### 6.1.1 Page: Personal Work Queue

**1. Page Objective**
Every ops reviewer's entry point each day. Shows only cases assigned to them, prioritized by urgency. Enables immediate action without navigating elsewhere.

**2. Primary Actors** Ops Reviewer

**3. Key Workflows**
Login → land here → triage queue by SLA + risk → open case → work → return to queue → repeat

**4. States**
Empty queue (no assignments) | Active queue (cases present) | Filtered view | Bulk action mode

**5. Actions**
Open case, mark insufficient (quick action), assign to vendor (quick action), escalate (quick action), bulk assign, bulk send reminder, export, filter, sort

**6. Data Blocks**
Case ID, candidate name, client, check type, current status, SLA remaining, AI risk score, last action timestamp, assigned vendor (if any), insufficiency age (if pending candidate)

**7. UI Regions**
- Top bar: "My Queue" title + case count + last refreshed timestamp + [Refresh] button
- Filter bar: Check type | Client | SLA status | Risk level | Date range
- Bulk action toolbar (appears on row selection): Assign | Remind | Export | Escalate
- Queue grid (main): sortable columns
- Empty state: "No cases assigned to you. Check All Cases or contact your team lead."

**8. Cards**
- SLA urgency summary strip (above table): Green count | Amber count | Red count | Breached count — clickable to filter
- "Action required today" banner card: cases with SLA expiring within business hours

**9. Tables**
Queue grid columns: Case ID | Candidate | Client | Package | Check Type | Status | SLA Remaining | Risk Score | Last Action | Quick Actions
- SLA Remaining: live countdown, color-coded
- Risk Score: Low/Medium/High/Critical badge
- Status: color-coded badge (Not Started / In Progress / Pending Candidate / Pending Vendor)
- Quick Actions: [Open] [Insufficient] [Vendor] [Escalate] icons inline

**10. Drawers**
- Quick Preview Drawer (row click without [Open]): Case summary, last 3 audit events, SLA details, AI flags summary, [Open Full Case] button

**11. Modals**
- Quick Insufficient Modal: Field-level remarks + channel + confirm (without navigating to full case)
- Quick Escalate Modal: Reason + target + note + confirm

**12. Tabs** None — single view (filter controls serve tab purpose)

**13. Filters**
Check type (multi-select) | Client (multi-select) | SLA status (Green/Amber/Red/Breached/Paused) | Risk level | Status | Date created (range)

**14. Bulk Actions**
Bulk assign to vendor | Bulk send candidate reminder | Bulk escalate | Bulk export (role-scoped)

**15. Alerts/Banners**
- "You have [N] cases breaching SLA today" — red sticky banner
- "New case assigned to you" — toast notification on new assignment
- "Candidate re-submitted for Case [X]" — toast, prompts return to case

**16. Timeline/Audit**
No timeline on this list page. All audit is at the case level.

**17. SLA Components**
- Live countdown per row (auto-refreshes every 60s)
- Color transition: Green → Amber at 30% remaining → Red at 10% → Breached (strikethrough style)
- SLA paused indicator: "⏸ Paused" badge with pause reason tooltip

**18. AI Components**
- Risk score badge per row (Low/Medium/High/Critical — not raw number)
- "AI flagged" dot indicator on rows where AI has unreviewed flags

**19. Evidence Components** None at queue level

**20. Mobile Considerations**
Reviewers may check queue on mobile morning. Mobile: card view (not table), SLA countdown prominent, swipe-to-open gesture, urgent cases first. Full work on desktop.

---

### 6.1.2 Page: Team Performance Monitor (Team Lead Dashboard)

**1. Page Objective**
Give team leads real-time visibility into reviewer workloads, productivity, and queue distribution — enabling rebalancing without asking each reviewer individually.

**2. Primary Actors** Team Lead, Ops Manager

**3. Key Workflows**
Review reviewer capacity → Identify bottlenecks → Reassign cases → Monitor daily throughput → Identify reviewers needing support

**4. States**
Live view | Historical view (date range) | Filtered by team/shift

**5. Actions**
View reviewer detail, reassign case from one reviewer to another (drag-and-drop or modal), send internal message, flag reviewer for QC attention, export team report

**6. Data Blocks**
Per reviewer: name, active cases, completed today, avg TAT, insufficiency rate, QC error rate, SLA breach responsibility, current status (online/offline)

**7. UI Regions**
- Top: Team KPI strip — total active cases / cases completed today / team SLA compliance % / breach count today
- Center: Reviewer capacity table
- Right sidebar: Queue rebalance panel (drag-drop interface)
- Bottom: Team productivity trend charts

**8. Cards**
- Team Health Card: Overall SLA compliance % vs target
- Bottleneck Alert Card: Reviewer with highest queue depth highlighted
- "Cases needing reassignment" card: Unassigned cases + cases from unavailable reviewers

**9. Tables**
Reviewer table: Name | Online status | Active cases | Completed today | Avg TAT (week) | Insufficiency rate | QC error rate | SLA breach count (week) | [View Queue] [Reassign]

**10. Drawers**
- Reviewer Queue Drawer: Opens selected reviewer's full queue (same as My Queue view but for that reviewer). Team lead can reassign from here.
- Reassignment Drawer: Select cases to move, select target reviewer, confirm

**11. Modals**
- Reassign Cases Modal: Source reviewer → Target reviewer → Case list (checkboxes) → confirm

**12. Filters**
Team (if multiple teams) | Shift | Date range | Check type specialization

**13. Bulk Actions**
Bulk reassign (select multiple cases across reviewers → assign to one reviewer)

**14. Alerts/Banners**
- "[Reviewer X] has [N] SLA-critical cases and has been offline for [N] hours — reassignment recommended" — red
- "Team SLA compliance dropped below target today" — amber

**15. SLA Components**
Per-reviewer SLA breach count (week), team-level SLA compliance %, at-risk case count by reviewer

**16. AI Components**
None direct — AI routing suggestions available when manually reassigning (suggests best-fit reviewer based on check type + workload)

**17. Timeline/Audit**
Reassignment events logged in case audit trail (who reassigned, from whom, to whom, reason)

**18. Mobile Considerations**
Team lead may check on mobile. Mobile: simplified capacity cards per reviewer, one-tap reassign for urgent cases.

---

### 6.1.3 Page: Personal Productivity Dashboard

**1. Page Objective**
Allow individual reviewers to track their own performance trends and understand where they can improve — without needing to ask their team lead.

**2. Primary Actors** Ops Reviewer (self-service)

**3. Key Workflows**
Check daily/weekly metrics → Compare to team average → Identify check types taking longest → Review QC feedback received

**4. States**
Current period | Historical period selector

**5. Actions**
Change time period, drill into specific metric, view QC feedback details, export personal report

**6. Data Blocks**
Cases completed (today/week/month), avg handling time per check type, insufficiency rate (my cases vs team avg), QC error feedback, SLA compliance rate (my cases), discrepancy detection rate

**7. Cards**
- Cases Completed Card: Today / This week / This month with trend arrow
- Avg TAT Card: My average vs team average (color: green if better, amber if worse)
- QC Feedback Card: Errors flagged on my cases this week (link to error details)
- SLA Compliance Card: % of my cases completed within SLA

**8. Charts**
- Cases completed trend: Bar chart (daily, last 30 days)
- Avg TAT by check type: Horizontal bar
- Insufficiency rate trend: Line chart (weekly, last 12 weeks)
- QC error type breakdown: Pie chart

**9. Tables**
QC Feedback Table: Case ID | Check type | Error type | QC Reviewer note | Date | Resolved (Y/N)

**10. Drawers**
- QC Feedback Detail Drawer: Opens specific case where QC flagged error — shows original submission and QC notes side-by-side

**11. Modals** None

**12. Filters**
Time period (This week / This month / Last month / Custom range) | Check type

**13. SLA Components**
SLA compliance % (my cases) vs team average — visual comparison

**14. AI Components** None

**15. Mobile Considerations**
Mobile: KPI cards only, no charts. "View full analytics on desktop" prompt.

---

### 6.1.4 Page: Master Case Registry

**1. Page Objective**
Global case list across all clients and reviewers — for team leads, managers, and admins who need cross-team visibility. Primary ops search and filter interface.

**2. Primary Actors** Team Lead, Ops Manager, Senior Reviewer, Compliance Reviewer

**3. Key Workflows**
Search for a specific case → Filter by any combination of criteria → Bulk act on filtered set → Export for reporting → Access any case directly

**4. States**
Default view (all active cases, today) | Filtered | Search results | Bulk action mode

**5. Actions**
Search, filter, sort, open case, bulk assign, bulk escalate, bulk export, save filter preset, share filter URL

**6. Data Blocks**
All case fields: Case ID, candidate, client, package, country, check types, status, SLA, risk score, assigned reviewer, assigned vendor, created date, updated date, outcome color, AI flag presence, duplicate flag

**7. UI Regions**
- Top: Global search bar (spans full width)
- Filter panel (collapsible left sidebar): all filterable dimensions
- Saved filter presets bar (below search): quick-access user-saved filter sets
- Main table: paginated, sortable
- Bulk action toolbar (appears on selection)
- Export button (top right)

**8. Cards**
- Result summary strip: "Showing [N] cases matching your filters"
- Active filter chips: Each active filter shown as removable chip below search bar

**9. Tables**
Full case table: Case ID | Candidate | Client | Package | Country | Checks (count) | Status | SLA | Risk | Reviewer | Vendor | Created | Updated | Outcome | AI Flags | [Open]
- Sortable by every column
- Column selector (show/hide) — **includes client's custom fields (Searchable = Yes) as optional columns [C-08 | RFP 12.3]**
- Sticky header on scroll
- Row color: subtle red tint for SLA-breached, amber for at-risk

**10. Drawers**
- Quick Preview Drawer: Hover/click row for case summary without full navigation
- Filter Panel Drawer: Full advanced filter form (collapses to icon on narrow screen)
- Export Config Drawer: Choose columns, format (CSV/Excel), redaction level

**11. Modals**
- Save Filter Preset Modal: Name this filter set for quick reuse
- Bulk Assign Modal: Assign selected cases to reviewer/vendor
- Bulk Escalate Modal: Reason + target for all selected

**12. Tabs** None — filter-based navigation

**13. Filters**
Client (multi) | Package | Country | Check type | Status (multi) | SLA health | AI flag (present/absent) | Assigned reviewer | Assigned vendor | Date created (range) | Date updated (range) | Outcome color | Duplicate flag | **Custom fields — any Searchable custom field for the scoped client appears here as an additional filter dimension [C-08 | RFP 12.3]**

**14. Bulk Actions**
Assign to reviewer | Assign to vendor | Send candidate reminder | Mark for QC | Escalate | Export | Update status (admin only)

**15. Alerts/Banners**
- "Showing results from last 30 days. Expand date range to see older cases."
- "Cross-client search enabled — results include all tenants (Super Admin view)"

**16. SLA Components**
SLA column: live countdown with color. Filter by SLA health is primary use case for team leads doing morning triage.

**17. AI Components**
AI flags column: badge count of unreviewed AI flags per case. Filter: "Has AI flags = Yes" surfaces fraud-risk cases for senior reviewer attention.

**18. Evidence Components** None at list level

**19. Mobile Considerations**
Desktop-primary — dense table doesn't fit mobile well. Mobile: simplified card list, search only, no bulk actions.

---

### 6.1.5 Page: Insufficiency Management Queue

**1. Page Objective**
Manage all cases where candidate action is pending after insufficiency marking — track re-submission SLA, send reminders, escalate unresponsive candidates.

**2. Primary Actors** Ops Reviewer, Team Lead

**3. Key Workflows**
Review pending re-submissions → Send reminder to long-waiting candidates → Mark candidate as unresponsive (after threshold) → Resume case on re-submission → Escalate to client for their candidate's non-response

**4. States**
Awaiting re-submission | Re-submission received (pending ops review) | Unresponsive declared | Escalated to client

**5. Actions**
Send reminder, view remarks sent, review re-submission, mark unresponsive, escalate to client, resume case verification

**6. Data Blocks**
Case ID, candidate, client, fields marked insufficient (count + types), remarks sent, date insufficient marked, days waiting, re-submission status, SLA impact (days lost)

**7. UI Regions**
- Top: Summary strip — Awaiting count | Received (pending review) count | Unresponsive count | Avg wait days
- Filter bar
- Queue table
- "Overdue" section (cases waiting > configured threshold, highlighted)

**8. Cards**
- "Long Waiting" alert card: Cases waiting > 7 days without re-submission — require action
- "Re-submissions Received Today" card: Quick count, review now button

**9. Tables**
Queue table: Case ID | Candidate | Client | Fields insufficient (count) | Remarks preview | Date marked | Days waiting | Re-submission status | SLA paused (days) | Actions
- Color: Days waiting column turns amber > 5 days, red > 10 days

**10. Drawers**
- Remarks Drawer: Full field-level remarks sent to candidate (what exactly was requested)
- Re-submission Review Drawer: When re-submission received — show what candidate updated vs what was requested. Accept or reject re-submission.

**11. Modals**
- Send Reminder Modal: Channel selector + preview of reminder message + confirm
- Mark Unresponsive Modal: "Mark [candidate] as unresponsive? SLA will be closed as candidate-delayed. Client will be notified. This is reversible if candidate responds." + confirm
- Escalate to Client Modal: Notify client their candidate has not responded for [N] days — client to intervene

**12. Filters**
Client | Days waiting (range) | Re-submission status | Check type | SLA impact (days lost)

**13. Bulk Actions**
Bulk send reminder | Bulk mark unresponsive (requires confirmation) | Bulk export

**14. Alerts/Banners**
- "[N] candidates have not re-submitted for > 10 days — consider marking unresponsive" — amber
- "[N] re-submissions received today — review pending" — blue informational

**15. SLA Components**
SLA pause log per case: "SLA paused since [date] — [N] days lost." Days lost counter updates daily.

**16. AI Components** None direct on this queue

**17. Mobile Considerations**
Sending reminders possible on mobile. Review of re-submissions on desktop (document comparison).

---



---

## GAP-1 FIX: WhatsApp Deep-Link for Re-Submission

### Addition to 6.1.5 Insufficiency Management Queue + 6.1.29 Communication Interface

**WhatsApp Re-Submission Deep-Link — Design Specification**

When ops marks a case Insufficient and selects WhatsApp as a notification channel, the system generates two delivery paths:

**Path A — Standard Browser Link (Email/SMS fallback)**
Standard HTTPS link: `https://bgv.clientdomain.com/resubmit?token=[signed-token]`
Opens in device browser. Standard re-submission form (6.3.12).

**Path B — WhatsApp Deep-Link (WhatsApp primary channel)**
WhatsApp Business API message delivered with:
- Message body: specific insufficiency remarks + action button
- Action button type: `CTA_URL` with URL = `https://bgv.clientdomain.com/resubmit?token=[signed-token]&channel=whatsapp`

When candidate opens the link from WhatsApp on mobile:
- URL parameter `channel=whatsapp` triggers the WhatsApp-optimized mini-form render
- Mini-form is a web view that renders inside WhatsApp's in-app browser
- Mini-form shows ONLY the flagged fields (never the full form)
- Mini-form UI: simplified, single-column, large touch targets, no navigation header (stays in WhatsApp context)
- Document re-upload: triggers device camera directly (no file browser)
- On submission: in-WhatsApp confirmation: "Submitted ✓. KPMG will continue your verification."

**WhatsApp Fallback (older WhatsApp versions)**
If WhatsApp version does not support in-app browser web views:
- Link opens in device's default browser instead
- Same re-submission form (6.3.12) renders in browser
- No difference in functionality — only UX context changes
- System detects failure automatically via WhatsApp delivery receipt signals

**Ops Insufficiency Drawer — Channel Indicator Update**
Add to Insufficiency Drawer (6.1.1 and 6.1.5):
- Channel selector now shows: [Email] [SMS] [WhatsApp — In-App Form] [WhatsApp — Browser Link]
- Default: WhatsApp In-App Form (if candidate mobile number is WhatsApp-registered)
- System indicator: "WhatsApp registered: ✓ In-App Form available" or "WhatsApp not registered: Email/SMS only"
- Preview button: "Preview what candidate will see in WhatsApp" — renders mock WhatsApp conversation with mini-form link

**Insufficiency Field-Level Remarks in WhatsApp Message**
WhatsApp message body (configurable template):
```
Hi [Candidate First Name],

[Client Name] background verification needs your attention.

The following information needs to be updated:
• [Field 1 remark — e.g., "Please provide correct end date at ABC Corp"]
• [Field 2 remark — e.g., "Please re-upload PAN card — current image is blurry"]

Tap below to update (takes 2-3 minutes):
[Update Now →]

This link expires in 72 hours.
Need help? Reply to this message.
```

**Audit**
- Notification event logged: channel, delivery method (in-app-form vs browser-fallback), delivery status, candidate open event (if available via WhatsApp read receipts)

---
### 6.1.6 Page: Active Escalations Manager

**1. Page Objective**
Track all in-flight escalations (auto-triggered and manual) from creation to resolution — ensuring no escalation is forgotten or stale.

**2. Primary Actors** Team Lead, Senior Reviewer, Ops Manager

**3. Key Workflows**
Review new escalations → Assign owner → Investigate → Resolve → Close → Analyze escalation patterns

**4. States**
New (unacknowledged) | Assigned | Under Investigation | Resolved | Closed

**5. Actions**
Acknowledge escalation, assign owner, add investigation note, resolve (with outcome), close, reopen if resolution insufficient

**6. Data Blocks**
Escalation ID, case ID, escalation type, originating trigger (auto rule / manual), triggered by (user or system), escalated to, time in escalation, resolution notes, outcome

**7. UI Regions**
- Top: Escalation count by type (SLA / Fraud / Client / Legal / Vendor)
- Active escalations table (primary)
- Resolved escalations section (collapsible, last 7 days)
- Trend chart (bottom): escalations by type per week

**8. Cards**
- "Unacknowledged Escalations" card: Count with age of oldest — should always trend toward zero
- "Avg Resolution Time" card: This week vs last week

**9. Tables**
Escalation table: Escalation ID | Case ID | Type | Source (Auto/Manual) | Triggered by | Escalated to | Time in escalation | Status | [Actions]
- Color: Time in escalation turns amber > 4h, red > 8h

**10. Drawers**
- Escalation Detail Drawer: Full context — case summary, trigger rule (if auto), original reviewer notes, all investigation notes, resolution panel
- Resolution Drawer: Outcome text + resolution category (Resolved-Verified / Resolved-Escalated-Higher / Resolved-Client-Informed / Closed-False-Alarm) + confirm

**11. Modals**
- Reopen Escalation Modal: Reason for reopening (resolution was insufficient) + new assignee

**12. Filters**
Type | Status | Assignee | Source (Auto/Manual) | Date range | Client | SLA impact

**13. Bulk Actions**
Bulk assign | Bulk close (for resolved batch)

**14. Alerts/Banners**
- "[N] escalations unacknowledged for > 2 hours" — red urgent
- "New auto-escalation: SLA breach imminent for Case [X]" — toast

**15. SLA Components**
Escalation SLA (how long an escalation itself can remain open before it becomes a meta-escalation). Time-in-escalation column with color thresholds.

**16. AI Components**
Auto-escalation trigger log: shows which AI model or rule triggered the auto-escalation (e.g., "Predictive SLA model: 87% breach probability")

**17. Timeline/Audit**
All escalation events (trigger, acknowledgment, assignments, notes, resolution, closure) logged in both the escalation record and the parent case audit trail.

**18. Mobile Considerations**
Team leads need to acknowledge escalations on mobile (often urgent). Mobile: escalation card view, one-tap acknowledge, one-tap assign. Resolution on desktop.

---

### 6.1.7 Page: Cross-Case Search

**1. Page Objective**
Find any case, candidate, employer, or document across the entire system using any identifying data point.

**2. Primary Actors** Senior Reviewer, Compliance Reviewer, Team Lead, Super Admin

**3. Key Workflows**
Search by known identifier → Locate case → Navigate directly → Save search for repeat lookups

**4. States**
Empty (search prompt) | Searching | Results (grouped by entity type) | No results

**5. Actions**
Search, filter results by entity type, open result, save search, clear

**6. Data Blocks**
Search input, result entity type, result summary fields, match highlighted, relevance score

**7. UI Regions**
- Large search bar (centered, prominent)
- Entity type tabs below results: All | Cases | Candidates | Employers | Documents
- Results list (grouped + highlighted)
- Recent searches (below search bar, before first search)
- Saved searches (bookmarks)

**8. Cards**
- Result card per entity: Entity type label, key fields, match highlight, [Open] button
- "No results" card: Suggestions (check spelling, try partial match, try different identifier)

**9. Tables** Results in card format (not table — mixed entity types)

**10. Drawers**
- Saved Searches Drawer: All user-saved searches with labels and last-run date

**11. Modals**
- Save Search Modal: Name this search + frequency (run daily alert if new results)

**12. Filters**
Entity type (Cases / Candidates / Employers / Documents) | Date range (for cases) | Client (for cross-client admin search — Super Admin only)

**13. Search Scope**
- Case ID (exact)
- Candidate name (fuzzy)
- PAN hash (exact — never raw PAN in search)
- Email (exact or domain)
- Mobile (last 4 digits + full)
- Employer name (fuzzy)
- Requisition reference (exact)
- Document name (if indexed)
Cross-client search: Super Admin only. Standard ops sees only their tenant's cases.

**14. Alerts/Banners**
- "Cross-client search is active (Super Admin mode) — results include all tenants"
- "Showing top 50 results. Refine your search for more precise results."

**15. SLA/AI/Evidence Components** None at search level — all accessed after navigating to result

**16. Mobile Considerations**
Search on mobile is a common use case (reviewer looking up a case reference given verbally). Mobile: full search functionality, card results, quick open.

---

### 6.1.8 Page: Employment Check Workspace

**1. Page Objective**
Execute complete employment verification for one employment entry — from candidate-submitted data through EPFO cross-check, employer outreach, document review, AI signals, and final outcome declaration.

**2. Primary Actors** Ops Reviewer, Senior Reviewer

**3. Key Workflows**
Review candidate employment data → Pull EPFO/UAN record → Reconcile → Send employer outreach → Review employer response → Check documents (experience letter, payslip, offer letter) → AI fraud signals → Declare outcome

**4. States**
Not Started | In Progress — Verification | Pending Employer Response | Pending Vendor | Evidence Received | Outcome Declared | Completed | Discrepancy Found

**5. Actions**
Initiate EPFO pull, send employer outreach, review employer response, review documents, add note, mark insufficient, assign to vendor, flag discrepancy, declare outcome

**6. Data Blocks**
Candidate-submitted: company, designation, dates, location, HR contact, reason for leaving
EPFO pull: UAN history, employer names, dates, contribution records
Employer response: confirmed dates, designation, rehire status, confirmation method
Documents: offer letter, payslip, experience letter, relieving letter
AI signals: experience letter fraud flags, payslip authenticity, dual employment flag, gap analysis

**7. UI Regions**
- Top: Employer header (company name, claim period, check SLA countdown)
- Left panel: Sub-sections tabs (Candidate Data | EPFO | Employer Response | Documents | AI Signals | Outcome)
- Center: Active sub-section content
- Right: Notes + audit trail for this check

**8. Cards**
- EPFO Result Card: Match status (Full match / Partial / No record), key discrepancies highlighted
- Employer Outreach Status Card: Not sent / Sent [date] / Responded [date] / Overdue
- Dual Employment Card (conditional): Overlapping tenure detected — employer names + overlapping dates
- Employment Gap Card (conditional): Gap period, candidate's explanation (if provided)

**9. Tables**
- Tenure Reconciliation Table: 3 columns — Candidate Claimed | EPFO Record | Employer Confirmed — row per data field (start date, end date, designation, location). Discrepancy cells highlighted red.
- Document Table: Document name | **Format** | Type | Upload source | Date | AI quality | Fraud flag | **Actions**
  - Format: PDF / DOCX / XLSX / JPG / PNG / ZIP / ZIP-child
  - Actions: [View] for PDF/image; [View as PDF] [Download Original] for DOCX/XLSX; [View Extracted Files] [Download ZIP] for ZIP parent
  - Filter by format (dropdown): All / PDF / Word / Excel / Image / ZIP

**10. Drawers**
- EPFO Detail Drawer: Full UAN contribution history (all employers, all dates, PF amounts — ops reference)
- Employer Outreach Drawer: Send outreach — auto-populates candidate details in tokenized link, channel selector (email/WhatsApp), custom note to employer, send
- Employer Response Drawer: Structured response from employer (all confirmed fields side-by-side with claimed)
- Document Review Drawer: Full document viewer with OCR overlay and fraud detection overlay
- AI Signal Drawer: Experience letter fraud flags with evidence overlays and reason codes

**11. Modals**
- Outcome Declaration Modal: Verified / Minor Discrepancy / Major Discrepancy / Unable to Verify — mandatory notes for any non-Verified — evidence attach — confirm
- Mark Insufficient Modal: Which specific fields need correction + remarks + notification channel
- Discrepancy Flag Modal: Type + severity + description — added to case discrepancy register

**12. Tabs**
Candidate Data | EPFO/UAN | Employer Response | References | Documents | AI Signals | Outcome

**13. Filters**
Documents tab: filter by document type, fraud flag status

**14. Alerts/Banners**
- "EPFO record shows different employer name — tenure reconciliation required" — amber
- "Experience letter flagged by AI — manual review required" — red
- "Employer has not responded in [N] days — SLA at risk" — orange
- "Dual employment detected — overlapping with [Company X]" — red

**15. SLA Components**
Per-check SLA countdown (top right). Auto-escalation if employer not responded within configured window.

**16. AI Components**
- Dual employment detector result
- Employment gap analysis widget (timeline visual)
- Experience letter fraud detection (font analysis, metadata edit, template match)
- Payslip authenticity check
- ITR income cross-validation result
- Tenure diff AI suggestion: "Candidate claimed 3 years; UAN shows 1 year 8 months — 16-month discrepancy"

**17. Evidence Components**
- Document viewer with OCR overlay (side-by-side OCR extracted vs claimed)
- Fraud detection overlay on experience letters (highlighted anomaly regions)
- EPFO data panel (structured display of UAN pull — not a raw document)

**18. Mobile Considerations**
Desktop-only. Document review requires screen real estate for side-by-side comparison.

---



---


---

## GAP-EXP-FF1 FIX: Missing Explicit Fields — Ops Portal Verification Workspaces

### FF-1 | Rehire Eligibility Field — Employment Check Workspace

**RFP Reference:** RFP 4.11

**RFP Text:**
> *"Rehire eligibility tracking — Track employer's rehire status and supporting notes"*

**Verdict:** EXPLICIT

**Analysis:**
RFP 4.11 explicitly names rehire eligibility tracking as a required capability, including supporting notes. The Employment Check Workspace (6.1.8) does not include a structured, five-value rehire eligibility field. The employer confirmation received from the structured employer response form (Employer Response Module) must be mapped to a standardized rehire eligibility outcome in the ops workspace — this structured mapping is absent. A free-text "notes" field alone is insufficient; a structured five-value field enables consistent adjudication, reporting, and analytics.

**Impact:**
- Without a structured rehire eligibility field, adjudicators must interpret free-text employer notes to determine eligibility — inconsistent and error-prone.
- Rehire eligibility data cannot be included in analytics or filtered in case lists — a significant reporting gap for clients in regulated hiring sectors.
- "Not Eligible for Rehire" is one of the most consequential discrepancy findings — requiring structured capture, not free-text.

**Recommendation:**
Add to 6.1.8 Employment Check Workspace — Outcome Section:

**Addition to 6.1.8 Page: Employment Check Workspace — Rehire Eligibility Component:**

**Structured Rehire Eligibility Field (add to Item 6 — Data Blocks and Item 8 — Cards):**

```
REHIRE ELIGIBILITY (per employer — captured after employer response)
──────────────────────────────────────────────────────────────────────
Employer: [Company name]
Response source: ☑ Employer outreach ☐ UAN/EPFO ☐ Manual

Rehire Eligibility Status:
○ Eligible for Rehire
○ Not Eligible for Rehire  ← flags as discrepancy; mandatory reason
○ Eligible with Conditions   ← mandatory condition notes
○ Not Disclosed by Employer   ← employer declined to confirm
○ Source Unavailable   ← employer dissolved / unreachable

Mandatory notes (required for all statuses except "Eligible"):
[Text area — max 500 characters]

Reason Code (for "Not Eligible"):
○ Performance-related     ○ Conduct/disciplinary
○ Redundancy/restructuring  ○ Policy (employer policy, not candidate-specific)
○ Not specified by employer  ○ Other: [___]

Evidence (employer response document, where available):
[Document reference — linked from Evidence Store]
──────────────────────────────────────────────────────────────────────
```

**Impact on Adjudication:**
- "Not Eligible for Rehire" → auto-flags as Discrepancy (Major) in discrepancy register
- "Eligible with Conditions" → auto-flags as Discrepancy (Minor), requires adjudicator review
- All rehire statuses appear in the Employment Outcome Card summary
- Rehire status is a separate line in the BGV Report (visible to client per adjudication policy)

---

### FF-2 | Transcript Verification Result Fields — Education Check Workspace

**RFP Reference:** RFP 5.5

**RFP Text:**
> *"Transcript verification — Support transcript validation with integrity checks"*

**Verdict:** EXPLICIT

**Analysis:**
RFP 5.5 explicitly names transcript verification as a required capability with integrity checks. The Education Check Workspace (6.1.9) covers degree/certificate verification, DigiLocker, and institution recognition — but has no dedicated field block for transcript-specific data. Transcript verification is distinct from degree verification: it validates the full academic record (subjects, grades, attendance) rather than just the conferral of the degree. Dedicated fields for transcript validation (academic year, subjects listed, grade per subject, transcript issuing authority, seal/signature authenticity) are required for this capability.

**Impact:**
- Without transcript fields, ops reviewers capture transcript data in generic notes — preventing structured comparison between candidate-submitted transcript and university-confirmed record.
- Transcript integrity checks (detecting altered grades, missing subjects, forged seals) cannot be executed without a structured field definition.
- Clients in professional services, healthcare, and finance sectors often require transcript verification beyond degree certificate verification.

**Recommendation:**
Add to 6.1.9 Education Check Workspace — Transcript Verification section:

**Addition to 6.1.9 Page: Education Check Workspace — Transcript Verification Tab:**

Add "Transcript" tab to the existing Education Workspace (Tabs section, Item 12):

**Transcript Verification Tab Content:**

```
TRANSCRIPT VERIFICATION
══════════════════════════════════════════════════════════

CANDIDATE-SUBMITTED TRANSCRIPT
Document reference: [link to Document Store]
Issuing institution: [auto-filled from Education Form]
Academic year(s): [range]
Total subjects/papers listed: [count]
Overall grade / CGPA / Percentage: [extracted via OCR]

AI TRANSCRIPT INTEGRITY CHECK:
□ Seal/watermark authentic: ✅ / ⚠ Suspect / ❌ Flag
□ Font consistency: ✅ / ⚠ / ❌
□ Grade field tampering indicators: ✅ / ⚠ / ❌
□ Metadata consistency: ✅ / ⚠ / ❌

SUBJECT-LEVEL DATA (OCR-extracted, editable)
Subject                 | Marks | Grade | Notes
─────────────────────── | ───── | ───── | ──────────────────
[Subject 1 — OCR fill]  | [85]  | [A]   |
[Subject 2 — OCR fill]  | [72]  | [B+]  |
[+ Add subject manually]

UNIVERSITY CONFIRMATION (via University Response Module)
Transcript confirmed by: [University name + response date]
Confirmed subjects count: [N] / [N submitted] 
Grade match: ✅ Matches / ⚠ Discrepancy found
Discrepancy detail: [if any — which subject, claimed vs confirmed]

TRANSCRIPT VERIFICATION OUTCOME
○ Verified — transcript matches university records
○ Discrepancy — grade/subject difference (see notes)
○ Unable to Verify — university did not confirm transcript
○ Fraudulent — integrity check failed (see AI flags)

Mandatory notes: [____________]
══════════════════════════════════════════════════════════
```

**API Addition:**
- `POST /v1/education/transcript-verify` → triggers university outreach specifically for transcript data (separate from degree conferral outreach)
- Response includes: subjects_confirmed, grades_confirmed, discrepancies (array), authority_contact, confirmation_date


## GAP-29 FIX: Supervisor Identity Validation in Employment Workspace

### Addition to 6.1.8 Employment Check Workspace

**Supervisor Identity Validation Sub-Section**

Add to Employment Workspace (6.1.8) under the Employer Response section:

```
SUPERVISOR / REFEREE IDENTITY VALIDATION

Supervisor: [Name from candidate form]
Contact: [Email / Mobile from candidate form]

Corporate email domain check:
  Email domain: @[company].com
  Known corporate domain: ✅ Confirmed (matches employer name)
  OR ❌ Domain registered < 6 months ago — suspicious
  OR ⚠️ Free email domain (gmail/yahoo) — cannot confirm corporate identity

LinkedIn verification (optional, non-blocking):
  [Search LinkedIn] button → opens LinkedIn search in new tab with pre-filled supervisor name + company
  Ops reviewer marks: ✅ Profile found and matches | ⚠️ Profile found — role/company mismatch | 
                       ❌ No profile found | — Not checked
  
Phone number check:
  [N] digit number — Country format: ✅ Valid Indian mobile
  Known VOIP/virtual number: ⚠️ May be temporary number
  
Overall supervisor credibility: [High / Medium / Low / Not Verified]
Credibility rationale (mandatory if Low or Not Verified): ____________________
```

**Reviewer Guidance**
"Supervisor identity validation is informational — a low credibility score does not automatically flag the check. Consider when: (1) Employer email is generic/free domain, (2) Response content is unusually brief, (3) Dates confirmed conflict with EPFO without explanation."

**Reference Check Extension**
Same supervisor identity validation block added to Reference Check Workspace (6.1.14) for referee identity validation.


---


---

## GAP FILLS — P2 ENHANCEMENTS


---
### 6.1.9 Page: Education Check Workspace

**1. Page Objective**
Execute complete education verification — from candidate-submitted academic history through DigiLocker fetch, institution recognition, degree fraud detection, and university outreach to final outcome.

**2. Primary Actors** Ops Reviewer, Senior Reviewer

**3. Key Workflows**
Review candidate education data → Fetch DigiLocker certificate (if available) → Check institution accreditation → Review degree certificate for fraud → Send university outreach → Review university response → Declare outcome

**4. States**
Not Started | DigiLocker Fetch Pending | Institution Check In Progress | Pending University Response | Evidence Reviewed | Outcome Declared | Discrepancy Found

**5. Actions**
Trigger DigiLocker fetch, check institution recognition, send university outreach, review documents, flag discrepancy, declare outcome, mark insufficient, assign to vendor

**6. Data Blocks**
Candidate-submitted: degree, institution, board/university, year, percentage/CGPA, course
DigiLocker result: fetched certificate details (if available), match vs claimed
Institution check: UGC/AICTE recognition status, fake university database result
Degree document: uploaded certificate, AI authenticity result
University response: enrollment confirmed, degree conferred, year, percentage
Name change: affidavit (if applicable)

**7. UI Regions**
Same 3-panel structure as Employment workspace — tabs differ per sub-section

**8. Cards**
- DigiLocker Result Card: Fetched (match/mismatch/not available) — comparison fields highlighted
- Institution Recognition Card: Recognized (UGC/AICTE/State) / Unrecognized / Fake university flagged
- Degree Fraud Detection Card: AI confidence badge — Authentic / Suspicious / Flagged
- University Outreach Card: Status + response date

**9. Tables**
- Education Data Reconciliation Table: Candidate Claimed | DigiLocker | University Confirmed — per field (degree, year, percentage, enrollment no.)
- Document Table: Document name | **Format** | Type | Upload source | Date | AI quality | Fraud flag | **Actions** (same structure and format-specific actions as 6.1.8 Employment — PDF/DOCX/XLSX/JPG/PNG/ZIP, per platform policy 4.7.5)

**10. Drawers**
- DigiLocker Fetch Drawer: Trigger fetch, show raw fetched data, comparison diff
- Institution Lookup Drawer: Search UGC/AICTE database, show recognition details, fake university hit (if any)
- University Outreach Drawer: Send outreach (tokenized link to university response module)
- Document Review Drawer: Degree certificate viewer with fraud detection overlays
- AI Signal Drawer: Fraud flag reason codes — font inconsistency evidence, metadata edit indicator, template match score

**11. Modals**
- Outcome Declaration Modal: Same structure as employment — Verified / Discrepancy / Unable to Verify
- Duplicate Certificate Modal: "This roll number has appeared in another case. Potential duplicate certificate fraud. Flag for investigation?"
- Name Change Review Modal: Affidavit review — accept (name change valid) or reject (insufficient evidence)

**12. Tabs**
Candidate Data | DigiLocker | Institution Check | University Response | Documents | AI Signals | Outcome

**13. Alerts/Banners**
- "Institution not recognized by UGC/AICTE — manual investigation required" — red
- "AI detected potential certificate fraud — manual review required" — red
- "DigiLocker certificate available and matches candidate data — no manual university outreach needed" — green (expedites workflow)
- "Course duration inconsistency — 4-year degree completed in 1 year 8 months per claimed dates" — amber

**14. AI Components**
- Degree certificate fraud detection (font analysis, metadata, print-scan artifacts)
- Institution fake university database match
- Course duration validator (deterministic rule + AI edge-case handling)
- Duplicate certificate detector (roll number hash matching across cases)
- OCR extraction with education-specific field extraction (degree name, year, percentage, institution name)

**15. Evidence Components**
- Certificate viewer with fraud overlay
- DigiLocker fetched certificate display (government-verified — shown with "Government Verified" badge)
- Side-by-side: uploaded certificate vs DigiLocker certificate (if both available)

**16. Mobile Considerations** Desktop-only for same reasons as employment.

---

### 6.1.10 Page: KYC Verification Workspace

**1. Page Objective**
Execute complete identity verification — government ID validation, biometric review, cross-document consistency check, fraud detection — all in one workspace.

**2. Primary Actors** Ops Reviewer, Senior Reviewer (for AI flag overrides)

**3. Key Workflows**
Review submitted IDs → Run API validations (Aadhaar/PAN/Passport/DL) → Review OCR extraction vs declared → Review biometric result → Check cross-document consistency → Review device/geo risk → Declare outcome

**4. States**
Not Started | API Validation In Progress | Biometric Review Pending | Manual Review (flagged) | Outcome Declared

**5. Actions**
Trigger ID API validation, review OCR comparison, review biometric result, override AI flag (senior role), flag discrepancy, declare outcome, mark insufficient

**6. Data Blocks**
Per ID document: type, API validation result, OCR extracted fields, fraud detection flags
Biometric: face match score category, liveness result, attempt count, deepfake flag
Cross-document: DOB match, name match, address consistency
Device/geo: device type, IP geolocation, VPN flag, distance from declared address

**7. UI Regions**
- Document gallery panel (left): Thumbnails of all submitted ID documents, click to make active
- Center: Active document — full viewer with API result + OCR overlay
- Right: Biometric panel + cross-document consistency + device risk

**8. Cards**
- Per-ID Validation Card: Document type + API result badge (Verified/Failed/API Unavailable) + key discrepancies
- Face Match Card: Two-pane (selfie face vs ID face), match score category (High/Medium/Low/Failed), liveness badge
- Cross-Document Consistency Card: DOB match across all docs, name match, address consistency — green/red per check
- Device Risk Card: IP country, VPN detected (Y/N), geo-distance from declared address, risk score category

**9. Tables**
- OCR Comparison Table: Field | OCR Extracted Value | Candidate-Entered Value | Match (Y/N) — highlighted mismatches
- Document Inventory Table: Type | Uploaded | API validation | Fraud flag | Quality score | [View]

**10. Drawers**
- Document Viewer Drawer: Full-screen document + OCR overlay (boxes + confidence) + fraud overlay (anomaly highlights)
- API Result Detail Drawer: Raw API response fields (DOB, name, address from government DB) — for reference only (not shown to candidate)
- Biometric Detail Drawer: Face match — selfie vs ID side-by-side, match score, liveness challenge steps passed, attempt history, deepfake signal details
- Device Risk Detail Drawer: Full device fingerprint analysis, IP geolocation map, VPN/proxy detection method

**11. Modals**
- AI Override Modal (Senior Reviewer only): "You are overriding an AI fraud flag. Reason is mandatory and will be permanently logged." Reason text field + [Confirm Override]
- Outcome Declaration Modal: Clear / Identity Mismatch / Document Fraud Suspected / Unable to Verify — mandatory notes for all non-Clear

**12. Tabs**
Documents | Biometric | Cross-Document Check | Device & Geo Risk | AI Signals | Outcome

**13. Filters**
Documents tab: filter by document type, fraud flag, API status

**14. Alerts/Banners**
- "Deepfake detection flag — senior reviewer required for override" — red
- "Name mismatch between PAN and Aadhaar — discrepancy flag" — amber
- "VPN/proxy detected during candidate submission — elevated fraud risk" — amber
- "Face match below threshold — manual biometric review required" — red
- "Biometric consent not captured — cannot process biometric data" — red blocker

**15. AI Components**
- Face match: categorical result displayed, not raw score
- Liveness: passed/failed per challenge step
- Deepfake: flag + reason codes (texture analysis, frequency domain anomaly, reflection inconsistency)
- OCR: per-field extraction with confidence per field
- Document fraud: per-document authenticity result with overlays
- Cross-document consistency: rule-based matching across all ID documents
- Device risk: composite score from device type + IP + geo + behavioral signals

**16. Evidence Components**
- Document viewer with dual overlay modes (OCR / Fraud detection — toggle)
- Biometric comparison pane (face crop from selfie vs face crop from ID — privacy: rest of image blurred)
- GPS evidence (if address check requested — shows map with IP location vs declared address)

**17. Mobile Considerations** Desktop-only. Evidence comparison requires screen space.

---

### 6.1.11 Page: Legal / Criminal Check Workspace

**1. Page Objective**
Execute court record searches, sanctions/PEP screening, and regulatory database checks — with identity resolution to avoid false positives — and declare a defensible adjudicated outcome.

**2. Primary Actors** Ops Reviewer, Senior Reviewer, Risk/Legal Reviewer

**3. Key Workflows**
Configure search scope → Execute court searches → Execute sanctions/PEP → Resolve identity (confirm same person) → Interpret case status → Apply adjudication matrix → Declare outcome

**4. States**
Not Started | Search In Progress | Results Returned — No Hit | Results Returned — Hit Found | Identity Resolution Required | Adjudication Pending | Outcome Declared

**5. Actions**
Configure search scope (which courts, which databases), trigger search, review results, confirm identity match, interpret case status, apply adjudication matrix, declare outcome, escalate to Risk/Legal

**6. Data Blocks**
Search scope: court list, database list
Court results: case number, type, petitioner, respondent, status, date
Sanctions results: list name, match type, confidence
Identity resolution: match criteria used (name, DOB, address, photo)
Adjudication matrix: role-specific policy guidance for each case type

**7. UI Regions**
- Left: Search scope configuration panel (which courts searched — checklist with status)
- Center: Results panel (court results + sanctions results — tabbed)
- Right: Identity resolution panel + adjudication matrix guidance

**8. Cards**
- Search Scope Coverage Card: "N courts searched, M courts not yet returned." Coverage indicator.
- Sanctions/PEP Result Card: No match (green) / Match found (red) / Potential match — manual review (amber)
- Identity Resolution Card: When hit found — match criteria confirmation (name ✓, DOB ✓, address ?)
- Adjudication Matrix Card: For this role + this case type → recommended action (Cleared / Minor Concern / Major Concern / Disqualifying)

**9. Tables**
- Court Results Table: Source court | Case number | Case type | Petitioner | Respondent | Status (Disposed/Pending/Convicted) | Date of judgment | Identity match confidence
- Sanctions Table: List name | Entry type (Individual/Entity) | Match type (Exact/Fuzzy) | Match score | Review required (Y/N)
- Regulatory Results Table: Authority (SEBI/SFIO/RBI/ED) | Proceeding type | Status | Date

**10. Drawers**
- Court Record Detail Drawer: Full case record details (case history, judge, orders, final outcome where available)
- Identity Resolution Drawer: Side-by-side — court record identity fields vs candidate identity fields — ops marks each as Match/No Match/Unable to Confirm
- Sanctions Detail Drawer: Full watchlist entry details — designation, nationality, DOB, address, reason for listing
- Adjudication Matrix Drawer: Full policy matrix for this role type — all case type + severity combinations with recommended actions

**11. Modals**
- Escalate to Risk/Legal Modal: Send case to Risk/Legal reviewer for decision on ambiguous hits — reason + note
- Outcome Declaration Modal: Clear (No adverse record) / Adverse — Minor / Adverse — Major / Unable to Verify — mandatory notes for any adverse outcome + evidence attach
- False Positive Confirmation Modal: "You are marking this court hit as a false positive (different person). Reason and identity resolution evidence are mandatory." Audit-logged permanently.

**12. Tabs**
Court Records | Sanctions & PEP | Regulatory | Identity Resolution | Adjudication Matrix | Outcome

**13. Alerts/Banners**
- "Court hit found — identity resolution required before outcome can be declared" — amber (blocking)
- "Sanctions list match detected — escalation to Risk/Legal required" — red (blocking for senior review)
- "Regulatory proceeding found (SEBI/RBI) — specific client policy applies" — amber
- "All searches returned — no adverse records found" — green

**14. SLA Components**
Legal check SLA is typically longest — countdown prominent. Auto-escalation if identity resolution pending > configured hours.

**15. AI Components**
- Identity disambiguation model: confidence score for "same person" determination based on name + DOB + address + photo similarity
- Court record summarizer: AI-generated plain-language summary of case type and likely implications

**16. Evidence Components**
- Court record viewer (where digital records available — structured display)
- Sanctions entry viewer (full entry with source list citation)
- Identity evidence comparison pane (candidate ID documents vs court record identity fields)

---

### 6.1.12 Page: Address Verification Workspace

**1. Page Objective**
Execute address verification through digital validation, field agent GPS evidence review, and remote video — reconciling declared vs verified address.

**2. Primary Actors** Ops Reviewer, Field Agent (submits evidence independently via app)

**3. Key Workflows**
Attempt digital verification → If insufficient: assign field agent → Review GPS evidence → Review photos + checklist → Reconcile declared vs verified → Declare outcome

**4. States**
Not Started | Digital Verification In Progress | Field Visit Assigned | Evidence Submitted | Evidence Under Review | Remote Video Scheduled | Outcome Declared

**5. Actions**
Trigger digital verification, assign field agent, review GPS evidence, review photos, review checklist, verify or dispute photo authenticity, schedule remote video, declare outcome

**6. Data Blocks**
Declared address (candidate-submitted), digital verification result (geo-coordinates, utility DB), field visit: GPS capture, photos (with embedded GPS+timestamp), checklist responses, neighbor notes, outcome. Remote video: session record.

**7. UI Regions**
- Top: Address display (candidate-declared + verified address if different)
- Left: Verification method tabs (Digital | Field Visit | Remote Video)
- Center: Active method workspace
- Right: Reconciliation panel (declared vs verified comparison)

**8. Cards**
- Digital Verification Card: Geo-coordinate match (map thumbnail + distance from declared), utility DB result
- Field Visit Status Card: Assigned / Acknowledged / In Transit / Evidence Submitted / Completed
- GPS Evidence Card: Coordinates, accuracy radius, distance from declared address, timestamp
- Photo Authenticity Card: AI result — Authentic / Suspicious / Flagged (GPS mismatch / photo spoof detected)
- Reconciliation Card: Declared address vs GPS-verified address — match / partial match / mismatch

**9. Tables**
- Photo Evidence Table: Photo number | Captured at (GPS) | Timestamp | Distance from declared | Authenticity flag | [View]
- Checklist Responses Table: Question | Response | Notes

**10. Drawers**
- Digital Verification Detail Drawer: Full geo-coordinate analysis, postal database lookup, utility/telecom DB result
- Field Agent Assignment Drawer: Agent pool filtered by geography, assign + SLA commitment, assignment confirmation
- GPS Evidence Map Drawer: Interactive map — pin at GPS capture location + pin at declared address + distance line. Photo markers clickable to open photo.
- Photo Viewer Drawer: Full-size photo + embedded GPS/timestamp metadata display + AI authenticity overlay (flagged regions highlighted)
- Neighbor Verification Drawer: Agent's neighbor notes, neighbor relationship, statement recorded
- Remote Video Drawer: Schedule session (calendar picker), candidate notification trigger, session recording (if policy allows)

**11. Modals**
- GPS Anomaly Review Modal: "GPS capture location is [N]km from declared address. Possible reasons: [agent moved, address incorrect, GPS error]. Review photos and confirm outcome."
- Photo Authenticity Override Modal: "AI flagged this photo as potentially inauthentic. Override requires senior reviewer + mandatory note."
- Outcome Declaration Modal: Address Confirmed / Address Confirmed with Discrepancy / Address Not Confirmed / Unable to Verify — mandatory notes for non-Confirmed

**12. Tabs**
Digital Verification | Field Visit | Remote Video | Address Reconciliation | Outcome

**13. Alerts/Banners**
- "GPS capture location is 1.2km from declared address — manual review required" — amber
- "Photo authenticity flag — AI detected potential GPS spoofing" — red
- "Field visit overdue — agent has not submitted evidence within SLA" — orange
- "Digital verification inconclusive — field visit recommended" — informational blue

**14. AI Components**
- Photo GPS cross-validation: EXIF coordinates vs agent GPS at capture time vs declared address
- Moiré/screen-capture photo detection
- Teleportation detection (agent GPS history — cannot move 50km in 5 minutes)
- Image quality assessment (blur, darkness, partial content)

**15. Evidence Components**
- Interactive GPS map with evidence pins
- Photo gallery with GPS metadata overlay
- Side-by-side: declared address vs GPS-verified address (geocoded both, shown on same map)
- Video session recording player (if remote video captured)

---



---

## GAP-3 FIX: Site Visit as Standalone Component

### New Page: 6.1.39 Site Visit Management

**1. Page Objective**
Manage site visits as a standalone verification sub-component with an independent 12-state machine, independent three-track SLA, field agent assignment engine, supervisor QC layer, and GPS evidence management — separate from the address check workflow.

**2. Primary Actors**
Ops Reviewer (assigns), Field Agent (executes via app), Vendor Supervisor (QC), QC Reviewer (second-level)

**3. Key Workflows**
Create site visit → Assign field agent → Agent acknowledges → GPS Check-In → Evidence capture → GPS Check-Out → Supervisor QC → Ops review → Outcome declaration

**4. States (12 States — Independent State Machine)**

| State | Description | Actor |
|---|---|---|
| Not Assigned | Site visit check created — no agent assigned | System |
| Scheduled | Visit date/time set, agent identified | Ops Reviewer |
| Agent Assigned | Specific agent confirmed and notified | System/Ops |
| GPS Check-In | Agent checked in at location — GPS + timestamp recorded | Field Agent |
| Evidence Capture | Agent capturing photos, checklist, notes | Field Agent |
| GPS Check-Out | Agent completed visit — GPS + timestamp recorded | Field Agent |
| Supervisor QC | Vendor supervisor reviewing agent submission | Vendor Supervisor |
| Sent Back to Agent | Supervisor rejected — agent must re-capture | Vendor Supervisor |
| Submitted | Supervisor approved — in ops review queue | System |
| Verified — Clear | Address confirmed by physical visit | Ops Reviewer |
| Discrepancy Found | Physical visit conflicts with declared address | Ops Reviewer |
| Unable to Verify | Inaccessible / candidate uncontactable after 2 attempts | Ops Reviewer |
| Cancelled | Client cancelled or candidate withdrew | Client/Ops |

**5. Actions**
Create site visit, assign agent (AI-suggested or manual), reschedule, view GPS evidence, review photos, review supervisor QC notes, override photo authenticity flag, declare outcome, cancel

**6. Data Blocks**
Site visit ID, parent case ID and check ID, candidate address, assigned agent, agent GPS check-in/out records, photos (with embedded GPS + timestamps), structured checklist responses, neighbor verification notes, supervisor QC result, outcome, three-track SLA timers

**7. UI Regions**
- Top: Site visit header (visit ID, candidate address, state badge, three-track SLA display)
- Left panel: State machine progress tracker (12 states as vertical stepper)
- Center: Current state workspace (content changes per state)
- Right: GPS evidence map + photo gallery + supervisor QC notes

**8. Three-Track SLA Display**
Site visit has its own three-track SLA (separate from parent case):
```
Client SLA: [countdown] — 7 days from assignment
Internal SLA: [countdown] — 5 days from assignment  
Vendor SLA: [countdown] — 3 days from assignment
```
Color-coded per track independently. Each track can breach independently.

**9. Cards**
- State Progress Card: Visual 12-step stepper with current state highlighted, completed states in green, future states in grey
- GPS Accuracy Card: "Agent GPS accuracy at Check-In: ±8m (Good) / ±45m (Fair) / GPS unavailable (Poor)"
- Distance Card: "Agent check-in location is [Xm] from declared address" — green <100m, amber 100-500m, red >500m
- Supervisor QC Card: QC status + any error flags from supervisor review

**10. Tables**
- Photo Evidence Table: Photo # | Capture GPS | Timestamp | Distance from declared address | AI authenticity result | [View]
- Checklist Responses Table: Question | Response | Notes
- Agent Attempt Log (for Unable to Verify): Attempt # | Date | Outcome | Notes

**11. Drawers**
- Agent Assignment Drawer: Agent pool filtered by geography (pin code → district → state expansion). Per agent: coverage area, current queue depth, historical TAT for site visits, QC pass rate. AI-suggested agent highlighted. Manual override available. Assignment confirmation → auto-notifies agent via Field Agent App + SMS.
- GPS Evidence Map Drawer: Interactive map — declared address pin + agent check-in pin + agent check-out pin + photo capture pins. Distance lines shown. Photo thumbnails clickable at each capture location.
- Photo Viewer Drawer: Full-size photo + embedded GPS metadata + AI authenticity overlay. Authenticity flags shown with region highlights (if any).
- Supervisor QC Review Drawer (Vendor Supervisor): Evidence package review — all photos, checklist, notes. [Approve] [Reject — specify error tags]. Error tags: Insufficient Photos / GPS Mismatch / Checklist Incomplete / Photo Authenticity Flag / Unclear Evidence.
- Outcome Declaration Drawer: Outcome selector + mandatory notes for non-Clear + evidence attach.

**12. Modals**
- Create Site Visit Modal: Triggered from address check workspace when digital verification is inconclusive. Pre-fills candidate address. Package type selector (standard / enhanced with neighbor verification). SLA tier selector. [Create Site Visit] — generates site visit ID linked to parent case.
- Cancel Site Visit Modal: Reason (client requested / candidate withdrew / address verified digitally) + confirm. Cancellation logged in parent case audit.
- GPS Anomaly Override Modal: "Agent check-in is [Xm] from declared address. This exceeds the 500m threshold. Override requires Supervisor QC confirmation. Proceed?" [Override — requires Supervisor QC] [Cancel].
- Photo Authenticity Override Modal: "AI flagged this photo as potentially inauthentic. Override requires Senior Reviewer + mandatory note." (Same as Case Workbench AI override pattern.)

**13. Filters**
State | Agent | Geography | SLA health | Client | Date range

**14. Bulk Actions**
Bulk assign agent (for batch site visit assignments to same geography) | Bulk export | Bulk escalate overdue

**15. Alerts/Banners**
- "Agent has not acknowledged assignment for > 4 hours — auto-reassignment triggered" — amber
- "GPS Check-Out not recorded — visit marked as in-progress for > 4 hours" — amber
- "Photo authenticity flag — Supervisor QC required before this can proceed" — red
- "Vendor SLA breached — visit not completed within 3 days. Client SLA at risk." — red
- "Site visit cancelled by client — [reason]. Parent case address check updated to 'Unable to Verify'." — informational

**16. SLA Components**
Three-track SLA timers per site visit (independent of parent case SLA). Auto-escalation at 75% and 100% of each track. SLA pause on: client hold, agent on-hold, force majeure. Vendor SLA breach logged to vendor scorecard.

**17. AI Components**
- Photo authenticity check (runs automatically after agent submission, before Supervisor QC): GPS cross-validation, EXIF metadata check, moiré/screen-capture detection, duplicate photo hash check, tamper detection
- AI-suggested agent: "Best match: Agent [X] — covers this pin code, current queue: 3 visits, 94% on-time rate, 98% QC pass rate"

**18. Evidence Components**
GPS map with evidence pins. Photo gallery with metadata overlay. Neighbor verification notes viewer. Supervisor QC decision with error tag history.

**19. Mobile Considerations**
Site Visit Management is ops desktop page. Field agent captures evidence via Field Agent App (6.6.1) separately. Ops reviewers on mobile can: view GPS evidence map, approve/reject supervisor QC outcomes, view photo gallery.

**20. Part 5 IA Addition**
Add to Operations Portal IA (Part 5.1) under Verification Execution:
```
├── 3.8 Site Visit Management (Standalone Sub-Component)
│   └── Page: Site Visit Management
│       Purpose: Manage physical address verification as independent component with 
│                own state machine, SLA, agent assignment, and supervisor QC
│       States: Not Assigned → Scheduled → Agent Assigned → GPS Check-In → 
│               Evidence Capture → GPS Check-Out → Supervisor QC → 
│               Sent Back to Agent → Submitted → Verified/Discrepancy/Unable/Cancelled
│       SLA Tracks: Client (7d) | Internal (5d) | Vendor (3d) — all independent
```

---
### 6.1.13 Page: Financial Check Workspace

**1. Page Objective**
Execute financial background checks (credit, insolvency, AML) with strict permissible-purpose enforcement — ensuring checks are only run when legal basis confirmed.

**2. Primary Actors** Ops Reviewer, Senior Reviewer

**3. Key Workflows**
Confirm permissible purpose + consent → Trigger credit bureau check → Check insolvency databases → AML screening → Declare outcome

**4. States**
Not Started | Consent Verified | Check In Progress | Results Received | Outcome Declared

**5. Actions**
Verify consent, trigger credit check, trigger insolvency check, trigger AML check, review results, declare outcome

**6. Data Blocks**
Consent record reference (financial-specific consent), credit bureau result, insolvency/bankruptcy result, AML screening result, purpose limitation documentation

**7. UI Regions**
- Top: Purpose limitation banner (always visible — shows the legal basis for this financial check)
- Consent verification panel (must confirm before any check can be triggered)
- Check result panels (one per check type)
- Outcome section

**8. Cards**
- Consent Validity Card: Financial check consent — valid (green) / missing (red — check blocked)
- Permissible Purpose Card: Shows stated purpose for financial check (role type + client confirmation)
- Credit Bureau Result Card: Score range indicator, adverse markers count, summary
- Insolvency Result Card: No record / Record found (with details)
- AML Result Card: No flag / Flag found + severity

**9. Tables**
- Adverse Credit Markers Table: Marker type | Date | Amount | Status (active/settled)
- Insolvency Records Table: Authority | Proceeding type | Date filed | Status

**10. Drawers**
- Consent Detail Drawer: Full financial consent record — text, signature, timestamp
- Credit Bureau Detail Drawer: Full credit report (ops view — structured, not raw bureau format)
- Insolvency Proceeding Drawer: MCA/DRT/NCLT record details
- AML Detail Drawer: AML flag details, transaction pattern summary

**11. Modals**
- Consent Missing Modal: "Financial check consent not captured — this check cannot proceed. Options: [Request consent from candidate] [Skip financial check] [Escalate to client]"
- Outcome Declaration Modal: Clear / Adverse Finding / Unable to Verify — mandatory notes for adverse

**12. Alerts/Banners**
- "Financial check consent not captured — check is blocked" — red blocker banner
- "Credit bureau result: adverse markers found — senior review required" — red
- "AML flag detected — escalation to Risk/Legal required" — red

**13. AI Components** AML pattern detection (where applicable)

**14. Compliance Notes**
Purpose limitation panel is non-dismissible — always visible. Financial data is the most legally sensitive check type. Every access to financial data is logged with purpose justification.

---

### 6.1.14 Page: Reference Check Workspace

**1. Page Objective**
Manage professional reference verification — outreach to referee, structured questionnaire response review, credibility check of the referee themselves.

**2. Primary Actors** Ops Reviewer

**3. Key Workflows**
Review referee contacts → Send outreach (tokenized link) → Track response → Review questionnaire responses → Check referee credibility → Declare outcome

**4. States**
Not Started | Outreach Sent | Response Received | Credibility Check | Outcome Declared | Referee Unresponsive

**5. Actions**
Send referee outreach, send reminder, review response, check referee's own employment (credibility), declare outcome, mark unresponsive

**6. Data Blocks**
Referee details (from candidate), outreach status, questionnaire responses (structured), referee credibility check result, outcome

**7. Cards**
- Referee Status Cards (one per referee): Name, relationship, outreach status, response status
- Questionnaire Response Card: Key ratings + highlights from referee response
- Referee Credibility Card: Was referee's own employment at candidate's company verified?

**8. Tables**
- Referee Table: Name | Relationship | Contact | Outreach status | Response status | Response date
- Questionnaire Response Table: Question | Response | Rating (if scale question)

**9. Drawers**
- Send Outreach Drawer: Referee selector + tokenized link generation + channel (email/WhatsApp) + custom message
- Response Review Drawer: Full structured questionnaire response — all questions and answers, rating scales shown visually, free-text responses displayed
- Credibility Check Drawer: Cross-reference referee's own claimed employment with candidate's employment (were they actually at the company at the same time?)

**10. Modals**
- Mark Unresponsive Modal: After N attempts — "Mark [referee] as unresponsive. Outcome will reflect inability to obtain reference."
- Outcome Declaration Modal: Positive Reference / Neutral Reference / Adverse Reference / Unable to Obtain

---

### 6.1.15 Page: Adjudication Queue

**1. Page Objective**
Central queue of all cases where verification is complete and final adjudication decision is pending. Enables adjudicators to prioritize by SLA, risk, and discrepancy severity.

**2. Primary Actors** Adjudicator, Senior Reviewer

**3. Key Workflows**
View queue → Sort by urgency → Open case → Complete adjudication → Return to queue

**4. States**
Awaiting Adjudicator | Assigned to Adjudicator | In Progress | Completed

**5. Actions**
Assign to self, assign to another adjudicator, open for adjudication, filter, sort

**6. Data Blocks**
Case ID, candidate, client, checks complete (count), discrepancy count by severity, AI risk score, SLA to report delivery deadline, assigned adjudicator, AI reviewer assist summary (preview)

**7. UI Regions**
- Top: Queue summary — Total pending | High-risk pending | SLA-critical pending
- Priority sort toggle: SLA urgency / Risk score / Discrepancy severity
- Queue table
- Escalated section (separate from standard queue — always top of page)

**8. Cards**
- AI Reviewer Assist Preview Card (per row, expandable): "Key discrepancies: [list]. Suggested outcome: [X]." Saves adjudicator time.
- "Escalated Cases" section card: Cases that escalated to adjudication level

**9. Tables**
Queue table: Case ID | Candidate | Client | Checks | Discrepancies (by severity) | AI Risk | SLA to delivery | Adjudicator | [Assign to Me] [Open]

**10. Filters**
Client | SLA urgency | Risk score | Discrepancy severity | Adjudicator (unassigned / mine / all)

**11. Bulk Actions**
Bulk assign to adjudicator

**12. Alerts/Banners**
- "[N] adjudication cases have SLA to delivery < 4 hours" — red
- "New escalated case requires senior adjudicator" — urgent notification

---

### 6.1.16 Page: Adjudication Workbench

**1. Page Objective**
Complete final adjudication decision interface — full case review, AI summary, discrepancy resolution, outcome declaration, pre-adverse/adverse notice, report trigger.

**2. Primary Actors** Adjudicator

**3. Key Workflows**
Review all check outcomes → Review AI summary → Review discrepancy register → Set outcome → Add notes → Attach evidence → Trigger pre-adverse if needed → Generate report

**4. States**
Under Review | Pre-Adverse Issued (waiting period active) | Decision Made | Report Triggered | Completed

**5. Actions**
Review case, set outcome, add notes, attach evidence, request waiver, issue pre-adverse notice, confirm adverse after waiting period, trigger report generation

**6. Data Blocks**
All check outcomes (summary), AI reviewer assist summary, discrepancy register (all discrepancies with severity), waiver requests, pre-adverse/adverse notice status, report template options

**7. UI Regions**
- Left: Check outcome summary list (all checks at a glance)
- Center: AI adjudication summary + discrepancy table + outcome declaration section
- Right: Evidence attach + audit trail

**8. Cards**
- AI Reviewer Assist Card: Full AI-generated summary — findings, discrepancy list, risk factors, suggested outcome
- Discrepancy Summary Card: All discrepancies with type, source check, severity, resolution status
- Pre-Adverse Status Card (conditional): If outcome is adverse — notice status, waiting period countdown, candidate notification delivery

**9. Tables**
- Check Outcomes Table: Check type | Outcome | Discrepancy (Y/N) | Severity | Notes
- Discrepancy Table: ID | Type | Source | Severity | Status | Recommended action
- Waiver Table: Discrepancy | Waiver reason | Waiver status | Approved by

**10. Drawers**
- Check Detail Drawer: Drill into any check outcome for full context without leaving adjudication workbench
- Pre-Adverse Notice Drawer: Notice text preview (auto-populated with findings), candidate contact details, send/schedule
- Waiver Request Drawer: Same as main waiver drawer
- Report Template Drawer: Template preview with client-specific layout

**11. Modals**
- Outcome Declaration Modal: Clear / Minor Discrepancy / Major Discrepancy / Unable to Verify / Failed. Mandatory notes for all non-Clear. Evidence attach. Pre-adverse trigger (if Major/Failed). Legal confirmation text. [Confirm — my decision is recorded with my identity and timestamp]
- Adverse Action Modal (after waiting period): Issue final adverse notice + confirm
- Waiver Approve Modal (if adjudicator has authority): Review waiver request + approve/reject + mandatory note

**12. AI Components**
Full reviewer assist summary (most AI-rich page after Case Workbench). Discrepancy severity classifier. Suggested outcome (not binding — human decides).

---

### 6.1.17 Page: Waiver Management

**1. Page Objective**
Process waiver requests through a configurable approval chain — ensuring waivers are documented, authorized at the right level, and auditable.

**2. Primary Actors** Adjudicator (initiates), Risk/Legal (approves high-tier), Client (approves if required by policy)

**3. Key Workflows**
Waiver requested → Routed to approval tier → Reviewer approves/rejects → Outcome applied to case → Audit logged

**4. States**
Requested | Pending Ops Lead Approval | Pending Risk/Legal Approval | Pending Client Approval | Approved | Rejected | Expired (if not acted on in time)

**5. Actions**
Approve, reject, request more info, forward to higher tier, view waiver history for this candidate

**6. Data Blocks**
Discrepancy being waived, waiver justification, supporting evidence, requester identity, approval chain (each tier and who approved), approval notes, waiver history (has this candidate had prior waivers?)

**7. Tables**
- Pending Waivers Table: Request ID | Case ID | Discrepancy | Tier required | Requestor | Pending with | Days pending
- Waiver History Table: Case ID | Discrepancy waived | Date | Approved by | Reason

**8. Drawers**
- Waiver Detail Drawer: Full context — discrepancy details, justification, evidence, approval chain status, [Approve] [Reject] [Request More Info] actions
- Waiver History Drawer: All prior waivers for this candidate across all cases (cross-case — rare but important for recurrence detection)

**9. Modals**
- Approve Modal: Approval note (mandatory) + confirm
- Reject Modal: Rejection reason (mandatory) + confirm (notifies requester)
- Recurrence Warning Modal: "This candidate has had [N] prior waivers. Consider escalating for senior review before approving."

**10. Alerts/Banners**
- "Waiver awaiting your approval for [N] days" — amber
- "Waiver expired — no action taken in [N] days — case returned to adjudicator" — informational

---



---

## GAP-4 FIX: Waiver Recurrence Detection

### Addition to 6.1.17 Waiver Management — Waiver Detail Drawer

**Candidate Waiver History Panel**

Add to Waiver Detail Drawer (opens when viewing any pending waiver):

```
CANDIDATE WAIVER HISTORY
─────────────────────────────────────────────────────────────
⚠️ This candidate has 2 prior waivers — review before approving.

Case        Date        Discrepancy          Approved by     Outcome
CK-00234    Mar 2024    Emp date diff        J. Smith (HM)   Hired
CK-00456    Aug 2024    Title discrepancy    R. Patel (HM)   Hired
─────────────────────────────────────────────────────────────
Current waiver would be the 3rd waiver for this candidate.
Consider escalating to Risk review given recurrence.
```

**Recurrence Alert Thresholds**
- 1 prior waiver: informational note (no warning)
- 2 prior waivers: amber warning banner (shown above)
- 3+ prior waivers: red warning + auto-escalation recommendation + notification to Ops Lead

**Recurrence Warning Banner (3+ waivers)**
```
⚠️ HIGH RECURRENCE — SENIOR REVIEW RECOMMENDED

This candidate has had [N] prior waivers across [N] cases with KPMG.
Pattern: [Employment discrepancies / Mixed types / Same check type repeated].

This waiver requires Ops Lead awareness before approval.
[Notify Ops Lead] [Proceed with standard approval anyway (note required)]
```

**Waiver History Drawer (standalone)**
Add to Waiver Management page (6.1.17) — new button on waiver list row: [Candidate Waiver History]:
- Full cross-case waiver history for this candidate
- Waiver type, severity, approver, date, outcome per case
- Trend indicator: "Discrepancy rate: increasing / stable / first occurrence"
- Export: candidate waiver history PDF for Risk team

**API Addition**
`GET /v1/candidates/{candidate_master_id}/waivers` — returns all waivers across all cases for this candidate identity master record.

---
### 6.1.18 Page: BGV Report Builder and Delivery

**1. Page Objective**
Generate, review, approve, and deliver the final BGV report to the client — the primary deliverable of the entire BGV process.

**2. Primary Actors** Adjudicator (generates), QC Reviewer (approves), System (delivers)

**3. Key Workflows**
Select template → Preview populated report → Apply color-code → Sign off → QC approve → Deliver to client portal + notification

**4. States**
Template Selection | Preview | Sign-off Pending | QC Pending | Approved | Delivered | Re-issued (version > 1)

**5. Actions**
Select template, preview, toggle section inclusion, apply color code, sign off, trigger QC review, approve for delivery, deliver, re-issue (if correction needed)

**6. Data Blocks**
Client template configuration, all verified check outcomes, discrepancy summaries (adjudicated), color-code matrix result, reviewer sign-off identity, QC approval record, delivery confirmation

**7. UI Regions**
- Left: Template selector + section toggles
- Center: Live report preview (PDF render in browser)
- Right: Sign-off panel + delivery config

**8. Cards**
- Template Status Card: Template name, version, client-specific customizations
- Color Outcome Card: Overall color (per client's matrix) + per-check color breakdown
- Sign-off Card: Adjudicator name + date + signature
- Delivery Card: Destination (client portal) + notification channels + delivery timestamp

**9. Drawers**
- Section Config Drawer: Show/hide sections per client agreement — e.g., hide financial check details if client agreed to summary-only
- Redaction Drawer: Mark specific fields for redaction before client delivery (per agreement)
- Delivery Preview Drawer: Preview exactly what the client will see in their report inbox

**10. Modals**
- Re-issue Modal: Reason for re-issue (error correction / new information / client request) — mandatory + version increment confirmation
- Delivery Confirmation Modal: "Deliver report to [Client] for [Candidate]? Client will be notified immediately." [Confirm Delivery]

**11. Alerts/Banners**
- "QC sign-off required before delivery" — amber (if QC configured for this package)
- "Report delivered successfully to [Client] on [timestamp]" — green toast
- "Pre-adverse waiting period active — report cannot be delivered until [date]" — red blocker

---

### 6.1.19 Page: Vendor Assignment Console

**1. Page Objective**
Route unassigned check items to appropriate vendors based on check type, geography, availability, and SLA history — with AI-assisted matching.

**2. Primary Actors** Ops Reviewer, Team Lead

**3. Key Workflows**
View unassigned items → Select vendor (AI suggestion + manual option) → Confirm assignment → Track acknowledgment

**4. States**
Unassigned | Assigned (awaiting acknowledgment) | Acknowledged | In Progress | Submitted | Overdue

**5. Data Blocks**
Unassigned check items (check type, geography, SLA deadline), vendor capability matrix (check types, geographies, SLA commitments), vendor workload (active assignments, capacity %), AI routing suggestion, assignment history

**6. Tables**
- Unassigned Items Table: Case ID | Check type | Geography | SLA deadline | AI suggested vendor | [Assign]
- Vendor Capability Matrix: Vendor | Check types | Geographies | SLA commitment | Current capacity | Avg TAT

**7. Drawers**
- Assignment Drawer: Vendor selector with capability + workload + SLA projection. AI recommendation highlighted. Manual override available. Confirm → vendor notified.
- Bulk Assignment Drawer: Assign 10–50 similar items to one vendor in one action

**8. Modals**
- Overload Warning Modal: "This vendor has [N] active assignments and is at [X]% capacity. SLA risk is elevated. Assign anyway or select alternate?"

**9. AI Components**
AI routing suggestion: "Best match: Vendor A — capability ✓, geography ✓, current load 60%, historical TAT for this check type: 2.1 days (SLA: 3 days)"

---

### 6.1.20 Page: Vendor Performance Dashboard

**1. Page Objective**
Monitor all vendors' SLA compliance, quality, and reliability — with drill-in per vendor for performance review meetings.

**2. Primary Actors** Ops Manager, Team Lead

**3. Key Workflows**
Review overall vendor scorecard → Identify underperforming vendors → Drill into specific vendor → Export for vendor review meeting → Trigger performance alert

**4. Data Blocks**
Per vendor + check type: avg TAT, SLA compliance %, quality score (QC error rate on submissions), response rate, active assignments, breach count

**5. Cards**
- Top Vendor Card: Best SLA compliance this month
- Bottom Vendor Card: Lowest SLA compliance — action required
- "Performance Alert" card: Vendors auto-flagged for below-threshold performance

**6. Charts**
- Vendor comparison bar chart (SLA compliance % for all vendors)
- TAT distribution per vendor (box plot — min/p50/p90)
- Quality score trend (monthly, last 6 months)

**7. Tables**
- Vendor Scorecard Table: Vendor | Check type | Avg TAT | SLA % | Quality score | Response rate | Active | Breaches (30d) | Status
- Breach Log: Vendor | Case ref | Check type | Breach date | Delay duration | Root cause

**8. Drawers**
- Vendor Detail Drawer: Individual vendor scorecard — all metrics with 6-month trend charts. [Export PDF] for vendor meeting.
- Performance Alert Drawer: Configure alert thresholds per vendor

**9. Alerts/Banners**
- "Vendor [X] SLA compliance below [target]% for 2 consecutive weeks — consider review meeting" — amber

---

### 6.1.21 Page: Vendor Onboarding Wizard

**1. Page Objective**
Onboard new verification vendors with complete capability configuration, SLA agreement capture, and mandatory DPA execution before activation.

**2. Primary Actors** Ops Admin, Vendor Manager

**3. Workflow Steps**
1. Vendor Details (org name, type, PAN, GSTN, primary contact)
2. Capability Configuration (check types + geographies — matrix toggles)
3. SLA Agreements (per check type + geography — days to complete)
4. User Accounts (vendor-side users: verifier, team lead, manager)
5. Documents (contract upload, DPA upload — mandatory gate before activation)
6. Activate

**4. Validation Gate**
Cannot activate without: contract uploaded, DPA uploaded, at least one capability configured, at least one user created.

**5. Modals**
- DPA Missing Modal: "A Data Processing Agreement must be executed before this vendor can be activated (DPDP/GDPR subprocessor requirement — RFP 22.3)."

**6. Audit**
Vendor onboarding event logged: creating admin, date, all configuration, DPA confirmation. Immutable.

---

### 6.1.22 Page: Ops-Vendor Communication Center

**1. Page Objective**
Track all structured communication between ops and vendors — replacing ad-hoc email threads with traceable, case-linked messages.

**2. Primary Actors** Ops Reviewer, Vendor Verifier

**3. Key Workflows**
Send assignment clarification → Request extension → Receive vendor query → Respond → Archive

**4. Data Blocks**
Per message: sender, recipient (vendor), case reference, message body, attachment, timestamp, read status

**5. Tables**
Communication log: Date | Vendor | Case ref | Subject | Delivery status | [View thread]

**6. Drawers**
- Message Compose Drawer: Vendor selector, case reference, message body, attachment, template option
- Thread View Drawer: Full message thread per case per vendor

**7. Alerts/Banners**
- "Vendor query unread for > 24 hours" — amber

---

### 6.1.23 Page: Reports Pending Generation Queue

**1. Page Objective**
List all cases where adjudication is complete and reports are pending creation — ensuring no delay between adjudication and report delivery.

**2. Primary Actors** Adjudicator, Ops Admin

**3. Key Workflows**
View queue → Select template → Generate report → Move to QC/delivery queue

**4. States**
Adjudication Complete — Report Pending | Template Selected | Generating | QC Pending | Ready for Delivery

**5. Tables**
Queue table: Case ID | Candidate | Client | Outcome color | Adjudicated by | Adjudication date | Template assigned | Status | [Generate]

**6. Cards**
- "Oldest pending report" card: Days since adjudication for the longest-waiting report (should trend to 0)
- "Blocked" card: Reports blocked (pre-adverse waiting period active, QC pending)

**7. Bulk Actions**
Bulk assign template | Bulk generate (for batch delivery clients)

**8. Alerts/Banners**
- "Report for Case [X] has been pending [N] days since adjudication" — amber

---

### 6.1.24 Page: Report Archive

**1. Page Objective**
Search and access all previously generated BGV reports — with version history, re-issue capability, and access logging.

**2. Primary Actors** Ops Reviewer, Adjudicator, Compliance Reviewer

**3. Key Workflows**
Search report by candidate/case → View/download → Check version history → Re-issue if needed → Audit who accessed report

**4. States**
Current version | Superseded version (archived — accessible but labeled)

**5. Tables**
Archive table: Case ID | Candidate | Client | Report date | Outcome color | Version | Template | Issued by | [View] [Download] [Re-issue]

**6. Drawers**
- Version History Drawer: All versions of a report (v1, v2...) — reason for re-issue per version
- Access Log Drawer: Who downloaded this report, from which portal, when

**7. Modals**
- Re-issue Modal: Reason (mandatory) + version increment + re-delivery confirmation

**8. Alerts/Banners**
- "This report has been superseded — version 2 available" — informational on v1 view

---

### 6.1.25 Page: Standard Operational Reports Library

> **C-13 | RFP 18.1, 18.6 | Legacy: PPTX "Reports: 10–15 — Mostly Generated Offline"**
> Scheduled delivery is the PRIMARY workflow. On-demand preview/download is SECONDARY.
> Recipients receive reports in their inbox automatically — they should not need to log in
> and run reports manually for recurring needs.

**1. Page Objective**
Pre-built reports for operational management, MIS, and client reporting. Primary use: set up
scheduled deliveries so reports arrive automatically in recipients' inboxes. Secondary use:
on-demand generation for ad-hoc investigation.

**2. Primary Actors** Ops Manager, Team Lead, Compliance Reviewer

**3. Report Catalog (10–15 minimum per RFP 18.6 KPI/KRI library)**
1. Cases Initiated — daily/weekly/monthly, by client/check type
2. Cases Completed — with TAT analysis
3. SLA Compliance Report — by client/vendor/check type
4. Discrepancy Frequency Report — by type/check/client
5. Vendor Performance Report
6. Insufficiency Rate Report — by check type/client
7. QC Error Report — by reviewer/check type
8. Fraud Flag Summary Report
9. Escalation Summary Report
10. Candidate Completion Rate Report
11. Waiver Report — by client/discrepancy type
12. Data Subject Request Summary
13. Consent Audit Report
14. Notification Delivery Report — channel-wise success rate
15. TAT by Check Type and Geography

**4. Per-Report UI Layout**

Each report opens with two tabs — Schedule is the default (primary) tab:

**TAB 1 — SCHEDULE DELIVERY (default, primary) [C-13]**
```
SCHEDULE THIS REPORT
──────────────────────────────────────────────────────────────
Frequency:    [Weekly ▼]
Day & time:   [Monday ▼]  at  [08:00 ▼]
Parameters:   Client: [All Clients ▼]  |  Check type: [All ▼]
              Period: [Last 7 days (rolling) ▼]
Format:       [PDF ▼]  /  [Excel]  /  [Both]
Recipients:   [ops.manager@kpmg.com     ] ×
              [sla.team@kpmg.com        ] ×
              [+ Add recipient]
──────────────────────────────────────────────────────────────
[Send Test Now]  ← generates one instance immediately for validation
[Save Schedule]  [Cancel]
──────────────────────────────────────────────────────────────
Active schedule (if one exists):
  ✅ Every Monday 08:00 → 4 recipients → PDF
  Last run: Mon 27-May 08:01 → Delivered ✅
  [Edit Schedule]  [Pause]  [Delete Schedule]
```

**TAB 2 — RUN NOW (secondary — for ad-hoc use)**
```
- Parameter selector: Date range, client, check type, geography
- [Generate Report] button
- In-portal preview: paginated table + chart
- Export: [Download PDF] [Download Excel] [Download CSV]
- Data freshness note: "Report data as of [timestamp] (Reporting DB — up to 60s lag)"
```

**5. Drawers**
- Schedule Edit Drawer: Modify frequency, recipients, parameters, format for an existing schedule
- Report Preview Drawer: Full paginated table view (from Tab 2 Run Now)

**6. Alerts/Banners**
- "Schedule active — next delivery: Monday 08:00 to 4 recipients" — green status bar
- "Last scheduled run failed — [reason]. [Retry Now]" — amber
- "No schedule set up for this report. [Set Up Schedule]" — blue informational (shown when Tab 2 is open and no schedule exists)
- "Test report sent to [email] — check your inbox to verify format and content" — green (after [Send Test Now])

**7. Data Source**
All reports served from Reporting DB (Part 4.8 — never operational DB).
Data freshness: up to 60-second lag (shown in report footer and Tab 2 banner).

---

---

## C-13 FIX: New Page — Scheduled Report Manager

> **RFP 18.1, 18.6 | Legacy: PPTX "Reports: 10–15 — Mostly Generated Offline"**
> Elevates scheduled delivery from a buried drawer to a first-class management page.
> Central hub for all active report schedules across all report types.

---

### Page: Scheduled Report Manager (Ops Portal Section 6.6)

**1. Page Objective**
Single management hub for all active report schedule deliveries across all report types.
Answers: "Is my weekly SLA report going out?" "Did last night's report succeed?"
"How do I pause the vendor performance report while the vendor manager is on leave?"
Replaces the legacy pattern of emailing ops staff to check whether scheduled reports ran.

**2. Primary Actors** Ops Manager, Team Lead, Compliance Reviewer

**3. Key Workflows**
View all active schedules → Check last delivery status → Edit schedule parameters →
Pause / resume → Retry failed delivery → Add new schedule → Export delivery audit log

**4. States**
Per schedule: Active | Paused | Error (last delivery failed) | Deleted
Per delivery: Delivered | Failed | Skipped (holiday / maintenance window) | Pending (next run)

**5. Actions**
View all schedules, add schedule (wizard), edit schedule, pause, resume, run now (one-time),
delete, view per-schedule delivery history, retry failed delivery, export delivery log

**6. Data Blocks**
Per schedule: schedule ID | report type | parameters snapshot | frequency | day/time |
recipients list | format | status | last run timestamp | last run result | next run timestamp |
created by | created at

Per delivery record: schedule ID | run timestamp | report type | period covered | recipients
count | status | failure reason (if failed) | file size | retry count

**7. UI Regions**
- Top: [+ Add Schedule] button (primary CTA) | Filter bar (status / frequency / report type)
- Active schedules table (main content area — all active and paused schedules)
- Delivery history panel (below table — last 30 delivery events, all schedules)

**8. Tables**

Active Schedules Table:
| Report Name | Frequency | Next Run | Recipients | Format | Status | Last Run | Actions |
|---|---|---|---|---|---|---|---|
| SLA Compliance Report | Weekly (Mon 08:00) | Mon 02-Jun 08:00 | 4 people | PDF | ✅ Active | ✅ Mon 27-May | [Edit] [Pause] [Run Now] [Delete] |
| TAT Analysis — All Clients | Monthly (1st, 09:00) | Sun 01-Jun 09:00 | 2 people | Excel | ✅ Active | ✅ 01-May | [Edit] [Pause] [Run Now] [Delete] |
| Escalation Summary | Daily (17:00) | Today 17:00 | 3 people | PDF | ✅ Active | ✅ Yesterday | [Edit] [Pause] [Run Now] [Delete] |
| Vendor Performance | Monthly (1st, 09:00) | — | 6 people | Both | ⏸ Paused | ⏸ Paused by [name] 14-May | [Edit] [Resume] [Delete] |
| QC Error Report | Weekly (Fri 18:00) | — | 2 people | Excel | ❌ Error | ❌ Fri 24-May — Failed | [Edit] [Retry] [Delete] |

Status icons: ✅ Active | ⏸ Paused | ❌ Error (last delivery failed)

Delivery History Table (last 30 runs, all schedules):
| Timestamp | Report | Period Covered | Recipients | Status | Details |
|---|---|---|---|---|---|
| Mon 27-May 08:01 | SLA Compliance | 20–26 May | 4 sent | ✅ Delivered | — |
| Fri 24-May 18:00 | QC Error Report | 17–23 May | 2 | ❌ Failed | SMTP timeout [Retry] |
| Thu 23-May 17:00 | Escalation Summary | 23 May | 3 sent | ✅ Delivered | — |

**9. Drawers**

Schedule Setup Wizard Drawer (on [+ Add Schedule]):
```
STEP 1 — SELECT REPORT
  [Report type dropdown — full catalog list]

STEP 2 — CONFIGURE PARAMETERS
  Client: [All / Specific client ▼]
  Check type: [All / Specific ▼]
  Period type: [Rolling last 7 days ▼]
             (Rolling last 30 days / Rolling last month /
              Fixed date range — requires manual update each run)

STEP 3 — DELIVERY SCHEDULE
  Frequency: [Weekly ▼]
  Day: [Monday ▼]  Time: [08:00 ▼]
  Timezone: [IST ▼]

STEP 4 — RECIPIENTS AND FORMAT
  Recipients: [+ Add email address]
  Format: [PDF ▼] / [Excel] / [Both]

STEP 5 — TEST AND CONFIRM
  [Send Test Now] → "Test report sent to [email]. Check inbox to confirm
                     format and content before saving schedule."
  [Save Schedule] → Schedule activated immediately
```

Schedule Edit Drawer: Pre-filled wizard with current values. All fields editable.
Note shown if schedule is currently Active: "Changes take effect from the next scheduled run."

Schedule History Drawer (per schedule): Full delivery log for that schedule — all runs
with timestamp, status, recipients, file size, failure reason, retry count.

**10. Modals**
- Delete Confirmation Modal: "Delete schedule for '[Report Name]'? This will stop all future
  deliveries. Delivery history is preserved for audit. [Confirm Delete]"
- Pause Confirmation Modal: "Pause schedule for '[Report Name]'? Deliveries will stop until
  you resume. [Pause] — Note: Resume must be done manually."
- Retry Modal: "[Report Name] failed on [date]. Retry now will generate the report for the
  original period ([dates]) and re-deliver to [N] recipients. [Confirm Retry]"

**11. Alerts/Banners**
- "1 schedule has failed and needs attention — [View Failed Schedules]" — red, persistent
- "3 schedules are paused — [View Paused]" — amber informational
- "Schedule saved — next delivery: [day] at [time] to [N] recipients." — green, after save
- "Test report sent — check [email] inbox." — green, dismissible, after test

**12. Audit**
Every schedule create / edit / pause / resume / delete / manual run-now is logged:
actor, timestamp, what changed. All delivery events (success/failure) logged with
file hash of the generated report. Exportable as delivery audit log (CSV/PDF).

**13. Mobile** Management of schedules is desktop-recommended. Mobile: view-only
(see schedule list and last delivery status). [Run Now] and [Retry] are mobile-accessible.

---

### 6.1.26 Page: MIS / Analytics Dashboard

**1. Page Objective**
Strategic analytics for ops leadership — pipeline visibility, TAT benchmarking, breach analysis, fraud trends, vendor trends, productivity analytics.

**2. Primary Actors** Ops Director, Operations Manager

**3. Key Workflows**
Review pipeline health → Analyze TAT trends → Identify breach root causes → Track fraud signal trends → Export for leadership reporting

**4. States**
Default view (MTD) | Custom period | Filtered (by client/check type)

**5. UI Regions**
- Top: Period selector + filter bar
- KPI strip: Total cases MTD | Completed | SLA compliance % | Avg TAT | Discrepancy rate | Fraud flag rate
- Chart grid: 2-column responsive
- BI export section (bottom)

**6. Cards / KPI Strip**
Cases MTD | Cases Completed | SLA Compliance % | Avg TAT (days) | Discrepancy Rate | AI Fraud Flag Rate | QC Error Rate

**7. Charts**
- Pipeline funnel: Cases by lifecycle stage (stacked bar)
- TAT heatmap: Client (Y) vs check type (X) — color = avg TAT vs SLA
- SLA breach trend: Line chart (weekly breach count, last 12 weeks)
- SLA breach root cause: Pie (vendor delay / candidate delay / system / ops)
- Discrepancy type frequency: Horizontal bar (top 10 types)
- Fraud flag trend: Area chart (AI flags raised vs confirmed vs false positive)
- Vendor TAT comparison: Bar chart per vendor
- Candidate completion rate trend: Line chart (% completing within 48h of invitation)

**8. Drawers**
- Chart Drilldown Drawer: Click any chart segment → filtered case list for that segment
- **BI Export Config Drawer [C-09 | RFP 18.5]:** Full BI connector configuration — two options:
  - **Option A (Database Connector):** JDBC/ODBC read-only connection to Reporting DB. Tenant-scoped. Generate credentials button → service account + connection string (host, port, DB name, read-only username, password). Copy connection string. Supported tools listed: Power BI (Import + DirectQuery), Tableau (Live/Extract), Looker, Metabase. Note: "All data served from Reporting DB — anonymised schema, no raw PII, row-level security by tenant view."
  - **Option B (REST API Connector):** OAuth 2.0 client credentials. Generate API key button. Base URL + available analytics endpoints listed. Download Power BI custom connector file. Download Tableau WDC template. Rate limit shown: "60 requests/minute."
  - Both options: Last used timestamp | Revoke credentials | Re-generate
  - Data freshness note: "Analytics data reflects state as of [N] seconds ago. Max lag: 60 seconds."

**9. Filters**
Time period | Client (multi) | Check type | Country | Check type

**10. AI Components**
- Trend anomaly detection: "Discrepancy rate for employment checks increased 12% this month vs prior 3-month avg — possible cause: [AI-suggested]"
- Vendor outlier detection: "Vendor X TAT is 2.3x higher than category average"

---


---

## GAP-EXP-H1 FIX: Fraud Intelligence Dashboard — Operations Portal

### H-1 | Fraud Intelligence Dashboard — Missing from Ops Portal

**RFP Reference:** RFP 2.24

**RFP Text:**
> *"Fraud intelligence dashboard — Central dashboard showing fraud patterns, top signals, and emerging threats"*

**Verdict:** EXPLICIT

**Analysis:**
RFP 2.24 is a direct, standalone named requirement under the AI Features category. "Central dashboard" is an explicit UI deliverable — not a tab embedded in a different report. The requirement for "patterns, top signals, and emerging threats" implies a dedicated intelligence view with trend analysis across cases, not just individual case-level fraud flags. The current design maps RFP 2.24 to the MIS Dashboard as a Fraud Analytics tab, which is insufficient: a tabbed view within a generic MIS report does not constitute a "central dashboard" for fraud intelligence. Risk and Fraud Review teams need a primary workspace for fraud signal monitoring.

**Impact:**
- Without a dedicated Fraud Intelligence Dashboard, the Risk team has no aggregate fraud visibility — they can only see fraud signals on individual cases.
- Emerging fraud patterns (e.g., a surge in credential farming from a specific geography) cannot be detected without cross-case aggregated views.
- AI fraud threshold calibration (which requires visibility into false positive rates and signal distribution) has no UI home.

**Recommendation:**
Add 6.1.27A: Fraud Intelligence Dashboard as a distinct page in the Ops Portal Reporting & Analytics section.

---

### New Page: 6.1.27A Fraud Intelligence Dashboard — Operations Portal

**1. Page Objective**
Provide the Risk team and Ops Management with a central, real-time intelligence view of fraud signals, fraud pattern trends, emerging threats, and AI detection performance — directly actionable from a single workspace.

**2. Primary Actors**
Fraud Reviewer, Senior Reviewer, Ops Manager, CISO (read-only)

**3. Key Workflows**
Review today's fraud flags → Investigate emerging patterns → Drill down to flagged cases → Calibrate AI thresholds (link to Super Admin) → Export fraud trend report

**4. States**
Live (real-time) | Forensic Investigation Mode (case frozen, fraud reviewer active) | Archived (historical analysis)

**5. Actions**
Drill down to flagged case, filter by signal type, filter by time period, compare to baseline, export trend report, flag for threshold review, open threshold configuration (Super Admin link)

**6. Data Blocks**
AI fraud signal aggregates (by type, by check, by geography) | Case-level fraud flags with severity | Emerging pattern alerts | False positive rate by signal | Threshold performance metrics | Manual fraud override log

**7. UI Regions**
- Top: Signal Health Strip (today's count vs 7-day average)
- Left: Fraud signal trend charts (time-series, by fraud type)
- Center: Active fraud flags table (sortable by severity, recency)
- Right: Emerging patterns panel (AI-generated alerts on anomalous clusters)
- Bottom: Threshold performance row (precision/recall per signal type)

**8. Cards**
- Today's Signal Strip:
  ```
  ┌──────────────┬──────────────┬──────────────┬─────────────────┐
  │ Total Flags  │ High/Critical│ Under Review │ Avg. Confidence │
  │ Today: 34    │ Today: 7     │ Active: 12   │ 87.3%           │
  │ 7d avg: 29   │ 7d avg: 5    │ Closed: 22   │ 7d avg: 85.1%   │
  └──────────────┴──────────────┴──────────────┴─────────────────┘
  ```
- Top Fraud Signal Card: Signal type | Count today | 7d trend | AI confidence range
- Emerging Pattern Alert Card: "📈 Surge detected: Document fraud (Aadhaar) — 340% above baseline in last 48 hours. 8 cases flagged. [Investigate]"

**9. Tables**

**Active Fraud Flags Table:**
| Case Ref | Signal Type | Severity | AI Confidence | Check | Flagged | Status | Assigned |
|---|---|---|---|---|---|---|---|
| CK-0921 | Deepfake selfie | Critical | 94% | KYC | 2h ago | Under Review | [Name] |
| CK-0918 | Document metadata edit | High | 88% | Education | 4h ago | Under Review | [Name] |
| CK-0915 | GPS spoofing (field agent) | High | 91% | Address | 6h ago | Closed — Agent suspended | [Name] |
| CK-0910 | Dual employer mismatch | Medium | 79% | Employment | 8h ago | Investigation | [Name] |

**Signal Type Distribution Table (7-day):**
| Signal Type | Count | % of total | False Positive Rate | Trend |
|---|---|---|---|---|
| Document authenticity | 89 | 42% | 6.2% | ↑ +12% |
| Deepfake / liveness fail | 34 | 16% | 2.1% | → Stable |
| GPS spoofing (field) | 18 | 8% | 4.8% | ↑ +34% |
| Employment gap anomaly | 41 | 19% | 18.3% | ↓ -5% |
| Duplicate identity | 12 | 6% | 0.9% | → Stable |
| Other | 19 | 9% | — | — |

**10. Charts**
- 30-day fraud signal trend line (with 7-day moving average)
- Fraud signal type distribution donut chart
- Geography heat map (fraud density by candidate location)
- AI confidence score distribution histogram

**11. Drawers**
- Fraud Pattern Detail Drawer: Full context for an emerging pattern — affected cases list, signal details, first detection time, AI confidence evolution, recommended action (threshold review / ops alert)
- Case Drill-Down Drawer: Quick preview of flagged case — fraud signal details, AI reasoning, current status, assigned reviewer, [Open Case] link
- Threshold Review Drawer: Current threshold for selected signal type, false positive rate at current setting, recommended adjustment → links to Super Admin Threshold Configuration

**12. Filters**
Signal type | Severity (Critical/High/Medium/Low) | Time period (today/7d/30d/custom) | Check type | Geography | Case status | AI confidence range | Reviewer assigned

**13. Alerts/Banners**
- "🚨 EMERGING THREAT: [Signal type] — [N]% above baseline in past [N] hours. [N] active cases. Immediate review recommended." — red, dismissible
- "⚠ Threshold alert: [Signal type] false positive rate exceeds 15%. Consider threshold calibration." — amber
- "AI model update applied [date] — compare pre/post metrics in threshold view" — informational

**14. AI Components**
- Pattern detection engine: clusters similar fraud flags across cases using time-window, signal type, and geography
- Threshold performance monitor: real-time precision/recall per signal type vs configured threshold
- Emerging threat detector: statistical anomaly detection on fraud signal volumes (Z-score based alert at 2σ+ deviation)
- AI confidence score trending: tracks model confidence drift per signal type over time

**15. Evidence Components** None direct — links to individual case evidence via drill-down.

**16. Audit / Timeline**
All fraud pattern investigations triggered from this dashboard are logged with the investigating user's identity, timestamp, and outcome note.

**17. Mobile Considerations**
Alert strip and critical flags visible on mobile. Full chart analysis desktop-only.

**Part 5 IA Addition:**
Add to Ops Portal IA (Part 5.1) under section 6. Reporting & Analytics:
```
├── 6.5 Fraud Intelligence Dashboard
│   └── Page: Fraud Intelligence Dashboard
│       Purpose: Central fraud signal monitoring, pattern detection, AI performance visibility
│       RFP: 2.24 | Actors: Fraud Reviewer, Ops Manager | Classification: AI-Required
│
└── 6.6 Scheduled Report Manager  [NEW — C-13 | RFP 18.1, 18.6]
    └── Page: My Scheduled Reports
        Purpose: Central management hub for all active report schedules. View, edit,
                 pause, retry, and delete. Single place to confirm "Is my weekly SLA
                 report going out?" and "Did last night's delivery succeed?"
        RFP: 18.1 (operational dashboards), 18.6 (KPI/KRI library)
        Components:
          - Active schedules table:
              Report Name | Frequency | Next Run | Recipients | Status | Last Run
          - Per-row actions: [Edit] [Pause/Resume] [Run Now] [Delete] [View History]
          - [+ Add Schedule] button → 5-step schedule setup wizard
          - Delivery history: last 30 deliveries with status + [Retry] per failure
          - Filter: Status / Frequency / Report type
          - Export delivery log (audit record of who received what, when)
```


### 6.1.27 Page: SLA Policy Editor

> **C-03 | RFP 1.7, 22.2, 23.14**
> Redesigned from single-track to three-track SLA (Client / Internal / Vendor).
> RFP 1.7: "Separate TAT mapping for Client/Vendor and internal team."
> Default values pre-loaded from KPMG baseline (derived from legacy TAT 12–18 days).

**1. Page Objective**
Configure and govern the three-track SLA model (Client / Internal / Vendor) per check type per client — with pre-loaded KPMG baseline defaults, escalation ladder, pause conditions, and penalty rules. The three tracks run independently: a case can have its Client SLA on track while its Internal SLA has breached, independently of its Vendor SLA.

**2. Primary Actors** Ops Admin (configures), Ops Manager (reviews and approves), Platform Admin (global default)

**3. Key Workflows**
Load default template → Review and adjust per client agreement → Configure escalation ladder → Set pause conditions → Preview impact → Publish | Reset individual rows to default | Compare custom values against KPMG baseline | Version and rollback

**4. States**
Draft | Published (active) | Superseded (historical version)

**5. UI Regions**
- Left: Client selector (global default / per-client override)
- Center: Three-track SLA policy table (main configuration surface)
- Right: Preview panel — shows how configured SLA applies to a sample case with live countdown simulation
- Bottom bar: [Load Default Template] [Save Draft] [Publish] [Version History]

**6. Tables**

**Primary — Three-Track SLA Policy Table [C-03 | RFP 1.7]:**

| Check Type | Client SLA (bd) | Internal SLA (bd) | Vendor SLA (bd) | Amber (%) | Red (%) | Actions |
|---|---|---|---|---|---|---|
| Identity / KYC | 3 | 2 | 1 | 60% | 85% | [Edit] [Reset to Default] |
| Employment — Standard | 7 | 5 | 4 | 60% | 85% | [Edit] [Reset to Default] |
| Employment — Executive | 10 | 8 | 6 | 60% | 85% | [Edit] [Reset to Default] |
| Education | 7 | 5 | 5 | 60% | 85% | [Edit] [Reset to Default] |
| Criminal / Legal | 10 | 8 | 7 | 60% | 85% | [Edit] [Reset to Default] |
| Address — Digital | 3 | 2 | 1 | 60% | 85% | [Edit] [Reset to Default] |
| Address — Physical | 7 | 5 | 3 | 60% | 85% | [Edit] [Reset to Default] |
| Financial | 5 | 4 | 3 | 60% | 85% | [Edit] [Reset to Default] |
| Reference Check | 7 | 5 | 5 | 60% | 85% | [Edit] [Reset to Default] |
| *Full Standard Package* | *15* | *12* | *—* | *—* | *—* | [Edit] [Reset to Default] |
| *Full Executive Package* | *20* | *15* | *—* | *—* | *—* | [Edit] [Reset to Default] |

These are the KPMG baseline defaults — label shown: **"Default Template: KPMG Standard Baseline"**
All values are editable per client. [Reset to Default] per row restores that row's KPMG baseline.
[Load Default Template] at bottom restores all rows simultaneously.

Column definitions (shown as column header tooltips):
- **Client SLA (bd):** Contractual commitment to client. Breach triggers penalty (RFP 22.2).
- **Internal SLA (bd):** KPMG ops internal target. Breach = ops efficiency issue, not client penalty.
- **Vendor SLA (bd):** Vendor's committed turnaround from assignment. Breach = vendor scorecard impact.
- **Amber (%):** % of Client SLA elapsed at which amber warning fires → reviewer notified.
- **Red (%):** % of Client SLA elapsed at which auto-escalation fires → Team Lead notified.
- **bd:** Business days — calculated using the holiday calendar configured in Step 6 of tenant provisioning (RFP 23.14).

**Secondary — Escalation Ladder Table:**
At X% Client SLA elapsed → notify [role] → at Y% → notify [role] → at Z% → auto-escalate to [target]

**Tertiary — Pause Conditions Table:**
Condition | Which track pauses | Auto-resume condition | Max pause duration

Pause condition examples:
| Condition | Pauses | Resumes When |
|---|---|---|
| Candidate has not submitted | Client SLA | Candidate submits |
| Employer outreach sent, awaiting response | Client SLA + Vendor SLA | Employer responds |
| Vendor not yet assigned | Vendor SLA | Vendor assigned |
| Dispute filed by candidate | All three tracks | Dispute resolved |
| Public holiday (calendar-aware) | All three tracks | Next business day |

**7. Drawers**
- Policy Edit Drawer: Edit all three SLA values + amber/red thresholds for a specific check type. Shows: "Current value vs KPMG default" side-by-side for reference.
- Impact Preview Drawer: "If you change Internal SLA for Employment to [N] days — this would affect [X] currently active cases. [N] cases would immediately show as Internal SLA breached."
- Version History Drawer: Timeline of all published versions. [View] per version shows full config. [Rollback to this version] button.

**8. Modals**
- Publish Confirmation Modal: "Publishing this SLA policy will affect [N] active cases. Cases in progress will not be retroactively affected — new SLA applies to cases initiated after this publish. Confirm?"
- Reset All to Default Modal: "This will restore all [N] check types to KPMG baseline values. Any custom values for this client will be lost. Confirm?"
- Version Rollback Modal: "Roll back to version [N] (published [date])? Current policy will be archived."

**9. Alerts/Banners**
- "Unpublished changes pending — changes will not take effect until published" — amber
- "Internal SLA is set higher than Client SLA for [check type] — this means ops has no buffer before client breach. Adjust?" — red warning (validation)
- "Vendor SLA is set higher than Internal SLA for [check type] — vendor would breach before ops can act. Adjust?" — amber warning (validation)
- "[N] rows differ from KPMG default template — [View differences]" — blue informational when client has custom values

**10. SLA Three-Track Interaction Rules**
These rules govern how the three clocks relate — critical for coding the SLA engine:

```
Clock start rules:
  Client SLA clock:   starts when case is activated (ops confirms case)
  Internal SLA clock: starts when case is activated (same as Client)
  Vendor SLA clock:   starts when vendor is ASSIGNED (not when case activated)

Clock independence rules:
  Each track pauses and resumes independently (per Pause Conditions table)
  A Client SLA breach does NOT automatically mean Internal or Vendor breach
  All three clocks are tracked in real-time and stored as separate fields in case record

Breach rules:
  Client SLA breach:   → Penalty calculation trigger (RFP 22.2) + Ops Manager alert
  Internal SLA breach: → Team Lead alert only (no client impact unless Client also breaches)
  Vendor SLA breach:   → Vendor performance log + auto-notify vendor + Team Lead alert

Display rules (Case Workbench):
  SLA Health Card shows all three countdowns simultaneously:
  [Client: 3d 4h remaining ✅] [Internal: 1d 2h remaining ⚠️] [Vendor: Overdue ❌]
  Each with its own color band (Green / Amber / Red / Breached)
```

---

### 6.1.28 Page: Historical Escalation Analytics

**1. Page Objective**
Analyze escalation patterns over time to identify root causes, recurring issues, and systemic improvements.

**2. Primary Actors** Ops Manager, Team Lead

**3. Charts**
- Escalation volume trend (by type, weekly, last 12 weeks)
- Avg time to resolve (trend)
- Top escalation causes (horizontal bar)
- Escalation recurrence (by client — which clients generate most escalations)
- Auto vs manual escalation ratio trend

**4. Tables**
Historical Escalation Table: Period | Type | Count | Avg resolution time | Top cause | Actions taken

**5. Filters**
Time period | Escalation type | Client | Reviewer (originated by)

---

### 6.1.29 Page: Multi-Channel Communication Interface

**1. Page Objective**
Compose and send structured communications to any stakeholder — with template management, multi-language support, and delivery confirmation.

**2. Primary Actors** Ops Reviewer, Team Lead

**3. Key Workflows**
Select recipient type → Choose template → Personalize → Select channel → Send or schedule → Confirm delivery

**4. States**
Composing | Sending | Delivered | Failed | Scheduled (pending send time)

**5. UI Regions**
- Recipient panel: type selector (candidate/employer/university/vendor/client) + individual selector
- Message panel: template selector + body (editable) + personalization tokens reference
- Channel panel: Email/SMS/WhatsApp availability indicator + selector
- Delivery options: Send now / Schedule
- Preview panel: Rendered message preview

**6. Cards**
- Template Preview Card: Renders template with actual case data substituted for tokens
- Delivery Channel Status Card: For selected recipient — which channels are available (has email? has mobile? WhatsApp registered?)

**7. Drawers**
- Template Library Drawer: Browse all templates by purpose/recipient type — preview each
- Personalization Tokens Drawer: Reference list of available tokens ({{candidate_name}}, {{case_id}}, etc.)
- Bulk Compose Drawer: Send one message to multiple recipients of same type (e.g., reminder to all candidates pending re-submission)

**8. Modals**
- Schedule Send Modal: Date/time picker + time zone confirmation
- Bulk Send Confirmation Modal: "You are sending to [N] recipients. [Preview first recipient] [Confirm Send All]"

**9. Alerts/Banners**
- "WhatsApp not registered for this recipient — SMS and Email will be used"
- "Previous notification to this recipient failed — check number/email before resending"

**10. SLA Components**
Delivery confirmation tracked per notification — failed delivery automatically pauses relevant SLA clock.

---

### 6.1.30 Page: Delivery Status & Failure Management

**1. Page Objective**
Real-time visibility into notification delivery failures — enabling manual intervention before candidates miss critical communications.

**2. Primary Actors** Ops Reviewer, Team Lead

**3. Key Workflows**
Review failed deliveries → Understand failure reason → Attempt alternate channel → Manual re-send → Update contact details if wrong → Resume SLA if paused

**4. States**
Per notification: Sent | Delivered | Opened | Failed — Channel Attempted | Failed — All Channels | Manually Resent | Unresolvable (no valid contact)

**5. Tables**
- Failure Table: Case ID | Candidate | Channel | Failure reason | Attempt count | Last attempt | SLA paused (Y/N) | [Re-send] [Update Contact] [Mark Unresolvable]
- Failure reason categories: Invalid number / WhatsApp not registered / Email bounced / Spam blocked / Carrier failure / Delivery timeout

**6. Drawers**
- Contact Update Drawer: Update candidate contact details (email/mobile) — logged in audit as ops-updated
- Re-send Config Drawer: Choose alternate channel + message + confirm

**7. Modals**
- Mark Unresolvable Modal: "Mark this candidate as unreachable. SLA will be noted as candidate-delay. Client will be notified." + confirm

**8. Charts**
- Failure trend: Daily failure rate by channel (last 30 days)
- Failure reason distribution: Pie chart (current week)

**9. Alerts/Banners**
- "Notification failure rate exceeded [threshold]% today — channel provider issue possible" — amber
- "[N] SLA clocks paused due to undeliverable notifications" — informational

---

### 6.1.31 Page: Communication Template Manager

**1. Page Objective**
Manage the library of email/SMS/WhatsApp templates — with versioning, approval workflow, and multi-language support.

**2. Primary Actors** Ops Admin, Team Lead

**3. Key Workflows**
Browse templates → Create/edit → Add language variants → Preview + test → Approval → Publish

**4. States**
Draft | Pending Approval | Published (active) | Archived (superseded)

**5. Tables**
Template Table: Name | Purpose | Channel | Languages | Version | Status | Last modified | [Edit] [Preview] [Test Send]

**6. Drawers**
- Template Edit Drawer: Rich text editor for email; plain text + character counter for SMS; WhatsApp template format (pre-approved structure required for WhatsApp Business API)
- Token Reference Drawer: Available personalization tokens with example values
- Language Variant Drawer: Manage translations per template — one language at a time

**7. Modals**
- Test Send Modal: Send test message to reviewer's own contact — verify rendering with real data
- Approval Request Modal: Submit template for review before publishing (change management)
- Archive Modal: "Archive this template? Active cases using this template will switch to the new version."

**8. Alerts/Banners**
- "WhatsApp templates require pre-approval from WhatsApp Business. Submit for review before publishing."
- "Template modified — re-approval required before publishing"

---

### 6.1.32 Page: Consent Record Viewer and Audit

**1. Page Objective**
Provide complete, tamper-evident consent audit trail — the primary compliance evidence surface for DPDP/GDPR audits.

**2. Primary Actors** Compliance Reviewer, Risk/Legal, Auditor

**3. Key Workflows**
Look up consent for specific candidate → Verify consent validity → Check version + scope → Export consent pack → Investigate withdrawal

**4. States**
Active | Expired (retention period over) | Withdrawn | Superseded (candidate re-consented on later version)

**5. Tables**
Consent Registry: Case ID | Candidate | Consent version | Signed date | IP address | Device fingerprint (hash) | Purpose scope | Status | [View] [Export Pack]

**6. Drawers**
- Consent Detail Drawer: Exact consent text (version at time of signing, immutable), e-signature image, signing metadata (timestamp, IP, device hash, geolocation if captured), consent version changelog
- Withdrawal Log Drawer: If consent withdrawn — withdrawal timestamp, reason (if given), downstream impact (cases paused/closed)
- Export Pack Drawer: Generate compliance export — PDF (human-readable) + JSON (machine-readable) + hash manifest

**7. Modals**
- Consent Validity Check Modal: For ops when unsure if consent covers a specific purpose — "Does consent version [X] cover [purpose]?" → Yes/No/Review

**8. Alerts/Banners**
- "Consent expired for Case [X] — verification cannot continue" — red
- "Candidate withdrew consent on [date] — case closed" — informational

---

### 6.1.33 Page: Immutable Audit Log Viewer

**1. Page Objective**
Provide complete, tamper-evident record of every action on every case — for regulatory audits, dispute investigation, and compliance defense.

**2. Primary Actors** Compliance Reviewer, Auditor, Risk/Legal

**3. Key Workflows**
Filter audit events by case/actor/type → View event detail → Verify log integrity → Export audit pack for regulatory submission

**4. States**
Live (current cases) | Archived (cold storage, cases > 12 months — query on demand)

**5. Tables**
Audit Event Table: Event ID | Case ID | Timestamp (UTC) | Actor | Actor role | Portal | Action type | Affected entity | Before value (redacted/hashed) | After value | Event hash | Chain link (prev hash)

**6. Drawers**
- Event Detail Drawer: Full event payload — all fields, raw hash, chain position, verification status
- Archive Query Drawer: Query cold storage for older events — date range + case ID + results returned asynchronously

**7. Modals**
- Hash Verification Modal: "Verify chain integrity for Case [X]. Running... Complete. [N] events verified. Chain intact. ✓" or "Chain broken at event [ID] — security incident alert triggered."

**8. Filters**
Case ID | Actor | Action type | Portal | Date range | Entity type (case/consent/document/user)

**9. Export**
PDF audit pack (formatted, per-case) + JSON with hash manifest. Each export event itself logged.

**10. Alerts/Banners**
- "Archive query in progress — results will be available in [N] minutes" (cold storage latency)
- "Hash chain integrity check: last verified [date]. ✓ Intact"

---

### 6.1.34 Page: DSAR Management

**1. Page Objective**
Manage DPDP/GDPR data subject rights requests within legally required timelines — access, correction, erasure, portability requests.

**2. Primary Actors** Compliance Reviewer, Risk/Legal

**3. Key Workflows**
DSAR received → Acknowledge (starts clock) → Investigate (pull all data for candidate) → Prepare response → Deliver → Archive

**4. States**
Received | Acknowledged | Under Investigation | Response Prepared | Delivered | Closed

**5. Data Blocks**
DSAR type, candidate identity, all data held (across all cases, all tenants for this candidate), legal hold check (active dispute or litigation), response package, delivery confirmation

**6. Tables**
DSAR Registry: Request ID | Type | Candidate | Filed date | Legal deadline | Assigned to | Status | Days remaining

**7. Drawers**
- Full Data Pull Drawer: All data held for this candidate — personal info, case records (case IDs only — not full case details), consent records, communication log, document metadata (not documents themselves)
- Erasure Impact Check Drawer: "Erasing this candidate's data will affect: [N] active cases (legal hold applies), [N] completed cases (retention period not expired), [N] cases eligible for erasure"
- Response Package Drawer: Structured response for Access requests — downloadable ZIP (CSV data export + document references + consent record)

**8. Modals**
- Erasure Legal Hold Modal: "Case [X] is under active dispute/litigation. Erasure cannot proceed for this case until legal hold is lifted. Partial erasure of other records can proceed."
- Acknowledge Modal: "Acknowledging this request starts the legal response clock. Response due by [date]."
- Close DSAR Modal: Response delivered, candidate notified, record archived

**9. SLA Components**
DPDP 30-day hard clock (non-adjustable). Countdown in table + case header. Red when < 7 days remaining.

---


---

## GAP-EXP-C6 FIX: Right-to-Correction Workflow — Candidate Portal + Ops Portal

### C-6 | Right-to-Correction Workflow Page — Missing (Conflated with Generic Dispute Page)

**RFP Reference:** RFP 15.7

**RFP Text:**
> *"Right-to-correction workflow — Allow correction requests and track resolutions"*

**Verdict:** EXPLICIT

**Analysis:**
RFP 15.7 is a standalone, named requirement listed separately from RFP 15.8 (erasure) and RFP 10.10 (dispute management). The RFP's explicit treatment of correction as a distinct workflow — not a subset of dispute — means that the current design of routing correction requests through the generic dispute page fails this requirement. DPDP Section 13 (India) establishes the right to correct as a separate statutory right with a distinct 30-day resolution SLA. The UI must reflect this distinction: different form, different SLA clock, different operator queue.

**Impact:**
- DPDP non-compliance from day one for Indian clients: Section 13 right-to-correction is a statutory obligation with penalty exposure.
- Candidates requesting correction of inaccurate data (distinct from disputing a verification outcome) receive no clear process — leading to trust failure and potential regulatory complaint.
- Ops teams cannot distinguish correction requests from factual disputes, causing incorrect SLA tracking and mishandled resolutions.

**Recommendation:**
Add the following two components to the architecture:

---

### New Page: 6.3.16 Right-to-Correction Request — Candidate Portal

**1. Page Objective**
Provide candidates with a dedicated, legally distinct interface to exercise their DPDP Section 13 right to correct inaccurate or incomplete personal data — separately from the factual dispute workflow.

**2. Primary Actors**
Candidate

**3. Access Path**
Candidate Portal → Help & Support → "Correct My Personal Data" OR direct link from status page → "My Data Rights" section

**4. Key Workflows**
Candidate identifies inaccurate field → Selects data category → Describes correction needed → Uploads supporting evidence → Submits correction request → Receives acknowledgement with request ID and 30-day SLA confirmation

**5. States**
Not Started | Draft | Submitted (pending ops review) | Information Requested (ops needs more context) | Correction Applied | Correction Rejected (with explanation)

**6. Actions**
Select data category, describe correction, upload evidence, submit, check correction status, re-submit if more information requested

**7. Data Blocks**
Request ID (system-generated) | Data category (personal info / employment data / education data / identity documents / address) | Current (incorrect) value (pre-filled from case data where possible) | Requested correction | Supporting evidence (upload) | Request timestamp | Acknowledgement receipt

**8. UI Regions**
- Header: "Correct My Personal Data — Your Right Under Applicable Privacy Law"
- Correction category selector
- Current data display (read-only, from candidate's submitted case data)
- Correction description field
- Evidence upload
- Submission confirmation with request ID + SLA statement

**9. Form Fields**

```
CORRECTION REQUEST FORM

What data would you like to correct?
○ Personal details (name, date of birth, address)
○ Employment information (company, dates, designation)
○ Education information (institution, degree, year)
○ Identity document details (ID numbers, validity)
○ Contact information (phone, email)

Current data on file (pre-filled):
[Display of current value from case — read-only]

What is the correct information?
[Free text — max 500 characters]

Why is the current data incorrect?
○ I entered it incorrectly
○ The data was changed (name change, moved address, etc.)
○ KPMG recorded it incorrectly from my submission
○ Other: [___________]

Upload supporting evidence (optional but recommended):
[Upload button — accepts PDF, DOCX, XLSX, JPG, PNG, ZIP — max 10 MB per file (per platform policy 4.7)]

[Submit Correction Request]

By submitting this request, you acknowledge that KPMG India will
review and respond within 30 days as required by applicable privacy law.
```

**10. Acknowledgement Screen**
```
✅ CORRECTION REQUEST RECEIVED

Request ID: CORR-2025-0421
Date submitted: [date]
Response due by: [date + 30 days]

You will receive an email at [email] when your request is reviewed.
If you need to follow up: Quote Request ID CORR-2025-0421

[Download Acknowledgement]  [Return to Home]
```

**11. Status Tracking (on Candidate Status Page — addition)**
Add "My Correction Requests" section:
| Request ID | Data Category | Submitted | Status | Due Date |
|---|---|---|---|---|
| CORR-2025-0421 | Employment info | 05-Jan-2025 | Under Review | 04-Feb-2025 |

---

### New Queue: Addition to 6.1.34 DSAR Management — Right-to-Correction Sub-Queue

**Addition to Part 6 — 6.1.34 DSAR Management Page:**

Add a dedicated "Right-to-Correction" tab to the DSAR Management page (in addition to existing DSAR tabs):

**Right-to-Correction Tab Content:**

**Correction Queue Table:**
| Request ID | Candidate | Case Ref | Data Category | Submitted | Status | Due Date | SLA Health |
|---|---|---|---|---|---|---|---|
| CORR-2025-0421 | [Name] | CK-0912 | Employment | 05-Jan | Under Review | 04-Feb | 🟢 24 days |
| CORR-2025-0389 | [Name] | CK-0876 | Personal | 28-Dec | Info Requested | 27-Jan | 🔴 2 days |

**Ops Actions per Correction Request:**
- [Review] → opens Correction Review Drawer
- [Request More Info] → sends candidate notification
- [Apply Correction] → updates case data + triggers audit event + notifies candidate
- [Reject with Explanation] → mandatory explanation field + candidate notification

**Correction Review Drawer:**
```
CORRECTION REQUEST REVIEW
─────────────────────────────────────────────────────
Request ID: CORR-2025-0421
Candidate: [masked name]      Case: CK-0912
Category: Employment Information
Submitted: 05-Jan-2025        Due: 04-Feb-2025 (24 days remaining)

CURRENT DATA ON FILE:
Company: Infosys Technologies Ltd
End Date: March 2022

REQUESTED CORRECTION:
End Date: June 2022
Reason: "I left in June, not March — please see resignation acceptance letter attached."

EVIDENCE UPLOADED:
📄 Resignation_Acceptance_Infosys.pdf   [View]

LINEAGE RECORD:
Original submission: 05-Jan-2025 (candidate-entered)
This correction request: 05-Jan-2025

DECISION:
[ Apply Correction ]  [ Request More Info ]  [ Reject ]

If applying: Mandatory note: ___________________________
If rejecting: Mandatory explanation (shown to candidate): ___
─────────────────────────────────────────────────────
```

**Audit Events (Right-to-Correction specific):**
| Event | Actor | Logged Data |
|---|---|---|
| Correction request submitted | Candidate | Request ID, data category, requested change, evidence |
| Request acknowledged (auto) | System | Acknowledgement sent, SLA start timestamp |
| Review started | Ops (Compliance Reviewer) | Reviewer identity, timestamp |
| Correction applied | Ops | Before value, after value, reviewer identity, timestamp — immutable |
| Correction rejected | Ops | Rejection reason, reviewer identity, timestamp |
| Candidate notified | System | Notification channel, delivery status |

**Part 5 IA Addition:**
```
Candidate Portal (Part 5.3) — add under section 6 (Dispute / DSAR):
├── 6.2 Right-to-Correction
│   └── Page: Right-to-Correction Request
│       Purpose: Candidate exercises DPDP Section 13 right to correct inaccurate data
│       RFP: 15.7 | DPDP: Section 13 | SLA: 30 days

Ops Portal (Part 5.1) — add to section 9.2 DSAR Management:
├── Right-to-Correction Sub-Queue (tab in 6.1.34 DSAR Management)
│   Purpose: Ops processes and tracks correction requests per DPDP Section 13
│   SLA: 30 business days | Audit: Immutable correction lineage record
```


### 6.1.35 Page: Data Retention Manager

**1. Page Objective**
Enforce configurable data retention policies — scheduled purge of expired cases, legal hold management, purge audit log.

**2. Primary Actors** Compliance Reviewer, Ops Admin

**3. Key Workflows**
Review approaching expiry → Legal hold check → Schedule purge → Execute (auto or manual) → Log purge event

**4. States**
Active (within retention period) | Expiring soon (within 30 days) | Scheduled for purge | Legal hold (exempt from purge) | Purged (record remains but data deleted)

**5. Tables**
- Retention Policy Table: Client | Check type | Country | Retention period (months) | Data scope
- Expiring Soon Table: Case ID | Candidate (anonymized) | Client | Expiry date | Legal hold (Y/N) | [Schedule Purge] [Apply Legal Hold]
- Purge Log: Purge date | Cases purged (count) | Data deleted | Rule applied | Executed by (system/user)

**6. Drawers**
- Legal Hold Drawer: Apply/remove legal hold — reason (active dispute / litigation / regulatory investigation) + expiry date for hold
- Purge Preview Drawer: "Purging Case [X] will delete: [list of data types]. Audit skeleton (case ID, anonymized timeline) will be retained per policy."

**7. Modals**
- Execute Purge Modal: "Purging [N] cases. This action is irreversible. [Confirm Purge]"

**8. Alerts/Banners**
- "[N] cases reach retention expiry in 30 days — review before automated purge"
- "Legal hold prevents purge for [N] cases"

---

### 6.1.36 Page: Ops User Administration

**1. Page Objective**
Manage ops team users — roles, access, workload, delegation, deactivation.

**2. Primary Actors** Ops Admin, Team Lead

**3. Key Workflows**
Add reviewer → Assign role + client access scope → Set delegation (if needed) → Deactivate (with open-case reassignment) → Manage temporary access

**4. Tables**
User Table: Name | Email | Role | Active cases | Last login | Status | Client access scope | [Edit] [Deactivate]

**5. Role Options**
Reviewer | Senior Reviewer | QC Reviewer | Adjudicator | Team Lead | Compliance Reviewer | Investigator | Ops Admin

**6. Drawers**
- Add/Edit User Drawer: Name, email, role, client access scope (which tenants visible), check type specialization
- Delegation Drawer: Delegate from User A to User B — duration (from/to date), scope (specific check types or all), reason

**7. Modals**
- Deactivate Modal: "Deactivating [User X] who has [N] active cases. Reassign cases to: [dropdown]. Confirm."
- Delegation Expiry Alert: Automatically notifies ops admin when delegation period ends

---

### 6.1.37 Page: Verification Check Configuration

**1. Page Objective**
Configure which check types are enabled, their routing rules, vendor assignment logic, and check-depth options.

**2. Primary Actors** Ops Admin

**3. Tables**
Check Type Config Table: Check type | Enabled (Y/N) | Default vendor routing rule | Check depth options | Country availability | Auto-assign (Y/N)

**4. Drawers**
- Check Config Edit Drawer: Per check type — routing rule (auto-assign logic), depth options (standard/enhanced), country availability toggles, SLA defaults
- Country Matrix Drawer: Which check types are available/enabled per country

---

### 6.1.38 Page: Notification Rules and Escalation Configuration

**1. Page Objective**
Configure which events trigger which notifications — to which roles — via which channels — and define escalation ladder.

**2. Primary Actors** Ops Admin

**3. Tables**
- Notification Rules Table: Triggering event | Recipient role | Channel (Email/SMS/WhatsApp) | Template | Delay (immediately/after N hours) | Active (Y/N)
- Escalation Ladder Table: Portal | SLA % elapsed | Notify role | Notification method | Auto-escalate (Y/N)

**4. Drawers**
- Rule Edit Drawer: Full rule configuration — event trigger + recipient + channel + template + timing + conditions
- Test Rule Drawer: Simulate a trigger event and preview what notification would be sent

**5. Modals**
- Deactivate Rule Modal: "Deactivating this rule means [event] will no longer trigger a notification for [recipient]. Confirm?"

---



---

## GAP-28 FIX: Continuous Monitoring Section — Operations Portal

### New Pages: 6.1.39 Active Monitoring Dashboard + 6.1.40 Drift Alerts Queue + 6.1.41 Re-Check Cases

**Part 5 IA Addition**
Add to Operations Portal IA (Part 5.1):
```
├── 11. CONTINUOUS MONITORING
│   ├── 11.1 Active Monitoring Dashboard
│   │   └── Page: Employees Under Monitoring
│   ├── 11.2 Drift Alerts Queue
│   │   └── Page: Identity Drift Alerts
│   └── 11.3 Re-Check Cases
│       └── Page: Triggered Re-Check Cases
```

**New Page: 6.1.39 Active Monitoring Dashboard**

**1. Page Objective**
Central visibility into all current employees under continuous screening — watchlist monitoring, periodic re-check schedules, identity drift monitoring.

**2. Tables**
Active Monitoring Table: Employee ID (anonymized) | Client | Monitoring type | Last screened | Next scheduled screen | Alert count | Risk trend | [View]

Monitoring Type breakdown:
- Watchlist (continuous): real-time sanctions/PEP rescreening
- Periodic re-check: schedule-based (annual/quarterly)
- Role-based: triggered by role change
- Post-adverse (rare): court-ordered monitoring

**3. Cards**
- "Active Monitoring Employees" count (by client)
- "New Alerts this week" count
- "Re-checks due this month" count
- "Expiring reports (next 30 days)" count

---

**New Page: 6.1.40 Drift Alerts Queue**

**1. Page Objective**
Review and action identity drift signals for existing employees — name changes, new watchlist hits, address anomalies, document expiry.

**2. Tables**
Alert queue: Alert ID | Employee (anonymized) | Client | Signal type | Detected date | HR response deadline (5 business days) | Status | [Review]

Signal types:
- Name change without declaration
- Sanctions/PEP watchlist hit post-joining
- ID document expiry (passport, work permit)
- Address change without update
- Biometric anomaly on re-verification
- New court record found

**3. Drawers**
- Alert Review Drawer:
  - Signal detail (what was detected, when, by which monitoring source)
  - Employee's current verified record vs new signal
  - HR decision prompt: [Accept with Documentation] [Investigate — Create Re-check Case] [Escalate to Risk/Legal]
  - Decision SLA: 5 business days from detection
  - [Notify HR Team] — sends structured alert to Client Admin with employee reference and signal type

**4. Alerts/Banners**
- "5 drift alerts approaching 5-day decision deadline" — amber
- "Sanctions hit detected for employee — immediate Risk/Legal escalation required" — red

---

**New Page: 6.1.41 Re-Check Cases**

**1. Page Objective**
Track and manage all re-verification cases triggered by continuous monitoring — showing which checks are being re-run and their status.

**2. Tables**
Re-check cases table: Re-check case ID | Original case ID | Client | Trigger type | Checks included (only delta checks) | Status | SLA | [View]

Trigger type display:
- Validity Expiry: "Original BGV expired [date] — full re-check"
- Role Change: "Promoted to [new role] — additional checks: [Criminal (Tier 4)]"
- Monitoring Hit: "Watchlist hit on [date] — targeted re-check: [Criminal/Identity]"
- Periodic: "Annual re-check — [package name]"

**Key Design Note**
Re-check cases run ONLY the delta checks (checks not already clear + not yet expired). The case workbench shows a "Re-check Mode" indicator: "This is a re-check case. Checks shown are only those requiring re-verification. Previous clear checks are preserved."

---
## 6.1 OPERATIONS PORTAL — Detailed Page Designs (Part B: Core Workbench & Verification Pages)


---


---

### 6.1.39 Page: Case Workbench (Central Verification Interface)
<!-- Previously numbered 6.1.1 in v4 — renumbered to avoid conflict with 6.1.1 Personal Work Queue -->

**1. Page Objective**
The most critical page in the platform. Centralizes all verification execution, adjudication, evidence review, AI signal review, communication, SLA management, and audit trail for a single case. Ops reviewers should rarely need to leave this page during a full case review cycle.

**2. Primary Actors**
Ops Reviewer (primary), Senior Reviewer, Adjudicator, QC Reviewer, Risk/Legal (read + approval)

**3. Key Workflows**
Check-by-check verification, insufficiency marking, vendor coordination, AI fraud review, adjudication decision, waiver request, pre-adverse/adverse notice generation, report trigger, dispute management, DSAR response initiation

**4. States**
New → In Progress → Pending Candidate → Pending Vendor → QC Review → Adjudication Pending → Report Generation → Completed / Escalated / Disputed / Closed

**5. Actions (Role-gated)**
- All roles: View case, view documents, view audit trail, add internal note
- Reviewer: Mark check verified, Mark insufficient, Flag discrepancy, Assign to vendor, Send communication, Upload evidence, **[Create Ticket] — raise ServiceNow/Jira ticket linked to this case (C-06 | RFP 13.9)**
- Senior Reviewer: All reviewer + Override AI flag (mandatory note), Set case priority
- Adjudicator: All above + Set final outcome, Generate report, Issue pre-adverse notice, Approve/reject waiver
- QC Reviewer: Tag QC error, Pass/fail QC — cannot change original outcome

**6. Data Blocks**
Case identity | Check inventory (all checks + status + SLA + AI flags) | Evidence store | AI signal stack | Discrepancy register | Vendor assignment log | Communication log | Consent record reference | Audit event stream

**7. UI Regions**
- Persistent top bar: Case ID, candidate, client, package, overall status badge, SLA master countdown, AI risk score badge, primary actions
- Left sidebar: Check navigation list (each with status icon + mini SLA countdown + AI flag dot)
- Center workspace: Active check verification interface (changes per selected check)
- Right context panel: Timeline / Communications / Documents / AI Signals / **Linked Tickets** / Audit (collapsible tabs) [Linked Tickets tab — C-06 | RFP 13.9]
- Context-aware bottom bar: Primary actions change based on check state
- Floating banner zone: Alerts rendered above center workspace

**8. Cards**
- AI Composite Risk Card: 0–100 gauge, color-banded zones, component drilldown (ID/Document/Behavioral/Employment/Device/Geo scores), trend vs prior cases
- SLA Health Card: Master deadline countdown, per-check color indicators
- Discrepancy Summary Card: Count by severity (Minor/Moderate/Major/Critical), resolution status, AI-recommended action
- Consent Validity Card: Status (Valid/Expired/Withdrawn), version, signed date, expiry
- Vendor Status Card: Vendor name, acknowledgment time, response deadline, SLA remaining

**9. Tables**
- Check Summary Table: Type | Status | Assigned | SLA | AI flags | Evidence count | Last action
- Discrepancy Table: ID | Type | Source check | Severity | Status | Detected by | Resolution
- Communication Log: Date | Channel | Recipient (role-masked) | Template | Delivery status
- Audit Event Table: Timestamp | Actor | Portal | Action | Affected field | Event hash
- Evidence Table: Name | **Format** | Type | Source | Date | AI quality score | Fraud flag | **Actions**
  - Format values: PDF / DOCX / XLSX / JPG / PNG / ZIP / ZIP-child
  - Actions column is format-specific (per platform policy 4.7.5):
    - PDF / JPG / PNG: [View]
    - DOCX / XLSX: [View as PDF] [Download Original]
    - ZIP (parent): [View Extracted Files] [Download ZIP] — expands inline to show all child document rows
    - ZIP (child): per-child format action + "Extracted from: [zip filename]" label

**10. Drawers**
- Evidence Review Drawer: Format-aware document viewer (per platform policy 4.7.5):
  - PDF / JPG / PNG: Full-width inline viewer; OCR overlay (bounding boxes + confidence); fraud signal overlay (highlighted anomaly regions); side-by-side with candidate-entered data, diff in yellow
  - DOCX / XLSX: Displays converted PDF with label: "Viewing converted PDF. [Download Original Word/Excel File]". OCR overlay and fraud detection run on converted PDF. Conversion quality noted: "Converted from .docx — formatting preserved."
  - ZIP (parent): Shows extracted files list — file name | format | size | AI quality | Fraud flag | [View] per file. Each child opens in its own format-appropriate viewer.
  - ZIP (child): Same viewer as its individual format (PDF/image/converted DOCX/XLSX), with breadcrumb: "← Back to ZIP: [filename.zip]"
- AI Signal Detail Drawer: Flag type, confidence %, reason codes (plain language), evidence links, model version, calibration history, override button (senior role only, mandatory note, audit-logged)
- Vendor Assignment Drawer: Filtered capability matrix (check type + geography); workload indicator; SLA projection; confirm assignment → auto-notifies vendor
- Communication Compose Drawer: Recipient type, channel, template, personalization preview, override edit, send now vs schedule, test send
- Waiver Request Drawer: Discrepancy selector, justification, evidence attach, approval tier, routing preview
- Insufficiency Drawer: Check selector, field-level remarks (specific not generic), channel selector, notification preview, confirm
- **Create Ticket Drawer [C-06 | RFP 13.9]:**
  ```
  CREATE EXTERNAL TICKET
  ─────────────────────────────────────────────
  Target system:   [ServiceNow ▼]  [Jira ▼]
  Ticket type:     [Incident ▼]
                   (Incident / Service Request / Change Request / Bug)
  Priority:        [P2 ▼]
  Title:           [KCheck — {case_id} — ] [ops edits]
  Description:     Pre-filled with: Case ID, client name, check types,
                   current status, SLA position, ops reviewer name,
                   direct link to this case in KCheck.
                   [Ops adds additional context in free text field below]
  Assignee group:  [Account Mgmt ▼] (from configured groups in 6.5.14)
  ─────────────────────────────────────────────
  [Submit to ServiceNow]   [Cancel]

  Note: Ticket will be linked to this case. Status visible in
        Linked Tickets tab. Case audit log will record ticket creation.
  ```

**11. Modals**
- Adjudication Outcome Modal: 5-option outcome selector; mandatory notes for non-Clear (UI + API enforced); evidence attach; pre-adverse trigger if Failed; reviewer identity capture; legal confirmation text; [Confirm with name and timestamp]
- Escalation Modal: Type (SLA/Fraud/Client/Legal), target (auto-suggested), note, urgency, confirm
- QC Error Modal: Error type dropdown, description, severity, route-back option, confirm
- Case Close Modal: Reason, outstanding items warning, client notification trigger, confirm
- Delete Evidence Modal: Reason required, supervisor approval required, "irreversible — logged" warning

**12. Tabs (Center workspace)**
Overview | Employment (N) | Education (N) | Identity/KYC | Legal/Criminal | Address | Financial | Reference | Documents | AI Signals | Communications | Audit

**Right context panel tabs (collapsible):**
- **Tab 1 — Timeline:** Chronological event stream (see Item 16)
- **Tab 2 — Communications:** All candidate/employer/vendor messages sent from this case
- **Tab 3 — Documents:** Quick-access document list (full detail in Evidence Table below)
- **Tab 4 — AI Signals:** All AI flags across all checks
- **Tab 5 — Linked Tickets [C-06 | RFP 13.9]:**
  ```
  LINKED TICKETS — Case KCHK-2026-09841
  ──────────────────────────────────────────────────────────
  INC0012345  ServiceNow  P2  SLA breach — Client X    🟡 In Progress
              Assigned: Account Mgmt | Created: 14-May 10:22
              [View in ServiceNow ↗]

  INC0012891  ServiceNow  P3  Vendor unresponsive        ✅ Resolved
              Resolved: 15-May 09:14 | Resolution: Vendor contacted
              [View in ServiceNow ↗]
  ──────────────────────────────────────────────────────────
  [+ Create New Ticket]

  No tickets? "No external tickets linked to this case."
  ```
  Status badges: 🟢 Open (unassigned) | 🟡 In Progress | ✅ Resolved | ⛔ Closed
  Ticket row: ticket ID | system | priority | title | status | last updated | [View in system ↗]
  Status syncs per configuration in 6.5.14 (webhook or polling)
  [+ Create New Ticket] → opens Create Ticket Drawer
- **Tab 6 — Audit:** Full audit event table (see Item 16)

**13. Filters**
- Documents: type, upload source, AI quality, fraud flag
- AI Signals: flag type, confidence level, check type, model
- Communications: channel, recipient type, date range, delivery status
- Audit: actor, action type, portal, date range

**14. Bulk Actions (from Case List)**
Assign reviewer | Assign vendor | Send reminder | Mark for QC | Escalate | Export | Update status

**15. Alerts/Banners (priority ordered)**
P1 Red: AI High-Confidence Fraud Flag | Consent Invalid | Major Discrepancy Auto-Detected
P2 Orange: SLA Breach Imminent (<2h) | Vendor Overdue | Waiver Approval Overdue
P3 Amber: Discrepancy Detected | QC Error Returned | Client Escalation Active
P4 Yellow: Notification Delivery Failure | SLA Pause Active | AI Override Pending

**16. Timeline/Audit Components**
Right panel Tab 1 — Event Timeline: Chronological, day-grouped. Per event: action icon, actor name + role badge + portal tag, timestamp (absolute + relative), action description, affected check/field, expandable for full detail, tamper-evident hash (last 8 chars visible; full hash in export). Hash integrity indicator: "Log integrity: Verified ✓".

**17. SLA Components [C-03 | RFP 1.7]**
Three-track SLA display — all three clocks visible simultaneously per case:
- **SLA Health Card (top bar):** Three status badges side-by-side:
  `[Client: 3d 4h ✅]  [Internal: 1d 2h ⚠️]  [Vendor: Overdue ❌]`
  Each badge: remaining time + color (Green / Amber / Red / Breached) + clock icon
  Click any badge → expands to show: SLA target, time elapsed, threshold crossings, pause history
- **Master countdown (top bar):** Client SLA countdown is the primary — DD:HH:MM, color transitions at configured Amber/Red thresholds
- **Per-check timers (left nav):** Mini countdown shows Client SLA per check. Hover shows all three tracks for that check.
- **Breach prediction tooltip (hover):** "Estimated completion: X hours. Predicted breach probability: 72% (Client SLA). Internal SLA already breached — 2d overdue."
- **SLA pause indicator:** Track-specific pause: "Client SLA paused — awaiting candidate re-submission since [date]." [Resume manually if auto-resume fails]
- **Escalation trigger log:** "Auto-escalation sent to [Team Lead] at 85% Client SLA elapsed." "Internal SLA breach — Team Lead notified."
- **Three-track interaction rules:** Per platform policy (6.1.27 Item 10) — clocks start/pause/breach independently

**18. AI Components**
- Composite Risk Score Widget: Gauge 0–100, hover for component breakdown, score trend (prior cases)
- AI Flag Panel (AI Signals tab): Per flag — type label, confidence %, evidence link, reason code (plain language), model version, override button
- Reviewer Assist Summary: Collapsible card, AI-generated: discrepancy list, key risks, suggested next action
- Discrepancy Severity Classifier: AI-suggested severity per discrepancy, human override logged

**19. Evidence Components**
- Document Viewer: Multi-page, zoom/pan/rotate, OCR overlay mode, fraud detection overlay mode
- Photo Evidence Map: GPS pin vs declared address on map, photo gallery, timestamp, accuracy radius
- Biometric Panel: Two-pane selfie vs ID face comparison, match score, liveness indicators
- Evidence Authenticity Badge: Per-document Authentic / Suspicious / Verified Manual; click for full detail

**20. Mobile Considerations**
- Approval-only mobile view: Adjudication + waiver approvals optimized for thumb navigation
- Push notifications for escalations with deep link
- Full verification execution intentionally desktop-only (evidence review quality requires screen real estate)

---



---

## GAP-5 FIX: Fraud Investigation State — Hard Freeze UI Enforcement

### Addition to 6.1.2 Case Workbench — State: Fraud Investigation (State 23)

**State Definition**
When a case enters State 23 (Fraud Investigation), the Case Workbench renders in a fundamentally different mode from all other states. This is not a soft disable — it is a hard UI + API enforcement.

**Hard Freeze UI Rules**
- Entire bottom action bar replaced with: "FRAUD INVESTIGATION IN PROGRESS — Standard ops actions suspended"
- [Generate Report] button: technically removed from DOM (not hidden, not grayed — not rendered at all). API endpoint POST /v1/reports/generate returns 403 for this case regardless of user role.
- [Mark Insufficient], [Assign Vendor], [Submit to QC], [Adjudicate] buttons: all removed from DOM
- Only permitted actions in freeze state:
  - [View Evidence] (read-only)
  - [View Audit Trail] (read-only)
  - [Add Fraud Investigation Note] (Fraud Reviewer role only)
  - [Resolve Investigation] (Fraud Reviewer role only — opens resolution modal)

**Full-Page Banner (persistent, non-dismissible)**
Red full-width banner at very top of page, above even the case header:
```
🔴 FRAUD INVESTIGATION ACTIVE
This case is under active fraud investigation. All standard verification, 
adjudication, and report operations are suspended until the investigation resolves.
Only the Fraud Reviewer can take action on this case.
Opened: [timestamp] | Assigned to: [Fraud Reviewer name]
```

**Left Panel (Check Navigator) in Freeze State**
- All check status indicators replaced with "⏸ Suspended" badge
- No check is clickable — click shows tooltip: "Check suspended during fraud investigation"

**Client Notification Display**
- Right panel shows auto-generated client notification sent on freeze: "Case [ID] for [Candidate] has been flagged for investigation. No report will be issued until the investigation is complete. [Timestamp delivered]."

**Fraud Investigation Resolution Modal (Fraud Reviewer only)**
Outcome selector:
- Fraud Confirmed → Case closes as Adverse. Pre-adverse workflow resumes automatically.
- Fraud Cleared — False Positive → Case unfreezes. Status returns to Adjudication In Progress. AI flag logged as false positive. Client notified.
- Unable to Determine → Case closes as Inconclusive. Legal team notified for next steps.

Mandatory fields: Investigation steps taken (free text), Evidence reviewed (document references), Final determination rationale.

**API Enforcement (beyond UI)**
Server-side: every state-modifying API call on a case in State 23 validates state before execution. If state = FRAUD_INVESTIGATION and the caller does not have FRAUD_REVIEWER role: HTTP 403 returned with error body: `{"error": "CASE_FROZEN", "message": "Case is under fraud investigation. Only Fraud Reviewer role can modify this case."}`. UI-level hard removal is secondary — API enforcement is primary.

**Audit Events**
- `fraud_investigation.opened` — trigger, AI flag details, opened by, timestamp
- `fraud_investigation.note_added` — Fraud Reviewer notes
- `fraud_investigation.resolved` — outcome, rationale, model version of triggering AI flag, false positive flag if cleared
- `fraud_investigation.client_notified` — client notification delivery confirmation

---


---

## GAP-9 FIX: Case States 22-24 in Case Workbench

### Addition to 6.1.2 Case Workbench — States Section (Item 4)

**Updated Complete State List (24 States)**

Add to Case Workbench States definition:

States 1-21 (existing — already defined). Adding:

**State 22 — On Hold / Paused by Client**
- Visual treatment: Amber dashed border around entire case workbench. Status badge: "⏸ On Hold"
- Banner: "This case has been paused by [Client Name] on [date]. [Reason: client-provided]. SLA timers are paused across all three tracks."
- All action buttons disabled EXCEPT: [View Case] [View Audit Trail] [Resume Case (Ops Admin or Client Admin)]
- Bottom bar: "Case is On Hold — contact client to resume or set auto-resume date"
- SLA treatment: All three SLA tracks paused. Pause reason logged. Resume restarts from pause point (elapsed time before pause preserved).
- Auto-exit: If no resume within 30 days → system auto-transitions to Closed — Withdrawn with client notification

**State 23 — Fraud Investigation** (Full specification in GAP-5 Fix above)
- Hard freeze. Detailed in GAP-5 section.

**State 24 — Re-Verification In Progress**
- Visual treatment: Blue border accent on disputed check(s) only. Non-disputed checks shown as read-only with lock icon. Status badge: "🔄 Re-Verification"
- Banner: "Dispute upheld. [N] check(s) are being re-verified: [check names]. Other checks are locked."
- Only disputed check workspaces are active — reviewer can take actions only on re-verification checks
- Non-disputed checks: evidence visible but all action buttons removed
- Adjudication cannot be completed until re-verification check reaches terminal state
- SLA: Re-verification has its own SLA timer (from dispute resolution date to re-verification completion) — shown as additional SLA row in SLA Card

**State Transition Rules (additions)**
Add to Case Workbench state transition logic:

| Transition | Permitted By | Condition |
|---|---|---|
| Any Active State → State 22 (On Hold) | Client Admin, KPMG Admin | Valid from: Invited, Pending Candidate, Pending Ops, Adjudication In Progress, Waiver Pending. NOT valid from: Fraud Investigation, Pre-Adverse, Closed states. |
| State 22 → Prior Active State | Client Admin, KPMG Admin | Manual resume action required. Auto-resume after 30 days → Closed Withdrawn. |
| Adjudication In Progress → State 23 | Fraud Reviewer, Senior Reviewer | Critical/Fraud classification. |
| State 23 → Adjudication In Progress | Fraud Reviewer only | Fraud Cleared outcome. |
| State 23 → Closed Adverse | Fraud Reviewer only | Fraud Confirmed outcome. |
| Dispute Received → State 24 | System | Dispute upheld, checks require re-run. |
| State 24 → Pending QC | System | Re-verification check(s) completed. |

**Visual State Indicator Update**
Case list rows (6.1.4 Master Case Registry) — add state color coding:
- State 22 (On Hold): Row background amber tint, "⏸ On Hold" badge
- State 23 (Fraud Investigation): Row background red tint, "🔴 Fraud Investigation" badge — restricted visibility (only Fraud Reviewer and Ops Lead see this row; TA/HR do not)
- State 24 (Re-Verification): Row background blue tint, "🔄 Re-Verification" badge

---


---

## GAP-6 FIX: Entity Graph Viewer

### Addition to 6.1.2 Case Workbench — AI Signals Tab + New Drawer

**Entity Graph Panel in AI Signals Tab**

Add as final section in AI Signals tab (after existing flag panels):

```
ENTITY GRAPH LINKS
─────────────────────────────────────────────────────────────
[N] connections found to other cases or known entities.

Type                  Connection           Confidence   Cases
Shared device         Same device ID       High (94%)   3 cases
Shared address        Same IP geo-block    Medium (71%) 1 case  
Shared document hash  Same PAN image hash  High (87%)   2 cases
─────────────────────────────────────────────────────────────
⚠️ 2 of the linked cases had adverse outcomes.
[View Entity Graph]
```

**Entity Graph Viewer Drawer**

[View Entity Graph] opens full-screen drawer:

Visual network graph (D3.js or similar):
- Center node: current candidate (circle with case ID)
- Connected nodes: other cases (labeled with outcome color — green/amber/red)
- Edge labels: connection type (shared device / shared address / shared document / shared ID fragment)
- Edge thickness: proportional to confidence score
- Node click: shows case summary card (case ID, outcome, date, check types run)

Text list view toggle (for accessibility):
- Table: Entity type | Connection type | Linked case ID | Linked case outcome | Confidence | [View Linked Case (if authorized)]

**Filters**
- Connection type: Device | Address | Document | ID Fragment
- Confidence threshold: High only | Medium+ | All
- Date range: linked cases created within last [N] months

**Privacy Controls**
- Linked case IDs shown only if reviewer has access to that tenant (multi-tenant cases: shows "Case in another organization — ID redacted" — no cross-tenant case exposure)
- Only entity connection type and outcome shown for restricted cases — no candidate identity data from other cases

**Alerts/Banners in Entity Graph Drawer**
- "This candidate shares a device with [N] cases that had adverse outcomes — elevated fraud risk signal." — red
- "No adverse links found — entity graph connections appear incidental." — green

**Part 5 IA Addition**
Add to Case Workbench AI Signals section:
```
└── Entity Graph Panel
    └── [View Entity Graph] → Entity Graph Drawer
        Visual network: current case + connected cases via shared signals
        Connection types: Device | Address | Document hash | ID fragment
        Outcome coloring: Green/Amber/Red per connected case
        Privacy: cross-tenant cases shown as redacted
```

---

---

## GAP-EXP-M8 FIX: Cross-Entity Navigation — Hyperlinked Navigation (All Portals)

### M-8 | Cross-Entity Navigation (Hyperlinked Navigation) — Not Specified at Design Depth

**RFP Reference:** RFP 19.11

**RFP Text:**
> *"Hyperlinked Navigation — Between cases, related records, and relevant pages"*

**Verdict:** EXPLICIT

**Analysis:**
RFP 19.11 explicitly names "Hyperlinked Navigation" as a requirement covering cases, related records, and relevant pages. This is a UI/UX specification requirement that must be reflected in the design depth of key pages (Case Workbench, Case Lists, Dashboard drill-downs, Vendor Performance, Check Cards). Its absence means frontend developers have no specification for which entities should be hyperlinked, what hover state they display, and where the link navigates. The result is an inconsistent navigation model where some items are clickable and others are not — a common usability failure in enterprise applications built without explicit navigation specifications.

**Impact:**
- Ops reviewers waste significant time navigating between cases, vendor records, and candidate profiles by manually using the search function instead of direct hyperlinks.
- Client portal users cannot drill from aggregate analytics to individual case detail without manual navigation.
- Cross-portal navigation (Ops → referencing vendor record linked to a case) is undefined.

**Recommendation:**
Add a cross-entity navigation specification to the design depth of all major case-facing pages in Part 6.

---

### Addition to Multiple Pages — Cross-Entity Navigation Specification

**Standard Hyperlink Behaviour (applies to all linked entities below):**

- **Visual style:** Underlined on hover; standard link colour (configurable per portal theme)
- **Hover state:** Tooltip showing destination entity summary (e.g., hover over Case ID → mini card showing candidate name, package, current status, SLA health)
- **Navigation behaviour:** Opens in current tab (within same portal) or new tab (cross-portal navigation, with explicit icon indicator)
- **Mobile:** Tappable with sufficient tap target (44px minimum)
- **Keyboard:** Tab-navigable; Enter/Space activates link

**Cross-Entity Navigation Map:**

| Source Entity | Source Page | Linked Element | Destination Page | Navigation Type |
|---|---|---|---|---|
| Case ID | All Cases (Ops) | Case reference number | Case Workbench | Same tab |
| Case ID | Client Case List | Case reference number | Case Detail (Client View) | Same tab |
| Candidate ID | Case Workbench | Candidate name/ID | Candidate history (if repeat) | Same tab |
| Check status icon | Case Workbench | Individual check badge | Check workspace (Employment/Education/etc.) | Same tab |
| Vendor name | Case Workbench | Vendor assignment panel | Vendor Performance page | Same tab |
| Vendor name | Assignment Console | Vendor name in table | Vendor Profile / Performance | Same tab |
| Case reference | Vendor Assignment Queue | Case reference | Case Workbench (Ops) | Same tab |
| Report reference | Report Archive | Report ID | Report preview | Same tab |
| SLA breach case | SLA Monitor | Breached case row | Case Workbench | Same tab |
| Fraud flag | Fraud Intelligence Dashboard | Case reference in flags table | Case Workbench | Same tab |
| Dispute reference | Dispute Workbench | Related case | Case Workbench | Same tab |
| Candidate in dispute | Dispute Workbench | Candidate name | Case Workbench | Same tab |
| DSAR request | DSAR Management | Related case | Case Workbench | Same tab |
| Correction request | Right-to-Correction Queue | Related case | Case Workbench | Same tab |
| Invoice case ref | Billing Dashboard | SLA penalty case | Case Workbench (Ops, read-only for client) | New tab (cross-portal) |
| BU breakdown | Client Analytics | BU name | Filtered Case List for that BU | Same tab |
| QC case | QC Queue | Case reference | QC Review Drawer | Same tab |
| Escalation case | Escalation Queue | Case reference | Case Workbench | Same tab |

**Addition to 6.1.39 Case Workbench (Item 19 — Hyperlinked Navigation Specification):**

```
19. HYPERLINKED NAVIGATION (RFP 19.11)

All entity references in the Case Workbench must be hyperlinked as follows:

CASE HEADER:
• Case ID: not linked (already on this case's page)
• Client name: links to Client Analytics filtered to this client
• Package name: links to Package detail in Super Admin (new tab)

CHECK NAVIGATOR (left panel):
• Each check type badge: links to its dedicated check workspace
  (Employment → 6.1.8, Education → 6.1.9, KYC → 6.1.10, etc.)

VENDOR PANEL:
• Vendor name: links to Vendor Performance Dashboard (6.1.20)
• Assigned vendor agent: links to Vendor Team view (if accessible)

DISCREPANCY TABLE:
• Case cross-references (if related case flagged): links to that case
• Document references: links to Document Viewer

SLA CARD:
• SLA configuration name: links to SLA Policy Editor (6.1.27)
• Escalation matrix: links to Escalation Resolution Log (6.1.28)

AUDIT TRAIL:
• Actor names: links to Ops User profile (if same portal)
• Related case references: links to that case

DISPUTE WORKBENCH (6.1.42):
• Related case: link to Case Workbench for that case
```

**Addition to 6.2.3 Case Detail — Client View (hyperlinked navigation):**

```
CLIENT-SIDE HYPERLINKED NAVIGATION:

• Case stage icons: each stage links to its detail drawer
• Assigned report: links to Report Inbox (filtered to this report)
• SLA countdown: links to SLA explanation tooltip (not a full page)
• Client billing: "View this case in billing" → Billing Dashboard filtered to this case
• Package name: links to Package detail (read-only view in Client Portal)
```


### 6.1.40 Page: Live SLA Dashboard
<!-- Previously numbered 6.1.2 in v4 — renumbered to 6.1.40 -->

**1. Page Objective**
Enable proactive SLA management across entire caseload — detect and act before breach, not after.

**2. Primary Actors** Team Lead, Ops Manager, SLA Governance role

**3. Key Workflows**
Monitor breach risk → Prioritize assignment → Trigger escalations → Analyze breach root causes → Configure SLA rules

**4. States (per case)**
On Track (Green) | At Risk (Amber, <30% time) | Critical (Red, <10%) | Breached | Paused (notification failure / candidate unresponsive)

**5. Actions**
Open case from SLA table, bulk assign urgent cases, manually escalate, view pause log, drill into breach root cause

**6. Data Blocks**
Per-case SLA state, breach prediction score, pause reason + duration, escalation trigger log, vendor contribution to breach, client-specific SLA tier

**7. UI Regions**
- Top KPI strip (clickable): Green count / Amber count / Red count / Breached count / Paused count
- Left: SLA distribution donut + today's compliance rate card
- Center: Live SLA countdown table (most urgent first, auto-refreshing 60s)
- Right: AI breach prediction panel ("12 cases likely to breach in 4h")
- Bottom: Historical SLA trend charts

**8. Cards**
- "Breach in 4 Hours" urgency card: count + [View & Act] button
- "SLA Paused" card: count + reason distribution (notification failure vs unresponsive)
- "Today's Compliance Rate" card: % completed within SLA today vs 7-day avg

**9. Tables**
- Live SLA Table: Case ID | Client | Check type | Reviewer | Deadline | Time Remaining | Health | Breach probability | [Open]
- Paused SLA Table: Case ID | Pause reason | Paused since | Resume condition | SLA days lost

**10. Drawers**
- Breach Detail Drawer: Selected case — check type history, current velocity, vendor status, recommended action
- SLA Config Drawer: Quick-edit SLA thresholds (ops admin role only)

**11. Modals**
- Bulk Escalation Modal: Select all cases in Red → assign escalation target → confirm

**12. Filters**
Client (multi-select) | Check type | Reviewer | SLA tier | Pause status | Geography

**13. SLA Components**
- Live countdown timers (auto-refresh)
- Predictive breach model: trained on historical velocity, check type, vendor TAT, time of day
- SLA pause/resume log (full history per case accessible from table)
- Escalation trigger log (which rules fired, when, to whom)
- Client-specific SLA tier label (different clients have different SLA agreements)

**14. AI Components**
- Predictive breach probability (per case): model considers current velocity + check complexity + vendor history
- Anomaly detection: Cases falling behind expected velocity flagged earlier than threshold-based rules
- "Top 3 breach contributors this week" insight card (AI-derived pattern)

**15. Alerts/Banners**
- "14 cases predicted to breach in 4 hours" — orange, [View & Act] button
- "Vendor [X] has 3 overdue cases — escalate now" — orange, [Contact Vendor] button
- "SLA compliance rate dropped below 90% today" — amber, trend link

**16. Timeline/Audit**
Escalation trigger log (per-row expandable): when auto-escalation fired, rule that triggered it, who was notified, outcome

**17. Mobile Considerations**
- Primary mobile use: manager checking status from phone
- Mobile shows simplified card view (not full table)
- Red/Critical cases shown first as alert cards
- One-tap escalation from mobile

---



---

## GAP-2 FIX: Three-Track SLA Display

### Addition to 6.1.2 Case Workbench — SLA Card (Item 8) and 6.1.3 Live SLA Dashboard

**Case Workbench — Updated SLA Card**

Replace single SLA countdown with three-track SLA display:

```
SLA STATUS
─────────────────────────────────────────────────
CLIENT SLA    [██████░░░░] 62% remaining
              Deadline: 15 Jan 2025 18:00 IST
              5 days 14 hours remaining
              Holiday calendar: Client (Mumbai)

INTERNAL SLA  [████░░░░░░] 41% remaining  
              Deadline: 13 Jan 2025 17:00 IST
              3 days 13 hours remaining
              Holiday calendar: KPMG India

VENDOR SLA    [█░░░░░░░░░] 14% remaining  ⚠️
              Deadline: 11 Jan 2025 12:00 IST
              1 day 8 hours remaining
              Holiday calendar: Vendor (Delhi)
              Vendor: [Assigned vendor name]
─────────────────────────────────────────────────
SLA Paused: No  |  Pause Events: 0
```

Color per track independently:
- Green: > 50% remaining
- Amber: 20-50% remaining
- Red: < 20% remaining
- Grey strikethrough + "BREACHED": 0% remaining
- Pause indicator: "⏸ PAUSED — [reason]" replaces countdown when paused

**Per-Check SLA in Left Navigator**
Each check in left nav panel shows three mini-indicators (tiny colored dots):
- Client SLA dot | Internal SLA dot | Vendor SLA dot
- Tooltip on hover: "[Check type] — Client: 3d remaining | Internal: 1d remaining | Vendor: ⚠️ Breached"

**Insufficiency SLA Pause Indicator**
When SLA is paused:
```
CLIENT SLA    ⏸ PAUSED
              Paused since: 10 Jan 2025 14:32 IST
              Reason: Candidate insufficiency — awaiting re-submission
              Days paused: 3
              [Resume on candidate re-submission: automatic]

INTERNAL SLA  ⏸ PAUSED  
              [same pause info]

VENDOR SLA    ⏸ PAUSED
              [same pause info]
```

**Live SLA Dashboard — Three-Track View (6.1.3)**
Add to Live SLA Dashboard:
- Filter toggle: "View by: [All Tracks] [Client SLA] [Internal SLA] [Vendor SLA]"
- When "All Tracks" selected: table shows three colored SLA columns per row
- When specific track selected: single countdown column + breach indicator for that track only
- Breach attribution section: "This week's breaches by track — Client: 2 | Internal: 5 | Vendor: 8" (different tracks breach independently — actionable insight)
- "Vendor-caused client SLA risk" panel: cases where vendor SLA breached and client SLA is now at risk

---
### 6.1.41 Page: QC Sampling Queue
<!-- Previously numbered 6.1.3 in v4 — renumbered to 6.1.41 -->

**1. Page Objective**
Execute second-level quality review on sampled completed verifications — catch errors before client delivery and maintain long-term accuracy standards.

**2. Primary Actors** QC Reviewer (read + flag only — cannot modify original outcome)

**3. Key Workflows**
Select case for QC → Review evidence and original outcome → Pass or flag error → If error: classify, route back to reviewer with feedback → Track correction → Pass QC → Approve for report

**4. States**
Selected for QC → QC In Progress → QC Passed → QC Failed (returned to reviewer) → Corrected and resubmitted → QC Passed (2nd attempt) → Report Approved

**5. Actions**
Open case for QC, tag error, classify error type, pass/fail, route feedback to reviewer, view reviewer correction, final approve

**6. Data Blocks**
Case ID + check type, original reviewer's outcome and notes, evidence, AI signals for this case, QC reviewer identity, error classification, resolution outcome

**7. UI Regions**
- Left: QC queue list (sortable by sampling reason, check type, reviewer)
- Center: QC review workspace — side-by-side: original outcome vs evidence
- Right: Error tagging panel + feedback composition

**8. Cards**
- QC metrics card: Pass rate this week / Top error types / Reviewer accuracy trend
- "Returned to Reviewer" card: Cases awaiting reviewer correction + SLA impact

**9. Tables**
- QC Queue: Case ID | Check type | Original Reviewer | QC Reviewer | Sampling reason | Status | QC deadline
- QC History: Case ID | Outcome | Error type | Resolution time | Reviewer score impact

**10. Drawers**
- QC Review Drawer: Side-by-side — left: original reviewer's outcome + notes. Right: evidence (documents, employer response, AI signals). Option: "Blind QC" mode — QC reviewer sees evidence before seeing original outcome (configurable)

**11. Modals**
- Error Tag Modal: Error type (Data accuracy / Process deviation / Evidence quality / Adjudication error) | Description | Severity (Minor/Major) | Route back (Y/N, with note to reviewer)
- QC Pass Modal: "Confirm QC pass — case approved for report generation"

**12. Filters**
Check type | Original Reviewer | Sampling reason (Random / Risk-triggered / Client-requested / New reviewer) | QC Status | Date range

**13. Bulk Actions**
Bulk assign QC reviewer | Bulk mark for sampling | Bulk export QC report

**14. AI Components**
- Smart sampling: AI prioritizes cases with lower reviewer confidence, higher AI signal activity, or new reviewer for QC sampling — not purely random
- Error pattern detection: "Reviewer X has 3x higher OCR data mismatch errors this week — recommend training"

**15. SLA Components**
QC turnaround target (internal SLA — cases should not sit in QC > N days); QC deadline per case displayed

**16. Alerts/Banners**
- "QC backlog: 34 cases pending review > 48h" — amber banner
- "Reviewer [X] has elevated error rate this week — flagged for team lead review"

**17. Timeline/Audit**
QC event added to case audit timeline: "QC Review — [Passed / Failed: error type] — by [QC Reviewer] — [timestamp]"

**18. Mobile Considerations**
QC review is desktop-only — document evidence comparison requires screen space. QC Reviewer receives push notification for new QC assignments.

---



---

## GAP-7 FIX: QC Color Matrix Panel

### Addition to 6.1.3 QC Sampling Queue — QC Review Drawer

**Color Matrix Reference Panel in QC Review Drawer**

Add collapsible side panel to QC Review Drawer:

```
[▼ Color Matrix Reference — Client: Acme Corp]

Finding                              Assigned Color  Matrix Rule
Employment: date diff < 1 month      AMBER          Minor discrepancy
Employment: date diff 1-6 months     YELLOW         Moderate discrepancy
Employment: date diff > 6 months     RED            Major discrepancy
Education: institution unrecognized  YELLOW         Moderate — role dependent
Criminal: spent conviction           GREEN          Rehabilitated — standard roles
Criminal: pending case              YELLOW          Ongoing — adjudicator review
─────────────────────────────────────────────────────
Current case overall color: AMBER
Assigned by: [Adjudicator name] — [timestamp]
Matrix version applied: v3 (active since 01-Dec-2024)

[View Full Matrix] [Open in New Tab]
```

**Color Code Mismatch Error Tag**

Add to QC Error Tag dropdown (6.1.3 Item 11 Modals):
```
Error Type: Color Code Mismatch
Description: The color assigned does not match the client's configured 
             color matrix for this finding type and severity.
             
Finding: [auto-populated from case]
Assigned color: [auto-populated]
Matrix rule suggests: [auto-populated from matrix]
Specific note (mandatory): ___________________________
```

**QC Pass Rate Addition**
QC metrics card (6.1.3 Item 8 Cards): add "Color Code Accuracy Rate: [%]" — percentage of QC reviews where color was correct on first pass.

---
### 6.1.42 Page: Dispute Workbench
<!-- Previously numbered 6.1.4 in v4 — renumbered to 6.1.42 -->

**1. Page Objective**
Manage DPDP/GDPR-mandated candidate dispute and data subject request resolution within legally required timelines.

**2. Primary Actors** Compliance Reviewer (primary), Risk/Legal (escalated disputes)

**3. Key Workflows**
Dispute intake → Acknowledge (starts legal clock) → Assign investigator → Investigate (review case data vs candidate claim) → Decision → Notify candidate → Archive in compliance log

**4. States**
Received → Acknowledged → Under Investigation → Escalated to Legal → Decision Made → Notified → Closed

**5. Actions**
Acknowledge dispute, assign investigator, view original case data, review candidate claim + evidence, make decision (Upheld/Partial/Rejected), write resolution note, notify candidate, escalate to legal, close

**6. Data Blocks**
Original case data (what KPMG verified, adjudication notes), candidate's disputed claim, candidate's supporting evidence, DPDP response deadline, investigation notes, resolution outcome, notification delivery record

**7. UI Regions**
- Left: Dispute registry list (sorted by DPDP deadline urgency)
- Center: Investigation workspace — two panes (KPMG findings | Candidate claim)
- Right: Resolution panel + legal clock

**8. Cards**
- "DPDP Deadline" countdown card: Days remaining for each open dispute
- "Overdue Disputes" alert card: Count of disputes past DPDP deadline (should always be 0)
- "DSAR vs Dispute" distribution card: What proportion are erasure/access/correction vs outcome challenge

**9. Tables**
- Dispute Registry: Dispute ID | Case ID | Type | Filed date | DPDP deadline | Days remaining | Assigned to | Status | Escalated
- DSAR Registry: DSAR ID | Type | Filed date | Response deadline | Data package status | Delivered

**10. Drawers**
- Investigation Drawer: Full case data visible (original adjudication notes, AI signals, evidence) vs candidate's claim. Diff panel where candidate disputes specific data point.
- DSAR Data Package Drawer: All data held for this candidate — structured export preview before delivery

**11. Modals**
- Decision Modal: Outcome (Upheld / Partially Upheld / Rejected) + mandatory rationale + candidate notification text preview + [Confirm and Notify Candidate]
- Escalate to Legal Modal: Reason + legal team member selection + urgency + note
- Erasure Confirmation Modal: Legal hold check — "This candidate is involved in [active case / pending dispute]. Erasure may not be permissible until resolved." Override requires legal sign-off.

**12. Tabs**
Disputes | DSARs — Access Requests | DSARs — Erasure Requests | DSARs — Correction Requests | Resolved / Closed

**13. Filters**
Dispute type | Status | Assigned to | DPDP deadline risk (< 7 days / < 3 days / Overdue) | Date range

**14. SLA Components**
- DPDP 30-day response clock (hard deadline, non-adjustable)
- Countdown visible in table row and case header
- Overdue dispute = immediate P1 alert to Compliance Lead
- DSAR 30-day response clock (same mechanics)

**15. AI Components**
None direct — AI signals from the original case are made available in the investigation workspace for context

**16. Alerts/Banners**
- "DPDP deadline in 3 days for 2 disputes" — orange urgent banner
- "1 dispute is overdue — immediate action required" — red banner with direct [Open] link
- "Legal hold prevents erasure for Case [X]" — amber informational banner

**17. Timeline/Audit**
Every dispute action is an audit event: filed, acknowledged, assigned, investigated, decided, notified, closed — all with actor + timestamp. This is the primary DPDP grievance redressal log.

**18. Mobile Considerations**
Compliance reviewers may need to acknowledge disputes on mobile (especially near DPDP deadline). Acknowledgment action and escalation must be mobile-accessible. Investigation (full review) is desktop-primary.

---



---

## GAP-8 FIX: GDPR Article 18 Processing Restriction on Dispute

### Addition to 6.1.4 Dispute Workbench — GDPR Article 18 Auto-Enforcement

**Jurisdiction Auto-Detection at Dispute Receipt**
When a dispute is filed, the system reads the case's `residency_region`. If `residency_region` is in EU/EEA countries: GDPR Article 18 processing restriction is automatically applied before any ops action.

**Processing Restriction Flag**
- DB flag: `case.gdpr_article18_restriction = TRUE` set atomically with dispute record creation
- This flag blocks: new employer outreach initiation, new vendor assignments, new AI checks on this case, new document collection requests
- Does NOT block: reading existing evidence, completing already-in-progress vendor assignments (these continue under GDPR Article 18(1)(c) — establishment/defence of legal claims), generating audit pack

**Case Workbench — GDPR Restriction Banner (EU cases only)**
Persistent amber banner added to Case Workbench when `gdpr_article18_restriction = TRUE`:
```
⚠️ GDPR Article 18 — Processing Restricted
An active dispute has applied a processing restriction under GDPR Article 18.
No new data processing operations may be initiated on this case until the dispute is resolved.
Dispute filed: [date] | DPDP/GDPR response due: [30-day deadline]
[View Dispute] [View Article 18 Guidance]
```

**Blocked Action Indicators**
When a reviewer attempts to take a blocked action (initiate new outreach, assign new vendor), the button is disabled with tooltip: "Action blocked — GDPR Article 18 processing restriction active. Resolve the dispute to re-enable."

**Dispute Workbench — Jurisdiction Display**
Add to Dispute Detail Drawer:
- Jurisdiction badge: GDPR (EU) / DPDP (India) / FCRA (US) — auto-detected from residency_region
- Processing restriction status: Active (if EU) / Not Applicable (India/US — different rights apply)
- DPA contact (for EU): supervisory authority contact pre-populated based on client's EU establishment country
- Candidate rights notice language: served in EU language of residency country (German for DE residents, French for FR residents)

**FCRA Jurisdiction Additional Enforcement**
For US-resident candidates (FCRA scope):
- Employer furnisher notification: on dispute receipt, system auto-generates outreach to the employer whose information is disputed, notifying them of the dispute (FCRA furnisher notification requirement). Shown in Dispute Detail Drawer as "Furnisher Notified: [employer name] — [timestamp]."
- Adverse action blocked: if case is in Pre-Adverse Issued state and dispute received — adverse action finalization button disabled. Banner: "Adverse action suspended — active FCRA dispute in progress."

**Resolution — Article 18 Lift**
On dispute resolution (Upheld / Rejected / Partially Upheld):
- `gdpr_article18_restriction` flag cleared automatically
- Case Workbench restriction banner removed
- Ops reviewer notified: "Processing restriction lifted — normal case operations resumed."
- If Upheld: case enters Re-Verification state (State 24) for disputed checks

**Audit Events**
- `dispute.gdpr_article18_restriction_applied` — auto on EU dispute receipt
- `dispute.gdpr_article18_restriction_lifted` — on resolution
- `dispute.fcra_furnisher_notified` — for FCRA cases

---
## 6.2 CLIENT PORTAL — Detailed Page Designs (Part A: Core Case & Report Pages)


---

### 6.2.1 Page: Case Initiation Wizard

> **C-01 UPDATE — RFP 10.1, 13.1:** This wizard now supports two initiation modes.
> Mode 1 (Invite Candidate): existing flow. Mode 2 (Enter Data Directly): non-candidate flow
> where client HR supplies all data — no candidate portal involvement. Legacy source: PPTX "Portal Access"
> path of 50% manual entry. RFP 10.1 "Request" precedes "invite" — invite is not mandatory.

**1. Page Objective**
Enable HR/TA users to create individual BGV cases via two modes: (a) invite the candidate to fill their own data, or (b) enter all candidate data directly without any candidate portal involvement.

**2. Primary Actors** Client Initiator (HR, TA), Client Admin

**3. Key Workflows**
- **Standard flow:** Package selection → Mode selection (Invite) → Candidate contact entry → Duplicate check → Confirm and invite
- **Non-candidate flow:** Package selection → Mode selection (Direct Entry) → Full data entry → Document upload → Consent declaration → Submit to ops

**4. States**
- Standard: Step 1 (Package) → Step 1B (Mode) → Step 2 (Candidate Contact) → Step 3 (Duplicate) → Step 4 (Review) → Confirmed | Cancelled
- Non-candidate: Step 1 (Package) → Step 1B (Mode) → Step 2 (Full Data Entry) → Step 3 (Duplicate) → Step 4 (Consent Declaration) → Confirmed | Cancelled

**5. Actions**
Select package, select initiation mode, enter candidate details, acknowledge duplicate alert, confirm and send (standard) or confirm and submit to ops (non-candidate), cancel, go back (preserves state)

**6. Data Blocks**
- Available packages (from tenant configuration)
- Initiation mode flag (invite_candidate / client_direct_entry)
- Standard: candidate contact details only (name, email, mobile)
- Non-candidate: full candidate profile (personal, employment, education, identity)
- Document uploads (non-candidate mode only)
- Consent declaration text and acknowledgement (non-candidate mode only)
- Requisition reference, duplicate check result, invitation delivery channels

**7. UI Regions**
- Progress indicator (top): Steps 1–4 with current step highlighted; step labels change based on mode selected
- Center: Current step content
- Right sidebar: Package summary (persists through steps 2–4 once selected)
- Bottom: Back / Next / Confirm navigation buttons

**8. Cards**
- Package Card (Step 1): Name, included checks (icon list), estimated TAT, cost preview, [Select] button. Selected state: highlighted border.
- Package Comparison Card (drawer from "Compare" link): Side-by-side check type matrix for all packages
- Mode Selection Card (Step 1B — NEW):
  - "Invite Candidate" card: "Candidate fills their own details via a secure portal link"
  - "Enter Data Directly" card: "You provide all candidate data — no portal link sent to candidate"
- Duplicate Alert Card (Step 3): Previous case summary (date, package, outcome color) with decision options
- Consent Declaration Card (Step 4 — non-candidate mode NEW): Declaration text with e-sign / acknowledgement checkbox
- Invitation Preview Card (Step 4 — standard mode): Shows which channels will be used

**9. Tables**
- Package Comparison Table (in drawer): Package name vs check types included — tick/cross matrix
- Non-candidate mode: Employment History table (add / edit / remove rows per employer)
- Non-candidate mode: Education table (add / edit / remove rows per qualification)

**10. Drawers**
- Package Comparison Drawer: Full comparison of all packages
- Country-specific info drawer: "For this country, additional checks are included"
- Non-candidate mode: Full form drawer per section (Employment, Education, Identity — expandable)

**11. Modals**
- Mode Warning Modal (when "Enter Data Directly" selected): "You are submitting candidate data on their behalf. Ensure you have written or verbal consent from the candidate before proceeding." [I understand — continue] [Cancel]
- Duplicate Confirmation Modal: Previous case details. Options: [Use Previous Report] [Initiate Fresh Verification] [Cancel]
- Confirmation Modal (Step 4 — standard): Full summary — candidate, package, estimated TAT, cost. [Confirm & Send Invitation]
- Confirmation Modal (Step 4 — non-candidate NEW): Full data summary. "No invitation will be sent. Case will go directly to KPMG ops." [Confirm & Submit to KPMG]

**12. Tabs** None — linear wizard; mode determines which form fields appear

**13. Filters** None — wizard flow

**14. Bulk Actions** None — single case wizard (see Bulk Upload page 6.2.2 for batch; Tab 2 for pre-filled batch)

**15. Alerts/Banners**
- Package mismatch: "This package does not include criminal check — continue?" (non-blocking warning)
- Missing contact (standard mode): "Neither email nor mobile provided — invitation cannot be sent until one is added"
- Country mismatch: "Package [X] is not configured for [Country]. Please select a valid package."
- Non-candidate mode: "No candidate email provided — candidate will not receive any system notifications" (amber, non-blocking)
- Non-candidate mode: "Consent declaration is mandatory before submitting on behalf of a candidate" (red, blocking)

**16. Timeline/Audit**
Case creation event logged with: creating user, client tenant, package selected, initiation_mode (invite_candidate OR client_direct_entry), candidate contact details hash, consent declaration acknowledgement (non-candidate mode). Duplicate check result logged.

**17. SLA Components**
Step 4 shows estimated TAT range. Standard mode: "Invitation will be sent immediately." Non-candidate mode: "Case will be reviewed by KPMG ops within [N] business hours."

**18. AI Components**
Duplicate detection (hash-based, catches near-duplicate entries like name typos)

**19. Evidence Components**
Non-candidate mode only: Document upload panel in Step 2 (employment/education/identity docs uploaded by client HR on behalf of candidate)

**20. Mobile Considerations**
- Standard mode: fully mobile-functional (HR on mobile is very common)
- Non-candidate (full data entry) mode: mobile-supported but desktop-recommended due to volume of fields
- Package cards: large tap targets (min 44px), scrollable horizontal card strip on mobile
- Step indicator: condensed on mobile (dots not full labels)
- Keyboard auto-advance on OTP-style fields
- Confirmation screen: shareable link to case for HR to share with manager

---

### 6.2.2 Page: Bulk Case Upload

> **C-01 UPDATE — RFP 10.15, 13.1:** Page now has two tabs.
> Tab 1 (existing): Bulk invite — uploads candidate list, sends invitations.
> Tab 2 (new): Bulk pre-filled data — uploads complete candidate data, no invitations sent.
> Legacy source: PPTX "50% Manual Entry via Excel". RFP 13.1 "pre-filled candidate details, reducing manual data entry".

**1. Page Objective**
Allow HR Admin to initiate 10–500+ candidate cases in one upload — either by inviting candidates to fill their own data (Tab 1) or by supplying complete pre-filled candidate data with no candidate portal step (Tab 2).

**2. Primary Actors** Client Admin, HR Operations

**3. Key Workflows**
- Tab 1 (Bulk Invite): Download template → Fill invitation data → Upload → Validate → Confirm → Invitations sent
- Tab 2 (Bulk Pre-filled): Download extended template → Fill complete candidate data → Upload → Validate → Consent confirm → Submit to ops

**4. States**
Template Downloaded → File Uploaded → Validating → Validation Complete (all valid / partial errors) → Confirmed → Processing → Results Available

**5. Actions**
Select tab (mode), download template, upload file, review errors, download error-only file, re-upload corrections, proceed with valid rows, confirm, download results

**6. Data Blocks**
- Tab 1: Name, email, mobile, package, BU, country (invitation-only fields)
- Tab 2: Full candidate profile per row (personal, employment, education, identity) + ConsentObtained column
- Validation results per row (valid/error/duplicate), created case IDs, failed row details

**7. UI Regions**
- Tab bar at top: [Bulk Invite] [Bulk Pre-filled Data]
- Left: Action steps (Download → Upload → Validate → Confirm → Track)
- Center: Current step content (dropzone → validation table → confirmation → results)
- Right: Column guide (what each column means, valid values)

**8. Cards**
- Validation Summary Card: "18 rows valid | 3 rows with errors | 2 rows are duplicates"
- Progress Card (during creation): Cases created / Total valid rows
- Tab 2 — Consent Declaration Card (before confirm): Declaration text with acknowledgement checkbox

**9. Tables**
- Validation Preview Table: Row number | Candidate name | Email | Mobile | Package | Status (Valid/Error/Duplicate) | Error details (inline per error cell)
- Results Table: Row | Candidate | Status (Created/Skipped/Failed) | Case ID (for created) | Reason (for failed)
- Tab 2 — extended preview shows all data fields (not just name/email)

**10. Drawers**
- Column Guide Drawer: Each column name, data type, required/optional, valid values, example values

**11. Modals**
- Tab 1 — Confirm Upload Modal: "You are about to create [N] cases and send invitations. [M] duplicate rows will be skipped. Estimated cost: [X]. Confirm?"
- Tab 1 — Error Summary Modal: Full error list before partial proceed
- Tab 2 — Confirm Submit Modal (NEW): "You are about to create [N] cases with client-supplied data. No candidate invitations will be sent. All candidates have consented per the ConsentObtained column. Cases will go directly to KPMG ops for verification. Confirm?"

**12. Filters** None in upload flow; results table filterable by status

**13. Bulk Actions**
- Tab 1: [Download Results] | [View Created Cases] (filter case list to this batch)
- Tab 2 (NEW): [Download Results] | [Upload Documents] (post-creation ZIP upload for candidate docs) | [View Created Cases]

**14. Alerts/Banners**
- "File format error: Column not found in uploaded file. Please use the provided template." — red, blocks proceed
- "3 rows have invalid mobile number format." — amber, non-blocking
- "14 duplicate candidates detected." — decision banner
- Tab 2 only (NEW): "ConsentObtained column is mandatory — all rows must have 'Yes' before submission" — red, blocking if any row is blank or No
- Tab 2 only (NEW): "No candidate invitation emails will be sent for any of these [N] cases" — blue, informational

**15. Timeline/Audit**
Bulk upload event logged: user, tab/mode used (bulk_invite OR bulk_prefilled), file hash, timestamp, rows attempted, rows created, rows skipped, rows failed. Tab 2: consent declaration acknowledgement logged.

**16. SLA Components**
- Tab 1: "All invitations will be sent within 5 minutes of confirmation."
- Tab 2 (NEW): "Cases will be visible to KPMG ops immediately. Ops review begins within [N] business hours."

**17. AI Components**
Duplicate detection on all rows (hash-based email + mobile + name fuzzy match) — both tabs

**18. Evidence Components**
- Tab 2 only (NEW): Post-creation document upload — ZIP upload with per-candidate documents matched by name/email

**19. Mobile Considerations**
Bulk upload is a desktop-primary feature. Mobile: soft warning "this feature is best used on desktop." Allow file upload on mobile if user insists. Tab 2 (full data) is desktop-only recommended.

---



---

## GAP-10 FIX: Bulk Validation Three-Section Format

### Addition to 6.2.2 Bulk Case Upload — Validation Engine and Results

**Updated Validation Report Structure (Three Sections)**

Replace current two-section (Valid/Error) with three-section format:

**Section 1 — Accepted Records (green)**
```
✅ ACCEPTED — 487 records
Ready for case creation. Review summary before confirming.

Preview: [Paginated table — 20 rows shown, scroll for more]
Row | Candidate | Package | BU | Consent Route | Predicted SLA Start | Routing Queue
1   | Priya S.  | Pro     | HR | Candidate Portal | 10-Jan 09:00 | Standard Queue
2   | Rahul M.  | Exec    | Fin| Candidate Portal | 10-Jan 09:00 | Senior Reviewer Queue
...
```

**Section 2 — Rejected Records (red — must fix)**
```
❌ REJECTED — 8 records (cannot be created — must correct)

Row | Candidate Ref | Field | Error | How to Fix
3   | Row 3        | Email | Invalid format | Use valid email address
7   | Row 7        | Package | "Pro Exec" not found | Use exact package name from dropdown
12  | Row 12       | Mobile | 9-digit number | Indian mobile must be 10 digits
...

[Download Rejected Records — Excel] [Fix and Re-upload Errors Only]
```

**Section 3 — Warning Records (amber — non-blocking, requires acknowledgement)**
```
⚠️ WARNINGS — 12 records (can proceed — review recommended)

Warning Type            | Count | Details
Fuzzy duplicate         | 3     | Near-match to existing candidates (>70% similarity but below threshold)
Vendor coverage gap     | 5     | Selected geography has no active vendor for Criminal check
Optional field missing  | 4     | Requisition reference not provided (tracking may be affected)

[Expand each warning type to see specific rows]

☐ I have reviewed all warnings and wish to proceed with these records.
(Acknowledgement required to include warning records in creation)
```

**Impact Summary (mandatory review before confirm)**
```
IMPACT SUMMARY — Review before confirming

Cases to be created:         487 accepted + 12 warning (if acknowledged) = up to 499
Invitations to be sent:      485 (candidate portal flow)
Alternate flow cases:        14 (consent-only link)
Vendor checks triggered:     Criminal — 234 cases | Employment — 499 cases
Financial checks triggered:  12 cases (require financial consent confirmation)
Estimated SLA start:         10-Jan-2025 09:00 IST
Smart routing queue:         Standard: 423 | Senior Reviewer: 64 | BFSI Specialist: 12

⚠️ This batch exceeds 200 records. Type CONFIRM to proceed:
[_______________] ← text field, must type exactly "CONFIRM"

[Confirm and Create Cases]  [Cancel]
```

---

---

## C-01 FIX: New Page — 6.2.22 Ops Manual Case Creation Workbench

> **RFP 10.1, 13.1 | Legacy source: MOM "Manual extraction from client systems" + PPTX "Email" path of 50% manual entry**
> This page covers Flow F2 — where client emails candidate data (Excel/Word/PDF) to KPMG
> and KPMG ops staff creates the case by entering data manually into KCheck.
> The non-candidate path in the Ops Portal — no candidate portal step occurs.

### 6.2.22 Page: Ops Manual Case Creation Workbench

**1. Page Objective**
Enable KPMG ops staff to create a BGV case and enter all candidate data directly — for cases where the client has sent data via email, Excel, or offline channel. Candidate does not interact with the system. This is the ops-side counterpart to the Client Portal "Enter Data Directly" flow.

**2. Primary Actors** Ops Reviewer, Senior Reviewer, Team Lead

**3. Key Workflows**
- Mode A (Excel Import): Upload client Excel → auto-populate fields → review/correct → add consent reference → submit
- Mode B (Manual Entry): Select client + package → type all fields from client email → upload docs → add consent reference → submit

**4. States**
Mode Selected → Data Entry (In Progress) → Docs Uploaded → Consent Reference Added → Review → Submitted → Case Active in Queue

**5. Actions**
Select entry mode, upload Excel (Mode A), type fields (Mode B), upload documents, enter consent reference, preview full case, submit, cancel

**6. Data Blocks**
- Client tenant selector (which client does this case belong to)
- BGV package selector
- Full candidate profile:
  - Personal: full name, DOB, gender, personal email, mobile, current address, nationality
  - Employment: per employer — company, designation, from/to dates, supervisor name/contact, reason for leaving (repeatable rows)
  - Education: per qualification — institution, degree/specialisation, year of passing, roll number (repeatable rows)
  - Identity: Aadhaar, PAN, Passport, DL — as required by selected package
- Document uploads (per section)
- Data source (Email / Excel / Phone / Courier / HRMS Extract)
- Consent reference (free-text — mandatory)
- Requisition reference / Job ID (optional)

**7. UI Regions**
- Top bar: Client selector | Package selector | Mode toggle [Excel Import] [Manual Entry]
- Left sidebar: Section navigator (Personal / Employment / Education / Identity / Documents / Consent)
- Center: Active section form
- Right panel: Completeness tracker (which sections are filled, which are pending)

**8. Cards**
- Section Completeness Card (right panel): Per section — Complete / Partial / Empty
- Consent Reference Card: "This is the audit trail for offline consent. Be specific — include date, sender name, and reference number."
- Excel Import Summary Card (Mode A): "Mapped [N] fields successfully. [M] fields could not be mapped — please fill manually."

**9. Tables**
- Employment History Table: Add / edit / remove rows. Columns: Employer | Designation | From | To | Supervisor | Reason for Leaving
- Education Table: Add / edit / remove rows. Columns: Institution | Degree | Year | Roll Number / Enrolment No.

**10. Drawers**
- Column Mapping Drawer (Mode A): Shows how Excel columns mapped to KCheck fields; unmapped columns listed for manual entry
- Document Upload Drawer (per section): Upload docs relevant to that section (employment → experience letters; education → degree certificates; identity → ID scans)

**11. Modals**
- Submit Confirmation Modal: Full case data summary. "This case will be created without candidate portal involvement. Candidate will NOT receive any system notifications." [Confirm & Create Case] [Go Back]
- Missing Fields Warning Modal (on submit attempt with incomplete mandatory fields): List of unfilled required fields with section links

**12. Tabs** Section tabs: Personal | Employment | Education | Identity | Documents | **Custom Fields** | Consent & Audit

**Custom Fields Tab [C-08 | RFP 12.3]:**
When the selected client has Active custom fields scoped to the applicable BU/country, a "Custom Fields" tab appears in the form. It shows all scoped custom fields with:
- Display label and data type (matching the registry configuration)
- Required fields marked with asterisk — ops cannot submit without filling these
- Conditional fields shown/hidden per their conditions
- Fields not applicable to this BU or country are automatically excluded
- "No custom fields configured for this client" message if client has none

**13. Filters** None

**14. Bulk Actions** None — single case only (bulk: use Client Portal Tab 2 Bulk Pre-filled)

**15. Alerts/Banners**
- "No candidate email provided — candidate will not receive any system notifications" — blue, informational
- "Consent Reference is mandatory — this is your audit trail for DPDP/GDPR compliance" — red, blocking on submit
- Mode A: "Excel uploaded — [N] fields auto-populated. [M] fields could not be mapped. Please review highlighted fields." — amber
- Mode A: "Column '[X]' in your Excel was not recognised and has been ignored. Check the data for this field manually." — amber per unrecognised column
- "Required field empty: [field name]" — red inline per mandatory field on submit attempt

**16. Timeline/Audit**
On case creation, audit event logged:
- Creating ops user + role
- Client tenant + package
- initiation_mode: ops_manual
- data_source: (Email / Excel / Phone / Courier / HRMS Extract) — from dropdown selection
- consent_reference: full text entered by ops (verbatim, not truncated)
- Timestamp (IST)
All audit fields are immutable after submission.

**17. SLA Components**
Case SLA begins at submission timestamp. No "Pending Candidate" phase in SLA chain — case enters "In Verification" directly.

**18. AI Components**
- Duplicate detection on candidate name + DOB + client (runs on submit, not in real-time)
- If duplicate found: "Case for [Candidate Name] (DOB: [date]) already exists for this client — Case [ID]. Do you want to proceed with a new case or link to the existing one?"

**19. Evidence Components**
Document upload per section — all documents uploaded by ops are tagged:
- Uploaded by: [Ops User Name]
- Source: Client-provided
- Section: Employment / Education / Identity
All documents stored in the same evidence store as candidate-uploaded documents; differentiated by upload_source tag.

**20. Mobile Considerations**
Desktop-only recommended. Mobile technically supported but strongly discouraged — volume of fields and document uploads makes mobile entry impractical. Mobile banner: "For best experience, use a desktop browser to create manual cases."

---

---


---

## C-08 FIX: New Page — 6.2.23 Custom Field Registry

> **RFP 12.3 | "Add custom data fields and validations per client/BU/country"**
> Distinct from Form Builder (RFP 12.4 / 6.2.12) which controls form presentation.
> Custom Field Registry extends the case DATA MODEL — making fields searchable,
> exportable, API-queryable, and validated server-side regardless of entry point.

---

### 6.2.23 Page: Custom Field Registry

**1. Page Objective**
Enable Client Admins to register client-specific data fields that extend the standard KCheck case data model — scoped per client, BU, and/or country. Registered fields become first-class case attributes: searchable in All Cases, included in exports, returned in API responses, visible in all case views, and validated server-side regardless of which portal submitted the data. RFP 12.3.

**2. Primary Actors** Client Admin (manages their tenant's fields), Platform Admin (read-only cross-tenant view)

**3. Key Workflows**
Register new field → Configure scope and validation → Publish → Field appears in Form Builder palette, All Cases column selector, exports, and API → Deactivate field (preserves historical data)

**4. States**
Per field: Active | Inactive (deactivated — hidden from new cases, preserved historically) | Draft (created but not yet published)

**5. Actions**
Add field, edit display label and options (field key is immutable after save), deactivate, reactivate, preview in form, view usage stats

**6. Data Blocks**
Per field: field key (API key, immutable) | display label | data type (Text/Number/Date/Dropdown/Multi-select/Boolean) | options list (for Dropdown/Multi-select) | scope (client-wide / specific BUs / specific countries) | required (Blocking/Optional/Conditional) | searchable | exportable | visible in (Candidate/Ops/Client/All) | status

**7. UI Regions**
- Top: Field count bar — "12 / 50 custom fields used"
- Main table: All fields with status, type, scope, usage count
- [Add Custom Field] button (top right)
- Per-row: [Edit] [Deactivate/Reactivate] [Preview] [View Usage]

**8. Tables**

Custom Field Registry Table:
| Field Key | Display Label | Type | Scope | Required | Searchable | Exportable | Cases Using | Status |
|---|---|---|---|---|---|---|---|---|
| employee_grade | Employee Grade | Dropdown | Client-wide | Blocking | Yes | Yes | 248 | Active |
| work_permit_type | Work Permit Type | Dropdown | Country: USA | Optional | Yes | Yes | 14 | Active |
| bu_cost_centre | Business Unit Code | Text | BU: India Ops | Optional | No | Yes | 87 | Active |
| hiring_batch | Campus Batch | Text | Client-wide | Optional | Yes | No | 0 | Draft |

"Cases Using" = active cases with a value for this field. Clicking count opens All Cases filtered to those cases.

**9. Drawers**

Add / Edit Field Drawer:
```
REGISTER CUSTOM FIELD
─────────────────────────────────────────────────────
Field Key *      [employee_grade          ]
                 Immutable once saved. Use lowercase_underscore.
                 API ref: custom_attributes.employee_grade

Display Label *  [Employee Grade          ]   (editable later)

Data Type *      [Dropdown               v]
  Options:       [ VP ] [ Director ] [ Managing Director ] [+ Add option]

Scope *
  o Client-wide
  o Specific Business Units: [Select BUs v]
  o Specific Countries:      [Select Countries v]

Required?
  o Blocking — case cannot submit without this
  * Optional
  o Conditional — required IF [field v] = [value]

Visible in:
  [x] Candidate Portal  [x] Ops Portal  [x] Client Portal

Searchable in All Cases: [x] Yes
Exportable:              [x] Yes
─────────────────────────────────────────────────────
[Save Draft]   [Publish]   [Cancel]
```

Field Usage Drawer: value distribution pie (VP: 42% | Director: 38% | MD: 20%), usage by BU/country, date range

Field Preview Drawer: field rendered in Candidate Portal, Ops Portal, and Client Portal views side-by-side

**10. Modals**
- Deactivate Modal: "Deactivating hides field from new cases. Preserved in [N] existing cases and their exports. Reversible. [Confirm]"
- Delete Draft Modal: "Permanently delete draft field with 0 usage? [Confirm]" (Draft only)
- Publish Modal: "Field immediately available in Form Builder, All Cases, exports, and API. [Confirm]"

**11. Alerts/Banners**
- "50/50 custom fields used — deactivate unused fields to register new ones." (red, blocks Add)
- "Field key already exists — choose a unique key." (red, inline)
- "[N] active cases use this field — deactivating preserves their data." (amber, on deactivate)

**12. Downstream Impact — Where Custom Fields Flow**
After publishing:
- Form Builder (6.2.12): field appears in palette under "Your Custom Fields" — drag onto any form
- All Cases (6.1.4 / 6.2.3): column selector + filter panel (if Searchable = Yes)
- Case Detail (Ops + Client): "Custom Fields" section shows field key/value pairs
- Ops Manual Case Creation (6.2.22): scoped fields appear in "Custom Fields" section; required fields are blocking
- API GET /v1/cases/{id}: returns { custom_attributes: { employee_grade: "Director" } }
- API POST /v1/cases and HRMS push: accepts custom_attributes block
- Bulk Export: column included (if Exportable = Yes) per case row
- MIS Reports: filter, group-by, and column dimensions
- Rule Engine (RFP 12.2): custom field values referenceable in routing/adjudication rules
- Data Catalog (6.5.20): auto-creates entry for each new field — flagged for Privacy Officer review

**13. Server-Side Validation**
Enforced at API layer for ALL entry points (Candidate Portal, Ops Manual, HRMS push, REST API):
- Required fields: HTTP 400 if missing and scope matches
- Dropdown/Multi-select: HTTP 422 if value not in configured options
- Date: ISO 8601 enforced
- Text: max 500 chars default
- Per-field errors returned in API response

**14. Mobile** Admin registration is desktop-only. Custom fields are visible and fillable on mobile in Candidate Portal (candidate-facing) and Ops Portal (ops-facing).

---



---

## C-11 FIX: New Page — 6.2.24 Client Audit Evidence Request

> **RFP 22.4 | "Right to audit — Customer right to audit vendor controls and evidence"**
> Distinct from the Auditor Module (5.7 — for external regulators) and standard BGV reports.
> This is the formal channel for CLIENT COMPANIES to exercise their contractual right
> to audit KPMG's verification process, controls, and evidence for their candidates.
> Integrates with C-06 Ticketing (ServiceNow) for KPMG-side request tracking.

---

### 6.2.24 Page: Client Audit Evidence Request

**1. Page Objective**
Enable Client Admin to formally exercise their contractual right (RFP 22.4) to audit KPMG's
verification controls, methodology, and evidence for their candidates. Provides a tracked,
ITSM-integrated channel replacing informal email requests. Three evidence categories:
per-case evidence, process controls, and compliance documentation.

**2. Primary Actors** Client Admin (raises request), KPMG Compliance Officer (fulfils request)

**3. Key Workflows**
Client raises request → selects type and scope → KPMG receives ServiceNow ticket →
KPMG prepares evidence pack → Client notified → Client downloads via time-limited secure link →
Download logged → Request closed

**4. States**
Per request: Draft | Submitted | In Review (KPMG received) | Evidence Preparation |
Ready for Download | Partially Downloaded | Fully Downloaded | Closed | Withdrawn

**5. Actions**
Raise new request, track status, download evidence pack, withdraw pending request, view history

**6. Data Blocks**
Request ID (auto-generated) | Request type | Scope (case IDs / date range) | Purpose (free text) |
Preferred format | Submitted by | Submitted at | KPMG owner assigned | Target completion date |
Status | Evidence ready timestamp | Download links (with expiry) | Download log (who/when) |
Linked ServiceNow ticket ID (via C-06)

**7. UI Regions**
- [Raise Audit Request] button (primary CTA, top of page)
- Active requests table (in-progress requests, most recent first)
- Completed requests accordion (closed requests, last 12 months)
- Evidence download section (shown when status = Ready for Download)

**8. Raise Audit Request Wizard**

```
STEP 1 — REQUEST TYPE
────────────────────────────────────────────────────────────────
What would you like to audit?

  [✓] Per-case verification evidence
      "Detailed evidence, adjudication notes, and process steps
       for specific candidate verification cases."
      → Scope: Select case IDs or date range

  [ ] Process controls and methodology
      "KPMG's verification procedures, QC sampling rates,
       reviewer qualification standards, and training documentation."
      → Scope: Not case-specific — KPMG-wide controls

  [ ] Compliance documentation
      "Data Processing Agreement, subprocessor DPAs, security
       certifications (ISO 27001, SOC 2), data retention schedule,
       incident history for your data."
      → Scope: Not case-specific — compliance artefacts

  (Select one or more)
────────────────────────────────────────────────────────────────

STEP 2 — SCOPE (if Per-case selected)
────────────────────────────────────────────────────────────────
  Which cases?
  ○ Specific cases:  [Search and select case IDs              ]
  ○ Date range:      From [____] To [____] (all cases in range)
  ○ All active cases (confirm: [N] cases will be included)
────────────────────────────────────────────────────────────────

STEP 3 — PURPOSE AND FORMAT
────────────────────────────────────────────────────────────────
  Purpose / reason for audit: *
  [                                                              ]
  (e.g., "Annual vendor compliance review Q1 2026",
         "Candidate dispute — Ravi Kumar, Case KCHK-2026-09841",
         "Regulatory inspection by DPDP authority")

  Preferred delivery format:
  ○ PDF evidence pack (downloadable)
  ○ In-portal view only (no download)
  ● Both (PDF + in-portal)

  Urgency:
  ○ Standard (5 business days)
  ○ Urgent (2 business days — requires justification)
    Justification: [                    ]
────────────────────────────────────────────────────────────────

STEP 4 — REVIEW & SUBMIT
  Summary of request:
    Type: Per-case evidence + Compliance documentation
    Scope: 3 cases (KCHK-2026-09841, KCHK-2026-09715, KCHK-2026-09601)
    Purpose: Regulatory inspection
    Format: PDF + In-portal
    Target: Within 5 business days

  Declaration: "I confirm this audit request is made in accordance with
  our contractual agreement with KPMG and the stated purpose above."
  [✓] I confirm

  [Submit Audit Request]
────────────────────────────────────────────────────────────────
→ On submit:
    • Request ID generated (AUD-2026-00041)
    • ServiceNow Service Request auto-created via C-06 ticketing integration
      Title: "KCheck Audit Evidence Request — [Client Name] — AUD-2026-00041"
      Assigned to: KPMG Compliance group
    • Client Admin receives confirmation email:
      "Your audit request AUD-2026-00041 has been received.
       Target completion: [date]. Reference: [ServiceNow ticket ID]."
```

**9. Tables**

Active Requests Table:
| Request ID | Type | Scope | Submitted | Status | KPMG Owner | Target Date | ServiceNow Ref |
|---|---|---|---|---|---|---|---|
| AUD-2026-00041 | Per-case + Compliance | 3 cases | 14-May | In Review | [KPMG Compliance] | 21-May | SVC0044521 |
| AUD-2026-00039 | Process Controls | KPMG-wide | 10-May | Evidence Preparation | [KPMG Compliance] | 17-May | SVC0044489 |

Evidence Download Section (shown when status = Ready for Download):
| Evidence Item | Type | Prepared | Format | Download | Expires | Downloaded By |
|---|---|---|---|---|---|---|
| Audit Pack — KCHK-2026-09841 | Per-case | 19-May | PDF | [Download] | 72h | — |
| Audit Pack — KCHK-2026-09715 | Per-case | 19-May | PDF | [Download] | 72h | — |
| ISO 27001 Certificate 2026 | Compliance | 19-May | PDF | [Download] | 72h | — |
| Data Processing Agreement | Compliance | 19-May | PDF | [Download] | 72h | — |
| Subprocessor List (current) | Compliance | 19-May | PDF | [Download] | 72h | — |

Completed Requests Accordion (last 12 months):
| Request ID | Type | Closed | Summary | Re-request |
|---|---|---|---|---|
| AUD-2026-00031 | Per-case (Annual Review) | 12-Mar | 47 cases | [Re-request same scope] |

**10. Drawers**
- Request Detail Drawer: Full request history — each status change, who changed it, when,
  KPMG compliance notes, ServiceNow ticket timeline
- Evidence Preview Drawer: In-portal view of evidence pack (if format = In-portal selected)
  Displays same format as Auditor Module — consent record, evidence list, adjudication trail
- Re-request Drawer: Pre-fills a new request wizard with same parameters as a previous request

**11. Modals**
- Submit Confirmation Modal: Full request summary + declaration checkbox. "Your request will
  be processed within [N] business days. You will be notified by email when evidence is ready."
- Download Confirmation Modal: "You are downloading [N] evidence files. This download is
  logged and will be included in your audit trail. Links expire in 72 hours. [Confirm Download]"
- Withdraw Request Modal: "Withdraw request AUD-2026-XXXXX? This cannot be undone if evidence
  preparation has already begun. KPMG will be notified. Reason: [mandatory field] [Confirm]"
- Link Expired Modal: "Your download link has expired (72-hour limit). Request a new download
  link? [Request New Link] — KPMG will re-generate within 1 business day."

**12. Alerts/Banners**
- "Evidence ready — Audit Request AUD-2026-00041 is ready for download. Links expire in [N] hours."
  (green banner, dismissible — also sent via email)
- "Urgent request acknowledged — KPMG compliance has been notified of your urgent request.
  Target: 2 business days." (blue, after urgent submission)
- "Download link expired — [Request New Link]" (amber, on expired link attempt)
- "Request AUD-XXXXX has been updated: Status changed to [In Review] by KPMG Compliance." (blue)

**13. Evidence Pack Contents (Per-Case Audit)**
When KPMG fulfils a per-case audit request, the evidence pack includes:
- Consent record (what consent was captured, when, which version)
- All documents uploaded by candidate (with upload timestamps and quality scores)
- All employer/university/referee responses received
- Check-by-check outcomes with source evidence references
- AI signals reviewed (type, confidence, whether overridden)
- Adjudication notes (full text — including internal reviewer notes)
- Communication log (all messages sent to candidate, employer, vendor)
- Audit event log (every action on this case, with actor and timestamp)
- Verification methodology note ("Employment check conducted via EPFO API + employer email outreach")
- Report version delivered to client

**14. Audit/Compliance**
Every request, status change, download, and withdrawal is immutably logged:
- Who raised the request, when, from which IP
- Each status change (who, when, what changed)
- Each download (who, when, which files, IP address)
- ServiceNow ticket ID linked
This log is available to KPMG Platform Admin and is included in KPMG's own compliance records.

**15. Mobile** Request submission accessible on mobile (simplified wizard). Evidence download
is desktop-recommended for bulk PDF packs. Mobile: soft warning "For best experience downloading
audit evidence packs, use a desktop browser."

## GAP-EXP-L4 FIX: Bulk Export Role-Based Redaction — Client Portal

### L-4 | Bulk Export Role-Based Redaction — Not Fully in Client Portal Design Depth

**RFP Reference:** RFP 18.4

**RFP Text:**
> *"Export to Excel/CSV — Configurable exports with role-based redaction"*

**Verdict:** EXPLICIT

**Analysis:**
RFP 18.4 explicitly names "role-based redaction" as a required feature of the export function. The Client Portal bulk export design depth does not specify which fields are redacted for which client roles (HR Viewer vs Client Admin), how the redaction is applied, or how the candidate is informed that the export may not contain all fields. Without this specification, frontend developers cannot build a compliant export that appropriately masks sensitive fields for lower-privileged client users.

**Impact:**
- HR Viewers (non-admin client users) could export full case data including adjudication notes, AI risk scores, and check-by-check outcomes — data they are not authorized to see.
- Bulk CSV exports sent to external HR systems via ATS integration could include sensitive fields not intended for that system.
- Absence of redaction specification violates the principle of least privilege for client-side data access.

**Recommendation:**

---

### Addition to 6.2.2 Bulk Case Upload and 6.2.7 Report Inbox — Bulk Export Redaction Specification

**Role-Based Export Redaction Matrix (add to bulk export and report archive pages):**

| Field | Client Admin | HR Manager | HR Viewer | Read-Only User |
|---|---|---|---|---|
| Case reference | ✅ Full | ✅ Full | ✅ Full | ✅ Full |
| Candidate name | ✅ Full | ✅ Full | ✅ Full | Redacted (initials only) |
| Candidate email | ✅ Full | ✅ Full | Redacted (***@domain) | Redacted |
| Candidate phone | ✅ Full | Redacted | Redacted | Redacted |
| Package name | ✅ Full | ✅ Full | ✅ Full | ✅ Full |
| Overall outcome (color) | ✅ Full | ✅ Full | ✅ Full | ✅ Full |
| Per-check outcomes | ✅ Full | ✅ Full | Summary only | Summary only |
| Adjudication notes | ✅ Full | Redacted | Redacted | Redacted |
| AI risk score | ✅ Full | Redacted | Redacted | Redacted |
| Discrepancy details | ✅ Full | ✅ Full | Summary only | Redacted |
| Vendor name | ✅ Full | Redacted | Redacted | Redacted |
| SLA breaches | ✅ Full | ✅ Full | Count only | Count only |
| Invoice amount per case | ✅ Full | Redacted | Redacted | Redacted |

**Export Preview Step (add to bulk export workflow in 6.2.2 and 6.2.8):**

Before download, show a preview of the export structure:

```
EXPORT PREVIEW — Your role: HR Manager
──────────────────────────────────────────────────────────
This export contains [N] cases.

Based on your role (HR Manager), the following fields
are included in this export:

✅ Case reference, Package, Outcome, Check summaries,
   Discrepancy summary, SLA status, BU tags

⚠ The following fields are not included (role-restricted):
   Adjudication notes, AI risk score, Vendor details,
   Candidate phone number, Invoice amounts

If you require full data access, contact your Client Admin.

[Proceed with Export — [N] cases, [N] columns]   [Cancel]
──────────────────────────────────────────────────────────
```

**Redaction Indicator in Exported File:**

In the exported CSV/Excel:
- Redacted fields are present as columns (so column structure is consistent) but show value: "[Restricted — Contact Admin]"
- This prevents downstream systems from misinterpreting missing columns as missing data
- The export header row includes: "Export generated for role: [role]. Redacted fields marked [Restricted]."

**Part 5 Impact:** No new page needed. This is an addition to the design depth of the existing bulk export and report archive pages.


### 6.2.3 Page: Case Detail (Client View)

**1. Page Objective**
Give clients clear status visibility with appropriate information filtering — no ops internals, no vendor details, no intermediate AI signals exposed.

**2. Primary Actors** Client Initiator (HR/TA), Client Viewer, Client Admin

**3. Key Workflows**
Check overall status → Review per-check progress → Download report when ready → Re-invite candidate if not submitted → Initiate dispute if outcome challenged → Trigger adjudication approval if required

**4. States**
Initiated → Invitation Sent → Candidate In Progress → Verification In Progress → Pending Client Review → Report Ready → Closed / On Hold

**5. Actions**
View status, download report, re-invite candidate, initiate dispute, approve/reject (if adjudication approval required), put on hold, close case

**6. Data Blocks — What Client Sees vs Does NOT See**
VISIBLE:
- Overall status (high-level: In Progress / Completed)
- Per-check status (Not Started / In Progress / Awaiting Candidate / Completed)
- Final adjudicated outcome per check (Verified / Discrepancy / Unable to Verify — final only)
- Report (when released)
- Discrepancy summary (type + severity + resolution — adjudicated only)
- Client-visible communications only
- SLA status (On Track / At Risk — not countdown)
- **Custom Fields section [C-08 | RFP 12.3]:** All Active custom fields scoped to this client and applicable to this case's BU/country shown with their current values. Displayed as a simple key-value list: "Employee Grade: Director | Business Unit Code: IB-001". If a required custom field has no value (e.g., case initiated before field was created), shown as "Employee Grade: — [Not set]"

NOT VISIBLE:
- Reviewer names, ops notes, QC status
- Vendor identities, vendor assignment details
- Intermediate AI flags (pre-adjudication)
- Internal escalation history
- Other clients' data

**7. UI Regions**
- Top: Case header (Case ID, candidate, package, status badge, outcome color post-adjudication)
- Center-left: Check progress timeline (visual per-check status icons)
- Center-right: Active alerts/actions (if any)
- Bottom: Report section + communications + dispute link

**8. Cards**
- Overall Status Card: Status badge, outcome color (post-adjudication), last updated
- Check Progress Cards (one per check): Check name, status icon, expected completion
- "Action Required" Card: Re-invite prompt / client approval request / dispute response needed
- Report Card: Download button, report date, version indicator

**9. Tables**
- Check Summary Table (simplified): Check type | Status | Outcome (post-adjudication only)
- Communication History Table (client-visible only): Date | Type | Direction (received/sent)

**10. Drawers**
- Report Preview Drawer: In-browser PDF preview before download
- Discrepancy Details Drawer: For each discrepancy (adjudicated) — type, severity, resolution; no ops internal notes

**11. Modals**
- Re-invite Modal: "Resend invitation to [candidate] via [channels]? Current status: Not submitted [N days]."
- On Hold Modal: Reason (candidate not joining / role cancelled / pending HR decision) + confirm
- Client Approval Modal: If client adjudication sign-off required — show discrepancy summary, outcome options, mandatory note

**12. Tabs**
Overview | Checks | Report | Communications | History

**13. Filters** None at case level

**14. SLA Components**
SLA status chip (On Track / At Risk) — no countdown shown to client (prevents gaming of SLA notification timing)

**15. AI Components**
None visible to client (AI signals are ops-internal until adjudicated)

**16. Evidence Components**
Report preview (formatted PDF, not raw evidence). Evidence documents not directly accessible to client.

**17. Alerts/Banners**
- "Candidate has not submitted information — [N] days since invitation sent. [Re-invite]" — amber
- "Your review is required before the report can be released. [Review Now]" — blue action banner
- "Report ready for download." — green
- "A dispute has been filed for this case. [View Status]" — informational

**18. Timeline/Audit**
Client-visible history: Initiated | Invitation sent | Candidate submitted | Verification started | Verification completed | Report issued. No ops-internal events shown.

**19. Mobile Considerations**
Status check is primary mobile use case for HR managers. Cards must be mobile-first (stacked, full-width). Report download must work on mobile. Re-invite one-tap action. Notification deep-links into this page directly.

---


---

## GAP-EXP-FA1 FIX: Missing Explicit Actions — Client Portal Case Detail

### FA-1 | 'Conditional Offer Extended' Trigger — Client Portal Case Detail

**RFP Reference:** RFP 6.8

**RFP Text:**
> *"Local policy constraints — Support ban-the-box style workflows / conditional-offer gating where applicable"*

**Verdict:** EXPLICIT

**Analysis:**
RFP 6.8 explicitly requires support for ban-the-box conditional-offer gating workflows. In ban-the-box jurisdictions (applicable UK, certain US states, and emerging Indian practice), a criminal background check cannot be initiated until a conditional employment offer has been extended to the candidate. The Client Portal Case Detail must include an explicit "Conditional Offer Extended" action so the client can trigger the criminal check gate — without this action, the system has no way to receive the signal and release the criminal check for processing.

**Impact:**
- In ban-the-box jurisdictions, criminal checks executed before conditional offer = statutory violation. The client has no UI mechanism to confirm offer status.
- The ops team cannot distinguish cases where criminal check is legitimately held pending conditional offer from cases where the check was forgotten.

**Recommendation:**
Add 'Conditional Offer Extended' action to 6.2.3 Case Detail (Client View):

**Addition to 6.2.3 Case Detail — Client View:**

**Ban-the-Box Gate Component (conditional — shown only when package has ban-the-box configuration):**

```
CONDITIONAL OFFER GATE
────────────────────────────────────────────────────────
⏸ Criminal Check HELD — Awaiting Conditional Offer Confirmation

This package requires confirmation that a conditional offer
has been extended before the criminal background check begins.
This is required by local policy / jurisdictional regulation.

[ ✅ Conditional Offer Extended — Release Criminal Check ]

By confirming, you acknowledge that a conditional employment
offer has been formally extended to the candidate.
────────────────────────────────────────────────────────
```

- Button state: Primary (prominent) — shown with case context card
- Confirmation modal: "Confirming conditional offer extended for [Candidate masked ID]. This will release the criminal background check for processing. The candidate's results will be reviewed under your configured adjudication policy. [Confirm]"
- After confirmation: gate closes, banner changes to "✅ Conditional offer confirmed [date] — Criminal check released for processing", check begins processing
- Audit event: actor identity, timestamp, confirmation

---

### FA-2 | 'Request Consent Renewal' Action — Ops Portal Case Workbench

**RFP Reference:** RFP 15.1

**RFP Text:**
> *"Consent lifecycle management — Capture, validate, store, renew, and withdraw consent with version history"*

**Verdict:** EXPLICIT

**Analysis:**
RFP 15.1 explicitly names "renew" as a lifecycle action. The ops-side trigger for consent renewal — an action the Ops Lead takes when consent is approaching expiry — has no UI specification in the Case Workbench. Without this action, the ops team has no mechanism to request consent renewal from the candidate. The candidate-facing renewal page (GAP-EXP-M3) requires this ops-side trigger action to function.

**Recommendation:**
Add 'Request Consent Renewal' action to 6.1.39 Case Workbench:

**Addition to 6.1.39 Case Workbench — Actions (Item 6) and SLA Components (Item 18):**

**Consent Renewal Warning Banner (shown when consent expiry is approaching):**
```
⚠ CONSENT EXPIRING IN [N] DAYS
Candidate consent expires on [date]. If verification is not
complete by then, you must request consent renewal or
the case must be placed on hold.

[ Request Consent Renewal ]   [ Place Case On Hold ]
```

**Consent Expired Banner:**
```
🚫 CONSENT EXPIRED — [date]
Processing this case without renewed consent is not permitted.
Request renewal from the candidate immediately or close the case.

[ Request Consent Renewal ]   [ Close Case — Consent Lapsed ]
```

**Request Consent Renewal Action:**
- Click → Renewal Request Modal:
  "Send a consent renewal request to the candidate? They will receive an email/WhatsApp/SMS with a link to renew their consent. [Confirm — Send Renewal Request]"
- After confirmation: candidate receives notification → directed to 6.3.18 Consent Renewal page (GAP-EXP-M3)
- Case status: tag "Consent Renewal Pending" on case card
- SLA: Case SLA paused from consent expiry until renewal received (or case closed)

---

### FA-3 | 'Publish Adverse Action Notice' — Client Portal Case Detail

**RFP Reference:** RFP 10.11

**RFP Text:**
> *"Pre-adverse/adverse action workflow — Configurable notices, waiting periods, and final decisions (where applicable)"*

**Verdict:** EXPLICIT

**Analysis:**
RFP 10.11 explicitly requires a pre-adverse/adverse action workflow, which includes client-side acknowledgement for adverse decisions. When KPMG issues a pre-adverse notice and the waiting period expires, the client HR Lead must formally acknowledge the adverse action before it takes effect in their hiring system. The Client Portal has no action for this acknowledgement — the client receives a notification but cannot act on it within the platform.

**Recommendation:**
Add 'Acknowledge Adverse Action' action to 6.2.3 Case Detail — Client View:

**Addition to 6.2.3 Case Detail — Client View:**

**Adverse Action Acknowledgement Component (shown in "Pending My Action" state):**

```
ACTION REQUIRED — ADVERSE ACTION NOTIFICATION
────────────────────────────────────────────────────────
Background Verification: Adverse Outcome
Case: CK-0921   Package: ExecutivePro

KPMG has completed the pre-adverse/adverse action process.
The candidate has been notified and the waiting period has elapsed.

Summary of findings: [Adjudication summary — major discrepancy]
Final outcome: ❌ ADVERSE

As the hiring organization, please acknowledge this adverse
outcome decision. Your acknowledgement is recorded for compliance.

[ ✅ Acknowledge Adverse Action ]   [ ❓ Query This Outcome ]
────────────────────────────────────────────────────────
```

- Acknowledgement modal: "By acknowledging, you confirm you have received KPMG's adverse action notification and that the candidate has been given the required pre-adverse notice and response period. [Confirm Acknowledgement]"
- After acknowledgement: case status updated to "Adverse — Client Acknowledged"; audit event created; KPMG ops notified
- "Query This Outcome" → opens communication to KPMG ops with pre-filled case reference


### 6.2.4 Page: Client Analytics Dashboard

**1. Page Objective**
Strategic BGV program insights for HR leadership — outcome trends, TAT performance, discrepancy patterns, and volume analytics.

**2. Primary Actors** Client Admin, HR Director, TA Manager

**3. Key Workflows**
Review volume trend → Analyze outcome distribution → Identify discrepancy patterns → Compare business units → Export for HR leadership deck

**4. States**
Loading → Rendered (time period = default MTD) → Filtered (period / BU / package changed)

**5. Actions**
Select time period, filter by BU / package / country, drill into specific chart, export

**6. Data Blocks**
Case volume by period, outcome color distribution, TAT by package/check, discrepancy type frequency, BU comparison, candidate completion rate, geography distribution

**7. UI Regions**
- Top: Time period selector + filter bar (BU, package, country)
- Left: KPI summary strip
- Main grid: Chart cards (2-column responsive grid)
- Bottom: Export button

**8. Cards**
- Volume KPI cards: Cases initiated / Completed / In Progress / Reports downloaded (MTD)
- SLA Compliance card: % cases completed within SLA (their cases only)
- Avg TAT card: Average days to completion for their cases (vs KPMG's committed SLA)
- Completion Rate card: % candidates who complete form within 48h of invitation

**9. Charts / Visualization Components**
- Volume trend: Line chart (monthly, 12-month rolling)
- Outcome distribution: Stacked bar chart (Green/Amber/Yellow/Red by month)
- TAT by package: Horizontal bar chart (avg days per package)
- Discrepancy type frequency: Horizontal bar chart (top 10 discrepancy types found in their candidates)
- BU comparison: Grouped bar (volume + outcome distribution per BU)
- Geography distribution: Map or pie chart (India domestic vs international)

**10. Drawers**
- Chart Drilldown Drawer: Click any bar/segment → opens filtered case list for that segment

**11. Export**
Excel download: All metric tables with raw data. PowerPoint-ready: charts exported as PNG for PPT. Date range clearly labeled in export.

**12. Filters**
Time period (MTD / QTD / YTD / Custom) | Business unit (multi-select) | Package (multi-select) | Country | Outcome color

**13. SLA Components**
TAT vs committed SLA comparison: visual indicator showing whether avg TAT is within SLA commitment

**14. AI Components** None direct — aggregated data visualized

**15. Mobile Considerations**
Analytics is primarily desktop (charts require screen space). Mobile: simplified KPI strip cards only; "View full analytics on desktop" prompt for charts.

---

## 6.3 CANDIDATE PORTAL — Page Design Depth

---

### 6.3.1 Page: Consent & Disclosure

**1. Page Objective**
Capture legally binding, DPDP/GDPR-compliant consent in a way that is thorough enough to be audit-defensible and clear enough that candidates actually read and understand it.

**2. Primary Actors** Candidate (external, mobile-first, non-expert)

**3. Key Workflows**
Arrival from invitation link → Language selection → Notice display → Scroll to completion → Consent signature → Receipt generation → Proceed to form

**4. States**
Loaded → Scrolling (signature locked) → Fully scrolled (signature unlocked) → Signed → Receipt generated → Proceeding to form | Withdrawn consent (BGV ended)

**5. Actions**
Select language, scroll notice, sign (canvas/type/DocuSign), download receipt, proceed, or withdraw consent

**6. Data Blocks**
Consent notice text (version-controlled, client-specific + jurisdiction-specific), candidate identity + case reference, signature image, signing metadata (timestamp, IP, device fingerprint, geolocation), consent version ID, receipt PDF

**7. UI Regions**
- Top: Client-branded header (logo, welcome message)
- Language selector (persistent, accessible at all scroll positions)
- Notice body (full scrollable text — cannot be truncated or behind "see more" for key sections)
- Scroll progress bar (side or top — shows % read)
- Signature zone (below notice — locked until fully scrolled)
- Action bar (Download Receipt, Proceed — locked until signed)

**8. Cards**
- "Your Data Rights" summary card: Access / Correction / Erasure / Object / Portability — bullet summary (plain language, above the full legal notice for clarity)
- Consent Receipt Card (post-signing): Case reference, timestamp, version, [Download PDF]

**9. Tables** None

**10. Drawers**
- Data Categories Detail Drawer: Opens from "What data do we collect?" link — full breakdown by check type
- Third Parties Detail Drawer: "Who do we share data with?" — subprocessor list (generalized categories for confidentiality)
- Rights Exercise Drawer: "How to exercise your rights" — contact form prefilled with case reference

**11. Modals**
- Biometric Consent Modal (conditional): Separate explicit modal for biometric data consent (special category under DPDP/GDPR). Cannot be bundled with general consent. Separate [Agree] button. Plain language explanation of what biometric data is collected, how it's used, that it's not retained beyond matching. Only shown if package includes biometric check.
- Financial Check Consent Modal (conditional): Separate explicit consent if package includes credit check. Purpose of financial check stated explicitly.
- Consent Withdrawal Confirmation Modal: "Withdrawing consent will end your background verification process. This may affect your employment process with [Client]. Are you sure?" [Confirm Withdrawal] [Keep Consent Active]. Withdrawal recorded in audit even if candidate later reverses.

**12. Tabs** None — linear flow

**13. Filters** None

**14. Alerts/Banners**
- Scroll prompt: "Please scroll to the end of the notice to enable signing." (non-blocking soft banner, disappears when scrolled)
- Language prompt: "Choose your preferred language for this verification." (first load, dismissible)

**15. Compliance-Critical Elements (non-negotiable)**
- All data categories must be individually listed (not "personal data" as a catch-all)
- Each purpose must be specifically stated per data category
- Third parties listed (can be generalized categories, not named subprocessors, for confidentiality)
- Retention period per category
- All 6 rights individually named and explained
- Grievance officer contact (name + email) visible
- Withdrawal consequence disclosed before withdrawal option
- Biometric consent MUST be separate (DPDP special category)
- Financial check consent MUST be separate (credit bureau regulatory requirement)
- Consent version ID recorded at signature moment (not current version — the version displayed when signed)

**16. Timeline/Audit**
Consent event is the most important single audit event in the system:
- Stored: Consent version ID, full consent text hash, candidate identity hash, signing timestamp (UTC), IP address, device fingerprint hash, geolocation (if captured), user agent, signature image (stored in immutable object storage)
- Hash chain: This event is the first link in the case's audit hash chain
- Receipt PDF: Auto-generated, stored in object storage with immutable lock, linked to case

**17. SLA Components**
Consent must be captured before any verification processing starts — enforced at API level (case cannot advance to verification without consent record). No SLA timer applies to consent itself, but consent delay = case delay.

**18. AI Components** None direct at consent stage. Device fingerprint and geolocation are captured here and used later by fraud risk scoring model.

**19. Evidence Components**
Consent receipt PDF is itself an evidence artifact — the primary proof of lawful basis for all subsequent processing.

**20. Mobile Considerations**
- Minimum font size: 14px on mobile (WCAG AA)
- Notice scrollable in a fixed-height container on mobile (not page scroll — easier to detect full scroll)
- Signature pad: minimum 200px height for usable touch signature
- Language selector: visible without scrolling, top of screen, flag icons for recognition
- All consent sections must render correctly on 360px width minimum
- Consent receipt email delivered automatically (in case user forgets to download)

---



---

## GAP-18 FIX: Consent Withdrawal Active-Case Flow

### Addition to 6.3.1 Consent & Disclosure — Withdrawal on Active Case

**Withdrawal Access Point**
Consent withdrawal is accessible from two locations in the Candidate Portal:
1. Consent page (6.3.1) — during initial consent flow (before submission)
2. Help & Support page (6.3.14) — "My Data Rights" section — [Withdraw Consent] button — accessible at any point during an active case

**Withdrawal on Active Case — Distinct from Pre-Submission Withdrawal**
Pre-submission withdrawal (candidate has not yet submitted form): simple close, no legal complexity.
Post-submission withdrawal (case is in progress, verification ongoing): legally significant — requires legal basis assessment within 24 hours.

**Withdrawal Modal — Full Design (Post-Submission)**

Step 1 — Consequence Disclosure (non-dismissible, must scroll to enable button):
```
Withdraw Consent — Important Information

Withdrawing your consent will have the following effects:

• All pending background checks that have not yet started will be cancelled.
• Your employer [Client Name] will be notified that verification cannot be completed.
• This may affect your employment process.
• Withdrawal cannot be reversed — if verification is required, you will need to be 
  re-invited by your employer.

KPMG will assess whether any checks already in progress must continue under an 
alternative legal basis (e.g., fraud prevention). You will be notified of the outcome 
within 24 hours.

Your data will be retained per legal retention obligations, after which it will be deleted.
You retain the right to access, correct, and erase your data as described in our privacy notice.
```

Step 2 — Confirmation:
```
[Confirm Consent Withdrawal]    [Keep My Consent Active]
```

If candidate confirms:
- Case status → "On Hold — Consent Withdrawn"
- Candidate sees: "Your consent withdrawal request has been received. KPMG will notify you of the next steps within 24 hours. Your reference number: [case ID]."

**Status Page Update (6.3.5) — Withdrawn State**
Add to Status Page when case is in "On Hold — Consent Withdrawn":
```
Status: Verification Paused — Consent Withdrawn

Your consent withdrawal request is being processed. KPMG has paused your 
background verification.

What happens next:
• KPMG will review which checks (if any) must continue under a legal obligation.
• You will receive an email update within 24 hours.
• Your employer has been notified.

Reference: [case ID] | Request received: [timestamp]
```

**Ops Side — Withdrawal Notification (Addition to 6.1.2 Case Workbench)**
When consent is withdrawn:
- Case Workbench shows amber banner: "Candidate withdrew consent on [date]. Legal basis assessment required within 24 hours. [Assess Legal Basis]"
- [Assess Legal Basis] button opens Legal Basis Assessment Drawer:
  - For each check in progress: Can this check continue under Legitimate Interest / Statutory basis?
  - Options per check: Continue (document alternative legal basis) | Cancel (stop all processing)
  - KPMG Legal notification trigger (mandatory for Major/Critical checks continuing under alternative basis)
- After assessment: Case status updated, candidate notified of outcome

**Audit Events**
- `consent.withdrawal_requested` — candidate initiated, timestamp, session context
- `consent.withdrawal_confirmed` — candidate confirmed, timestamp
- `consent.legal_basis_assessment_completed` — ops assessment outcome per check
- `consent.alternative_basis_applied` — which checks continue under alternative basis, legal basis cited
- `case.status_changed_consent_withdrawn` — case state transition

---


---

## GAP-17 FIX: WCAG 2.1 Accessibility Requirements

### Addition to all Candidate Portal Pages — Item 21: Accessibility Requirements

Add standardized "20. Accessibility Requirements (WCAG 2.1 AA)" section to every Candidate Portal page design (6.3.x):

**Standard Accessibility Checklist for All Candidate Pages:**

```
20. Accessibility Requirements (WCAG 2.1 AA)

Keyboard Navigation:
- All interactive elements reachable via Tab key in logical reading order
- Focus indicator: 2px solid #0057B8 outline on all focused elements (minimum 3:1 contrast ratio)
- No keyboard traps — Escape key closes all modals/drawers, returns focus to trigger
- Skip-to-main-content link: first focusable element on each page

Screen Reader Compatibility:
- All form fields: visible label + aria-label or aria-labelledby
- All buttons: descriptive text (not just icons — "Submit application" not "→")
- Error messages: aria-live="polite" region, associated with field via aria-describedby
- Progress indicators: aria-valuenow, aria-valuemin, aria-valuemax, aria-label="Step N of M"
- Modals: role="dialog", aria-modal="true", aria-labelledby pointing to modal title, focus trapped inside modal while open
- Status updates (auto-save, validation): aria-live="polite" announcement

Color and Contrast:
- Body text: minimum 4.5:1 contrast ratio against background
- Large text (18pt+): minimum 3:1 contrast ratio
- Error states: never color alone — error icon + text label + border
- Status badges (Green/Amber/Red): include text label alongside color ("Clear ✓" not just green badge)

Images and Media:
- Decorative images: alt="" (empty alt, not absent)
- Informational images: descriptive alt text
- Document upload preview: alt text describing "Uploaded document preview — [document type]"

Timeout Handling:
- Session expiry warning: announced via aria-live="assertive" 60 seconds before timeout
- Timeout warning modal: keyboard accessible, focus moves to modal, can extend via keyboard

Touch Targets (Mobile):
- Minimum 44×44 CSS pixels for all interactive elements
- Adequate spacing between adjacent touch targets (minimum 8px gap)

Forms:
- autocomplete attributes on all applicable fields (name, email, tel, bday, country)
- Required fields: aria-required="true" + visible asterisk + legend explaining asterisk
- Error recovery: focus moves to first error on invalid submit, errors listed at top + inline

Page-Specific Additions:
[Each page lists any additional page-specific WCAG requirements]
```

**Page-Specific WCAG Additions:**

*Consent Page (6.3.1):*
- Scroll detection: timeout warning announced via screen reader when approaching 10 minutes on page
- E-signature: keyboard alternative (type-to-sign) must be equally accessible
- Language selector: aria-label="Select language", options listed with language name in that language

*Document Upload (6.3.3):*
- Camera capture: voice-activated file selection supported where device permits
- Quality feedback: "Image quality: Good" announced via aria-live when quality check completes
- Upload progress: progress bar with aria-valuenow updating every 10%

*Biometric Capture (6.3.4):*
- Active liveness challenge: text instruction + animated visual guide (not motion-only)
- Audio instruction option: each challenge step announced via audio (configurable — user can enable)
- Passive alternative: keyboard-accessible option to request passive liveness instead of active

*OTP Login (6.3.7):*
- OTP auto-fill (Android SMS listener): must not break keyboard navigation
- OTP field: each digit input is individually labelled: "OTP digit 1 of 6"

---
### 6.3.2 Page: Employment Entry Form

**1. Page Objective**
Capture structured, accurate employment history from the candidate, with smart validation that catches common fraud patterns and data errors before submission.

**2. Primary Actors** Candidate

**3. Key Workflows**
Add employer entries → Validate dates → Detect gaps → Detect overlaps → Provide gap explanation → Resubmission (specific field correction only)

**4. States**
Empty → Partially filled → Validated (no errors) → Validated (with warnings) → Submitted | Resubmission mode (specific fields locked/editable)

**5. Actions**
Add employer, fill fields, remove employer, acknowledge gap, explain gap, save and continue, go back, re-submit (if in resubmission mode)

**6. Data Blocks**
Per employer: company, designation, employment type, start/end date, location, HR contact, reason for leaving, supervisor; Gap explanations; Reference contacts (if package includes)

**7. UI Regions**
- Progress bar (top, persistent)
- Employer entry cards (repeating, collapsible after filling)
- [Add Another Employer] button
- Gap detection alert zone (appears between cards where gap detected)
- [Save & Continue] bottom bar

**8. Cards**
- Employment Entry Card (per employer): All fields for one employer, collapsible, edit icon, remove button, validation status badge
- Gap Alert Card: "Gap detected [date] to [date] — [N months]. Please explain." Expandable: free text explanation field + optional document upload (gap certificate, study, freelance, break declaration)
- Dual Employment Warning Card: "These two positions overlap by [N months]. Please verify your dates or explain."

**9. Tables** None — card-based repeating form

**10. Drawers**
- Employer Search Drawer: Auto-suggest known company names (from company database); handles name variations ("Infosys Ltd" vs "Infosys Limited" vs "Infosys BPO")
- Reference Guide Drawer: "What is a supervisor contact used for? Will they be contacted?" — FAQ for candidate

**11. Modals**
- Remove Employer Modal: "Are you sure you want to remove [Company]? This entry will be deleted." (prevents accidental removal)
- Gap Acknowledgment Modal: If candidate skips gap explanation — "You have an unexplained gap. Proceeding without explanation may delay your verification. Continue anyway?"

**12. Tabs** None — sequential section

**13. Filters** None

**14. Smart Validation Components**
- Employment gap detector: Triggered on date entry. Calculates gaps > 30 days between consecutive entries. Shows inline gap card.
- Dual employment detector: Triggered on date overlap between two entries. Shows warning card.
- Date validation: Start date < End date; End date ≤ today; "Currently working" toggle disables End date.
- Future date blocker: Start date cannot be in future.
- Company name deduplication: Warning if same company appears twice without explanation.

**15. Resubmission Mode (Critical)**
- Approved fields: Read-only with lock icon. Tooltip: "This information has been verified and cannot be changed."
- Flagged fields: Editable with orange border + ops remark displayed above: "KPMG: Please provide the correct end date for ABC Corp Employment. The date entered does not match our records."
- Submit button label changes: "Submit Updated Information" (not "Submit Application")
- Confirmation: "Your updated information has been received. We will continue your verification."

**16. Alerts/Banners**
- "You have [N] employers with incomplete information — please complete before continuing."
- "Gap detected in your employment history — please review the highlighted sections."

**17. Timeline/Audit**
Each submission and resubmission is an audit event: fields submitted, timestamp, session ID. Resubmission events clearly distinguished from original submission.

**18. SLA Components** None direct — but delay in candidate form completion directly impacts overall case SLA.

**19. AI Components**
Gap detection uses date arithmetic (deterministic, not ML). Employer name normalization uses fuzzy match. OCR cross-check (after ops reviews employment documents) is on the ops side — not in candidate form.

**20. Mobile Considerations**
- Keyboard type optimization: number keyboards for phone/date fields; text for name fields
- Date pickers: mobile-native date pickers (not custom dropdowns)
- Collapsible employer cards keep form manageable on mobile
- "Add Another Employer" button: sticky at bottom of viewport (not buried after long form)
- Camera upload for employment documents: integrated in same form step (optional upload)

---


---

## GAP-EXP-M7 FIX: Contractor / Gig Employment Fields — Candidate Portal Employment Form

### M-7 | Contractor / Gig Employment Fields — Missing from Candidate Portal Form

**RFP Reference:** RFP 4.9

**RFP Text:**
> *"Gig/contractor checks — Support contractor history checks and vendor employment validations"*

**Verdict:** EXPLICIT

**Analysis:**
RFP 4.9 explicitly names gig/contractor checks as a required verification capability. The current Employment Entry Form (6.3.2) captures fields for salaried employment only (company, designation, start/end date, HR contact). Contractor-specific employment has a fundamentally different data structure: engagement-based (not tenure-based), often without an HR contact, with a Statement of Work (SOW) reference, platform-based work, and multiple simultaneous engagements. Without contractor-specific form fields, the platform cannot capture the data required to perform RFP 4.9 gig/contractor checks.

**Impact:**
- Contractor candidates are forced to misuse salaried employment fields, resulting in incorrect data capture and failed verification.
- Ops cannot execute contractor history checks without engagement type, SOW reference, or platform identity.
- Growing gig workforce at KPMG clients (IT contractors, management consultants, platform workers) have no supported submission path.

**Recommendation:**
Add contractor-specific form fields to 6.3.2 Employment Entry Form, activated by an employment type selector.

---

### Addition to 6.3.2 Page: Employment Entry Form — Contractor/Gig Fields

**Employment Type Selector (add as Item 0 — before all other form fields):**
```
EMPLOYMENT TYPE
○ Salaried/Full-time (permanent employee)
○ Contractor / Consultant (fixed-term, SOW-based)
○ Gig / Platform Worker (app-based, freelance)
○ Self-Employed / Proprietor
○ Internship / Trainee
○ Currently unemployed (explain gap)
```

**Conditional Form Fields — CONTRACTOR / CONSULTANT Mode:**

When "Contractor / Consultant" is selected, show these fields instead of/in addition to standard employment fields:

```
ENGAGEMENT DETAILS
──────────────────────────────────────────────────
Contracting Company / Agency: [_______________]
(Leave blank if directly contracted)

End Client / Project Company: [_______________]
(The company you were placed at)

Engagement Type:
○ Fixed-term contract   ○ Project-based (SOW)
○ Body shopping         ○ Consulting engagement

SOW / Purchase Order Reference: [_______________]
(Statement of Work number, PO number, or contract ID)

Engagement Start Date: [date picker]
Engagement End Date: [date picker] / ○ Ongoing

Role / Designation during engagement: [_______________]

Approximate monthly billing rate: [_______________]
(Optional — used for ITR cross-check)

Contracting Manager / Engagement Lead: [_______________]
Contracting Manager Contact (email/phone): [_______________]

Was this engagement through a platform?
○ Yes → Which platform? [Toptal / Upwork / LinkedIn / Other: ___]
○ No
──────────────────────────────────────────────────
```

**Conditional Form Fields — GIG / PLATFORM WORKER Mode:**

When "Gig / Platform Worker" is selected:
```
PLATFORM WORK DETAILS
──────────────────────────────────────────────────
Platform(s) worked on: [multi-select or text entry]
□ Ola/Uber     □ Swiggy/Zomato   □ Urban Company
□ Upwork       □ Fiverr          □ Toptal
□ Other: [_______________]

Platform ID / Username: [_______________]
(Your public profile handle or registered ID)

Nature of work: [_______________]

Active period: From [date] To [date] / ○ Still active

Average monthly income during period: [_______________]
(Optional — for ITR cross-check)

Any linked GST number? [_______________] ○ N/A
──────────────────────────────────────────────────
```

**Validation Rules (add to Item 14 — Smart Validation Components):**

- Contractor engagement type: If "SOW-based," SOW reference field is mandatory.
- Gig worker: Platform ID is recommended (soft warning if blank, not hard block).
- If contractor/gig: HR Contact field label changes to "Engagement Manager / Contact" (less intimidating than "HR contact" for non-employees).
- Date validation: Same as salaried (start < end; no future dates).
- Contractor can have overlapping engagements — overlap detection shows info card ("Overlapping contractor engagements are common and will be reviewed") not a warning card.

**Gap Detection Adaptation:**
- Gaps in contractor history: gap alert card message changes to "Gap detected — if this was between engagements, please indicate 'Between contracts' and upload any available documentation."

**Ops-Side Impact (addition to 6.1.8 Employment Check Workspace):**
- Employment check workspace receives employer type flag from candidate form: "Contractor — SOW engagement"
- Ops sees contractor-specific data panel: engagement type, SOW reference, platform, contracting manager
- Verification approach changes: instead of HR outreach, ops sends structured employer outreach to contracting manager or platform; ITR cross-check with billing rate; GST verification if GST number provided

**Part 5 IA Impact:** No new page needed — this is a form field addition to the existing Employment Entry Form. Updates the Employment Form component specification in Part 6.


### 6.3.3 Page: Document Upload Center

**1. Page Objective**
Collect high-quality document uploads from mobile-first candidates with real-time AI quality feedback — minimizing insufficiency rates and re-submission cycles.

**2. Primary Actors** Candidate

**3. Key Workflows**
View required documents checklist → Upload per document (camera or file) → Real-time quality check → Review OCR extraction → Confirm or retake → Overall completeness check → Proceed

**4. States**
Checklist displayed → Per-document: Not uploaded / Uploading / Processing (AI quality) / Good / Fair / Poor (blocked) / Insufficient (returned by ops — resubmission mode)

**5. Actions**
Upload document (camera or file), retake, replace, confirm OCR extraction, skip optional document, proceed to next section

**6. Data Blocks**
Required documents list (from package config), per-document upload state, AI quality score, OCR extraction result, insufficiency remarks (if returned by ops)

**7. UI Regions**
- Top: Document checklist progress ("4 of 6 required documents uploaded")
- Per-document: Upload widget card
- Bottom: [Proceed] button (disabled until required documents at Good/Fair quality)

**8. Cards (per document)**
- Not Uploaded Card: Document name, type hint, accepted formats (PDF / Word / Excel / JPG / PNG / ZIP), [Upload] and [Use Camera] buttons. Format hint below document name: e.g. "Accepted: PDF, Word, JPG, PNG" for most docs; "Accepted: PDF, Word, Excel, ZIP" for payslips/salary docs.
- Uploading Card: Progress bar (upload + AI processing)
- Quality Result Card (Good): Green checkmark, OCR extraction preview ("We extracted: Name: Prudhvi, DOB: 15-Jan-1990. Correct?")
- Quality Result Card (Fair): Amber indicator, "Quality is acceptable but may cause delays. Retake recommended." [Retake] [Use anyway]
- Quality Result Card (Poor): Red indicator, specific error: "Image is blurry — please retake in better lighting." [Retake] button (proceed blocked until retaken or skipped if optional)
- Insufficient Card (resubmission): Orange border, ops remark: "KPMG: Please re-upload your PAN card — the document appears cropped." [Re-upload] button

**9. Drawers**
- Document Example Drawer (per document type): Good example image, bad example images with labeled issues, tips for mobile capture
- Supported Formats Drawer: Full accepted formats reference — sourced from platform policy (4.7.1):

  | Format | Extensions | Max Size | Notes |
  |---|---|---|---|
  | PDF | .pdf | 10 MB | Primary format — full inline preview |
  | Image | .jpg .png | 10 MB | Auto-compressed to <3 MB on mobile before upload |
  | Word | .docx | 10 MB | Converted to PDF for viewing; original preserved |
  | Excel | .xlsx .xls | 10 MB | Converted to PDF for viewing; original preserved |
  | ZIP | .zip | 50 MB extracted, max 20 files | Each file inside is checked individually; no nested ZIPs |

  Compression note: "For faster uploads on mobile, images are automatically compressed before sending. No quality relevant to verification is lost."
  Unsupported formats: "Files like .mp4, .exe, .pptx are not accepted. Convert to PDF or JPG before uploading."

**10. Modals**
- Camera Access Modal: "KCheck needs camera access to capture your documents. [Allow] [Deny — use file upload instead]" + explanation of why
- OCR Confirmation Modal: "We extracted the following information from your document. Please confirm this is correct." [fields] [Confirm] [Incorrect — edit]
- Skip Optional Modal: "Skipping [document] may delay your verification. [Skip Anyway] [Upload Now]"

**11. Alerts/Banners**
- "You are missing [N] required documents — please upload before proceeding."
- "Poor quality document: please retake [document name]. Tip: [specific advice]."
- "All required documents uploaded — you can proceed to the next step."
- [C-02 NEW] "ZIP file received — extracting [N] documents. Each document will be quality-checked individually. This may take a few moments." (blue, shown immediately after ZIP upload — auto-dismisses when extraction complete)
- [C-02 NEW] "Your Word document is being converted for secure viewing. The original file is saved." (blue, shown for DOCX uploads — auto-dismisses on completion)
- [C-02 NEW] "Your Excel file is being converted for secure viewing. The original file is saved." (blue, shown for XLSX uploads — auto-dismisses on completion)
- [C-02 NEW] "ZIP file rejected — contains a ZIP inside it. Please extract and upload each document separately." (red, blocking)
- [C-02 NEW] "ZIP file rejected — contains [N] files. Maximum allowed is 20 files per ZIP." (red, blocking)
- [C-02 NEW] "Unsupported file type: [filename]. Accepted formats are PDF, Word, Excel, JPG, PNG, and ZIP." (red, per-file blocking)

**12. AI Components (core feature of this page)**
- Quality Scoring: Every upload → OCR + quality analysis within 3 seconds. Returns: quality tier (Good/Fair/Poor), specific feedback text, extracted field values
- Quality Feedback Text: Generated from model (not static text): "Glare detected on top-right corner. Tilt the document slightly to reduce reflection." "Text in bottom section is partially obscured. Ensure all edges are within frame."
- OCR Preview: Extracted fields shown to candidate with visual confidence indicators. Candidate confirms or flags error. Discrepancies between OCR and candidate-entered data (from personal form) highlighted for candidate to resolve.
- Presentation Attack Detection (background): Camera-only enforcement; gallery photo allowed but flagged. Screenshot of screen (moiré pattern detection) flagged. Returned to ops for manual review.
- [C-02 NEW] Format-aware processing pipeline (per platform policy 4.7):
  - PDF / JPG / PNG: Direct OCR + quality scoring (existing pipeline)
  - DOCX / XLSX: Virus scan → server-side PDF conversion (LibreOffice headless) → OCR on converted PDF → quality score based on converted output. Note: quality feedback shown to candidate reflects converted PDF quality, not original file quality. AI fraud detection runs on converted PDF.
  - ZIP: Extraction pipeline (4.7.2) → each extracted file routed to its own format pipeline → per-file quality scores shown as a checklist: "Document 1 (degree_certificate.pdf): Good | Document 2 (payslip.xlsx): Converted — Good | Document 3 (letter.docx): Converted — Fair"

**13. Evidence Components**
Document viewer in OCR confirmation shows extracted bounding boxes on the uploaded image — candidate sees exactly what was read.

**14. Mobile Considerations**
- Camera integration is primary upload method on mobile (not file upload)
- Camera viewfinder with document outline guide (align document to frame)
- Auto-capture when document fills frame (hands-free for one-handed use)
- Flash toggle for dark environments
- Capture quality check before leaving camera view — immediate feedback ("Retake now?" vs navigating back)
- File size: auto-compress on device before upload (target: < 3MB per document)
- Upload queue: if on poor connectivity, queue uploads and sync when connection improves (offline resilience)
- Progress indicator: visible during slow mobile upload

---

### 6.3.4 Page: Biometric Capture

**1. Page Objective**
Frictionless, accessible biometric identity verification that works across variable mobile camera quality and lighting conditions while being robust against fraud attacks.

**2. Primary Actors** Candidate

**3. Key Workflows**
Consent confirmation → Camera permission → Guide displayed → Challenge completion → Processing → Result display (Match/Retry/Escalate)

**4. States**
Consent required (for biometric) → Camera permission → Guide active → Challenge in progress → Processing → Matched / Retry required / Manual escalation triggered

**5. Actions**
Confirm biometric consent, grant camera permission, follow liveness challenge, retry (up to 3 attempts), skip to manual escalation (after 3 failures)

**6. Data Blocks**
Biometric consent record, liveness challenge result, face match score, attempt count, failure reasons, device fingerprint, lighting quality metric, escalation flag

**7. UI Regions**
- Top: Consent reminder ("Your selfie will be compared to your ID documents for identity verification")
- Center: Camera viewfinder with face alignment guide (oval overlay)
- Challenge instructions: Text + animated guide per step
- Result zone: Match result display after processing
- Bottom: Action button (changes per state: [Begin] / [Retry] / [Continue])

**8. Cards**
- Privacy Assurance Card: "Your biometric data is used only to verify your identity. It is not stored after matching." (visible before camera opens)
- Result Card (Success): Green checkmark, "Identity verified — your face matched your ID documents."
- Result Card (Retry): Specific error + corrective guidance. Attempt counter visible.
- Result Card (Escalate): "We were unable to verify your identity automatically. Your case will continue with a manual review." (soft messaging — does not alarm or accuse)

**9. Drawers** None during flow (minimize distraction during biometric capture)

**10. Modals**
- Biometric Consent Modal (full-screen on mobile): "Your face scan is sensitive personal data under privacy laws. By continuing, you consent to: [1] capturing your face image, [2] comparing it to your ID documents, [3] storing only the match result (not the image). You have the right to withdraw this consent (but verification cannot continue without it)." [Agree] [Decline]
- Camera Permission System Dialog: Native OS permission request (cannot be customized but explained before it appears)
- Accessibility Alternative Modal: "Unable to complete the automated check? A KPMG reviewer will manually verify your identity using the documents you've uploaded." (after 3 failed attempts — soft exit, no hard block)

**11. Active Liveness Challenge UX (detailed)**
- Frame 1: Face centered in oval — animated pulse, "Hold still — we're checking..."
- Frame 2: Blink prompt — eye blink animation, "Please blink slowly" — waits for detected blink
- Frame 3: Turn prompt — animated head turning left — "Slowly turn your head to the left"
- Frame 4: Return to center — "Look straight ahead"
- Completion animation: Brief green flash overlay, processing spinner
- Each step: text instruction + animated visual guide + optional audio instruction (accessibility)

**12. Passive Liveness (alternative for accessibility or package type)**
- Single selfie with quality assessment (no movement required)
- Guide: "Take a clear selfie looking straight at the camera"
- Quality check: lighting, face coverage, no glasses/hat/mask guidance

**13. Failure Handling UX**
- Attempt 1: "[Specific reason]. Tips: [targeted advice]. [Try Again]"
- Attempt 2: Different specific advice. Attempt counter shown: "Attempt 2 of 3."
- Attempt 3: Final attempt. Post-failure: "Manual review will be performed. Please continue."

**14. AI Components**
- Face match: Selfie vs ID document photo (face region extracted). Match score (not shown to candidate — shown to ops as categorical Good/Fair/Poor match). Threshold configurable in Super Admin.
- Liveness detection: Active or passive model. Returns: Passed/Failed + reason code (to ops, not to candidate).
- Deepfake detection: Background signal on submitted selfie. Flag to ops if detected (candidate not informed — avoids coaching).
- Presentation attack: Screen photo detection (moiré pattern), 3D mask detection signals.

**15. Evidence Components**
- Selfie stored: Face-cropped thumbnail only (not full image) in immutable object storage with case reference. Not retained after verification period expires.
- Match result stored: Score category (not raw score to candidate-facing systems) + model version + timestamp.

**16. Alerts/Banners**
- Lighting warning: "Poor lighting detected. Move to a brighter location for better results." (shown before capture starts if ambient light API detects low light)
- Glasses warning: "Remove glasses if possible for better face matching." (soft, not blocking)
- "Attempt [N] of 3" counter bar

**17. SLA Components** None direct — biometric is one step in overall form completion

**18. Timeline/Audit**
- Each attempt logged: timestamp, result, reason code, device fingerprint, model version
- Final result logged: Match/Fail/Escalated, attempt count, model version used
- Override event logged (if ops manually overrides escalated case)

**19. Mobile Considerations**
- Camera fills available viewport (not small inline frame) — critical for face detection quality
- Minimal UI during challenge (no distracting elements in camera view)
- Instructions font: minimum 16px (must be readable while holding phone at arm's length)
- Portrait orientation enforced during challenge
- Auto-torch: suggest enabling torch in low light (iOS/Android torch API where available)
- Horizontal orientation lock prompt: "Please hold your phone upright for this step"

**20. Compliance Notes**
- Biometric data = special category personal data under DPDP Section 2 and GDPR Article 9
- Separate, explicit, informed, revocable consent required before any biometric capture
- Data minimization: match result stored, not full biometric template beyond what's needed for verification period
- Retention: biometric data deleted at end of retention period (configurable per tenant)

---

### 6.3.5 Page: Application Status Page

**1. Page Objective**
Give candidates appropriate visibility into their BGV progress without exposing ops internals. Reduce support contact by proactively answering "where is my verification?"

**2. Primary Actors** Candidate

**3. Key Workflows**
Check status → Identify pending actions → Re-submit if insufficient → Contact support → Download consent receipt

**4. States**
Submitted (awaiting verification start) → Verification In Progress → Action Required (insufficient) → Verification Complete → Report Delivered (candidate notified)

**5. Actions**
View status, respond to insufficient (re-enter flagged information), contact support, download consent receipt, file dispute

**6. Data Blocks**
Overall status, per-check status (high-level only), pending actions (insufficient fields), expected completion estimate, support contacts

**7. UI Regions**
- Top: Client-branded header
- Center: Overall progress bar (Submitted → In Verification → Complete)
- Per-check status cards (simplified — no ops details)
- Action required zone (prominent — if candidate action needed)
- Support zone (bottom)

**8. Cards**
- Overall Status Card: Big status label, stage progress bar
- Per-Check Status Card: Check name, status icon (In Progress / Awaiting Your Action / Complete)
- "Action Required" Card (conditional — high priority): "KPMG has requested additional information for [check type]. [Provide Information →]" — orange border, above all other content
- Expected Completion Card: Date range estimate ("Expected by [date range]")
- Consent Receipt Card: Download link (persistent — always accessible)

**9. Alerts/Banners**
- Action Required Banner (sticky top): "Action required — please provide additional information to continue your verification." [Take Action] button
- Completion Banner: "Your background verification is complete. [Your employer name] has been notified."

**10. Drawers**
- Check Details Drawer (per check, optional): Expanded info about what the check involves (educational, not internal details). "What is an employment check?" type content.
- Support Drawer: Chat widget + FAQ + contact options

**11. Modals**
- Dispute Filing Modal: Quick access from status page. "I want to challenge a finding." → Opens dispute form pre-populated with case reference.

**12. AI Components** None visible to candidate

**13. SLA Components**
Expected completion estimate (calculated from case creation date + package avg TAT — not revealing internal SLA mechanics)

**14. Mobile Considerations**
- This is the most common mobile use case (candidates checking on their phone)
- Status must load in < 2 seconds on 4G
- Action Required card: large tap target, sticky on mobile scroll
- All elements finger-tap friendly (no hover-only interactions)
- Push notifications deep-link into this page directly

---



---

## GAP-16 FIX: Step-Up Verification Page — Candidate Portal

### New Page: 6.3.15 Step-Up Verification

**1. Page Objective**
Present additional identity verification challenges to candidates when risk signals exceed configured thresholds, without alarming the candidate or revealing the specific risk signal.

**2. Primary Actors**
Candidate

**3. Key Workflows**
Risk signal detected → System pauses candidate flow → Step-up page rendered → Candidate completes challenge → Risk state updated → Candidate returned to interrupted step OR escalated to ops

**4. Trigger Conditions (background — not shown to candidate)**
- Device risk score above threshold
- Geo-location mismatch with declared address
- OTP failure pattern (3+ failed attempts)
- Document/biometric risk signal
- High-risk role/package requiring enhanced identity

**5. States**
Challenge Not Presented → Challenge Presented → Attempt In Progress → Passed (returned to flow) → Failed (retry available) → Max Attempts Exceeded (escalated to ops)

**6. Actions**
Complete challenge, retry (up to 3 attempts), contact support, optionally escalate to video KYC

**7. Data Blocks**
Step-up trigger type (not shown to candidate — ops-internal), challenge method, attempt count, result per attempt, final outcome, device/session context at trigger

**8. UI Regions**
- Header: client branding (persistent)
- Step-up explanation card (generic — never reveals specific risk signal)
- Challenge interface (changes per challenge type)
- Attempt counter (shown after first failure)
- Support link (persistent)

**9. Cards**
- Explanation Card: Generic, non-accusatory language. Examples:
  - "Additional verification required: We need to confirm your identity before continuing."
  - "Security check: Please complete this step to protect your application."
  - Never: "Fraud detected", "Suspicious activity", "Your device is flagged"
- Result Card (Success): "Identity confirmed — continuing your application."
- Result Card (Retry): Specific corrective guidance (e.g., "Please ensure good lighting", "Remove glasses", "Use a different network connection")
- Result Card (Escalated): "We're having trouble completing this step automatically. A KPMG team member will review your application. You'll receive an update within [timeframe]."

**10. Challenge Types and Interfaces**

Second-Channel OTP:
- "We've sent a verification code to your [email/alternate mobile]"
- OTP entry field (6-digit, same as login OTP)
- Resend button (60s cooldown)
- Use alternate channel option

Selfie Re-Capture:
- "Please take a new selfie to confirm your identity"
- Camera viewfinder with face alignment guide
- Same liveness + face match flow as 6.3.4 Biometric Capture
- Attempt counter shown

ID Re-Upload:
- "Please re-upload your [document type] for clearer verification"
- Same upload widget as 6.3.3 Document Upload
- Specific guidance for the document type required

Video KYC Escalation (for packages requiring it or after biometric failure):
- "A live verification session is required. Please choose a convenient time."
- Scheduling calendar (available slots from ops)
- Confirmation: "Session booked for [date/time]. You'll receive a link 10 minutes before."

**11. Drawers**
- Support Drawer: "Having trouble with this step? Chat with us." — opens chat widget
- What is this? Drawer: FAQ explaining why additional verification may be needed (no specific risk signal revealed)

**12. Modals**
- Max Attempts Modal: "We've been unable to complete this verification automatically. Your application has been flagged for review by the KPMG team. You'll receive an email update within [timeframe]. No further action is required from you right now." [Okay] button.
- Video KYC Confirmation Modal: Session time, what to prepare (ID document, good lighting, quiet location), technical requirements (camera access needed).

**13. Alerts/Banners**
- Attempt counter: "Attempt [N] of 3" — shown after first failure only (not on first attempt — avoids anxiety)
- Connectivity warning: "Poor connection detected — this may affect video verification quality"

**14. SLA Components**
- Pending step-up cases: ops dashboard shows "Pending Step-Up" state with time waiting
- If candidate does not complete step-up within 72 hours: system treats as abandoned (same as session expiry — OTP re-auth required)

**15. AI Components**
- Risk signal assessment runs in background — candidate never sees raw signal
- After successful step-up: risk score updated (successful step-up reduces open risk state but does not erase original signal from audit trail)
- After failed step-up: additional risk flag added to case

**16. Evidence Components**
- Biometric evidence from step-up stored identically to original biometric (same evidence store, labeled as "Step-Up Verification — [timestamp]")
- ID re-upload evidence stored as "Step-Up Document Re-Upload"

**17. Timeline/Audit**
Every step-up event logged: trigger signal type (ops-visible only), challenge method, attempt number, result, device context, timestamp. Included in case audit pack.

**18. Mobile Considerations**
Step-up is triggered primarily on mobile. Full mobile optimization required:
- Camera challenges: full-screen camera (same as biometric page 6.3.4)
- OTP: numeric keyboard auto-triggered
- Support: one-tap access (not buried in footer)
- Video KYC scheduling: mobile-native calendar date picker

**19. Ops Visibility (not candidate-facing)**
In Case Workbench (6.1.2), if case has pending step-up:
- Status indicator in check navigator: "⏸ Pending Step-Up Verification"
- Banner: "Candidate has been presented with a step-up challenge. Awaiting completion."
- Ops can override step-up and manually advance if appropriate (Senior Reviewer role, with mandatory note)

**20. Part 5 IA Addition**
Add to Candidate Portal IA (Part 5.3) under section 3 (Verification Form):
```
├── 3.9 Step-Up Verification (Triggered programmatically)
│   └── Page: Additional Identity Verification
│       Purpose: Challenge candidate when risk signals exceed configured thresholds
│       Trigger: Automatic — based on risk engine evaluation
│       Challenge types: Second-channel OTP | Selfie re-capture | ID re-upload | Video KYC
│       States: Presented → Attempt → Passed | Retry | Escalated
```

---
## 6.4 VENDOR PORTAL — Page Design Depth

---

### 6.4.1 Page: Assignment Inbox

**1. Page Objective**
Give desk vendors a clear, prioritized view of their new assignments with all information needed to acknowledge and begin work.

**2. Primary Actors** Vendor Verifier, Vendor Team Lead

**3. Key Workflows**
Receive assignment notification → Review assignment details → Access candidate documents for this check → Acknowledge (starts vendor SLA clock) → Begin verification work

**4. States**
New (unacknowledged) → Acknowledged → In Progress → Submitted → Completed | Declined (with reason)

**5. Actions**
Acknowledge assignment, decline (with reason), view documents, begin evidence submission, contact KPMG ops (query)

**6. Data Blocks**
Assignment: Case reference (anonymized), check type, geography, SLA deadline, documents relevant to this specific check (not full case), KPMG assignment notes

**7. UI Regions**
- Top: New assignments count badge
- Table: All new assignments
- Per-row: Quick expand for key details without leaving list
- Action bar (per row): [Acknowledge] [View Documents] [Decline]

**8. Cards**
- New Assignment Summary Card (expandable per row): Check type, geography, documents attached count, SLA deadline, assignment notes, [Acknowledge] button
- SLA Urgency Card: Color-coded SLA health (Green/Amber/Red based on deadline)

**9. Tables**
- Assignment Table: Ref number | Check type | Geography | Documents attached | SLA deadline | Assigned date | [Actions]

**10. Drawers**
- Document Access Drawer: View/download candidate documents relevant to this specific check (scoped — vendor does not see full case documents). Documents are purpose-limited to what the vendor needs.
- Decline Drawer: Reason selector (Capacity / Geography not covered / Conflict of interest / Other) + notes + confirm. Declines route back to KPMG ops for reassignment.

**11. Modals**
- Bulk Acknowledge Modal: "Acknowledge all [N] new assignments? SLA clock starts for all." [Confirm]

**12. Alerts/Banners**
- "New assignment — SLA deadline in 48 hours. [Acknowledge Now]" — urgent amber
- "You have [N] new assignments awaiting acknowledgment." — notification banner on login

**13. SLA Components**
SLA clock starts from acknowledgment moment (not assignment moment — incentivizes prompt acknowledgment). Countdown visible per assignment. Color transitions at 50% / 20% remaining.

**14. Compliance**
Candidate documents visible to vendor are purpose-limited — vendor sees only what's needed for their specific check type. No PII beyond what's necessary (data minimization for subprocessors — RFP 22.3). All vendor document access events are logged in case audit trail.

**15. Mobile Considerations**
Vendors are primarily desktop. Mobile: check new assignments, acknowledge. Evidence submission on desktop preferred.

---



---

## GAP-19 FIX: Vendor Revalidation Queue

### New Page: 6.4.9 Revalidation Queue

**1. Page Objective**
Provide vendors with a dedicated, clearly labeled queue for revalidation assignments — distinguishing them from standard new assignments and providing full context about why revalidation was triggered and what prior work exists.

**2. Primary Actors**
Vendor Verifier (executes), Vendor Supervisor (monitors and approves)

**3. Key Workflows**
Receive revalidation notification → Review context package (prior evidence + rejection reason) → Acknowledge assignment → Execute re-verification → Submit with supervisor QC

**4. States**
New (unacknowledged) | Context Reviewed | In Progress | Supervisor QC Pending | Submitted | Completed

**5. Actions**
Acknowledge, view context package, begin evidence capture, submit, contact KPMG ops (query)

**6. Data Blocks**
Revalidation assignment ID, revalidation type tag, check type, geography, context package (prior vendor evidence — anonymized, rejection reason, open questions from ops), SLA from revalidation date, parent case reference (anonymized)

**7. UI Regions**
- Top: Revalidation count badge (distinct from standard new assignments)
- Revalidation type filter tabs: All | Fallback Assignment | Independent Recheck | Parallel Corroboration | Site Visit Reassignment
- Revalidation cards list

**8. Cards (per revalidation assignment)**
- Revalidation Card:
  - Tag: [Fallback Assignment] / [Independent Recheck] / [Parallel Corroboration] / [Site Visit Reassignment] — color-coded badge
  - Check type, geography, SLA deadline (from revalidation date)
  - Context summary: "[Prior vendor] attempted this check but [rejection reason]. Please verify independently."
  - [View Context Package] [Acknowledge] buttons
  - Important note: "This is an independent verification. Your result will be compared against prior findings."

**9. Drawers**
- Context Package Drawer: Read-only view of prior evidence package contents:
  - Prior vendor's work (what they found, what they captured — without revealing prior vendor identity)
  - Rejection/trigger reason (in neutral language: "Previous verification was inconclusive" / "SLA exceeded without resolution" / "Evidence quality insufficient")
  - Open questions from KPMG ops (specific things to verify or clarify)
  - Candidate check data (what was claimed — scoped to this check type only)
  - Evidence checklist: what KPMG needs in the revalidation submission
  - Note: "Prior vendor identity is confidential. Focus on independent verification."
- Evidence Submission Drawer: Same as standard evidence submission (6.4.2) — check-type specific structured form + evidence upload + outcome declaration

**10. Modals**
- Acknowledge Revalidation Modal: "You are accepting a [type] assignment. Your result will be reviewed alongside prior findings by KPMG ops. SLA: [deadline]. [Acknowledge]"
- Decline Revalidation Modal: Reason required — same as standard decline (6.4.1). Routes back to KPMG for next vendor in priority list.

**11. Alerts/Banners**
- "[N] revalidation assignments are waiting — these are time-sensitive" — amber banner on vendor dashboard
- "Parallel Corroboration: Your result will be compared with another independent verification. Do not contact the same sources as indicated in the context package." — informational for parallel assignments
- "SLA breach approaching — this revalidation is due in [N] hours" — red when <20% time remaining

**12. SLA Components**
- Revalidation SLA starts from revalidation assignment date (NOT from original assignment date)
- Shown clearly: "SLA: [deadline] from [revalidation date]" — distinct from original assignment date
- SLA breach tracked separately in vendor scorecard (revalidation breach vs standard breach)

**13. Part 5 IA Addition**
Add to Vendor Portal IA (Part 5.4) under Case Queue:
```
├── 2.4 Revalidation Queue
│   └── Page: Revalidation Assignment Queue
│       Purpose: Dedicated queue for fallback, recheck, and parallel verification assignments
│       Tags: Fallback Assignment | Independent Recheck | Parallel Corroboration | Site Visit Reassignment
│       Context Package: Prior evidence (anonymized), rejection reason, open questions
│       Note: Prior vendor identity always hidden
```

---
### 6.4.2 Page: Evidence Submission Interface

**1. Page Objective**
Enable vendors to submit structured, auditable verification findings — replacing email with structured data that feeds directly into the ops workbench.

**2. Primary Actors** Vendor Verifier

**3. Key Workflows**
Select case from active queue → Complete check-type-specific structured form → Upload supporting evidence → Declare outcome → Submit

**4. States**
Active (in progress) → Submitted (read-only) | Returned for correction (if QC flags an error on the submission)

**5. Actions**
Fill structured form, upload evidence, declare outcome, add notes, submit, view previous submission (read-only)

**6. Data Blocks (by check type)**

Employment Form Fields:
- Confirmed start date (calendar picker)
- Confirmed end date (calendar picker or "Currently Employed" toggle)
- Confirmed designation/job title
- Department (optional)
- Direct reporting manager name (optional)
- Reason for leaving (dropdown: Resignation / Termination / Redundancy / Contract end / Unknown / Refused to disclose)
- Rehire eligibility (Yes / No / Conditionally / Refused to disclose)
- Confirmation method (Verbal-phone / Written-email / Employer portal / In person)
- Name + title of person who confirmed (for verbal/in-person confirmations)

Education Form Fields:
- Enrollment confirmed (Yes / No)
- Degree conferred (Yes / No / Discontinued)
- Actual year of passing
- Actual percentage/CGPA (or "Refused to disclose — only confirm/deny")
- Course/program name (as per institution records)
- Roll number / Registration number (if institution provided)

Legal Form Fields:
- Courts searched (checklist — which courts were queried)
- Cases found (Y/N). If Yes: case number, petitioner/respondent, case type, status (Pending/Disposed/Convicted), date of judgment
- Identity confirmed (same person match criteria: Name match / DOB match / Address match / Photo match)
- Outcome: No adverse record / Adverse record found / Unable to confirm identity

**7. UI Regions**
- Left: Case reference panel (check type, candidate reference number, SLA)
- Center: Structured form (check-type-specific)
- Right: Evidence upload panel
- Bottom: Outcome declaration + submit

**8. Cards**
- SLA Countdown Card: Persistent during form fill — deadline visible at all times
- Pre-fill Alert Card (if candidate data available to compare): "Candidate claimed: [X]. Please confirm or correct."

**9. Tables** None in submission form

**10. Drawers**
- Evidence File Drawer: Upload panel — file drop or browse. Accepted formats: **PDF / DOCX (Word) / XLSX (Excel) / JPG / PNG / ZIP** (per platform policy 4.7). Each file linked to specific finding. Mandatory for Discrepancy Found outcomes.
  - DOCX/XLSX: automatically converted to PDF for ops viewing; original preserved
  - ZIP: extracted and each file individually quality-checked; max 20 files, 50 MB extracted
  - Max per file: 10 MB; ZIP max extracted size: 50 MB
- Field Guide Drawer: "What to fill in this field" — help for each structured field

**11. Modals**
- Outcome: Discrepancy Found Modal: Opens structured discrepancy detail form when "Discrepancy Found" selected. Fields: discrepancy type, specific field with discrepancy, candidate claimed value, actual confirmed value, severity assessment.
- Unable to Verify Modal: Reason required (Company closed / No response after [N] attempts / Contact refused / Not enough information). Attempt log requested (date + method of each contact attempt).
- Submit Confirmation Modal: "You are submitting findings for [Case ref]. Outcome: [X]. This submission is final and will be visible to KPMG ops immediately." [Confirm Submit]

**12. Alerts/Banners**
- "Evidence upload required for discrepancy findings — please attach supporting documents." (red, blocking submit if discrepancy declared without evidence)
- "SLA deadline approaching in [N] hours." (amber when <20% time remaining)
- "This submission has been returned for correction: [QC error reason]. Please review and resubmit." (if QC returns the submission)

**13. Compliance**
Submission is immutable after submit (read-only). Any correction requires KPMG ops to return it to vendor (audit trail). All submission events logged in case audit trail (vendor ID + timestamp + outcome declared).

**14. Mobile Considerations**
Desk vendors are desktop-primary. Mobile: view submission status, receive notifications. Submission itself on desktop.

---

### 6.4.3 Page: Vendor SLA Scorecard

**1. Page Objective**
Give vendors self-service visibility into their SLA compliance and quality performance — enabling self-governance and reducing KPMG's need to chase vendors.

**2. Primary Actors** Vendor Team Lead, Vendor Manager

**3. Key Workflows**
Review current SLA compliance → Identify at-risk metrics → Compare against target → Download for internal review → Request SLA extension for specific cases

**4. States**
Current period view → Historical view → Filtered by check type / geography

**5. Data Blocks**
Per check type + geography: avg TAT, SLA compliance %, quality score, response rate, breach count, pending assignments with SLA status

**6. Cards**
- Overall SLA Compliance Card: % vs target (current month). Color: Green if ≥ target, Red if below.
- Quality Score Card: % submissions accepted first time (no QC return)
- Active Assignments Card: Count by SLA health (Green/Amber/Red)
- Breach Risk Card: Assignments predicted to breach in next 24h

**7. Charts**
- SLA Compliance Trend: Line chart, last 6 months, vs target line
- TAT Distribution: Box plot (min/p50/p90/max TAT) per check type
- Quality Trend: Error rate per month

**8. Tables**
- At-Risk Assignments Table: Ref | Check type | Geography | SLA deadline | Hours remaining | Status
- Recent Breach Log: Case ref | Breach date | Check type | Delay duration | Root cause (vendor-entered post-breach)

**9. Alerts/Banners**
- "Your SLA compliance dropped below [target]% this month. [N] breaches in [period]." — amber
- "Quality score alert: [N] submissions returned for correction this week." — amber

**10. Mobile Considerations**
Management may check scorecard on mobile. Cards-first view on mobile; charts secondary. Download PDF scorecard action available on mobile.

---

## 6.5 SUPER ADMIN PORTAL — Page Design Depth

---

### 6.5.1 Page: Tenant Provisioning Wizard

**1. Page Objective**
Onboard new client organizations with complete, gated configuration — ensuring nothing critical (data residency, consent setup, legal agreements) is missed before the tenant goes live.

**2. Primary Actors** KPMG Platform Admin

**3. Key Workflows**
Enter org details → Set data residency → Configure jurisdiction + check types → Enable AI features → Configure SLA template → Set branding seed → Create first admin user → Activate

**4. States**
Step 1–9 wizard. Each step has: Incomplete / Complete / Validation Error. Cannot advance without completing required fields. Cannot activate without all mandatory steps complete.

**5. Actions**
Fill each step, go back (preserves all previous state), save as draft (return later), activate tenant, cancel (deletes draft)

**6. Validation Gates (non-negotiable)**
- Cannot reach Step 9 (Activate) without: data residency selected, at least one check type enabled, Client Admin user created, contract dates entered, DPA acknowledgment confirmed
- AI auto-decisioning enablement requires: explicit acknowledgment that human review gate is configured for non-Clear outcomes. Warning shown: "Enabling auto-decisioning without human review gate may violate DPDP/GDPR Article 22. Confirm human review is required for all non-Clear outcomes."

**7. Step-by-Step UI Components**

Step 1 — Organization Details:
- Org name, legal entity name, org type (Corporate / Government / SME)
- Primary contact: name, email, mobile
- Contract start date, contract end date
- Data classification (Standard / Sensitive — affects security controls)
- [Next]

Step 2 — Data Residency (CRITICAL):
- Radio selection: India / European Union / United States / Multi-region
- Residency impact summary: "Selecting [EU] means all candidate data will be stored in EU-region cloud infrastructure. Cross-region replication to India will be disabled."
- GDPR adequacy status display (if EU selected): "EU adequacy decision for India: Not yet recognized. Standard Contractual Clauses will apply for any cross-border transfers."
- Confirmation checkbox: "I confirm this tenant's data residency requirement is [X]."
- [Next — selection cannot be changed after activation without migration workflow]

Step 3 — Jurisdiction + Country Scope:
- Multi-select: Countries this tenant operates in
- Jurisdiction-specific checks auto-suggested based on country selection
- "Country-specific requirements" info panel (India: EPFO + DigiLocker; EU: GDPR consent; US: FCRA disclosures)

Step 4 — Check Type Enablement:
- Toggle grid: All available check types
- Per enabled check: depth options available (Standard / Enhanced / Comprehensive)
- Some checks disabled by default for certain countries (shown with reason)
- Cost indicator per check type (if pricing configured)

Step 5 — AI Features:
- Toggle per feature: Face Match / Liveness / OCR / Fraud Detection / Auto-Decisioning / Predictive SLA / Reviewer Assist
- Auto-Decisioning toggle: Shows warning modal on enable (see validation gate above)
- Per-feature: Which model version will be used (latest stable default)

Step 6 — SLA Templates [C-03 | RFP 1.7, 23.14]:
- Three-track SLA model: Client SLA / Internal SLA / Vendor SLA configured independently per check type
  - Client SLA = contractual commitment to client (breach may trigger penalty — RFP 22.2)
  - Internal SLA = ops team internal target (breach = efficiency issue, not client penalty)
  - Vendor SLA = vendor commitment (breach = vendor scorecard impact)
- Default Template pre-loaded (KPMG baseline — derived from legacy TAT 12–18 days, PPTX/MOM):

  ```
  DEFAULT SLA TEMPLATE — "KPMG Standard Baseline"
  ─────────────────────────────────────────────────────────────────────────────
  Check Type              │ Client │ Internal │ Vendor │ Amber │ Red
                          │  (bd)  │   (bd)   │  (bd)  │  (%)  │ (%)
  ────────────────────────┼────────┼──────────┼────────┼───────┼─────
  Identity / KYC          │   3    │    2     │   1    │  60%  │ 85%
  Employment — Standard   │   7    │    5     │   4    │  60%  │ 85%
  Employment — Executive  │  10    │    8     │   6    │  60%  │ 85%
  Education               │   7    │    5     │   5    │  60%  │ 85%
  Criminal / Legal        │  10    │    8     │   7    │  60%  │ 85%
  Address — Digital       │   3    │    2     │   1    │  60%  │ 85%
  Address — Physical      │   7    │    5     │   3    │  60%  │ 85%
  Financial               │   5    │    4     │   3    │  60%  │ 85%
  Reference Check         │   7    │    5     │   5    │  60%  │ 85%
  ────────────────────────┼────────┼──────────┼────────┼───────┼─────
  Full Standard Package   │  15    │   12     │   —    │   —   │  —
  Full Executive Package  │  20    │   15     │   —    │   —   │  —
  ─────────────────────────────────────────────────────────────────────────────
  bd = business days (holiday-calendar aware — RFP 23.14)
  Amber = SLA clock % elapsed at which amber warning triggers
  Red   = SLA clock % elapsed at which auto-escalation triggers
  ```

- Threshold meaning (shown inline in Step 6 as tooltip):
    Amber threshold: "At 60% of SLA elapsed → reviewer notified to prioritise"
    Red threshold:   "At 85% of SLA elapsed → auto-escalate to Team Lead"
    Breach (100%):   "Client SLA breach → Ops Manager notified + penalty trigger (RFP 22.2)"

- [Apply KPMG Default] button: loads the table above as starting point (all values editable)
- [Clear All] button: blanks all values for fully custom configuration
- [Reset Row to Default] per check type: restores just that row to baseline

- Holiday calendar (RFP 23.14): Select base calendar for business-day SLA calculation
    Options: India National | India State-specific | UK | US | UAE | Custom
    Preview: "SLA of 7 business days starting 14-May-2026 = due by 22-May-2026
              (excluding: Saturday, Sunday, Maharashtra Public Holidays)"
    Multiple calendars selectable if client operates across regions

- Preview: "For a standard package (KYC + Employment + Education + Criminal), Client SLA =
            15 business days. Internal target = 12 days. Vendor must return within 7 days
            of assignment." (Calculated from enabled check types + their SLA values above)

Step 7 — Branding Seed:
- Logo upload (PNG, minimum 200×80px, transparent background preferred)
- Domain prefix (client.kcheck.com subdomain)
- Primary brand color picker (for candidate portal button/header color)
- Welcome message (multilingual — default provided, editable)
- Preview: Live candidate portal preview with branding applied

Step 8 — Admin User:
- First Client Admin: name, email (invite will be sent on activation)
- Role confirmation: "This user will have full Client Admin access"

Step 9 — Review & Activate:
- Full summary of all configuration (collapsible sections)
- DPA confirmation: "KPMG has executed a Data Processing Agreement with this client. [Confirm]"
- [Activate Tenant] button — sends welcome email to Client Admin + creates tenant infrastructure
- [Save as Draft] — for when provisioning is split across multiple sessions

**8. Cards**
- Step Completion Cards: Per step — green checkmark when complete, red when validation error
- Residency Confirmation Card (Step 9): Big residency display — "All data: EU region only"
- AI Features Summary Card (Step 9): Which AI features are enabled

**9. Modals**
- Auto-Decisioning Warning Modal: Legal text + explicit checkbox + [I understand and confirm human review gate is configured]
- Activate Confirmation Modal: "This will create a live tenant. The Client Admin will receive their login within 5 minutes. Confirm?"
- Cancel Tenant Setup Modal: "Canceling will delete all unsaved configuration. Are you sure?"

**10. Audit**
Full provisioning event logged: Platform Admin identity + timestamp + all configuration choices + DPA confirmation. Immutable.

**11. Mobile Considerations**
Tenant provisioning is a desktop-only task for KPMG platform admins. Mobile: not optimized (complex configuration wizard).

---

### 6.5.2 Page: AI Bias & Fairness Monitor

**1. Page Objective**
Continuously monitor AI models for demographic bias — ensuring AI-assisted verification does not produce discriminatorily disparate outcomes across protected groups.

**2. Primary Actors** KPMG Platform Admin, AI Governance Lead, Compliance Officer

**3. Key Workflows**
Review subgroup performance metrics → Detect disparities → Investigate disparity root cause → Determine if corrective action needed → Log investigation outcome → Monitor post-correction

**4. States**
Healthy (no disparity alert) → Disparity Detected → Under Investigation → Corrective Action Taken → Post-Correction Monitoring

**5. Data Blocks**
Per demographic dimension (where data lawfully available and statistically meaningful): false positive rate, false negative rate, auto-clear rate, manual review referral rate. Sample size per group. Disparity ratio vs reference group.

**6. UI Regions**
- Top: Alert banner if active disparity detected
- Left: Dimension selector (age group / document type / geography)
- Center: Subgroup performance table + disparity chart
- Right: Investigation log

**7. Cards**
- "System Status" card: Green (no active disparity alerts) / Red (active disparity alert — investigation required)
- Disparity Ratio Card: Per flagged dimension — ratio of worst-performing group vs reference group
- Investigation Status Card: Open / In Progress / Resolved

**8. Tables**
- Subgroup Performance Table: Dimension | Group | Auto-clear rate | False positive rate | Manual review rate | Sample size | Disparity flag
- Investigation Log: Alert date | Dimension | Magnitude | Investigator | Finding | Action taken | Model version before/after action

**9. Charts**
- Disparity bar chart: Per group, false positive rate as bar. Reference group shown as baseline. Disparity threshold shown as line.
- Trend chart: How disparity has changed over time (pre/post model updates)

**10. Modals**
- Start Investigation Modal: Assign investigator + target resolution date + description of suspected cause
- Close Investigation Modal: Finding (Legitimate correlation / Discriminatory pattern / Inconclusive) + action taken + model retraining trigger (if required)

**11. Alerts/Banners**
- Active Disparity Alert (Red): "Disparity detected in [dimension]. Group [X] has [N]x higher false positive rate than reference group. Investigation required." [Start Investigation]

**12. Compliance Context**
- GDPR Article 22 safeguards: Human review for automated decisions + monitoring for bias
- DPDP equivalent obligations
- Proactive monitoring log is evidence of KPMG's due diligence on algorithmic fairness

**13. Mobile Considerations**
Compliance governance task — desktop primary. Mobile: receive alert notifications + acknowledge. Investigation on desktop.

---



---

## GAP-23 FIX: Country Management Page — Super Admin Portal

### New Pages: 6.5.17 Country Registry + 6.5.18 Country Configuration

**1. New Page: 6.5.17 Country Registry**

**Page Objective**
Central registry of all countries configured in the platform, with activation status, compliance readiness, and country-specific check governance.

**Tables**
Country Registry: Country | Code | Status (Active/Inactive/In Setup) | Data Residency Region | Checks Enabled | Legal Basis Configured | Vendor Coverage | Last Updated | [Configure]

Compliance Readiness per Country:
| Country | Consent Template | Holiday Calendar | Check Governance | Vendor Coverage | Adjudication Matrix | Status |
|---|---|---|---|---|---|---|
| India (IN) | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ Ready |
| UK (GB) | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ Ready |
| Germany (DE) | ✅ | ✅ | ✅ | ⚠️ Partial | ✅ | ⚠️ Partial |
| France (FR) | ✅ | ⚠️ Missing | ✅ | ❌ None | ⚠️ Draft | ❌ Not Ready |

**Bulk Actions**
[Add New Country] | [Export Country Config] | [Compliance Report]

---

**2. New Page: 6.5.18 Country Configuration (Per-Country)**

**Page Objective**
9-step admin configuration workflow for adding/editing a country — zero code changes required.

**Step-by-Step Wizard**

Step 1 — Country Record:
- Country name, ISO code, timezone, default language, currency, data residency region
- Status: Draft / Active

Step 2 — Legal Basis Configuration:
- Per processing purpose: Legal basis dropdown (Consent | Legitimate Interest | Contract | Statutory)
- Jurisdiction notes (e.g., "Germany BDSG Section 26 applies for employment verification")
- Legal sign-off: "KPMG Legal has reviewed this configuration" + legal reviewer field

Step 3 — Check Governance:
- Check governance table (per check type for this country):
  - Permitted: check runs normally
  - Conditional: runs only with documented justification (attachment required)
  - Prohibited: system blocks — cannot be added to any package for this country
  - Ban-the-box gated: criminal check held until conditional offer stage
- Prohibition notes: reason + legal reference for each prohibited check

Step 4 — SLA Calendar:
- Business hours (from/to, timezone)
- Holiday list upload (Excel template or manual entry)
- Import from another country (e.g., "Import UK holidays as base")

Step 5 — Consent Template:
- Select or create country-specific consent notice (links to Template Manager)
- Consent language (primary + required dual-language for legal notices)
- FCRA/GDPR/DPDP section indicator

Step 6 — Adjudication Normalization:
- Add country-specific finding mappings to global normalization table
- E.g., "Spent conviction (UK Rehabilitation Act) → Green for standard roles"

Step 7 — Vendor Assignment:
- Configure vendor coverage for this country (links to Vendor Federation)
- Primary vendor per check type for this country
- Fallback vendor(s)
- Alert if no vendor coverage: "⚠️ No vendor configured for [check type] in [country]"

Step 8 — Test:
- Test Mode: create a test case with this country's settings
- Verify: correct form rendered, correct consent shown, correct check governance applied, correct vendor assigned, correct SLA calendar applied
- Test results shown inline before proceeding

Step 9 — Activate:
- Review summary of all configuration
- Compliance checklist confirmation
- [Activate Country] — makes country available for new cases
- Sends notification to Ops Lead: "Country [X] is now active for case creation"

**Part 5 IA Addition**
Add to Super Admin Portal IA (Part 5.5):
```
├── 9. Country Management
│   ├── 9.1 Country Registry
│   │   └── Page: Country Registry
│   │       Purpose: All configured countries with compliance readiness status
│   └── 9.2 Country Configuration
│       └── Page: Country Configuration Wizard (9 steps)
│           Steps: Country Record → Legal Basis → Check Governance → SLA Calendar →
│                  Consent Template → Adjudication Normalization → Vendor Assignment → 
│                  Test → Activate
│           Zero code changes required for any new country
```

---
## 6.6 FIELD AGENT APP — Page Design Depth

---

### 6.6.1 Page: Evidence Capture (On-Site Verification)

**1. Page Objective**
Enable field agents to capture GPS-timestamped evidence of physical address verification — replacing paper-based and unstructured mobile photo submission with structured, audit-grade, tamper-resistant digital evidence.

**2. Primary Actors** Field Agent (KPMG vendor — on-site, mobile-only)

**3. Key Workflows**
Navigate to address → Arrive at address → GPS auto-capture → Structured checklist completion → Photo capture (GPS-tagged, timestamp-embedded) → Neighbor verification → Outcome declaration → Submit (online) or Queue (offline)

**4. States**
Navigating → Arrived (GPS within range) → Evidence Capture In Progress → Checklist Complete → Outcome Declared → Submitted (online) | Queued (offline) → Synced

**5. Actions**
View address on map, confirm arrival, capture photos, complete checklist, capture neighbor verification, capture signature (if required), declare outcome, submit, queue for offline sync

**6. Data Blocks**
GPS coordinates (lat/long/accuracy/timestamp), photos (with embedded GPS + timestamp metadata), checklist responses, neighbor notes, resident/neighbor signature, outcome declaration, agent identity, device attestation payload

**7. UI Regions (Mobile-first, single-column)**
- Top bar: Case reference + SLA countdown
- GPS Status Band: "Location acquired — [coords] — Accuracy ±8m" (persistent, color-coded: green = accurate, amber = low accuracy, red = GPS unavailable)
- Photo Capture Section: Camera trigger + captured photo thumbnails + GPS match indicator
- Structured Checklist: Scrollable yes/no questions
- Notes Section: Free text for neighbor verification + observations
- Signature Section (conditional): Signature pad for resident/neighbor signature
- Outcome Declaration: Outcome selector
- Submit Button: [Submit Now] (online) or [Save for Sync] (offline)

**8. Cards**
- GPS Accuracy Card: Real-time accuracy radius ("±8m — Good" / "±45m — Fair — move to open area" / "GPS unavailable — check settings")
- GPS-to-Declared Address Distance Card: "You are [X meters] from the declared address." Green if <100m, amber if 100–500m, red if >500m with warning.
- Photo Cards (per captured photo): Thumbnail, GPS coordinates embedded, timestamp, GPS match indicator (green if photo location matches agent GPS location)
- Offline Queue Card (when offline): "3 submissions pending sync. Will sync automatically when connected."

**9. Structured Checklist Questions (configurable per client/package)**
- "Is this address a residential address?" (Y / N / Not Applicable)
- "Is an address board/nameplate visible with the declared name?" (Y / N)
- "Was a resident present at the address?" (Y / N — if No: note required)
- "Did the resident confirm they reside at this address?" (Y / N / Refused)
- "Were any identity documents sighted?" (Y / N — if Yes: which type)
- "Neighbor verification conducted?" (Y / N — if Yes: opens neighbor notes field)
- "Any concerns about the address?" (Y / N — if Yes: opens observations field)

**10. Photo Capture (Core Feature)**
- In-app camera (no gallery upload option — prevents pre-captured photo fraud)
- Required shots: (1) Address board/nameplate, (2) Front of building/house, (3) Agent at location (selfie with surroundings — optional, per config)
- Per capture: GPS auto-embedded in EXIF metadata (lat/long + accuracy + timestamp) on server side validation
- Minimum required photos: configurable (default 2)
- Photo quality check: basic blur/darkness detection
- Anti-spoofing: Screenshot detection (moiré pattern), screen reflection detection
- Server-side: GPS in EXIF vs agent's GPS capture timestamp cross-validated (must match within 200m and 5 minutes)

**11. Signature Capture (Conditional)**
- Canvas-based signature pad (touch/stylus)
- Signed by (field): Resident / Neighbor / Agent only (when resident not available)
- If resident signs: strongest evidence; if agent only: lower evidentiary weight noted

**12. Neighbor Verification Notes**
- Triggered by "Neighbor verification conducted: Yes"
- Fields: Neighbor's approximate relationship to address (adjacent unit / opposite building / building security), neighbor's confirmation statement (free text, agent-recorded), neighbor's name (optional)

**13. Modals**
- GPS Warning Modal (when distance > 500m from declared address): "You appear to be more than 500 meters from the declared address. Please confirm you are at the correct location before capturing evidence. [I am at the correct address — capture anyway] [Navigate to address]"
- Offline Submit Modal: "You are offline. Evidence will be saved locally and submitted when connectivity is restored. [Save Locally]"
- Low Accuracy GPS Modal: "GPS accuracy is low (±[N]m). For best results, move to an open area away from buildings. [Continue anyway] [Wait for better signal]"

**14. Outcome Declaration**
- Address Confirmed: All verification points satisfied
- Address Confirmed — With Observations: Confirmed but agent noted something (notes required)
- Address Not Confirmed: Resident absent, refused, or address does not match (reason required)
- Unable to Verify — Location Not Found: GPS and physical navigation could not locate address
- Unable to Verify — Access Denied: Gated community, security refused access (notes + security photo required)

**15. Alerts/Banners**
- "SLA in [N] hours — please complete and submit." — persistent amber banner when <4h remaining
- "GPS signal lost — accuracy may be affected." — amber, dismissible
- "Pending offline submissions: [N] — please sync when connected." — persistent until synced

**16. Timeline/Audit**
Per submission event:
- Agent identity + device fingerprint
- GPS coordinates at: (a) page open, (b) first photo capture, (c) submission — all three captured and compared
- All checklist responses (timestamped per interaction)
- All photos (with embedded + server-validated GPS + timestamp)
- Device attestation result (SafetyNet/DeviceCheck pass/fail)
- Outcome declared + outcome timestamp
- Sync timestamp (if offline → synced)

**17. SLA Components**
- SLA countdown visible in top bar (persistent during entire evidence capture session)
- SLA urgency changes bar color: Green → Amber (<30%) → Red (<10%)

**18. AI Components**
- Photo authenticity check (server-side, post-submission): GPS cross-check between EXIF and captured GPS, teleportation detection, moiré/screen detection
- Results visible to ops in Address Verification Workspace (not to field agent)

**19. Offline Capability**
- All form state saved locally (IndexedDB / local SQLite)
- Photos stored in app local storage
- Submission queued in offline queue
- On connectivity restore: auto-sync with progress indicator
- Conflict detection: if case was reassigned while agent was offline → alert agent

**20. Mobile Considerations (this entire page is mobile — no desktop version)**
- Minimum supported: Android 8+ / iOS 13+
- Tested at: 360px width (minimum), 375px (iPhone SE), 390px (iPhone 14)
- All tap targets: minimum 48×48dp (WCAG mobile)
- One-handed operation: primary actions (camera trigger, submit) in bottom thumb zone
- Glove-compatible stylus targets for winter climates
- Offline-first: app functions completely offline; sync is secondary
- Battery efficiency: GPS polling only active when page is open (not background)
- Low-data mode: photos compressed to < 2MB before upload; metadata never compressed

---
---



---

## GAP-26/27 FIX: GPS Check-In/Out States + QC Return Flow in Field Agent App

### Addition to 6.6.1 Evidence Capture — GPS Check-In/Out as Distinct States

**Updated Page Structure: Evidence Capture Broken into Explicit Phases**

The Evidence Capture page (6.6.1) is restructured to reflect the 12-state site visit machine. The page renders differently based on current state:

**Phase 1: Pre-Check-In (State: Agent Assigned)**
Page renders as:
- Assignment details (address, SLA, instructions)
- Navigation button ([Navigate → opens native maps])
- [GPS Check-In] button — large, primary action, thumb-accessible
- Note: "Tap Check-In when you arrive at the address. Your location will be recorded."

GPS Check-In Action:
- On tap: system captures GPS coordinates (lat/long/accuracy/timestamp) — single read, no continuous tracking
- Shows: "Location recorded: [coords] — Accuracy: ±8m — [timestamp]"
- Distance check: "You are [X meters] from the declared address" — green/amber/red indicator
- If distance > 500m: Warning modal appears (GAP-3 GPS Anomaly Override Modal)
- [Confirm Check-In] → transitions page to Evidence Capture phase

GPS Check-In Record stored: `{lat, long, accuracy_meters, timestamp_utc, device_id, attestation_payload}`

**Phase 2: Evidence Capture (State: Evidence Capture)**
Page renders as evidence capture interface (existing 6.6.1 design — GPS capture, photos, checklist, notes). No changes to this phase. Check-in timestamp shown in header: "Checked in: [time] | [duration at site]"

**Phase 3: GPS Check-Out (State: GPS Check-Out)**
Appears AFTER checklist completion + photo upload — before final submit button.

New Section added to bottom of Evidence Capture page:
```
─────────────────────────────
GPS CHECK-OUT

You are about to submit your evidence. Please record your check-out 
before submitting.

[GPS Check-Out] button

This records that you have left the address. Check-out location 
and time are included in the evidence package.
─────────────────────────────
```

GPS Check-Out Action:
- Captures: GPS coordinates (lat/long/accuracy/timestamp) — second independent GPS read
- Shows: "Check-out recorded: [coords] — [timestamp]"
- Time at site calculated: "Time at address: [duration]" — shown for agent's reference and stored in evidence
- [Confirm Check-Out and Submit] → final submission

GPS Check-Out Record stored: `{lat, long, accuracy_meters, timestamp_utc, device_id}` — separate from check-in record

**Offline Check-In/Check-Out**
GPS Check-In and Check-Out work in offline mode:
- GPS captured directly from device (does not require connectivity)
- Check-in/out events queued in offline store
- Sync'd to server when connection restored (same as photo sync — with server-side timestamp validation)

**Evidence Summary (shown before submit)**
```
Evidence Package Summary:
GPS Check-In:  [coords] — [timestamp] — ±8m accuracy
GPS Check-Out: [coords] — [timestamp] — ±5m accuracy
Time at address: 23 minutes
Photos: 4 (all GPS-tagged)
Checklist: Complete
```

---

### New Page: 6.6.6 QC Return Queue (Field Agent App)

**1. Page Objective**
Allow field agents to see when their submitted evidence has been rejected by Supervisor QC, understand the specific error, and take corrective action (re-capture / re-visit).

**2. Primary Actors**
Field Agent

**3. Key Workflows**
Receive QC return notification → View error details → Plan corrective action → Navigate back to address → Re-capture evidence → Re-submit

**4. States**
New Return (unreviewed) | Reviewing Error | Re-Capture Required | Re-Captured | Re-Submitted

**5. Actions**
View error details, plan re-visit, navigate to address, re-capture evidence, re-submit

**6. UI Regions**
- QC Returns list (if any returned items)
- Empty state: "No QC returns — great work!" (encourages quality)
- Per return: Assignment reference + error tags + action required

**7. Cards (per QC return)**
```
[!] QC Return — Action Required

Assignment: [ref]
Check type: Address Verification
Address: [address]

Supervisor notes:
• GPS coordinates did not match address (captured 800m away)
• Photo 2 is blurry — please retake

SLA: Re-submission due by [date/time]

[Re-Capture Evidence] [Contact Supervisor]
```

**8. Error Tag Display**
Standardized, agent-readable error tags (plain language):
- "Your GPS location was too far from the address" → Means: GPS Mismatch
- "Not enough photos were submitted" → Means: Insufficient Evidence
- "The checklist was incomplete" → Means: Checklist Incomplete
- "A photo appears unclear or low quality" → Means: Evidence Quality
- "Photo location and GPS check-in don't match" → Means: Photo GPS Mismatch

**9. Re-Capture Workflow**
[Re-Capture Evidence] button → navigates to Evidence Capture page (6.6.1) in "Re-Capture Mode":
- Previous submission shown as reference: "Original submission on [date]"
- Error areas highlighted: e.g., "Photo 2 needs to be retaken — currently flagged as blurry"
- New GPS Check-In required (fresh coordinates)
- [Submit Corrected Evidence] → routes to Supervisor QC again

**10. Mobile Considerations**
- QC return badge on app home screen / Assignment List (6.6.3): red badge count
- Push notification on new QC return: "Your submission for [address] was returned by your supervisor. Tap to view."
- [Navigate] button available directly from QC return card — agent can go straight to address without switching pages

**11. Part 5 IA Addition**
Add to Field Agent App IA (Part 5.6):
```
└── 6. QC Returns
    └── Page: QC Return Queue
        Purpose: View supervisor-rejected submissions, understand errors, 
                 plan and execute corrective re-capture
        States: New Return | Reviewing | Re-Capture Required | Re-Submitted
        Error tags: GPS Mismatch | Insufficient Evidence | Checklist Incomplete | 
                    Evidence Quality | Photo GPS Mismatch
```


---


---

## GAP FILLS — P1 REQUIRED RFP FEATURES


---
## 6.2 CLIENT PORTAL — Detailed Page Designs (Part B: Dashboard, Config & Billing Pages)


---

---

### 6.2.5 Page: Client Overview Dashboard

**1. Page Objective**
Client's primary landing page after login — gives immediate visibility into their entire BGV program status, pending actions, and recent activity without navigating elsewhere.

**2. Primary Actors**
Client Initiator (HR/TA), Client Viewer, Client Admin

**3. Key Workflows**
Login → review program health → identify cases needing action → access pending reports → navigate to specific case or report

**4. States**
Loading | Rendered (default: MTD view) | No cases yet (first-time user onboarding state)

**5. Actions**
Navigate to case, download ready report, re-invite non-responding candidate, go to action queue, initiate new case, view analytics

**6. Data Blocks**
Active cases count by status, SLA compliance rate (their cases), outcome distribution, pending candidate actions, recent reports ready, monthly volume trend, business unit breakdown

**7. UI Regions**
- Top: Welcome strip ("Good morning, [Name] — [N] cases need your attention")
- KPI strip (below welcome)
- Left: Status distribution chart + action required panel
- Right: Recent reports panel + notification feed
- Bottom: Monthly volume trend chart

**8. Cards**
- KPI Cards (clickable to filtered case list):
  - Active Cases (total in progress)
  - Pending Candidate Submission (not yet submitted)
  - Reports Ready for Download (new, undownloaded)
  - Avg TAT This Month (days)
  - SLA Compliance % (their cases)
- "Action Required" Panel Card: Candidates who haven't submitted (> 3 days), reports awaiting client approval, disputes pending client response — each with direct action button
- Recent Reports Card: Last 5 completed reports — candidate name, outcome color, [Download] button per report

**9. Charts**
- Status Distribution Donut: In Progress / Pending Candidate / Completed / On Hold — count per segment, clickable filter
- Outcome Color Distribution (month): Green / Amber / Yellow / Red — proportion chart
- Monthly Volume Trend: Bar chart (cases initiated vs completed per month, last 6 months)

**10. Drawers**
- Notification Drawer (bell icon): System messages from KPMG — downtime notices, feature announcements, SLA updates

**11. Modals**
None on dashboard — all actions navigate to appropriate page

**12. Tabs** None — single-page overview

**13. Filters**
Business unit selector (if client uses BU segregation — filters all dashboard widgets)

**14. Alerts/Banners**
- "You have [N] candidates who have not submitted for > 5 days — consider re-inviting" — amber
- "SLA compliance for your cases is [X]% this month vs [Y]% last month" — informational
- "System maintenance scheduled for [date/time] — plan accordingly" — info banner

**15. Timeline/Audit** None on dashboard

**16. SLA Components**
SLA compliance % KPI card — their cases only, vs KPMG's committed SLA tier

**17. AI Components** None direct

**18. Evidence Components** None

**19. Mobile Considerations**
Dashboard is primary mobile landing. KPI cards: stacked full-width on mobile. Action required panel: sticky top priority on mobile. Charts: hidden on mobile (text KPIs only). "View full dashboard" link for desktop.

---

### 6.2.6 Page: Client Action Required Queue

**1. Page Objective**
Centralize all items requiring client's explicit response — adjudication approvals, dispute responses, waiver confirmations — so nothing is missed.

**2. Primary Actors**
Client Admin, Client Initiator (HR/TA)

**3. Key Workflows**
Review pending actions → Respond to each (approve adjudication / respond to dispute / confirm waiver) → Reduce queue to zero

**4. States**
Per action: Pending Client Response | Responded | Overdue (if SLA applies to client response)

**5. Actions**
Approve adjudication outcome, reject (request re-review), respond to dispute, confirm waiver, view case detail

**6. Data Blocks**
Action type, case ID, candidate, what is required from client, deadline (if applicable), days pending

**7. UI Regions**
- Top: Action type filter tabs (All | Adjudication Approval | Dispute Response | Waiver Confirmation)
- Action list (cards — not table, more readable)
- Each card: context summary + direct action button

**8. Cards**
- Adjudication Approval Card: Candidate name | Outcome (color) | Key discrepancy summary | [Approve Outcome] [Request Re-review]
- Dispute Response Card: Candidate name | Dispute type | KPMG's preliminary finding | [View & Respond]
- Waiver Confirmation Card: Discrepancy being waived | Waiver rationale from KPMG | [Confirm Waiver] [Reject Waiver]

**9. Tables** None — card-based for clarity

**10. Drawers**
- Adjudication Detail Drawer: Full adjudicated outcome (same as Case Detail report-ready view) — discrepancies + resolution — [Approve] [Request Re-review with note]
- Dispute Detail Drawer: Candidate's claim + KPMG's investigation finding + [Client Response] text area + [Submit Response]

**11. Modals**
- Approve Modal: "Confirm your approval of this outcome for [candidate]? This approves release of the BGV report." [Confirm]
- Request Re-review Modal: Reason text (mandatory) + [Submit Request]
- Waiver Confirm Modal: "You are approving a waiver for [discrepancy type] for [candidate]. [Confirm Waiver]"
- Waiver Reject Modal: Reason (mandatory) + [Submit]

**12. Filters**
Action type | Business unit | Days pending (range)

**13. Alerts/Banners**
- "[N] adjudication approvals pending — reports cannot be released until approved" — amber
- "Client response required for dispute — [N] days remaining" — amber with countdown

**14. SLA Components**
If client response has a deadline (agreed in SLA) — countdown per action item

---


---

## GAP-EXP-H10 FIX: Client-Side Waiver Approval Workbench — Client Portal

### H-10 | Client-Side Waiver Approval Workbench — Missing

**RFP Reference:** RFP 10.7

**RFP Text:**
> *"Waiver and approval workflow — Configurable waiver process with approval matrix and evidence attachment"*

**Verdict:** EXPLICIT

**Analysis:**
RFP 10.7 explicitly requires a "configurable waiver process with approval matrix." An approval matrix necessarily involves multiple approval tiers — including client-side approvers (Hiring Manager, Risk/Legal) — because the waiver ultimately affects the client's hiring decision. An ops-only waiver process where the client only receives a notification is not an "approval matrix." The "approval matrix" language implies client-side actors have an active approval/rejection role with evidence review capability. The existing Client Portal has a "Pending My Action" queue but lacks a detailed waiver approval workbench with discrepancy evidence view, AI risk context, and multi-step approval actions.

**Impact:**
- Without this workbench, client-side approvers (Hiring Manager, HR Risk Lead, Legal) have no designed UI to review discrepancy evidence, understand AI risk score, or make an informed waiver decision.
- KPMG's ops team cannot receive a well-documented client approval — impacting the audit trail for waiver decisions.
- Clients in regulated industries (BFSI, government) require formal documented approval workflows that this gap prevents.

**Recommendation:**
Expand 6.2.6 Client Action Required Queue or add a dedicated Waiver Approval Workbench page to the Client Portal.

---

### New Page: 6.2.6A Client Waiver Approval Workbench — Client Portal

**1. Page Objective**
Provide Client Hiring Manager, Risk Lead, and Legal approvers with a structured, evidence-backed workspace to review KPMG's waiver recommendation and make a formal approve/reject/request-more-information decision on discrepancy waivers that require client sign-off.

**2. Primary Actors**
Client Hiring Manager, Client Risk/Legal Lead, Client Admin (view-only)

**3. Key Workflows**
Receive waiver notification → Open waiver workbench → Review discrepancy summary → Review AI risk score → Review KPMG recommendation → Review evidence → Approve / Reject / Request info → Decision confirmed with mandatory note → Audit log updated

**4. States**
Pending Client Review | Information Requested (by client approver) | Approved | Rejected | Escalated (to senior approver)

**5. Actions**
Approve waiver, reject waiver, request additional information from KPMG, escalate to senior approver, download waiver evidence pack, add notes

**6. Data Blocks**
Case reference | Candidate ID (masked) | Waiver type | Discrepancy summary | Severity | KPMG recommendation | AI risk score | Evidence attachments | Approval deadline | Prior waivers for this candidate

**7. UI Regions**
- Left: Case & Waiver Summary Panel
- Center: Evidence Viewer (primary workspace)
- Right: Decision Panel (approve/reject/request info)

**8. Cards**

**Waiver Header Card:**
```
WAIVER REQUEST — CASE CK-0921
─────────────────────────────────────────────────────────────
Candidate: [Masked — initials + role]    Package: Executive Pro
Discrepancy: Employment — 14-month gap (Apr 2019–Jun 2020) 
             Candidate explanation: Career break (personal)
             No verification possible — employer dissolved
─────────────────────────────────────────────────────────────
Severity: MODERATE            AI Risk Score: 42/100 (Medium)
KPMG Recommendation: WAIVE — Low-risk profile; single gap
Waiver requested by: Ops Lead [Name]      Date: 10-Jan-2025
Decision required by: 17-Jan-2025 (7 days)
─────────────────────────────────────────────────────────────
```

**AI Risk Score Context Card:**
```
AI RISK SCORE BREAKDOWN — 42/100 (Medium Risk)

Identity signals:        ✅ Low risk (face match 97%)
Employment signals:      ⚠ Medium (14-month gap, 1 employer dissolved)
Education signals:       ✅ Low risk (DigiLocker verified)
Criminal signals:        ✅ Clear (all jurisdictions)
Document signals:        ✅ Authentic (no fraud flags)

KPMG Adjudicator Note:
"Gap period coincides with documented industry-wide layoffs
(Feb 2020 wave). Candidate's explanation is plausible.
All other signals are clear. Recommended: Waive."
```

**Prior Waivers Card (if applicable):**
```
⚠ PRIOR WAIVERS FOR THIS CANDIDATE: 0
This is the first waiver request for this candidate.
```

**9. Evidence Viewer Panel**

Documents available for review (tabbed):
- Tab 1: Candidate-submitted gap explanation (text + uploaded documents)
- Tab 2: KPMG verification evidence (employer contact log, verification attempts)
- Tab 3: AI fraud detection results (all signals green — per check type)
- Tab 4: Adjudication worksheet (KPMG adjudicator's notes)

Evidence viewer: inline PDF/image viewer with zoom, rotate, download.

**10. Decision Panel**

```
YOUR DECISION
─────────────────────────────────────────────
[ ✅ Approve Waiver ]  → opens Approval Modal
[ ❌ Reject Waiver ]   → opens Rejection Modal
[ ℹ Request Info ]    → opens Info Request Modal

Decision notes (required for all decisions):
[Text area — min 50 characters — max 1000 characters]

Your decision will be:
• Recorded with your identity and timestamp
• Notified to KPMG Operations immediately
• Included in the final verification report
─────────────────────────────────────────────
```

**11. Modals**

- **Approve Waiver Modal:**
  "You are approving a waiver for Case [Ref]. This means verification will proceed despite the identified discrepancy. The discrepancy will be disclosed in the verification report. Your approval is legally binding under your client agreement with KPMG. [Confirm Approval]"

- **Reject Waiver Modal:**
  "Rejecting this waiver will result in the case being marked as [Outcome per adjudication matrix]. KPMG will notify the candidate as required. [Confirm Rejection]"

- **Request More Information Modal:**
  "What additional information do you need from KPMG Operations? [Text area] → [Send Request]"
  Response SLA selector: Required by [N] business days

- **Escalate to Senior Approver Modal:**
  "Who should review this waiver? [Select from your org's configured approvers] [Escalate]"

**12. Alerts/Banners**
- "⚠ Decision required by [date] — [N] days remaining. Failure to respond may delay the candidate's onboarding." — amber, time-based
- "⚠ Decision overdue — please review immediately." — red (post-deadline)
- "This waiver requires Risk/Legal sign-off in addition to your approval" — amber (if approval matrix requires dual sign-off)

**13. Audit Trail**
| Event | Actor | Timestamp | Data Logged |
|---|---|---|---|
| Waiver notification sent | System | [time] | Notification delivery status |
| Workbench opened | Client Approver | [time] | Approver identity, session |
| Evidence viewed | Client Approver | [time] | Which tabs/documents viewed |
| Decision made | Client Approver | [time] | Decision, mandatory notes, identity |
| Decision acknowledged | System | [time] | KPMG ops notified |

**14. Part 5 IA Addition:**
Add to Client Portal IA (Part 5.2) under section 2 (Case Management):
```
├── 2.6 Waiver Approval Workbench
│   └── Page: Client Waiver Approval Workbench
│       Purpose: Client approvers review and decide on KPMG waiver recommendations
│       RFP: 10.7 | Actors: Hiring Manager, Risk/Legal | Classification: Compliance-Critical
```


### 6.2.7 Page: Report Inbox

**1. Page Objective**
Clients' primary interface to access completed BGV reports — new reports prominently surfaced, easy download, access log visible.

**2. Primary Actors**
Client Initiator, Client Viewer, Client Admin

**3. Key Workflows**
Login → see new reports → preview or download → bulk download for periodic processing → archive old reports

**4. States**
New (not yet downloaded by anyone on the client team) | Downloaded | Superseded (re-issued — older version)

**5. Actions**
Preview (in-browser), download (PDF), bulk download, mark as reviewed, view access log

**6. Data Blocks**
Case ID, candidate name, package, report date, outcome color, version, downloaded by (client team), downloaded at

**7. UI Regions**
- Top: "New Reports" count badge
- New Reports section (highlighted, top): Undownloaded reports
- All Reports section: Full list (paginated)

**8. Cards**
- New Report Card (per report): Candidate name, outcome color badge, report date, [Preview] [Download] buttons. "New" badge until first download.

**9. Tables**
Reports Table: Case ID | Candidate | Package | Report Date | Outcome Color | Version | First Downloaded | Downloaded by | [Preview] [Download]

**10. Drawers**
- Report Preview Drawer: In-browser PDF viewer (full report rendered) — [Download] button inside
- Access Log Drawer: Who on the client team downloaded this report, when, from which device (for audit)

**11. Modals**
- Bulk Download Modal: Select reports (date range / outcome / package) → [Download as ZIP] — shows count and estimated file size

**12. Filters**
Date range | Outcome color | Package | Business unit | Downloaded (yes/no)

**13. Bulk Actions**
Bulk download (ZIP) | Bulk mark as reviewed

**14. Alerts/Banners**
- "[N] new reports available since your last visit" — blue informational
- "Report for [candidate] has been re-issued (version 2). Previous version is archived." — informational

**15. Compliance Notes**
Report download events logged in case audit trail (who downloaded, portal, timestamp). Client cannot delete reports from inbox — KPMG controls retention.

**16. Mobile Considerations**
Download on mobile: PDF opens in device default viewer. Preview may be limited on mobile — "Open in browser" fallback. New reports badge visible on mobile dashboard.

---

### 6.2.8 Page: Historical Report Archive

**1. Page Objective**
Full searchable archive of all reports ever issued to this client — for compliance lookups, HR record-keeping, re-verification decisions.

**2. Primary Actors**
Client Admin, HR Compliance

**3. Key Workflows**
Search by candidate name or date → Locate historical report → Download → Check re-issued versions

**4. States**
Current version (latest) | Superseded (older version — accessible, labeled)

**5. Tables**
Archive Table: Case ID | Candidate | Package | Issue Date | Outcome Color | Version (v1/v2/...) | Re-issue Reason | [Download]

**6. Drawers**
- Version Comparison Drawer: Side-by-side of v1 vs v2 report (what changed between versions — highlighted diff summary, not full PDF comparison)

**7. Filters**
Date range | Outcome color | Package | Business unit | Candidate name search | Case ID search | Version (all / latest only)

**8. Bulk Actions**
Bulk download (selected range) — ZIP file

**9. Alerts/Banners**
- "This report has been superseded — version [N] is the current version" — informational on older version

**10. Retention Notice**
"Reports are retained for [N] years per your data agreement. Reports will be automatically removed on [date] unless extended." — visible in archive footer.

---

### 6.2.9 Page: Client-Specific Outcome Analytics (Report Analytics)


---

### 6.2.10 Page: Screening Package Manager

**1. Page Objective**
Allow Client Admin to create and manage screening packages — the configuration that drives what checks are run for each type of hire.

**2. Primary Actors**
Client Admin

**3. Key Workflows**
Create package → Select check types → Configure depth per check → Associate to job roles → Activate → Review audit history

**4. States**
Draft | Active | Inactive (deactivated — cases already using it not affected)

**5. Actions**
Create, edit, duplicate, activate, deactivate, view audit history, preview estimated TAT + cost

**6. Data Blocks**
Package name, description, check types (enabled/disabled per package), depth per check (standard/enhanced/comprehensive), role associations, country applicability, estimated TAT, cost preview

**7. UI Regions**
- Package list (left): All configured packages with status badges
- Package detail (center): Configuration for selected package
- Action bar: Edit / Duplicate / Activate / Deactivate

**8. Cards**
- Package Card (list): Name | Status | Check count | Estimated TAT | Associated roles | Last modified
- TAT Estimate Card (in detail view): Calculated from check types + depth + country — "Estimated: 5–8 business days"
- Cost Preview Card (in detail view): Per-check cost breakdown + total (if pricing configured)

**9. Tables**
- Check Type Config Table: Check type | Enabled | Depth (dropdown) | Country availability | Notes
- Role Associations Table: Job role / Level → Package mapped

**10. Drawers**
- Check Type Detail Drawer: For each check — what Standard / Enhanced / Comprehensive means (what's included at each depth)
- Audit History Drawer: Who changed what on this package, when — version history

**11. Modals**
- Duplicate Package Modal: "Name for duplicate: ___" → creates copy in Draft state for editing
- Deactivate Modal: "Deactivating this package will prevent new cases from using it. Existing cases are not affected. Confirm?"
- Activate Modal: Confirmation with estimated TAT and cost display

**12. Alerts/Banners**
- "Package has no role associations — new case initiators won't see this package as a recommendation" — informational
- "Check type [X] not available for [Country Y] — will be excluded for cases in that country" — informational

---

### 6.2.11 Page: Client User Administration

**1. Page Objective**
Manage client-side users — who can initiate, view, or administer within their organization's tenant.

**2. Primary Actors**
Client Admin

**3. Key Workflows**
Add user → Assign role → Set BU scope → Invite (email) → Manage (edit/deactivate) → Temporary access for contract staff

**4. States**
Invited (not yet logged in) | Active | Inactive (deactivated)

**5. Actions**
Add user, edit role/scope, resend invite, deactivate, set temporary access with expiry, configure SSO

**6. Data Blocks**
Name, email, role, business unit scope, last login, status, SSO linked (Y/N), access expiry (if temporary)

**7. Tables**
User Table: Name | Email | Role | BU Scope | Last Login | Status | SSO | Expiry | [Edit] [Deactivate]

**8. Role Definitions (shown in UI as tooltips)**
- Initiator: Can create cases and view their own initiated cases
- Viewer: Can view all cases in their BU scope (cannot initiate)
- Admin: Full configuration access + user management

**9. Drawers**
- Add/Edit User Drawer: Name, email, role selector, BU scope (multi-select), access expiry toggle (for temporary staff)
- SSO Config Drawer (Admin-only): SAML 2.0 configuration — IdP metadata URL, attribute mapping

**10. Modals**
- Deactivate Modal: "Deactivating [name] — they will lose access immediately. Any pending cases they initiated will remain active and visible to admins. Confirm?"
- Resend Invite Modal: "Resend invitation email to [email]? Previous invite link will be invalidated."

**11. Alerts/Banners**
- "[N] users have not accepted their invitation for > 7 days — consider resending or checking email"
- "SSO is configured — users will be authenticated via your organization's identity provider"
- "Temporary access for [user] expires in 3 days — extend or let expire"

---

### 6.2.12 Page: Custom Form Builder

**1. Page Objective**
Allow Client Admin to customize consent forms, employer verification forms, and reference questionnaires — adapting KPMG's standard forms to their organization's specific requirements.

**2. Primary Actors**
Client Admin

**3. Key Workflows**
Select form type → Drag-and-drop field editor → Add/remove/reorder fields → Configure conditions → Add language variants → Preview → Publish

**4. States**
Draft | Pending Review (if KPMG approval required) | Published | Archived

**5. Actions**
Add field, remove field, reorder, configure field properties, add conditional logic, add language variant, preview (desktop + mobile), test, publish, rollback to previous version

**6. Data Blocks**
Form type, fields (type, label, required/optional, conditions), language variants, version, publish history

**7. UI Regions**
- Left: Field palette (available field types)
- Center: Form canvas (drag-drop area — rendered form preview)
- Right: Selected field properties panel (label, placeholder, required, validation, conditional logic)
- Top toolbar: Form type selector, language selector, [Preview] [Publish] buttons

**8. Cards**
- Field Type Cards (palette): Text / Long Text / Dropdown / Date / Checkbox / File Upload / Signature / Scale (1–5) / Section Divider
- **Custom Fields Section in palette [C-08 | RFP 12.3]:** Below standard field types, a "Your Custom Fields" section shows all Active custom fields registered in the Custom Field Registry (6.2.23) for this client. Each registered field appears as a drag-able card showing: display label + data type icon + scope badge. Dragging it onto the form canvas adds it with all pre-configured properties (type, options, required state). Fields already on the canvas are greyed out in the palette. "Register new custom field →" link opens 6.2.23 in a new tab.

**9. Drawers**
- Conditional Logic Drawer: "Show this field only if [field X] equals [value Y]" — rule builder
- Language Variant Drawer: Translate all field labels and placeholder text for selected language
- Mobile Preview Drawer: Renders form as it would appear on mobile

**10. Modals**
- Publish Modal: "Publishing will make this form active for new cases immediately. [N] cases in progress will continue using current version until re-submission." [Confirm Publish]
- Rollback Modal: "Rollback to version [N]? Current draft will be saved but deactivated."
- KPMG Approval Modal (for consent forms): "Changes to consent forms require KPMG compliance review before publishing. Submitting for review..."

**11. Alerts/Banners**
- "Consent form changes require KPMG compliance review — submit for review before publishing" — important for consent forms
- "This form is used in [N] active packages — changes will affect future cases using these packages"
- "Mobile preview recommended — majority of candidates use mobile"

**12. Mobile Considerations**
Form builder itself is desktop-only (drag-drop). Mobile preview is accessible from desktop builder.

---

### 6.2.13 Page: Outcome Color Code Matrix

**1. Page Objective**
Allow Client Admin to define what each outcome color means for their organization — aligning KPMG's verification outcomes to their specific hiring policy.

**2. Primary Actors**
Client Admin

**3. Key Workflows**
Review standard matrix → Customize per scenario → Preview → Save → Audit history

**4. States**
Standard (KPMG default) | Customized | Pending Review

**5. UI Regions**
- Left: Pre-built schemes (Conservative / Standard / Flexible — quick apply)
- Center: Matrix configuration table
- Right: Preview panel (sample case outcomes with this matrix applied)

**6. Cards**
- Pre-built Scheme Cards: "Conservative — any discrepancy = Red", "Standard — major discrepancy = Red, minor = Amber", "Flexible — client reviews all Amber before deciding"
- Preview Card: 3 sample scenarios with outcome colors applied per current matrix

**7. Tables**
Color Matrix Table: Scenario (e.g., "Employment dates differ by < 1 month") | Severity | Client-assigned color | Notes/meaning

**8. Drawers**
- Custom Scenario Builder Drawer: IF [check type] AND [discrepancy type] AND [severity] THEN [color] — rule builder
- Audit History Drawer: Previous matrix versions with change log

**9. Modals**
- Apply Scheme Modal: "Applying [Scheme] will overwrite your current custom configuration. Confirm?"
- Save Matrix Modal: "Save changes to color matrix? This will affect all future case outcomes for your organization." [Confirm]

**10. Alerts/Banners**
- "Color matrix affects report outcomes — changes apply to cases adjudicated after save date (not retroactively)"
- "KPMG recommends having your legal/HR team review color matrix before publishing"

---

### 6.2.14 Page: Holiday List Manager

**1. Page Objective**
Configure location-based holiday lists that drive SLA and TAT calculations — ensuring business days are accurately computed for your organization's operating locations.

**2. Primary Actors**
Client Admin

**3. Key Workflows**
Select country/state → Import or manually add holidays → Review → Save → Preview SLA impact

**4. States**
Default (KPMG-provided national holidays) | Customized | Overdue (holiday list not updated for upcoming year — alert)

**5. Tables**
Holiday Table: Date | Holiday name | Country | State/Region | Recurrence (annual Y/N) | Source (KPMG default / Client custom)

**6. UI Regions**
- Left: Country/state selector
- Center: Holiday list for selected location
- Right: SLA preview (how a standard case TAT is affected with this holiday list)

**7. Drawers**
- Import Drawer: Upload Excel with holiday list (template downloadable). Validation: date format, duplicate check.
- Add Holiday Drawer: Single holiday entry form

**8. Modals**
- Delete Holiday Modal: "Remove [holiday] from [year]? This will affect SLA calculations for cases with this date in their TAT window."

**9. Alerts/Banners**
- "Holiday list for [country] has not been updated for [year] — please review before year-end" — amber
- "Importing [N] holidays. [N] duplicates found and skipped." — post-import summary

---

### 6.2.15 Page: Candidate Portal Branding Configuration

**1. Page Objective**
White-label the candidate portal with the client's brand — ensuring candidates recognize their employer's identity, improving trust and completion rates.

**2. Primary Actors**
Client Admin

**3. Key Workflows**
Upload logo → Set primary color → Configure custom domain → Edit messages → Preview → Publish

**4. States**
Draft | Published | Preview Mode

**5. UI Regions**
- Left: Configuration form (logo, color, domain, messages)
- Right: Live candidate portal preview (updates in real-time as config changes)

**6. Cards**
- Live Preview Card: Rendered candidate portal with current branding applied — shows: welcome screen, form header, button colors, logo placement

**7. Drawers**
- Logo Upload Drawer: Upload area, format/size guide, preview in different contexts (mobile header, desktop header, email footer)
- Custom Domain Drawer: Domain configuration (e.g., bgv.clientname.com), DNS CNAME instructions, SSL status indicator

**8. Modals**
- Publish Modal: "Publishing will make these branding changes live for all new candidate sessions immediately. In-progress sessions continue with previous branding until they re-authenticate." [Confirm]

**9. Alerts/Banners**
- "Custom domain DNS not yet propagated — using default domain until DNS resolves" — informational
- "Logo dimensions are outside recommended range — may appear distorted on mobile" — warning

**10. Mobile Preview**
Live preview must show mobile view (most candidates on mobile). Toggle: Desktop / Mobile preview.

---

### 6.2.16 Page: ATS / HRIS Integration Settings

**1. Page Objective**
Configure integrations between the client's ATS/HRIS systems and KCheck — enabling automatic case initiation when an offer is accepted in the ATS.

**2. Primary Actors**
Client IT Admin, Client Admin

**3. Key Workflows**
Select connector → Authenticate → Map fields → Configure triggers → Test → Activate → Monitor health

**4. States**
Not configured | Configuring | Sandbox testing | Active | Error (health check failed) | Disconnected

**5. UI Regions**
- Left: Available connectors list (Workday / SuccessFactors / Darwinbox / Keka / Generic REST)
- Center: Configuration wizard for selected connector
- Right: Health monitor (live status + last sync + error log)

**6. Cards**
- Connector Cards (catalog): Connector name, logo, connection status (Not connected / Connected / Error)
- Health Monitor Card (active connections): Last sync, success rate, error count (last 7 days), latency

**7. Connection Wizard Steps**
1. Authentication: OAuth 2.0 / API Key / Webhook secret — credential entry
2. Field Mapping: ATS candidate fields → KCheck fields (table with dropdowns)
3. Trigger Events: Which ATS event initiates BGV? (Offer Accepted / Pre-join / Manual trigger)
4. Package Mapping: Which ATS role type → which KCheck package
5. Sandbox Test: Send test payload, verify case created correctly
6. Activate

**8. Tables**
- Field Mapping Table: ATS Field | KCheck Field | Transformation (if needed) | Required (Y/N)
- Event Log Table: Timestamp | Event type | Payload summary | Status (Success/Failed) | Error (if failed)

**9. Drawers**
- Field Mapping Drawer: Detailed mapping with sample values from ATS (test payload)
- Error Detail Drawer: Full error payload for failed sync events — for IT debugging
- Webhook Config Drawer: KCheck → ATS outbound webhook (case status updates, report availability) — endpoint URL + secret + event types

**10. Modals**
- Test Connection Modal: Runs live test → "Connection successful. Test case created: [Case ID]" or "Connection failed: [error reason]"
- Disconnect Modal: "Disconnecting will pause auto-initiation. Active cases created via integration continue normally. Confirm?"

**11. Alerts/Banners**
- "Integration health check failed — [N] case initiations may have failed in last [N] hours" — red
- "Sandbox test successful — activate integration when ready" — green
- "API key expires in 7 days — please rotate before expiry" — amber

---



---

## GAP-11 FIX: SCIM Provisioning Configuration in Client Portal

### Addition to 6.2.11 Client User Administration + 6.2.16 Integration Settings

**SCIM Provisioning Tab in Integration Settings (6.2.16)**

Add new tab to Integration Settings page: "User Provisioning (SCIM)"

```
SCIM 2.0 USER PROVISIONING
─────────────────────────────────────────────────────────
Status: ● Connected | ○ Not Configured

Your organization's Identity Provider (IdP) can automatically 
create, update, and deactivate KCheck users via SCIM 2.0.

SCIM Endpoint (provide to your IT team):
https://api.kcheck.in/v1/scim/v2
Bearer Token: [Masked — click to reveal once] [Regenerate Token]

─────────────────────────────────────────────────────────
ATTRIBUTE MAPPING

IdP Attribute          → KCheck Field
─────────────────────────────────────────────────────────
userName               → Email (login identifier)
name.givenName         → First Name
name.familyName        → Last Name
emails[primary].value  → Email
active                 → Account Status

─────────────────────────────────────────────────────────
GROUP → ROLE MAPPING

IdP Group Name         → KCheck Role
─────────────────────────────────────────────────────────
BGV-TA                 → TA / HR Recruiter        [Edit]
BGV-Manager            → Hiring Manager           [Edit]
BGV-HRSS               → HR Shared Services       [Edit]
BGV-Admin              → Client Admin             [Edit]
BGV-RiskLegal          → Risk / Legal             [Edit]
[+ Add Group Mapping]

─────────────────────────────────────────────────────────
DEPARTMENT → BUSINESS UNIT MAPPING

IdP Department/CostCenter → KCheck BU
─────────────────────────────────────────────────────────
Engineering              → Engineering BU          [Edit]
Finance                  → Finance BU              [Edit]
[+ Add Department Mapping]

─────────────────────────────────────────────────────────
```

**Test Provisioning Panel**
```
TEST SCIM PROVISIONING

Test user email: [_______________]
[Test Create User] — sends SCIM CREATE to KCheck, verifies user appears
[Test Update User] — sends SCIM UPDATE, verifies role change reflects
[Test Deactivate User] — sends SCIM DELETE, verifies access revoked

Test Results: [Last test: 10-Jan-2025 14:32 — ✅ All tests passed]
```

**SCIM Activity Log**
```
RECENT SCIM EVENTS (last 30 days)

Timestamp          | Event      | User                | Result
10-Jan 14:32      | CREATE     | ravi.kumar@acme.com | ✅ Created — Role: TA
09-Jan 11:15      | UPDATE     | priya.s@acme.com    | ✅ Role changed: Viewer → Admin
08-Jan 09:00      | DELETE     | ex-employee@acme.com| ✅ Deactivated — 2 cases reassigned
```

**Drawers**
- SCIM Setup Guide Drawer: Step-by-step instructions for IT admin — how to configure SCIM in Okta / Azure AD / OneLogin / Generic IdP. Includes SCIM endpoint URL, required attributes, test procedure.
- Group Mapping Edit Drawer: Map IdP group to KCheck role. Warning if mapping would grant more permissions than current user's role (privilege escalation prevention).

---
### 6.2.17 Page: Client Adjudication Policy

**1. Page Objective**
Configure client-specific adjudication rules — which outcomes require client sign-off, pre-adverse notice settings, waiver pre-authorizations.

**2. Primary Actors**
Client Admin

**3. Key Workflows**
Define auto-approve threshold → Set client sign-off requirements → Configure pre-adverse notice preferences → Pre-authorize waiver types → Save → Audit

**4. Tables**
- Auto-Approve Rules Table: Outcome type | Auto-approve (Y/N) | Condition
- Sign-off Requirements Table: Outcome type | Requires client sign-off (Y/N) | SLA for response (days)
- Waiver Pre-authorization Table: Discrepancy type | Pre-authorized (Y/N) | Conditions

**5. Drawers**
- Pre-adverse Notice Config Drawer: Waiting period duration (default/custom), delivery method (email/WhatsApp/both), notice template preview

**6. Modals**
- Save Policy Modal: "Changes to adjudication policy affect all future cases. Existing cases in adjudication will use current policy until completed. Confirm?"

**7. Alerts/Banners**
- "All non-Clear outcomes require client sign-off — this may slow report delivery" — informational
- "Pre-adverse notices are legally required in some jurisdictions — KPMG will apply mandatory notices regardless of this configuration" — compliance note

---



---

## GAP-12 FIX: Report Validity and Re-Check Policy Configuration

### New Page: 6.2.19 Report Validity & Re-Check Policy

**1. Page Objective**
Allow Client Admin to configure report validity windows and automatic re-check triggers — ensuring BGV reports remain current for employees in monitored roles.

**2. Primary Actors**
Client Admin

**3. Key Workflows**
Set validity window per package → Configure re-check triggers → Set re-check package → Preview impact → Save → Monitor expiring reports

**4. UI Regions**
- Top: "Report validity and re-check rules are per-package. Changes affect new reports only — existing reports retain their original validity window."
- Validity configuration table (per package)
- Re-check trigger configuration
- Impact preview

**5. Validity Configuration Table**
| Package | Validity Period | Re-check Package | Re-check Notice (days before expiry) |
|---|---|---|---|
| Basic | 12 months ▼ | Basic ▼ | 30 days ▼ |
| Pro | 24 months ▼ | Pro ▼ | 45 days ▼ |
| Executive | 36 months ▼ | Executive ▼ | 60 days ▼ |
| [Custom Package] | [configure] | [configure] | [configure] |

**6. Re-Check Trigger Configuration**
```
Automatic Re-Check Triggers:

[✓] Validity period expiry — re-check initiated N days before expiry
[✓] Role change (from HRMS) — re-check when employee promoted to higher-risk role
    → Only run checks not already clear in the current report
    → Package for re-check: [dropdown — based on new role's risk tier]
[ ] Periodic schedule — re-check all employees in [role type] every [N] months
    → Applicable to: [role selector]
[ ] Continuous monitoring hit — HR team reviews and manually triggers
    (System creates re-check case when HR confirms — not fully automatic)
```

**7. Impact Preview**
"Preview: Employees whose reports expire in next 90 days: [N]. Estimated re-check volume per month: [N] cases."

**8. Report Inbox Addition — Expiry Indicator**
Add to Report Inbox (6.2.7): Expiry date column. "Expires in [N] days" indicator on reports nearing validity expiry. Badge: "Re-check due" for expired reports.

**9. Part 5 IA Addition**
Add to Client Portal IA (Part 5.2) under Configuration:
```
├── 4.9 Report Validity & Re-Check Policy
│   └── Page: Report Validity and Re-check Configuration
│       Purpose: Configure validity windows per package and auto re-check triggers
│       Triggers: Validity expiry | Role change | Periodic schedule | Monitoring hit
```

---
### 6.2.18 Page: Client Billing Dashboard

**RFP Reference:** RFP 18.10, RFP 22.1, RFP 22.2

**RFP Text:**
> *RFP 18.10: "Billing Dashboard — Configurable billing dashboard with visibility into client invoicing, revenue analytics etc."*
> *RFP 22.1: "Pricing transparency — Per-check and package pricing, add-on charges, volume slabs"*
> *RFP 22.2: "SLA penalties — Contractual penalties for SLA/TAT breaches"*

**Verdict:** EXPLICIT

**1. Page Objective**
Give Client Admin and Client Finance full, transparent visibility into current and historical invoices, per-check pricing, volume slab progression, add-on charges, and SLA penalty lines — satisfying RFP 18.10, 22.1, and 22.2.

**2. Primary Actors**
Client Admin, Client Finance Lead, Client DPO

**3. Key Workflows**
Review current billing period → View invoice line items → Check volume slab status → Review SLA penalties → Download invoice PDF → Dispute a line item → View billing history

**4. States**
Current Period (live) | Invoice Generated | Invoice Paid | Invoice Disputed | Invoice Overdue

**5. Actions**
Download invoice PDF, dispute a line item, view invoice detail, export to CSV, toggle billing period, contact KPMG billing, view volume slab history

**6. Data Blocks**

**Billing Overview Strip (top of page):**
```
┌───────────────┬───────────────┬──────────────┬───────────────┐
│ Current Period│ Total Checks  │ Volume Slab  │ SLA Penalty   │
│ Jan 2025      │ 642 checks    │ Slab 3       │ ₹ 4,800       │
│ ₹ 1,24,600    │ this month    │ (600–800 /mo)│ (2 breaches)  │
└───────────────┴───────────────┴──────────────┴───────────────┘
```

**Volume Slab Progression Widget:**
```
VOLUME SLAB — JANUARY 2025
[==========================================>       ] 642/800 (Slab 3)

Slab 1: 0–199 checks       ₹ 220/check
Slab 2: 200–599 checks     ₹ 200/check   ← Previous months
Slab 3: 600–800 checks     ₹ 190/check   ← YOU ARE HERE
Slab 4: 801+ checks        ₹ 175/check   (Reach in 158 more checks)

Per-check rate this month: ₹ 190
Estimated saving vs Slab 1: ₹ 19,350
```

**7. UI Regions**
- Top: Billing period selector (monthly/quarterly toggle) + Download All button
- Billing overview strip (KPI row)
- Volume slab progression panel
- Invoice line items table (primary content)
- SLA penalty register section
- Add-on charges section
- Billing history accordion (collapsed by default)

**8. Tables**

**Invoice Line Items Table:**
| # | Check Type | Cases | Unit Price | Slab Applied | Amount |
|---|---|---|---|---|---|
| 1 | Identity (KYC) | 642 | ₹ 45 | Slab 3 | ₹ 28,890 |
| 2 | Employment (Standard) | 598 | ₹ 80 | Slab 3 | ₹ 47,840 |
| 3 | Education | 512 | ₹ 60 | Slab 3 | ₹ 30,720 |
| 4 | Criminal (Basic) | 420 | ₹ 55 | Slab 3 | ₹ 23,100 |
| 5 | Address | 201 | ₹ 75 | Slab 2 | ₹ 15,075 |
| — | **Base Total** | | | | **₹ 1,45,625** |

**SLA Penalty Register:**
| Case Reference | Check Type | Breach Date | TAT Target | Actual TAT | Penalty | Status |
|---|---|---|---|---|---|---|
| CK-2024-4521 | Employment | 14-Jan | 3 days | 5.2 days | ₹ 2,400 | Applied |
| CK-2024-4389 | Criminal | 10-Jan | 5 days | 7.8 days | ₹ 2,400 | Applied |
| **Total Penalties** | | | | | **₹ 4,800** | |

**Add-On Charges Register:**
| Add-On Type | Count | Unit Price | Amount |
|---|---|---|---|
| Executive-level criminal (enhanced depth) | 12 | ₹ 350 | ₹ 4,200 |
| International employment verification | 8 | ₹ 600 | ₹ 4,800 |
| Video KYC session | 3 | ₹ 250 | ₹ 750 |
| Repeat check (re-initiation) | 5 | ₹ 100 | ₹ 500 |
| **Total Add-Ons** | | | **₹ 10,250** |

**Billing Summary Footer:**
```
Base checks:       ₹ 1,45,625
Add-on charges:  + ₹  10,250
Credit (disputes): - ₹      0
SLA penalties:   + ₹   4,800
                 ──────────────
TOTAL DUE:         ₹ 1,60,675
Invoice date: 01-Feb-2025 | Due date: 15-Feb-2025
```

**9. Cards**
- Volume Slab Card: Current slab, rate, threshold progress, estimated next slab threshold
- SLA Health Card: Count of breaches this period, total penalty, link to breach details
- Billing Alert Card: "Invoice generated — due [date]" / "Invoice overdue by [N] days — please pay"

**10. Drawers**
- Invoice Detail Drawer: Full line-by-line invoice with downloadable PDF; includes KPMG address, GSTIN, invoice number
- SLA Penalty Detail Drawer: Full case trail for each breached case — SLA timeline, actual events, reason for pause/resume (if any), penalty calculation formula shown
- Add-On Detail Drawer: Per-case breakdown of each add-on charge with case reference and charge rationale
- Volume Slab History Drawer: Month-by-month check volume and slab applied for trailing 12 months; useful for forecasting
- Pricing Transparency Drawer: Full pricing schedule as agreed in contract — read-only

**11. Modals**
- Download Invoice Modal: Select format (PDF / CSV) + Select period → [Download]
- Dispute Line Item Modal: (See GAP-15 FIX above — billing dispute tracking, already added)
- Request Invoice Correction Modal: "Flag an invoice for correction before payment" — free text + upload supporting evidence

**12. Tabs**
- Current Invoice | Invoice History | Pricing Schedule | Disputes

**13. Alerts/Banners**
- "Invoice INV-2025-01 is due on 15-Feb-2025 — [Pay Now] [Download Invoice]" — amber (7 days before due)
- "Invoice INV-2025-01 is OVERDUE — [Contact KPMG Billing]" — red (after due date)
- "SLA penalty applied this period — [N] breaches totalling ₹[X]. Dispute a penalty? [View Penalties]"
- "You are approaching Slab 4 — [N] more checks this month will unlock lower per-check pricing." — green, informational

**14. Filters**
Period (month/quarter/year) | Invoice status | Check type | Slab | Sort (newest/oldest/amount)

**15. Revenue Analytics Tab (RFP 18.10 — analytics requirement):**
- Spend-by-check-type bar chart (trailing 6 months)
- Monthly check volume trend line (with slab boundary overlays)
- Per-BU spend breakdown (if available from case data — linked to business unit tag at initiation)
- Year-on-year spend comparison
- Export analytics: CSV / PDF

**16. Mobile Considerations**
- Summary strip and pending invoice banner visible without scroll on mobile
- Tables horizontally scrollable on mobile with pinned first column (check type)
- Download/dispute actions accessible via floating action button on mobile

**17. Part 5 IA Confirmation**
Client Portal section 5. Billing & Invoicing — already present. This design depth fully satisfies the single-page IA entry with the required component complexity per RFP 22.1, 22.2, and 18.10.



## GAP-13 FIX: Subprocessor Register in Client Portal

### New Page: 6.2.20 Subprocessor Register

**1. Page Objective**
Provide Client Admin with transparent, always-accessible view of all third-party data processors involved in their candidates' background verification — satisfying GDPR Article 28(2) and RFP 22.3.

**2. Primary Actors**
Client Admin, Risk/Legal (Client)

**3. UI Regions**
- Top: "This register lists all third-party organizations (subprocessors) that process candidate personal data as part of your background verification service. It is maintained by KPMG and updated before any new subprocessor begins processing."
- Subprocessor table
- Change notification history
- Object to new subprocessor action

**4. Subprocessor Table**
| Subprocessor | Service Type | Data Processed | Processing Country | DPA Status | Effective Since |
|---|---|---|---|---|---|
| [Name] | Document OCR | Identity documents, photos | India | ✅ Active | 01-Jan-2024 |
| [Name] | Credit Bureau | Financial data (with consent) | India | ✅ Active | 01-Jan-2024 |
| [Name] | Sanctions Screening | Name, DOB, nationality | UK/India | ✅ Active | 01-Jan-2024 |
| [Name] | Biometric Processing | Facial biometrics | India | ✅ Active | 01-Jan-2024 |
| [Name] | Address Field Visits | Address, photos | India (regional) | ✅ Active | 01-Jan-2024 |

**5. Change Notification History**
```
CHANGE NOTIFICATIONS

Date          Change Type      Subprocessor      Status          Your Response
15-Nov-2024   New Addition     [Name]            30-day notice   Awaiting acknowledgement →
01-Oct-2024   Removed          [Name]            Effective       Informational
01-Jan-2024   Initial setup    (Multiple)        Effective       —
```

**6. Drawers**
- Subprocessor Detail Drawer: Full DPA details, data categories processed, transfer mechanism (SCC/Adequacy), data retention at subprocessor, contact for queries.
- Change Notice Drawer: Full details of proposed new subprocessor — same format as notification email. [Acknowledge] [Object] buttons with mandatory notes for objection.

**7. Modals**
- Object to New Subprocessor Modal: "Filing an objection. KPMG will review and respond within [N] business days. If the subprocessor cannot be excluded for your data, you will be notified and may have the right to terminate the contract without penalty."

**8. Part 5 IA Addition**
Add to Client Portal IA (Part 5.2) as new menu section:
```
├── 7. Compliance & Legal
│   ├── 7.1 Subprocessor Register
│   │   └── Page: Subprocessor Register
│   │       Purpose: GDPR Art. 28(2) compliant subprocessor transparency
│   │       Includes: Register table, change notifications, objection workflow
│   └── 7.2 Data Export & Exit Status  [see GAP-14]
```

---


---

## GAP-14 FIX: Client Exit Page in Client Portal

### New Pages: 6.2.21 Data Export & Exit Status

**Part 5 IA Addition**
Add to Client Portal IA (Part 5.2) under Compliance & Legal section (GAP-13):
```
└── 7.2 Data Export & Exit Status
    └── Page: Data Export and Exit Status
        Purpose: Visibility into contract exit progress, data export status, 
                 deletion certificate, transition support period
```

**New Page: 6.2.21 Data Export & Exit Status**

**1. Page Objective**
Give Client Admin visibility into their exit process — data export status, confirm receipt of exports, transition support period countdown, and deletion certificate download.

**2. States**
Not Initiated (KPMG must initiate after contract termination notice) | Export In Progress | Export Ready (awaiting client confirmation) | Transition Support Period | Deletion In Progress | Completed — Deletion Certificate Issued

**3. UI Regions (per state)**

**State: Export In Progress**
```
DATA EXPORT — IN PROGRESS

Your data export is being prepared. You will be notified when ready.

Package                        Status          ETA
Case records (JSON)            Generating...   [date]
BGV Reports (PDF)              Generating...   [date]
Audit logs (CSV)               ✅ Ready        —
Consent records (JSON)         Generating...   [date]
Document archive (ZIP)         Queued          [date] (may take up to 20 days)
Configuration export (JSON)    ✅ Ready        —
```

**State: Export Ready**
```
DATA EXPORT — READY FOR DOWNLOAD

Both export packages are ready. Please download and verify completeness 
before confirming receipt. Transition support period starts on your confirmation.

Metadata Package:
  [Download Secure Link ↓] — Link expires 72 hours | [Regenerate Link]
  Includes: Case records, Reports, Audit logs, Consent records, Configuration

Document Archive:
  [Download via Secure Transfer ↓] — [Transfer method: Encrypted link / External media]
  Includes: [N] documents, [N] photos, [N] GB total

[Confirm Receipt of Both Packages]
(Starts 30-day transition support period — deletion will be scheduled after 30 days)
```

**State: Transition Support Period**
```
TRANSITION SUPPORT PERIOD — ACTIVE

You have 30 days to verify your export and raise any data gaps.

Transition support ends: [date] (21 days remaining)

Have questions or found a gap in your export?
[Contact KPMG Transition Team] — Named contact: [KPMG Account Manager name]

Found missing data? [Report a Data Gap]
→ Gap report must be filed before transition support ends.
```

**State: Completed**
```
EXIT COMPLETED

All your data has been securely deleted from KCheck infrastructure.

Deletion Certificate:
  [Download Deletion Certificate (PDF) ↓]
  Certificate ID: [ID] | Issued: [date] | Valid for: permanent record

The deletion certificate confirms all candidate data has been deleted across 
all storage regions. Retain this certificate for your compliance records.
```

**4. Drawers**
- Data Gap Report Drawer: "Describe the missing data: [category / date range / case IDs]. KPMG will investigate and provide missing data within 5 business days."
- Deletion Certificate Detail Drawer: Full certificate contents — data categories deleted, regions purged, deletion timestamps per region, KPMG Admin who executed.

---


---

## GAP-15 FIX: Billing Dispute Tracking

### Addition to 6.2.18 Client Billing Dashboard

**Billing Dispute Section**

Add "Disputes" tab to Billing Dashboard:

**Open Disputes Table**
| Dispute ID | Invoice | Line Item Disputed | Amount | Filed Date | Status | KPMG Response Due | [View] |
|---|---|---|---|---|---|---|---|
| BD-001 | INV-2024-12 | SLA penalty — Case CK-456 | ₹2,400 | 08-Jan-2025 | Under Review | 28-Jan-2025 | [View] |

**Dispute Status Flow**
Filed → Under Review (KPMG ops reviewing) → Information Requested (KPMG needs more context) → Resolved — Upheld (credit note issued) | Resolved — Rejected (with explanation)

**File New Dispute Button**
[+ Dispute a Line Item] → opens Dispute Modal:
```
DISPUTE A BILLING LINE ITEM

Invoice: [dropdown — recent invoices]
Line item: [dropdown — items from selected invoice]
Amount disputed: [auto-filled, editable if partial dispute]

Reason for dispute:
○ SLA penalty was incorrectly calculated
○ SLA pause was not applied (candidate insufficiency / hold)
○ Check was not completed — should not be billed
○ Incorrect check type billed
○ Volume slab should have applied
○ Other: [___________________]

Supporting notes: [text area — max 500 chars]
Supporting documents: [upload — optional]

[Submit Dispute]
```

**Dispute Detail Drawer**
Full dispute timeline: filed → KPMG review → resolution. KPMG's response with explanation. Credit note reference (if upheld). Resolution date.

**Invoice Page Addition**
Add "Dispute" icon button next to each line item on invoice view. Tooltip: "Dispute this line item." One-click to open Dispute Modal pre-filled with this line item.

---
## 6.3 CANDIDATE PORTAL — Page Design Depth (Complete)

*(6.3.1 Consent & Disclosure, 6.3.2 Employment Entry Form, 6.3.3 Document Upload Center, 6.3.4 Biometric Capture, 6.3.5 Application Status Page — already written in expanded_p6_complete.md)*

---

### 6.3.6 Page: Invitation Landing Page

**1. Page Objective**
First impression of the BGV process — orient the candidate (who might be confused about why they received a link), build trust through client branding, and motivate them to begin.

**2. Primary Actors**
Candidate (external, often first-time BGV user, mobile)

**3. Key Workflows**
Receive invitation link → Land on page → Understand what it is and why → See expected effort/time → Click Begin

**4. States**
Valid invitation (active) | Expired invitation (link > configured expiry) | Already completed (re-visit after submission) | Cancelled (case closed by client)

**5. Actions**
Begin verification, change language, view privacy notice preview (brief), contact support

**6. Data Blocks**
Client branding (logo, color, welcome message), candidate name (pre-filled from invitation), expected sections list, estimated completion time, support contact

**7. UI Regions**
- Full-screen branded layout (client logo top-center)
- Welcome headline: "Your background verification for [Client Name]"
- Sub-text: What BGV is and why it's needed (plain language, not legal jargon)
- "What to expect" section: Step list with icons (Consent → Personal Info → Employment → Education → Documents → Submit) + time estimate per step
- Estimated total time: "Typically takes 15–25 minutes"
- Primary CTA: [Begin Verification] button (large, client color)
- Language selector (top right — persistent)
- Support link (bottom)

**8. Cards**
- "What you'll need" card: List of documents to have ready (based on package — dynamic)
  - e.g., "Aadhaar / PAN card, Employment documents (offer letters, relieving letters), Education certificates"
- "Your privacy" card: 3-line summary — "Your data is used only for background verification. You can access, correct, or delete it at any time. [Read full notice →]"

**9. Modals**
None — frictionless entry

**10. Alerts/Banners**
- Expired Link Banner: "This invitation link has expired. Please contact [Client HR contact] for a new link." — full-screen replacement of page content
- Already Submitted Banner: "You've already completed your verification. [Check your status →]"
- Cancelled Banner: "This verification has been cancelled. Please contact your employer for more information."

**11. Mobile Considerations**
- Full-screen mobile-first design
- [Begin Verification] button: minimum 56px height, thumb-accessible
- Language selector: large tap target, flag icons for recognition
- "What you'll need" section: collapsible on mobile (reduce scroll before CTA)
- Auto-detect language from device locale (apply as default selection)
- **RTL Layout (Arabic locale) [C-10 | RFP 11.9 | 4.10.5]:** When candidate selects Arabic (`ar-AE`), the entire page switches to RTL layout: `<html dir="rtl">`, layout mirrors (CTA button on left, language selector on right of RTL origin), text aligns right, Arabic font (Cairo or Noto Naskh Arabic) loaded. Step icons (→ between steps) flip direction. Client logo and branding remain centred. This RTL requirement applies to ALL Candidate Portal pages — not just Landing. RTL QA pass required for all 6.3.x pages in Arabic locale.

**12. Compliance Notes**
- No personal data collected on this page
- No tracking pixels, no third-party analytics (privacy by design)
- Privacy notice preview linked but not mandatory on this page (mandatory on consent page)

**13. SLA Components** None — this is pre-session

**14. AI Components** None

**15. Evidence Components** None

**16. Timeline/Audit**
Landing page visit event logged (timestamp, IP, device type, language selected, invitation token). This is the start of the candidate session audit trail.

---

### 6.3.7 Page: OTP Authentication

**1. Page Objective**
Verify candidate identity with OTP before allowing access to the verification form — ensuring the person with access to the candidate's mobile/email is the one filling the form.

**2. Primary Actors**
Candidate

**3. Key Workflows**
Pre-fill contact details (from invitation) → Send OTP → Candidate enters OTP → Session created | Fallback to email OTP if mobile fails

**4. States**
OTP Not Sent | OTP Sent (waiting for entry) | OTP Sent — Resend Available (after 30s cooldown) | OTP Verified | OTP Failed (wrong code) | OTP Expired | Max Attempts Exceeded (temporary lock)

**5. Actions**
Request OTP, enter OTP, resend OTP, switch to email OTP, contact support

**6. Data Blocks**
Candidate mobile (masked, from invitation), OTP delivery channel used, attempt count, session token on success, device fingerprint (captured background), geolocation (captured background, consent-disclosed)

**7. UI Regions**
- Client-branded header
- Mobile number display (masked: "OTP sent to +91 ••••• 67890")
- OTP entry: 6-digit individual input boxes (auto-advance on each digit)
- Resend button (disabled 30s, then active)
- "Use email instead" link (fallback)
- [Verify] button (or auto-verify on last digit entry)

**8. Cards**
- Delivery channel indicator: "Sent via WhatsApp" (or SMS/Email with channel icon)
- Resume session card (if returning candidate): "Welcome back, [Name]. Your previous progress is saved. [Continue where you left off]" — shown after OTP verification if prior session exists

**9. Modals**
- Max Attempts Modal: "Too many failed attempts. Please try again in [N] minutes or contact support." [Contact Support] button

**10. Alerts/Banners**
- "OTP not received? Check your WhatsApp messages, or [Resend] / [Use email instead]" — shown after 60 seconds without entry

**11. SLA Components** None — authentication is pre-SLA

**12. AI Components**
- Device fingerprint captured (background) — used downstream in fraud risk scoring
- Geo-location captured (background, consent already disclosed on landing page) — used downstream

**13. Mobile Considerations**
- OTP input: auto-trigger numeric keyboard on mobile
- Auto-read OTP from SMS (Android OTP autofill API where supported)
- WhatsApp OTP: deep-link to WhatsApp message for easy copying
- 6 individual boxes: large touch targets (minimum 44px each)
- Auto-submit on 6th digit entry (no [Verify] tap needed)

**14. Security**
- OTP valid for 10 minutes
- Max 3 failed attempts before temporary lockout
- OTP is single-use (invalidated on first correct use)
- Session token: JWT with expiry + device fingerprint binding
- IP rate limiting: max 5 OTP requests per IP per hour

---

### 6.3.8 Page: Personal Details Form

**1. Page Objective**
Collect candidate's personal identity information — the foundation data that links all other verification checks.

**2. Primary Actors**
Candidate

**3. Key Workflows**
Fill personal info → Real-time validation → Auto-save → Proceed to employment section | Resubmission: edit only flagged fields

**4. States**
Empty → Partially filled → Complete (all required fields valid) → Submitted | Resubmission mode (locked/editable fields)

**5. Actions**
Fill fields, correct validation errors, save and continue, go back to consent

**6. Data Blocks**
Full legal name, date of birth, gender (package-dependent), nationality, PAN, Aadhaar (optional consent toggle), current address, permanent address, mobile, alternate email, relationship declarations (package-dependent), directorship declarations (package-dependent)

**7. UI Regions**
- Progress bar (top, persistent): Step 1 of N highlighted
- Form body (scrollable)
- Auto-save indicator (bottom: "Saved" on each field blur)
- [Save & Continue] sticky bottom button

**8. Cards**
- "Why we need this" info card (collapsible): Plain-language explanation of why PAN/Aadhaar is needed — reduces abandonment from privacy concern

**9. Field-Level Components**
- PAN field: Masked input (shows AAAPA****A format), format validator (AAAAA9999A), info tooltip ("10-character alphanumeric — found on your PAN card")
- Aadhaar field: 12-digit, masked input, separate consent toggle ("I consent to use of Aadhaar for identity verification") — toggle is default-off, candidate must explicitly enable
- Address: Auto-complete from postal/geo API with "Enter manually" fallback
- Date of birth: Date picker — mobile-native on mobile; desktop custom picker
- Nationality: Searchable dropdown with country flags

**10. Drawers**
- Aadhaar Consent Drawer: "What Aadhaar verification means — how it is used, what is retained" — full explanation before consent toggle

**11. Modals**
- Name Mismatch Warning Modal: If name entered differs significantly from what was in the invitation — "The name you entered differs from your employer's records. Please confirm [entered name] is your legal name as per your ID documents. [Confirm] [Edit]"

**12. Validation Rules**
- PAN: AAAAA9999A format — real-time
- Aadhaar: 12 digits, Verhoeff algorithm check — real-time (format only, not API call at this stage)
- Date of birth: Must be 18+ years old
- Email: Valid format
- Mobile: 10-digit India / country-code format for international
- Name: No special characters except hyphen and apostrophe; minimum 2 characters

**13. Resubmission Mode**
- Locked fields: Read-only with lock icon. Tooltip: "Verified — cannot be changed."
- Flagged fields: Editable, orange border, ops remark above: e.g., "KPMG: Please confirm your date of birth — it does not match your Aadhaar record."

**14. Alerts/Banners**
- "All fields marked * are required"
- "Your progress is automatically saved every time you move to a new field"

**15. Mobile Considerations**
- Keyboard type per field: numeric for PAN suffix, date picker for DOB, address keyboard for address fields
- Long forms: Section dividers every 4–5 fields to break visual monotony
- "Permanent address same as current" checkbox: prominent on mobile (saves significant typing)
- Scroll position preserved on back navigation

**16. Compliance Notes**
- Aadhaar: explicit separate consent toggle per UIDAI guidelines
- Minimal data collection: Fields shown are only those required for the package (dynamic rendering)
- Data not transmitted until [Save & Continue] pressed (not on each keystroke)

---

### 6.3.9 Page: Education Entry Form


---

### 6.3.10 Page: Other Check-Specific Form Sections

**1. Page Objective**
Collect additional information required by specific check types in the candidate's package — address confirmation, reference contacts, financial declarations, legal declarations.

**2. Primary Actors**
Candidate

**3. Section: Address Confirmation (shown if address check in package)**

**Page Objective**
Confirm and geo-validate candidate's current and permanent residence addresses for physical or digital verification.

**Key Components**
- Current address (pre-filled from personal details — confirm or edit)
- Permanent address (pre-filled or separate entry)
- Address type: Owned / Rented / Family / PG / Hostel
- Duration at current address (from/to date)
- Previous address (if at current address < 2 years — shown conditionally)
- Landmark / nearby landmark (for physical visit navigation)
- Map confirmation: "Pin your location" map widget (candidate drags pin to confirm geo-location)
- Geocoding validation: If geo-pin is > 2km from address text → "The location you pinned seems far from the address entered. Please re-check."

**4. Section: Reference Contacts (shown if reference check in package)**

**Page Objective**
Collect professional reference contact details for KPMG to reach out to.

**Key Components**
- Reference 1 and Reference 2 (configurable count per package)
- Per reference: Name, current designation, current organization, relationship to candidate (Manager / Colleague / Client / Other), contact mobile, contact email
- "Note to candidate": "References should be professional contacts who can speak to your work experience. Please inform them they may be contacted."
- Validation: Reference cannot be the same person as candidate (name + mobile check)
- Cannot use personal references (family members) — soft warning if "Family" selected as relationship

**5. Section: Legal Declarations (shown if legal check in package)**

**Page Objective**
Capture self-declaration of any existing legal proceedings — for cross-reference with court record search.

**Key Components**
- "Have you ever been convicted of a criminal offense?" (Yes / No)
- If Yes: text field for details
- "Are there any pending criminal proceedings against you?" (Yes / No)
- If Yes: details field
- "Have you ever been banned from any regulated industry?" (Yes / No)
- If Yes: details
- Declaration checkbox: "I confirm the above declarations are accurate to the best of my knowledge. I understand that providing false information is grounds for termination."

**Important UX Note**
No guilt-implying language. All questions neutral. "Yes" answer does not block progress — flagged for adjudication but candidate not told their answer created a flag. Privacy note: "Your declarations are used solely for this background verification."

**6. Section: Financial Declarations (shown if credit check in package)**

**Page Objective**
Capture explicit separate consent for financial check + self-declaration.

**Key Components**
- Separate explicit consent: "I consent to KPMG conducting a credit bureau check as part of this background verification. Purpose: [stated purpose per client]. [Agree] [Decline]"
- If declined: "Declining the financial check may affect your background verification outcome. Your employer may be notified of this decision. Do you wish to proceed? [Decline anyway] [Agree]"
- Self-declaration: "Have you ever declared personal insolvency/bankruptcy?" (Yes / No + details if Yes)

**7. Mobile Considerations (all sections)**
- Conditional sections only appear if relevant to package — no empty sections shown
- Map pin widget: mobile-optimized — uses device GPS to auto-center map, then candidate adjusts
- Reference section: collapsible contacts for better mobile scroll management

---

### 6.3.11 Page: Review & Submit

**1. Page Objective**
Final checkpoint before formal submission — candidate reviews all entered information, confirms completeness, and submits. This is the last point of voluntary correction.

**2. Primary Actors**
Candidate

**3. Key Workflows**
Review all sections → Identify incomplete items → Edit (back to relevant section) → Confirm all complete → Sign declaration → Submit → Receive confirmation

**4. States**
Incomplete (some required sections missing) → Complete (all required items filled) → Submitted | Submission Failed (network error — retry)

**5. Actions**
Review sections (expand/collapse), edit any section (back navigation), confirm declaration, submit, download pre-submission summary (optional)

**6. Data Blocks**
Summary of all entered data per section, document upload status per document, completeness score per section, declaration text, submission timestamp on success

**7. UI Regions**
- Progress bar: Final step highlighted
- Section summary cards (collapsible): One per form section
- Completeness checklist (right column on desktop, below on mobile)
- Declaration section: Text + checkbox
- [Submit Application] button (sticky bottom — disabled until complete + declaration checked)

**8. Cards**
- Section Summary Cards (one per section): Section name | Status (Complete ✓ / Incomplete ⚠ / Optional) | Key data preview (e.g., "Employment: 3 employers added") | [Edit] link
- Document Checklist Card: Each required document with status (Uploaded ✓ / Missing ✗ / Quality: Fair ⚠)
- Completeness Indicator Card: Overall % complete — "You are 95% complete. Missing: [specific item]"

**9. Alerts/Banners**
- "1 required document missing — upload before submitting" — red, [Go to Documents] link
- "Some optional documents not uploaded — this may delay verification but will not block submission" — amber
- Resubmission mode banner: "You are updating specific information as requested by KPMG. Only highlighted fields have been changed."

**10. Modals**
- Submit Confirmation Modal: "You are about to formally submit your background verification. Once submitted, you cannot edit your information unless KPMG requests a correction. [Confirm Submission]"
- Submission Success Modal / Page: Full-screen success state:
  - Client-branded header
  - "Your background verification has been submitted successfully."
  - Case reference number (prominent)
  - "What happens next" timeline (KPMG reviews → verifications conducted → report delivered → employer decides — estimated [N] business days)
  - "You'll receive email and SMS updates on your verification status."
  - [Track your status] button

**11. Declaration Text (compliance-critical)**
"I declare that all information I have provided in this background verification application is true, accurate, and complete to the best of my knowledge. I understand that providing false or misleading information may result in disqualification from the recruitment process or termination of employment. I acknowledge that KPMG may verify any information I have provided with relevant third parties, in accordance with the consent I provided."

**12. Mobile Considerations**
- Submit button: sticky at bottom of viewport, always visible
- Section cards: fully collapsible on mobile (long review page is manageable)
- [Edit] links: navigate back to specific section preserving all other data
- Submission confirmation: full-screen, shareable case reference

---

### 6.3.12 Page: Re-submission Interface

**1. Page Objective**
Allow candidate to correct only the specific information flagged as insufficient by KPMG ops — without re-entering everything, and without being able to alter approved data.

**2. Primary Actors**
Candidate

**3. Key Workflows**
Receive re-submission notification → Log in via OTP → Land on this page → Read specific remarks per flagged field → Edit only flagged fields → Re-submit

**4. States**
Re-submission Required (flagged fields listed) → Editing (candidate updating) → Re-submitted → Under Review (ops reviewing re-submission)

**5. Actions**
Read remarks, edit flagged fields only, upload replacement documents, re-submit

**6. Data Blocks**
Flagged fields list (from ops), specific remarks per field, current submitted value (read-only for locked), editable current value for flagged fields

**7. UI Regions**
- Top: Prominent banner: "KPMG has requested additional information. Please review and update the highlighted fields."
- Section navigation: Tabs or accordion for each section with flagged fields
- Per flagged field: Orange border + remark box above the field
- Locked fields: Read-only with grey background + lock icon
- Re-submit button (sticky bottom, disabled until all flagged fields updated)

**8. Cards**
- Remarks Card (per flagged field): KPMG's specific instruction — e.g., "Please provide your correct end date at ABC Corp. The date you entered (Mar 2022) does not match our records." Orange border, icon, clear text.
- Re-submission Summary Card (on review step): Shows only changed fields for candidate to confirm before re-submitting

**9. Modals**
- Re-submit Confirmation Modal: "You are submitting updated information for: [list of changed fields]. [Confirm]"
- Re-submission Success: "Your updated information has been received. KPMG will continue your verification." + case reference + expected timeline

**10. Alerts/Banners**
- "Please update all [N] highlighted items before re-submitting" — amber count
- "Fields not highlighted are verified and cannot be changed" — informational

**11. Compliance Notes**
- Locked field enforcement is UI + API level (API rejects changes to non-flagged fields from candidate session)
- Re-submission creates a new audit event: original submission + re-submission both preserved
- Ops marks are field-level, not section-level — candidate does not need to re-fill entire section

**12. Mobile Considerations**
- Flagged fields clearly highlighted even on small screen (orange border + remark card above)
- Direct deep-link from notification to this specific page (not homepage)
- Re-submit button: large, sticky, prominent

---

### 6.3.13 Page: Dispute / Raise a Concern

**1. Page Objective**
Provide candidate with a self-service interface to challenge a finding, request data access, or raise a process concern — fulfilling DPDP/GDPR rights.

**2. Primary Actors**
Candidate

**3. Key Workflows**
Select concern type → Describe issue → Attach evidence → Submit → Track status → Receive resolution notification

**4. States**
Not submitted | Draft | Submitted | Under Review | Resolved | Closed

**5. Actions**
Select type, describe issue, attach evidence, submit, track status, view resolution

**6. Data Blocks**
Dispute type, description, supporting evidence, submission timestamp, resolution outcome (when available), communication on resolution

**7. UI Regions**
- Dispute type selector (prominent — top of page)
- Dynamic form based on type selected
- Evidence upload (optional)
- Submission confirmation

**8. Dispute Type Options (with plain-language labels)**
- "My information is incorrect in the verification" → Data Accuracy dispute
- "I believe there was a process error" → Process Complaint
- "I disagree with the verification outcome" → Outcome Challenge
- "I want to see what data KPMG holds about me" → Data Access Request (DSAR)
- "I want to correct my personal data" → Data Correction Request
- "I want my data deleted" → Data Erasure Request
- "Something else" → Free-form concern

**9. Form Components per Type**

Data Accuracy:
- Which check type the error is in (Employment / Education / Identity / Legal / Address / Financial)
- What is incorrect (description)
- What the correct information is
- Evidence upload (document proving correct information)

Outcome Challenge:
- Which aspect of the outcome is challenged
- Reason for challenge
- Supporting evidence

DSAR (Access):
- Confirmation of identity (OTP already completed)
- Specific data requested (or "all data held about me")
- Preferred format for response (email / download)

DSAR (Erasure):
- Which data to erase (or "all")
- Understanding of consequence (BGV may not be completable without data)

**10. Cards**
- "Your Rights" info card (above form): Plain language — "Under Indian data protection law, you have the right to access your data, correct inaccuracies, and challenge automated decisions." [Learn more →]
- Dispute Status Card (after submission): Submission reference + "Expected response within [N] business days per legal requirements"

**11. Modals**
- Erasure Consequence Modal: "Requesting erasure of your data while your background verification is in progress will end the verification process. Your employer may be informed. Are you sure you want to proceed?"
- Submission Confirmation Modal: "Your [type] has been submitted. Reference: [ID]. KPMG is legally required to respond within [N] business days."

**12. Alerts/Banners**
- "This concern will be reviewed by KPMG's compliance team. You will receive a response within [N] business days."

**13. Compliance**
- DPDP: Response required within 30 days
- Acknowledgment automated (immediate on submission — legal clock starts)
- Erasure requests: legal hold check performed by KPMG before acting

**14. Mobile Considerations**
- Type selector: Large card buttons (not dropdown) on mobile for easy tap
- Evidence upload: Camera capture supported
- Status check: Accessible from main status page

---


---

## GAP-EXP-L5 FIX: Jurisdiction-Specific Dispute Acknowledgement Notice — Candidate Portal

### L-5 | Jurisdiction-Specific Dispute Acknowledgement Notice — Missing from Candidate Dispute Page

**RFP Reference:** RFP 23.15

**RFP Text:**
> *"Region-specific dispute workflows — Local candidate rights and dispute processes encapsulated"*

**Verdict:** EXPLICIT

**Analysis:**
RFP 23.15 explicitly requires region-specific dispute workflows that encapsulate local candidate rights. A single-format dispute acknowledgement notice that does not vary by jurisdiction fails this requirement. Each jurisdiction has distinct statutory rights and timelines: GDPR (EU) mandates a 30-day response with Article 18 processing restriction right; FCRA (US-equivalent) mandates a 30-day free investigation period; DPDP (India) mandates 30-day grievance redressal with a right to correct. A generic "We received your dispute" acknowledgement does not encapsulate these local rights as required.

**Impact:**
- Candidates in EU jurisdictions receive no mention of GDPR Article 18 processing restriction right — a statutory entitlement that must be communicated at dispute filing.
- Candidates in FCRA-applicable workflows receive no notice of their right to a free investigation within 30 days.
- DPDP-scoped candidates receive no confirmation of the 30-day grievance redressal obligation — making KPMG's compliance unverifiable.

**Recommendation:**

---

### Addition to 6.3.13 Page: Dispute / Raise a Concern — Jurisdiction-Aware Acknowledgement

**Jurisdiction Detection:**
At dispute submission, the system determines the applicable regulatory framework based on:
1. Candidate's declared country of residence (from personal details form)
2. Client's configured jurisdiction(s) (from tenant configuration)
3. Fallback: KPMG India / DPDP (if no jurisdiction determinable)

**Jurisdiction-Specific Acknowledgement Notice (add to confirmation screen after dispute submission):**

**DPDP / India jurisdiction:**
```
✅ YOUR DISPUTE HAS BEEN RECEIVED

Dispute Reference: DISP-2025-0412

Applicable Law: Digital Personal Data Protection Act, 2023 (India)

Your Rights in This Dispute:
• You have the right to have your complaint addressed within 30 days.
• If your dispute relates to incorrect personal data, you also have
  the right to request correction (separate process).
• If not resolved, you may approach the Data Protection Board of India.

Next Steps:
KPMG will review your dispute and respond by: [date + 30 days]
You will be notified at [email] when your dispute is resolved.

Grievance Officer: [Name] | privacy@kpmg.in

[Download This Notice]
```

**GDPR / EU jurisdiction:**
```
✅ YOUR COMPLAINT HAS BEEN RECEIVED

Complaint Reference: DISP-2025-0412

Applicable Law: EU General Data Protection Regulation (GDPR)

Your Rights in This Complaint:
• Under GDPR Article 18, you have the right to request restriction
  of processing while your complaint is under investigation.
  [Request Processing Restriction →]
• KPMG must respond to your complaint within 30 days
  (extendable to 90 days with notification).
• If not resolved, you may lodge a complaint with your local
  Data Protection Authority (DPA).

Response Due By: [date + 30 days]
Processing of related verification data: [Continued / Restricted if you select above]

[Download This Notice]   [Find Your Local DPA →]
```

**FCRA-equivalent (US / applicable jurisdictions):**
```
✅ YOUR DISPUTE HAS BEEN RECEIVED

Dispute Reference: DISP-2025-0412

Applicable Law: Fair Credit Reporting Act (FCRA) — Equivalent Rights

Your Rights in This Dispute:
• You have the right to a free, complete investigation of your dispute.
• If the disputed information is found to be inaccurate or incomplete,
  it will be corrected or deleted.
• KPMG must complete the investigation within 30 days
  (extended to 45 days if you submit additional information).
• You have the right to add a statement of dispute to your file
  if KPMG disagrees with your correction.

Investigation Completion Target: [date + 30 days]

[Download This Notice]
```

**Processing Restriction Implementation (GDPR Article 18 — addition to Dispute Workbench 6.1.42):**

If candidate selects "Request Processing Restriction" on GDPR acknowledgement:
- Ops Portal Dispute Workbench: Banner appears on case — "⚠ GDPR Art. 18 Processing Restriction Active — Verification processing suspended per candidate request."
- Case workbench: all verification actions disabled until dispute resolved (per existing GAP-8 FIX)
- Candidate status page: updated status "Dispute Under Investigation — Processing Restricted"

**Audit Events:**
| Event | Data Logged |
|---|---|
| Dispute submitted | Jurisdiction identified, acknowledgement version served |
| Acknowledgement downloaded | Download timestamp, format |
| Processing restriction requested (GDPR) | Request timestamp, restriction applied |


### 6.3.14 Page: Help & Support

**1. Page Objective**
Provide candidates with self-service help and access to human support — reducing drop-off from confusion or technical issues.

**2. Primary Actors**
Candidate

**3. Key Workflows**
Search FAQ → If not answered: use chat / email / phone → Case reference auto-included in support contact

**4. States**
Browsing FAQ | Active chat | Email form submitted | Awaiting callback

**5. UI Regions**
- Search bar: "What do you need help with?" — searches FAQ
- FAQ accordion: Organized by stage (Getting Started / Consent / Filling the Form / Documents / Status / Technical Issues)
- Live chat widget: Bot-first with live agent escalation
- Contact options: Email form, Toll-free number, WhatsApp link

**6. FAQ Topics (key categories)**
Getting Started: What is background verification? Why is my employer doing this? How long does it take?
Consent: What am I agreeing to? Can I withdraw? What happens if I decline?
Form: What documents do I need? What if I don't remember exact dates? What is an employment gap?
Documents: What format? Camera tips. What if my document quality is rejected?
Status: How do I know when it's complete? What does "In Progress" mean?
Technical: OTP not received. Session expired. Camera not working. Can't upload file.

**7. Cards**
- Popular Questions Card: Top 5 most-searched FAQs (dynamic, based on usage analytics)
- "Still need help?" Card: Escalation options — Chat / Email / Phone — with expected response times

**8. Drawers**
- Chat Drawer: Embedded chat widget (slides in from right on desktop, full-screen on mobile)

**9. Modals**
None — support is a standalone page

**10. Alerts/Banners**
- "You're currently logged in as [case reference]. Include this in any support contact for faster assistance."

**11. Mobile Considerations**
- Chat widget: full-screen on mobile (not sidebar)
- Phone number: tap-to-call on mobile
- WhatsApp link: opens WhatsApp directly
- FAQ: accordion with generous tap targets

---


---

## GAP-EXP-M1 FIX: Candidate Rights Information Page — Candidate Portal

### M-1 | Candidate Rights Information Page — Missing

**RFP Reference:** RFP 11.12

**RFP Text:**
> *"Rights information — Clear presentation of candidate rights and policies"*

**Verdict:** EXPLICIT

**Analysis:**
RFP 11.12 is a standalone named requirement in the Candidate section. "Clear presentation of candidate rights" requires a dedicated, accessible interface — not rights embedded in the consent page as fine-print. A candidate who wants to understand their rights mid-journey or post-submission needs a consistent, accessible reference point that is distinct from the consent capture workflow. This page is the candidate-facing implementation of DPDP Chapter V rights and GDPR Articles 12–22 (right to information, access, correction, erasure, portability).

**Impact:**
- Without this page, candidates have no discoverable reference for their data rights during the BGV process.
- DPDP Section 12 (right to information) requires the data principal to have transparent access to rights information at any point.
- Absence increases candidate distress and support burden (candidates calling to ask "what are my rights?").

**Recommendation:**

---

### New Page: 6.3.17 My Data Rights — Candidate Portal

**1. Page Objective**
Provide candidates with a clear, plain-language, always-accessible presentation of their rights under applicable privacy law (DPDP/GDPR/FCRA-equivalent) — and direct links to exercise those rights.

**2. Primary Actors**
Candidate

**3. Access Path**
Candidate Portal persistent footer link "My Data Rights" | Help & Support → "My Data Rights" section | Post-submission status page "Your Rights" banner

**4. Key Workflows**
View rights → Select a right to exercise → Directed to appropriate action (DSAR form, correction form, dispute form, consent withdrawal)

**5. States**
Informational (always available) | Action triggered (when candidate clicks to exercise a right)

**6. UI Content Structure**

```
MY DATA RIGHTS
════════════════════════════════════════════════════

Your background verification is conducted by KPMG India.
You have the following rights regarding your personal data:

────────────────────────────────────────────────────
1. RIGHT TO ACCESS YOUR DATA
────────────────────────────────────────────────────
You may request a copy of all personal data KPMG holds
about you, including what was verified and when.
Timeline: Within 30 days of your request.
[Request Access to My Data →]

────────────────────────────────────────────────────
2. RIGHT TO CORRECT INACCURATE DATA
────────────────────────────────────────────────────
If any information about you is inaccurate or incomplete,
you have the right to request correction.
Timeline: Within 30 days of your request.
[Request a Correction →]

────────────────────────────────────────────────────
3. RIGHT TO DISPUTE VERIFICATION RESULTS
────────────────────────────────────────────────────
If you believe a verification outcome is incorrect or unfair,
you may file a formal dispute.
Timeline: KPMG will respond within 30 days.
[File a Dispute →]

────────────────────────────────────────────────────
4. RIGHT TO WITHDRAW CONSENT
────────────────────────────────────────────────────
You may withdraw your consent to this background verification
at any time. Please note: withdrawal may affect your employment
offer depending on your employer's requirements.
[Withdraw My Consent →]

────────────────────────────────────────────────────
5. RIGHT TO DATA PORTABILITY
────────────────────────────────────────────────────
You may request your personal data in a machine-readable
format for transfer to another service.
[Request Data Export →]

────────────────────────────────────────────────────
6. WHAT HAPPENS TO YOUR DATA?
────────────────────────────────────────────────────
Your data is used solely for background verification purposes.
Retention period: [configurable per client / jurisdiction]
After retention period: data is securely deleted per policy.

────────────────────────────────────────────────────
GRIEVANCE OFFICER
────────────────────────────────────────────────────
If you believe your rights have been violated:
Name: [Grievance Officer Name]
Email: privacy@kpmg.in
Phone: [Helpline number]
Response time: 7 business days

────────────────────────────────────────────────────
REGULATORY AUTHORITY
────────────────────────────────────────────────────
If your complaint is not resolved, you may contact:
[Applicable authority by jurisdiction — DPBI / ICO / etc.]
════════════════════════════════════════════════════
```

**7. Action Links (each navigates to respective page):**
- "Request Access to My Data" → DSAR form (6.3.13 Dispute / Raise a Concern — DSAR tab)
- "Request a Correction" → 6.3.16 Right-to-Correction Request (GAP-EXP-C6)
- "File a Dispute" → 6.3.13 Dispute / Raise a Concern — Dispute tab
- "Withdraw My Consent" → 6.3.1 Consent & Disclosure — Withdrawal flow (GAP-18 FIX)
- "Request Data Export" → DSAR form — Portability request type

**8. Alerts/Banners** None — purely informational page

**9. Mobile Considerations**
Accordion format on mobile: each right collapses/expands. Action links remain prominent. No horizontal scrolling.

**10. Part 5 IA Addition:**
Add to Candidate Portal IA (Part 5.3):
```
├── 8. My Data Rights
│   └── Page: My Data Rights
│       Purpose: Plain-language rights presentation; RFP 11.12; DPDP Section 12
│       Access: Footer link (persistent) + Help page + Status page banner
│       RFP: 11.12 | Classification: Compliance-Critical
```

---

## GAP-EXP-M2 FIX: Video KYC Scheduling — Candidate Portal & Ops Portal

### M-2 | Video KYC Scheduling Page — Missing from Candidate Portal and Ops Portal

**RFP Reference:** RFP 3.5

**RFP Text:**
> *"Video KYC for high-risk — Live/recorded video KYC with reviewer notes and audit trail"*

**Verdict:** EXPLICIT

**Analysis:**
RFP 3.5 explicitly names Video KYC as a required capability with three sub-components: live/recorded session, reviewer notes, and audit trail. The existing Biometric Capture page (6.3.4) handles passive/active liveness and face match. The Step-Up Verification page (GAP-16 FIX, 6.3.15) includes a brief mention of "Video KYC scheduling" as an escalation option. However, neither page provides the full Video KYC workflow — a dedicated scheduling interface for the candidate, a review workspace for the ops reviewer, and a session recording with audit trail. These three components are explicitly mandated by RFP 3.5.

**Impact:**
- High-risk candidates (packages requiring Video KYC, step-up escalations) have no defined UI path to complete this verification type.
- Ops reviewers have no workspace to conduct and document Video KYC sessions.
- No audit trail for video sessions = no evidentiary record for adverse decisions based on Video KYC.

**Recommendation:**

---

### Addition to 6.3.15 Step-Up Verification / New Sub-Flow: Video KYC Scheduling (Candidate)

**Candidate-Facing Video KYC Flow (addition to existing Step-Up page or as sub-page 6.3.15A):**

**State: Video KYC Required**
When a candidate's package or risk tier requires Video KYC (or step-up escalates to Video KYC):

**Calendar Scheduling Component:**
```
VIDEO VERIFICATION APPOINTMENT

A live video session is required to complete your
identity verification.

Please select a convenient time slot:

◄ January 2025 ►
Mo  Tu  We  Th  Fr
         [1]  [2]  [3]
[6]  [7]  [8]  [9]  [10]
Available slots shown in blue | Full slots greyed out

Selected: Tuesday 7 January 2025

Available times:
○ 10:00 AM – 10:20 AM  (20 mins)
● 11:00 AM – 11:20 AM  (Selected)
○ 2:00 PM – 2:20 PM
○ 4:00 PM – 4:20 PM

[Confirm Appointment]
```

**Pre-Session Preparation Screen:**
```
YOUR VIDEO APPOINTMENT IS CONFIRMED
─────────────────────────────────────────────────
Date: Tuesday 7 January 2025
Time: 11:00 AM IST
Duration: approximately 20 minutes
Link will be sent 10 minutes before your session.

Please prepare:
☐ Original photo ID (same as uploaded — Aadhaar/Passport)
☐ Good lighting (face clearly visible, no backlighting)
☐ Quiet location (audio must be clear)
☐ Stable internet connection

Device: Mobile or desktop with camera and microphone.

[Add to Calendar]   [WhatsApp Reminder On]
─────────────────────────────────────────────────
```

**During Session — Candidate Interface:**
- Simple join link (video widget embedded — WebRTC or vendor SDK)
- Camera/mic permission prompt on session start
- "You are now in session with a KPMG verification officer"
- End session button (candidate cannot end early without notification)

---

### New Panel: 6.1.10A Video KYC Review Workspace — Operations Portal Addition

**Addition to 6.1.10 KYC Verification Workspace — Video KYC Tab:**

Add "Video KYC" tab to the KYC Verification Workspace:

**Video KYC Tab Content:**

**Pre-Session:**
- Scheduled sessions list: Candidate name | Appointment time | Duration | Status (Scheduled / Joined / Completed / No-show)
- [Join Session] button (active 5 minutes before scheduled time)
- Candidate's submitted ID documents visible for side-by-side comparison during session

**During Session:**
- Video feed panel (reviewer sees candidate; candidate sees reviewer)
- ID document display (reviewer sees candidate's uploaded ID for comparison)
- Reviewer notes field (real-time text entry during session)
- Checklist:
  ```
  ☐ Identity confirmed — face matches submitted ID
  ☐ ID document visible and authentic
  ☐ Candidate confirmed identity verbally
  ☐ Liveness confirmed (real-time, not recording)
  ```
- Screen recording auto-starts (disclosed to candidate pre-session)

**Post-Session:**
- Outcome selector: Identity Confirmed | Unable to Confirm — Re-schedule | Fraud Suspected — Escalate
- Mandatory reviewer notes field (min 100 characters)
- Session recording stored in case evidence pack (encrypted, access-controlled)
- Audit event: session duration, reviewer identity, outcome, notes timestamp

**Audit Trail (per session):**
| Event | Data Logged |
|---|---|
| Session scheduled | Candidate request time, slot selected, confirmation sent |
| Session joined (candidate) | Join timestamp, device type |
| Session joined (reviewer) | Reviewer identity, join timestamp |
| Session completed | Duration, recording reference |
| Outcome declared | Outcome, notes, reviewer identity, timestamp |
| Recording stored | Storage reference, encryption key ID |

**Part 5 IA Addition:**
```
Candidate Portal (Part 5.3) — add under section 1 (Entry & Authentication):
├── 1.3 Video KYC Scheduling (triggered for high-risk packages or step-up escalation)
│   └── Page: Video Appointment Scheduling
│       Purpose: Candidate books video KYC slot; receives confirmation and joining instructions
│       RFP: 3.5 | Classification: Compliance-Critical

Ops Portal (Part 5.1) — add to section 3.1 KYC Workspace:
├── Video KYC Review (tab in 6.1.10 KYC Workspace)
│   └── Component: Video KYC Review Panel
│       Purpose: Reviewer conducts session, captures notes, declares outcome, auto-records
│       RFP: 3.5 | Classification: Compliance-Critical
```

---

## GAP-EXP-M3 FIX: Consent Renewal Page — Candidate Portal

### M-3 | Consent Renewal Page — Missing from Candidate Portal

**RFP Reference:** RFP 15.1

**RFP Text:**
> *"Consent lifecycle management — Capture, validate, store, renew, and withdraw consent with version history"*

**Verdict:** EXPLICIT

**Analysis:**
RFP 15.1 explicitly lists "renew" as one of five named consent lifecycle actions (capture, validate, store, renew, withdraw). A platform that captures and stores consent but provides no UI for the "renew" action fails to implement a named RFP requirement. Consent renewal is operationally necessary for long-running engagement cases (>12 months) where the initial consent expires. Without a candidate-facing renewal page, the consent expires silently and the platform has no lawful basis for continuing processing — a DPDP/GDPR violation.

**Impact:**
- Expired consent with no renewal UI means all processing after expiry is unlawful.
- No candidate-facing renewal page = ops must manually handle renewals, with no structured audit trail.
- Candidates receive a renewal notification but have nowhere to go to complete the renewal.

**Recommendation:**

---

### New Page: 6.3.18 Consent Renewal — Candidate Portal

**1. Page Objective**
Allow candidates to review and renew their consent for a background verification that has extended beyond the original consent period — with a fresh e-signature, updated receipt, and full audit record.

**2. Primary Actors**
Candidate

**3. Trigger**
Ops Lead triggers "Request Consent Renewal" action from Case Workbench (when consent is approaching expiry or has expired). Candidate receives email/WhatsApp/SMS notification with a deep-link to this page.

**4. Key Workflows**
Candidate receives renewal notification → Clicks link → OTP authentication (short-form, same as existing) → Reviews original and updated consent → E-signs renewed consent → Downloads updated receipt → System updates consent record

**5. States**
Renewal Pending | Under Review (OTP authenticated) | Renewed (signed) | Declined (candidate chose not to renew) | Expired (candidate did not respond — ops notified)

**6. Actions**
Authenticate via OTP, review consent text, e-sign, download updated receipt, decline renewal

**7. UI Regions**
- Header: client branding (persistent)
- Renewal notification card (context-setting)
- Consent text display (updated version if any changes; diff-highlighted if version changed)
- E-signature widget (same options as original: on-screen draw, type-to-sign, DocuSign)
- Confirmation and receipt download

**8. Renewal Notification Card:**
```
YOUR CONSENT NEEDS RENEWAL
─────────────────────────────────────────────────────
Your background verification is still in progress.
The consent you provided on [original consent date] has
reached its validity period.

To continue your verification, please review and renew
your consent below.

If you choose not to renew, your verification may be
stopped and you will be notified.
─────────────────────────────────────────────────────
```

**9. Consent Comparison Display (if consent version changed):**
```
WHAT HAS CHANGED IN THIS CONSENT?
──────────────────────────────────────────────────────
Version: 1.0 → 2.0 (updated [date])
Changes:
• Added: International data transfer disclosure (UK operations)
• Updated: Retention period (18 months → 24 months per new policy)
• No changes to: purposes, checks, your rights
──────────────────────────────────────────────────────
```

**10. E-Signature (same widget as 6.3.1 Consent & Disclosure)**

**11. Confirmation Screen:**
```
✅ CONSENT RENEWED

Thank you for renewing your consent.
Your verification will continue.

New consent version: 2.0
Date signed: [date/time]
Valid until: [date + new validity period]

[Download Updated Consent Receipt (PDF)]
[Return to Application Status]
```

**12. Decline Flow:**
- "I do not wish to renew my consent" → confirmation modal:
  "Are you sure? If you decline, your background verification will be stopped and KPMG will notify your employer that you withdrew consent. This may affect your employment offer. [Yes, decline consent] [Cancel]"
- On decline: Ops notified immediately; case enters "Consent Withdrawn" state; processing stops; audit event created.

**13. Audit Events:**
| Event | Data Logged |
|---|---|
| Renewal request sent | Request timestamp, notification channel, delivery status |
| Candidate authenticated | OTP success, device context, timestamp |
| Renewal consent signed | Consent version, signature method, timestamp, candidate IP |
| Renewal receipt generated | Receipt hash, storage reference |
| Consent declined | Declination timestamp, candidate acknowledgement |

**14. Part 5 IA Addition:**
Add to Candidate Portal IA (Part 5.3) under section 2 (Consent & Disclosure):
```
├── 2.2 Consent Renewal (triggered by ops when consent expires/near-expiry)
│   └── Page: Consent Renewal
│       Purpose: Candidate renews consent for extended verification engagement
│       RFP: 15.1 | GDPR Art. 7 | DPDP Section 6 | Classification: Compliance-Critical
```


## 6.4 VENDOR PORTAL — Page Design Depth (Complete)

*(6.4.1 Assignment Inbox, 6.4.2 Evidence Submission, 6.4.3 Vendor SLA Scorecard — already written in expanded_p6_complete.md)*

---

### 6.4.4 Page: Vendor Operations Dashboard

**1. Page Objective**
Give vendors a real-time overview of their active workload, SLA status, and performance — enabling self-management without KPMG having to chase them.

**2. Primary Actors**
Vendor Verifier, Vendor Team Lead, Vendor Manager

**3. Key Workflows**
Login → review new assignments → check SLA at-risk cases → act on urgent items → review performance snapshot

**4. States**
Live view (default) | Filtered by check type / geography

**5. Actions**
Acknowledge new assignments, open at-risk cases, drill into performance metric, go to assignment inbox

**6. Data Blocks**
New assignments (count + oldest), in-progress (count), completed today, SLA at-risk (count), overdue (count), performance scorecard snapshot, notification center (unread alerts)

**7. UI Regions**
- Top: Welcome strip + notification bell
- KPI strip: [New] [In Progress] [Completed Today] [At Risk] [Overdue]
- Left: SLA countdown list (top 5 most urgent)
- Center: Performance scorecard (mini)
- Right: Notification feed (new assignments, QC feedback, reminders)

**8. Cards**
- New Assignments Card: Count + [Go to Inbox] button. "Oldest unacknowledged: [N hours ago]" — urgency indicator.
- SLA At-Risk Card: Count of cases approaching SLA deadline. [View All] link.
- Overdue Card: Cases past SLA deadline. Red background. [Take Action] button.
- Performance Snapshot Card: SLA compliance % (this month), Quality score (this month) — both vs target.

**9. Tables**
SLA Urgency Table (condensed — top 5): Ref | Check type | Deadline | Hours remaining | Status | [Open]

**10. Drawers**
- Notification Drawer: All unread alerts — new assignments, QC returns, KPMG messages, SLA warnings

**11. Alerts/Banners**
- "You have [N] new assignments awaiting acknowledgment" — blue, persistent until acknowledged
- "[N] cases are past SLA deadline — contact KPMG if extension is needed" — red
- "QC returned [N] submissions for correction" — amber

**12. SLA Components**
SLA countdown in urgency table. Color-coded by health. Overdue cases shown in red section.

**13. Mobile Considerations**
Dashboard mobile view: KPI cards stacked. New assignments card always first. Notification badge on header. [Acknowledge All New] quick action button prominent on mobile.

---



---

## GAP-20 FIX: Vendor API Integration Settings

### New Page: 6.4.10 API Integration Settings (Vendor Portal)

**Part 5 IA Addition**
Add to Vendor Portal IA (Part 5.4) under Profile & Settings:
```
└── 5.3 API Integration Settings
    └── Page: Vendor API Integration
        Purpose: Configure API access for vendors using external platforms instead of KCheck portal
```

**New Page: 6.4.10 Vendor API Integration Settings**

**1. Page Objective**
Allow vendors with their own platforms to receive assignments, submit results, and receive status updates via API instead of (or in addition to) the KCheck Vendor Portal.

**2. Sections**

API Credentials:
```
API CREDENTIALS

API Key: bgv_vendor_[••••••••••••••••]  [Show] [Copy] [Regenerate]
Generated: 01-Jan-2025 | Last used: 10-Jan-2025 14:32

⚠️ Your API key provides full vendor portal access via API.
   Keep it secure — never share or commit to version control.
```

Webhook Configuration (KCheck → Your Platform):
```
WEBHOOKS — RECEIVE EVENTS FROM KCHECK

Endpoint URL: [https://your-platform.com/kcheck-webhook]  [Test]
Secret (for signature verification): [••••••••••] [Show] [Regenerate]

Events to receive:
[✓] vendor.assignment_created — New assignment available
[✓] vendor.qc_sent_back — Submission returned for correction  
[✓] vendor.sla_warning — SLA approaching breach
[✓] vendor.sla_breach — SLA breached
[ ] vendor.check_cancelled — Assignment cancelled

[Save Webhook Config]

Recent Deliveries: [Last 24h: 12 delivered, 0 failed]
```

API Endpoints Reference:
```
AVAILABLE ENDPOINTS

Assignment Management:
  GET  /v1/vendor/assignments                 — List your assignments
  GET  /v1/vendor/assignments/{id}            — Get assignment details + context package
  POST /v1/vendor/assignments/{id}/accept     — Accept assignment
  POST /v1/vendor/assignments/{id}/reject     — Reject with reason code

Evidence & Results:
  POST /v1/vendor/checks/{id}/evidence        — Submit evidence files
  POST /v1/vendor/checks/{id}/result          — Submit verification result

Status Updates:
  PATCH /v1/vendor/assignments/{id}/status    — Update assignment status

[View Full API Documentation →]
```

**3. Integration Health Monitor**
```
API HEALTH (last 7 days)

API calls:           1,247
Successful:          1,241  (99.5%)
Failed:              6      (0.5%)
Avg latency:         142ms
Webhook delivery:    98.8% (last 100 events)

[View Error Log]
```

---
### 6.4.5 Page: Active Assignment Workspace

**1. Page Objective**
Work interface for in-progress assignments — view candidate documents, update status, and submit evidence without leaving the workspace.

**2. Primary Actors**
Vendor Verifier

**3. Key Workflows**
Select case from active queue → Review candidate documents → Update status (In Progress / Awaiting Response) → Submit findings → View SLA countdown

**4. States**
In Progress | Awaiting Response (vendor sent outreach, waiting) | Evidence Ready (can submit) | Submitted (read-only)

**5. Actions**
View documents (scoped), update status, submit evidence (goes to Evidence Submission Interface), add internal note, contact KPMG ops (query)

**6. Data Blocks**
Case reference, check type, geography, SLA countdown, documents for this check (scoped to vendor's need), assignment notes from KPMG, current status, submission history

**7. UI Regions**
- Active cases list (left): All in-progress cases, SLA-sorted
- Case detail panel (center): Documents + status + evidence submission trigger
- SLA countdown (top of each case detail)

**8. Cards**
- Document Cards (scoped): Only documents relevant to this check type. E.g., employment check vendor only sees experience letters and payslips — not identity documents.
- SLA Card: Countdown + deadline date + assignment date

**9. Drawers**
- Document Viewer Drawer: View/download candidate document (scoped access — logged in audit)
- Evidence Submission Drawer: Opens evidence submission form inline (same as Evidence Submission page — accessible here for context)
- KPMG Query Drawer: Send message to ops with case reference pre-filled

**10. Modals**
- Status Update Modal: Move case to "Awaiting Response" — reason (sent employer email, awaiting HR callback, etc.) + expected response date

**11. Alerts/Banners**
- "SLA deadline in [N] hours" — red banner when < 20% time remaining
- "KPMG message received for this case" — notification dot on case in list

---

### 6.4.6 Page: Completed Assignments Archive

**1. Page Objective**
Archive of all submitted and completed assignments — reference for performance review and QC feedback review.

**2. Primary Actors**
Vendor Verifier, Vendor Team Lead

**3. Key Workflows**
Search completed case → Review submitted findings → Check QC feedback → Appeal QC error (via KPMG message)

**4. States**
Submitted (read-only) | QC Passed | QC Failed (returned, then corrected) | Disputed (vendor appeals QC finding)

**5. Tables**
Completed Table: Ref | Check type | Submitted date | Outcome declared | QC result | QC error type (if failed) | [View]

**6. Drawers**
- Submission Review Drawer: Read-only view of submitted evidence + outcome + QC feedback (if any)
- QC Feedback Drawer: Error type, KPMG's QC note, how to avoid in future — educational

**7. Filters**
Date range | Check type | QC result (Passed / Failed) | Geography

**8. Alerts/Banners**
- "[N] submissions returned by QC this month — review to improve quality score"

---

### 6.4.7 Page: Vendor Account Profile

**1. Page Objective**
Manage vendor organization details, coverage configuration, and compliance documents.

**2. Primary Actors**
Vendor Manager, Vendor Admin

**3. Key Workflows**
Update coverage areas → Upload/renew DPA → Update bank details → Review contract status

**4. Tables**
Coverage Matrix: Check type | Geography | SLA commitment | Active (Y/N)

**5. Drawers**
- Coverage Edit Drawer: Toggle check types and geographies on/off, update SLA commitment
- Document Upload Drawer: DPA, contract, ISO certification, insurance — mandatory documents with expiry tracking

**6. Alerts/Banners**
- "DPA document expires in 30 days — please renew" — amber
- "Coverage for [geography] is inactive — KPMG cannot assign cases for this area"

---

### 6.4.8 Page: Vendor Team Management

**1. Page Objective**
Manage vendor-side user accounts — who on the vendor's team can access which assignments.

**2. Primary Actors**
Vendor Manager

**3. Key Workflows**
Add verifier → Assign role → Set check type specialization → Deactivate departing staff

**4. Tables**
User Table: Name | Email | Role (Verifier / Team Lead / Manager) | Active assignments | Last login | Status

**5. Roles**
Verifier: Can view and submit assigned cases
Team Lead: Can view all vendor's cases, reassign within team
Manager: Full access + account settings

**6. Drawers**
- Add User Drawer: Name, email, role, check type specialization (which check types they're trained for)
- Deactivate Drawer: Reassign active cases to another verifier before deactivation

---

## 6.5 SUPER ADMIN PORTAL — Page Design Depth (Complete)

*(6.5.1 Tenant Provisioning Wizard, 6.5.2 AI Bias Monitor — already written in expanded_p6_complete.md)*

---

### 6.5.3 Page: Platform Command Center Dashboard

**1. Page Objective**
KPMG's highest-level operational view — platform health, all-tenant case volume, system status, AI service health, security alerts.

**2. Primary Actors**
KPMG Platform Admin, CTO, CISO (security events)

**3. Key Workflows**
Monitor system health → Identify degraded services → Review active incidents → Check AI model health → Monitor cross-tenant case volume

**4. States**
All healthy (green) | Degraded service (amber) | Critical incident (red)

**5. UI Regions**
- Top: Platform status banner (green "All systems operational" / amber/red with incident details)
- System health panel (real-time API/service status)
- Tenant health grid (all tenants at a glance)
- AI service health panel
- Security alerts panel
- Case volume (all tenants aggregated — anonymized)

**6. Cards**
- System Status Cards (per service): API gateway, Case service, Notification service, Document service, AI service, Auth service — Green/Amber/Red per service
- Tenant Health Card Grid: Tenant name tiles — color by health (any SLA issues, error rates)
- AI Health Card: OCR accuracy (today), Face match accuracy, Liveness pass rate, Fraud flag rate
- Security Card: Failed logins (last hour), Unusual access patterns, Geo-anomalies, Active incidents

**7. Tables**
Active Incidents Table: Incident ID | Severity | Service affected | Start time | Status | Owner

**8. Drawers**
- Service Health Detail Drawer: For any service — latency p50/p90/p99, error rate (last 1h/24h/7d), dependency status
- Tenant Health Detail Drawer: Specific tenant — case volume, SLA compliance, error rate, support tickets open

**9. Alerts/Banners**
- "Critical incident: [Service] is degraded — [N] tenants affected" — full-width red banner
- "AI model accuracy below threshold — investigation triggered" — amber

**10. Mobile Considerations**
Platform admins on mobile for incident alerts. Mobile: incident banner + service status cards. Full analytics on desktop.

---

### 6.5.4 Page: All Tenants Registry

**1. Page Objective**
Complete registry of all client organizations on the platform — with provisioning, status management, and configuration drill-in.

**2. Primary Actors**
Platform Admin

**3. Key Workflows**
View all tenants → Filter by status → Drill into tenant → Suspend/reactivate → Offboard

**4. States**
Active | Trial | Suspended | Offboarding | Offboarded

**5. Tables**
Tenant Table: Org name | Type | Status | Data residency | Active cases | Contract start/end | Primary contact | Case volume (MTD) | [View] [Suspend] [Offboard]

**6. Drawers**
- Tenant Detail Drawer: Full configuration summary (data residency, enabled checks, AI features, SLA templates, case volume, user count)
- Suspend Drawer: Reason + duration (temporary/indefinite) + notification to client admin
- Offboarding Drawer: Trigger offboarding workflow — data export schedule, deletion schedule, final invoice generation

**7. Modals**
- Suspend Confirmation Modal: "Suspending [Tenant] will immediately block all logins and API access. Existing cases are not deleted. Confirm?"
- Offboard Confirmation Modal: "Offboarding [Tenant] will initiate data export and scheduled deletion per contract terms. This cannot be undone. Confirm?"

**8. Alerts/Banners**
- "[N] tenants have contracts expiring within 30 days — renewal follow-up needed"
- "[Tenant X] has had [N] failed login attempts in last hour — security review recommended"

---

### 6.5.5 Page: Per-Tenant Deep Configuration

**1. Page Objective**
Edit any aspect of a specific tenant's configuration from the platform admin level — override defaults, enable/disable features, adjust data residency.

**2. Primary Actors**
Platform Admin

**3. Key Workflows**
Select tenant → Edit any configuration parameter → Publish changes → Audit log of all admin-made changes

**4. Sections**
- General: Org name, type, contract dates, primary contact
- Data Residency: Region selection (with migration trigger if changing)
- Check Types: Enable/disable + depth options per check type
- AI Features: Feature toggles per AI capability + threshold overrides
- SLA Templates: Override default SLA per check type
- Branding: Logo, domain, colors
- Pricing: Per-check pricing, volume slabs
- Compliance: GDPR/DPDP settings, data retention overrides, breach notification contacts

**5. Drawers**
- Data Residency Change Drawer: Impact assessment ("Changing from India to EU will trigger data migration — downtime: [estimate], candidate access during migration: [impact]") — requires Platform Admin + Legal sign-off
- AI Threshold Override Drawer: Per-model threshold adjustment for this tenant only

**6. Modals**
- Publish Changes Modal: "The following changes will be applied to [Tenant] immediately: [change summary]. Confirm?"

**7. Audit**
Every change logged: Platform Admin identity + before/after values + timestamp. Client Admin notified of significant changes (via email).

---



---

## GAP-24 FIX: Data Residency Migration Workflow

### Addition to 6.5.5 Per-Tenant Deep Configuration — Data Residency Change

**When Migration Is Triggered**
Changing a tenant's `data_residency_region` after the tenant is active requires a full data migration. This is not a config toggle — it initiates a complex infrastructure operation.

**Data Residency Change Section in Tenant Configuration Page**
Current residency display: "Current Data Residency: [Region] — [Storage cluster] — [Encryption KMS]"

[Change Data Residency] button (visible to Platform Admin only — not Client Admin):

**Step 1 — Impact Assessment (mandatory before proceeding)**
System generates real-time impact assessment:
```
Changing data residency from INDIA to EU will require:

• Migration of [N,XXX] case records to EU storage cluster
• Migration of [N,XXX] documents to EU object storage
• Encryption key migration (India KMS → EU KMS)
• All active candidate portal sessions will be invalidated (candidates must re-authenticate)
• Estimated downtime for this tenant: [X hours]
• Estimated migration duration: [X hours]
• Candidate portal access during migration: READ-ONLY (status check only — no form submission)

Legal requirements:
• New consent notice (EU/GDPR jurisdiction) required for all future cases
• Existing cases continue under original consent version
• SCCs required for any India-based ops team accessing EU-stored data
• Data transfer: India → EU requires adequacy assessment or SCCs
```

**Step 2 — Legal/Compliance Sign-Off (mandatory gate)**
- Assign Legal Reviewer: dropdown of users with Legal role
- Legal Reviewer receives in-platform notification + email
- Legal Reviewer must confirm: "I confirm the data residency change from [X] to [Y] has been legally assessed and SCCs/adequacy documentation is in place."
- [Approve] [Reject with reason] — both require mandatory note
- Cannot proceed to Step 3 without Legal approval

**Step 3 — Migration Scheduling**
- Maintenance window selector (calendar picker — must be within planned maintenance window or scheduled with client notification)
- Client notification trigger: auto-generates notification to Client Admin: "Your data residency will be migrated from [X] to [Y] on [date/time]. Candidate portal will be in read-only mode for approximately [X hours]."
- Client acknowledgement required (within 5 business days) before migration is scheduled

**Step 4 — Migration Execution (automated, monitored)**
Migration Status Tracker (replaces static config while migration in progress):
```
Data Residency Migration — IN PROGRESS
Started: [timestamp]
Progress:
  Case records: [████████░░] 82% — 4,210 / 5,128 records migrated
  Documents: [██████░░░░] 61% — 12,441 / 20,394 files migrated  
  Audit logs: [████████████] 100% — Complete
  Encryption key migration: [░░░░░░░░░░] Pending (starts after all data migrated)

Estimated completion: [time]
Current status: ACTIVE — candidate portal in read-only mode
Errors: 0
```

**Step 5 — Validation and Completion**
After migration completes:
- System runs validation: queries EU storage, verifies all records present, verifies India storage shows no remaining records for this tenant
- Encryption key migration executed and verified
- Candidate portal read-only mode lifted
- Platform Admin receives completion notification with: migration summary, record counts, any errors (zero expected), new residency region active timestamp
- Compliance log entry: "Data residency migrated from [X] to [Y]. Legal sign-off by [user]. Migration completed [timestamp]. [N] records migrated. Validation: passed."

**Failure Handling**
If migration fails mid-way:
- System automatically rolls back: copies back any partially migrated data, restores original residency
- Platform Admin receives incident alert (P1 severity)
- Candidate portal restored to full access immediately
- Failure logged with full diagnostic information

**Part 5 IA Addition**
Add to Super Admin Portal IA (Part 5.5) under Tenant Configuration:
```
└── Page: Data Residency Migration
    Purpose: Manage tenant data residency change with legal sign-off and monitored migration
    Triggered from: Tenant Configuration > Data Residency > [Change]
    States: Impact Assessment → Legal Approval → Client Notification → Scheduled → 
            Migration In Progress (read-only) → Validation → Complete | Rolled Back
```


---


---

## GAP FILLS — P0 CORE WORKFLOW


---
### 6.5.6 Page: Global Rule Engine

**1. Page Objective**
Configure platform-wide routing rules, auto-decisioning thresholds, escalation matrices, and risk scoring weights.

**2. Primary Actors**
Platform Admin

**3. Key Workflows**
Review active rules → Edit → Simulate impact → Publish → Monitor effect

**4. Sections**
- Auto-routing Rules: IF case [attributes] THEN assign to [reviewer type / team / queue]
- Auto-decisioning: Confidence thresholds for auto-approve (zero-flag cases only)
- Escalation Matrix Templates: Default escalation ladder for new tenants
- Risk Score Weights: Weight of each component in composite risk score
- SLA Policy Templates: Default SLA templates

**5. Tables**
Rule Table: Rule ID | Type | Condition | Action | Active (Y/N) | Last modified | Impact (cases/day affected)

**6. Drawers**
- Rule Edit Drawer: Full condition + action builder with condition grouping (AND/OR logic)
- Rule Simulation Drawer: "Run this rule against last 7 days of cases — [N] would have been affected. Preview results."

**7. Modals**
- Publish Rule Modal: "This rule will affect approximately [N] cases per day. Test in sandbox first? [Yes — run simulation] [Publish directly]"

**8. Alerts/Banners**
- "Rule [X] has not been reviewed in > 90 days — consider review for continued relevance"

---



---

## GAP-22 FIX: Routing Rule State Machine and Conflict Resolution

### Addition to 6.5.6 Global Rule Engine — Rule State Machine and Conflict Resolution

**Rule State Machine Display**

Each rule in the Rule Engine table shows a State badge:

| State | Badge | Description |
|---|---|---|
| Draft | Grey "Draft" | Being created/edited. Not executable. |
| In Test | Blue "In Test" | Available in simulation only. |
| Pending Approval | Amber "Awaiting Approval" | Activation requested. Legal/Risk review required. |
| Active | Green "Active" | Used by assignment engine for new cases. |
| Rejected | Red "Rejected" | Approval rejected. Returns to Draft. |
| Superseded | Grey "Superseded" | Newer version active. Historical reference. |
| Retired | Grey strikethrough "Retired" | No longer in use. |
| Archived | Grey "Archived" | Read-only. Retained for audit. |

**Rule State Transitions (enforced)**
```
Draft → In Test (on KPMG Admin save with "Move to Test")
In Test → Pending Approval (on KPMG Admin "Submit for Activation")
In Test → Draft (on KPMG Admin "Send Back to Draft")
Pending Approval → Active (on approver "Approve")
Pending Approval → Rejected (on approver "Reject")
Rejected → Draft (automatic — admin must edit before re-submitting)
Active → Superseded (when newer version of same rule activated)
Active → Retired (on KPMG Admin "Retire Rule")
Superseded/Retired → Archived (after 90 days — automatic)
```

**Mandatory Approval for Regulated Rules**
When submitting a rule for activation, system checks:
- Does this rule affect: criminal/legal check routing | adverse action workflows | cross-border data movement | vendor subprocessors | ban-the-box gating?
- If YES: "This rule requires Risk/Legal approval before activation."
- Approval assignment: mandatory selection of Risk or Legal reviewer
- Approver receives notification with: rule details, scope, predicted impact (from Test Mode simulation results)

**Conflict Detection on Save**

When KPMG Admin saves a new rule in Draft:
- System runs conflict check against all Active rules with overlapping scope
- If conflict found:
```
⚠️ RULE CONFLICT DETECTED

Your new rule conflicts with an existing active rule:

Existing Rule:  "Education-UK-Executive-SLA-High → Senior Reviewer Queue"  [Active]
Your New Rule:  "Education-UK-Executive → Standard Queue"
Conflict type:  Both rules match the same conditions but target different queues.

Resolution required before this rule can be activated:
Option 1: Change priority (make your rule higher priority to override existing rule)
Option 2: Edit conditions to reduce overlap
Option 3: Retire existing rule before activating this one

[Edit Priority]  [Edit Conditions]  [Retire Conflicting Rule]  [Cancel]
```

**Prohibition Override Lock**
Visual indicator on rules that enforce prohibitions (check_enabled: false):
```
🔒 PROHIBITION RULE — Cannot be overridden by permission rules
   This rule disables [check type] for [country/context].
   No other rule can re-enable this check for the same scope.
   Legal basis: [stored reference]
```

**Test Mode Simulation Output (enhanced)**
Add to simulation output:
```
SIMULATION RESULT

Case attributes: Education | UK | Executive | SLA Urgency: High

Matched Rules (in priority order):
1. [Rule ID] "Education-UK-Exec-High-SLA" → Priority: 90 [WINS]
2. [Rule ID] "Education-UK-All" → Priority: 50 [OVERRIDDEN — lower priority]
3. [Rule ID] "Global-Default" → Priority: 10 [OVERRIDDEN — lower priority]

Assignment Result:
  Reviewer Pool: Senior Reviewer — UK Education Specialist
  Queue: Urgent Review Queue
  Vendor: [Vendor A — UK education vendor]
  SLA: Client 12d | Internal 9d | Vendor 6d

Conflicts: None detected
Prohibited checks: Criminal check blocked (UK — ban-the-box — pending conditional offer)
```

---
### 6.5.7 Page: AI Model Registry

**1. Page Objective**
Track all AI model versions deployed across the platform — with performance metrics, rollback capability, and changelog.

**2. Primary Actors**
Platform Admin, AI Governance Lead

**3. Key Workflows**
Review model versions → Check accuracy metrics → Identify degrading models → Rollback if needed → Record model updates

**4. Tables**
Model Registry Table: Model name | Type | Current version | Deployed date | Accuracy (current) | Drift score | Status | [Details] [Rollback]

**5. Cards (per model)**
Model Card: Name | Version | Accuracy metric | Deployment date | Drift indicator (Green/Amber/Red) | Key performance chart (sparkline)

**6. Drawers**
- Model Detail Drawer: Full performance history — accuracy over time chart, false positive/negative rates, version changelog, sample decision examples
- Rollback Drawer: Select previous version → impact analysis ("cases processed in last [N] days would be re-evaluated") → confirm

**7. Alerts/Banners**
- "Model [X] accuracy dropped > [threshold]% in last 7 days — investigation triggered" — amber/red

---



---

## GAP-21 FIX: AI Model Deployment Change Control

### Addition to 6.5.7 AI Model Registry — Deploy New Version Workflow

**[Deploy New Version] Button**

Add to Model Registry page (6.5.7) per model row: [Deploy New Version] button (Platform Admin only).

**Model Deployment Wizard**

Step 1 — Upload New Model Artifact:
- Model type (pre-selected from row)
- Model version (semantic version: X.Y.Z)
- Release notes: what changed, performance improvements, known issues
- Model artifact upload (or vendor API version reference)

Step 2 — Sandbox Validation (mandatory):
```
SANDBOX VALIDATION

Deploy this model version to SANDBOX environment for testing.

[Deploy to Sandbox] → runs against 100 recent production cases
                       (data anonymized for sandbox)

Validation Metrics vs Current Production Model:
Metric                  Current v2.3.1    New v2.4.0    Change
Accuracy                94.2%             95.1%         +0.9% ✅
False positive rate     6.8%              5.9%          -0.9% ✅
Confidence calibration  87.3%             89.1%         +1.8% ✅
Processing latency p95  340ms             315ms         -25ms ✅

[Validation passed — proceed to approval]  [Validation failed — review issues]
```

Step 3 — Legal / Risk Review (conditional — required for high-impact models):
```
LEGAL / RISK REVIEW REQUIRED

This model (Face Match) makes decisions that directly affect employment 
outcomes. Legal and Risk team review is required before production deployment.

Assign Legal Reviewer: [dropdown]
Assign Risk Reviewer: [dropdown]

Reviewers receive notification with:
- Model change summary
- Validation metrics comparison
- Bias analysis results (showing no demographic performance regression)
- Sample predictions from sandbox validation

[Submit for Review]

Reviews received: 1 of 2
  ✅ Legal: Approved (10-Jan-2025) — "Performance improvement verified. No new legal risk."
  ⏳ Risk: Pending
```

Step 4 — Production Deployment:
```
PRODUCTION DEPLOYMENT

All approvals received. Ready to deploy.

Deployment impact:
• New model version will apply to all new AI checks from deployment time
• Cases already in progress will continue with model version locked at case creation
• Model version will be logged with every AI decision for audit

Deployment window:
○ Deploy now (immediate)  
○ Schedule for maintenance window: [Sunday 02:00-04:00 IST]

[Deploy to Production]
```

**Model Deployment Audit Log**
Every deployment event logged:
- Old version, new version, deployer identity
- Sandbox validation metrics (stored permanently)
- Approval records (legal + risk sign-offs)
- Deployment timestamp
- Cases affected (count of new cases that will use new version)

**Rollback (existing feature — add to deployment context)**
After deployment, [Rollback to v2.3.1] button available for 72 hours:
- Rollback creates a new deployment event back to prior version
- Cases processed with new version retain their version lock (consistent audit trail)
- Platform Admin notified with rollback confirmation

---


---

## GAP-25 FIX: AI Model Deployment Change Control Workflow (Module 21 supplement)

*(Note: This gap was identified as related to GAP-21 — both addressed above in GAP-21 Fix. The following adds the Change Control Policy reference in the Model Registry page.)*

### Addition to 6.5.7 AI Model Registry — Change Control Policy Reference

Add to Model Registry page (6.5.7) — new "Change Control Policy" info section:

```
CHANGE CONTROL POLICY

All AI model updates follow this mandatory process:

Step          Required For                           Approver
Sandbox test  All model versions                    Platform Admin (self-approve)
Legal review  Face Match, Fraud Detection,          Legal + Risk
              Risk Score, Auto-Decisioning
Risk review   Same as above                         Risk Lead
Bias analysis Required if subgroup metrics          AI Governance Lead
              change > 2% from prior version

Minimum time from sandbox to production: 
  Standard models: 48 hours
  High-impact models (listed above): 5 business days

Emergency deployment (P1 security fix):
  Bypass sandbox and approval — CTO sign-off required
  Post-deployment review within 48 hours
  Emergency deployments logged and reviewed in next AI governance meeting
```
### 6.5.8 Page: AI Decision Threshold Configuration

**1. Page Objective**
Configure confidence thresholds that determine when AI decisions are auto-approved vs require human review.

**2. Primary Actors**
Platform Admin (with mandatory Risk/Legal sign-off for changes)

**3. Key Workflows**
Review current thresholds → Simulate impact of threshold change → Get Risk/Legal approval → Publish → Monitor effect

**4. Tables**
Threshold Table: Model | Decision type | Current threshold | Auto-action | Last changed | Changed by | Impact (cases/day at this threshold)

**5. Drawers**
- Threshold Edit Drawer: Slider + impact preview ("Moving threshold from 85% to 80% would auto-approve [N]% more cases — [X] more per day. False positive risk: [estimate]")
- Approval Workflow Drawer: Submit threshold change for Risk/Legal sign-off — reason + impact statement

**6. Modals**
- Change Approval Modal: Risk/Legal reviewer approves/rejects threshold change with mandatory note. Change not published until approved.

**7. Alerts/Banners**
- "Auto-decisioning threshold changes require Risk/Legal approval — submit for review"
- "Threshold change pending approval for [N] days" — amber

---

### 6.5.9 Page: AI Explainability Audit

**1. Page Objective**
Review quality of AI-generated reason codes — ensuring they are accurate, human-readable, and defensible for regulatory purposes.

**2. Primary Actors**
AI Governance Lead, Compliance Officer

**3. Key Workflows**
Sample AI decisions → Review reason codes → Assess quality (accurate / misleading / generic) → Flag low-quality reason codes → Feed back to AI team

**4. Tables**
Reason Code Quality Table: Sample case ID | Model | Decision | Reason code text | Quality rating (Human-rated) | Actionable (Y/N) | Flagged for improvement (Y/N)

**5. Drawers**
- Sample Review Drawer: Full AI decision context — model input, output, reason code, reviewer's quality rating form

**6. Metrics**
- Reason code actionability rate (% that gave reviewer clear next action)
- Reason code accuracy rate (% that were factually correct per human review)
- Generic reason code rate (% that were too vague to be useful — e.g., "Document anomaly detected" with no specifics)

---

### 6.5.10 Page: Platform-Level Audit Log

**1. Page Objective**
Cross-tenant platform-level audit log — admin actions, tenant provisioning events, configuration changes, security events.

**2. Primary Actors**
Platform Admin, CISO, External Auditor

**3. Key Workflows**
Filter by event type → Review event detail → Export for compliance submission

**4. States**
Live (current) | Archived (cold storage)

**5. Tables**
Platform Audit Table: Event ID | Timestamp | Actor | Action type | Affected entity (tenant/model/rule) | Before value | After value | Event hash

**6. Drawers**
- Event Detail Drawer: Full payload, raw hash, chain position
- Export Drawer: Date range + event type filter + format (PDF/JSON)

**7. Filters**
Actor | Action type (Tenant Provisioning / Config Change / AI Model Update / Security Event / Admin Login) | Date range | Tenant affected

---


---

## GAP-EXP-M9 FIX: Admin Activity Log Viewer — Super Admin Portal (Full Design Depth)

### M-9 | Admin Activity Log Viewer — No Design Depth

**RFP Reference:** RFP 12.10

**RFP Text:**
> *"Admin Activity Log Monitoring — Track/log all admin actions with timestamp monitoring"*

**Verdict:** EXPLICIT

**Analysis:**
RFP 12.10 is a standalone named requirement: Admin Activity Log Monitoring with timestamp monitoring. The current architecture includes the Platform-Level Audit Log (6.5.10) for cross-tenant platform events, but this is distinct from the per-admin, per-action activity log required by RFP 12.10. Admin Activity Log Monitoring tracks every configuration action taken by admin users (Client Admins, Ops Admins, Platform Admins) — not just platform-level security events. The RFP-referenced admin activity log needs design depth with saved filter templates and asynchronous export capability (per Module 12.4 specification). The existing 6.5.10 has only 7 design depth items with no saved filters, no async export, and no admin-action-specific context.

**Impact:**
- Without detailed admin activity log design depth, frontend developers cannot build a compliant, queryable audit log.
- Regulators investigating a compliance incident (wrong rule applied, unauthorized configuration change) cannot receive a structured admin action trail.
- KPMG's internal auditors cannot perform admin access reviews — a SOC 2 Type II control requirement.

**Recommendation:**
Expand 6.5.10 Platform-Level Audit Log with Admin Activity Log Monitoring design depth additions, or add a dedicated sub-page.

---

### Addition to 6.5.10: Admin Activity Log Viewer — Full Design Depth Supplement

**Admin Activity Log Supplement (addition to 6.5.10 Platform-Level Audit Log):**

**1. Page Objective Supplement:**
In addition to cross-tenant platform events, the Admin Activity Log tracks every admin user action with full context — actor identity, role, action type, before/after values, affected entity, timestamp, IP address, and session ID. This provides a complete, queryable admin accountability trail for SOC 2 Type II and DPDP compliance.

**2. Admin Action Categories Tracked (complete taxonomy):**

| Category | Examples |
|---|---|
| User Management | Create user, assign role, deactivate account, reset password, delegate access |
| Package Configuration | Create package, add check, change check depth, activate/deactivate package |
| Rule Engine | Create rule, modify rule, activate rule, deactivate rule, change routing logic |
| Tenant Configuration | Onboard tenant, update tenant settings, change data residency, modify SLA config |
| Billing Configuration | Update pricing, create invoice, modify volume slab, apply SLA penalty |
| Consent Configuration | Update consent template, change consent version, modify purpose statement |
| Country Configuration | Add country, update regulatory rules, change check availability per country |
| AI Governance | Adjust threshold, approve model deployment, disable AI signal |
| Security Configuration | Update IP allowlist, change session timeout, modify MFA policy, rotate API key |
| System Access | Admin login, failed login, session timeout, session revocation |

**3. Admin Activity Log Table (enhanced):**

| Log ID | Timestamp | Actor | Role | Action | Entity | Before Value | After Value | IP Address | Session ID |
|---|---|---|---|---|---|---|---|---|---|
| LOG-004521 | 2025-01-10 14:32:11 | [Name] | Platform Admin | Updated pricing | Tenant: ABC Corp | ₹220/KYC check | ₹195/KYC check | 10.0.1.45 | SES-8921 |
| LOG-004518 | 2025-01-10 13:15:04 | [Name] | Client Admin | Created package | Package: ExecutivePro-v2 | (new) | (created) | 192.168.2.10 | SES-8910 |
| LOG-004502 | 2025-01-10 11:48:22 | [Name] | Platform Admin | Threshold change | AI Signal: Deepfake | 85% | 90% | 10.0.1.45 | SES-8891 |

**4. Saved Filter Templates (per Module 12.4):**

Admin users can save frequently used filter combinations:

```
MY SAVED FILTERS
────────────────────────────────────────────────
[★ Security Config Changes — Last 30 Days]
   Actor: All | Category: Security Configuration
   Date: Last 30 days

[★ Pricing Changes — Current Quarter]
   Actor: All | Category: Billing Configuration
   Date: Current quarter

[★ My Actions — This Week]
   Actor: [Current user] | Date: This week
────────────────────────────────────────────────
[+ Save current filter as template]
```

**5. Advanced Filters:**

| Filter | Options |
|---|---|
| Actor | Search by name / email / role |
| Action category | Multi-select (see taxonomy above) |
| Entity type | Tenant / Package / Rule / User / AI Model |
| Entity name | Search |
| Date range | Today / Last 7d / Last 30d / Custom |
| Sensitive changes only | Toggle — shows only changes flagged as high-impact |
| IP address | Filter by specific IP or subnet |
| Session ID | Trace all actions in a specific session |

**6. Async Export Capability (per Module 12.4):**

- [Export Admin Log] button → opens Export Drawer:
  - Format: PDF / CSV / JSON
  - Date range: select
  - Filters: apply current filter set to export
  - Delivery: Download (small exports < 10,000 rows) / Email link (large exports)
  - "Large export queued — you will receive an email when ready. Estimated: [time]."
- Export jobs tracked in "My Exports" panel:
  | Export ID | Requested | Filters | Status | Download |
  |---|---|---|---|---|
  | EXP-001 | 10-Jan 14:45 | All — Jan 2025 | ✅ Ready | [Download] |
  | EXP-002 | 10-Jan 14:48 | Security Config — 90 days | ⏳ Processing | — |

**7. Risk-Flagged Actions:**

System automatically flags high-risk admin actions for review:
- Pricing change > 20% variance
- AI threshold change (any direction)
- Role escalation (granting Super Admin to existing user)
- Tenant data residency change
- Bulk user deactivation (> 5 users in one session)

Flagged actions appear with red border in log table and are visible in the Super Admin notification panel.

**8. API Endpoint:**
`GET /v1/admin-activity-log?actor_id=&category=&entity_type=&from=&to=&page=&per_page=`
→ Returns paginated log with full context. Supports sort by timestamp (default desc).


### 6.5.11 Page: Security Incident Response Center

**1. Page Objective**
Manage security incidents — from detection through containment, notification (regulatory), and post-incident review.

**2. Primary Actors**
CISO, Platform Admin, Legal

**3. Key Workflows**
Incident detected → Triage → Assess breach status → Notify regulators if breach (within 72h GDPR/DPDP clock) → Contain → Remediate → Post-incident review

**4. States**
Detected | Triaging | Breach Confirmed | Notification In Progress | Contained | Remediated | Post-Incident Review | Closed

**5. Tables**
Incident Table: ID | Severity (P1–P4) | Type | Start time | Status | Affected tenants | Owner | Breach status

**6. Cards**
- GDPR/DPDP Notification Clock Card: 72-hour countdown from breach confirmation. Red when < 24h remaining.
- Affected Tenants Card: Which tenants' data was involved — with affected candidate count (estimate)

**7. Drawers**
- Incident Detail Drawer: Full incident timeline, containment steps, root cause (as known), evidence
- Breach Notification Drawer: Generate notification for DPA — pre-filled with incident details, authority contact (by country), send/schedule

**8. Modals**
- Breach Confirmation Modal: "Confirming breach status starts regulatory notification clock (72h under GDPR). Confirm breach?" [Confirm — starts clock] [Not a breach — close]
- CISO Escalation Modal: [Notify CISO] — triggers call/SMS alert

**9. Alerts/Banners**
- "Security incident requires your attention" — full-screen alert on login
- "Regulatory notification due in [N] hours" — persistent red banner

---

### 6.5.12 Page: Data Residency & Transfer Tracker

**1. Page Objective**
Verify that data is processed and stored within legally mandated geographies — and that any cross-border transfers have valid legal basis.

**2. Primary Actors**
Platform Admin, Privacy Officer

**3. Key Workflows**
Review data location per tenant → Detect any cross-border flows → Verify SCCs/adequacy decisions in place → Export compliance report

**4. UI Regions**
- World map visualization: Tenant pins colored by residency region
- Per-tenant residency table
- Cross-border transfer log
- SCC/adequacy status panel

**5. Tables**
Residency Table: Tenant | Mandated region | Actual storage region | Status (Compliant/Violation) | Last verified
Transfer Log: Timestamp | Source region | Destination region | Data category | Legal basis (SCC/Adequacy) | Volume (records count)

**6. Alerts/Banners**
- "Data residency violation detected: [Tenant] data replicated to [non-compliant region]" — critical red
- "SCC for [Transfer corridor] expires in 30 days — renew before expiry"

---

### 6.5.13 Page: Security Assurance Dashboard (Pen Test & Vulnerability Tracker)

**1. Page Objective**
Track security posture — open vulnerabilities from pen tests, CVE monitoring for platform dependencies, certification status.

**2. Primary Actors**
CISO, Platform Admin

**3. Key Workflows**
Review open vulnerabilities → Prioritize by CVSS score → Track remediation → Update certification status

**4. Tables**
Vulnerability Table: CVE/Finding ID | Source (Pen test / CVE feed) | Severity | CVSS score | Component affected | Status (Open/In Progress/Remediated) | Target date | Owner
Certification Table: Certification | Status | Expiry | Last audit date | Auditor

**5. Cards**
- Security Posture Card: Critical open / High open / Medium open / Low open — counts with trend vs last quarter
- Certification Status Cards: ISO 27001 / SOC 2 / PCI DSS (if applicable) — green (current) / amber (expiring) / red (expired)

**6. Alerts/Banners**
- "[N] critical vulnerabilities open > 30 days — escalation to CISO recommended"

---

### 6.5.14 Page: Platform-Wide Integration Registry

**1. Page Objective**
Manage all external API integrations — AI vendor APIs, government database APIs, notification providers, ATS connectors, HRMS connectors — with health monitoring and credential management. Also governs how HRMS and ATS systems create cases in KCheck automatically (F4 and F5 non-candidate flows — RFP 13.1, 13.2).

**2. Primary Actors**
Platform Admin, DevOps

**3. Key Workflows**
Review integration health → Rotate credentials → Add new integration → Configure HRMS/ATS auto-push behaviour → Review subprocessor registry (DPDP/GDPR)

**4. Tables**
Integration Table: Integration name | Type (AI/Gov DB/Notification/ATS/HRMS) | Status | Last success | Error rate (24h) | Latency p50 | Credential expiry | [Health] [Rotate Credentials]
Subprocessor Table: Vendor name | Service type | Data processed | DPA status | DPA expiry | Country of processing

**5. Drawers**
- Integration Health Drawer: Latency trend (7 days), error rate trend, timeout count, dependency graph
- Credential Rotation Drawer: Generate new API key, apply with zero-downtime rotation, confirm old key invalidated
- HRMS Connector Configuration Drawer (NEW — C-01 | RFP 13.1): See section 6A below
- API Case Creation Settings Drawer (NEW — C-01 | RFP 13.2): See section 6B below

**6. Alerts/Banners**
- "Credential for [integration] expires in 7 days — rotate now" — amber
- "Integration [X] error rate > [threshold]% — health check failing" — red
- "HRMS auto-push failed for [N] cases in last 24h — review error log" — red (new)

---

**6A. HRMS Connector Configuration (F4 — HRMS Auto-Push | RFP 13.1)**

> C-01 addition. Configures how client's HRMS system pushes candidate data to KCheck
> automatically on new hire events — creating cases without any human action.
> Per-tenant configuration (each client has their own HRMS connector settings).

Configuration fields per tenant HRMS connector:
```
HRMS Connector Settings — [Client Tenant Name]
─────────────────────────────────────────────────────────────────
Connector type:    SAP SuccessFactors / Workday / Oracle HCM /
                   BambooHR / Darwinbox / Custom (webhook)

Trigger event:     [New Hire] [Offer Accepted] [Onboarding Started]
                   (dropdown — what HRMS event fires the push)

Default package:   [Package selector — applied to all HRMS-pushed cases]
                   "Package applied to all cases from this connector unless
                    overridden by a package_id field in the HRMS payload"

Field Mapping:
  HRMS field          →  KCheck field
  [employee_name]     →  candidate.full_name
  [date_of_birth]     →  candidate.dob
  [personal_email]    →  candidate.email
  [mobile_number]     →  candidate.mobile
  [aadhaar_number]    →  candidate.identity.aadhaar
  [pan_number]        →  candidate.identity.pan
  [consent_field]     →  consent_obtained (must map to a boolean field)
  [Add mapping row]

Consent handling:
  ○ HRMS sends consent flag — map field above (system reads flag value)
  ● HRMS does not send consent flag — ops must confirm consent before
    activating each HRMS-sourced case

Post-push case status:
  ○ "Pending Ops Review" — ops must review and activate (default, recommended)
  ● "Auto-activate" — case goes directly to verification queue without ops review
    (Warning: only select if HRMS data quality is validated and trusted)

Ops notification on push:
  [✓] Notify ops team when HRMS case received
  Notification channel: [Email] [In-app] [Both]
  Notify: [All ops reviewers] [Team lead only] [Specific user]

Error handling:
  On validation failure:  [Notify ops] [Notify client HR contact] [Both]
  Client HR contact email: [___________________]

Two-way status sync:
  [✓] Send case status updates back to HRMS
  Webhook URL (HRMS receives updates): [___________________]
  Events to push back: [Case Activated] [Verification Complete] [Report Ready]
  Status field mapping: KCheck outcome → HRMS field name: [___________________]
─────────────────────────────────────────────────────────────────
[Test Connection]  [Save Configuration]  [Deactivate Connector]
```

HRMS Push Error Log (tab within Integration Health Drawer):
- Timestamp | HRMS Employee ID | Client | Error type | Field errors | Status (Resolved/Pending)
- [Retry] per failed push (re-sends the HRMS payload through validation)
- [Download Error Report] — Excel export for client to correct their HRMS data

---

**6B. API Case Creation Settings (F5 — ATS / Third-Party API | RFP 13.2)**

> C-01 addition. Configures REST API case creation for clients whose ATS or external systems
> call the KCheck API directly to create cases — fully automated, no portal used.
> Per-tenant API key management.

Configuration per client tenant:
```
API Case Creation Settings — [Client Tenant Name]
─────────────────────────────────────────────────────────────────
API keys:
  Key ID          Created        Last used       Scopes         Status
  key_abc123      01-Jan-2026    15-May-2026     cases:write    Active   [Rotate] [Revoke]
  key_def456      01-Mar-2026    —               cases:read     Active   [Rotate] [Revoke]
  [Generate New API Key]

Default package (API-created cases):
  [Package selector — applied when no package_id in API payload]

Post-creation case status:
  ○ "Pending Ops Review" (default — ops must activate)
  ● "Auto-activate" (direct to verification — for trusted high-volume clients)

Rate limit:
  Max cases per hour: [100]  Max cases per day: [500]
  (Prevents accidental bulk flooding; client notified when limit approached)

Sandbox environment:
  [✓] Enable sandbox for this tenant
  Sandbox API URL: https://sandbox-api.kcheck.in/v1/
  Sandbox cases are not verified — for integration testing only

Webhook configuration (two-way status sync):
  Status update webhook URL: [___________________]
  Events: [Case Created] [Case Activated] [Verification Complete] [Report Ready]
  [Test Webhook]  [Save]

Consent enforcement:
  consent_obtained field is MANDATORY in all API payloads.
  Requests with consent_obtained: false or absent → rejected (HTTP 422).
  API caller legally certifies consent by setting this field to true.
─────────────────────────────────────────────────────────────────
[Save Settings]
```

API Usage Log (tab in Integration Health Drawer):
- Timestamp | Endpoint | Status code | Case ID (if created) | Error (if failed) | Processing time
- Filter: date range / success / failure / rate-limit hits
- [Download log — CSV]

Ops Queue filter additions (both HRMS and API flows):
- "HRMS Sourced" filter tag in All Cases (6.1.4) — shows all cases created via HRMS connector
- "API Created" filter tag in All Cases (6.1.4) — shows all cases created via API
- Both tags visible in Case Detail top bar for ops context

---

**6C. Ticketing Connector Configuration (C-06 | RFP 13.9)**

> Integrates KCheck with KPMG's enterprise ITSM platform (ServiceNow and/or Jira).
> Allows KCheck events to auto-create tickets, ops users to manually raise tickets from
> the Case Workbench, and ticket status to sync back to KCheck without context-switching.
> RFP 13.9: "Integration with ServiceNow/Jira for incidents and requests."

```
TICKETING CONNECTOR CONFIGURATION
─────────────────────────────────────────────────────────────────────────────
Connected systems (enable one or both):
  [✓] ServiceNow   Instance URL: [________________________]
                   Auth method:  [OAuth 2.0 ▼]
                   Client ID:    [________________________]
                   Secret:       [••••••••••••]
                   [Test Connection]

  [ ] Jira         Instance URL: [________________________]
                   Auth method:  [API Token ▼]
                   Email:        [________________________]
                   API Token:    [••••••••••••]
                   Project key:  [________________________]
                   [Test Connection]

Default system for manual ticket creation (ops): [ServiceNow ▼]
─────────────────────────────────────────────────────────────────────────────
EVENT-TO-TICKET MAPPING RULES

When this KCheck event fires → Create this ticket automatically:

  KCheck Event                    │ System      │ Ticket Type      │ Priority │ Assign To
  ────────────────────────────────┼─────────────┼──────────────────┼──────────┼───────────────────
  Client SLA breached             │ ServiceNow  │ Incident         │ P2       │ Account Mgmt group
  System integration failure      │ ServiceNow  │ Incident         │ P1       │ IT Operations group
  AI model confidence degraded    │ Jira        │ Bug              │ P2       │ KCheck Dev board
  Vendor unresponsive > [N] days  │ ServiceNow  │ Service Request  │ P3       │ Vendor Ops group
  [Add rule row]

  Each rule:
    Enabled toggle | KCheck event (dropdown) | Target system | Ticket type |
    Priority | Assignee group | Title template | Description template | Conditions

  Title template example: "KCheck SLA Breach — {client_name} — {case_id}"
  Description template: auto-populates {case_id}, {client_name}, {check_types},
                        {sla_target}, {elapsed}, {ops_reviewer}, {case_url}
─────────────────────────────────────────────────────────────────────────────
STATUS SYNC CONFIGURATION

How KCheck learns when a ticket resolves:

  ○ Webhook (preferred):
      KCheck webhook URL (read-only, copy for ServiceNow/Jira config):
      https://api.kcheck.in/webhooks/ticketing-status
      → ServiceNow/Jira posts status updates here on ticket change
      → KCheck updates linked ticket status in real time

  ● Polling (fallback):
      Poll interval: [15 minutes ▼]
      → KCheck calls ServiceNow/Jira API every N minutes for linked ticket status
      → Recommended only if webhook setup is not possible

  Sync events: [✓] Ticket assigned  [✓] Ticket resolved  [✓] Ticket closed
               [ ] All status changes (verbose — use for debugging only)
─────────────────────────────────────────────────────────────────────────────
ESCALATION QUEUE INTEGRATION (Optional)

When a KCheck internal escalation reaches severity threshold,
also create an external ticket automatically:

  Escalation type          │ Severity threshold │ Create ticket in
  ─────────────────────────┼────────────────────┼──────────────────
  SLA escalation           │ P1 only            │ ServiceNow (P2)
  Fraud investigation      │ All                │ ServiceNow (P1)
  Client complaint         │ All                │ ServiceNow (P3)
  [Disabled — not mapped]  │                    │
  [Add mapping]

  Note: Internal escalation workflow in Ops Portal (2.5) is unchanged.
  External ticket is created in addition to — not instead of — the internal escalation.
─────────────────────────────────────────────────────────────────────────────
TICKETING HEALTH MONITOR

  ServiceNow connection:    ✅ Connected   Last sync: 2 min ago   Tickets open: 3
  Jira connection:          ❌ Not configured
  Auto-ticket rules:        4 active rules | 0 errors in last 24h
  Recent tickets created:   [View log — last 20 auto-created tickets with status]
─────────────────────────────────────────────────────────────────────────────
[Save Configuration]
```

---

**1. Page Objective**
Configure pricing per tenant, invoice schedules, SLA penalty calculation rules, and billing reports.

**2. Primary Actors**
Platform Admin, Finance

**3. Key Workflows**
Set per-tenant pricing → Configure volume slabs → Set invoice schedule → Calculate SLA penalties → Generate invoices

**4. Tables**
Pricing Table: Tenant | Check type | Unit price | Volume slab configuration
Invoice Schedule Table: Tenant | Frequency (Monthly/Quarterly) | Invoice date | Last invoice | Status

**5. Drawers**
- Pricing Edit Drawer: Per-tenant per-check pricing with volume slab configuration
- SLA Penalty Drawer: Configure penalty calculation (penalty per day per breach, max cap)
- Invoice Preview Drawer: Preview invoice for selected tenant and period before generating

**6. Modals**
- Generate Invoice Modal: "Generate invoice for [Tenant] for [Period]? Total: [amount]. [Confirm]"

---

**6D. Legacy SOAP API Management (C-12 | RFP 13.1, 13.2 — Migration Bridge)**

> Manages the SOAP→REST migration bridge for legacy HRMS/SAP clients.
> Per architectural decision 4.11, the bridge is active for 12 months post go-live,
> then decommissioned. This section provides visibility and control over that sunset.

```
LEGACY SOAP API — MIGRATION MANAGEMENT
─────────────────────────────────────────────────────────────────────────────
Adapter status:   ✅ Active   |   Sunset date: [Go-live date + 12 months]
Days until sunset: [N] days   |   Clients migrated: 2 / 5

Sunset countdown banner (shows when < 90 days):
  ⚠️ "SOAP adapter decommissions in [N] days.
      [N] clients have not yet migrated to REST. [Notify All]"
─────────────────────────────────────────────────────────────────────────────

REGISTERED SOAP CLIENTS

  Client Name       │ SOAP Operations Used     │ Daily Calls │ Migration Status
  ──────────────────┼──────────────────────────┼─────────────┼──────────────────
  HDFC Bank (SAP)   │ InitiateBGV, GetBGVStatus│ ~45/day     │ In Progress
                    │                          │ (trending ↓)│ REST testing begun
  ──────────────────┼──────────────────────────┼─────────────┼──────────────────
  Infosys (HRMS)    │ GetBGVStatus only        │ ~12/day     │ Not Started
  ──────────────────┼──────────────────────────┼─────────────┼──────────────────
  Client C (SAP HR) │ All three operations     │ ~30/day     │ Complete ✅
                    │                          │ (0 calls 8d)│ REST migrated
  ──────────────────┼──────────────────────────┼─────────────┼──────────────────
  [Add registered client]

Per-client actions:
  [View call log]  [Send migration notice]  [Mark complete]  [View REST migration guide]

─────────────────────────────────────────────────────────────────────────────

SOAP CALL VOLUME TREND (last 30 days)
  [Line chart: total SOAP calls per day, all clients stacked]
  Target trend: declining toward zero before sunset date.
  Alert threshold: any client with SOAP calls > 0 in the 7 days before sunset.

─────────────────────────────────────────────────────────────────────────────

AUTOMATED NOTIFICATIONS (migration schedule)
  Day 0 (go-live):     ✅ Sent — Initial migration notice to all SOAP clients
  Day 90 (month 3):    ✅ Sent — First progress reminder
  Day 270 (month 9):   ⏳ Scheduled — 90-day sunset warning
  Day 330 (month 11):  ⏳ Scheduled — 30-day final warning
  Day 365 (month 12):  ⏳ Scheduled — Decommission confirmation

  [Send custom notice to selected clients]
  [Preview notification template]

─────────────────────────────────────────────────────────────────────────────

DECOMMISSION CONTROLS (Platform Admin only — visible 30 days before sunset)
  [Decommission SOAP Adapter]
  "After decommissioning, SOAP endpoint will return HTTP 410 Gone.
   This action cannot be undone. Confirm that all registered clients
   have migrated to REST (status = Complete) before proceeding."
  Pre-flight check: [Run check — confirms all clients show 0 SOAP calls for 7+ days]
─────────────────────────────────────────────────────────────────────────────
```

---

### 6.5.16 Page: Build, Release & Feature Management

**1. Page Objective**
Manage platform deployments, feature flags, maintenance windows, and rollbacks.

**2. Primary Actors**
Platform Admin, DevOps Lead

**3. Key Workflows**
Review deployment status → Toggle feature flags → Schedule maintenance → Rollback if needed → Manage CI/CD pipeline status

**4. Tables**
Deployment History: Version | Environment | Deploy time | Deployer | Status (Success/Rollback) | Changes summary
Feature Flag Table: Feature name | Environment | Enabled tenants | Status | Created by | [Toggle] [Expand to all]

**5. Cards**
- Environment Status Cards: Dev / UAT / Prod — deployed version, last deploy time, health status
- Active Feature Flags Card: Count enabled per environment

**6. Drawers**
- Feature Flag Edit Drawer: Enable for specific tenants (canary rollout), enable for all, disable
- Maintenance Mode Drawer: Configure maintenance window — portal(s) affected, start/end time, user-facing message editor (candidates and clients see this message during maintenance)
- Rollback Drawer: Select version to roll back to → impact assessment → confirm

**7. Alerts/Banners**
- "Production deployment in progress — avoid config changes until complete"
- "Maintenance window scheduled for [date/time] — tenant notifications sent"

---


---

## GAP-EXP-M5 FIX: Regulatory Change Management Workflow Page — Super Admin Portal

### M-5 | Regulatory Change Management Workflow Page — Missing from Super Admin

**RFP Reference:** RFP 23.16

**RFP Text:**
> *"Regulatory change management — Process to update rules when country laws change"*

**Verdict:** EXPLICIT

**Analysis:**
RFP 23.16 is a standalone named requirement. "Process to update rules" in a multi-country, compliance-critical platform requires an admin UI workflow — not merely backend capability. The platform operates across jurisdictions (India, UK, EU) where privacy laws, criminal check restrictions, and adverse action regulations change periodically. Without a structured change management process, regulatory updates are applied ad-hoc without version control, impact assessment, approval workflow, or audit trail. The six-step regulatory change management process (defined in Module 12.3) requires a corresponding UI home in the Super Admin Portal.

**Impact:**
- Without this page, regulatory changes are applied without a formal process — creating compliance risk and unauditable state changes.
- KPMG cannot demonstrate to regulators that rule changes were reviewed, tested, and approved before production deployment.
- Multiple simultaneous country-law changes (common post-DPDP/EU AI Act amendments) cannot be tracked and managed.

**Recommendation:**

---

### New Page: 6.5.19 Regulatory Change Management — Super Admin Portal

**1. Page Objective**
Provide a structured, auditable six-step workflow for KPMG's compliance team to receive, assess, test, approve, and deploy regulatory rule changes across all applicable countries and tenants — satisfying RFP 23.16.

**2. Primary Actors**
Compliance Lead (KPMG), Legal Counsel, Platform Admin, Chief Compliance Officer (approval)

**3. Key Workflows**
Regulatory change identified → Change request created → Impact assessment → Rule modification in sandbox → Legal/compliance review → CCO approval → Staged deployment → Audit record created

**4. States**
Draft | Impact Assessment In Progress | Under Legal Review | Approved | Deployed to UAT | Deployed to Production | Rejected | Superseded

**5. Actions**
Create change request, assess impact, modify rules (sandbox), submit for review, approve/reject, deploy to UAT, deploy to production, rollback

**6. Data Blocks**
Change ID | Country affected | Regulation changed (name + article) | Effective date of law change | Current rule on platform | Proposed new rule | Impact assessment (check types affected, tenant count, candidate flow changes) | Legal review notes | Approval record | Deployment log

**7. UI Regions**
- Change Request Table (primary)
- Change Detail / Workflow View (per-change)
- Regulatory Calendar (upcoming known regulation changes)
- Deployment History

**8. Tables**

**Regulatory Change Register:**
| Change ID | Country | Regulation | Status | Effective Date | Impact | Owner | Due |
|---|---|---|---|---|---|---|---|
| RC-2025-004 | India | DPDP Amendment — Section 7(3) | Under Legal Review | 01-Apr-2025 | Medium | [Name] | 15-Mar |
| RC-2025-003 | UK | ICO — Biometric Data Guidance | Deployed (Prod) | 15-Jan-2025 | Low | [Name] | — |
| RC-2025-002 | EU | EU AI Act — Art. 13 BGV prohibition | Draft | 01-Aug-2025 | Critical | [Name] | 01-Jul |

**9. Change Detail Workflow View:**

```
REGULATORY CHANGE — RC-2025-004
══════════════════════════════════════════════════════

STEP 1: CHANGE IDENTIFICATION ✅ COMPLETE
Country: India
Regulation: DPDP Act Amendment — Section 7(3) revised consent period
Change: Consent validity period extended from 12 to 24 months
Identified by: Compliance Lead [Name]   Date: 10-Jan-2025
Source: DPBI Circular 2025/01

──────────────────────────────────────────────────────
STEP 2: IMPACT ASSESSMENT ✅ COMPLETE
Affected check types: All (consent is platform-wide)
Affected tenants: All India-scoped tenants (14 tenants)
Candidate flow changes: Consent page update; renewal trigger date update
System rule change: consent_validity_days: 365 → 730
Estimated change effort: Low (config change only)
Completed by: [Name]   Date: 12-Jan-2025

──────────────────────────────────────────────────────
STEP 3: RULE MODIFICATION (SANDBOX) 🔄 IN PROGRESS
Modified in: Sandbox environment
Rule engine change: consent_validity_days: 365 → 730
Test cases run: 12/20
Test result: PASSING (12/12 so far)
Modified by: [Name]   Target: 20-Jan-2025

──────────────────────────────────────────────────────
STEP 4: LEGAL REVIEW ⏳ PENDING
Assigned to: [Legal Counsel]
Due: 25-Jan-2025

──────────────────────────────────────────────────────
STEP 5: CCO APPROVAL ⏳ PENDING

──────────────────────────────────────────────────────
STEP 6: DEPLOYMENT ⏳ PENDING
Target: UAT → Production (01-Feb-2025)
══════════════════════════════════════════════════════
```

**10. Drawers**
- Change Detail Drawer: Full 6-step workflow view per change (as above)
- Impact Assessment Drawer: Full tenant list, check-type breakdown, estimated candidate flow changes, test plan
- Rule Preview Drawer: Side-by-side comparison — current rule (production) vs proposed rule (sandbox)
- Deployment Drawer: Choose target environment (UAT / Production) → staged rollout % → confirm → rollback option

**11. Modals**
- Create Change Request Modal: Country selector | Regulation field | Summary | Effective date | Owner assignment
- Approve Modal: "You are approving regulatory change RC-XXXX for deployment. This will modify platform rules affecting [N] tenants and [N] active cases. [Confirm Approval]"
- Rollback Modal: "Rollback RC-XXXX to previous rule state? All affected tenants will immediately revert. Rollback reason: [mandatory field] [Confirm Rollback]"

**12. Regulatory Calendar Panel:**
```
UPCOMING REGULATORY CHANGES (KNOWN)
─────────────────────────────────────────────────
● 01-Apr-2025 | India | DPDP Amendment — Section 7(3)     [RC-2025-004]
● 01-Aug-2025 | EU    | EU AI Act Art. 13 BGV provision    [RC-2025-002]
● TBD          | UK    | ICO Biometric Refresh (expected)   [Not yet created]
─────────────────────────────────────────────────
[+ Create Change Request for upcoming regulation]
```

**13. Audit Events:**
| Event | Data Logged |
|---|---|
| Change request created | Creator, timestamp, regulation reference |
| Impact assessment completed | Assessor, findings, affected tenants list |
| Rule modified (sandbox) | Modified by, before/after values, test results |
| Legal review completed | Reviewer, outcome, notes |
| CCO approval | Approver identity, approval timestamp, approval notes |
| Deployment (UAT/Prod) | Deployer, timestamp, environment, version |
| Rollback (if any) | Initiator, reason, rollback timestamp |

**14. Part 5 IA Addition:**
Add to Super Admin Portal IA (Part 5.5) under new section — Compliance Governance:
```
├── 9. Compliance Governance
│   ├── 9.1 Regulatory Change Management
│   │   └── Page: Regulatory Change Management
│   │       Purpose: Structured 6-step process to update platform rules on law changes
│   │       RFP: 23.16 | Module: 12.3 | Classification: Compliance-Critical
│   └── [future: DPIA Repository, Cross-border Transfer Register]
│
└── 10. DATA GOVERNANCE  [NEW — C-05 | RFP 17.1–17.7]
    ├── 10.1 Platform Data Catalog
    │   └── Page: Data Element Inventory
    │       Purpose: Registry of every type of personal data collected across all portals —
    │                field name, source, purpose, retention period, pseudonymization rule.
    │                Satisfies DPDP/GDPR Record of Processing Activities (ROPA) — RFP 17.1
    │       RFP: 17.1 | Actor: Platform Admin, Privacy Officer
    │
    ├── 10.2 Candidate Identity Master
    │   └── Page: Candidate Master Record Management
    │       Purpose: Cross-case candidate identity consolidation — one master record
    │                per real-world person, linked to all cases they appear in.
    │                Merge/split controls for deduplication. DSAR lookup anchor.
    │       RFP: 17.5 | Actor: Platform Admin, Compliance Officer
    │
    ├── 10.3 Field Lineage & Evidence Linking
    │   └── Page: Data Provenance Viewer
    │       Purpose: For any field in any case — show the full source chain from
    │                candidate entry through verification sources to stored value.
    │                Link verification outcomes to the specific evidence that justified them.
    │       RFP: 17.2, 17.3 | Actor: Compliance Officer, Ops Admin (for disputes)
    │
    └── 10.4 Data Quality & Masking Rules
        └── Page: Data Quality & Pseudonymization Configuration
            Purpose: Configure field-level validation rules (data quality), pseudonymization
                     masking matrix (which fields masked per role), and anonymization
                     schedule (what is preserved after retention purge).
            RFP: 17.4, 17.6, 17.7 | Actor: Platform Admin, Privacy Officer




---

## C-05 FIX: Data Governance Pages — Super Admin Portal

> **RFP 17.1–17.7 | All 7 items in RFP Section 17 ("Data") were absent from the architecture.**
> Four new pages added: 6.5.20 Data Catalog, 6.5.21 Candidate Identity Master,
> 6.5.22 Field Lineage & Evidence Linking, 6.5.23 Data Quality & Masking Rules.

---

### 6.5.20 Page: Platform Data Catalog

**1. Page Objective**
Maintain a complete inventory of every personal data element type collected — the platform's ROPA (Record of Processing Activities) under GDPR Article 30 / DPDP. Enables KPMG to show regulators what data is held, why, where it came from, and how long it is kept. RFP 17.1.

**2. Primary Actors** Platform Admin, Privacy Officer, DPO

**3. Key Workflows**
Review all data elements → Filter by sensitivity / portal / retention → Export ROPA → Add new element when new field added to platform → Update retention or masking rules → Version and publish

**4. States**
Per element: Active | Deprecated (no longer collected — historical data remains under retention) | Proposed (under review, not yet in production)

**5. Actions**
View, filter, search, export ROPA PDF/Word, add element, edit element, deprecate element, view version history

**6. Data Blocks**
Per element: field ID | display name | portal(s) | collection method (Candidate form / OCR / API pull / Ops manual / HRMS push) | purpose | legal basis | data category (Standard / Special / Biometric / Financial) | retention period (by country) | pseudonymization rule | anonymization rule | source system | status

**7. UI Regions**
- Filter bar: Portal / Sensitivity / Legal basis / Status
- Main table: All data elements (sortable, paginated)
- Detail panel (right on row click): Full element spec + version history
- Action bar: [Add Element] [Export ROPA] [Export CSV]

**8. Tables**

Data Element Registry:

| Field ID | Element Name | Category | Portal(s) | Legal Basis | Retention | Pseudonymization | Status |
|---|---|---|---|---|---|---|---|
| candidate.identity.aadhaar | Aadhaar Number | Special — Gov ID | Candidate, Ops | Consent | 7 years | Masked last 4 | Active |
| candidate.identity.pan | PAN Number | Standard Personal | Candidate, Ops | Consent | 7 years | Masked last 4 | Active |
| candidate.biometric.selfie_hash | Biometric Face Hash | Special — Biometric | Candidate | Explicit Consent | Deleted post-match | Hash only | Active |
| candidate.employment[n].start_date | Employment Start Date | Standard Personal | Candidate, Ops, Vendor | Consent | 7 years | None | Active |
| ops.adjudication.notes | Adjudication Notes | Standard Professional | Ops only | Legitimate interest | 7 years | None | Active |

**9. Drawers**
- Element Detail Drawer: Full spec + edit form + version history
- ROPA Preview Drawer: Rendered ROPA document formatted for DPA submission
- Country Retention Override Drawer: Per-element per-country retention overrides

**10. Modals**
- Add Element Modal: Full spec form — Privacy Officer acknowledgement required for Special Category elements
- Deprecate Element Modal: "Existing data in [N] cases retained per policy. Confirm?"
- Export ROPA Modal: Format (PDF/Word), language, last-updated date field

**11. Alerts/Banners**
- "New data element detected in platform code but not in Data Catalog — registration required" (red, blocks deployment)
- "ROPA not exported in [N] days — DPA submission may be overdue" (amber)
- "[N] elements approaching retention expiry in 30 days" (amber)

**12. Compliance Context**
The Data Catalog IS the platform ROPA. Must be updated whenever any new form field, API field, or data collection point is added to any portal. Privacy Officer sign-off enforced for Special Category and Biometric elements.

**13. Audit** Every element change logged immutably: actor, timestamp, before/after values. Exportable for regulatory inspection.

**14. Mobile** Desktop only.

---

### 6.5.21 Page: Candidate Identity Master

**1. Page Objective**
Maintain one canonical identity record per real-world candidate — linking all BGV cases they have appeared in across all clients and time periods. Enables DSAR response, cross-case fraud detection, name-variation tracking, and merge/split deduplication. RFP 17.5.

**2. Primary Actors** Platform Admin, Compliance Officer (DSAR), Fraud Investigator

**3. Key Workflows**
Search by identity anchor → View master record → See all linked cases → Initiate merge (two records = same person) → Initiate split (one record wrongly combined) → Export DSAR pack

**4. States**
Active | Merged-into (redirect exists) | Split-pending | DSAR-in-progress

**5. Actions**
Search, view, merge, split, export DSAR pack, flag for fraud investigation

**6. Data Blocks**
Per master record: Master ID (not PII) | identity anchors (PAN hash, Aadhaar hash, email hash, mobile hash — hashed only, not raw) | canonical name | case count by client and outcome | first/last seen | linked case IDs | merge history | DSAR log | fraud flag

**7. UI Regions**
- Search bar: name / email / PAN last 4 / Aadhaar last 4 / Master ID
- Results list: Matched master records with case count
- Master Record Detail (right panel): full record + linked cases + actions

**8. Tables**

Linked Cases Table:
| Case ID | Client | Package | Date | Outcome | Initiation Mode |
|---|---|---|---|---|---|
| KCHK-2024-04411 | Client A | Standard | Mar 2024 | Clear | Candidate Portal |
| KCHK-2026-09841 | Client B | Executive | May 2026 | Amber | Ops Manual |

Name Variation Table:
| Case | Name Used | Source | Match to Canonical |
|---|---|---|---|
| KCHK-2024-04411 | Priya Sharma | Candidate-entered | Exact |
| KCHK-2026-09841 | P. Sharma | Ops-entered | Fuzzy match 85% |

**9. Drawers**
- Merge Drawer: Search target record → preview combined cases + anchors → [Confirm Merge] (reversible 30 days)
- Split Drawer: Select cases for other person → new master created → [Confirm Split]
- DSAR Export Drawer: Complete PII export across all linked cases — formatted for regulatory delivery

**10. Modals**
- Merge Confirmation: "[N] cases re-linked. Reversible within 30 days. [Confirm]"
- Split Confirmation: "[N] cases split into new master. [Confirm]"
- Fraud Flag: Structured reason + free text + investigator assignment

**11. Alerts/Banners**
- "Possible duplicate: [Master A] and [Master B] share PAN hash — review for merge" (amber)
- "DSAR deadline in [N] days — export required by [date]" (red)
- "Merge reversal window closes in [M] days" (blue)

**12. Audit** Every merge, split, DSAR export, fraud flag logged immutably.

**13. Mobile** Desktop only.

---

### 6.5.22 Page: Field Lineage & Evidence Linking

**1. Page Objective**
For any data field in any case — display its complete provenance chain from original entry through every verification source to the final stored value. Link verification outcomes to the specific evidence that justified them. Makes dispute resolution and regulatory audit defensible. RFP 17.2, 17.3.

**2. Primary Actors** Compliance Officer, Ops Admin, Auditor (read-only), Legal

**3. Key Workflows**
Select case → Select field → View lineage chain → View outcome → See linked evidence → Export lineage pack

**4. States**
Per field: Single-source | Consistent (all sources agree) | Discrepant (sources disagree — adjudicator resolved) | Unresolved

**5. Actions**
Search case, select field, view lineage, view linked evidence, export lineage pack (per field or full case)

**6. Data Blocks**
Field lineage per source: source type | source system | value recorded | timestamp | match status vs other sources | adjudicator resolution (if discrepant)

Evidence linking per outcome: outcome type | declared by | declared at | linked evidence IDs | linked AI signal IDs | adjudicator notes

**7. UI Regions**
- Left: Case selector + field navigator (tree: Case → Check Type → Field)
- Center: Lineage chain for selected field
- Right: Evidence panel — documents + AI signals linked to selected check outcome

**8. Tables**

Field Lineage (sample — Date of Birth):

| Seq | Source Type | System | Value | Timestamp | Status |
|---|---|---|---|---|---|
| 1 | Candidate-entered | KCheck Portal | "14-Jan-1992" | 05-May 09:41 | First source |
| 2 | OCR-extracted | Aadhaar scan | "14/01/1992" | 05-May 09:42 | Match |
| 3 | API pull | UIDAI | "1992-01-14" | 05-May 09:43 | Match |
| 4 | Employer-confirmed | ABC Corp | "14-01-1992" | 08-May 14:20 | Match |
| Final | Stored | KCheck DB | "1992-01-14" | 08-May 14:21 | Consistent — 4 sources |

Evidence Linking (per outcome):

| Evidence ID | Document | Format | Source | AI Flags |
|---|---|---|---|---|
| EVD-2026-0441 | Experience_Letter.pdf | PDF | Candidate upload | None |
| EVD-2026-0442 | EPFO_Statement.pdf | PDF | EPFO API | None |
| EVD-2026-0443 | Employer_Response.docx | DOCX | Employer portal | None |

**9. Drawers**
- Full Case Lineage Drawer: All fields across all checks in one scrollable view
- Evidence Review Drawer: Opens actual document (same viewer as 6.1.39 Evidence Review Drawer)
- Discrepancy Detail Drawer: Adjudicator reasoning, date, supporting notes

**10. Modals**
- Export Lineage Pack: Scope (field / check / case) + format (PDF / JSON) → tamper-evident report with hash manifest

**11. Alerts/Banners**
- "Outcome declared without linked evidence — compliance gap" (red — triggers ops admin review queue)
- "Discrepant sources — adjudication outcome available" (amber)

**12. Audit** Page access logged: viewer, case, timestamp. Lineage data is read-only from this view.

**13. Mobile** Desktop only.

---

### 6.5.23 Page: Data Quality & Masking Rules

**1. Page Objective**
Configure three interconnected rule sets in one page: (1) data quality validation rules per field, (2) pseudonymization masking matrix defining field visibility per role per portal, (3) anonymization schedule defining what is preserved vs deleted after retention expiry. Satisfies RFP 17.4, 17.6, 17.7.

**2. Primary Actors** Platform Admin, Privacy Officer

**3. Key Workflows**
Configure quality rules → Test → Publish | Configure masking matrix → Preview per role → Publish | Configure anonymization schedule → Preview anonymized record → Publish

**4. States**
Per rule set: Draft | Published | Testing (sandbox) | Superseded

**5. Actions**
Add/edit/delete rules, test rule against sample data, publish, rollback to previous version, preview masked view per role, preview anonymized record

**6. Data Blocks**

Tab 1 — Data Quality Rules (RFP 17.4):
Per rule: field ID | rule type (Required / Format / Range / Plausibility / Cross-field consistency) | rule expression (e.g., `employment.end_date > employment.start_date`) | applies to (portal, check type, country, client) | error message | severity (Blocking / Warning) | status

Tab 2 — Pseudonymization Masking Matrix (RFP 17.7):

| Field | Ops Reviewer | Senior Reviewer | Adjudicator | Client Viewer | Client Admin |
|---|---|---|---|---|---|
| Aadhaar Number | Last 4 only | Full | Full | Not shown | Not shown |
| PAN Number | Last 4 only | Full | Full | Not shown | Not shown |
| Mobile Number | Last 4 only | Full | Full | Hashed | Last 4 only |
| Adjudication Notes | Full | Full | Full | Not shown | Not shown |
| Bank account | Not shown | Full | Full | Not shown | Not shown |

Values: Full / Last 4 only / Hashed (SHA-256, not reversible) / Tokenized (reversible) / Not shown

Tab 3 — Anonymization Schedule (RFP 17.6):

| Field Category | After Retention Expires | Preserved As |
|---|---|---|
| Direct identifiers (name, DOB, Aadhaar, PAN, email, mobile) | Deleted permanently | Nothing |
| Employment (company name, designation) | Anonymized | Check type + outcome + TAT duration only |
| Education (institution, degree name) | Anonymized | Degree level only (Graduate / Postgraduate) |
| Adjudication outcome | Kept | Outcome color only — notes deleted |
| TAT and SLA data | Kept | Full — no PII |
| Audit log skeleton | Kept | Event type + timestamp — actor identity deleted |

**7. UI Regions**
- Tab bar: [Data Quality Rules] [Masking Matrix] [Anonymization Schedule]
- Per tab: Configuration table + [Preview] [Test] [Publish] action bar

**8. Cards**
- Coverage Card (Masking tab): "All [N] sensitive fields covered" / "[M] fields without masking rule — review required" (red if gaps)
- Anonymization Preview Card: Sample case record before and after anonymization

**9. Drawers**
- Rule Edit Drawer (Quality): Expression builder + scope selector + error message + severity
- Rule Test Drawer (Quality): Enter sample values → pass/fail result with explanation
- Masking Preview Drawer: Select role + portal → see full sample case with masking applied
- Anonymization Preview Drawer: Select sample case → exact record state after anonymization

**10. Modals**
- Publish Modal: "[N] rules changed. Affects all portals and exports immediately. Privacy Officer sign-off required. [Confirm]"
- Rollback Modal: "Roll back to version [N]? [Confirm]"

**11. Alerts/Banners**
- "[N] sensitive fields in Data Catalog have no masking rule — coverage gap" (red, blocks publish)
- "Anonymization schedule does not cover [N] data elements — DPDP/GDPR risk" (red)
- "Rule [X] conflicts with rule [Y] — one will override. Review." (amber)

**12. Compliance Context**
Masking Matrix → RFP 17.7 + RFP 14.11 (field masking by role). Anonymization Schedule → RFP 17.6 + RFP 15.5 (retention + auto-purge). Quality Rules → RFP 17.4 + RFP 11.3 (form validation). Privacy Officer approval enforced in publish modal.

**13. Audit** All rule changes logged immutably. Masking matrix version history queryable by date — can show what masking was applied on any historical date.

**14. Mobile** Desktop only.

---


## 6.6 FIELD AGENT MOBILE APP — Page Design Depth (Complete)

*(6.6.1 Evidence Capture — already written in full 20-point depth in expanded_p6_complete.md)*

---

### 6.6.2 Page: Agent Login

**1. Page Objective**
Authenticate field agent securely before allowing access to assignment data — with offline tolerance for areas with poor connectivity.

**2. Primary Actors**
Field Agent

**3. Key Workflows**
Enter credentials → OTP or biometric → Session created → Offline mode initialized if no connectivity

**4. States**
Online authentication | Offline mode (last-authenticated session) | Session expired | Account locked

**5. Actions**
Enter username + OTP, use biometric (fingerprint/face ID), request OTP resend, contact support

**6. UI Components**
- Username field
- OTP entry (6 digits, auto-advance)
- Biometric login button (if device supports — preferred on mobile for speed)
- "Work offline" button: Uses last valid session token (valid for configured period — e.g., 8 hours) for field agents in no-signal areas
- Offline mode indicator: "Offline mode — assignments loaded from last sync [timestamp]"
- App version display (for support calls)

**7. Alerts/Banners**
- "You are offline. Working with assignments from last sync [time]. Submissions will queue until connected." — informational

**8. Security**
- JWT with device fingerprint binding (session only valid on same device)
- Offline session token: time-limited (8 hours), cannot be extended without online re-auth
- Failed login: 5 attempts → 30-minute lockout

**9. Mobile Considerations**
- Biometric: primary login method on supported devices (faster for field use)
- Large tap targets (agents may be wearing gloves)
- Works on all screen sizes (minimum tested: 360px)
- Low-bandwidth optimized: login endpoint call < 2KB

---

### 6.6.3 Page: Today's Assignment List

**1. Page Objective**
Show field agent all assignments scheduled for today — prioritized by SLA urgency, with navigation to each address.

**2. Primary Actors**
Field Agent

**3. Key Workflows**
Open app → View today's assignments → Sort by proximity or SLA urgency → Navigate to address → Begin evidence capture

**4. States**
All Pending | Mix of Pending + In Progress + Completed | All Completed (end of day)

**5. Actions**
Sort assignments (by SLA / by proximity), navigate to address, begin evidence capture, view assignment details, sync pending submissions

**6. Data Blocks**
Per assignment: case reference (anonymized — no candidate full name on mobile for privacy), check type, address, SLA deadline, status, assignment notes from KPMG

**7. UI Regions**
- Top: Date display + total count (e.g., "Today — 8 assignments")
- Sort bar: By SLA urgency | By proximity (uses GPS)
- Assignment cards list (scrollable)
- Offline sync status bar (bottom if pending submissions)

**8. Cards (per assignment)**
- Assignment Card: Reference number (anonymized) | Address | Check type | SLA deadline + countdown | Status badge | [Navigate] [Begin] buttons
- SLA color indicator: Green / Amber / Red on card left border

**9. Map View Toggle**
- Toggle: List view / Map view
- Map view: All assignments pinned on map, color-coded by SLA health. Tap pin → card view for that assignment.

**10. Drawers**
- Assignment Detail Drawer: Full details — address, any special instructions from KPMG, previously submitted evidence (if re-visit), contact notes
- Offline Queue Drawer: List of submissions waiting to sync + sync progress when connected

**11. Alerts/Banners**
- "[N] pending submissions will sync when you connect to internet" — bottom bar, persistent
- "SLA deadline in 2 hours for [Ref X]" — push notification on lock screen + in-app banner

**12. Mobile Considerations**
- Optimized for outdoor use (high contrast, large text)
- [Navigate] opens native maps (Google Maps / Apple Maps) with address pre-filled
- Proximity sort uses GPS — requires location permission (explained on first use)
- Works fully offline — shows assignments cached from last sync

---

### 6.6.4 Page: Offline Submission Queue

**1. Page Objective**
Show all evidence submissions that were captured offline and are waiting to be synced to the server — with sync status and conflict alerts.

**2. Primary Actors**
Field Agent

**3. Key Workflows**
Review pending submissions → Connect to internet → Auto-sync triggers → Confirm all synced → Investigate any sync failures

**4. States**
Pending (waiting for connectivity) | Syncing (in progress) | Synced (complete) | Sync Failed (conflict or validation error)

**5. UI Regions**
- Connection status indicator (top): Online (green) / Offline (grey) / Syncing (animated)
- Pending queue list
- Synced confirmation list (today)
- Sync failed section (requires attention)

**6. Cards (per queued submission)**
- Pending Card: Reference | Evidence summary (e.g., "3 photos, checklist complete") | Size | [Sync Now] button (if online)
- Synced Card: Reference | Sync time | Confirmation number
- Failed Card: Reference | Failure reason | [Retry] [View Error Detail] buttons — red

**7. Modals**
- Sync Conflict Modal: "Case [Ref] was reassigned while you were offline. Your evidence will still be submitted, but review by KPMG is required." [Proceed]
- Sync Failure Detail Modal: Technical error reason + [Contact Support] button

**8. Alerts/Banners**
- "You are back online — syncing [N] submissions..." — animated progress
- "All submissions synced successfully" — green confirmation
- "[N] submissions failed to sync — action required" — red

**9. SLA Components**
If a queued submission is for a case approaching SLA — urgency indicator on that card ("Sync this first — SLA in [N] hours")

---

### 6.6.5 Page: Agent Performance Dashboard

**1. Page Objective**
Give field agents visibility into their own performance metrics — completed cases, SLA compliance, QC feedback — for self-improvement and accountability.

**2. Primary Actors**
Field Agent

**3. Key Workflows**
Review today's completions → Check monthly SLA compliance → Review QC feedback (if any)

**4. States**
Today view | Monthly view

**5. UI Components (mobile-optimized cards)**
- Cases Completed Card: Today / This week / This month
- SLA Compliance Card: % of cases submitted within SLA (this month) — vs target
- Pending Sync Card: Count of offline submissions waiting (link to sync queue)
- QC Feedback Card: "KPMG reviewed [N] of your submissions this month. [N] passed, [N] had feedback." [View Feedback →]

**6. Drawers**
- QC Feedback Drawer: Per-case feedback — what was noted, how to improve (e.g., "Photo 2 had insufficient GPS accuracy — move to open area before capturing")
- Contact KPMG Ops Drawer: Phone + WhatsApp contact for field agent support

**7. Alerts/Banners**
- "Your SLA compliance dropped this month — [N] cases submitted after deadline"
- "QC feedback available for [N] recent submissions"

**8. Mobile Considerations**
This is a 100% mobile page. Card layout, large text, no tables. Minimal scroll. Simple, glanceable metrics.

---

# PART 8 — CRITICAL ARCHITECTURAL RISKS (EXPANDED WITH RISK SCORING & MITIGATION OWNERSHIP)

## 8.1 Risk Scoring Methodology

Each risk is scored on:
- **Likelihood (L):** 1 (Very Low) → 5 (Very High) — Probability of occurrence given current architecture
- **Impact (I):** 1 (Negligible) → 5 (Catastrophic) — Consequence if risk materializes
- **Risk Score (R) = L × I:** 1–25
- **Risk Level:** 1–6 Low | 7–12 Medium | 13–19 High | 20–25 Critical

---

## 8.2 Complete Risk Register

### RISK-01: Candidate Portal Not Independently Deployed
| Attribute                          | Detail                                                                                                                                                                                                                                     |
| ---------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Category**                       | Security / Underengineering                                                                                                                                                                                                                |
| **Description**                    | If Candidate Portal shares a runtime or deployment unit with Operations Portal, a vulnerability in the public-facing layer (XSS, CSRF, injection attacks, rate limit bypass) directly exposes the internal verification operations surface |
| **Likelihood**                     | 4 (High — common mistake in early SaaS builds)                                                                                                                                                                                             |
| **Impact**                         | 5 (Catastrophic — ops data exposed to public internet)                                                                                                                                                                                     |
| **Risk Score**                     | 20 — CRITICAL                                                                                                                                                                                                                              |
| **Trigger Conditions**             | Single codebase deployment, shared API gateway without BFF isolation, shared session store                                                                                                                                                 |
| **What Breaks**                    | Entire ops security perimeter; GDPR data breach notification required; candidate data exposed                                                                                                                                              |
| **Mitigation**                     | Independent deployment unit (separate container/app service). Separate CDN. WAF in front of Candidate Portal. Zero shared runtime with Ops. BFF layer enforces zero ops-internal API access from candidate session tokens                  |
| **Mitigation Owner**               | Platform Architect + DevOps Lead                                                                                                                                                                                                           |
| **Verification Gate**              | Penetration test (external) specifically targeting candidate→ops boundary before go-live                                                                                                                                                   |
| **Residual Risk After Mitigation** | L:1 × I:5 = 5 (Low)                                                                                                                                                                                                                        |

---

### RISK-02: Multi-Tenant Data Isolation Failure
| Attribute | Detail |
|---|---|
| **Category** | Compliance / Architecture |
| **Description** | A misconfigured RBAC rule, a missing tenant_id filter on a query, or a BFF layer bug could expose Client A's cases to Client B's users |
| **Likelihood** | 3 (Medium — requires code defect) |
| **Impact** | 5 (Catastrophic — contractual breach, GDPR Article 5 violation, reputational destruction) |
| **Risk Score** | 15 — HIGH |
| **Trigger Conditions** | Missing tenant_id WHERE clause in a query; RBAC policy misconfiguration; API response not scoped to tenant context |
| **What Breaks** | Entire multi-tenancy trust model; every client's contractual data privacy obligation |
| **Mitigation** | Three-layer isolation: (1) DB-level: PostgreSQL Row Level Security with tenant_id policy on every table; (2) BFF-level: every API call validated against session token's tenant claim; (3) RBAC: third layer defense. Automated test suite: cross-tenant query probe tests run on every CI deployment. |
| **Mitigation Owner** | Backend Architect + QA Lead (automated test ownership) |
| **Verification Gate** | Cross-tenant penetration tests; automated CI test: "can tenant A's token retrieve tenant B's case?" must fail |
| **Residual Risk After Mitigation** | L:1 × I:5 = 5 (Low) |

---

### RISK-03: Consent Record Mutability
| Attribute | Detail |
|---|---|
| **Category** | Compliance / Legal |
| **Description** | If consent records are stored in the same mutable operational database, they can be altered (intentionally or by bug) — destroying the lawful basis for all verification processing done under that consent |
| **Likelihood** | 2 (Low — requires deliberate action or specific bug) |
| **Impact** | 5 (Catastrophic — all verification done under that consent is retroactively unlawful; regulatory fine; litigation) |
| **Risk Score** | 10 — MEDIUM (elevated to HIGH given DPDP/GDPR stakes) |
| **Trigger Conditions** | Consent record updated after creation (any UPDATE/DELETE on consent table); database migration script accidentally modifying consent records |
| **What Breaks** | Lawful basis for all processing; DPDP compliance; GDPR Article 7 compliance |
| **Mitigation** | Append-only consent table (DB trigger rejecting UPDATE/DELETE on consent records). Cryptographic hash per consent record (hash stored separately; computed on consent text + metadata at creation; re-verified on read). Consent receipts stored in immutable object storage (S3 Object Lock / Azure Blob Immutability). Consent DB user has INSERT-only permissions — no UPDATE or DELETE. |
| **Mitigation Owner** | Compliance Architect + DBA |
| **Verification Gate** | Quarterly consent log integrity verification (hash chain audit). DPDP/GDPR legal review of consent storage architecture. |
| **Residual Risk After Mitigation** | L:1 × I:5 = 5 (Low) |

---

### RISK-04: AI Fraud Threshold Reverse Engineering
| Attribute | Detail |
|---|---|
| **Category** | Security / AI |
| **Description** | If AI confidence scores are exposed as raw percentages in API responses, sophisticated candidates or organized fraud rings can probe the system to identify exact thresholds and coach applicants to just-barely pass |
| **Likelihood** | 3 (Medium — organized document fraud exists; API probing is feasible) |
| **Impact** | 4 (Severe — fraud detection rendered ineffective; KPMG's core value proposition compromised) |
| **Risk Score** | 12 — MEDIUM |
| **Trigger Conditions** | Raw confidence scores (e.g., "92.3%") returned in API response visible to candidate/vendor portal; threshold values hardcoded in frontend code |
| **What Breaks** | AI fraud detection; verification integrity; KPMG's quality reputation |
| **Mitigation** | Confidence scores exposed as categorical buckets only (Low/Medium/High/Critical — never raw %). Threshold values stored in Super Admin only — never in frontend environment variables. AI signal API endpoints restricted to Ops BFF only (candidate and vendor BFFs have no access). Regular threshold rotation (change thresholds periodically even if models don't change). |
| **Mitigation Owner** | AI/ML Lead + Security Architect |
| **Verification Gate** | API security review: verify no raw threshold data in candidate-facing API responses |
| **Residual Risk After Mitigation** | L:1 × I:4 = 4 (Low) |

---

### RISK-05: Field Agent GPS Spoofing
| Attribute | Detail |
|---|---|
| **Category** | Operational / Fraud |
| **Description** | Field agents submitting fake GPS coordinates (via GPS spoofing apps) and/or pre-captured photos for address verifications without physically visiting the address |
| **Likelihood** | 3 (Medium — GPS spoofing apps are widely available; agent fraud has precedent in field-verification industry) |
| **Impact** | 4 (Severe — false address verification delivered to client; KPMG liability; criminal hired based on false verification) |
| **Risk Score** | 12 — MEDIUM |
| **Trigger Conditions** | Agent uses GPS mock location app; agent submits archived photos; agent submits photos from different location |
| **What Breaks** | Physical address verification integrity; KPMG liability for false verification |
| **Mitigation** | Device attestation (Android: Google Play Integrity API; iOS: DeviceCheck) — rejects submissions from rooted/modified devices. GPS teleportation detection server-side (agent cannot move 50km in 5 minutes). Photo EXIF metadata validation server-side (GPS coordinates embedded in photo must match declared capture location within 200m). Photo timestamp cross-check with GPS timestamp. Anti-screenshot measure: camera-only capture (no gallery upload). Periodic audit: QC sample of field verifications (cross-check visit record with agent's device trail). |
| **Mitigation Owner** | Mobile App Architect + Operations QC Lead |
| **Verification Gate** | Penetration test: GPS spoofing attempt on Field Agent App. QC sampling rate review quarterly. |
| **Residual Risk After Mitigation** | L:2 × I:4 = 8 (Medium — cannot be fully eliminated; residual risk through QC) |

---

### RISK-06: Notification Delivery Failure Silently Killing SLA
| Attribute | Detail |
|---|---|
| **Category** | Operational / SLA |
| **Description** | If WhatsApp/SMS fails silently without fallback, candidates never receive invitations. Cases stall. SLA clock runs. Breach accumulates. Operations not notified. |
| **Likelihood** | 4 (High — WhatsApp delivery failure is common, especially international numbers) |
| **Impact** | 3 (Significant — SLA breach, candidate blaming KPMG, poor client experience) |
| **Risk Score** | 12 — MEDIUM |
| **Trigger Conditions** | WhatsApp not registered on candidate's number; SMS delivery failure (carrier issue); email in spam; no fallback chain configured |
| **What Breaks** | Candidate invitation delivery; case initiation; overall SLA; client confidence in KPMG |
| **Mitigation** | Multi-channel retry chain: WhatsApp (T+0) → SMS (T+5min if no delivery receipt) → Email (T+15min if no delivery receipt). Delivery receipt tracking (all channels). Ops dashboard notification failure counter (real-time alert if failure rate exceeds threshold). SLA pause on Undeliverable status (automatic — documented in SLA agreement with clients). Escalation: if after 3 channels failed → ops manual outreach flag. |
| **Mitigation Owner** | Ops Architect + DevOps (channel provider SLA monitoring) |
| **Verification Gate** | Monthly channel delivery success rate report. Alert threshold: > 2% failure rate triggers ops review. |
| **Residual Risk After Mitigation** | L:2 × I:3 = 6 (Low) |

---

### RISK-07: Audit Log Becoming Unqueryable at Scale
| Attribute | Detail |
|---|---|
| **Category** | Scalability / Compliance |
| **Description** | At 600–700 cases/day with 50+ events per case, the audit log grows at ~35,000 events/day (~12.8M/year). An unpartitioned, unarchived audit log becomes too slow to query within 3–6 months — impeding regulatory investigations and DSAR responses |
| **Likelihood** | 4 (High — inevitable if not designed for from the start) |
| **Impact** | 3 (Significant — cannot produce audit evidence on time; DSAR responses delayed; compliance risk) |
| **Risk Score** | 12 — MEDIUM |
| **Trigger Conditions** | Audit log in same DB as operational data; no partitioning; no archival strategy; full table scans on every audit query |
| **What Breaks** | DSAR response (legal deadline); regulatory audit response; QC investigation; KPMG internal audit |
| **Mitigation** | Dedicated audit database (not operational DB). Time-partitioned tables (partition by month). Index: case_id (hash) + actor_id + event_type + created_at. Archive to cold storage (object storage) after 12 months with query-on-demand. Retention aligned to client configuration (not one-size-fits-all). Audit query API with pre-defined access patterns (no arbitrary slow queries). |
| **Mitigation Owner** | DBA + Platform Architect |
| **Verification Gate** | Load test: audit log query for 100,000 case audit trail must return in < 2 seconds. |
| **Residual Risk After Mitigation** | L:1 × I:3 = 3 (Low) |

---

### RISK-08: AI Auto-Decisioning Without Human Oversight
| Attribute | Detail |
|---|---|
| **Category** | Compliance / AI Ethics |
| **Description** | If auto-decisioning thresholds are set too aggressively, cases are auto-declined without human review — violating FCRA-equivalent regulations and DPDP/GDPR Article 22 (right to human review of automated decisions) |
| **Likelihood** | 3 (Medium — business pressure to reduce manual review creates threshold-lowering pressure) |
| **Impact** | 4 (Severe — regulatory fine; candidate legal challenge; KPMG legal liability) |
| **Risk Score** | 12 — MEDIUM |
| **Trigger Conditions** | Auto-decisioning threshold set to include non-Clear outcomes; Super Admin lowers threshold without legal review; no human review gate for adverse outcomes |
| **What Breaks** | Legal compliance; candidate rights; KPMG's duty of care |
| **Mitigation** | Policy: Auto-approve restricted to zero-flag, high-confidence-clear cases only. All non-Clear outcomes require mandatory human adjudicator. All auto-decisions logged with model version + reason codes + confidence (RFP 2.13). Threshold change requires Risk/Legal sign-off (workflow in Super Admin). Candidate right to request human review surfaced in candidate portal and in adverse notice. |
| **Mitigation Owner** | Compliance Architect + AI/ML Lead + Legal |
| **Verification Gate** | Monthly auto-decision audit: what % of auto-decisions were non-Clear? Any = alert. |
| **Residual Risk After Mitigation** | L:1 × I:4 = 4 (Low) |

---

### RISK-09: Cross-Tenant Duplicate Identity Not Detected
| Attribute | Detail |
|---|---|
| **Category** | Fraud / Platform |
| **Description** | The same fraudulent candidate applies at two different KPMG clients. Per-tenant duplicate detection catches within-tenant duplicates. Cross-tenant detection is architecturally harder (tenant isolation prevents obvious cross-tenant queries) — creating a blind spot for organized fraud rings using the same fraudulent identity across multiple employers |
| **Likelihood** | 2 (Low — requires organized fraud; less common) |
| **Impact** | 4 (Severe — fraudulent hire cleared by KPMG; client liability; KPMG reputational damage) |
| **Risk Score** | 8 — MEDIUM |
| **Trigger Conditions** | Same PAN/Aadhaar hash seen in cases across different tenants within rolling window |
| **What Breaks** | Cross-client fraud detection; KPMG's fraud prevention value proposition |
| **Mitigation** | Pseudonymized cross-tenant identity index: Store irreversible hash of PAN + Aadhaar + email (not raw values) in a platform-level table. If hash match found across tenants: flag to ops for investigation (not automatically disclosed to either client — tenant isolation preserved). No raw PII in the cross-tenant index. |
| **Mitigation Owner** | Platform Architect + Privacy Architect |
| **Verification Gate** | Privacy review of cross-tenant hash approach. Test: same identity across two tenants must trigger flag. |
| **Residual Risk After Mitigation** | L:1 × I:4 = 4 (Low) |

---

### RISK-10: Premature Microfrontend Architecture
| Attribute | Detail |
|---|---|
| **Category** | Overengineering / Delivery |
| **Description** | Adopting full module federation (Webpack Module Federation / single-spa) before the team has experience with it adds build tooling complexity, runtime performance degradation from remote module loading, CSS isolation issues, and debugging complexity — delaying delivery with no proportional benefit at current scale |
| **Likelihood** | 3 (Medium — architects often over-index on scalability patterns) |
| **Impact** | 3 (Significant — 3–6 month delivery delay; performance regressions on Candidate Portal) |
| **Risk Score** | 9 — MEDIUM |
| **Trigger Conditions** | Architect mandates module federation for all 6 portals before team expertise established |
| **What Breaks** | Delivery timeline; Candidate Portal performance (critical for mobile); developer productivity |
| **Mitigation** | Start with monorepo multi-app (Nx or Turborepo): separate deployable apps sharing a component library. Each app is independently deployable without module federation complexity. Evolve to module federation only if: (a) team is experienced, (b) operational need (feature hot-patching) justifies it. |
| **Mitigation Owner** | Frontend Architect + Tech Lead |
| **Verification Gate** | Architecture decision record (ADR) with explicit criteria for when module federation will be reconsidered |
| **Residual Risk After Mitigation** | L:1 × I:3 = 3 (Low) |

---

### RISK-11: Workflow State Machine in Application Code (Not Persistent)
| Attribute | Detail |
|---|---|
| **Category** | Architecture / Reliability |
| **Description** | If case workflow state transitions are managed in application code (in-memory state machine) rather than persisted in DB with optimistic locking, a service restart during a state transition results in cases stuck in intermediate states — invisible to ops, not queryable, not SLA-trackable |
| **Likelihood** | 3 (Medium — common mistake in first iteration) |
| **Impact** | 4 (Severe — lost cases in production; SLA breach; compliance gap in audit trail) |
| **Risk Score** | 12 — MEDIUM |
| **Trigger Conditions** | State transition in application code not wrapped in DB transaction; no persisted state event log |
| **What Breaks** | Case reliability; SLA accuracy; audit trail completeness |
| **Mitigation** | Persistent state machine: every state transition is a DB write (case_status update + audit event insert) in a single transaction. Optimistic locking (version field on case record — prevents concurrent transitions). Orphaned state detector: background job checking for cases in transitional states > configured threshold → alert ops. State transition events published to audit event bus. |
| **Mitigation Owner** | Backend Architect |
| **Verification Gate** | Chaos test: kill service mid-state-transition; verify case recovers to correct state on restart |
| **Residual Risk After Mitigation** | L:1 × I:4 = 4 (Low) |

---

### RISK-12: Document Fraud Detection False Positive Rate
| Attribute | Detail |
|---|---|
| **Category** | AI / Operational |
| **Description** | AI document fraud detection flags legitimate documents as fraudulent at a rate that creates unacceptable ops burden or wrongful adverse outcomes for honest candidates |
| **Likelihood** | 3 (Medium — all AI models have false positives; document quality variation in India is high) |
| **Impact** | 3 (Significant — wrongful adverse outcomes; candidate and client complaints; ops overload) |
| **Risk Score** | 9 — MEDIUM |
| **Trigger Conditions** | Low-quality genuine documents (old certificates, regional document formats) triggering fraud flags; model not trained on diverse Indian document types |
| **What Breaks** | Verification accuracy; candidate experience; ops efficiency |
| **Mitigation** | Mandatory human review for all AI fraud flags (never auto-reject based on AI flag alone). Track false positive rate actively (ops reviews: "AI flagged fraud, human found legitimate" — logged). Monthly model feedback loop: false positives fed back to AI vendor for retraining. Confidence threshold calibrated conservatively for fraud detection (high precision over high recall). Document type-specific models (Aadhaar model vs degree certificate model vs payslip model). |
| **Mitigation Owner** | AI/ML Lead + QA Lead |
| **Verification Gate** | Monthly false positive rate report. Target: < 5% false positive rate. Alert if > 8%. |
| **Residual Risk After Mitigation** | L:2 × I:3 = 6 (Low) |

---

### RISK-13: Report Template Proliferation
| Attribute | Detail |
|---|---|
| **Category** | Operational / Maintainability |
| **Description** | Every client requesting unique report layouts, sections, and branding creates an unbounded library of one-off templates that becomes unmaintainable — any structural change to the report (new check type, new field) requires touching every template |
| **Likelihood** | 4 (High — enterprise clients almost always want customization) |
| **Impact** | 2 (Moderate — ops and dev maintenance overhead; delayed report changes) |
| **Risk Score** | 8 — MEDIUM |
| **Trigger Conditions** | Report templates built as static HTML/PDF templates per client; no shared component model |
| **What Breaks** | Template maintainability; time-to-add new check type (must update all templates) |
| **Mitigation** | Template engine with configurable components: core report structure is shared; per-client configuration = which sections to include/exclude, branding (logo, color), custom terminology. Hard limit: max 1 custom section per client beyond standard template set. Section versioning: when new check type added, new section auto-added to all templates (clients can opt-out). |
| **Mitigation Owner** | Product Manager + Backend Engineer (template engine owner) |
| **Verification Gate** | Adding a new check type should require zero changes to existing templates |
| **Residual Risk After Mitigation** | L:2 × I:2 = 4 (Low) |

---

### RISK-14: Data Residency Violation Under Multi-Country Operation
| Attribute | Detail |
|---|---|
| **Category** | Compliance / Multi-country |
| **Description** | For EU clients with European candidate data, data must be processed and stored within the EU. For India-only clients, DPDP data localization requirements apply. If cloud infrastructure routing sends data to wrong region (auto-failover to non-compliant region, CDN caching in wrong region), GDPR/DPDP violation occurs |
| **Likelihood** | 3 (Medium — cloud auto-scaling and CDN can cause unintended data movement) |
| **Impact** | 4 (Severe — GDPR fine up to €20M/4% global revenue; DPDP penalties) |
| **Risk Score** | 12 — MEDIUM |
| **Trigger Conditions** | Cloud auto-failover to non-compliant region; CDN caching candidate data in wrong region; multi-region DB replication without residency controls |
| **What Breaks** | GDPR compliance; DPDP compliance; client contractual obligations |
| **Mitigation** | Per-tenant data residency tagging: every data object tagged with residency constraint. Cloud infrastructure: tenant-specific storage accounts in mandated region. CDN: Candidate Portal static assets served globally; candidate data never cached at CDN (API responses marked no-cache for personal data). DB replication: cross-region replication disabled for GDPR-scoped tenants. Super Admin: data residency monitor alerts on any detected cross-region data movement. |
| **Mitigation Owner** | Cloud Architect + Privacy Architect |
| **Verification Gate** | Data residency audit quarterly. Cloud config review: verify no replication to non-compliant regions for EU tenants. |
| **Residual Risk After Mitigation** | L:1 × I:4 = 4 (Low) |

---

### RISK-15: SLA Penalty Calculation Errors
| Attribute | Detail |
|---|---|
| **Category** | Operational / Financial |
| **Description** | Incorrect SLA pause/resume logic (holiday lists not applied, notification failure pause not triggered, or incorrectly resumed) results in wrong SLA calculations — either incorrectly billing SLA penalties to KPMG or failing to catch actual breaches |
| **Likelihood** | 3 (Medium — SLA calculation with pauses, holidays, and multi-country is complex) |
| **Impact** | 3 (Significant — financial impact, client disputes, audit findings) |
| **Risk Score** | 9 — MEDIUM |
| **Trigger Conditions** | Holiday list not updated; pause trigger not firing on notification failure; SLA resumed incorrectly; timezone handling errors for multi-country |
| **What Breaks** | SLA accuracy; billing accuracy; client trust |
| **Mitigation** | SLA calculation engine as standalone tested module (unit tests for every edge case: holiday + pause + multi-timezone). SLA calculation is deterministic and reproducible from event log (can re-run calculation from audit events). Holiday list validation: alert if holiday list not updated for upcoming month. SLA pause/resume: explicit events in audit log (not implicit state). Timezone: always store in UTC; display in client's configured timezone. |
| **Mitigation Owner** | Backend Architect + QA Lead |
| **Verification Gate** | SLA calculation test suite: 50+ test cases covering holiday edge cases, pause scenarios, timezone conversions |
| **Residual Risk After Mitigation** | L:1 × I:3 = 3 (Low) |

---

## 8.3 Risk Summary Dashboard

| Risk ID | Description | L | I | Score | Level | Mitigation Owner | Post-Mitigation Score |
|---|---|---|---|---|---|---|---|
| RISK-01 | Candidate Portal not independently deployed | 4 | 5 | 20 | CRITICAL | Platform Architect + DevOps | 5 |
| RISK-02 | Multi-tenant data isolation failure | 3 | 5 | 15 | HIGH | Backend Architect + QA | 5 |
| RISK-03 | Consent record mutability | 2 | 5 | 10 | HIGH | Compliance Arch + DBA | 5 |
| RISK-04 | AI threshold reverse engineering | 3 | 4 | 12 | MEDIUM | AI/ML Lead + Security | 4 |
| RISK-05 | Field agent GPS spoofing | 3 | 4 | 12 | MEDIUM | Mobile Arch + QC Lead | 8 |
| RISK-06 | Notification failure kills SLA | 4 | 3 | 12 | MEDIUM | Ops Arch + DevOps | 6 |
| RISK-07 | Audit log unqueryable at scale | 4 | 3 | 12 | MEDIUM | DBA + Platform Arch | 3 |
| RISK-08 | AI auto-decisioning without oversight | 3 | 4 | 12 | MEDIUM | Compliance Arch + Legal | 4 |
| RISK-09 | Cross-tenant duplicate not detected | 2 | 4 | 8 | MEDIUM | Platform + Privacy Arch | 4 |
| RISK-10 | Premature microfrontend | 3 | 3 | 9 | MEDIUM | Frontend Arch + Tech Lead | 3 |
| RISK-11 | Workflow state machine not persisted | 3 | 4 | 12 | MEDIUM | Backend Architect | 4 |
| RISK-12 | Document fraud detection false positives | 3 | 3 | 9 | MEDIUM | AI/ML Lead + QA | 6 |
| RISK-13 | Report template proliferation | 4 | 2 | 8 | MEDIUM | PM + Backend Engineer | 4 |
| RISK-14 | Data residency violation | 3 | 4 | 12 | MEDIUM | Cloud + Privacy Arch | 4 |
| RISK-15 | SLA calculation errors | 3 | 3 | 9 | MEDIUM | Backend Arch + QA | 3 |

---

# PART 9 — COMPLETE RFP REQUIREMENT TRACEABILITY MAPPING (EXPANDED)

> Full mapping for every RFP section to portal, page, functionality, UI component, API, AI dependency, compliance impact, and classification.

---

## 9.1 RFP SECTION 1 — STRATEGY & VISION

| RFP Ref | Requirement | Portal | Page | Functionality | UI Component | API Dependency | AI Dependency | Actor(s) | Why Needed | Compliance Impact | Classification |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1.1 | Platform modernization (legacy .NET → modern) | All Portals | All | Architecture-level — modern tech stack | N/A (infra) | REST APIs replacing SOAP | N/A | KPMG Engineering | Replace tightly coupled legacy system | N/A | Core Platform |
| 1.2 | API-first architecture | All | All | REST API layer per portal (BFF pattern) | N/A | All APIs RESTful with versioning | N/A | All actors | Enables ATS/HRIS integration; future extensibility | N/A | Core Platform |
| 1.3 | Phased delivery (not big bang) | All | N/A | Release management module (Super Admin) | Feature flags panel | Feature flag API | N/A | Platform Admin | Risk reduction in migration | N/A | Operational Enhancement |
| 1.4 | Risk-based adjudication support | Ops Portal | Adjudication Workbench | Adjudication matrix, risk-based outcome recommendation | Risk score card, adjudication matrix panel | GET /v1/cases/{id}/risk-profile | Risk scoring model | Adjudicator | Enables nuanced decisions beyond binary pass/fail | Audit — adjudication rationale recorded | Core Workflow |
| 1.5 | Multi-country/jurisdiction support | All | Country-specific form sections, check availability matrix | Country selector, jurisdiction-specific fields | GET /v1/countries/{id}/check-config | N/A | All actors | India domestic + international BGV in same platform | GDPR/DPDP jurisdiction-specific processing rules | Multi-Country |
| 1.7 | Three-track SLA/TAT configuration (Client / Internal / Vendor) | Ops Portal + Super Admin | SLA Policy Editor (6.1.27) + Tenant Provisioning Wizard Step 6 (6.5.1) | Three independent SLA clocks per check type; default template pre-loaded (KPMG baseline); configurable per client; holiday-aware calculation (RFP 23.14) | Three-track SLA Health Card (Case Workbench); SLA Policy Table with Client/Internal/Vendor columns; [Reset to Default] per row; Amber/Red threshold config | GET /v1/sla/policy?client_id= — POST /v1/sla/policy — GET /v1/cases/{id}/sla-status (returns all three tracks) | Predictive breach model (optional — SLA breach probability) | Ops Admin (configures), Ops Reviewer (monitors), Adjudicator (governed by) | Separate TAT accountability per track; enables vendor performance tracking without confusing client SLA; penalty trigger accuracy (RFP 22.2) | Client SLA breach → penalty trigger (RFP 22.2); Vendor SLA breach → vendor scorecard; Internal SLA breach → ops efficiency audit | Core Workflow — C-03 |

---

## 9.2 RFP SECTION 2 — AI & FRAUD DETECTION

| RFP Ref | Requirement | Portal | Page | Functionality | UI Component | API Dependency | AI Dependency | Actor(s) | Why Needed | Compliance Impact | Classification |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 2.1 | Face match (selfie vs ID) | Candidate Portal | Biometric Capture | Selfie capture, face match against ID document | Face match panel, match score meter | POST /v1/biometric/{case_id}/face-match | Face recognition model (≥ 95% accuracy) | Candidate (primary), Ops (reviews result) | Prevent identity fraud — ensure person matches ID | Biometric data = special category under DPDP/GDPR — separate consent required | AI-Required + Compliance-Critical |
| 2.2 | Active liveness detection | Candidate Portal | Biometric Capture | Active challenge (blink, turn) | Liveness challenge UI, step progress | POST /v1/biometric/{case_id}/liveness | Liveness detection model | Candidate | Prevent photo/video replay attacks | N/A | AI-Required |
| 2.3 | Passive liveness | Candidate Portal | Biometric Capture | Single-frame liveness analysis | Passive liveness UI | POST /v1/biometric/{case_id}/liveness-passive | Passive liveness model | Candidate | Accessibility alternative to active | N/A | AI-Required |
| 2.4 | Deepfake detection | Ops Portal | KYC Workspace | Review deepfake detection flag on submitted selfie | Deepfake flag badge, confidence score, evidence | GET /v1/biometric/{case_id}/ai-signals | Deepfake detection model | Ops Reviewer | Sophisticated fraud prevention | N/A | AI-Required |
| 2.5 | Document OCR + data extraction | Candidate Portal + Ops | Upload Center + KYC Workspace | OCR extraction from ID documents, quality feedback | OCR preview in candidate upload; OCR comparison panel in ops | POST /v1/documents/{id}/ocr | OCR model (multi-document type) | Candidate (upload quality), Ops (verification) | Eliminates manual data entry; enables automated comparison | N/A | AI-Required |
| 2.6 | Document authenticity check | Ops Portal | KYC + All check workspaces | Fraud detection on all uploaded documents | Authenticity badge, fraud signal overlay, region highlights | POST /v1/documents/{id}/authenticity | Document fraud detection model | Ops Reviewer | Detect forged certificates, edited documents | N/A | AI-Required |
| 2.7 | Presentation attack detection | Candidate Portal | Document Upload | Camera-only enforcement; screenshot/gallery block | Camera widget (no gallery option) | POST /v1/documents/{id}/upload (with anti-spoof validation) | Presentation attack detector | Candidate | Prevent photo-of-photo or screen-capture document submission | N/A | AI-Required |
| 2.8 | MRZ/barcode validation | Ops Portal | KYC Workspace | MRZ and barcode parsing from Passport/DL | MRZ validation result panel | POST /v1/documents/{id}/mrz-validate | MRZ parsing module | Ops Reviewer | Machine-readable zone validation — confirms document integrity | N/A | AI-Required |
| 2.9 | AI-assisted discrepancy detection | Ops Portal | Case Workbench | Auto-detection and classification of discrepancies across all checks | Discrepancy panel, severity badge | GET /v1/cases/{id}/discrepancies | Discrepancy detection model | Ops Reviewer | Reduces manual discrepancy identification; increases consistency | Discrepancy audit trail required | AI-Required |
| 2.10 | Fraud risk scoring | Ops Portal | Case Workbench | Composite fraud risk score with component breakdown | Risk score gauge, component drilldown card | GET /v1/cases/{id}/risk-score | Composite risk scoring model | Ops Reviewer, Adjudicator | Prioritizes high-risk cases for senior review | Risk score in adjudication record | AI-Required |
| 2.11 | Explainable AI (reason codes) | Ops Portal | Case Workbench → AI Signals tab | Human-readable reason codes for each AI flag | Reason code display per flag, AI signal drawer | GET /v1/cases/{id}/ai-signals | Explainability wrapper on all models | Ops Reviewer | Required for human override decisions; regulatorily necessary for automated decisions | GDPR Article 22 — meaningful information about logic | AI-Required + Compliance-Critical |
| 2.12 | AI-powered case routing | Ops Portal | Case Management | Auto-assign cases to reviewers based on check type, geography, workload, skill | Auto-assignment logic (background) | POST /v1/cases/{id}/auto-assign | Case routing model | Ops Admin, System | Reduces manual assignment overhead | N/A | AI-Required |
| 2.13 | Auto-decisioning with audit | Ops Portal + Super Admin | Case Workbench (ops), Threshold Config (super admin) | Auto-approve zero-flag clear cases; full audit of every auto-decision | Auto-decision log, model version tag | POST /v1/cases/{id}/auto-decision | Decisioning model | System | Reduces ops workload for clear cases | GDPR Article 22 — auto-decision logged with rationale | AI-Required + Compliance-Critical |
| 2.14 | Predictive SLA alerts | Ops Portal | Live SLA Dashboard | Breach probability prediction per case | Breach prediction widget, urgency ticker | GET /v1/sla/breach-predictions | Predictive SLA model | Ops Manager, Team Lead | Enables proactive (not reactive) SLA management | SLA penalty reduction | AI-Required + SLA-Critical |
| 2.15 | Reviewer assist summary | Ops Portal | Case Workbench | AI-generated case summary for reviewer | Reviewer assist card (collapsible) | GET /v1/cases/{id}/ai-summary | Case summarization model | Ops Reviewer | Reduces time-to-context for reviewer; guides investigation | N/A | AI-Required |
| 2.16 | Model version tracking per decision | Ops Portal + Super Admin | AI Signals tab, AI Model Registry | Model version logged for every AI decision | Model version tag per flag, model registry table | GET /v1/ai-models (registry) | All models | Ops Reviewer, Platform Admin | Reproducibility; audit defense; model rollback capability | Required for explainable AI audit | Audit-Critical |
| 2.17 | Bias/fairness monitoring | Super Admin Portal | AI Bias Monitor | Subgroup performance monitoring, disparity detection | Subgroup table, disparity chart, investigation workflow | GET /v1/ai-governance/bias-metrics | Monitoring layer on all models | Platform Admin | Prevent discriminatory AI outcomes | GDPR Article 22 safeguards; emerging AI regulation | Compliance-Critical |
| 2.18 | OCR data vs declared data comparison | Ops Portal | KYC Workspace | Side-by-side comparison of OCR-extracted vs candidate-entered fields | OCR comparison panel with diff highlighting | GET /v1/cases/{id}/ocr-comparison | OCR model | Ops Reviewer | Catches data entry fraud (candidate entered different name/DOB than ID shows) | N/A | Core Workflow |
| 2.19 | Duplicate session detection | Platform (background) | All portals (background) | Detect same candidate submitting from multiple devices simultaneously | Alert to ops (background flag) | Fraud signal API | Session anomaly model | System | Organized fraud detection (group submission coaching) | N/A | AI-Required |
| 2.20 | Device/geo risk signal | Candidate Portal + Ops | Biometric Capture (candidate), KYC Workspace (ops) | Device fingerprint, IP geo, VPN/proxy detection | Device risk panel (ops view) | POST /v1/sessions/{id}/device-risk | Device risk scoring | Candidate (data collected), Ops (reviewed) | Context risk signals — candidate submitting from unusual location | N/A | AI-Required |
| 2.21 | Employment gap analysis | Ops Portal + Candidate Portal | Employment Workspace (ops), Employment Form (candidate) | AI-generated gap analysis from declared tenures | Gap analysis widget (ops); gap detection alert (candidate) | GET /v1/cases/{id}/employment-gaps | Gap analysis model | Ops Reviewer, Candidate | Detect undisclosed employment history | N/A | AI-Required |
| 2.22 | Duplicate candidate detection | Client Portal + Ops | Case Initiation (client), All Cases (ops) | Detect when same candidate initiated across cases | Duplicate alert card | GET /v1/candidates/duplicate-check | Hash-based matching | Client Initiator, Ops | Avoid redundant verifications; detect fraud repetition | N/A | Operational Enhancement |
| 2.23 | Dual employment detection | Ops Portal | Employment Workspace | Detect overlapping employment tenures (UAN cross-check + date analysis) | Dual employment flag panel | GET /v1/cases/{id}/dual-employment | Date overlap analysis | Ops Reviewer | Declared tenures overlap — integrity signal | N/A | AI-Required |
| 2.24 | Fraud intelligence dashboard | Ops Portal | MIS Dashboard → Fraud Analytics tab | Aggregated fraud signal trends, fraud type distribution | Fraud flag trend chart, fraud type breakdown | GET /v1/analytics/fraud-summary | Aggregated AI analytics | Ops Manager, Senior Reviewer | Pattern detection across cases; informs threshold calibration | N/A | AI-Required |

---

## 9.3 RFP SECTION 3 — KYC VERIFICATION

| RFP Ref | Requirement | Portal | Page | Functionality | UI Component | API Dependency | AI Dependency | Actor(s) | Why Needed | Compliance Impact | Classification |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 3.1 | Aadhaar OTP verification | Ops Portal | KYC Workspace | Aadhaar API call (UIDAI) with masked display | Aadhaar result panel, masked number display | POST /v1/kyc/aadhaar-verify | N/A | Ops Reviewer | Government-backed identity verification | Aadhaar data handling under UIDAI regulations — strict data minimization | Compliance-Critical |
| 3.2 | PAN verification | Ops Portal | KYC Workspace | NSDL/CDSL PAN API — name + DOB match | PAN result panel | POST /v1/kyc/pan-verify | N/A | Ops Reviewer | Tax identity verification | N/A | Core Workflow |
| 3.3 | Passport verification | Ops Portal | KYC Workspace | Passport authority check (ICAO, immigration DB where accessible) + MRZ validation | Passport result panel, MRZ panel | POST /v1/kyc/passport-verify | MRZ parser | Ops Reviewer | International identity; anti-fraud | N/A | Core Workflow |
| 3.4 | Driving license verification | Ops Portal | KYC Workspace | RC/DL API (Sarathi, Vahan) | DL result panel | POST /v1/kyc/dl-verify | N/A | Ops Reviewer | Secondary ID verification | N/A | Core Workflow |
| 3.5 | Voter ID verification | Ops Portal | KYC Workspace | Election Commission API (where accessible) | Voter ID result panel | POST /v1/kyc/voter-verify | N/A | Ops Reviewer | Secondary ID | N/A | Core Workflow |
| 3.6 | Document upload + AI quality check | Candidate Portal | Document Upload Center | Upload with real-time quality AI | Quality indicator, OCR preview | POST /v1/documents/upload + quality check | OCR + quality model | Candidate | Reduce insufficiency from poor document quality | N/A | Candidate-Experience |
| 3.7 | Cross-document consistency | Ops Portal | KYC Workspace | Name/DOB/address match across all submitted ID documents | Cross-doc consistency panel | GET /v1/cases/{id}/cross-doc-consistency | OCR + name match | Ops Reviewer | Multi-document fraud detection | N/A | AI-Required |
| 3.8 | Biometric face match | Candidate Portal + Ops | Biometric Capture + KYC Workspace | (See 2.1) | (See 2.1) | (See 2.1) | (See 2.1) | Candidate + Ops | (See 2.1) | (See 2.1) | AI-Required |
| 3.9 | DigiLocker integration | Candidate Portal + Ops | Education Form (candidate), Education Workspace (ops) | OAuth to DigiLocker; fetch verified certificates | DigiLocker fetch button, fetched data panel | GET /v1/digilocker/fetch?case_id={id} | N/A | Candidate | Reduces document fraud; government-verified certificates | N/A | Core Workflow |
| 3.10 | PEP/sanctions screening | Ops Portal | Legal Check Workspace | Watchlist screening — OFAC, UN, EU, domestic PEP lists | Sanctions result panel | POST /v1/legal/sanctions-check | N/A | Ops Reviewer | Anti-money laundering and high-risk hire detection | PMLA/FATF compliance where applicable | Compliance-Critical |

---

## 9.4 RFP SECTION 4 — EMPLOYMENT VERIFICATION

| RFP Ref | Requirement | Portal | Page | Functionality | UI Component | API Dependency | AI Dependency | Actor(s) | Why Needed | Compliance Impact | Classification |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 4.1 | Structured employer outreach | Ops Portal + Employer Module | Employment Workspace + Employer Response Form | Tokenized outreach link; structured employer response form | Outreach status panel, [Send Outreach] button; Employer response form (module) | POST /v1/employer-outreach/{case_id}/send | N/A | Ops Reviewer (sends), Employer (responds) | Replace email/phone verification with structured digital response | Employer response = audit evidence | Core Workflow |
| 4.2 | Digital employer response channel | Employer Response Module | Employer Response Form | Secure form with pre-filled candidate data; employer confirms/corrects | Response form (tokenized) | POST /v1/employer-response/{token} | N/A | Employer | Structured, auditable response vs unstructured email | Employer response audit trail | Core Workflow |
| 4.3 | EPFO/UAN verification | Ops Portal | Employment Workspace | UAN API pull + employment history from EPFO | EPFO result panel, tenure diff table | POST /v1/employment/epfo-verify | N/A | Ops Reviewer | Official employment record cross-check | Data minimization — EPFO data used only for employment verification | Core Workflow |
| 4.4 | Tenure reconciliation | Ops Portal | Employment Workspace | Side-by-side: candidate claimed vs UAN vs employer confirmed | Tenure reconciliation 3-column panel | GET /v1/cases/{id}/employment-reconciliation | Gap analysis model | Ops Reviewer | Find discrepancies between three independent data sources | Discrepancy = audit-documented | Core Workflow |
| 4.5 | Experience letter fraud detection | Ops Portal | Employment Workspace | AI authenticity check on uploaded experience letters | Experience letter fraud flag, authenticity badge | POST /v1/documents/{id}/authenticity | Document fraud model | Ops Reviewer | Experience letters are most commonly forged document in India BGV | N/A | AI-Required |
| 4.6 | ITR/payslip verification | Ops Portal | Employment Workspace | Cross-reference ITR income data with employment tenure | ITR result panel | POST /v1/employment/itr-verify | N/A | Ops Reviewer | Financial cross-verification of employment | Permissible purpose documentation required | Core Workflow |
| 4.7 | Dual employment detection | Ops Portal | Employment Workspace | (See 2.23) | (See 2.23) | (See 2.23) | Date overlap model | Ops Reviewer | (See 2.23) | N/A | AI-Required |
| 4.8 | Employment gap analysis | Ops Portal + Candidate | (See 2.21) | (See 2.21) | (See 2.21) | (See 2.21) | Gap model | Both | (See 2.21) | N/A | AI-Required |
| 4.9 | Self-employment / freelance verification | Ops Portal | Employment Workspace | GST registration check, portfolio verification, bank statement review | Self-employment verification panel | POST /v1/employment/self-employment-verify | N/A | Ops Reviewer | Non-traditional employment verification | N/A | Operational Enhancement |
| 4.10 | International employer verification | Ops Portal | Employment Workspace | International outreach via email/tokenized link (same module); LinkedIn data assist | International outreach panel, LinkedIn assist button | POST /v1/employer-outreach/{case_id}/send (international) | N/A | Ops Reviewer | Multi-country workforce at KPMG clients | Multi-country requirement | Multi-Country |
| 4.11 | Company closure/non-response handling | Ops Portal | Employment Workspace | Mark as "Unable to Verify — Company non-responsive" with evidence of attempt | Unable-to-verify panel, evidence attach | POST /v1/cases/{check_id}/mark-unable-to-verify | N/A | Ops Reviewer | Many older employers may be closed or unresponsive | Audit trail of verification attempt | Core Workflow |
| 4.12 | Reference check | Ops Portal + Referee Module | Reference Check Workspace + Referee Response Form | Structured reference questionnaire sent via tokenized link | Reference status panel, [Send Reference Link] button; Referee questionnaire form | POST /v1/reference-check/{case_id}/send | N/A | Ops Reviewer (sends), Referee (responds) | Professional reference verification | Referee response = audit evidence | Operational Enhancement |
| 4.13 | Reference questionnaire (configurable) | Client Portal | Form Builder | Client configures reference questionnaire questions | Form builder drag-and-drop | PUT /v1/tenants/{id}/reference-form | N/A | Client Admin | Different clients need different reference questions | N/A | Operational Enhancement |
| 4.14 | Vendor routing for employment checks | Ops Portal | Vendor Assignment Console | Assign employment check to external BGV vendor | Vendor assignment drawer | POST /v1/cases/{id}/vendor-assign | AI routing suggestion | Ops Reviewer | Some employers require on-site or specialized verification | Subprocessor documentation required | Vendor-Governance |
| 4.15 | Designation match (role-level accuracy) | Ops Portal | Employment Workspace | Compare claimed designation vs UAN vs employer confirmed | Designation comparison in tenure reconciliation panel | Employment verification API | N/A | Ops Reviewer | Designation inflation is common fraud type | N/A | Core Workflow |

---

## 9.5 RFP SECTION 5 — EDUCATION VERIFICATION

| RFP Ref | Requirement | Portal | Page | Functionality | UI Component | API Dependency | AI Dependency | Actor(s) | Why Needed | Compliance Impact | Classification |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 5.1 | University direct verification | Ops Portal + University Module | Education Workspace + University Response Form | Tokenized university response form; structured academic response | University outreach panel; University response form | POST /v1/university-outreach/{case_id}/send | N/A | Ops Reviewer (sends), University (responds) | Structured verification vs email/manual | University response = audit evidence | Core Workflow |
| 5.2 | Institution accreditation check | Ops Portal | Education Workspace | UGC/AICTE/State Board recognition status | Recognition status badge, accreditation result panel | POST /v1/education/institution-check | N/A | Ops Reviewer | Fake universities are a common fraud vector in India | N/A | Core Workflow |
| 5.3 | Degree fraud detection | Ops Portal | Education Workspace | AI authenticity check on degree certificates | Degree fraud flag, certificate authenticity panel | POST /v1/documents/{id}/authenticity | Certificate fraud model (education-specific) | Ops Reviewer | Certificate fabrication is prevalent | N/A | AI-Required |
| 5.4 | DigiLocker integration | Candidate + Ops | (See 3.9) | (See 3.9) | (See 3.9) | (See 3.9) | N/A | (See 3.9) | (See 3.9) | N/A | Core Workflow |
| 5.5 | Batch university verification | University Module | University Response Form | Batch response option for large institutions | Batch upload template in university module | POST /v1/university-response/batch | N/A | University (large institution) | Reduces friction for high-volume institutions (IITs, IIMs) | N/A | Operational Enhancement |
| 5.6 | Course duration validation | Ops + Candidate | Education Workspace + Education Form | Auto-validate claimed duration vs standard duration for degree type | Duration validation alert | GET /v1/education/validate-duration | Duration validation logic | Ops Reviewer, Candidate | A 2-year degree cannot be completed in 1 year | N/A | AI-Required |
| 5.7 | Duplicate certificate detection | Ops Portal | Education Workspace | Same roll number/registration in another case | Duplicate cert alert | POST /v1/education/duplicate-check | Hash matching | Ops Reviewer | Organized fraud (same certificate used across multiple applications) | N/A | AI-Required |
| 5.8 | Name change handling | Candidate + Ops | Education Form + Education Workspace | Affidavit upload if name differs; ops reviews affidavit | Name mismatch alert; affidavit viewer | N/A | Name match model | Candidate, Ops Reviewer | Women's name changes (marriage) — legitimate but needs documentation | N/A | Core Workflow |
| 5.9 | International education verification | Ops Portal | Education Workspace | Equivalency check (AIU); international institution recognition | International education panel | POST /v1/education/international-verify | N/A | Ops Reviewer | Multi-country educational backgrounds | Multi-country requirement | Multi-Country |

---

## 9.6 RFP SECTION 6 — LEGAL / CRIMINAL VERIFICATION

| RFP Ref | Requirement | Portal | Page | Functionality | UI Component | API Dependency | AI Dependency | Actor(s) | Why Needed | Compliance Impact | Classification |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 6.1 | District court search | Ops Portal | Legal Check Workspace | Court record search by name + DOB + geography | Court results table | POST /v1/legal/court-search (district) | N/A | Ops Reviewer | Primary criminal background source | Legal check consent required | Compliance-Critical |
| 6.2 | High court search | Ops Portal | Legal Check Workspace | High Court records per state | Court results (High Court section) | POST /v1/legal/court-search (high-court) | N/A | Ops Reviewer | Escalated legal proceedings | (See 6.1) | Core Workflow |
| 6.3 | Supreme court search | Ops Portal | Legal Check Workspace | Supreme Court records | Court results (SC section) | POST /v1/legal/court-search (supreme) | N/A | Ops Reviewer | Highest-risk legal proceedings | (See 6.1) | Core Workflow |
| 6.4 | SEBI/SFIO/RBI search | Ops Portal | Legal Check Workspace | Regulatory enforcement database search | Regulatory results panel | POST /v1/legal/regulatory-check | N/A | Ops Reviewer | Financial misconduct for finance-sector roles | PMLA/SEBI compliance | Compliance-Critical |
| 6.5 | Global sanctions/PEP screening | Ops Portal | Legal Check Workspace | OFAC, UN, EU watchlists + domestic PEP | Sanctions/PEP result panel | POST /v1/legal/sanctions-check | N/A | Ops Reviewer | Regulatory requirement for banking/finance/govt sector clients | PMLA/FATF | Compliance-Critical |
| 6.6 | Case status interpretation | Ops Portal | Legal Check Workspace | Distinguish disposed/pending/convicted — different risk levels | Case status badge (Disposed/Pending/Convicted), interpretation guidance | Court search API | N/A | Ops Reviewer | A disposed case has different risk than a pending charge | Adjudication matrix required for legal hits | Core Workflow |
| 6.7 | Identity resolution for legal hits | Ops Portal | Legal Check Workspace | Confirm legal hit is same person (name + DOB + address match) | Identity disambiguation panel | N/A | Name/identity match model | Ops Reviewer | Common names produce false positive hits | Wrongful adverse action risk | Core Workflow |
| 6.8 | Role-based check depth | Client Portal + Ops | Package Configurator + Legal Workspace | Senior executives get deeper search scope | Package config: check depth selector; Workspace: jurisdiction coverage indicator | GET /v1/packages/{id}/legal-scope | N/A | Client Admin (configures), Ops (executes) | Risk-appropriate verification depth | N/A | Core Workflow |

---

## 9.7 RFP SECTION 7 — ADDRESS VERIFICATION

| RFP Ref | Requirement | Portal | Page | Functionality | UI Component | API Dependency | AI Dependency | Actor(s) | Why Needed | Compliance Impact | Classification |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 7.1 | Digital address verification | Ops Portal | Address Workspace | Geo-coordinate validation, distance check, utility/telecom DB | Digital verification panel, map widget | POST /v1/address/digital-verify | N/A | Ops Reviewer | Remote-first verification for urban addresses | N/A | Core Workflow |
| 7.2 | GPS-tagged field visit | Field Agent App | Evidence Capture | GPS capture, photo with coordinates embedded, timestamp | GPS status, photo capture, coordinate display | POST /v1/field/evidence-submit | GPS authenticity check | Field Agent | Tamper-evident physical presence evidence | GPS evidence = audit artifact | Core Workflow |
| 7.3 | Photo with timestamp | Field Agent App | Evidence Capture | Timestamp embedded in photo metadata + server-side validation | Photo gallery with timestamps | POST /v1/field/evidence-submit | Photo metadata validator | Field Agent | Prevents pre-captured photo submission | N/A | Core Workflow |
| 7.4 | Neighbor verification | Field Agent App | Evidence Capture | Structured neighbor verification checklist | Neighbor verification notes field | POST /v1/field/evidence-submit | N/A | Field Agent | Corroborates residence without candidate present | N/A | Core Workflow |
| 7.5 | Remote video verification | Ops Portal | Address Workspace | Scheduler + video session for remote-friendly packages | Remote video scheduler, session status | POST /v1/address/video-schedule | N/A | Ops Reviewer (schedules), Candidate (participates) | Remote address verification option | N/A | Operational Enhancement |
| 7.6 | Photo authenticity check | Ops Portal | Address Workspace | AI check on field photos for GPS spoofing / non-authentic images | Photo authenticity badge | POST /v1/documents/{id}/photo-authenticity | Photo authenticity model (GPS cross-check) | Ops Reviewer | Detect fraudulent field agent submissions | N/A | AI-Required |

---

## 9.8 RFP SECTION 8 — FINANCIAL VERIFICATION

| RFP Ref | Requirement | Portal | Page | Functionality | UI Component | API Dependency | AI Dependency | Actor(s) | Why Needed | Compliance Impact | Classification |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 8.1 | Credit bureau check | Ops Portal | Financial Workspace | CIBIL/Experian API check (permissible purpose only) | Credit result panel | POST /v1/financial/credit-check | N/A | Ops Reviewer | Finance-sector specific hire requirement | Strict permissible purpose — explicit consent and legal basis required | Compliance-Critical |
| 8.2 | Bankruptcy/insolvency check | Ops Portal | Financial Workspace | MCA/DRT/NCLT search | Insolvency result panel | POST /v1/financial/insolvency-check | N/A | Ops Reviewer | Finance/senior executive hire requirement | N/A | Core Workflow |
| 8.3 | AML screening | Ops Portal | Financial Workspace | AML pattern analysis (where permissible) | AML flag panel | POST /v1/financial/aml-check | N/A | Ops Reviewer | Banking sector clients | PMLA compliance | Compliance-Critical |
| 8.4 | Financial check consent | Candidate Portal | Consent Capture | Separate explicit consent for financial data | Separate financial consent checkbox | POST /v1/consent/{case_id}/financial | N/A | Candidate | Financial data = sensitive — separate consent required beyond general consent | DPDP financial data handling; credit bureau regulatory requirement | Compliance-Critical |
| 8.5 | Purpose limitation display | Candidate Portal + Ops | Consent + Financial Workspace | Display specific legal purpose for financial check | Purpose statement in consent; purpose indicator in ops workspace | N/A | N/A | Candidate, Ops | Data minimization — only collect what's needed for stated purpose | GDPR Article 5(1)(b); DPDP purpose limitation | Compliance-Critical |

---

## 9.9 RFP SECTION 10 — WORKFLOW & OPERATIONS

| RFP Ref | Requirement | Portal | Page | Functionality | UI Component | API Dependency | AI Dependency | Actor(s) | Why Needed | Compliance Impact | Classification |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 10.1 | Case initiation | Client Portal + Ops Portal | Case Initiation Wizard (6.2.1) — two modes; Bulk Upload Tab 2 (6.2.2); Ops Manual Case Creation (6.2.22) | Single-case creation (invite or direct entry), bulk pre-filled upload, ops manual entry | Wizard (5 steps, mode-aware), package tiles, consent declaration (non-candidate mode), confirmation screen | POST /v1/cases | Duplicate detection; initiation_mode tag | Client Initiator, Client Admin, Ops Reviewer | All five non-candidate flows (F1–F5) + standard candidate flow covered | Consent chain initiation triggered (candidate mode); consent reference captured (non-candidate mode) | Core Workflow |
| 10.2 | Requisition reference tracking | Client Portal + Ops | Case Initiation + Case Detail | Requisition/Job ID field linked to case | Req ref field (client initiation), req ref display (ops case) | POST /v1/cases (req_ref field) | N/A | Client Initiator | Links BGV case to hiring workflow | N/A | Core Workflow |
| 10.3 | Candidate invitation flow | All | Invitation delivery → Candidate portal auth | OTP invitation link delivery with multi-channel | Invitation confirmation screen (client), OTP login (candidate) | POST /v1/invitations | N/A | System (delivers), Candidate (receives) | Entry point for candidate into platform | N/A | Core Workflow |
| 10.4 | Dynamic form (package-driven) | Candidate Portal | Verification Form | Only show fields/sections required by package | Dynamic form renderer | GET /v1/packages/{id}/form-schema | N/A | Candidate | Data minimization; reduce candidate friction | DPDP/GDPR data minimization | Compliance-Critical |
| 10.5 | SLA governance | Ops Portal | Live SLA Dashboard + Case Workbench | Per-check SLA timers, breach prediction, pause/resume, escalation | SLA countdown, prediction widget, pause log | GET /v1/cases/{id}/sla-status | Predictive SLA model | Ops Manager, Team Lead | Core operational commitment to clients | SLA penalties apply (RFP 22.2) | SLA-Critical |
| 10.6 | Insufficiency management | Ops Portal | Case Workbench + Insufficiency Queue | Field-level remarks, candidate re-submission flow, SLA pause | Insufficiency drawer, re-submission status | POST /v1/cases/{id}/insufficiency | N/A | Ops Reviewer, Candidate | Core case management for incomplete submissions | Re-submission audit required | Core Workflow |
| 10.7 | Waiver management | Ops Portal + Client Portal | Waiver Management + Case Detail | Waiver request, approval routing, waiver history | Waiver drawer, approval chain, history log | POST /v1/waivers | N/A | Adjudicator, Risk/Legal, Client (if required) | Operational flexibility for nuanced outcomes | Waiver decisions = audit artifacts | Compliance-Critical |
| 10.8 | Report generation and delivery | Ops Portal | Report Builder | Client-specific template, sign-off, delivery | Report preview, template selector, delivery confirmation | POST /v1/reports/generate | N/A | Adjudicator, System | Core deliverable to client | Report is formal verification record | Core Workflow |
| 10.9 | Adjudication outcome | Ops Portal | Adjudication Workbench | Final decision with mandatory notes, evidence, pre-adverse trigger | Outcome modal, AI summary, evidence attach | POST /v1/cases/{id}/adjudication | Reviewer assist, discrepancy classifier | Adjudicator | Formal BGV closure | Primary compliance artifact — must be auditable | Compliance-Critical |
| 10.10 | Dispute management | Ops Portal + Candidate Portal | Dispute Workbench + Raise a Concern | Dispute intake, investigation, resolution, candidate notification | Dispute registry, investigation workspace, resolution modal | POST /v1/disputes, PUT /v1/disputes/{id}/resolve | N/A | Candidate (files), Compliance Reviewer (resolves) | DPDP/GDPR right to challenge | Mandatory under DPDP | Compliance-Critical |
| 10.11 | Pre-adverse / adverse notice | Ops Portal | Adjudication Workbench | Generate and deliver FCRA-style notices | Notice generator, waiting period timer, delivery tracker | POST /v1/cases/{id}/adverse-notice | N/A | Adjudicator | Legal requirement before adverse hiring action | FCRA/equivalent compliance | Compliance-Critical |
| 10.12 | Case status visibility (client) | Client Portal | Case Detail (client view) | High-level status without ops internals | Status timeline, check status icons | GET /v1/cases/{id}/client-view | N/A | Client User | Client right to status transparency | N/A | Core Workflow |
| 10.13 | Ops case queue management | Ops Portal | All Cases + My Queue | Sortable, filterable case queues with bulk actions | Mega-table, filters, bulk action toolbar | GET /v1/cases (paginated, filtered) | Case routing model | Ops Reviewer, Team Lead | High-volume operations management | N/A | Core Workflow |
| 10.14 | QA/QC workflow | Ops Portal | QC Sampling Queue | Second-level quality review with error tagging | QC queue, error tag interface, reviewer feedback | POST /v1/cases/{id}/qc-result | QC targeting model | QC Reviewer | Quality assurance; catches reviewer errors before delivery | QC records = quality audit artifacts | Audit-Critical |
| 10.15 | Bulk case upload | Client Portal | Bulk Upload Page (6.2.2) — Tab 1: bulk invite; Tab 2: bulk pre-filled data (no candidate invite) | Excel upload with validation — two modes: invite-based and pre-filled data | Tab bar, file upload, row validation, ConsentObtained column (Tab 2), preview, confirm | POST /v1/cases/bulk | Duplicate detection; consent column enforcement (Tab 2) | Client Admin | Enterprise-scale case initiation efficiency; covers 50% manual entry legacy pattern (PPTX) | Consent column per-row in Tab 2 | Operational Enhancement |
| 10.16 | Auto-save and resume | Candidate Portal | Verification Form | Server-side form state, OTP resume | Auto-save indicator, session expiry modal | PUT /v1/sessions/{id}/state | N/A | Candidate | Mobile network resilience | N/A | Candidate-Experience |
| 10.17 | Color-code outcome | Ops Portal + Client Portal + Reports | All relevant pages | Green/Amber/Yellow/Red per adjudicated outcome | Color badge on case and report | GET /v1/cases/{id}/outcome-color | N/A | All | Standardized outcome communication | Color outcomes are part of formal report | Core Workflow |
| 10.18 | Delegation/temp access | Ops Portal + Super Admin | Team Management | Temporary elevated access with expiry | Delegation setup form, expiry date | PUT /v1/users/{id}/delegate | N/A | Ops Admin | Holiday/absence coverage | Delegation logged in audit | Audit-Critical |
| 10.19 | Vendor orchestration | Ops Portal | Vendor Assignment Console | Case-to-vendor assignment, tracking, SLA | Vendor matrix, assignment drawer, tracking panel | POST /v1/cases/{id}/vendor-assign | AI routing model | Ops Reviewer | Route specialized checks to capable vendors | Subprocessor documentation | Vendor-Governance |

---

## 9.10 RFP SECTION 11 — CANDIDATE PORTAL

| RFP Ref | Requirement | Portal | Page | Functionality | UI Component | API Dependency | AI Dependency | Actor(s) | Why Needed | Compliance Impact | Classification |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 11.1 | Mobile-first design | Candidate Portal | All pages | Responsive, PWA-ready, touch-optimized | All components mobile-responsive | N/A | N/A | Candidate | Majority of candidates on mobile | N/A | Candidate-Experience |
| 11.2 | Client branding (white-label) | Candidate Portal | All pages | Client logo, color, domain, welcome message | Branded header, branded buttons | GET /v1/tenants/{id}/branding | N/A | Candidate | Candidate trust — recognizes their employer | N/A | Candidate-Experience |
| 11.3 | OTP-based authentication | Candidate Portal | Login | Mobile OTP (WhatsApp/SMS) + email fallback | OTP entry, resend, fallback | POST /v1/auth/otp-request | N/A | Candidate | No persistent account required; secure one-time access | Session audit required | Core Workflow |
| 11.4 | E-signature consent | Candidate Portal | Consent Page | Canvas signature, type-to-sign, DocuSign | Signature pad, DocuSign iframe | POST /v1/consent/{case_id}/signature | N/A | Candidate | Legally binding consent | Signed consent = lawful basis for processing | Compliance-Critical |
| 11.5 | Document upload with quality check | Candidate Portal | Document Upload | (See 3.6 and 2.5 cross-ref) | Quality indicator, OCR preview | (See above) | OCR + quality model | Candidate | (See above) | N/A | AI-Required |
| 11.6 | Multi-language support | Candidate Portal | All pages | UI language selector (6–8 languages) | Language selector (persistent) | GET /v1/i18n/{lang}/strings | N/A | Candidate | India's linguistic diversity | N/A | Candidate-Experience |
| 11.7 | Multi-channel notifications | All (candidate-facing) | All | Email + SMS + WhatsApp with fallback chain | Notification delivery status display | POST /v1/notifications/send | N/A | System (delivers), Candidate (receives) | Invitation delivery must reach candidate | Notification delivery = audit event | Core Workflow |
| 11.8 | Consent receipt | Candidate Portal | Consent Page | Downloadable consent receipt PDF | Download button + email delivery | POST /v1/consent/{id}/receipt | N/A | Candidate | Candidate right to evidence of consent | DPDP/GDPR consent receipt | Compliance-Critical |
| 11.9 | Multilingual UI — support multiple languages with locale-specific formats [C-10] | Candidate Portal | All pages (Candidate Portal) | 6-language minimum (en, hi, ta, te, kn, ar) with locale-specific date/number/currency formats. Language selector persistent across all pages. Arabic requires RTL layout. Scope boundary defined in Part 4.10. | Language selector (persistent, flag icons, auto-detect from device) | GET /v1/i18n/{locale}/strings | N/A | Candidate | India's linguistic diversity + ME region (Arabic) | Consent notice legally required in candidate's language (DPDP/GDPR) | Core Workflow — C-10 |
| 11.10 | Status tracking | Candidate Portal | Status Page | High-level case status with expected completion | Progress indicator, per-check status | GET /v1/cases/{id}/candidate-view | N/A | Candidate | Candidate right to know process status | N/A | Candidate-Experience |
| 11.11 | Dispute initiation | Candidate Portal | Raise a Concern | Self-service dispute form | Dispute form, type selector, evidence upload | POST /v1/disputes | N/A | Candidate | DPDP right to challenge | Mandatory under DPDP | Compliance-Critical |
| 11.12 | Support access | Candidate Portal | Help & Support | Chat, email, toll-free, WhatsApp | Chat widget, contact form | N/A | N/A | Candidate | Candidate assistance during unfamiliar process | N/A | Candidate-Experience |
| 11.13 | WhatsApp deep-link | Candidate Portal | Status Page + Support | WhatsApp support link | WhatsApp link button | N/A | N/A | Candidate | WhatsApp is primary communication in India | N/A | Candidate-Experience |
| 11.14 | Completion notification | All | Post-report delivery | Notify candidate that BGV is complete | Notification (email + SMS + WhatsApp) | POST /v1/notifications/send (completion) | N/A | System, Candidate | Candidate right to know outcome status | N/A | Core Workflow |

---

## 9.11 RFP SECTION 12 — ADMIN / CONFIGURATION

| RFP Ref | Requirement | Portal | Page | Functionality | Actor | Classification |
|---|---|---|---|---|---|---|
| 12.1 | Package management | Client Portal | Package Manager | Create/edit screening packages with check type selection | Client Admin | Core Workflow |
| 12.2 | Role-based check bundles | Client Portal | Package Manager | Associate packages to job levels/roles | Client Admin | Core Workflow |
| 12.3 | Custom fields — add custom data fields and validations per client/BU/country [C-08] | Client Portal | 6.2.23 Custom Field Registry | Register client-specific data fields extending the case data model. Scoped per client/BU/country. Fields are searchable, exportable, API-queryable, and server-side validated. Appear in Form Builder palette, All Cases column selector, exports, API responses, and Ops Manual Case Creation. Max 50 fields per tenant. | Client Admin | Core Workflow — C-08 |
| 12.4 | Check depth configuration | Client Portal | Package Manager | Standard/Enhanced/Comprehensive per check | Client Admin | Core Workflow |
| 12.5 | Consent form customization | Client Portal | Form Builder | Country-specific consent form variants | Client Admin | Compliance-Critical |
| 12.6 | Branding configuration | Client Portal | Branding Config | Logo, domain, color, messages | Client Admin | Candidate-Experience |
| 12.7 | Role-based access control | All Portals | User Management (all portals) | Role assignment, permission matrix | All Admins | Compliance-Critical |
| 12.8 | Delegated access with expiry | Ops + Client Portal | Team Management | Temporary elevated access | Ops Admin, Client Admin | Audit-Critical |
| 12.9 | Audit views | Ops + Auditor Module | Audit Trail Viewer, Auditor Module | Immutable audit log access | Ops Compliance, Auditor | Compliance-Critical |
| 12.10 | Holiday list configuration | Client Portal | Holiday List Manager | Country/state holiday list for SLA calculation | Client Admin | SLA-Critical |
| 12.11 | Color code matrix | Client Portal | Color Code Matrix | Client-defined outcome color meanings | Client Admin | Core Workflow |
| 12.12 | Check type activation | Super Admin | Tenant Configuration | Enable/disable check types per tenant | Platform Admin | Core Workflow |

---

## 9.12 RFP SECTIONS 13–23 — CONDENSED TRACEABILITY

### Section 13 — Integration

| RFP Ref | Requirement | Portal | Page | Functionality | Classification |
|---|---|---|---|---|---|
| 13.1 | ATS/HRIS integration — native connectors, configurable field mapping, hybrid HRMS pre-fill [C-12 migration note] | Client Portal | 6.5.14 Integration Registry (6A HRMS Config + 6B API Case Creation) | Connector config, field mapping, trigger event, consent flag, two-way status sync. **Migration: Legacy SOAP clients (HRMS/SAP) supported via SOAP→REST adapter (Part 4.11) for 12 months post go-live, then decommissioned.** New HRMS integrations must use REST/webhook. SOAP client registry managed in 6.5.14 Section 6D. | Operational Enhancement — C-12 |
| 13.2 | REST API-first coverage — APIs for case create, update, status, documents, results, audit logs [C-12 migration note] | All portals | BFF API layer | REST APIs for all major operations. **Migration: Legacy SOAP API callers supported via SOAP→REST adapter (Part 4.11) for 12 months sunset period. Adapter exposes 3 operations only: InitiateBGV → POST /v1/cases, GetBGVStatus → GET /v1/cases?ref=, GetBGVResult → GET /v1/cases/{id}/result. No new capabilities via SOAP.** | Core Platform — C-12 |
| 13.3 | SSO/SAML support | Client Portal + Ops | User Management | SAML 2.0 / OAuth 2.0 SSO | Operational Enhancement |
| 13.4 | Webhook notifications | Client Portal + Super Admin | Integration Settings | Outbound webhooks on case events | Operational Enhancement |
| 13.5 | Pre-built ATS connectors | Client Portal | Integration Settings | Workday, SuccessFactors, Darwinbox connectors | Operational Enhancement |
| 13.6 | API key management | Client Portal + Super Admin | Integration Settings | API key generation, rotation, revocation | Audit-Critical |
| 13.7 | Sandbox/test environment | Client Portal + Super Admin | Integration Settings | Test mode for ATS integration | Operational Enhancement |
| 13.8 | Field mapping (custom) | Client Portal | Integration Settings | Map HRIS fields to KCheck fields | Core Workflow |
| 13.9 | Ticketing integration — ServiceNow/Jira for incidents and requests [C-06] | Ops Portal + Super Admin | 6.1.39 Case Workbench (Create Ticket action + Linked Tickets tab) + 6.5.14 Integration Registry (6C — Ticketing Connector Config) | Auto-create tickets from KCheck events (SLA breach, system error, vendor overdue); manual ticket creation from Case Workbench; bidirectional status sync (webhook/polling); escalation-to-ticket optional mapping | Operational Enhancement — C-06 |
| 13.10 | SFTP bulk data exchange | Super Admin | Integration Registry | Legacy SFTP connector for batch data | Operational Enhancement |

### Section 14 — Security

| RFP Ref | Requirement | Portal | Implementation | Classification |
|---|---|---|---|---|
| 14.1 | HTTPS/TLS 1.3 | All | Transport layer — all portals, all APIs | Core Platform |
| 14.2 | Encryption at rest | All | AES-256 for DB + object storage | Compliance-Critical |
| 14.3 | Encryption in transit | All | TLS 1.3 end-to-end | Compliance-Critical |
| 14.4 | MFA for all portals | All | TOTP/OTP second factor for ops, client, vendor portals | Core Platform |
| 14.5 | Session timeout | All | Configurable session expiry per portal | Core Platform |
| 14.6 | IP restriction (ops/admin) | Ops + Super Admin | VPN + IP allowlist for ops portal access | Compliance-Critical |
| 14.7 | Rate limiting | Candidate Portal (primary) | API gateway rate limiting — especially login/OTP | Core Platform |
| 14.8 | WAF | Candidate Portal | Web Application Firewall in front of public-facing portal | Core Platform |
| 14.9 | Penetration testing (annual) | All | External pen test requirement | Compliance-Critical |
| 14.10 | Tenant isolation | All | DB-level + BFF-level isolation | Compliance-Critical |
| 14.11 | RBAC | All | Two-layer RBAC (BFF + domain service) | Compliance-Critical |
| 14.12 | Immutable audit log | All | Append-only audit DB with hash chain | Compliance-Critical |
| 14.13 | Breach notification workflow | Super Admin | Incident Management | Compliance-Critical |

### Section 15 — Privacy / DPDP / GDPR

| RFP Ref | Requirement | Portal | Page | Classification |
|---|---|---|---|---|
| 15.1 | Consent capture | Candidate Portal | Consent Page | Compliance-Critical |
| 15.2 | Consent versioning | Candidate + Ops | Consent Page + Consent Audit | Compliance-Critical |
| 15.3 | Purpose-specific consent | Candidate Portal | Consent Page | Compliance-Critical |
| 15.4 | Data minimization | All | Dynamic forms + API data scope | Compliance-Critical |
| 15.5 | Configurable retention + auto-purge | Ops + Super Admin | Data Retention Manager | Compliance-Critical |
| 15.6 | Data access right (DSAR) | Ops + Candidate | DSAR Management + Dispute/Help page | Compliance-Critical |
| 15.7 | Data correction right | Ops + Candidate | DSAR Management + Dispute | Compliance-Critical |
| 15.8 | Data erasure right | Ops | DSAR Management (with legal hold check) | Compliance-Critical |
| 15.9 | Grievance redressal | Ops + Candidate | Dispute Workbench + Help page | Compliance-Critical |
| 15.10 | DPIA support | Super Admin | Compliance Documentation | Compliance-Critical |
| 15.11 | Cross-border transfer compliance | Super Admin | Data Residency Monitor | Compliance-Critical |

### Section 16 — Compliance / FCRA / Adverse Action

| RFP Ref | Requirement | Portal | Page | Classification |
|---|---|---|---|---|
| 16.1 | FCRA-style disclosure | Candidate Portal | Consent Page (separate section) | Compliance-Critical |
| 16.2 | Pre-adverse notice generation | Ops Portal | Adjudication Workbench | Compliance-Critical |
| 16.3 | Adverse action notice | Ops Portal | Adjudication Workbench | Compliance-Critical |
| 16.4 | Waiting period timer | Ops Portal | Adjudication Workbench | Compliance-Critical |
| 16.5 | Adjudication matrix (configurable) | Ops + Client Portal | Case Workbench + Adjudication Policy | Core Workflow |

### Section 17 — Data Governance

> **C-05: This section was previously mislabelled "Global Competency / Multi-Country" with Section 23 content assigned here.**
> **Corrected below. RFP Section 17 = "Data" — 7 explicit requirements, all now covered by pages 6.5.20–6.5.23.**

| RFP Ref | Requirement | Portal | Page | Functionality | Classification |
|---|---|---|---|---|---|
| 17.1 | Data catalog & inventory — maintain inventory of all collected data elements and sources | Super Admin | 6.5.20 Platform Data Catalog | Complete ROPA registry: field ID, source, purpose, legal basis, retention, pseudonymization rule per element. Export ROPA for DPA submission. | Compliance-Critical — C-05 |
| 17.2 | Source lineage — track lineage for each field (candidate/doc/db/employer) for audit | Super Admin | 6.5.22 Field Lineage & Evidence Linking | Per-field provenance chain from original entry through all verification sources to stored value. Timestamp, actor, source system per step. | Compliance-Critical — C-05 |
| 17.3 | Evidence linking — link verification outcomes to evidence artifacts and source references | Super Admin + Ops | 6.5.22 Field Lineage (Evidence Linking tab) + 6.1.39 Case Workbench (Evidence Table) | Outcome-to-evidence linkage: each adjudication outcome linked to specific document IDs and AI signal IDs reviewed. | Compliance-Critical — C-05 |
| 17.4 | Data quality rules — validation rules, required fields, plausibility checks | Super Admin | 6.5.23 Data Quality & Masking Rules (Tab 1) | Configurable field-level validation rules: required / format / range / plausibility / cross-field consistency. Severity: blocking or warning. Scope: per portal / check type / country / client. | Core Workflow — C-05 |
| 17.5 | Master data management — candidate identity master record with merge/split controls | Super Admin | 6.5.21 Candidate Identity Master | One canonical record per real-world candidate across all cases and clients. Merge/split deduplication controls. DSAR lookup anchor. Cross-case fraud detection. | Compliance-Critical — C-05 |
| 17.6 | Data anonymization — anonymize data after retention period while preserving statistics | Super Admin | 6.5.23 Data Quality & Masking Rules (Tab 3 — Anonymization Schedule) | Per-field-category anonymization rules: what is deleted vs preserved as aggregate after retention expiry. Ties to Data Retention Manager (9.4 Ops Portal). | Compliance-Critical — C-05 |
| 17.7 | Pseudonymization — support pseudonymization through masking to prevent direct identification | Super Admin | 6.5.23 Data Quality & Masking Rules (Tab 2 — Masking Matrix) | Per-field × per-role × per-portal masking: Full / Last 4 / Hashed / Tokenized / Not shown. Configurable without code change. Connects to RFP 14.11 (field masking by role). | Compliance-Critical — C-05 |

### Section 18 — Reporting

> **C-09: Multiple rows in this section had incorrect RFP attributions.**
> **8 of 10 rows have been corrected to match actual RFP 18.1–18.10 content.**

| RFP Ref | Requirement | Portal | Page | Functionality | Classification |
|---|---|---|---|---|---|
| 18.1 | Operational dashboards — pipeline, pending, SLA breach, productivity metrics | Ops + Client | 6.1.2 Ops Dashboard + 6.1.26 MIS/Analytics Dashboard | Case pipeline funnel, SLA compliance KPI, TAT heatmap, breach root-cause chart, discrepancy frequency. All data served from Reporting DB (C-09 / 4.8). | Core Workflow |
| 18.2 | Risk dashboards — risk score distribution, discrepancy types, fraud trends | Ops | 6.1.26 MIS Dashboard (Fraud Analytics tab) + Fraud Intelligence Dashboard (GAP-H1) | AI fraud flag trends, risk score distribution, top discrepancy types, fraud signal emergence. Reporting DB (4.8). | Core Workflow |
| 18.3 | Audit packs — candidate-wise audit pack (consent, checks, evidence, adjudication, notices) | Ops + Auditor Module | Audit Trail Viewer + Auditor Module (5.7) | Per-case audit pack: consent record, evidence list, adjudication outcome, pre-adverse/adverse notices. Tamper-evident hash manifest. | Audit-Critical |
| 18.4 | Export to Excel/CSV — configurable exports with role-based redaction | Ops + Client | Bulk Export (6.2.2) + GAP-EXP-L4 FIX (role-based redaction) | Column-selectable exports with redaction rules per role. Client Viewer gets redacted PII columns. Reporting DB (4.8). | Compliance-Critical |
| 18.5 | BI integration — connect to Power BI/Tableau via secure connectors [C-09] | Ops + Client | 6.1.26 MIS Dashboard (BI Export Config Drawer) + 6.5.14 Integration Registry (BI Connectors) | Two connector options: JDBC/ODBC read-only to Reporting DB (Option A) and REST API OAuth connector (Option B). Anonymised schema, tenant-scoped, no raw PII. Full design in 4.8.6. | Operational Enhancement — C-09 |
| 18.6 | KPI/KRI library — prebuilt KPIs (TAT, fallouts, disputes) and KRIs (fraud signals) | Ops | 6.1.25 Standard Operational Reports Library + 6.1.26 MIS Dashboard (KPI strip) | 10–15 prebuilt KPIs: avg TAT by check type, SLA compliance %, discrepancy rate, QC error rate, fraud flag rate. KRIs: fraud signal velocity, anomaly rate. Reporting DB (4.8). | Core Workflow |
| 18.7 | Trend analysis — cohort analysis by role, location, vendor, recruiter | Ops | 6.1.26 MIS Dashboard (TAT heatmap, breach trend, vendor comparison charts) | TAT heatmap by client × check type, SLA breach trend (12-week), vendor TAT comparison, candidate completion rate trend. Drilldown to case list per segment. Reporting DB (4.8). | Operational Enhancement |
| 18.8 | API usage analytics — monitor integration calls, failures, latency | Super Admin | 6.5.14 Integration Registry (API Usage Log tab) | Per-connector: call volume, error rate, latency p50/p95, rate limit hits. Time-series charts. Downloadable CSV log. Reporting DB (4.8). | Operational Enhancement |
| 18.9 | Color code tagging — visible at Quality Check level per color code matrix | Ops + Client | 6.2.13 Outcome Color Code Matrix + QC Sampling Queue (6.1.4/QC workspace) | Per-check outcome color badge driven by client's configured color matrix. Visible in case list, case detail, QC review, and reports. | Core Workflow |
| 18.10 | Billing Dashboard — configurable visibility into client invoicing and revenue analytics | Client + Super Admin | Client Billing Dashboard (6.2.8) + Platform Pricing & Billing Config (6.5.15) | Invoice list, per-check cost breakdown, volume slab progress, SLA penalty line items, revenue analytics (Super Admin view). GAP-EXP-FA1 FIX covers full billing dashboard design. | Core Workflow |

### Section 19 — Candidate Experience

| RFP Ref | Requirement | Portal | Implementation | Classification |
|---|---|---|---|---|
| 19.1 | Guided form flow | Candidate | Wizard progress indicator | Candidate-Experience |
| 19.2 | Real-time validation | Candidate | Inline field validation | Candidate-Experience |
| 19.3 | Auto-save | Candidate | Server-side state save | Candidate-Experience |
| 19.4 | Expected completion estimate | Candidate | Status page | Candidate-Experience |
| 19.5 | Support access | Candidate | Help & Support page | Candidate-Experience |
| 19.6 | Multi-language | Candidate | Language selector | Multi-Country |
| 19.7 | Mobile-optimized | Candidate | Responsive PWA | Candidate-Experience |
| 19.8 | Completion confirmation | Candidate | Submission confirmation screen | Candidate-Experience |
| 19.9 | Dispute access | Candidate | Raise a Concern page | Compliance-Critical |
| 19.10 | Configurable field tooltips | Candidate + Client | Form fields + Client admin tooltip config | Candidate-Experience |
| 19.11 | Accessibility (WCAG AA) | Candidate Portal | All pages | Candidate-Experience |

### Section 20 — Infrastructure & Reliability

| RFP Ref | Requirement | Portal | Implementation | Classification |
|---|---|---|---|---|
| 20.1 | 99.9% uptime SLA | All | HA deployment, blue-green deploy | Core Platform |
| 20.2 | Data residency | All | Per-tenant regional deployment | Compliance-Critical |
| 20.3 | Auto-scaling | Candidate Portal (primary) | Horizontal pod autoscaling | Core Platform |
| 20.4 | Disaster recovery (RPO/RTO) | All | Multi-AZ + geo-redundant backup | Core Platform |
| 20.5 | Performance targets (page load) | Candidate Portal | CDN + SSR optimization | Core Platform |
| 20.6 | Offline capability (field agent) | Field Agent App | PWA offline mode | Core Workflow |
| 20.7 | CI/CD pipeline | All | Automated build/test/deploy | Core Platform |
| 20.8 | Feature flags (canary) | Super Admin | Build & Release Management | Core Platform |

### Section 21 — Reliability & Observability

> **C-14: Five of seven rows in this section had incorrect RFP attributions.**
> **SLA-related content from other sections had been placed here incorrectly.**
> **Corrected below to match actual RFP 21.1–21.7 content.**

| RFP Ref | Requirement | Portal | Implementation | Classification |
|---|---|---|---|---|
| 21.1 | Reliability: Uptime SLA — define uptime SLA (99.9%+) and maintenance windows [C-04] | All Portals | HA deployment + Client Portal auto-scaling (4.5, 4.6). Client Portal peak: 700 concurrent sessions. Load test target: p95 < 2s on all core endpoints. | SLA-Critical — C-04 |
| 21.2 | Reliability: DR/BCP — disaster recovery RPO/RTO with periodic DR drills | All | Infra — multi-site or multi-AZ deployment (Phase 3). Phase 1 on-prem: secondary server + SQL Server Always-On or log shipping DR target. RPO target: < 1 hour. RTO target: < 4 hours. Periodic DR drills: minimum annual. | Core Platform |
| 21.3 | Observability: Central logging — centralized logs with correlation IDs for each case [C-14] | All Portals | Structured logging on all services with correlation_id (case_id + session_id + request_id). Logs shipped to central log aggregator (ELK / Azure Log Analytics / equivalent). Log retention: minimum 90 days hot, 1 year cold. Super Admin > System Health: log search by correlation_id. | Core Platform — C-14 |
| 21.4 | Metrics & tracing — latency, throughput, error rates; distributed tracing [C-14] | All Portals | OpenTelemetry (or equivalent) for distributed tracing across BFF → domain service → DB. Key metrics: API p50/p95/p99 latency, error rate, throughput per endpoint. Reporting DB CDC lag metric (4.8.3A) included as a platform metric. Alerting: p95 > SLA threshold → PagerDuty / Super Admin alert. Super Admin > System Health: live metric dashboard. | Core Platform — C-14 |
| 21.5 | Alerting — alerts for integration failures, SLA breaches, security anomalies [C-14] | All | Alerting for: integration API failures (6.5.14 health monitor), CDC lag spikes (4.8.3A), SLA breach events (6.1.40 SLA Dashboard), security anomalies (6.5.11 Incident Response), SOAP adapter errors (4.11). Alert channels: Super Admin in-app + email + optional PagerDuty webhook. Alert rules configurable in Super Admin > System Health. | Core Platform — C-14 |
| 21.6 | Load testing — validated performance for peak hiring volumes [C-04] | All Portals | Client Portal target: 700 concurrent sessions, p95 < 2s on case-list + status + report-inbox. Candidate Portal target: 600–700 daily unique users, < 3s document upload response. Load test suite: k6 / JMeter / Locust against staging environment before each major release. See 4.5, 4.6. | Core Platform — C-04 |
| 21.7 | Application level logging — for troubleshooting and ensuring uptime [C-14] | All | Application-level debug and info logs per service — separate from audit logs (immutable, compliance) and access logs (security). Includes: slow query logs (DB queries > 500ms), job queue backlogs, background job failures, CDC processor events (4.8.3A). Retention: 30 days hot. Accessible to Platform Admin in Super Admin > System Health > Application Logs. Not exposed to Ops Portal or Client Portal. | Core Platform — C-14 |

### Section 22 — Commercial / Billing

| RFP Ref | Requirement | Portal | Page | Classification |
|---|---|---|---|---|
| 22.1 | Invoice generation | Super Admin + Client | Billing Config + Billing Dashboard | Core Workflow |
| 22.2 | SLA penalty calculation | Super Admin | Billing Config + SLA engine | SLA-Critical |
| 22.3 | Subprocessor disclosure — list of subprocessors and change notification policy | Super Admin | 6.5.14 Integration Registry (Subprocessor Register tab) | Compliance-Critical |
| 22.4 | Right to audit — customer right to audit vendor controls and evidence [C-11] | Client Portal | 6.2.24 Client Audit Evidence Request | Formal audit evidence request wizard (per-case / process controls / compliance docs). ServiceNow integration (C-06). Time-limited secure download. Immutable request audit log. | Compliance-Critical — C-11 |
| 22.5 | Data portability — full export on exit with defined format and timelines | Ops + Client | DSAR Export (6.5.21 Candidate Identity Master) + Client case bulk export (6.2.2) | Compliance-Critical |
| 22.6 | Exit assistance — transition support and secure deletion confirmation | Ops + Super Admin | Tenant Offboarding (6.5.4 All Tenants Registry — Offboard action) | Compliance-Critical |

### Section 23 — Compliance & Regulatory (Global)

| RFP Ref | Requirement | Portal | Implementation | Classification |
|---|---|---|---|---|
| 23.1 | DPDP compliance | All | Consent, DSAR, retention, audit | Compliance-Critical |
| 23.2 | GDPR compliance (EU candidates) | All | Data residency, consent, DSAR, audit | Compliance-Critical |
| 23.3 | FCRA-equivalent compliance | Candidate + Ops | Consent, pre-adverse, adverse notice | Compliance-Critical |
| 23.4 | Localization framework — language, date, address formats, currencies, and document standards per country [C-10] | Candidate Portal (primary) + All portals (format rules) | Part 4.10 (scope boundary) + 6.3.6 Invitation Landing Page (RTL) + 6.3.7–6.3.10 Candidate form pages | Locale-specific date formats (DD/MM/YYYY vs Jan 14 1992 vs ١٤ يناير ١٩٩٢), number formats (1,00,000 Indian vs 1.000.000 EU), currency symbols, address field ordering. RTL layout for Arabic. Supported locales: en-IN, hi-IN, ta-IN, te-IN, kn-IN, ar-AE, fr-FR, de-DE. | Language selector + locale-aware formatters (Intl.DateTimeFormat, Intl.NumberFormat) | GET /v1/i18n/{locale}/strings | N/A | Candidate | Multi-country BGV requires locale-correct date/number presentation | Date format errors cause DOB mismatches — compliance impact | Multi-Country — C-10 |
| 23.5 | SOC 2 Type II | All | Security, availability, confidentiality controls | Compliance-Critical |
| 23.6 | PMLA/AML compliance | Ops | Legal + Financial check workspaces | Compliance-Critical |
| 23.7 | UIDAI Aadhaar usage compliance | Ops | KYC Workspace | Compliance-Critical |
| 23.8 | RBI guidelines (financial checks) | Ops | Financial Workspace | Compliance-Critical |
| 23.9 | SEBI compliance (regulatory checks) | Ops | Legal Workspace | Compliance-Critical |
| 23.10 | FATF/PEP guidelines | Ops | Legal Workspace — sanctions screening | Compliance-Critical |
| 23.19 | Breach notification timelines | Super Admin | Incident Management | Compliance-Critical |

---

## 9.13 Final Gap Analysis Matrix

### Missing from RFP — Operationally Required

| Gap | Why Needed | Risk if Absent | Recommended Solution |
|---|---|---|---|
| Notification delivery failure ops dashboard | 600+/day volume means failures are daily events; silent failure = SLA breach | Silent TAT extension; SLA breach attribution errors | Real-time delivery failure counter + case-level SLA pause in ops dashboard |
| Tokenized employer/university/referee response modules | RFP implies digital outreach but doesn't spec the response interface | Email/manual stays — TAT impact 3–5 days per check | Lightweight tokenized web forms (Part 5.7) |
| Field agent device attestation (anti-GPS spoofing) | RFP requires GPS evidence but not anti-spoofing | GPS fraud risk; address verification compromised | Google Play Integrity + DeviceCheck + server-side teleportation detection |
| AI model version pinning per case | Model retraining mid-case changes how same evidence is evaluated | Inconsistent adjudication; audit challenge | Pin model version at case creation; re-evaluate only with explicit ops action |
| Cross-tenant pseudonymized identity index | Same fraudulent candidate across two clients is undetected | Organized fraud ring passes BGV at multiple KPMG clients | Hash-only cross-tenant identity index (PAN hash, Aadhaar hash) with flag to ops |
| Candidate notification for final completion | Candidate has no way to know BGV is done unless employer tells them | Poor candidate experience; support burden | Automated completion notification (Email + WhatsApp) on report delivery |
| SLA penalty calculation unit test suite | SLA with pauses + holidays + multi-timezone is complex | Wrong SLA outcomes; billing disputes | Standalone tested SLA calculation module with 50+ edge case tests |

### Mentioned in Workflow but Absent in RFP

| Item | Workflow Reference | Note |
|---|---|---|
| Session expiry + server-side auto-save | Module 1 Section 1.3 | Implied by mobile-first but not specified — implement as must-have |
| Multi-channel notification fallback chain spec | Module 1 Section 1.4 | Fallback order and timing not specified — needs SLA agreement with client |
| Candidate support SLA | Module 1 Section 1.5 | Support responsiveness not specified — operational necessity |
| AI model retraining feedback loop | Workflow AI section | False positives fed back to model — critical for long-term accuracy |
| Legal hold on DSAR erasure | Workflow compliance section | Cannot erase data involved in active dispute or litigation — needs legal hold flag |

### Potential Overengineering Areas

| Item | Risk | Recommendation |
|---|---|---|
| Custom MLOps platform | 6+ month build for marginal improvement over third-party AI vendors | Use vetted AI vendor APIs (face match, OCR, liveness) — no custom ML training |
| Blockchain audit logs | Operational complexity; no regulatory requirement beyond immutability | Append-only DB + hash chain is sufficient and auditable |
| Full event-driven microservices from day one | Excessive decomposition before team experience established | State machine in DB + async job queues is sufficient; evolve to event streaming if scale demands |
| Real-time collab features (multiple ops on same case) | Adds WebSocket complexity; ops cases are not collaborative by workflow | Pessimistic locking on case (one reviewer at a time) is sufficient and simpler |
| Subscription billing engine | RFP only needs invoice visibility and penalty calculation | Lightweight billing module with invoice PDF generation; no e-commerce engine |

---


---

# PART 10 — EXPLICIT GAP RESOLUTION SUMMARY (RFP TRACEABILITY)

> This section provides a consolidated registry of all explicit gaps identified in the KCheck BGV Platform — Validation Report and verified against BGV_RFP_24_Apr_26.xlsx. All items in this registry are classified as EXPLICIT per the KCheck_Gap_RFP_Validation.md source of truth. All 23 explicit gaps have been addressed with design depth additions or new page specifications in this document.

## 10.1 Consolidated Explicit Gap Register

| Gap ID | Gap Title | Severity | RFP Reference | Portal | Resolution Location | Status |
|---|---|---|---|---|---|---|
| C-1 | Vendor Revalidation Queue | Critical | RFP 10.19 | Ops + Vendor | GAP-19 FIX (§6.4.9) | ✅ Resolved |
| C-3 | Pre-Adverse Waiting Period UI Enforcement | Critical | RFP 10.11, 16.1 | Ops | GAP-EXP-C3 FIX (§6.1.16 addition) | ✅ Resolved |
| C-4 | Client Billing Dashboard — Underspecified | Critical | RFP 18.10, 22.1, 22.2 | Client, Super Admin | GAP-EXP-C4 FIX (§6.2.18 full depth) | ✅ Resolved |
| C-5 | Three-Track SLA Timers + Default Values | Critical | RFP 1.7, 23.14 | Ops + Super Admin | GAP-2 FIX (§6.1.40) + C-03 (§6.1.27 + §6.5.1 Step 6) | ✅ Resolved |
| C-6 | Right-to-Correction Workflow Page | Critical | RFP 15.7 | Candidate + Ops | GAP-EXP-C6 FIX (§6.3.16 + §6.1.34 addition) | ✅ Resolved |
| H-1 | Fraud Intelligence Dashboard | High | RFP 2.24 | Ops | GAP-EXP-H1 FIX (§6.1.27A new page) | ✅ Resolved |
| H-2 | AI Governance Pages — Zero Design Depth | High | RFP 2.11, 2.16, 2.17 | Super Admin | §6.5.2, §6.5.7–6.5.9 (existing depth) | ✅ Resolved |
| H-3 | Continuous Monitoring Dashboard | High | RFP 9.1–9.4 | Ops | GAP-28 FIX (§6.1.39–6.1.41 new pages) | ✅ Resolved |
| H-4 | Client Exit Workflow | High | RFP 22.5, 22.6 | Client + Super Admin | GAP-14 FIX (§6.2.21 new page) | ✅ Resolved |
| H-7 | Field Agent Mobile App — Zero Design Depth | High | RFP 7.2–7.5 | Field Agent App | §6.6.1–6.6.5 (full design depth) | ✅ Resolved |
| H-8 | Subprocessor Register — Client Portal | High | RFP 22.3 | Client | GAP-13 FIX (§6.2.20 new page) | ✅ Resolved |
| H-10 | Client-Side Waiver Approval Workbench | High | RFP 10.7 | Client | GAP-EXP-H10 FIX (§6.2.6A new page) | ✅ Resolved |
| M-1 | Candidate Rights Information Page | Medium | RFP 11.12 | Candidate | GAP-EXP-M1 FIX (§6.3.17 new page) | ✅ Resolved |
| M-2 | Video KYC Scheduling Page | Medium | RFP 3.5 | Candidate + Ops | GAP-EXP-M2 FIX (§6.3.15A addition + §6.1.10A panel) | ✅ Resolved |
| M-3 | Consent Renewal Page | Medium | RFP 15.1 | Candidate | GAP-EXP-M3 FIX (§6.3.18 new page) | ✅ Resolved |
| M-4 | Country Management Page | Medium | RFP 23.2, 23.20 | Super Admin | GAP-23 FIX (§6.5.17–6.5.18 new pages) | ✅ Resolved |
| M-5 | Regulatory Change Management Page | Medium | RFP 23.16 | Super Admin | GAP-EXP-M5 FIX (§6.5.19 new page) | ✅ Resolved |
| M-7 | Contractor/Gig Employment Fields | Medium | RFP 4.9 | Candidate + Ops | GAP-EXP-M7 FIX (§6.3.2 addition) | ✅ Resolved |
| M-8 | Cross-Entity Navigation (Hyperlinked) | Medium | RFP 19.11 | All Portals | GAP-EXP-M8 FIX (§6.1.39 + §6.2.3 addition) | ✅ Resolved |
| M-9 | Admin Activity Log Viewer Design Depth | Medium | RFP 12.10 | Super Admin | GAP-EXP-M9 FIX (§6.5.10 supplement) | ✅ Resolved |
| L-3 | QC Color Matrix Reference Panel | Low | RFP 18.9 | Ops | GAP-7 FIX (§6.1.41 QC addition) | ✅ Resolved |
| L-4 | Bulk Export Role-Based Redaction | Low | RFP 18.4 | Client | GAP-EXP-L4 FIX (§6.2.2 + §6.2.8 addition) | ✅ Resolved |
| L-5 | Jurisdiction-Specific Dispute Notice | Low | RFP 23.15 | Candidate | GAP-EXP-L5 FIX (§6.3.13 addition) | ✅ Resolved |

## 10.2 Explicit Missing Actions — Resolution Register

| Action | Portal / Page | RFP Reference | Resolution Location | Status |
|---|---|---|---|---|
| 'Conditional Offer Extended' trigger (ban-the-box gate) | Client Portal — Case Detail | RFP 6.8 | GAP-EXP-FA1 FIX (§6.2.3 addition) | ✅ Resolved |
| 'Request Consent Renewal' action | Ops Portal — Case Workbench | RFP 15.1 | GAP-EXP-FA2 FIX (§6.1.39 addition) | ✅ Resolved |
| 'Withdraw Consent' action (Candidate Portal) | Candidate Portal | RFP 15.1 | GAP-18 FIX (§6.3.1 addition) | ✅ Resolved |
| 'Process Right-to-Correction' action | Ops Portal — DSAR Management | RFP 15.7 | GAP-EXP-C6 FIX (§6.1.34 addition) | ✅ Resolved |
| 'Initiate Vendor Revalidation' action | Ops Portal — Vendor Assignment Console | RFP 10.19 | GAP-19 FIX (§6.4.9) | ✅ Resolved |
| 'Generate Deletion Certificate' action | Super Admin — Tenant Management | RFP 22.6 | GAP-14 FIX (§6.2.21) | ✅ Resolved |
| 'Add New Country' workflow trigger | Super Admin — Configuration | RFP 23.2, 23.20 | GAP-23 FIX (§6.5.17–6.5.18) | ✅ Resolved |
| 'Publish / Acknowledge Adverse Action' | Client Portal — Case Detail | RFP 10.11 | GAP-EXP-FA3 FIX (§6.2.3 addition) | ✅ Resolved |

## 10.3 Explicit Missing Fields — Resolution Register

| Missing Field | Portal / Page | RFP Reference | Resolution Location | Status |
|---|---|---|---|---|
| Rehire Eligibility (structured 5-value field) | Ops Portal — Employment Workspace | RFP 4.11 | GAP-EXP-FF1 FIX (§6.1.8 addition) | ✅ Resolved |
| Contractor / Gig employment fields | Candidate Portal — Employment Form | RFP 4.9 | GAP-EXP-M7 FIX (§6.3.2 addition) | ✅ Resolved |
| Transcript verification result fields | Ops Portal — Education Workspace | RFP 5.5 | GAP-EXP-FF2 FIX (§6.1.9 addition) | ✅ Resolved |
| Three-track SLA timers (Client/Internal/Vendor) | Ops Portal — Case Workbench | RFP 1.7 | GAP-2 FIX (§6.1.40 addition) | ✅ Resolved |

## 10.4 Gaps Excluded from This Document (Non-Explicit)

The following gaps were identified in the Validation Report but are classified as IMPLICIT, PARTIALLY IMPLICIT, or NOT IN RFP by the KCheck_Gap_RFP_Validation.md source of truth. They are not added to this document per the governing editorial rule (only EXPLICIT gaps added):

| Gap ID | Gap Title | Classification | Reason Excluded |
|---|---|---|---|
| C-2 | Fraud Investigation Workspace | IMPLICIT | Freeze mechanism is internal design; RFP 2.24 + 10.9 only imply it |
| H-5 | Breach Countdown Timer (72h) | IMPLICIT | Timer is GDPR Art. 33 consequence; not named in RFP directly |
| H-6 | Vendor DPA Status Page | IMPLICIT | Subprocessor disclosure (RFP 22.3) is explicit; DPA page is an implementation consequence |
| H-9 | Smart Routing Test Mode | IMPLICIT | Test mode implied by RFP 12.2 rule engine; not explicitly named |
| M-6 | Candidate BGV Report View | IMPLICIT | Status tracking (RFP 11.6) is explicit; completed report view is implied |
| M-10 | Role Risk Tier Display (Tier 1-5) | IMPLICIT | Tier 1-5 taxonomy is internal design; RFP 6.7 mandates differentiation but not the tier system |
| L-1 | HRMS Pre-fill Conflict Resolution | IMPLICIT | Pre-fill (RFP 13.1) is explicit; conflict resolution UI is an implementation consequence |
| L-2 | Vendor Scorecard Page | IMPLICIT | Scorecard metrics and trend charts are internal design; RFP 10.19 implies but does not name |
| L-6 | Holiday List Excel Import | IMPLICIT | Holiday configuration (RFP 12.12) is explicit; import mechanism is not named |

---

*KCheck BGV Platform — Enterprise Architecture Review v5 with Explicit Gap Resolutions*
*Gap Source: KCheck_Gap_RFP_Validation.md | KCheck_Validation_Report.md | BGV_RFP_24_Apr_26.xlsx*
*All EXPLICIT gaps (23 of 32 total) resolved in this document. 9 IMPLICIT gaps excluded per editorial policy.*


*End of Expanded Parts 5, 6, 8, and 9 — KCheck BGV Platform Enterprise Architecture Review*
*Document Version: 2.0 — Expanded*
