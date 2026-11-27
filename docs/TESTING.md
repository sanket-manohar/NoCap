# Testing — NoCap

> **Audience:** Contributors
> **TL;DR:** Unit tests for every rule family, scoring, suppression and CLI; CI smoke-tests all installers.
> **Last verified:** 2026-11-27 · v1.0.0

| Layer | Command | What it covers |
|---|---|---|
| Unit | `python3 -m unittest discover -s tests` | 38+ rules fire on fixtures, a clean project scores A+, placeholders ignored, redaction, toolkit skip, CLI outputs |
| Smoke | CI `install-smoke` job | bash install → scan → uninstall; npx init |
| Self-scan | CI `self-scan` job | Repo passes its own Action at `fail-on: high` |
| Drift | CI `git diff --exit-code adapters/` | Adapters match AGENTS.md |

Matrix: Ubuntu/macOS/Windows × Python 3.8/3.12/3.13.
