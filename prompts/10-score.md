# 10 · `nocap score` — The NoCap Score

If you can run commands:
```bash
python3 .nocap/scanner/nocap.py . --badge docs/nocap-badge.svg
```
Otherwise compute it manually with the same formula:

- **Security (70%)**: start at 100 and subtract 25 per Critical, 10 per High, 4 per Medium and 1 per Low. Count at most 3 occurrences per issue type, and floor the result at 0.
- **Documentation (30%)**: the percentage present of these 17: README, ARCHITECTURE, DESIGN, MODULES, API, DATA_MODEL,
  SECURITY, THREAT_MODEL, COMPLIANCE, PRIVACY, TESTING, DEPLOYMENT, RUNBOOK, ADR folder, CHANGELOG, CONTRIBUTING, LICENSE.
- **Caps**: any Critical caps the overall score at 49. Any High caps it at 79.
- **Grade**: A+ ≥ 95 · A ≥ 85 · B ≥ 70 · C ≥ 55 · D ≥ 40 · F < 40.

Report:
```
NoCap Score: B · 78/100   (security 82 · docs 71)
🟥 0  🟧 1  🟨 3  🟦 4
Top 5 actions to raise your score:
1. … (+N)
```
Add the badge to the README:
`![NoCap](docs/nocap-badge.svg)`
