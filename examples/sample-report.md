# NoCap Report

> Sample output (deliberately vulnerable demo app) · NoCap Scanner v1.0.0 · 22 files scanned

## Score: **F — 0/100** · _cooked 💀 — fix the criticals first_

| Security | Documentation | Critical | High | Medium | Low | Info |
|---|---|---|---|---|---|---|
| 0/100 | 0/100 | 13 | 14 | 13 | 3 | 0 |

_Any critical finding caps the score at 49; any high finding caps it at 79._

## Detected stack

- **Languages:** JavaScript/TypeScript, Python, C/C++, Terraform/HCL, PHP, Go, Dockerfile, Java/Kotlin, Ruby, SQL
- **Platforms:** Docker, Node.js, Supabase
- **Frameworks / services:** Express, OpenAI SDK, Supabase

## Documentation coverage

| Document | Status |
|---|---|
| README | ❌ missing |
| ARCHITECTURE | ❌ missing |
| DESIGN | ❌ missing |
| MODULES | ❌ missing |
| API | ❌ missing |
| DATA_MODEL | ❌ missing |
| SECURITY | ❌ missing |
| THREAT_MODEL | ❌ missing |
| COMPLIANCE | ❌ missing |
| PRIVACY | ❌ missing |
| TESTING | ❌ missing |
| DEPLOYMENT | ❌ missing |
| RUNBOOK | ❌ missing |
| ADR | ❌ missing |
| CHANGELOG | ❌ missing |
| CONTRIBUTING | ❌ missing |
| LICENSE | ❌ missing |

> Generate missing docs: open your AI assistant and say **`nocap docs`** (or paste `MASTER_PROMPT.md`).

## Findings

### 🟥 Critical (13)

#### `INJ005` SQL with request input (PHP)
_CWE-89 · A05:2025 Injection_

- `index.php:1` — `<?php echo $_GET['q']; mysqli_query($c, "SELECT * FROM u WHERE id=" . $_GET['id']); ?>`

**✅ Standard fix:** Use PDO / mysqli prepared statements with bound parameters (or Eloquent / Doctrine query builder).

#### `BAAS001` Firebase rules allow public read/write
_CWE-284 · A01:2025 Broken Access Control_

- `firestore.rules:1` — `service cloud.firestore { match /{d=**} { allow read, write: if true; } }`

**✅ Standard fix:** Require auth and ownership: allow read, write: if request.auth != null && request.auth.uid == userId; test rules with the emulator.

#### `INJ004` SQL built with fmt.Sprintf / concatenation (Go)
_CWE-89 · A05:2025 Injection_

- `main.go:1` — `db.Query(fmt.Sprintf("SELECT * FROM u WHERE id=%s", id))`

**✅ Standard fix:** Use placeholders: db.Query("SELECT ... WHERE id = $1", id).

#### `INJ003` SQL built with string concatenation (Java/Kotlin/C#)
_CWE-89 · A05:2025 Injection_

- `Main.java:1` — `stmt.executeQuery("SELECT * FROM u WHERE id=" + id);`

**✅ Standard fix:** Use PreparedStatement with ? placeholders / JPA named parameters / SqlParameter / FromSqlInterpolated. Never concatenate input into SQL.

#### `INJ006` SQL with string interpolation (Ruby)
_CWE-89 · A05:2025 Injection_

- `app.rb:1` — `User.where("email = '#{params[:email]}'")`

**✅ Standard fix:** Use placeholders: where('email = ?', email) or hash conditions where(email: email).

#### `INJ002` SQL built with string formatting (Python)
_CWE-89 · A05:2025 Injection_

- `app.py:2` — `cursor.execute(f"SELECT * FROM t WHERE name = '{name}'")`

**✅ Standard fix:** Use DB-API parameters: cursor.execute('SELECT ... WHERE id = %s', (user_id,)) or the ORM. Never use f-strings / % / .format / + to build SQL.

#### `INJ001` SQL built with string interpolation (JS/TS)
_CWE-89 · A05:2025 Injection_

- `src/db.js:1` — `const r = await pool.query('SELECT * FROM users WHERE id = ${req.params.id}');`

**✅ Standard fix:** Use parameterized queries / prepared statements (pg: query('... $1', [v]); Prisma: $queryRaw tagged template or the query builder; Knex: bindings). Never interpolate user input into SQL.

#### `SEC013` Secret exposed to the browser via public env prefix
_CWE-200 · A01:2025 Broken Access Control_

- `src/env.js:1` — `const k = process.env.NEXT_P…[redacted 26 chars];`

