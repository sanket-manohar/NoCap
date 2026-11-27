# 09 · `nocap update` — Keep docs in sync with code

1. Read the `Last verified: … · commit <sha>` stamp in each doc.
2. Run `git diff --stat <sha>..HEAD` (or ask which files changed if git is unavailable).
3. Map changed files to docs:
   - routes/controllers/handlers → `API.md`, `SECURITY.md` (authz matrix)
   - models/migrations/schema/rules → `DATA_MODEL.md`, `PRIVACY.md`
   - new folders/modules → `MODULES.md`, `ARCHITECTURE.md`
   - new dependencies/SDKs → `ARCHITECTURE.md` (external systems), `PRIVACY.md` (sub-processors), `THREAT_MODEL.md`
   - env/config/infra/CI → `README.md` env table, `DEPLOYMENT.md`
   - auth, crypto, uploads, payments, AI → re-run `nocap review` on those files
4. Update only the affected sections, then refresh the stamps.
5. Add an entry to `CHANGELOG.md` (`Unreleased`).
6. Report: docs touched, sections changed, and anything that now needs a security re-review.
