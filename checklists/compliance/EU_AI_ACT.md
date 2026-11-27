# EU AI Act — Engineering Checklist

> Not legal advice. The Act (Regulation (EU) 2024/1689) applies in phases: prohibitions and AI literacy from Feb 2025, general-purpose AI (GPAI)
> obligations from Aug 2025, most other obligations from Aug 2026 onward, and some high-risk obligations later. **Timelines have been subject to
> EU "digital omnibus" proposals, so check the current official dates.**

## 1. Classify your system
- [ ] **Prohibited?** (e.g. social scoring, manipulative techniques, untargeted facial scraping, emotion recognition at work or school). If so, do not build it
- [ ] **High-risk?** (Annex III: employment/HR screening, credit scoring, education access/grading, essential services, law enforcement, migration, critical infrastructure, biometrics; or a safety component of regulated products)
- [ ] **Limited risk / transparency obligations?** (chatbots, AI-generated content, deepfakes, emotion recognition)
- [ ] **Minimal risk?** (most apps). Voluntary codes apply
- [ ] Are you a **provider** (you build or brand it) or a **deployer** (you use it)?

## 2. Transparency (most AI apps)
- [ ] Tell users they are interacting with an AI system unless it is obvious
- [ ] Mark AI-generated or manipulated content (machine-readable where feasible). Disclose deepfakes
- [ ] AI literacy: staff using AI systems are adequately trained

## 3. If high-risk (provider obligations)
- [ ] Risk management system across the lifecycle
- [ ] Data governance: training/validation/test data quality and bias examination
- [ ] Technical documentation (Annex IV). NoCap ARCHITECTURE/DATA_MODEL/THREAT_MODEL are a starting point
- [ ] Automatic logging of events (record-keeping)
- [ ] Instructions for use for deployers
- [ ] Human oversight measures designed in
- [ ] Accuracy, robustness and cybersecurity (see OWASP LLM Top 10)
- [ ] Quality management system, conformity assessment, CE marking, EU database registration
- [ ] Post-market monitoring and serious-incident reporting

## 4. If you build on a GPAI model
- [ ] Keep the model provider's documentation and usage policy. Your obligations depend on whether you modify or fine-tune the model substantially