**✅ Standard fix:** Anything prefixed NEXT_PUBLIC_/VITE_/REACT_APP_/EXPO_PUBLIC_ is compiled into the JS bundle and readable by every visitor. Rename it without the public prefix and call the third-party API from a server route / edge function instead.

#### `INJ012` Shell command built from interpolated input (Node)
_CWE-78 · A05:2025 Injection_

- `src/run.js:1` — `exec('git log ${req.query.ref}');`

**✅ Standard fix:** Use execFile/spawn with an argument array and shell:false; validate input against an allow-list.

#### `SEC005` OpenAI API key
_CWE-798 · A04:2025 Cryptographic Failures_

- `src/cfg.js:1` — `const OPENAI = 'sk-pro…[redacted 56 chars]';`

**✅ Standard fix:** Remove the secret from source, ROTATE it immediately (assume it is leaked — git history keeps it), load it from environment variables / a secrets manager (Vault, AWS Secrets Manager, Doppler, 1Password, GitHub Encrypted Secrets), and add a pre-commit secret scanner (gitleaks / trufflehog). Purge history with git-filter-repo if the repo was public.

#### `SEC001` AWS access key ID
_CWE-798 · A04:2025 Cryptographic Failures_

- `src/aws.py:1` — `KEY = 'AKIAZZ…[redacted 20 chars]'`

**✅ Standard fix:** Remove the secret from source, ROTATE it immediately (assume it is leaked — git history keeps it), load it from environment variables / a secrets manager (Vault, AWS Secrets Manager, Doppler, 1Password, GitHub Encrypted Secrets), and add a pre-commit secret scanner (gitleaks / trufflehog). Purge history with git-filter-repo if the repo was public.

#### `BAAS002` Row Level Security disabled (Postgres/Supabase)
_CWE-284 · A01:2025 Broken Access Control_

- `supabase/migrations/1.sql:2` — `alter table notes disable row level security;`

**✅ Standard fix:** Enable RLS on every table in an exposed schema and write explicit policies (auth.uid() = user_id).

#### `HYG002` .env file present but not git-ignored
_CWE-538 · A02:2025 Security Misconfiguration_

- `.env` — `.env`

**✅ Standard fix:** Add `.env*` (and `!.env.example`) to .gitignore, run `git rm --cached .env`, rotate every secret in it.

### 🟧 High (14)

#### `MEM001` Unsafe C string function
_CWE-120 · A06:2025 Insecure Design_

- `x.c:1` — `char b[8]; gets(b); strcpy(b, s);`

**✅ Standard fix:** Use bounded versions (fgets, snprintf, strlcpy/strncpy with explicit termination) or std::string; compile with -D_FORTIFY_SOURCE=2 and sanitizers.

#### `IAC007` Public storage bucket / public database
_CWE-284 · A01:2025 Broken Access Control_

- `main.tf:1` — `resource "aws_s3_bucket" "b" { acl = "public-read" }`

**✅ Standard fix:** Keep buckets and databases private; serve public assets through a CDN with origin access control.

#### `XSS004` Echoing request input (PHP)
_CWE-79 · A05:2025 Injection_

- `index.php:1` — `<?php echo $_GET['q']; mysqli_query($c, "SELECT * FROM u WHERE id=" . $_GET['id']); ?>`

**✅ Standard fix:** Escape output: htmlspecialchars($v, ENT_QUOTES, 'UTF-8'), or use a templating engine (Blade/Twig).

#### `TLS001` TLS certificate verification disabled
_CWE-295 · A04:2025 Cryptographic Failures_

- `main.go:2` — `tls.Config{InsecureSkipVerify: true}`
- `app.py:7` — `requests.get(url, verify=False)`

**✅ Standard fix:** Never disable certificate validation. Fix the trust store / use the correct CA bundle instead.

#### `IAC002` Secret baked into image via ENV/ARG
_CWE-798 · A04:2025 Cryptographic Failures_

- `Dockerfile:2` — `ENV API_SECRET=abc123456`

**✅ Standard fix:** Use BuildKit secrets (RUN --mount=type=secret) at build time and inject runtime secrets via the orchestrator.

#### `INJ007` SQL concatenation with a string literal
_CWE-89 · A05:2025 Injection_

- `Main.java:1` — `stmt.executeQuery("SELECT * FROM u WHERE id=" + id);`

**✅ Standard fix:** Use parameterized queries. Concatenating variables into SQL enables SQL injection.

#### `MOB001` Android cleartext traffic / debuggable build
_CWE-319 · A02:2025 Security Misconfiguration_

- `AndroidManifest.xml:1` — `<application android:usesCleartextTraffic="true" android:allowBackup="true">`

