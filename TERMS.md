# NoCap — Terms of Use & Disclaimer

**Last updated:** 28 November 2026

These Terms of Use ("**Terms**") apply to everyone who downloads, installs, copies, runs, forks or otherwise uses
NoCap: the scanner, prompts, templates, checklists, adapters, installers, GitHub Action, documentation and every
other file in this repository (together, the "**Software**"). NoCap is created and maintained by
**Sanket Santosh Vidya Manohar** and contributors (together, the "**Author**", "**we**", "**us**").

**By using the Software you agree to these Terms. If you do not agree, do not use the Software.**

These Terms work alongside the [MIT License](LICENSE). The MIT License governs your copyright permissions. These Terms
explain what the Software is and is not, and confirm where responsibility lies. If the two conflict, the
MIT License's grant of rights prevails, and the disclaimers of both apply in full.

---

## 1. What NoCap is: a development aid

NoCap is a **free, open-source helper tool** for developers. It assists with writing documentation, spotting common
security weaknesses, and preparing for compliance reviews. It provides **suggestions, checklists, templates and
automated pattern checks**, nothing more.

NoCap is **not**:
- a security guarantee, certification, penetration test or professional security audit;
- legal, regulatory, compliance, privacy, financial, medical or any other professional advice;
- a substitute for qualified security engineers, auditors, lawyers or data-protection officers;
- a product or service with any support, maintenance or uptime commitment.

A good score, an "A+" grade, a clean report or a "GO" verdict **does not mean** your software is secure, compliant,
bug-free or fit for production. It only means that the checks NoCap performs did not report issues. Many serious
problems, including business-logic flaws, authorisation design errors, zero-day vulnerabilities, misconfigured infrastructure
and vulnerable dependencies, **can and will go undetected**.

## 2. Your responsibility: final checks are yours

**You alone are responsible** for your code, your applications, your data, your users and your decisions. In particular,
you are solely responsible for:

1. **Reviewing and verifying** every finding, suggestion, fix, document and code change produced by NoCap or by any AI
   assistant using NoCap's instructions, before you rely on it, merge it or deploy it;
2. **Testing** your software, including security testing, before release;
3. **Final security and quality checks** before any deployment, launch or release;
4. **Determining which laws, regulations and standards apply** to you (for example GDPR, India's DPDP Act 2023 and Rules
   2025, CCPA/CPRA, HIPAA, PCI DSS, SOC 2, ISO 27001, WCAG and the EU AI Act) and ensuring you comply with them, with qualified
   professional advice where appropriate;
5. **Protecting secrets and data**, including rotating any credentials that were exposed, whether or not NoCap detected them;
6. **Backing up** your code and data before running any tool, installer or AI-generated change;
7. Complying with the terms of every **third-party tool, AI service, platform and dependency** you use with NoCap.

## 3. AI-generated output

NoCap's prompts and rules are designed to be used with third-party AI assistants (for example Cursor, Claude Code, GitHub
Copilot, ChatGPT, Gemini, Windsurf and others). **We do not control those AI systems.** AI output can be incomplete,
outdated, inaccurate or entirely made up ("hallucinated"), and can introduce new bugs or vulnerabilities. Any
documentation, audit, compliance analysis, score or code produced by an AI assistant is **the output of that third-party
system, not of the Author**, and must be independently verified by you. Your use of any AI service is governed solely
by that service's own terms and privacy policy.

## 4. No warranty

THE SOFTWARE IS PROVIDED **"AS IS" AND "AS AVAILABLE", WITHOUT WARRANTY OF ANY KIND**, EXPRESS, IMPLIED OR STATUTORY,
INCLUDING BUT NOT LIMITED TO WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, ACCURACY, COMPLETENESS,
RELIABILITY, SECURITY, NON-INFRINGEMENT, AND ANY WARRANTY THAT THE SOFTWARE WILL DETECT ANY OR ALL VULNERABILITIES,
ERRORS OR COMPLIANCE GAPS, OR WILL OPERATE WITHOUT INTERRUPTION OR ERROR. Standards, laws and dates referenced in the
Software may change or contain errors. Always check the official sources.

