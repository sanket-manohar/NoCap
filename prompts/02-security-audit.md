# 02 · `nocap audit` — Security audit

**Goal:** find real, exploitable weaknesses and give the **standard, correct fix** for this exact stack.
Output: `docs/SECURITY_AUDIT.md` (template: `templates/SECURITY_AUDIT.md`).

## Step 1 — Automated baseline
If you can run commands:
```bash
python3 .nocap/scanner/nocap.py . --json .nocap-results.json
# Optional, if available locally:
osv-scanner scan source -r .     # dependency CVEs (all ecosystems)
gitleaks detect                  # secrets in git history
semgrep --config auto            # deeper SAST
```
Triage each scanner finding as **true positive / false positive (with reason)**. Don't copy scanner output blindly.

## Step 2 — Manual review (what scanners miss)
Work through these in order. Load the checklists recommended for the detected stack:

1. **Attack surface map.** List every entry point: routes, server actions, GraphQL resolvers, RPC, webhooks,
   cron jobs, queue consumers, file uploads, admin panels, LLM tools. Note the auth requirement of each.
2. **Authorisation matrix.** For each entry point: who may call it, and which records they may touch. Then
   read the code and confirm that it enforces exactly that. Look hard for IDOR/BOLA, i.e. IDs taken from the request
   and used without an ownership check.
3. **Authentication flows.** Signup, login, logout, reset, MFA, OAuth callback (`state`, PKCE, redirect URI
   validation), session lifetime, and account enumeration.
4. **Data flow of sensitive data.** Trace PII, credentials and payment data from input → storage → logs → third parties.
5. **Business logic abuse.** Price/quantity tampering, coupon reuse, race conditions (double spend), workflow-step
   skipping, unlimited free-tier use, unbounded AI spend.
6. **Injection sinks.** SQL/NoSQL, shell, path, template, HTML/JS, LDAP, XPath, header/CRLF, log injection, prompt injection.
7. **Client-side exposure.** Secrets in bundles, source maps in prod, sensitive logic only in the frontend, data over-fetching.
8. **Configuration.** CORS, CSP and other headers, cookies, debug flags, error pages, default credentials, exposed admin/docs/metrics endpoints.
9. **Supply chain.** Lockfiles, typosquatted or non-existent packages, abandoned packages, install scripts, unpinned CI actions.
10. **Infrastructure.** Containers, IaC, cloud IAM, network exposure, backups, logging/alerting.
11. **AI/LLM** (if present). Work through the full OWASP LLM Top 10 2025 checklist.

Checklists: `checklists/security/OWASP_TOP10_2025.md`, `OWASP_API_TOP10_2023.md`, `OWASP_LLM_TOP10_2025.md`,
`VIBE_CODING_TOP25.md`, `ASVS_ESSENTIALS.md`, plus `checklists/languages/<lang>.md` and `checklists/platforms/<platform>.md`.

## Step 3 — Write findings
Each finding:
```
### VP-<NNN> <Title>
Severity: Critical | High | Medium | Low      Confidence: Confirmed | Likely | Needs verification
Location: path/to/file.ext:LINE (and others)
CWE: CWE-xxx     OWASP: A0x:2025 … / APIx:2023 … / LLMxx:2025 …
Evidence: <minimal code excerpt — never paste real secrets>
Impact: <what an attacker can do, concretely>
Attack scenario: <1–3 steps>
Standard fix: <explanation referencing the framework's built-in mechanism>
<corrected code snippet for THIS stack>
Verify: <test or manual step that proves it is fixed>
```
Rate severity by **exploitability × impact**. Don't inflate it. A missing header is not critical, and a public admin endpoint is.

## Step 4 — Summary & plan
- Executive summary in at most 5 lines, written for a non-technical founder.
- Table of findings by severity and OWASP category.
- Fix plan: **Today** (critical) / **This week** (high) / **This month** (medium) / **Backlog**.
- The NoCap score (see `prompts/10-score.md`).
- What was **out of scope** or could not be verified.
