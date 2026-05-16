"""
Verification domain — check execution per check type.

Check types covered (CLAUDE.md Part 5.1, Section 3):
    - Employment (incl. EPFO/UAN, employer outreach)
    - Education (incl. DigiLocker, university outreach)
    - Identity / KYC (Aadhaar, PAN, Passport, DL, biometrics)
    - Legal / Criminal (court records, sanctions, PEP)
    - Address (digital + field visit — see Site Visit sub-component)
    - Financial (credit bureau, insolvency, AML)
    - Reference

Each check has its own outcome, evidence references, and SLA timers
relative to the parent case.

Models intentionally not implemented yet — scaffolding only.
"""
from django.db import models  # noqa: F401
