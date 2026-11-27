# SQL & Databases (Postgres, MySQL, SQL Server, MongoDB, Redis) — Security & Standards Checklist

## Checks and standard fixes
- [ ] **Least privilege** → app user has only needed DML; no superuser; separate migration user; read-only user for reporting/LLM agents
- [ ] **Network** → DB not publicly reachable; private network/VPC; TLS required (`sslmode=verify-full`)
- [ ] **Row Level Security** → Postgres RLS for multi-tenant/BaaS: `ALTER TABLE t ENABLE ROW LEVEL SECURITY` + policies; `FORCE ROW LEVEL SECURITY` for owners
- [ ] **Encryption** → at rest (managed), field-level for highly sensitive columns (pgcrypto/app-level)
- [ ] **Backups** → automated, encrypted, off-site, **restore tested**; PITR enabled
- [ ] **Migrations** → versioned, reviewed, reversible; no destructive changes without backup
- [ ] **Auditing** → log DDL and privileged access (pgaudit)
- [ ] **MongoDB** → auth enabled, no `0.0.0.0` bind without firewall, schema validation, sanitize operators
- [ ] **Redis** → `requirepass`/ACLs, not exposed publicly, `rename-command` for dangerous commands, TLS
- [ ] **Performance-as-security** → statement timeouts, connection limits, indexes for auth lookups, pagination limits

## Correct pattern
```sql
-- ✅ Supabase/Postgres owner-scoped RLS
alter table public.notes enable row level security;
create policy "owner can read"   on public.notes for select using ( auth.uid() = user_id );
create policy "owner can insert" on public.notes for insert with check ( auth.uid() = user_id );
create policy "owner can update" on public.notes for update using ( auth.uid() = user_id ) with check ( auth.uid() = user_id );
create policy "owner can delete" on public.notes for delete using ( auth.uid() = user_id );
```

## Tools
pgaudit, Supabase Security Advisor / `supabase db lint`, sqlfluff, cloud provider DB security recommendations.
