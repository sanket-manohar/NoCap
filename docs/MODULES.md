# Modules — NoCap

> **Audience:** Contributors
> **TL;DR:** Six top-level areas; only the scanner contains executable logic beyond installers.
> **Last verified:** 2026-11-27 · v1.0.0

| Module | Path | Responsibility | Depends on |
|---|---|---|---|
| Agent brain | `AGENTS.md` | Commands, guard rules, doc and finding standards | — |
| Master prompt | `MASTER_PROMPT.md` | Zero-install, self-contained audit + docs prompt | — |
| Workflows | `prompts/` | Step-by-step procedures per command | templates, checklists |
| Templates | `templates/` | Output skeletons for 18 docs | — |
| Checklists | `checklists/` | Standards-based checks with fixes | — |
| Scanner | `scanner/nocap.py` | Stack detection, rules, scoring, reports | Python ≥ 3.8 stdlib |
| Adapter generator | `tools/build_adapters.py` | Builds `adapters/*` + `MANIFEST` from AGENTS.md | AGENTS.md |
| Installers | `install.sh`, `install.ps1`, `bin/nocap.js` | Copy toolkit, apply MANIFEST, optional CI | MANIFEST |
| GitHub Action | `action.yml` | Run scanner in CI, step summary, artifact, outputs | scanner |
| Tests | `tests/test_scanner.py` | Rule firing, scoring, suppression, CLI | scanner |
