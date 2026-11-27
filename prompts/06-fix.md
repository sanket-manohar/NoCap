# 06 · `nocap fix` — Remediate findings safely

1. Read `docs/SECURITY_AUDIT.md` (or `.nocap-results.json` / `NOCAP_REPORT.md`). If none exists, run `nocap audit` first.
2. Show the plan: findings grouped **Critical → High → Medium → Low**, each with the intended fix. Ask before
   touching anything destructive (data migrations, key rotation, auth provider changes).
3. For each finding, in order:
   - Write a **failing test** that demonstrates the issue (e.g. user B gets 403 on user A's record) whenever that is feasible.
   - Apply the **standard fix** using the framework's built-in mechanism. Keep the change minimal and focused.
   - Run the tests. Re-run the scanner for that file.
   - Update the finding's status in `docs/SECURITY_AUDIT.md` to `✅ Fixed in <commit/file>`.
4. Some things code alone can't fix. Leaving a hard-coded secret removed but unrotated is not a fix. List the human actions clearly:
   *"Rotate the OpenAI key in the dashboard → update the env var in Vercel → redeploy."*
5. Update affected docs (SECURITY.md, API.md, CHANGELOG.md under "Security").
6. Finish with before/after NoCap scores and the remaining open items.

Never "fix" a finding by suppressing it (`nocap-ignore`) unless it is a confirmed false positive. If you do, add the reason in the same comment.
