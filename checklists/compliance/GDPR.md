# GDPR / UK GDPR — Engineering Checklist

> Not legal advice. Applies when you process personal data of people in the EU/EEA (and UK GDPR for the UK).

| ✓ | Requirement | Article | Engineering evidence |
|---|---|---|---|
| [ ] | Lawful basis recorded for each processing purpose | Art. 6 | `docs/PRIVACY.md` data inventory |
| [ ] | Valid consent: freely given, specific, informed, unambiguous; as easy to withdraw as to give; recorded | Art. 7 | Consent table (user, purpose, version, timestamp) and a withdraw endpoint |
| [ ] | Children: parental consent below the national age (13–16) | Art. 8 | Age gate + parental flow |
| [ ] | Transparent privacy notice | Art. 12–14 | Public privacy page linked at data collection |
| [ ] | Right of access / data portability (machine-readable export) | Art. 15, 20 | `/account/export` → JSON |
| [ ] | Right to rectification | Art. 16 | Profile edit |
| [ ] | Right to erasure | Art. 17 | Delete-account flow including backups policy and processors |
| [ ] | Right to object / restrict processing (incl. direct marketing) | Art. 18, 21 | Preference centre |
| [ ] | Safeguards for automated decision-making with legal effects | Art. 22 | Human review path |
| [ ] | Privacy by design & default | Art. 25 | Minimal fields, private-by-default settings |
| [ ] | Processor contracts (DPAs) with every vendor | Art. 28 | Sub-processor list |
| [ ] | Records of processing activities | Art. 30 | Data inventory |
| [ ] | Security of processing (encryption, pseudonymisation, resilience, testing) | Art. 32 | `docs/SECURITY.md`, audit results |
| [ ] | Breach notification to authority ≤ 72 h; to individuals if high risk | Art. 33–34 | `docs/RUNBOOK.md` breach procedure |
| [ ] | DPIA for high-risk processing (large-scale sensitive data, profiling, monitoring) | Art. 35 | DPIA document |
| [ ] | DPO appointed if required | Art. 37 | Contact in privacy notice |
| [ ] | International transfers: adequacy / SCCs / EU-US DPF | Ch. V | Vendor region list |
| [ ] | Cookies & trackers: prior opt-in consent for non-essential (ePrivacy) | ePrivacy Dir. | No analytics/ads before consent. "Reject all" as prominent as "Accept" |

**Engineering patterns:** a PII column tagger in the data model, retention cron jobs, soft delete → hard delete pipeline, log redaction, a consent ledger.
