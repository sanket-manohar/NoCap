# PCI DSS v4.0.1 — Engineering Checklist

> Not legal advice. All future-dated requirements became mandatory on **31 March 2025**.
> **Best strategy: keep card data off your systems.** Use hosted fields/checkout (Stripe Checkout/Elements, Razorpay Checkout,
> Adyen Drop-in, Braintree Hosted Fields). That greatly reduces scope (often to SAQ A).

## Scope reduction
- [ ] PAN never touches your servers, logs or DB (only tokens from the provider)
- [ ] Payment page scripts inventoried, authorised and integrity-checked (**Req. 6.4.3**)
- [ ] Change/tamper detection for payment page HTTP headers and content (**Req. 11.6.1**)
- [ ] Webhooks verified by signature

## The 12 requirements (summary)
1. [ ] Network security controls (firewalls, segmentation of the cardholder data environment)
2. [ ] Secure configurations, no vendor defaults
3. [ ] Protect stored account data (don't store SAD after authorisation; render PAN unreadable)
4. [ ] Strong cryptography for PAN in transit over open networks
5. [ ] Anti-malware protection; anti-phishing mechanisms
6. [ ] Secure development: secure SDLC, code review, vulnerability management, WAF or automated tooling for public web apps (6.4.2)
7. [ ] Restrict access by business need-to-know
8. [ ] Identify users and authenticate. **MFA for all access into the CDE** (8.4.2), passwords ≥ 12 characters
9. [ ] Restrict physical access
10. [ ] Log and monitor all access. Automated log review (10.4.1.1)
11. [ ] Test security regularly: ASV scans quarterly, internal/external penetration testing, change detection
12. [ ] Information security policy, risk assessments (targeted risk analysis), incident response, third-party service provider management

**Determine your SAQ type** (A, A-EP, D…) with your acquirer or a QSA.
