# Security Policy

## Reporting a vulnerability in NoCap
Please **do not** open a public issue. Use GitHub's **"Report a vulnerability"** (Security → Advisories),
or email **sanketsmanohar1@gmail.com**. We aim to acknowledge reports within 72 hours.

In scope: the scanner, the installers (`install.sh`, `install.ps1`, `bin/nocap.js`), the GitHub Action, and
any prompt or adapter content that could make an AI assistant act unsafely.

## Our own practices
- Zero runtime dependencies. The scanner uses the Python standard library only.
- No network access or telemetry from the scanner.
- Installers only write NoCap-owned files and marked blocks, and support clean uninstall.
- CI runs with `contents: read` permissions.

> Prefer to inspect before running? Download `install.sh`, read it, then run it locally. It is under 150 lines.
