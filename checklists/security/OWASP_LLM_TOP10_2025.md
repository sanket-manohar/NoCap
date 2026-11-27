# OWASP Top 10 for LLM Applications 2025 Checklist

Source: [genai.owasp.org](https://genai.owasp.org/llm-top-10/). Use this for chatbots, RAG, agents, copilots and AI features.

- [ ] **LLM01 Prompt Injection**: treat all user input *and* retrieved content (web pages, files, emails, tool results) as untrusted. Keep instructions separate from data, constrain output formats, filter tool calls, and require human approval for high-impact actions. Red-team with injection payloads.
- [ ] **LLM02 Sensitive Information Disclosure**: no secrets or other users' data in prompts or context. Apply per-user access control *before* retrieval. Redact PII in logs. Get opt-out/zero-retention terms from the provider where needed.
- [ ] **LLM03 Supply Chain**: models, datasets, LoRAs and plugins come from trusted sources with pinned versions and checksums. Prefer `safetensors` and avoid pickle-based model files. Review model licences.
- [ ] **LLM04 Data and Model Poisoning**: vet training and fine-tuning data and the RAG corpus. Track provenance. Restrict who can write to vector stores and knowledge bases.
- [ ] **LLM05 Improper Output Handling**: encode model output before rendering (XSS). Never pass it to `eval`, shell, SQL or file paths. Validate structured output against a schema.
- [ ] **LLM06 Excessive Agency**: give tools only the minimum needed, scoped to the current user's permissions. No generic shell/SQL tools. Require confirmation for destructive or financial actions. Log every tool call.
- [ ] **LLM07 System Prompt Leakage**: assume system prompts become public. Put no secrets, credentials or authorisation logic in them. Enforce rules in code.
- [ ] **LLM08 Vector and Embedding Weaknesses**: keep tenants isolated in vector DBs (metadata filters enforced on the server), validate ingested documents, and guard against embedding inversion of sensitive data.
- [ ] **LLM09 Misinformation**: ground answers with RAG and citations, show uncertainty, add human review for high-stakes outputs (medical, legal, financial), and add disclaimers in the UI.
- [ ] **LLM10 Unbounded Consumption**: per-user rate limits, max tokens, request timeouts, budget alerts and hard spend caps, and abuse detection for scraping or model extraction.

## Architecture must-haves
- [ ] LLM API keys are **server-side only** (no `dangerouslyAllowBrowser`, no keys in mobile apps)
- [ ] An AI gateway or proxy with auth, quotas, logging and content filtering
- [ ] Evals and red-team test suite in CI for prompts
- [ ] Users are told they are interacting with AI (transparency, which the EU AI Act requires for many systems)
