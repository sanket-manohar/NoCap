# Contributing

## Workflow
1. Branch from `main`: `feat/…`, `fix/…`, `docs/…`
2. Commit using [Conventional Commits](https://www.conventionalcommits.org/): `feat(auth): add passkeys`
3. Open a PR, fill in the template, make sure CI is green.

## PR security checklist
- [ ] No secrets, keys, or `.env` files committed
- [ ] New endpoints check authentication **and** object-level authorisation
- [ ] Inputs validated with a schema; no string-built SQL/commands/HTML
- [ ] New dependencies verified (exist, maintained, needed) and lockfile updated
- [ ] Tests include a negative/abuse case
- [ ] `docs/` updated (API, data model, env vars, modules)
- [ ] `nocap review` run on the diff

## Code style
Formatter/linter commands.
