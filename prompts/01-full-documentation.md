# 01 · `nocap docs` — Full documentation set

**Goal:** produce accurate, standards-based documentation that lets a new developer, a security
reviewer or an auditor understand the system without reading all the code.

## Step 1 — Discover (do not write docs yet)
1. List the repo tree (skip `node_modules`, `vendor`, build output).
2. Read manifests (`package.json`, `requirements.txt`, `pyproject.toml`, `go.mod`, `pom.xml`, `Gemfile`,
   `composer.json`, `Cargo.toml`, `pubspec.yaml`, …), config files, env examples, Dockerfiles, IaC, CI files.
3. Find entry points: servers, route definitions, CLI mains, serverless handlers, mobile app roots, cron jobs, queues.
4. Find data stores: ORM models, migrations, schema files, BaaS rules.
5. Find integrations: SDK imports and outbound HTTP calls (auth, payments, AI, email, SMS, storage, analytics).
6. Produce the **System Snapshot** (purpose, users and roles, stack, data, integrations, hosting) and show it to the user.

## Step 2 — Generate
Create or update each file from `.nocap/templates/` (keep the template headings; fill every section,
or write `N/A — reason`):

| File | Template | Must include |
|---|---|---|
| `README.md` | `templates/README.md` | Quick start that actually works, env var table, scripts, structure |
| `docs/ARCHITECTURE.md` | `templates/ARCHITECTURE.md` | C4 L1+L2 Mermaid, runtime sequence diagrams, deployment view |
| `docs/DESIGN.md` | `templates/DESIGN.md` | Patterns, state, errors, caching, UI system, accessibility |
| `docs/MODULES.md` | `templates/MODULES.md` | One section per module with interface, deps, risks |
| `docs/API.md` | `templates/API.md` | Every route with auth/role/schema/errors/limits |
| `docs/DATA_MODEL.md` | `templates/DATA_MODEL.md` | ER diagram, PII classification, retention, access policies |
| `docs/SECURITY.md` + root `SECURITY.md` | `templates/SECURITY.md` | AuthN/AuthZ matrix, secrets, crypto, headers, disclosure policy |
| `docs/THREAT_MODEL.md` | `templates/THREAT_MODEL.md` | DFD with trust boundaries, STRIDE + LINDDUN tables |
| `docs/PRIVACY.md` | `templates/PRIVACY.md` | Data inventory, purposes, legal basis, rights, sub-processors |
| `docs/COMPLIANCE.md` | `templates/COMPLIANCE.md` | Applicable frameworks + gap tables |
| `docs/TESTING.md` | `templates/TESTING.md` | Strategy, coverage, missing critical tests |
| `docs/DEPLOYMENT.md` | `templates/DEPLOYMENT.md` | Environments, pipeline, infra, rollback |
| `docs/RUNBOOK.md` | `templates/RUNBOOK.md` | Alerts → diagnosis → fix, backup/restore, incident & breach response |
| `docs/ONBOARDING.md` | `templates/ONBOARDING.md` | Day-1 setup, mental model, where to change what |
| `docs/adr/NNNN-title.md` | `templates/adr/0000-template.md` | 3–5 key decisions inferred from code |
| `CHANGELOG.md` | `templates/CHANGELOG.md` | Keep a Changelog format |
| `CONTRIBUTING.md` | `templates/CONTRIBUTING.md` | Branching, commits, review, security checklist for PRs |

## Step 3 — Quality bar (self-check before finishing)
- [ ] Every claim is traceable to a file path. Unknowns are marked `⚠️ UNVERIFIED`.
- [ ] All Mermaid blocks are syntactically valid. Keep them simple and quote labels containing special characters.
- [ ] Env var table matches the code (search for `process.env`, `os.environ`, `getenv`, `@Value`, `ENV[`).
- [ ] Every API route in code appears in `API.md`, and every table appears in `DATA_MODEL.md`.
- [ ] No secrets were copied into the docs.
- [ ] Each doc has the header: audience, TL;DR, `Last verified: <date> · commit <sha>`.

## Step 4 — Report
Finish with a short summary: files created/updated, open questions, and the suggested next command
(usually `nocap audit`).
