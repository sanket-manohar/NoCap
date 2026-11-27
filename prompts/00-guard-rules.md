# 00 · Guard Rules — secure-by-default coding (always on)

Apply these rules to **every** line of code you generate or modify, in any language. They are the
condensed, practical form of OWASP ASVS 5.0, the OWASP Top 10:2025, OWASP API Top 10:2023, the OWASP LLM Top 10:2025
and CWE Top 25.

## Secrets & configuration
- Secrets come from env vars / a secrets manager only. Never in code, tests, Dockerfiles, client bundles or logs.
- Public env prefixes (`NEXT_PUBLIC_`, `VITE_`, `REACT_APP_`, `EXPO_PUBLIC_`, `PUBLIC_`) are **public**. Never put secrets there.
- Keep `.env*` in `.gitignore` and maintain `.env.example` with placeholder values.
- Validate the required config at startup and fail fast with a clear message.
- Debug/verbose modes come from env and default to OFF.

## Authentication
- Use the framework's or provider's auth (Auth.js, Clerk, Supabase Auth, Firebase Auth, Django auth, Spring Security, ASP.NET Identity, Devise). Don't roll your own.
- Hash passwords with Argon2id (or bcrypt cost ≥ 12). Enforce a length of at least 8 and check against breached-password lists. Don't impose composition rules.
- Offer MFA (TOTP/WebAuthn/passkeys) for admin and sensitive accounts.
- Rate-limit and add lockout/backoff on login, signup, OTP, password reset, magic links.
- Login and reset errors must be identical for unknown and known users, so attackers can't tell which accounts exist.
- Sessions: `HttpOnly; Secure; SameSite=Lax|Strict` cookies; rotate the session ID on login; set idle and absolute timeouts; invalidate the session on the server at logout.
- JWT: verify the signature with an explicit algorithm list; validate `exp`, `iss`, `aud`. Keep access tokens short-lived (≤ 15 min) and rotate refresh tokens.

## Authorisation (the #1 risk in AI-built apps)
- Deny by default. Check permissions **on the server** for every request.
- Check object-level ownership: `WHERE id = :id AND owner_id = :currentUser` (prevents IDOR/BOLA).
- Check function-level role for admin actions (BFLA).
- Allow-list writable fields; never mass-assign request bodies (BOPLA).
- On BaaS (Supabase/Firebase): enable RLS / security rules on **every** table/collection, scoped to `auth.uid()`.
- Never ship a service-role/admin key to a client.

## Input, output & injection
- Validate every input at the boundary with a schema: type, length, format, range, enum.
- SQL: parameterised queries or the ORM only. Interpolating raw strings into SQL is forbidden.
- NoSQL: reject objects where scalars are expected (blocks `$ne`/`$where` injection).
- OS commands: avoid them. If you must, use an argument array with `shell=false` and allow-listed values.
- Files: never build paths from user input. Map IDs to paths, and check that resolved paths stay inside the base dir.
- HTML: rely on template auto-escaping. If raw HTML is required, sanitise with DOMPurify/nh3/HtmlSanitizer.
- URLs fetched by the server: allow-list hosts and block private, link-local and metadata IPs (SSRF).
- Redirects: relative paths or an allow-list only.
- Deserialisation: JSON only for untrusted data. Never pickle, Java serialisation, BinaryFormatter, `unserialize` or `yaml.load`.
- Uploads: limit size, verify type by magic bytes, rename to random IDs, store outside the web root or in object storage, and scan if possible.

## Cryptography & transport
- TLS 1.2+ everywhere, with HSTS. Never disable certificate validation.
- Encryption: AES-256-GCM or ChaCha20-Poly1305 through a high-level library (libsodium, Tink, `cryptography`). No ECB, DES, RC4 or custom crypto.
- Randomness for tokens/IDs/OTPs: a CSPRNG only (`crypto.randomUUID`, `secrets`, `SecureRandom`, `crypto/rand`).
- Encrypt sensitive data at rest. Keep keys in a KMS, not next to the data.

## Web hardening
- Headers: `Content-Security-Policy`, `Strict-Transport-Security`, `X-Content-Type-Options: nosniff`, `frame-ancestors 'none'` / `X-Frame-Options: DENY`, `Referrer-Policy: strict-origin-when-cross-origin`, `Permissions-Policy`.
- CORS: an exact origin allow-list. Never use `*` together with credentials.
- CSRF protection for cookie-authenticated, state-changing requests.
- Verify webhook signatures (Stripe, Razorpay, GitHub…) with constant-time comparison and replay protection.

## Resource limits & business logic
- Rate-limit every public endpoint. Use stricter limits for auth, search, export and AI endpoints.
- Cap pagination (`limit ≤ 100`), request body size, upload size, query complexity (GraphQL depth/cost), and timeouts on outbound calls.
- Make payments, coupons, votes and other sensitive flows idempotent and abuse-resistant (server-side price calculation, no trust in client totals).

## Errors, logging & monitoring
- Users get a generic message and a correlation ID. Details go to server logs.
- Fail closed: an exception in an auth check means *deny*.
- Log security events (login success/failure, permission denied, admin actions, config changes) as structured logs with no secrets or PII.
- Alert on anomalies (spikes in 401/403/429/5xx, new admin, mass export).

## Dependencies & supply chain
- Before adding a package, confirm it exists, is maintained, and is popular enough to trust. AI tools hallucinate package names, and attackers register them ("slopsquatting").
- Pin versions, commit lockfiles, use `npm ci` / `pip install --require-hashes` in CI.
- Enable Dependabot/Renovate and run `osv-scanner` / `npm audit` / `pip-audit`.
- Pin GitHub Actions to a commit SHA. Set CI permissions to `contents: read` by default.

## AI / LLM features
- Never call model APIs from the browser or a mobile app with an embedded key. Proxy through your server.
- Keep system prompts free of secrets. Assume they will leak.
- Treat model output as untrusted. Encode it before rendering, and never `eval` it or pass it to a shell or SQL.
- Least agency: tools get the current user's permissions only. Destructive actions need human confirmation.
- Defend against indirect prompt injection from retrieved documents, web pages and emails: separate data from instructions and filter tool calls.
- RAG: enforce per-user access control on retrieved chunks.
- Cap tokens, requests and spend per user. Set timeouts.

## Containers, cloud & CI
- Containers: pinned base image, non-root `USER`, no secrets in layers, minimal image (distroless/alpine), read-only filesystem where possible.
- Cloud: least-privilege IAM, private buckets and DBs, no public admin ports, encryption at rest, backups tested.
- IaC is reviewed like code and scanned (Checkov/tfsec/Trivy).

## Privacy by design
- Collect the minimum data. Record its purpose, legal basis and retention period.
- Support export and delete for user data. Get consent where it is required, and make withdrawing consent as easy as giving it.
- Mask PII in logs, analytics and error trackers.

## Quality
- Small, single-purpose modules with clear interfaces. No god files.
- Typed code where the language allows (TypeScript strict, Python type hints, etc.).
- Tests for business logic and **negative auth tests**.
- Update `docs/` whenever you add a module, endpoint, table, env var or external service.
