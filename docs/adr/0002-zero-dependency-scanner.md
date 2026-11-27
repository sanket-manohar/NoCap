# ADR-0002: Zero-dependency, regex-based scanner

- **Status:** Accepted · **Date:** 2026-11-27

## Context
Vibe coders often lack security tooling. Every install step loses users.

## Decision
We will ship a single-file Python stdlib scanner using curated regex rules plus project-level checks. Deep analysis (taint tracking, CVE lookup) is delegated to optional tools (Semgrep, CodeQL, osv-scanner) and to the AI workflows.

## Alternatives
| Option | Why not |
|---|---|
| Wrap Semgrep | Needs pip install and network for rules |
| Node-only scanner | Excludes Python-only environments, which matter for CI |

## Consequences
+ Runs anywhere with Python. + Easy to contribute rules. − Pattern-level only. This is documented.
