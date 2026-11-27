# Supabase / Firebase / BaaS Checklist

These platforms let the client talk to the database directly, so **the database rules are your backend**.

## Supabase
- [ ] RLS **enabled on every table** in exposed schemas (`public`, any schema listed in the API settings)
- [ ] Policies scoped to `auth.uid()`. No `using (true)` except for truly public read-only data
- [ ] Separate policies for select/insert/update/delete. `with check` on insert and update
- [ ] `service_role` key only in server env (edge functions, backend). Never in the client or a public env var
- [ ] Storage buckets private by default, with storage policies per bucket/path
- [ ] `security definer` functions have `set search_path = ''` and check `auth.uid()` internally
- [ ] Views use `security_invoker = true` (Postgres 15+) so they don't bypass RLS
- [ ] Email confirmation on. Leaked-password protection, MFA and rate limits configured in Auth settings
- [ ] Security Advisor / `supabase db lint` warnings resolved
- [ ] Point-in-time recovery or backups enabled for production

## Firebase
- [ ] Firestore, Realtime Database and Storage rules are **not** in test mode. No `if true`
- [ ] Rules check `request.auth != null` **and** ownership (`request.auth.uid == resource.data.ownerId`)
- [ ] Rules validate data shape and types on write (`request.resource.data.keys().hasOnly([...])`)
- [ ] Rules unit-tested with the Emulator Suite in CI
- [ ] App Check enforced on Firestore, Storage, Functions and Auth
- [ ] Browser API key restricted by HTTP referrer and API scope in Google Cloud Console
- [ ] Admin SDK credentials only on the server. Cloud Functions validate `context.auth`
- [ ] Budget alerts on (an open DB or Functions can create huge bills)

## Any BaaS (Appwrite, PocketBase, Convex, Amplify…)
- [ ] Collection/table permissions reviewed per role
- [ ] No admin or master keys in clients
- [ ] Server functions re-check auth and validate input
