# CLI & Action Reference — NoCap

> **Audience:** Users and CI integrators
> **TL;DR:** Everything is driven by `nocap.py` flags or the Action inputs.
> **Last verified:** 2026-11-27 · v1.0.0

## Scanner CLI
| Flag | Default | Description |
|---|---|---|
| `path` | `.` | Directory to scan |
| `--out FILE` | `NOCAP_REPORT.md` | Markdown report (`-` to skip) |
| `--json FILE` | — | Machine-readable results |
| `--badge FILE` | — | SVG score badge |
| `--fail-on SEV` | `none` | Exit 1 if a finding ≥ SEV exists |
| `--min-severity SEV` | `info` | Hide findings below SEV |
| `--exclude GLOB` | — | Repeatable |
| `--list-rules` | — | Print all rules |
| `--no-color`, `--quiet` | — | Output control |

Exit codes: `0` ok · `1` threshold exceeded · `2` bad input / Python missing.

## JSON schema (summary)
`{ version, score: {overall, grade, security, docs, by_severity}, stack: {languages, platforms, frameworks}, docs: {NAME: bool}, recommendations: {checklists[], compliance[]}, findings: [{rule, severity, category, title, file, line, snippet, cwe, owasp, fix}] }`

## GitHub Action
Inputs: `path`, `fail-on` (default `high`), `exclude` (comma globs), `upload-report`. Outputs: `score`, `grade`.

## npx CLI
`init [dir] [--tools a,b] [--ci]` · `scan [dir] [flags]` · `prompt`
