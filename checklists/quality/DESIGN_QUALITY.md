# Design & Code Quality Checklist

Rate each 1–5 with evidence. Aligned with ISO/IEC 25010 quality characteristics.

## Architecture
- [ ] Clear layers/boundaries (UI → application → domain → infrastructure); dependencies point inward
- [ ] Modules have a single responsibility and a small public interface
- [ ] No circular dependencies. No god files (> 500 lines is a smell)
- [ ] Shared code lives in a deliberate place, not copy-pasted
- [ ] Significant decisions are recorded as ADRs

## Code
- [ ] Consistent naming, formatting (Prettier/Black/gofmt/rustfmt) and linting in CI
- [ ] Typed boundaries (TypeScript strict, type hints, DTOs)
- [ ] Functions are short and do one thing. Low cyclomatic complexity
- [ ] No dead code, commented-out blocks or stray TODOs without tickets
- [ ] SOLID / composition over inheritance where it helps clarity

## Reliability
- [ ] Consistent error-handling strategy. Fail closed on security paths
- [ ] Timeouts, retries with backoff and circuit breakers for external calls
- [ ] Idempotent handlers for retries, webhooks and jobs
- [ ] Transactions around multi-step writes

## Performance & scalability
- [ ] No N+1 queries. Indexes match query patterns
- [ ] Caching with explicit invalidation
- [ ] Stateless app servers (12-factor). Sessions in a shared store
- [ ] Heavy work in background jobs or queues
- [ ] Load-tested on the critical path (k6/Locust/Gatling)

## Operability (12-factor + observability)
- [ ] Config in env. Same build artifact across environments
- [ ] Structured logs, metrics (RED/USE) and traces (OpenTelemetry)
- [ ] Health/readiness endpoints. Graceful shutdown
- [ ] Dashboards and alerts tied to SLOs

## Testability
- [ ] Unit tests for domain logic. Integration tests for DB and auth rules. E2E for critical journeys
- [ ] Tests run in CI in under 10 minutes. Flaky tests quarantined and fixed
- [ ] Test data factories. No production data in tests

## Documentation
- [ ] NoCap docs score ≥ 80
- [ ] README quick start works on a clean machine
- [ ] Public functions and APIs documented
