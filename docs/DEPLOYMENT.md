# Release & Distribution — NoCap

> **Audience:** Maintainers
> **TL;DR:** Tag a release; users pull via raw GitHub URLs, npx github:, or the Action @v1.
> **Last verified:** 2026-11-27 · v1.0.0

0. First publish only: `./tools/publish.sh <github-user> <email>` (Windows: `tools\publish.ps1`).
1. Update `CHANGELOG.md` and `VERSION` in `scanner/nocap.py` and `package.json`.
2. `python3 tools/build_adapters.py && python3 -m unittest discover -s tests`
3. Copy release highlights into `RELEASE_NOTES.md`, then `git tag -a v1.x.y -m v1.x.y && git push --tags`.
4. `.github/workflows/release.yml` tests, builds a zip + SHA-256, creates the GitHub Release and moves the `v1` tag automatically.
5. Optional: tick "Publish this Action to the GitHub Marketplace" on the release page.

Rollback: move the `v1` tag back to the previous release.
