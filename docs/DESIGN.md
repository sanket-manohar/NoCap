# Design — NoCap

> **Audience:** Contributors
> **TL;DR:** Plain files over frameworks; plain-language commands over CLIs; every finding carries its fix.
> **Last verified:** 2026-11-27 · v1.0.0

## Principles
1. **Content is the product.** Markdown that any AI can read beats a plugin for one IDE.
2. **Commands are phrases, not syntax.** "nocap audit" works in every chat box.
3. **Every problem ships with its standard fix**, citing CWE/OWASP and the framework's built-in mechanism.
4. **Zero dependencies.** Python stdlib for the scanner, POSIX shell, PowerShell and Node built-ins for installers.
5. **Truth over polish.** Generated docs must cite files and mark unknowns `⚠️ UNVERIFIED`.

## Scanner design
- Rules are data (`R(...)` entries) so contributors add checks without touching the engine.
- Severity weights: critical 25, high 10, medium 4, low 1. Each rule counts at most 3 times so one noisy pattern can't zero the score.
- Grade caps (critical → ≤ 49, high → ≤ 79) keep a pretty docs score from hiding real risk.

## Accessibility
Console output works without colour (`--no-color`, auto-off when not a TTY). The badge has an `aria-label`.
