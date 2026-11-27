# HIPAA (US health data) — Engineering Checklist

> Not legal advice. Applies to covered entities and business associates handling Protected Health Information (PHI).

## Before writing code
- [ ] Determine whether you are a covered entity or business associate. Sign **BAAs** with every vendor that touches PHI (cloud, DB, email, LLM provider, logging, analytics)
- [ ] Use only HIPAA-eligible services and configure them as the BAA requires

## Security Rule — technical safeguards (45 CFR §164.312)
- [ ] **Access control**: unique user IDs, emergency access procedure, automatic logoff, encryption/decryption
- [ ] **Audit controls**: record and examine activity in systems containing ePHI
- [ ] **Integrity**: protect ePHI from improper alteration/destruction (checksums, immutability, backups)
- [ ] **Person/entity authentication**: MFA strongly recommended
- [ ] **Transmission security**: TLS 1.2+ everywhere, including internal traffic

## Administrative & physical safeguards
- [ ] Documented risk analysis and risk-management plan (§164.308(a)(1))
- [ ] Workforce training, sanctions policy, security officer named
- [ ] Contingency plan: backups, disaster recovery, emergency mode
- [ ] Device and media controls

## Privacy & breach
- [ ] Minimum necessary use/disclosure
- [ ] Patient rights: access, amendment, accounting of disclosures
- [ ] Breach notification: individuals without unreasonable delay (≤ 60 days); HHS; media if 500+ in a state

## Engineering gotchas
- [ ] No PHI in logs, URLs, analytics, error trackers or push notifications
- [ ] No PHI sent to AI/LLM APIs without a BAA and zero-retention configuration
- [ ] Tracking pixels on authenticated patient pages can count as impermissible disclosures. Review HHS guidance
