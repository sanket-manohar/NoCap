# ADR-0001: AGENTS.md is the single source of truth for AI instructions

- **Status:** Accepted · **Date:** 2026-11-27

## Context
Each AI tool reads a different rules file (CLAUDE.md, .cursor/rules, copilot-instructions.md, …). Hand-maintaining them would drift.

## Decision
We will write instructions once in `AGENTS.md` (the open cross-tool convention) and generate every tool-specific file with `tools/build_adapters.py`. CI blocks drift.

## Consequences
+ One place to edit. + New tools are a few lines of code. − Contributors must run the generator (enforced in CI).
