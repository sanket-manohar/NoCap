# OWASP Top 10:2025 Checklist

Source: [owasp.org/Top10/2025](https://owasp.org/Top10/2025/). Mark each item ✅ / ❌ / N/A, with evidence.

## A01 · Broken Access Control (now includes SSRF)
- [ ] Deny by default. Every route, action and resolver checks the session **on the server**
- [ ] Object-level checks on every ID taken from the request (IDOR/BOLA)
- [ ] Function-level checks on admin and privileged actions
- [ ] No mass assignment: writable fields are allow-listed
- [ ] CORS allow-list. No `*` with credentials
- [ ] JWT/session invalidated on logout. Tokens can't be reused after a role change
- [ ] Directory listing is off. Metadata files (`.git`, `.env`, backups) aren't served
- [ ] SSRF: outbound URLs allow-listed; private, link-local and metadata IPs blocked
- [ ] Rate limits on APIs to slow down automated attacks
- [ ] Access-control failures are logged and alerted
**Standard fix:** central authorisation middleware or policy layer (CASL, Oso, Casbin, Pundit, Spring Security, ASP.NET policies, Supabase RLS) plus negative tests.

## A02 · Security Misconfiguration
- [ ] Debug off, no stack traces, no default credentials or sample apps in prod
- [ ] Security headers: CSP, HSTS, nosniff, frame-ancestors, Referrer-Policy, Permissions-Policy
- [ ] Cloud storage private. Unused ports, services and features disabled
- [ ] Same hardened config across environments, applied automatically (IaC)
- [ ] XML parsers have DTD/external entities disabled (XXE)
- [ ] Cookies set with `HttpOnly; Secure; SameSite`
**Standard fix:** a repeatable hardening baseline in code (IaC, Helmet/django-security, Spring Security headers) checked in CI.

## A03 · Software Supply Chain Failures
- [ ] Lockfiles committed. CI installs reproducibly (`npm ci`, `pip --require-hashes`)
- [ ] Every dependency exists, is maintained and is actually needed (no hallucinated or typosquatted packages)
- [ ] Automated updates (Dependabot/Renovate) and vulnerability scanning (osv-scanner, npm audit, pip-audit)
- [ ] CI/CD hardened: least-privilege tokens, actions pinned to SHA, protected branches, required reviews
- [ ] Build artifacts are signed or come from trusted builds. Generate an SBOM (CycloneDX/SPDX) for releases
- [ ] No `curl | sh` and no install scripts that download unverified code
**Standard fix:** SLSA-style build integrity, plus dependency policy and automated audit gates.

## A04 · Cryptographic Failures
- [ ] TLS 1.2+ everywhere with HSTS. No certificate-validation bypass
- [ ] Passwords hashed with Argon2id / scrypt / bcrypt (cost ≥ 12)
- [ ] AES-GCM or ChaCha20-Poly1305 through a vetted library. No ECB, DES, RC4, MD5 or SHA-1 for security
- [ ] Keys in a KMS or secrets manager, rotated, and never hard-coded
- [ ] CSPRNG for tokens, OTPs and IDs
- [ ] Sensitive data classified, minimised, and encrypted at rest
**Standard fix:** libsodium / Google Tink / `cryptography` / platform KMS. Never write custom crypto.

## A05 · Injection (SQL, NoSQL, OS, LDAP, template, XSS)
- [ ] Parameterised queries / ORM everywhere
- [ ] No `eval`, `exec` or shell calls with user input
- [ ] Output encoding through auto-escaping templates. Raw HTML is sanitised (DOMPurify/nh3)
- [ ] Server-side schema validation on all input
- [ ] A strict CSP as defence-in-depth against XSS
**Standard fix:** safe APIs by construction (prepared statements, argument arrays, templating engines).

## A06 · Insecure Design
- [ ] Threat model exists and is current (`docs/THREAT_MODEL.md`)
- [ ] Abuse cases covered: rate limits, quotas, anti-automation, business-logic limits
- [ ] Tenant isolation designed in (tenant_id on every query / RLS)
- [ ] Secure defaults and paved-road libraries for auth, validation and crypto
- [ ] Unit and integration tests for critical flows, including misuse
**Standard fix:** threat modelling plus secure design patterns, and ASVS as the requirements baseline.

## A07 · Authentication Failures
- [ ] Mature auth provider or framework. No home-grown auth
- [ ] MFA available (TOTP/WebAuthn). Passkeys if possible
- [ ] Credential stuffing defence: rate limiting, breached-password check, bot detection
- [ ] Generic error messages (no user enumeration)
- [ ] Session IDs regenerated on login, with idle and absolute timeout, and server-side invalidation
- [ ] Reset tokens are single-use, short-lived and high-entropy
**Standard fix:** NIST SP 800-63B-aligned password and session policy through your framework's auth module.

## A08 · Software or Data Integrity Failures
- [ ] No unsafe deserialisation of untrusted data
- [ ] Webhooks signature-verified (HMAC, constant-time compare, timestamp tolerance)
- [ ] Updates and plugins verified with signatures. CDN scripts use Subresource Integrity (SRI)
- [ ] Critical data changes are audited and tamper-evident
**Standard fix:** signed artifacts, SRI, and JSON-only data exchange with schema validation.

## A09 · Logging & Alerting Failures
- [ ] Logins (success and failure), access denials, admin actions and input-validation failures are logged
- [ ] Logs are structured, centralised, protected from tampering, and contain no secrets or PII
- [ ] Alerts reach a human: auth failure spikes, 5xx, unusual exports, new admin
- [ ] An incident response plan exists (`docs/RUNBOOK.md`)
**Standard fix:** OpenTelemetry plus a log platform with alert rules. Use the OWASP Logging Cheat Sheet.

## A10 · Mishandling of Exceptional Conditions
- [ ] Errors are caught at boundaries. Unexpected states fail **closed** (deny), not open
- [ ] No swallowed exceptions. Errors are logged with context
- [ ] Generic error responses to users, with a correlation ID
- [ ] Resource cleanup (`finally`, `using`, `defer`, context managers). No partial transactions left behind
- [ ] Timeouts, retries with backoff, and circuit breakers for dependencies
- [ ] Null, overflow, and empty or malformed input handled explicitly
**Standard fix:** consistent error-handling middleware, plus transactions and defensive defaults.
