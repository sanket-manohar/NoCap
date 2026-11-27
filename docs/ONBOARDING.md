# Onboarding — NoCap

> **Audience:** New contributors
> **TL;DR:** Read AGENTS.md, run the tests, then add a rule with a test.
> **Last verified:** 2026-11-27 · v1.0.0

1. `git clone … && cd nocap && python3 -m unittest discover -s tests`
2. Mental model: **content** (what AIs read) + **scanner** (what machines check) + **installers** (how it gets into projects).
3. Change agent behaviour → edit `AGENTS.md` → `python3 tools/build_adapters.py`.
4. Add a check → add an `R(...)` entry → add a fixture line to `VULN` in the tests → run the tests.
5. Add an AI tool → add a target in `tools/build_adapters.py` and in the installers' `tool_of` maps.
