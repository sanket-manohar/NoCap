# 04 · `nocap compliance <framework>` — Compliance gap analysis

Output: `docs/COMPLIANCE.md` (template: `templates/COMPLIANCE.md`).

> ⚖️ Always state: *"This is an engineering gap analysis, not legal advice. Confirm obligations with a
> qualified lawyer or auditor."*

## Step 1 — Applicability (do this even if the user named a framework)
Decide from the code and the user's answers:

| Signal in the product | Framework(s) to check | Checklist |
|---|---|---|
| Any personal data of people in the EU/EEA/UK | GDPR / UK GDPR | `checklists/compliance/GDPR.md` |
| Digital personal data of people in India, or offering services to them | DPDP Act 2023 + DPDP Rules 2025 | `checklists/compliance/INDIA_DPDP.md` |
| California consumers (thresholds apply) | CCPA/CPRA | `checklists/compliance/CCPA_CPRA.md` |
| US protected health information (covered entity or business associate) | HIPAA | `checklists/compliance/HIPAA.md` |
| Stores, processes or transmits card data, or can affect its security | PCI DSS v4.0.1 | `checklists/compliance/PCI_DSS_4.md` |
| B2B SaaS selling to companies | SOC 2 (TSC 2017, rev. points of focus 2022) | `checklists/compliance/SOC2.md` |
| Enterprise / international customers asking for an ISMS | ISO/IEC 27001:2022 | `checklists/compliance/ISO27001_2022.md` |
| Any public-facing UI (and legally required in many places, e.g. the European Accessibility Act) | WCAG 2.2 AA | `checklists/compliance/WCAG_2_2_ACCESSIBILITY.md` |
| AI system placed on the EU market or used in the EU | EU AI Act | `checklists/compliance/EU_AI_ACT.md` |
| Children's data | COPPA (US), GDPR Art. 8, DPDP verifiable parental consent | in GDPR/DPDP checklists |

Ask the user only for facts the code can't reveal: where users are located, company size, whether card data
touches their servers, whether they are a HIPAA covered entity or business associate.

## Step 2 — Gap analysis
For each applicable framework, fill a table: **Requirement · Where in the law/standard · Status (✅ Met / ⚠️ Partial / ❌ Gap / N/A)
· Evidence (file path, config, doc) · Gap · Engineering fix · Owner**.

Map technical controls to code: consent capture, data export/delete endpoints, retention jobs, encryption,
access logs, breach detection, processor list, cookie banner behaviour, age gating, accessibility of components.

## Step 3 — Deliverables
- Gap table per framework, sorted by risk.
- A **data inventory** (what, why, where stored, retention, shared with) if one is missing. This is the foundation of every privacy law.
- Draft policy snippets the team still needs a lawyer to review: privacy notice sections, cookie notice, DPA checklist, breach-notification runbook.
- A 30/60/90-day compliance roadmap.
