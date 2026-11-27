# 🔥 The 25 Ways Vibe-Coded Apps Get Hacked

The issues that come up again and again in apps built fast with AI assistants. Each item says what goes wrong and the standard fix.
Run `nocap audit` to check all 25 automatically and manually.

| # | What goes wrong | Why AI does it | ✅ Standard fix |
|---|---|---|---|
| 1 | **API keys hard-coded** in source | The fastest way to make the demo work | Env vars + secrets manager. Rotate any key that was ever committed |
| 2 | **Secrets in the frontend** via `NEXT_PUBLIC_` / `VITE_` / `REACT_APP_` | "Make the env var available" | Call third-party APIs from a server route. Only truly public values get public prefixes |
| 3 | **OpenAI/Anthropic SDK called from the browser** (`dangerouslyAllowBrowser: true`) | No backend in the prototype | Server or edge proxy with auth, rate limits and spend caps |
| 4 | **Supabase tables without Row Level Security** | RLS policies are extra work | `enable row level security` on every table plus `auth.uid()`-scoped policies |
| 5 | **Supabase `service_role` key in client code** | "Permission denied" errors go away | Anon key on the client. service_role only on the server |
| 6 | **Firebase rules `allow read, write: if true`** | Test-mode rules never get changed | Auth- and ownership-based rules, tested in the emulator |
| 7 | **Auth checked only in the UI** (hidden button = "secure") | Generating UI is easier than enforcing access | Enforce on every API route / server action / DB policy |
| 8 | **IDOR**: `/api/orders/123` returns anyone's order | The happy path never tests other users | `WHERE id = ? AND user_id = currentUser` plus negative tests |
| 9 | **Mass assignment**: `update(req.body)` lets users set `role: "admin"` | Shortest code | Allow-list fields with a schema (zod/pydantic/DTO) |
| 10 | **No rate limiting** on login, OTP, signup or AI endpoints | Not visible in a demo | Rate limit + lockout/backoff + CAPTCHA on abuse-prone flows |
| 11 | **SQL built with template strings** | Looks readable | Parameterised queries / ORM |
| 12 | **No server-side input validation** | Frontend validation "already exists" | Schema validation at every boundary |
| 13 | **`dangerouslySetInnerHTML` / `v-html` with user content** | Rich text rendering | Sanitise with DOMPurify, or render as text |
| 14 | **JWT in localStorage** | Copied from tutorials | HttpOnly Secure SameSite cookies |
| 15 | **CORS `*`** | Fixes the CORS error instantly | Exact origin allow-list |
| 16 | **Debug mode / verbose errors in production** | Left on from development | Env-driven config. Generic errors plus server logs |
| 17 | **Hallucinated or typosquatted packages** ("slopsquatting") | The model invents plausible names | Verify every package on its registry before installing. Use a lockfile |
| 18 | **Outdated dependencies with known CVEs** | Training data is old | Dependabot/Renovate plus `osv-scanner` in CI |
| 19 | **Webhooks without signature verification** (Stripe/Razorpay) | The happy path works without it | Verify the HMAC signature with the provider SDK and reject replays |
| 20 | **Client-side price/total calculation** trusted by the server | Simple cart logic | Recalculate prices on the server from the DB |
| 21 | **Unrestricted file uploads** (type, size, path) | "Upload works" | Size limits, magic-byte checks, random names, private bucket + signed URLs |
| 22 | **Missing security headers** (CSP, HSTS, frame-ancestors) | Not part of the feature | Helmet / framework middleware / platform header config |
| 23 | **`.env` committed** or no `.gitignore` | New repo, first commit | `.gitignore` before the first commit. If already committed: purge history and rotate keys |
| 24 | **No logging/alerting**, so breaches go unnoticed | Not a feature | Error tracking, auth event logs, alerts to a human |
| 25 | **LLM output executed or rendered raw**, and prompt injection via RAG content | "Let the AI do it" | Treat output as untrusted, use least-agency tools, human approval for actions |

> Share this list. Most of these take minutes to fix and cause real breaches when ignored.
