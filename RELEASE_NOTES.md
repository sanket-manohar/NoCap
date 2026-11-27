# NoCap v1.0.0 🧢

**Your AI wrote the code. NoCap tells you the truth about it.**

The first public release of NoCap: one toolkit that makes any AI assistant document your app, audit its security,
check compliance, and score it. It works in any IDE, with any AI and any language.

## Highlights
- 💬 **Plain-word commands** in any AI tool: `nocap docs`, `nocap audit`, `nocap fix`, `nocap compliance dpdp`, `nocap ship`
- 📋 **Zero-install mode**: paste `MASTER_PROMPT.md` into ChatGPT, Claude, Gemini or any chat
- 🔍 **Zero-dependency scanner**: 95 rules + project checks across 20+ languages and formats, with a standard fix for every finding
- 📚 **17 standard docs** generated from 18 templates (C4/arc42 architecture, API, ER data model, STRIDE/LINDDUN threat model, runbook…)
- ✅ **33 checklists**: OWASP Top 10:2025, API Top 10:2023, LLM Top 10:2025, ASVS 5.0, 13 languages, 5 platforms, and GDPR, India DPDP 2023 + Rules 2025, CCPA, HIPAA, PCI DSS 4.0.1, SOC 2, ISO 27001:2022, WCAG 2.2, EU AI Act
- 🧠 **12+ AI tools supported out of the box**: Claude Code, Cursor, GitHub Copilot, Windsurf, Cline, Roo, Continue, Gemini, Junie, Aider, and every `AGENTS.md` tool
- ⚙️ **Install your way**: bash, PowerShell, `npx`, or the GitHub Action
- 🏅 **Score + badge**, from A+ "it's giving secure ✨" to F "cooked 💀"

## Install
```bash
curl -fsSL https://raw.githubusercontent.com/sanket-manohar/nocap/main/install.sh | bash
```
```powershell
irm https://raw.githubusercontent.com/sanket-manohar/nocap/main/install.ps1 | iex
```
```bash
npx github:sanket-manohar/nocap init
```

## GitHub Action
```yaml
- uses: sanket-manohar/nocap@v1
  with:
    fail-on: high
```

Built by **Sanket Santosh Vidya Manohar** · MIT License
