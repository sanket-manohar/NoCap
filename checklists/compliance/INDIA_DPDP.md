# India — Digital Personal Data Protection Act 2023 + DPDP Rules 2025

> Not legal advice. The DPDP Rules 2025 were notified on **13/14 November 2025** with a phased rollout of up to
> **18 months**. The Data Protection Board provisions took effect first. Consent-manager provisions apply from **November 2026**,
> and most substantive obligations (notice, security safeguards, breach intimation, retention, data-principal rights,
> Significant Data Fiduciary duties) apply from **May 2027**. Check the official MeitY notifications for exact dates.

Applies to processing of **digital personal data** within India, and outside India when offering goods or services to people in India.

| ✓ | Obligation | Engineering evidence |
|---|---|---|
| [ ] | **Notice**: clear, standalone, itemised notice of the data collected and its purpose, in plain language (English or a language from the Eighth Schedule) | Consent screen copy + notice versioning |
| [ ] | **Consent**: free, specific, informed, unconditional, unambiguous, clear affirmative action; limited to necessary data | Consent ledger (purpose, timestamp, notice version) |
| [ ] | **Withdrawal** as easy as giving consent; processing stops within a reasonable time | Withdraw button + propagation to processors |
| [ ] | **Consent Managers** (registered with the Board) supported where relevant | Integration plan |
| [ ] | **Legitimate uses** documented where consent is not the basis | Data inventory |
| [ ] | **Purpose limitation & erasure** once the purpose is served or consent is withdrawn (Rules set retention periods and advance notice before erasure for certain classes) | Retention jobs + pre-deletion notice email |
| [ ] | **Reasonable security safeguards**: encryption/obfuscation/masking, access control, logging & monitoring, backups, logs retained for at least 1 year (per Rules) | `docs/SECURITY.md`, log retention config |
| [ ] | **Breach intimation** to the Data Protection Board and every affected Data Principal, without delay; detailed report to the Board (Rules: within 72 hours, unless extended) | `docs/RUNBOOK.md` |
| [ ] | **Data Principal rights**: access summary, correction, completion, update, erasure, grievance redressal, nominate a representative | Self-service endpoints + grievance contact |
| [ ] | **Grievance redressal** within a prescribed period (Rules: up to 90 days) with a published contact | Support workflow |
| [ ] | **Children (< 18)**: verifiable parental consent; no tracking, behavioural monitoring or targeted ads to children | Age gate + parent verification (e.g. DigiLocker / existing verified identity) |
| [ ] | **Persons with disabilities**: consent from the lawful guardian | Guardian flow |
| [ ] | **Processors** only under a valid contract; the Fiduciary remains responsible | Vendor DPAs |
| [ ] | **Cross-border transfer** allowed except to countries restricted by the Government; follow any requirements notified | Region map |
| [ ] | **Significant Data Fiduciary** (if notified): DPO in India, independent data auditor, annual DPIA + audit, algorithmic due diligence | Governance docs |

Penalties under the Schedule go up to **₹250 crore** for failing to take reasonable security safeguards.
