# 11 · `nocap ship` — Production readiness gate

Run every check below and output a **GO / NO-GO** decision with reasons.

| Gate | Pass condition |
|---|---|
| 🔐 Security | 0 Critical, 0 High open (or formally risk-accepted in `docs/SECURITY.md`) |
| 🔑 Secrets | No secrets in code or history; all prod secrets in a manager; leaked keys rotated |
| 🧱 Access control | Authz matrix documented; negative tests exist for every role/resource pair |
| 🗄️ Data | Backups automated **and a restore tested**; migrations reversible; RLS/rules on |
| 🌐 Web hardening | HTTPS + HSTS, CSP, cookie flags, CORS allow-list, rate limits on auth & AI routes |
| 📦 Supply chain | Lockfile committed; no known critical CVEs; Dependabot/Renovate on |
| 🔭 Observability | Error tracking, structured logs (no PII), uptime check, alerting to a human |
| 🚨 Incident ready | `RUNBOOK.md` with on-call contact, breach-notification steps, rollback steps |
| ⚖️ Compliance | Applicable frameworks identified; privacy policy & terms live; consent flows work |
| ♿ Accessibility | Key flows pass WCAG 2.2 AA basics (keyboard, contrast, labels, focus) |
| 🧪 Quality | CI green; tests cover core flows; no debug flags in prod config |
| 📚 Docs | NoCap docs score ≥ 80 |
| 💸 Cost guardrails | Billing alerts; per-user limits on paid APIs (LLM, SMS, email) |

Output the table with ✅/❌ and evidence, the blockers list, and the final verdict.
