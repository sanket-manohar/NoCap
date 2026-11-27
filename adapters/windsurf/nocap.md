---
trigger: always_on
description: NoCap documentation & security guard rules
---
# NoCap (documentation + security guard)

This project uses **NoCap**. Full instructions: `.nocap/AGENTS.md`. Read it before running any command below.

## Commands
When the user types one of these phrases (in any language and in any chat), run the matching workflow.
Each workflow has a detailed prompt in `.nocap/prompts/`.

| Command | What you do | Prompt file |
|---|---|---|
| `nocap` or `nocap help` | Show this table and suggest the best next command | — |
| `nocap docs` | Generate or refresh the **full documentation set** in `docs/` | `.nocap/prompts/01-full-documentation.md` |
| `nocap audit` | Full **security audit** with the standard fix for each issue → `docs/SECURITY_AUDIT.md` | `.nocap/prompts/02-security-audit.md` |
| `nocap threat-model` | STRIDE + LINDDUN threat model → `docs/THREAT_MODEL.md` | `.nocap/prompts/03-threat-model.md` |
| `nocap compliance <framework>` | Compliance gap analysis (`gdpr`, `dpdp`, `hipaa`, `pci`, `soc2`, `iso27001`, `ccpa`, `wcag`, `ai-act`, `all`) → `docs/COMPLIANCE.md` | `.nocap/prompts/04-compliance.md` |
| `nocap review [path or diff]` | Secure code review of a file, folder or the current diff | `.nocap/prompts/05-code-review.md` |
| `nocap fix` | Fix findings from the latest audit, critical first, with tests | `.nocap/prompts/06-fix.md` |
| `nocap architecture` | Architecture + design docs with diagrams (C4 / Mermaid) | `.nocap/prompts/07-architecture.md` |
| `nocap explain` | Plain-English walkthrough of the codebase for a new developer → `docs/ONBOARDING.md` | `.nocap/prompts/08-explain.md` |
| `nocap update` | Detect code changes since the docs were written and update only what changed | `.nocap/prompts/09-update.md` |
| `nocap score` | Run the scanner (or a manual equivalent) and report the NoCap score | `.nocap/prompts/10-score.md` |
| `nocap ship` | Production-readiness gate: run everything above and give a GO / NO-GO | `.nocap/prompts/11-ship.md` |

If you cannot read files in `.nocap/`, use the summaries in this document — they are enough to do the job.

## Always-on guard rules
These rules apply even when no command is used. They are defined in full in
`.nocap/prompts/00-guard-rules.md`. The non-negotiables:

1. **No secrets in code.** Read secrets from environment variables or a secrets manager. Never put a
   secret behind a public env prefix (`NEXT_PUBLIC_`, `VITE_`, `REACT_APP_`, `EXPO_PUBLIC_`). Keep `.env*` in `.gitignore`
   and commit a `.env.example`.
2. **Authorise on the server, every time.** Deny by default. Check that the current user owns or may access
   *this specific* record (no IDOR/BOLA). UI checks are cosmetic.
3. **Validate all input** at the trust boundary with a schema (zod, pydantic, Joi, Bean Validation, FluentValidation…).
   Whitelist fields — never write `req.body` straight into a model.
4. **Never build queries, commands, paths or HTML from strings.** Use parameterised queries, argument arrays,
   path allow-lists and auto-escaping templates.
5. **Use proven crypto only.** Argon2id/bcrypt for passwords, AES-GCM/ChaCha20-Poly1305 for encryption, a CSPRNG for tokens, TLS everywhere.
   Never disable certificate checks.
6. **Secure sessions.** Tokens go in `HttpOnly; Secure; SameSite` cookies, not localStorage. Short-lived access tokens, rotating refresh tokens.
7. **Rate-limit and size-limit** every public endpoint, especially auth, OTP, password reset, file upload and LLM calls.
8. **Fail closed and log safely.** Return generic errors to users, keep details in server logs, never log secrets or personal data.
9. **Least privilege everywhere**: DB users, cloud IAM, containers (non-root), CI tokens, LLM tools.
10. **Dependencies:** use well-maintained packages, pin versions, commit lockfiles. **Before you add a package, check that it really exists** (AI tools sometimes invent package names, and attackers register those names).
11. **For LLM features:** treat model output as untrusted, keep system prompts free of secrets, never let the model act with more rights than the user, and cap tokens and spend.
12. **Security headers** on web apps: CSP, HSTS, X-Content-Type-Options, frame-ancestors/X-Frame-Options, Referrer-Policy.
13. **Write the test.** For every auth or permission rule, add a negative test (user A cannot read user B's data).
14. **Document as you go.** When you add a module, endpoint, table, env var or third-party service, update the matching file in `docs/`.

If the user asks for something that breaks a guard rule, do it the secure way and explain the change in one line.
If they insist, comply only when the risk is theirs to accept. Add a `SECURITY-RISK-ACCEPTED:` comment and record it in `docs/SECURITY.md`.

Generated docs go to `docs/` using templates in `.nocap/templates/`. Findings use the format in `.nocap/AGENTS.md` §4.
