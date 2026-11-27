# SOC 2 — Engineering Readiness Checklist

> SOC 2 is an attestation by a CPA firm against the AICPA **Trust Services Criteria** (Security = Common Criteria CC1–CC9, plus optional
> Availability, Processing Integrity, Confidentiality, Privacy). Type I = design at a point in time. Type II = operating effectiveness over a period (usually 3–12 months).

| Area (CC) | What auditors look for | Evidence to automate |
|---|---|---|
| CC1 Control environment | Policies, org chart, background checks, security training | Policy repo, HR system exports |
| CC2 Communication | Security policies communicated; customer-facing security page | Trust page, onboarding records |
| CC3 Risk assessment | Annual risk assessment, fraud risk, vendor risk | Risk register |
| CC4 Monitoring | Internal control reviews, vulnerability scans, pen tests | Scanner reports, pen-test letter |
| CC5 Control activities | Documented controls mapped to risks | Control matrix |
| CC6 Logical & physical access | SSO + MFA, least privilege, quarterly access reviews, offboarding within 24 h, encryption | IdP logs, access review tickets |
| CC7 System operations | Logging, alerting, incident response, vulnerability management | SIEM alerts, incident tickets, RUNBOOK |
| CC8 Change management | PR reviews, CI tests, separation of duties, approved deploys | Branch protection, PR history |
| CC9 Risk mitigation | Vendor management, BCP/DR, insurance | Vendor list with SOC reports, DR test results |

**Fast path for startups:** a compliance automation platform (Vanta, Drata, Secureframe, Sprinto, etc.) plus these NoCap docs as the system description.
