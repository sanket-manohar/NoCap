# Contributing to NoCap

Thanks for helping make AI-built software safer! 💜

## Quick setup
```bash
git clone https://github.com/sanket-manohar/nocap && cd nocap
python3 -m unittest discover -s tests      # run tests (no dependencies)
```

## Ways to contribute
| Contribution | Where | Notes |
|---|---|---|
| 🔍 New scanner rule | `scanner/nocap.py` → `RULES` | Must include `fix`, `cwe`, `owasp`, and a test in `tests/test_scanner.py` |
| 🐞 False positive report | Issue → "False positive" template | Include the minimal code snippet |
| ✅ New checklist | `checklists/<area>/` | Cite the official source; every check needs a standard fix |
| 🧰 New AI tool / IDE | `tools/build_adapters.py` | Add the target, then run the generator. Never hand-edit `adapters/` |
| 📝 Better prompts/templates | `prompts/`, `templates/` | Keep them tool-agnostic and test with 2+ AI assistants |
| 🌍 Translations | `i18n/<lang>/` | Translate the README and MASTER_PROMPT first |

## Rule-writing guidelines
1. **Precision over recall.** A noisy rule gets ignored. Prefer patterns that indicate a real problem.
2. Every rule needs: a unique ID (`CAT###`), a severity based on exploitability × impact, a CWE, an OWASP mapping, and a **standard fix** that names the framework's built-in mechanism.
3. Put secret-like test fixtures together at runtime (see `J()` in the tests) so the repo never trips secret scanners.
4. Run `python3 tools/build_adapters.py` whenever you edit `AGENTS.md`. CI checks that the adapters are up to date.

## Pull requests
- Use [Conventional Commits](https://www.conventionalcommits.org/) (`feat(scanner): add Laravel mass-assignment rule`).
- Keep PRs focused. Add or update tests. Update `CHANGELOG.md` under *Unreleased*.
- By contributing you agree your work is released under the MIT License.

Please follow our [Code of Conduct](CODE_OF_CONDUCT.md).
