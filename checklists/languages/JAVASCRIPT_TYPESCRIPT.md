# JavaScript / TypeScript (Node, React, Next.js, Vue, Svelte, Express, NestJS) — Security & Standards Checklist

## Checks and standard fixes
- [ ] **TypeScript strict mode** → `"strict": true`, no `any` at trust boundaries
- [ ] **Input validation** → zod / valibot / class-validator at every route, server action and webhook
- [ ] **SQL/ORM** → Prisma/Drizzle/Knex query builders; `$queryRaw` tagged template only, never `$queryRawUnsafe` with input
- [ ] **NoSQL injection** → reject non-string values (`{ $ne: null }`); `express-mongo-sanitize`; `mongoose.set('sanitizeFilter', true)`
- [ ] **Command execution** → `execFile`/`spawn` with arg arrays; never `exec` with template strings
- [ ] **XSS** → React escapes by default; avoid `dangerouslySetInnerHTML`/`v-html`; sanitize with DOMPurify; strict CSP with nonces
- [ ] **Next.js server actions & route handlers** → authenticate + authorise *inside* every action/handler; middleware alone is not enough
- [ ] **Secrets exposure** → only non-secret values in `NEXT_PUBLIC_`/`VITE_`; mark server-only modules with `import 'server-only'`
- [ ] **Security headers** → `helmet()` for Express; `headers()` in `next.config.js`; CSP via middleware
- [ ] **Rate limiting** → `express-rate-limit`, `@upstash/ratelimit`, NestJS `ThrottlerModule`
- [ ] **Sessions/JWT** → HttpOnly cookies; `jose`/`jsonwebtoken.verify` with `algorithms`; never `jwt.decode` for auth
- [ ] **Prototype pollution** → avoid deep-merge of user objects; use `Object.create(null)` / `Map`; validate keys
- [ ] **ReDoS** → avoid catastrophic regex on user input; use `re2` or limits
- [ ] **Path traversal** → `path.resolve` + `startsWith(baseDir)` check; never `res.sendFile(req.query.f)`
- [ ] **Dependencies** → lockfile + `npm ci`; `npm audit --omit=dev`; check package exists/maintained before install; `--ignore-scripts` where possible
- [ ] **Error handling** → central error middleware; no `res.send(err)`; handle promise rejections
- [ ] **Source maps** → don't publish production source maps publicly

## Correct pattern
```ts
// ✅ Next.js route handler: validate, authenticate, authorise, parameterise
import { z } from "zod";
const Body = z.object({ title: z.string().min(1).max(200) });
export async function PATCH(req: Request, { params }: { params: { id: string } }) {
  const session = await auth();                      // 1. authenticate
  if (!session) return new Response(null, { status: 401 });
  const body = Body.safeParse(await req.json());     // 2. validate
  if (!body.success) return Response.json(body.error.flatten(), { status: 400 });
  const note = await db.note.updateMany({            // 3. authorise by ownership in the query
    where: { id: params.id, ownerId: session.user.id },
    data: { title: body.data.title },                // 4. allow-listed fields only
  });
  if (note.count === 0) return new Response(null, { status: 404 });
  return new Response(null, { status: 204 });
}
```

## Tools
ESLint + `eslint-plugin-security`, `typescript-eslint` strict, Semgrep, `npm audit`, osv-scanner, Socket.dev, Snyk.
