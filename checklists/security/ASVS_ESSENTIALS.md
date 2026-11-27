# OWASP ASVS 5.0 — Essentials

The [Application Security Verification Standard](https://owasp.org/www-project-application-security-verification-standard/) is the most complete *requirements* standard
for web app security. ASVS 5.0 has three levels: **L1** (baseline, every app), **L2** (most apps with sensitive data,
the recommended default), and **L3** (high-value apps: banking, health, critical infrastructure).

Use this as a quick map from ASVS chapter to what to verify. For a formal assessment, use the full standard.

| ASVS 5.0 chapter | Verify (summary) |
|---|---|
| V1 Encoding & Sanitization | Context-aware output encoding, safe parsers, injection prevention |
| V2 Validation & Business Logic | Server-side schema validation, business-limit enforcement, anti-automation |
| V3 Web Frontend Security | CSP, cookie attributes, CORS, framing, browser security features |
| V4 API & Web Service | REST/GraphQL/WebSocket hardening, HTTP method handling |
| V5 File Handling | Upload validation, storage outside web root, download safety |
| V6 Authentication | Password policy (NIST 800-63B), MFA, credential recovery, lockout |
| V7 Session Management | Token entropy, rotation, timeouts, termination |
| V8 Authorization | Deny by default, object/function/field-level checks |
| V9 Self-contained Tokens | JWT validation, algorithm allow-lists, claims checks |
| V10 OAuth & OIDC | PKCE, state/nonce, redirect URI exact match, token handling |
| V11 Cryptography | Approved algorithms, key management, CSPRNG |
| V12 Secure Communication | TLS configuration, certificate validation, internal TLS |
| V13 Configuration | Secrets management, hardened builds, dependency control |
| V14 Data Protection | Classification, minimisation, client-side storage, caching of sensitive data |
| V15 Secure Coding & Architecture | Dependencies, safe concurrency, documented architecture |
| V16 Security Logging & Error Handling | Security event logging, log protection, safe errors |
| V17 WebRTC | Media/TURN security (if used) |

> Chapter titles reflect ASVS 5.0.0. Always cross-check requirement IDs against the official release before citing them in an audit.
