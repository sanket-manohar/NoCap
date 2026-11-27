# API Reference

> **Audience:** Frontend/mobile devs, integrators, security reviewers
> **TL;DR:** _3 lines max — what this document tells the reader._
> **Last verified:** YYYY-MM-DD · commit `abc1234` · Owner: @name

Base URL: `https://api.example.com/v1` · Auth: … · Format: JSON · Spec: `openapi.yaml` (OpenAPI 3.1)

## Conventions
Errors (RFC 9457 problem+json recommended), pagination (`limit` ≤ 100, cursor), idempotency keys, versioning, rate limits.

## Endpoint index
| Method | Path | Auth | Roles | Rate limit | Description |
|---|---|---|---|---|---|

## `POST /resource`
- **Auth:** required (session cookie) · **Roles:** `user` · **Ownership check:** `resource.owner_id = currentUser.id`
- **Request**
```json
{ "name": "string (1–100 chars)" }
```
- **Responses:** `201` created · `400` validation · `401` unauthenticated · `403` forbidden · `429` rate limited
```json
{ "id": "uuid", "name": "string" }
```
- **Side effects:** emails, webhooks, audit log entries.

## Webhooks (incoming)
| Source | Path | Signature verification | Replay protection |
|---|---|---|---|