## 5. Limitation of liability

TO THE MAXIMUM EXTENT PERMITTED BY APPLICABLE LAW, **IN NO EVENT SHALL THE AUTHOR OR ANY CONTRIBUTOR BE LIABLE** FOR ANY
CLAIM, LOSS OR DAMAGE OF ANY KIND, WHETHER DIRECT, INDIRECT, INCIDENTAL, SPECIAL, CONSEQUENTIAL, EXEMPLARY OR PUNITIVE,
INCLUDING BUT NOT LIMITED TO: SECURITY BREACHES OR INCIDENTS; DATA LOSS, CORRUPTION OR LEAKAGE; LEAKED OR MISUSED
CREDENTIALS; REGULATORY FINES, PENALTIES OR SANCTIONS; LEGAL CLAIMS BY YOUR USERS OR THIRD PARTIES; LOSS OF PROFITS,
REVENUE, BUSINESS, GOODWILL OR REPUTATION; SERVICE DOWNTIME; OR COSTS OF REMEDIATION OR SUBSTITUTE SERVICES, ARISING
OUT OF OR IN CONNECTION WITH THE SOFTWARE, ITS OUTPUT, ANY AI OUTPUT PRODUCED USING IT, OR ANY RELIANCE ON ANY OF THEM,
WHETHER IN CONTRACT, TORT (INCLUDING NEGLIGENCE), STRICT LIABILITY OR OTHERWISE, EVEN IF ADVISED OF THE POSSIBILITY OF
SUCH DAMAGE.

Where applicable law does not allow a full exclusion of liability, the Author's total aggregate liability is limited to
the amount you paid for the Software, which is **zero (₹0 / $0)**.

## 6. Indemnity

You agree to **defend, indemnify and hold harmless** the Author and contributors from and against any claims, damages,
losses, liabilities, penalties, costs and expenses (including reasonable legal fees) arising from or related to your use
of the Software, your software or products, your data, your violation of these Terms, or your violation of any law or
third-party right.

## 7. Acceptable use

Use NoCap only on code, systems and data that **you own or are explicitly authorised to test**. Do not use the Software
to attack, scan or analyse systems without permission, or for any unlawful purpose. You are responsible for
ensuring your use is lawful where you are.

## 8. Privacy

The NoCap scanner runs **locally on your machine**, makes **no network connections** and collects **no telemetry**. The
Author does not receive, store or process your code or data. When you use NoCap with an AI assistant, CI service
or other platform, that provider may process your code under its own terms. You are responsible for that choice.

## 9. Third-party names and standards

OWASP®, product names, company names and standards referenced in the Software belong to their respective owners. Their
mention is for identification and interoperability only and does not imply affiliation, endorsement or sponsorship.
NoCap is an independent project and is not affiliated with OWASP or with any AI, IDE or cloud vendor.

## 10. Contributions

By submitting a contribution (code, rules, docs, issues or pull requests), you confirm that you have the right to submit
it and you license it under the MIT License. These Terms, including the disclaimers and limitation of liability, also
protect contributors.

## 11. Changes, severability and governing law

- We may update these Terms at any time by committing a new version to this repository. Continued use after an update
  means you accept the updated Terms.
- If any provision is held unenforceable, it will be enforced to the maximum extent permissible, and the remaining
  provisions stay in full force.
- These Terms are governed by the laws of **India**, without regard to conflict-of-law rules, except where mandatory
  consumer-protection law in your country provides otherwise.
- No failure to enforce any provision is a waiver of it.

## 12. Summary in plain words

> 🧢 **NoCap is a free helper. It can miss things and so can AI. Check everything yourself before you ship.
> You are responsible for your app, your data and your compliance. We are not liable for anything that happens
> from using it.**

---

*Questions about these Terms: open an issue or contact sanketsmanohar1@gmail.com.*
