# 03 · `nocap threat-model` — STRIDE + LINDDUN

Output: `docs/THREAT_MODEL.md` (template: `templates/THREAT_MODEL.md`). Method follows the
OWASP Threat Modeling Cheat Sheet and the Threat Modeling Manifesto's four questions:

1. **What are we working on?** Draw a Mermaid data-flow diagram (DFD): external entities, processes, data
   stores, data flows, and **trust boundaries** (internet ↔ edge, edge ↔ app, app ↔ DB, app ↔ third parties,
   app ↔ LLM). List the assets: data, credentials, money, reputation, availability.
2. **What can go wrong?**
   - **STRIDE** per element: Spoofing, Tampering, Repudiation, Information disclosure, Denial of service, Elevation of privilege.
   - **LINDDUN** for personal data: Linking, Identifying, Non-repudiation, Detecting, Data disclosure, Unawareness, Non-compliance.
   - **Abuse cases**: write 5–10 "As an attacker I want to … so that …" stories for this specific app.
   - **AI threats** (if relevant): direct/indirect prompt injection, data exfiltration via tools, model DoS / cost exhaustion.
3. **What are we going to do about it?** For each threat: existing control (with file path), gap, mitigation,
   owner, and a status of Mitigate / Accept / Transfer / Avoid. Rate risk as Likelihood (1–5) × Impact (1–5).
4. **Did we do a good job?** List assumptions, out-of-scope items, and when to re-run the model (new
   integration, new data type, new role, before major release).

Keep it actionable: the top 10 risks must map to concrete backlog items.
