# Security

> **Audience:** Security reviewers, engineers, customers' security teams
> **TL;DR:** _3 lines max — what this document tells the reader._
> **Last verified:** YYYY-MM-DD · commit `abc1234` · Owner: @name

## Reporting a vulnerability
Email **security@example.com** (or use GitHub private vulnerability reporting). We acknowledge within 72 h. Please don't open public issues for vulnerabilities.

## Authentication
Provider, methods (password, OAuth, passkeys, MFA), session type and lifetime, password policy, lockout/rate limits.

## Authorisation matrix
| Resource / action | Anonymous | User (own) | User (others') | Admin | Enforced at |
|---|---|---|---|---|---|
| Read profile | ❌ | ✅ | ❌ | ✅ | `src/…:LINE` / RLS policy |

## Secrets management
Where secrets live (per environment), who can access them, rotation schedule.

## Cryptography
In transit (TLS version, HSTS) · at rest (DB/disk/KMS) · field-level · password hashing algorithm.

## Web security controls
| Control | Value | Location |
|---|---|---|
| Content-Security-Policy | | |
| HSTS | | |
| CORS allow-list | | |
| Cookie flags | HttpOnly; Secure; SameSite=Lax | |
| CSRF | | |
| Rate limiting | | |

## Logging & monitoring
Security events logged, retention, alerting, PII redaction.

## Dependency & supply-chain security
Lockfiles, automated updates, audit tooling, SBOM, CI action pinning.

## Accepted risks
| ID | Risk | Reason accepted | Accepted by | Review date |
|---|---|---|---|---|
