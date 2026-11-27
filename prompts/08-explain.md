# 08 · `nocap explain` — Explain the codebase to a human

Write `docs/ONBOARDING.md` for a developer joining tomorrow, or for the founder who vibe-coded it and
now needs to understand it.

1. **The 60-second version**: what the app does, for whom, and how a request flows through it (one diagram).
2. **Run it locally**: exact commands, required env vars, seed data, test accounts (no real credentials).
3. **Mental model**: the 5–7 core concepts/entities and how they relate.
4. **Folder map**: each top-level folder → what lives there → "change this when you want to …".
5. **Walkthrough**: follow one real feature end-to-end (UI → API → DB → back) with file links.
6. **Gotchas**: surprising behaviour, magic config, implicit conventions, known debt.
7. **How to make a safe change**: branch → test → `nocap review` → PR checklist.
8. **Glossary** of domain terms.

Write plainly, define jargon on first use, and link every file mentioned.
