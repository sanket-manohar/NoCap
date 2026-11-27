# Security Design — NoCap

> **Audience:** Security reviewers
> **TL;DR:** Offline, dependency-free, least-privilege CI; installers touch only NoCap-owned content.
> **Last verified:** 2026-11-27 · v1.0.0

See the root [SECURITY.md](../SECURITY.md) for disclosure.

| Control | Implementation |
|---|---|
| No network in scanner | stdlib only; no sockets or HTTP imports |
| Supply chain | 0 runtime deps; Dependabot for Actions; CI `contents: read` |
| Install safety | Marked blocks, idempotent, `--uninstall`, `copy-if-missing` for user configs |
| Secret redaction | Secret-category matches replaced with `…[redacted N chars]` |
| Action injection safety | Inputs passed via `env:`, never interpolated into `run:` |
| Remote install | Users can download and read `install.sh` first. It is short and commented |

## Accepted risks
| Risk | Reason |
|---|---|
| `curl \| bash` install path | Industry-standard convenience. Inspect-first path documented |
