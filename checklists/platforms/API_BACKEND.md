# API & Backend Checklist (REST, GraphQL, gRPC, serverless)

- [ ] OpenAPI 3.1 / GraphQL schema is the source of truth and matches the code
- [ ] AuthN on every non-public route. AuthZ at object, function and property level
- [ ] Schema validation on requests. Response DTOs avoid over-exposure
- [ ] Rate limiting (per IP, per user, per API key), request size limits, timeouts
- [ ] Pagination with max page size. No unbounded queries
- [ ] Idempotency keys for payment and create endpoints
- [ ] Errors in RFC 9457 problem+json, with no stack traces
- [ ] CORS allow-list. HTTPS only
- [ ] Webhooks: signature verification, replay protection (timestamp tolerance), idempotent processing
- [ ] Background jobs: re-check authorisation, handle retries and poison messages
- [ ] Serverless: least-privilege role per function, secrets from a manager, concurrency limits, cold-start-safe init
- [ ] GraphQL: depth/complexity limits, introspection disabled or protected in prod, field-level auth, batching limits
- [ ] Health endpoints reveal nothing sensitive. Admin/metrics/docs endpoints protected
- [ ] API versioning and deprecation policy. Old versions retired (inventory)

**Tools:** OWASP ZAP, Schemathesis (property-based API fuzzing), 42Crunch, Burp Suite, k6 for load tests.