**✅ Standard fix:** Disable cleartext and debuggable in release builds; use a Network Security Config with HTTPS only.

#### `INJ013` Shell execution (Python)
_CWE-78 · A05:2025 Injection_

- `app.py:3` — `os.system('rm ' + path)`

**✅ Standard fix:** Use subprocess.run([...args], shell=False, check=True) with an argument list; never pass user input to a shell.

#### `DES001` Unsafe deserialization (Python)
_CWE-502 · A08:2025 Software or Data Integrity Failures_

- `app.py:4` — `data = pickle.loads(blob)`

**✅ Standard fix:** Never unpickle untrusted data. Use JSON / msgpack; for models use safetensors or torch.load(weights_only=True).

#### `DES002` yaml.load without SafeLoader
_CWE-502 · A08:2025 Software or Data Integrity Failures_

- `app.py:5` — `cfg = yaml.load(open('c.yml'))`

**✅ Standard fix:** Use yaml.safe_load().

#### `AI001` LLM SDK used directly in the browser (API key exposed)
_CWE-522 · LLM02:2025 Sensitive Information Disclosure_

- `src/ai.js:1` — `const client = new OpenAI({ apiKey: k, dangerouslyAllowBrowser: true });`

**✅ Standard fix:** Never call OpenAI/Anthropic/etc. from the client. Create a server route that holds the key, authenticates the user, rate-limits, and proxies the request.

#### `IAC009` GitHub Actions script injection from untrusted event data
_CWE-78 · A08:2025 Software or Data Integrity Failures_

- `.github/workflows/ci.yml:5` — `- run: echo "${{ github.event.issue.title }}"`

**✅ Standard fix:** Pass untrusted values through env: variables and reference them as "$VAR" in run: steps.

#### `BAAS004` 1 of 1 tables may lack Row Level Security
_CWE-284 · A01:2025 Broken Access Control_

- `supabase/` — `create table: 1, enable RLS: 0`

**✅ Standard fix:** Run `alter table <t> enable row level security;` for every table and add owner-scoped policies.

### 🟨 Medium (13)

#### `IAC006` Ingress open to the whole internet (0.0.0.0/0)
_CWE-284 · A02:2025 Security Misconfiguration_

- `main.tf:2` — `ingress { cidr_blocks = ["0.0.0.0/0"] }`

**✅ Standard fix:** Restrict security groups to known CIDRs; never expose SSH/RDP/DB ports publicly — use a bastion, VPN or SSM.

#### `IAC011` Container runs as root (no non-root USER)
_CWE-250 · A02:2025 Security Misconfiguration_

- `Dockerfile:1` — `no USER instruction`

**✅ Standard fix:** Add a dedicated user: RUN adduser -D app && USER app (or USER node / USER nonroot for distroless).

#### `IAC003` curl | sh remote script execution
_CWE-494 · A08:2025 Software or Data Integrity Failures_

- `Dockerfile:3` — `RUN curl https://x.sh | sh`

**✅ Standard fix:** Download, verify a checksum/signature, then execute; or use a package manager.

#### `DEP001` Unpinned dependency 'openai': "*"
_CWE-1104 · A03:2025 Software Supply Chain Failures_

- `package.json:1` — `"openai": "*"`

**✅ Standard fix:** Pin versions (^x.y.z at minimum), commit the lockfile and use `npm ci` in CI.

#### `MOB002` Android allowBackup enabled
_CWE-530 · A02:2025 Security Misconfiguration_

- `AndroidManifest.xml:1` — `<application android:usesCleartextTraffic="true" android:allowBackup="true">`

**✅ Standard fix:** Set allowBackup=false or define dataExtractionRules excluding sensitive files.

#### `CRY001` Weak hash (MD5/SHA-1)
_CWE-328 · A04:2025 Cryptographic Failures_

- `app.py:6` — `h = hashlib.md5(pw.encode())`

**✅ Standard fix:** Use SHA-256+ for integrity. For PASSWORDS use a slow KDF: Argon2id (preferred), scrypt or bcrypt (cost>=12). Never MD5/SHA for passwords.

#### `WEB003` Debug mode enabled
_CWE-489 · A02:2025 Security Misconfiguration_

- `app.py:8` — `DEBUG = True`

**✅ Standard fix:** Drive debug flags from environment and make sure they are OFF in production; never expose stack traces to users.

#### `XSS002` dangerouslySetInnerHTML / v-html / {@html}
_CWE-79 · A05:2025 Injection_

- `src/ui.jsx:1` — `<div dangerouslySetInnerHTML={{__html: bio}} />`

**✅ Standard fix:** Render as text, or sanitize with DOMPurify (isomorphic-dompurify on the server) immediately before rendering.

