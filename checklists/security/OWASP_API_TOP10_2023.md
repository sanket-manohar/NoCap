# OWASP API Security Top 10:2023 Checklist

Source: [owasp.org/API-Security](https://owasp.org/API-Security/editions/2023/en/0x11-t10/)

- [ ] **API1 Broken Object Level Authorization**: every handler that takes an ID verifies the caller may access *that* object. Use UUIDs, but don't treat them as the security control.
- [ ] **API2 Broken Authentication**: standard auth, rate-limited credential endpoints, token validation (signature, exp, aud), no API keys in URLs.
- [ ] **API3 Broken Object Property Level Authorization**: response DTOs expose only allowed fields (no over-exposure), and request DTOs accept only allowed fields (no mass assignment).
- [ ] **API4 Unrestricted Resource Consumption**: limits on rate, payload size, page size, upload size, query depth/cost, timeouts, and spend caps on paid third-party calls (SMS, email, LLM).
- [ ] **API5 Broken Function Level Authorization**: admin and privileged routes have role checks. Don't rely on "hidden" URLs.
- [ ] **API6 Unrestricted Access to Sensitive Business Flows**: anti-automation on signup, checkout, voting, booking and referrals (device fingerprinting, CAPTCHA, velocity limits).
- [ ] **API7 Server Side Request Forgery**: allow-list outbound hosts, block internal ranges, disable redirects, validate schemes.
- [ ] **API8 Security Misconfiguration**: TLS, CORS, headers, verbose errors off, unused HTTP methods disabled, consistent config.
- [ ] **API9 Improper Inventory Management**: all API versions and hosts documented (OpenAPI), old versions retired, no forgotten staging/debug endpoints exposed.
- [ ] **API10 Unsafe Consumption of APIs**: validate and sanitise third-party responses, use TLS, set timeouts, don't follow redirects blindly, limit what you trust.

**GraphQL extras:** disable introspection in prod (or protect it), depth/complexity limits, field-level authorisation, persisted queries.
**gRPC extras:** TLS/mTLS, per-method auth interceptors, message size limits.
