# 05 · `nocap review [target]` — Secure code review

**Target:** a file, a folder, a PR, or (by default) the uncommitted diff (`git diff` + `git diff --staged`).

Review in this order and stop to report anything Critical immediately:

1. **Intent.** What is this change trying to do? Does it actually do that?
2. **Trust boundaries.** Which inputs come from users, third parties, the LLM or the network? Follow each one to its sinks.
3. **AuthN/AuthZ.** Does every new route, action or resolver check identity *and* object-level permission?
4. **Injection & output encoding.** Any string-built queries, commands, paths, HTML or prompts?
5. **Secrets & config.** Any new keys, URLs, flags? Are they in env, with an `.env.example` entry?
6. **Data.** New PII? Is it logged, encrypted, retained, exportable and deletable?
7. **Dependencies.** New packages: do they exist, are they maintained, are they needed? Is the lockfile updated?
8. **Errors & edge cases.** Nulls, empty lists, huge inputs, timeouts, retries, concurrency, partial failure. Does the code fail closed?
9. **Tests.** Is there a test for the happy path **and** an abuse/negative path?
10. **Docs.** Do `docs/API.md`, `DATA_MODEL.md`, `MODULES.md` or the env table need updating?
11. **Maintainability.** Naming, duplication, function size, dead code, types.

Output format (GitHub-review style):
```
🟥/🟧/🟨/🟦 path/file.ext:LINE — <issue>
Why: <one line>
Fix:
<suggested code>
```
End with: ✅ Approve / ⚠️ Approve with comments / ❌ Request changes, plus the top 3 must-fix items.
