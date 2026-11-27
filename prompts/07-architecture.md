# 07 · `nocap architecture` — Architecture & design documentation

Produce `docs/ARCHITECTURE.md` and `docs/DESIGN.md` using arc42 structure and C4 diagrams in Mermaid.

## Diagrams (Mermaid, GitHub-renderable)
1. **System context (C4 L1)**: users/roles, the system, external systems.
2. **Containers (C4 L2)**: web app, API, workers, DBs, caches, queues, object storage, LLM providers, with protocols on edges.
3. **Components (C4 L3)** for the 1–2 most complex containers.
4. **Sequence diagrams** for: sign-in, the core value flow, payment/checkout (if any), AI request (if any), a background job.
5. **Deployment diagram**: environments, regions, CDN, edge/serverless, managed services.
6. **ER diagram** (or link to DATA_MODEL.md).

Use `flowchart LR` with `subgraph` for C4 if the renderer lacks C4 support. Keep labels short and quote those containing special characters.

## arc42 sections
1 Introduction & goals (top 3 quality goals) · 2 Constraints · 3 Context & scope · 4 Solution strategy ·
5 Building block view · 6 Runtime view · 7 Deployment view · 8 Cross-cutting concepts (auth, errors,
logging, i18n, caching, config, security) · 9 Architecture decisions (link ADRs) · 10 Quality requirements
(with measurable scenarios, ISO/IEC 25010) · 11 Risks & technical debt · 12 Glossary.

## Design review
Assess these, rating each 1–5 with evidence: separation of concerns, coupling/cohesion, layering violations, dependency direction,
SOLID, 12-factor compliance, statelessness/scalability, single points of failure, observability, and
consistency of patterns. Recommend refactors only where the payoff is clear. Record significant ones as ADRs.