#### `CRY003` Non-cryptographic RNG used for a secret
_CWE-338 · A04:2025 Cryptographic Failures_

- `src/auth.js:2` — `const t = Math.random().toString(36); // reset token`

**✅ Standard fix:** Use a CSPRNG: crypto.randomUUID()/crypto.getRandomValues (JS), secrets.token_urlsafe (Python), SecureRandom (Java/Ruby), crypto/rand (Go), random_bytes (PHP).

#### `WEB010` Auth token stored in localStorage/sessionStorage
_CWE-922 · A07:2025 Authentication Failures_

- `src/auth.js:1` — `localStorage.setItem('token', jwt);`

**✅ Standard fix:** Store session tokens in HttpOnly, Secure, SameSite cookies so XSS cannot steal them.

#### `HYG001` No .gitignore — secrets and build output may be committed
_CWE-538 · A02:2025 Security Misconfiguration_

- `.gitignore` — `missing`

**✅ Standard fix:** Add a .gitignore covering .env*, keys, build output and dependency folders.

#### `HYG004` Node.js project without a lockfile
_CWE-1104 · A03:2025 Software Supply Chain Failures_

- `/` — `expected one of: package-lock.json, yarn.lock, pnpm-lock.yaml, bun.lockb, bun.lock`

**✅ Standard fix:** Commit the lockfile so builds are reproducible and dependency audits are meaningful.

#### `HYG006` No automated tests found
_CWE-1164 · A06:2025 Insecure Design_

- `/` — `missing`

**✅ Standard fix:** Add unit tests for business logic and integration tests for auth/permissions — especially negative cases (user A cannot read user B's data).

### 🟦 Low (3)

#### `IAC001` Docker image uses 'latest' or no tag
_CWE-1104 · A03:2025 Software Supply Chain Failures_

- `Dockerfile:1` — `FROM node:latest`

**✅ Standard fix:** Pin images to a version and ideally a digest (node:20.11-alpine@sha256:...). Rebuild regularly for patches.

#### `HYG003` No .env.example documenting required configuration
_CWE-1059 · A02:2025 Security Misconfiguration_

- `.env.example` — `missing`

**✅ Standard fix:** Commit a .env.example with every variable name and a safe placeholder value.

#### `HYG005` No automated dependency updates (Dependabot/Renovate)
_CWE-1104 · A03:2025 Software Supply Chain Failures_

- `/` — `missing`

**✅ Standard fix:** Enable Dependabot or Renovate plus security alerts.

## Next: manual review checklists for your stack

- [ ] `checklists/security/OWASP_TOP10_2025.md`
- [ ] `checklists/security/VIBE_CODING_TOP25.md`
- [ ] `checklists/quality/DESIGN_QUALITY.md`
- [ ] `checklists/languages/JAVASCRIPT_TYPESCRIPT.md`
- [ ] `checklists/languages/PYTHON.md`
- [ ] `checklists/languages/C_CPP.md`
- [ ] `checklists/languages/PHP.md`
- [ ] `checklists/languages/GO.md`
- [ ] `checklists/languages/JAVA_KOTLIN.md`
- [ ] `checklists/languages/RUBY.md`
- [ ] `checklists/languages/SQL_DATABASES.md`
- [ ] `checklists/security/OWASP_API_TOP10_2023.md`
- [ ] `checklists/platforms/CLOUD_CONTAINERS_IAC.md`
- [ ] `checklists/security/OWASP_LLM_TOP10_2025.md`
- [ ] `checklists/platforms/BAAS_SUPABASE_FIREBASE.md`

## Compliance frameworks to review

- [ ] `checklists/compliance/EU_AI_ACT.md`
- [ ] `checklists/compliance/GDPR.md`
- [ ] `checklists/compliance/INDIA_DPDP.md`
- [ ] `checklists/compliance/WCAG_2_2_ACCESSIBILITY.md`

## Also run (dependency CVEs need a live database)

- `npx osv-scanner -r .` or `osv-scanner scan source -r .` (all ecosystems)
- `npm audit --omit=dev` · `pip-audit` · `bundle audit` · `composer audit` · `cargo audit` · `govulncheck ./...`
- `gitleaks detect` (scans full git history for secrets)
- Semgrep / CodeQL for deeper SAST, OWASP ZAP for DAST on a staging URL

---
_⚠️ **Disclaimer:** NoCap is a development aid, not a guarantee. A clean report or high score does **not** mean the software is secure or compliant. Final verification, testing and compliance are the user's own responsibility. Provided "as is" without warranty; the author accepts no liability. See TERMS.md._
