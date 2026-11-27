#!/usr/bin/env python3
# nocap-ignore-file (this file contains the rule patterns themselves)
"""
NoCap Scanner — zero-dependency security, hygiene & documentation audit
for any codebase (especially AI-generated / "vibe-coded" ones).

    python3 nocap.py [path] [--out report.md] [--json out.json]
                         [--badge badge.svg] [--fail-on high] [--exclude GLOB]

* Pure Python 3.8+ standard library. No network. No telemetry.
* Detects your stack, scans 20+ languages / config formats for secrets and
  dangerous patterns, checks project hygiene and documentation completeness,
  and prints the standard, correct fix for every finding.
* Suppress a finding by adding `nocap-ignore` (optionally followed by the
  rule id) in a comment on the same line, or skip a whole file with a
  `nocap-ignore-file` comment in its first 5 lines.

This is a fast first line of defence, NOT a replacement for a full SAST/DAST,
dependency audit or a human penetration test. See checklists/ for the rest.
"""
from __future__ import annotations

import argparse
import fnmatch
import json
import os
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone

VERSION = "1.0.0"

# --------------------------------------------------------------------------- #
# File classification
# --------------------------------------------------------------------------- #
LANG_EXT = {
    "js": {".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs", ".vue", ".svelte", ".astro"},
    "py": {".py", ".pyw"},
    "java": {".java", ".kt", ".kts", ".scala", ".groovy"},
    "go": {".go"},
    "php": {".php", ".phtml"},
    "rb": {".rb", ".erb", ".rake"},
    "cs": {".cs", ".cshtml", ".razor", ".vb"},
    "rs": {".rs"},
    "c": {".c", ".h", ".cpp", ".cc", ".cxx", ".hpp", ".hh", ".m", ".mm"},
    "swift": {".swift"},
    "dart": {".dart"},
    "sql": {".sql"},
    "shell": {".sh", ".bash", ".zsh", ".ps1", ".bat", ".cmd"},
    "sol": {".sol"},
    "html": {".html", ".htm", ".jinja", ".jinja2", ".j2", ".hbs", ".ejs", ".njk", ".twig", ".liquid"},
    "yaml": {".yml", ".yaml"},
    "json": {".json", ".jsonc"},
    "tf": {".tf", ".hcl", ".tfvars"},
    "xml": {".xml", ".plist", ".config", ".csproj"},
    "conf": {".toml", ".ini", ".cfg", ".conf", ".properties", ".env", ".rules"},
    "md": {".md", ".mdx", ".txt"},
}
EXT_TO_LANG = {e: l for l, exts in LANG_EXT.items() for e in exts}
LANG_NAMES = {
    "js": "JavaScript/TypeScript", "py": "Python", "java": "Java/Kotlin", "go": "Go", "php": "PHP",
    "rb": "Ruby", "cs": "C#/.NET", "rs": "Rust", "c": "C/C++", "swift": "Swift", "dart": "Dart",
    "sql": "SQL", "shell": "Shell", "sol": "Solidity", "html": "HTML/Templates", "tf": "Terraform/HCL",
    "docker": "Dockerfile",
}
CODE = {"js", "py", "java", "go", "php", "rb", "cs", "rs", "c", "swift", "dart", "shell", "sol"}
ALL_TEXT = set(LANG_EXT) | {"docker"}

SKIP_DIRS = {
    ".git", "node_modules", "vendor", "venv", ".venv", "env", "__pycache__", "dist",
    "build", "out", ".next", ".nuxt", ".svelte-kit", "target", "bin", "obj", ".idea",
    ".vscode", "coverage", ".gradle", "Pods", ".dart_tool", ".terraform", ".cache",
    ".turbo", ".vercel", ".output", "bower_components", "jspm_packages", ".pytest_cache",
    ".mypy_cache", ".tox", "site-packages", ".expo", "DerivedData",
}
SKIP_FILES = {
    "package-lock.json", "yarn.lock", "pnpm-lock.yaml", "poetry.lock", "Pipfile.lock",
    "composer.lock", "Gemfile.lock", "Cargo.lock", "go.sum", "bun.lockb", "uv.lock",
}
MAX_BYTES = 1_500_000


def classify(path: str):
    name = os.path.basename(path)
    if name == "Dockerfile" or name.startswith("Dockerfile.") or name.endswith(".dockerfile"):
        return "docker"
    if name.startswith(".env"):
        return "conf"
    if name in {"firestore.rules", "storage.rules", "database.rules.json"}:
        return "conf"
    _, ext = os.path.splitext(name)
    return EXT_TO_LANG.get(ext.lower())


# --------------------------------------------------------------------------- #
# Rules — every rule carries the standard, correct fix.
# --------------------------------------------------------------------------- #
SEV_ORDER = ["critical", "high", "medium", "low", "info"]
SEV_WEIGHT = {"critical": 25, "high": 10, "medium": 4, "low": 1, "info": 0}

PLACEHOLDER = re.compile(
    r"(example|sample|dummy|changeme|change_me|your[_-]?|xxx+|\*\*\*|placeholder|"
    r"<[^>]+>|\$\{|\{\{|process\.env|os\.environ|getenv|env\(|config\(|settings\.|"
    r"test|fake|redacted|replace|todo|null|none|undefined|password123|secret123|\.\.\.)",
    re.I,
)


def _not_placeholder(m):
    return not PLACEHOLDER.search(m.group(0))


def R(id, sev, cat, title, langs, pattern, cwe, owasp, fix, flags=re.I, filt=None, files=None):
    return {
        "id": id, "severity": sev, "category": cat, "title": title,
        "langs": set(langs), "regex": re.compile(pattern, flags), "cwe": cwe,
        "owasp": owasp, "fix": fix, "filter": filt,
        "files": re.compile(files) if files else None,
    }


A01, A02, A03, A04, A05 = ("A01:2025 Broken Access Control", "A02:2025 Security Misconfiguration",
                           "A03:2025 Software Supply Chain Failures", "A04:2025 Cryptographic Failures",
                           "A05:2025 Injection")
A06, A07, A08, A09, A10 = ("A06:2025 Insecure Design", "A07:2025 Authentication Failures",
                           "A08:2025 Software or Data Integrity Failures",
                           "A09:2025 Logging & Alerting Failures",
                           "A10:2025 Mishandling of Exceptional Conditions")
LLM01, LLM02, LLM05, LLM06 = ("LLM01:2025 Prompt Injection", "LLM02:2025 Sensitive Information Disclosure",
                              "LLM05:2025 Improper Output Handling", "LLM06:2025 Excessive Agency")

FIX_SECRET = ("Remove the secret from source, ROTATE it immediately (assume it is leaked — git history "
              "keeps it), load it from environment variables / a secrets manager (Vault, AWS Secrets "
              "Manager, Doppler, 1Password, GitHub Encrypted Secrets), and add a pre-commit secret "
              "scanner (gitleaks / trufflehog). Purge history with git-filter-repo if the repo was public.")

RULES = [
    # ---------------- Secrets (all text files) ----------------
    R("SEC001", "critical", "secrets", "AWS access key ID", ALL_TEXT,
      r"(?<![A-Z0-9])(AKIA|ASIA)[0-9A-Z]{16}(?![A-Z0-9])", "CWE-798", A04, FIX_SECRET, flags=0),
    R("SEC002", "critical", "secrets", "GitHub token", ALL_TEXT,
      r"\b(gh[pousr]_[A-Za-z0-9]{36,}|github_pat_[A-Za-z0-9_]{50,})\b", "CWE-798", A04, FIX_SECRET, flags=0),
    R("SEC003", "critical", "secrets", "Stripe live secret / restricted key", ALL_TEXT,
      r"\b(sk|rk)_live_[0-9a-zA-Z]{20,}\b", "CWE-798", A04, FIX_SECRET, flags=0),
    R("SEC004", "critical", "secrets", "Anthropic API key", ALL_TEXT,
      r"\bsk-ant-[A-Za-z0-9_\-]{30,}", "CWE-798", A04, FIX_SECRET, flags=0),
    R("SEC005", "critical", "secrets", "OpenAI API key", ALL_TEXT,
      r"\bsk-(?!ant-)(?:proj-|svcacct-|admin-)?[A-Za-z0-9_\-]{40,}", "CWE-798", A04, FIX_SECRET, flags=0),
    R("SEC006", "high", "secrets", "Google / Firebase API key", ALL_TEXT,
      r"\bAIza[0-9A-Za-z_\-]{35}\b", "CWE-798", A04,
      "Google browser keys are semi-public by design, so RESTRICT them (HTTP referrer / app restrictions "
      "and API restrictions in Google Cloud Console) and enforce Firebase Security Rules + App Check. "
      "Server keys must never be in client code — move them to env vars.", flags=0),
    R("SEC007", "critical", "secrets", "Slack token or webhook", ALL_TEXT,
      r"(xox[baprs]-[0-9A-Za-z\-]{10,}|hooks\.slack\.com/services/T[0-9A-Z]+/B[0-9A-Z]+/[0-9A-Za-z]+)",
      "CWE-798", A04, FIX_SECRET, flags=0),
    R("SEC008", "critical", "secrets", "Private key block committed", ALL_TEXT,
      r"-----BEGIN (RSA |EC |DSA |OPENSSH |PGP |ENCRYPTED )?PRIVATE KEY-----", "CWE-321", A04, FIX_SECRET, flags=0),
    R("SEC009", "critical", "secrets", "SendGrid API key", ALL_TEXT,
      r"\bSG\.[\w\-]{22}\.[\w\-]{43}\b", "CWE-798", A04, FIX_SECRET, flags=0),
    R("SEC010", "critical", "secrets", "Supabase service_role key in source", ALL_TEXT,
      r"service[_-]?role.{0,60}eyJ[A-Za-z0-9_\-]{10,}\.eyJ", "CWE-798", A01,
      "The service_role key BYPASSES Row Level Security. Never ship it to a browser/mobile app. Use the "
      "anon key client-side with RLS policies on every table; keep service_role only in server env vars. Rotate it now."),
    R("SEC011", "high", "secrets", "Database URL with embedded credentials", ALL_TEXT,
      r"\b(postgres|postgresql|mysql|mariadb|mongodb(\+srv)?|redis|rediss|amqp|mssql)://[^:\s'\"/]+:[^@\s'\"]{3,}@[^\s'\"]+",
      "CWE-798", A04, FIX_SECRET, filt=lambda m: not re.search(r"(\$\{|<|localhost|127\.0\.0\.1|example|user:pass|password@)", m.group(0), re.I)),
    R("SEC012", "high", "secrets", "Hard-coded password / secret / API key", ALL_TEXT,
      r"[\w\-]*(password|passwd|pwd|secret|api[_\-]?key|apikey|access[_\-]?token|auth[_\-]?token|private[_\-]?key|client[_\-]?secret)[\w\-]*['\"]?\s*[:=]\s*['\"][^'\"\s]{8,}['\"]",
      "CWE-798", A07, FIX_SECRET, filt=_not_placeholder),
    R("SEC013", "critical", "secrets", "Secret exposed to the browser via public env prefix", ALL_TEXT,
      r"\b(NEXT_PUBLIC|VITE|REACT_APP|EXPO_PUBLIC|NUXT_PUBLIC|PUBLIC|GATSBY)_[A-Z0-9_]*(SECRET|PRIVATE|SERVICE_ROLE|OPENAI|ANTHROPIC|STRIPE_SK|SK_LIVE|DATABASE_URL|PASSWORD)[A-Z0-9_]*",
      "CWE-200", A01,
      "Anything prefixed NEXT_PUBLIC_/VITE_/REACT_APP_/EXPO_PUBLIC_ is compiled into the JS bundle and "
      "readable by every visitor. Rename it without the public prefix and call the third-party API "
      "from a server route / edge function instead.", flags=0),
    R("SEC014", "medium", "secrets", "Hard-coded JWT", ALL_TEXT,
      r"\beyJ[A-Za-z0-9_\-]{10,}\.eyJ[A-Za-z0-9_\-]{10,}\.[A-Za-z0-9_\-]{10,}", "CWE-798", A07,
      "Do not hard-code tokens. Issue short-lived tokens at runtime; if this is a Supabase anon key it is "
      "public by design — make sure RLS is enabled on every table.", flags=0),

    # ---------------- AI / LLM apps ----------------
    R("AI001", "high", "ai", "LLM SDK used directly in the browser (API key exposed)", {"js"},
      r"dangerouslyAllowBrowser\s*:\s*true", "CWE-522", LLM02,
      "Never call OpenAI/Anthropic/etc. from the client. Create a server route that holds the key, "
      "authenticates the user, rate-limits, and proxies the request."),
    R("AI002", "critical", "ai", "LLM output passed to eval/exec/shell", CODE,
      r"\b(eval|exec|execSync|system|popen|Function)\s*\(.*\b(completion|choices|llm|response\.content|output_text|message\.content|generated)",
      "CWE-94", LLM05,
      "Treat model output as untrusted user input. Never execute it. If code execution is a feature, run it "
      "in an isolated sandbox (gVisor/Firecracker/e2b) with no secrets, no network, and strict timeouts."),
    R("AI003", "low", "ai", "Possible user input concatenated into a system prompt", CODE,
      r"(role['\"]?\s*:\s*['\"]system['\"]|system_prompt|systemPrompt|SYSTEM_PROMPT).{0,120}(\$\{|f['\"]|\+\s*\w*(input|query|message|req|user))",
      "CWE-77", LLM01,
      "Keep system instructions static. Put user content only in the user role, delimit it, validate it, "
      "and never grant the model more tools/permissions than the current user has (least agency)."),
    R("AI004", "medium", "ai", "LLM agent given shell / filesystem / SQL tools", CODE,
      r"(ShellTool|BashTool|PythonREPLTool|PythonAstREPLTool|create_sql_agent|FileManagementToolkit|allow_dangerous_code\s*=\s*True)",
      "CWE-250", LLM06,
      "Apply least agency: allow-list commands, run tools in a sandbox, require human approval for "
      "destructive actions, and use read-only DB credentials for SQL agents."),

    # ---------------- Injection: SQL ----------------
    R("INJ001", "critical", "injection", "SQL built with string interpolation (JS/TS)", {"js"},
      r"(query|execute|raw|\$queryRawUnsafe|\$executeRawUnsafe|sequelize\.query|knex\.raw)\s*\(\s*`[^`]*\b(SELECT|INSERT|UPDATE|DELETE|WHERE)\b[^`]*\$\{",
      "CWE-89", A05,
      "Use parameterized queries / prepared statements (pg: query('... $1', [v]); Prisma: $queryRaw tagged "
      "template or the query builder; Knex: bindings). Never interpolate user input into SQL."),
    R("INJ002", "critical", "injection", "SQL built with string formatting (Python)", {"py"},
      r"\.(execute|executemany|raw|extra|executescript)\(\s*(f['\"]|['\"][^'\"]*['\"]\s*(%|\.format|\+))",
      "CWE-89", A05,
      "Use DB-API parameters: cursor.execute('SELECT ... WHERE id = %s', (user_id,)) or the ORM. "
      "Never use f-strings / % / .format / + to build SQL."),
    R("INJ003", "critical", "injection", "SQL built with string concatenation (Java/Kotlin/C#)", {"java", "cs"},
      r"(executeQuery|executeUpdate|execute|prepareStatement|createQuery|createNativeQuery|SqlCommand|FromSqlRaw|ExecuteSqlRaw)\s*\(\s*(\$?\"[^\"]*\"\s*\+|\$\"[^\"]*\{)",
      "CWE-89", A05,
      "Use PreparedStatement with ? placeholders / JPA named parameters / SqlParameter / FromSqlInterpolated. "
      "Never concatenate input into SQL."),
    R("INJ004", "critical", "injection", "SQL built with fmt.Sprintf / concatenation (Go)", {"go"},
      r"\.(Query|QueryRow|Exec|QueryContext|ExecContext|QueryRowContext)\(\s*(ctx,\s*)?(fmt\.Sprintf|\"[^\"]*\"\s*\+)",
      "CWE-89", A05, "Use placeholders: db.Query(\"SELECT ... WHERE id = $1\", id)."),
    R("INJ005", "critical", "injection", "SQL with request input (PHP)", {"php"},
      r"(mysqli?_query|->query|->exec|pg_query)\s*\(.*\$_(GET|POST|REQUEST|COOKIE)", "CWE-89", A05,
      "Use PDO / mysqli prepared statements with bound parameters (or Eloquent / Doctrine query builder)."),
    R("INJ006", "critical", "injection", "SQL with string interpolation (Ruby)", {"rb"},
      r"(where|find_by_sql|order|group|having|joins|select|exec_query|execute)\s*\(?\s*\"[^\"]*#\{",
      "CWE-89", A05, "Use placeholders: where('email = ?', email) or hash conditions where(email: email)."),
    R("INJ007", "high", "injection", "SQL concatenation with a string literal", {"js", "py", "php", "rb", "go", "java", "cs"},
      r"['\"]\s*(SELECT|INSERT INTO|UPDATE|DELETE FROM)\b[^'\"]*(WHERE|VALUES|SET)[^'\"]*['\"]\s*\+\s*[A-Za-z_]",
      "CWE-89", A05, "Use parameterized queries. Concatenating variables into SQL enables SQL injection."),
    R("INJ008", "high", "injection", "NoSQL query built from raw request body", {"js"},
      r"\.(find|findOne|findOneAndUpdate|updateOne|deleteOne|deleteMany|aggregate)\(\s*req\.(body|query|params)\b",
      "CWE-943", A05,
      "Validate and whitelist fields with a schema (zod/joi/class-validator); reject objects where strings are "
      "expected (blocks $ne/$gt operator injection); use express-mongo-sanitize."),

    # ---------------- Injection: command / code ----------------
    R("INJ010", "high", "injection", "Dynamic code evaluation (eval)", {"js", "py", "php", "rb"},
      r"(?<![\w.])eval\s*\(", "CWE-95", A05,
      "Remove eval. Parse data with JSON.parse / ast.literal_eval, or use a lookup table of allowed operations."),
    R("INJ011", "high", "injection", "new Function() code evaluation", {"js"},
      r"\bnew\s+Function\s*\(", "CWE-95", A05, "Avoid constructing code from strings; use explicit functions."),
    R("INJ012", "critical", "injection", "Shell command built from interpolated input (Node)", {"js"},
      r"\b(exec|execSync)\s*\(\s*(`[^`]*\$\{|['\"][^'\"]*['\"]\s*\+)", "CWE-78", A05,
      "Use execFile/spawn with an argument array and shell:false; validate input against an allow-list."),
    R("INJ013", "high", "injection", "Shell execution (Python)", {"py"},
      r"(os\.system|os\.popen|commands\.getoutput|subprocess\.\w+\([^)]*shell\s*=\s*True)", "CWE-78", A05,
      "Use subprocess.run([...args], shell=False, check=True) with an argument list; never pass user input to a shell."),
    R("INJ014", "high", "injection", "Python exec() / compile() on dynamic input", {"py"},
      r"(?<![\w.])(exec|compile)\s*\(\s*(?!['\"])", "CWE-95", A05, "Remove exec; use safe parsing or explicit dispatch tables."),
    R("INJ015", "high", "injection", "Runtime.exec / ProcessBuilder (Java)", {"java"},
      r"(Runtime\.getRuntime\(\)\.exec|new\s+ProcessBuilder)\s*\(", "CWE-78", A05,
      "Pass a fixed command with a String[] argument array, validate every argument against an allow-list."),
    R("INJ016", "high", "injection", "Shell via exec.Command(\"sh\",\"-c\") (Go)", {"go"},
      r"exec\.Command(Context)?\(\s*(ctx,\s*)?\"(sh|bash|cmd|powershell)\"\s*,\s*\"(-c|/c)\"", "CWE-78", A05,
      "Call the binary directly with separate arguments: exec.Command(\"git\", \"log\", ref)."),
    R("INJ017", "critical", "injection", "OS command with request input (PHP)", {"php"},
      r"\b(system|exec|shell_exec|passthru|popen|proc_open)\s*\(.*\$_(GET|POST|REQUEST|COOKIE)", "CWE-78", A05,
      "Never pass request data to the shell. Use escapeshellarg as a last resort, prefer library APIs."),
    R("INJ018", "critical", "injection", "File include from request input (PHP LFI/RFI)", {"php"},
      r"\b(include|require)(_once)?\s*\(?\s*['\"]?[^;]*\$_(GET|POST|REQUEST|COOKIE)", "CWE-98", A05,
      "Map user choices to a fixed allow-list of files; set allow_url_include=Off."),
    R("INJ019", "high", "injection", "Ruby system/backticks with params", {"rb"},
      r"(system|exec|spawn|`|%x)\s*\(?[^\n]*#\{\s*params", "CWE-78", A05, "Use system('cmd', arg1, arg2) array form; never interpolate params."),
    R("INJ020", "high", "injection", "C# Process.Start with dynamic arguments", {"cs"},
      r"Process\.Start\s*\(\s*(?!\")", "CWE-78", A05, "Use ProcessStartInfo with ArgumentList and UseShellExecute=false; validate input."),

    # ---------------- XSS / output encoding ----------------
    R("XSS001", "medium", "xss", "Unsafe DOM sink (innerHTML / document.write)", {"js", "html"},
      r"(\.innerHTML\s*=|\.outerHTML\s*=|insertAdjacentHTML\s*\(|document\.write(ln)?\s*\()", "CWE-79", A05,
      "Use textContent / innerText, or sanitize with DOMPurify before inserting HTML. Add a strict Content-Security-Policy."),
    R("XSS002", "medium", "xss", "dangerouslySetInnerHTML / v-html / {@html}", {"js", "html"},
      r"(dangerouslySetInnerHTML|v-html\s*=|\{@html\s)", "CWE-79", A05,
      "Render as text, or sanitize with DOMPurify (isomorphic-dompurify on the server) immediately before rendering."),
    R("XSS003", "medium", "xss", "Template auto-escaping bypassed", {"py", "html", "rb", "cs", "go", "php"},
      r"(\|\s*safe\b|mark_safe\(|autoescape\s*=?\s*(False|false|off)|\.html_safe\b|\braw\(|Html\.Raw\(|template\.HTML\(|\{!!)",
      "CWE-79", A05, "Keep auto-escaping on. Only mark content safe after sanitizing it with a vetted HTML sanitizer (bleach/nh3, Loofah, HtmlSanitizer)."),
    R("XSS004", "high", "xss", "Echoing request input (PHP)", {"php"},
      r"(echo|print)\s+\$_(GET|POST|REQUEST|COOKIE)", "CWE-79", A05, "Escape output: htmlspecialchars($v, ENT_QUOTES, 'UTF-8'), or use a templating engine (Blade/Twig)."),

    # ---------------- Deserialization / integrity ----------------
    R("DES001", "high", "deserialization", "Unsafe deserialization (Python)", {"py"},
      r"(pickle\.loads?|cPickle\.loads?|marshal\.loads?|shelve\.open|dill\.loads?|joblib\.load|torch\.load\((?![^)]*weights_only\s*=\s*True))",
      "CWE-502", A08, "Never unpickle untrusted data. Use JSON / msgpack; for models use safetensors or torch.load(weights_only=True)."),
    R("DES002", "high", "deserialization", "yaml.load without SafeLoader", {"py"},
      r"yaml\.(load|load_all)\((?![^)]*(SafeLoader|CSafeLoader|BaseLoader))", "CWE-502", A08, "Use yaml.safe_load()."),
    R("DES003", "high", "deserialization", "Java native deserialization", {"java"},
      r"(new\s+ObjectInputStream|\.readObject\s*\(\)|XMLDecoder|enableDefaultTyping|activateDefaultTyping)", "CWE-502", A08,
      "Avoid Java serialization for untrusted data; use JSON with explicit types. If unavoidable, use an ObjectInputFilter allow-list."),
    R("DES004", "high", "deserialization", "BinaryFormatter / insecure .NET deserializer", {"cs"},
      r"(BinaryFormatter|NetDataContractSerializer|SoapFormatter|LosFormatter|TypeNameHandling\.(All|Auto|Objects))", "CWE-502", A08,
      "BinaryFormatter is obsolete and unsafe. Use System.Text.Json without polymorphic type handling."),
    R("DES005", "high", "deserialization", "PHP unserialize", {"php"},
      r"\bunserialize\s*\(", "CWE-502", A08, "Use json_decode; if unserialize is unavoidable pass ['allowed_classes' => false]."),
    R("DES006", "high", "deserialization", "Ruby Marshal / unsafe YAML load", {"rb"},
      r"(Marshal\.load|YAML\.load\((?!.*permitted_classes)|YAML\.unsafe_load)", "CWE-502", A08, "Use JSON or YAML.safe_load."),

    # ---------------- Crypto ----------------
    R("CRY001", "medium", "crypto", "Weak hash (MD5/SHA-1)", CODE,
      r"(hashlib\.(md5|sha1)\b|createHash\(\s*['\"](md5|sha1)['\"]|MessageDigest\.getInstance\(\s*\"(MD5|SHA-?1)\"|\bMD5\.Create|\bSHA1\.Create|crypto/md5|crypto/sha1|\bmd5\s*\(|\bsha1\s*\(|Digest::(MD5|SHA1))",
      "CWE-328", A04,
      "Use SHA-256+ for integrity. For PASSWORDS use a slow KDF: Argon2id (preferred), scrypt or bcrypt (cost>=12). Never MD5/SHA for passwords."),
    R("CRY002", "high", "crypto", "Broken cipher or ECB mode", CODE,
      r"(\bDES\b|DESede|TripleDES|\bRC4\b|\bRC2\b|Blowfish|/ECB/|MODE_ECB|AES\.new\([^)]*\)\s*$|Cipher\.getInstance\(\s*\"AES\"\s*\)|createCipher\()",
      "CWE-327", A04, "Use AES-256-GCM or ChaCha20-Poly1305 via a high-level library (libsodium, Tink, cryptography Fernet/AESGCM) with random nonces."),
    R("CRY003", "medium", "crypto", "Non-cryptographic RNG used for a secret", CODE,
      r"((token|secret|password|passwd|otp|nonce|salt|session|api_?key|reset)[\w\s\.=:]{0,40}(Math\.random|random\.(random|randint|choice|choices)|\brand\(\)|mt_rand|new\s+Random\()|(Math\.random|random\.(randint|choice))[^\n]{0,40}(token|secret|otp|password))",
      "CWE-338", A04, "Use a CSPRNG: crypto.randomUUID()/crypto.getRandomValues (JS), secrets.token_urlsafe (Python), SecureRandom (Java/Ruby), crypto/rand (Go), random_bytes (PHP)."),
    R("CRY004", "high", "crypto", "JWT 'none' algorithm or signature verification disabled", CODE,
      r"(algorithms?\s*[:=]\s*\[?\s*['\"]none['\"]|verify_signature['\"]?\s*:\s*False|verify\s*=\s*False[^\n]*jwt|jwt\.decode\([^)]*verify\s*=\s*False|ignoreExpiration\s*:\s*true)",
      "CWE-347", A07, "Always verify JWT signatures with an explicit algorithm allow-list (e.g. ['RS256']) and validate exp, iss, aud."),
    R("CRY005", "medium", "crypto", "jwt.decode() does not verify the token (Node)", {"js"},
      r"\bjwt\.decode\s*\(", "CWE-347", A07, "Use jwt.verify(token, key, { algorithms: ['RS256'], audience, issuer }) — decode() only base64-decodes."),

    # ---------------- TLS / transport ----------------
    R("TLS001", "high", "transport", "TLS certificate verification disabled", CODE | {"yaml", "conf", "json"},
      r"(rejectUnauthorized\s*:\s*false|NODE_TLS_REJECT_UNAUTHORIZED['\"]?\s*[:=]\s*['\"]?0|verify\s*=\s*False|InsecureSkipVerify\s*:\s*true|CURLOPT_SSL_VERIFYPEER\s*,\s*(false|0)|ServerCertificateValidationCallback[^;]*=>\s*true|danger_accept_invalid_certs\(\s*true|ALLOW_ALL_HOSTNAME_VERIFIER|NoopHostnameVerifier|ssl\._create_unverified_context|check_hostname\s*=\s*False)",
      "CWE-295", A04, "Never disable certificate validation. Fix the trust store / use the correct CA bundle instead."),
    R("TLS002", "low", "transport", "Plain-HTTP URL", CODE | {"yaml", "conf", "json", "html"},
      r"['\"`]http://(?!localhost|127\.0\.0\.1|0\.0\.0\.0|\[::1\]|[\w.-]*example\.|schemas\.|www\.w3\.org|xmlns|json-schema|purl\.org|[\w.-]*\.local\b|host\.docker\.internal)[\w.-]+",
      "CWE-319", A04, "Use https:// everywhere and enable HSTS (Strict-Transport-Security: max-age=63072000; includeSubDomains)."),

    # ---------------- Access control / web config ----------------
    R("WEB001", "medium", "config", "CORS allows any origin", CODE | {"yaml", "conf", "json"},
      r"(origin\s*:\s*['\"]\*['\"]|Access-Control-Allow-Origin['\"]?\s*[,:=]\s*['\"]\*|allow_origins\s*=\s*\[\s*['\"]\*['\"]|AllowAnyOrigin\(\)|@CrossOrigin\s*(\(\s*\)|\(\s*origins\s*=\s*\"\*\")|CORS_ALLOW_ALL_ORIGINS\s*=\s*True|CORS_ORIGIN_ALLOW_ALL\s*=\s*True)",
      "CWE-942", A02, "Allow-list exact trusted origins. Never combine wildcard origins with credentials."),
    R("WEB002", "low", "config", "cors() with default (allow-all) options", {"js"},
      r"\bcors\(\s*\)", "CWE-942", A02, "Pass an explicit config: cors({ origin: ['https://app.example.com'], credentials: true })."),
    R("WEB003", "medium", "config", "Debug mode enabled", {"py", "conf", "yaml", "json", "js", "php"},
      r"(^\s*DEBUG\s*=\s*True|app\.run\([^)]*debug\s*=\s*True|APP_DEBUG\s*=\s*true|display_errors\s*=\s*On|FLASK_DEBUG\s*=\s*1)",
      "CWE-489", A02, "Drive debug flags from environment and make sure they are OFF in production; never expose stack traces to users.",
      flags=re.I | re.M),
    R("WEB004", "medium", "config", "CSRF protection disabled", {"java", "py", "rb", "php", "js", "cs"},
      r"(csrf\(\)\.disable\(\)|csrf\(\s*\w+\s*->\s*\w+\.disable\(\)\)|AbstractHttpConfigurer::disable|@csrf_exempt|skip_before_action\s+:verify_authenticity_token|protect_from_forgery\s+except|IgnoreAntiforgeryToken|csrf\s*:\s*false)",
      "CWE-352", A01, "Keep CSRF protection on for cookie-authenticated endpoints (SameSite=Lax/Strict cookies + CSRF tokens). Only disable for pure token-auth APIs."),
    R("WEB005", "medium", "config", "Django ALLOWED_HOSTS wildcard", {"py"},
      r"ALLOWED_HOSTS\s*=\s*\[\s*['\"]\*['\"]", "CWE-16", A02, "List your real hostnames in ALLOWED_HOSTS."),
    R("WEB006", "high", "access", "Mass assignment (permit all)", {"rb", "js", "php"},
      r"(params\.permit!|\$guarded\s*=\s*\[\s*\]|Object\.assign\(\s*\w+\s*,\s*req\.body\)|\.create\(\s*req\.body\s*\)|\.update\(\s*req\.body\s*\)|\.(create|update)\(\s*\{\s*data\s*:\s*req\.body\s*\})",
      "CWE-915", A01, "Whitelist assignable fields explicitly (strong params, DTOs, zod schemas). Never write req.body straight into a model — users will set role=admin."),
    R("WEB007", "high", "access", "Path traversal: file access from request input", {"js", "py", "php", "java", "go", "rb"},
      r"(readFile|readFileSync|createReadStream|sendFile|res\.download|open|send_file|file_get_contents|fopen|new\s+File|os\.Open|File\.read)\s*\([^)\n]*(req\.(query|params|body)|request\.(args|GET|POST|form)|\$_(GET|POST|REQUEST)|params\[)",
      "CWE-22", A01, "Resolve the path, then verify it stays inside an allowed base directory; better, map IDs to files server-side."),
    R("WEB008", "high", "access", "SSRF: server fetches a user-supplied URL", {"js", "py", "php", "java", "go", "rb"},
      r"(fetch|axios(\.\w+)?|got|request|needle|requests\.(get|post|put)|urlopen|httpx\.\w+|file_get_contents|curl_init|http\.Get|Net::HTTP\.get|URI\.open)\s*\(\s*(req\.(query|body|params)|request\.(args|GET|POST|json|form)|\$_(GET|POST|REQUEST)|params\[)",
      "CWE-918", A01, "Allow-list destination hosts, block private/link-local/metadata IP ranges (169.254.169.254), disable redirects, resolve DNS once and pin."),
    R("WEB009", "medium", "access", "Open redirect", {"js", "py", "php", "java", "rb", "go"},
      r"(res\.redirect|redirect|HttpResponseRedirect|header\(\s*['\"]Location:|sendRedirect|redirect_to|http\.Redirect)\s*\(?[^)\n]*(req\.(query|body|params)|request\.(args|GET)|\$_(GET|REQUEST)|params\[)",
      "CWE-601", A01, "Only redirect to relative paths or an allow-list of URLs."),
    R("WEB010", "medium", "auth", "Auth token stored in localStorage/sessionStorage", {"js"},
      r"(localStorage|sessionStorage)\.setItem\(\s*['\"`][^'\"`]*(token|jwt|auth|session|refresh)", "CWE-922", A07,
      "Store session tokens in HttpOnly, Secure, SameSite cookies so XSS cannot steal them."),
    R("WEB011", "info", "access", "Client-side role/admin check (must also be enforced server-side)", {"js"},
      r"(isAdmin|role\s*===?\s*['\"]admin['\"]|user\??\.role\s*===?)", "CWE-602", A01,
      "UI checks are cosmetic. Every API route / DB policy must independently verify the user's permissions (deny by default)."),
    R("WEB012", "low", "config", "Cookie without Secure/HttpOnly flags", CODE,
      r"(httpOnly\s*:\s*false|secure\s*:\s*false|SESSION_COOKIE_SECURE\s*=\s*False|SESSION_COOKIE_HTTPONLY\s*=\s*False|HttpOnly\s*=\s*false)",
      "CWE-614", A07, "Set HttpOnly, Secure and SameSite=Lax (or Strict) on all session cookies."),
    R("WEB013", "high", "access", "PHP extract() on request data", {"php"},
      r"\bextract\s*\(\s*\$_(GET|POST|REQUEST|COOKIE)", "CWE-621", A01, "Read explicit keys from the request instead of extract()."),
    R("WEB014", "low", "config", "XML parser — make sure XXE is disabled", {"java", "cs", "py", "php"},
      r"(DocumentBuilderFactory\.newInstance|SAXParserFactory\.newInstance|XMLInputFactory\.newInstance|XmlDocument\(\)|lxml\.etree\.(parse|fromstring)|xml\.etree|simplexml_load_string|libxml_disable_entity_loader\(\s*false)",
      "CWE-611", A02, "Disable DTDs and external entities (disallow-doctype-decl=true), or use defusedxml in Python."),

    # ---------------- Logging / errors ----------------
    R("LOG001", "medium", "logging", "Sensitive data written to logs", CODE,
      r"(console\.(log|info|debug|error)|print|logger\.\w+|logging\.\w+|log\.\w+|System\.out\.print\w*|fmt\.Print\w*|Console\.Write\w*|puts|error_log)\s*\(?[^\n]*\b(password|passwd|secret|api_?key|access_?token|credit_?card|card_?number|cvv|ssn|aadhaar|pan_?number)\b",
      "CWE-532", A09, "Never log secrets or personal data. Use structured logging with a redaction list."),
    R("LOG002", "low", "errors", "Empty catch / swallowed exception", CODE,
      r"(catch\s*\([^)]*\)\s*\{\s*\}|except(\s+\w+(\s+as\s+\w+)?)?\s*:\s*pass\b|rescue\s*(=>\s*\w+)?\s*;?\s*end\b)", "CWE-390", A10,
      "Handle or log the error, fail closed (deny access on error), and return a generic message to the user."),
    R("LOG003", "low", "errors", "Stack trace / error details returned to client", {"js", "py", "java", "php", "cs"},
      r"(res\.(send|json)\(\s*(err|error)(\.stack)?\s*\)|res\.status\(500\)\.(send|json)\(\s*(err|error)\b|traceback\.format_exc\(\)|printStackTrace\(\))",
      "CWE-209", A10, "Log details server-side with a correlation ID; return a generic error body."),
    R("LOG004", "low", "hygiene", "Security-related TODO/FIXME left in code", CODE,
      r"(TODO|FIXME|HACK|XXX)[^\n]{0,60}\b(auth|security|password|token|validate|sanitiz|permission|encrypt|csrf|xss|injection|rate.?limit)",
      "CWE-1078", A06, "Resolve before release or track it as an issue with an owner and due date."),

    # ---------------- Memory safety (C/C++) ----------------
    R("MEM001", "high", "memory", "Unsafe C string function", {"c"},
      r"\b(gets|strcpy|strcat|sprintf|vsprintf|scanf|sscanf|strtok)\s*\(", "CWE-120", A06,
      "Use bounded versions (fgets, snprintf, strlcpy/strncpy with explicit termination) or std::string; compile with -D_FORTIFY_SOURCE=2 and sanitizers."),
    R("MEM002", "high", "memory", "Format string with non-literal argument", {"c"},
      r"\b(printf|fprintf\s*\(\s*\w+\s*,|syslog\s*\(\s*\w+\s*,)\s*\(?\s*[a-zA-Z_]\w*\s*\)", "CWE-134", A05, "Always use a literal format: printf(\"%s\", s)."),
    R("MEM003", "low", "memory", "Rust unsafe block", {"rs"},
      r"\bunsafe\s*\{", "CWE-119", A06, "Minimise unsafe, document the invariants in a // SAFETY: comment, and fuzz/miri-test it."),

    # ---------------- Mobile ----------------
    R("MOB001", "high", "mobile", "Android cleartext traffic / debuggable build", {"xml"},
      r"(android:usesCleartextTraffic\s*=\s*\"true\"|android:debuggable\s*=\s*\"true\"|cleartextTrafficPermitted\s*=\s*\"true\")",
      "CWE-319", A02, "Disable cleartext and debuggable in release builds; use a Network Security Config with HTTPS only."),
    R("MOB002", "medium", "mobile", "Android allowBackup enabled", {"xml"},
      r"android:allowBackup\s*=\s*\"true\"", "CWE-530", A02, "Set allowBackup=false or define dataExtractionRules excluding sensitive files."),
    R("MOB003", "high", "mobile", "iOS App Transport Security disabled", {"xml"},
      r"<key>NSAllowsArbitraryLoads</key>\s*<true\s*/>", "CWE-319", A02, "Remove NSAllowsArbitraryLoads; add narrow exceptions only for specific domains."),
    R("MOB004", "medium", "mobile", "Secret stored in plain mobile storage", {"swift", "java", "dart", "js"},
      r"(UserDefaults[^\n]*(password|token|secret)|SharedPreferences[^\n]*(password|token|secret)|putString\(\s*\"(password|token|secret)|AsyncStorage\.setItem\(\s*['\"][^'\"]*(token|password|secret)|SharedPreferences\.getInstance[^\n]*(token|password))",
      "CWE-312", A04, "Use the Keychain (iOS), EncryptedSharedPreferences/Keystore (Android), flutter_secure_storage or expo-secure-store."),
    R("MOB005", "medium", "mobile", "WebView JavaScript bridge exposed", {"java", "swift", "dart"},
      r"(addJavascriptInterface\s*\(|setAllowUniversalAccessFromFileURLs\(\s*true|setAllowFileAccess\(\s*true)", "CWE-749", A02,
      "Only load trusted HTTPS content in WebViews with bridges; disable file access."),

    # ---------------- Containers / IaC / CI ----------------
    R("IAC001", "low", "container", "Docker image uses 'latest' or no tag", {"docker"},
      r"^\s*FROM\s+(?!scratch\b)(?:--platform=\S+\s+)?[\w./-]+(:latest)?\s*(AS\s+\w+)?\s*$", "CWE-1104", A03,
      "Pin images to a version and ideally a digest (node:20.11-alpine@sha256:...). Rebuild regularly for patches.", flags=re.I | re.M,
      filt=lambda m: ":" not in m.group(0).split()[-1] or m.group(0).strip().endswith(":latest")),
    R("IAC002", "high", "container", "Secret baked into image via ENV/ARG", {"docker"},
      r"^\s*(ENV|ARG)\s+\w*(PASSWORD|SECRET|TOKEN|API_KEY|PRIVATE_KEY|ACCESS_KEY)\w*\s*[= ]\s*\S+", "CWE-798", A04,
      "Use BuildKit secrets (RUN --mount=type=secret) at build time and inject runtime secrets via the orchestrator.", flags=re.I | re.M),
    R("IAC003", "medium", "container", "curl | sh remote script execution", {"docker", "shell", "yaml"},
      r"(curl|wget)\s[^|\n]*\|\s*(sudo\s+)?(ba|z)?sh\b", "CWE-494", A08, "Download, verify a checksum/signature, then execute; or use a package manager."),
    R("IAC004", "medium", "container", "World-writable permissions (chmod 777)", {"docker", "shell", "yaml"} | CODE,
      r"chmod\s+(-R\s+)?0?777\b", "CWE-732", A02, "Grant the minimum permission needed (e.g. 750/640) to a dedicated non-root user."),
    R("IAC005", "high", "container", "Privileged container / privilege escalation", {"yaml", "json", "shell", "tf"},
      r"(privileged\s*:\s*true|--privileged\b|allowPrivilegeEscalation\s*:\s*true|hostNetwork\s*:\s*true|hostPID\s*:\s*true|runAsNonRoot\s*:\s*false|runAsUser\s*:\s*0\b|/var/run/docker\.sock)",
      "CWE-250", A02, "Run as non-root, drop all capabilities, readOnlyRootFilesystem: true, allowPrivilegeEscalation: false."),
    R("IAC006", "medium", "cloud", "Ingress open to the whole internet (0.0.0.0/0)", {"tf", "yaml", "json"},
      r"(cidr_blocks\s*=\s*\[\s*\"0\.0\.0\.0/0\"|CidrIp['\"]?\s*:\s*['\"]?0\.0\.0\.0/0|source_address_prefix\s*=\s*\"(\*|0\.0\.0\.0/0|Internet)\"|::/0)",
      "CWE-284", A02, "Restrict security groups to known CIDRs; never expose SSH/RDP/DB ports publicly — use a bastion, VPN or SSM."),
    R("IAC007", "high", "cloud", "Public storage bucket / public database", {"tf", "yaml", "json"},
      r"(acl\s*=\s*\"public-read(-write)?\"|publicly_accessible\s*=\s*true|block_public_acls\s*=\s*false|PublicAccessBlockConfiguration[^}]*false|allUsers|allAuthenticatedUsers)",
      "CWE-284", A01, "Keep buckets and databases private; serve public assets through a CDN with origin access control."),
    R("IAC008", "medium", "cloud", "Encryption at rest disabled", {"tf", "yaml", "json"},
      r"(encrypted\s*=\s*false|storage_encrypted\s*=\s*false|enable_encryption\s*=\s*false|kms_key_id\s*=\s*\"\")", "CWE-311", A04,
      "Enable encryption at rest with KMS-managed keys for every datastore and volume."),
    R("IAC009", "high", "ci", "GitHub Actions script injection from untrusted event data", {"yaml"},
      r"\$\{\{\s*github\.(event\.(issue|pull_request|comment|review|review_comment|head_commit|discussion)\.[\w.]*(title|body|message|name|label|ref)|head_ref)\s*\}\}",
      "CWE-78", A08, "Pass untrusted values through env: variables and reference them as \"$VAR\" in run: steps."),
    R("IAC010", "medium", "ci", "Over-privileged CI token / pull_request_target", {"yaml"},
      r"(permissions\s*:\s*write-all|on\s*:\s*\[?[^\n]*pull_request_target)", "CWE-250", A08,
      "Set top-level permissions: contents: read and grant write per-job only. Avoid pull_request_target with checkout of PR code."),

    # ---------------- BaaS (Firebase / Supabase) ----------------
    R("BAAS001", "critical", "access", "Firebase rules allow public read/write", {"conf", "json"},
      r"(allow\s+(read|write|read\s*,\s*write)\s*(:\s*if\s+true|;)|\"\.(read|write)\"\s*:\s*(true|\"true\"))", "CWE-284", A01,
      "Require auth and ownership: allow read, write: if request.auth != null && request.auth.uid == userId; test rules with the emulator.",
      files=r"(firestore\.rules|storage\.rules|database\.rules\.json|\.rules)$"),
    R("BAAS002", "critical", "access", "Row Level Security disabled (Postgres/Supabase)", {"sql"},
      r"disable\s+row\s+level\s+security", "CWE-284", A01,
      "Enable RLS on every table in an exposed schema and write explicit policies (auth.uid() = user_id)."),
    R("BAAS003", "high", "access", "Overly permissive RLS policy (using true)", {"sql"},
      r"create\s+policy[\s\S]{0,200}?using\s*\(\s*true\s*\)", "CWE-284", A01,
      "Scope policies to the owner: USING (auth.uid() = user_id) WITH CHECK (auth.uid() = user_id)."),

    # ---------------- Smart contracts ----------------
    R("SOL001", "high", "web3", "tx.origin used for authorization", {"sol"},
      r"tx\.origin", "CWE-477", A07, "Use msg.sender for authorization."),
    R("SOL002", "medium", "web3", "Low-level call / delegatecall", {"sol"},
      r"\.(call|delegatecall)\s*[({]", "CWE-841", A06, "Follow checks-effects-interactions, use ReentrancyGuard, check return values; audit before mainnet."),
]


# --------------------------------------------------------------------------- #
# Stack detection
# --------------------------------------------------------------------------- #
FRAMEWORK_HINTS = {
    # dependency name (lower) -> label
    "next": "Next.js", "react": "React", "vue": "Vue", "nuxt": "Nuxt", "svelte": "Svelte",
    "@sveltejs/kit": "SvelteKit", "@angular/core": "Angular", "express": "Express",
    "@nestjs/core": "NestJS", "fastify": "Fastify", "hono": "Hono", "react-native": "React Native",
    "expo": "Expo", "electron": "Electron", "@supabase/supabase-js": "Supabase", "firebase": "Firebase",
    "firebase-admin": "Firebase", "prisma": "Prisma", "@prisma/client": "Prisma", "drizzle-orm": "Drizzle",
    "mongoose": "MongoDB", "openai": "OpenAI SDK", "@anthropic-ai/sdk": "Anthropic SDK", "langchain": "LangChain",
    "@langchain/core": "LangChain", "ai": "Vercel AI SDK", "stripe": "Stripe", "@stripe/stripe-js": "Stripe",
    "next-auth": "NextAuth", "@clerk/nextjs": "Clerk", "django": "Django", "flask": "Flask",
    "fastapi": "FastAPI", "streamlit": "Streamlit", "gradio": "Gradio", "anthropic": "Anthropic SDK",
    "llama-index": "LlamaIndex", "llama_index": "LlamaIndex", "sqlalchemy": "SQLAlchemy", "celery": "Celery",
    "razorpay": "Razorpay", "paypal": "PayPal", "braintree": "Braintree", "twilio": "Twilio",
}
MANIFESTS = {
    "package.json": "Node.js", "requirements.txt": "Python", "pyproject.toml": "Python", "Pipfile": "Python",
    "go.mod": "Go", "pom.xml": "Java (Maven)", "build.gradle": "JVM (Gradle)", "build.gradle.kts": "JVM (Gradle)",
    "Gemfile": "Ruby", "composer.json": "PHP", "Cargo.toml": "Rust", "pubspec.yaml": "Flutter/Dart",
    "Package.swift": "Swift", "mix.exs": "Elixir", "Dockerfile": "Docker", "docker-compose.yml": "Docker Compose",
    "compose.yaml": "Docker Compose", "serverless.yml": "Serverless", "vercel.json": "Vercel",
    "netlify.toml": "Netlify", "firebase.json": "Firebase", "supabase": "Supabase", "hardhat.config.js": "Hardhat",
    "foundry.toml": "Foundry", "Chart.yaml": "Helm", "wrangler.toml": "Cloudflare Workers",
}
LOCKFILES = {
    "Node.js": ["package-lock.json", "yarn.lock", "pnpm-lock.yaml", "bun.lockb", "bun.lock"],
    "Python": ["poetry.lock", "Pipfile.lock", "uv.lock", "requirements.txt"],
    "Ruby": ["Gemfile.lock"], "PHP": ["composer.lock"], "Rust": ["Cargo.lock"], "Go": ["go.sum"],
    "Flutter/Dart": ["pubspec.lock"],
}
SENSITIVE_DATA = {
    "payments": ["Stripe", "Razorpay", "PayPal", "Braintree"],
    "ai": ["OpenAI SDK", "Anthropic SDK", "LangChain", "LlamaIndex", "Vercel AI SDK"],
}
EXPECTED_DOCS = {
    "README": ["README.md", "README.rst", "README"],
    "ARCHITECTURE": ["docs/ARCHITECTURE.md"],
    "DESIGN": ["docs/DESIGN.md"],
    "MODULES": ["docs/MODULES.md"],
    "API": ["docs/API.md", "openapi.yaml", "openapi.json", "docs/openapi.yaml"],
    "DATA_MODEL": ["docs/DATA_MODEL.md"],
    "SECURITY": ["SECURITY.md", "docs/SECURITY.md", ".github/SECURITY.md"],
    "THREAT_MODEL": ["docs/THREAT_MODEL.md"],
    "COMPLIANCE": ["docs/COMPLIANCE.md"],
    "PRIVACY": ["docs/PRIVACY.md", "PRIVACY.md"],
    "TESTING": ["docs/TESTING.md"],
    "DEPLOYMENT": ["docs/DEPLOYMENT.md"],
    "RUNBOOK": ["docs/RUNBOOK.md"],
    "ADR": ["docs/adr"],
    "CHANGELOG": ["CHANGELOG.md"],
    "CONTRIBUTING": ["CONTRIBUTING.md", ".github/CONTRIBUTING.md"],
    "LICENSE": ["LICENSE", "LICENSE.md", "LICENSE.txt"],
}


# --------------------------------------------------------------------------- #
# Scanner
# --------------------------------------------------------------------------- #
class Scanner:
    def __init__(self, root, excludes=(), min_sev="info"):
        self.root = os.path.abspath(root)
        self.excludes = list(excludes)
        self.min_rank = SEV_ORDER.index(min_sev)
        self.findings = []
        self.lang_counts = Counter()
        self.files_scanned = 0
        self.manifests = set()
        self.frameworks = set()
        self.all_files = []
        self.sql_text = []
        self.node_has_deps = False

    # ---- helpers
    def rel(self, p):
        return os.path.relpath(p, self.root).replace(os.sep, "/")

    def excluded(self, rel):
        return any(fnmatch.fnmatch(rel, g) or fnmatch.fnmatch(os.path.basename(rel), g) for g in self.excludes)

    def add(self, rule_id, sev, cat, title, file, line, snippet, cwe, owasp, fix):
        if SEV_ORDER.index(sev) > self.min_rank:
            return
        self.findings.append({
            "rule": rule_id, "severity": sev, "category": cat, "title": title, "file": file,
            "line": line, "snippet": snippet[:180], "cwe": cwe, "owasp": owasp, "fix": fix,
        })

    # ---- walk
    def walk(self):
        for dirpath, dirnames, filenames in os.walk(self.root):
            rel_dir = self.rel(dirpath)
            # Skip vendored dirs and NoCap's own toolkit (its rules contain example patterns)
            dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS
                           and not os.path.exists(os.path.join(dirpath, d, ".nocap-toolkit"))
                           and not self.excluded(self.rel(os.path.join(dirpath, d)))]
            if os.path.exists(os.path.join(dirpath, ".nocap-toolkit")) and dirpath != self.root:
                dirnames[:] = []
                continue
            for f in filenames:
                full = os.path.join(dirpath, f)
                rel = self.rel(full)
                self.all_files.append(rel)
                if rel_dir in (".", "") or rel.count("/") <= 2:
                    if f in MANIFESTS:
                        self.manifests.add(MANIFESTS[f])
                if f in SKIP_FILES or f.endswith((".min.js", ".min.css", ".map")) or self.excluded(rel):
                    continue
                yield full, rel
            if os.path.basename(dirpath) == "supabase":
                self.manifests.add("Supabase")

    def read(self, path):
        try:
            if os.path.getsize(path) > MAX_BYTES:
                return None
            with open(path, "rb") as fh:
                raw = fh.read()
            if b"\x00" in raw[:4096]:
                return None
            return raw.decode("utf-8", errors="replace")
        except OSError:
            return None

    # ---- detection
    def detect_deps(self, rel, text):
        name = os.path.basename(rel)
        deps = set()
        if name == "package.json":
            try:
                data = json.loads(text)
                for k in ("dependencies", "devDependencies", "peerDependencies"):
                    deps.update((data.get(k) or {}).keys())
                if deps:
                    self.node_has_deps = True
                for dep, ver in {**(data.get("dependencies") or {}), **(data.get("devDependencies") or {})}.items():
                    if str(ver).strip() in ("*", "latest", ""):
                        self.add("DEP001", "medium", "supply-chain", f"Unpinned dependency '{dep}': \"{ver}\"", rel, 1,
                                 f"\"{dep}\": \"{ver}\"", "CWE-1104", A03,
                                 "Pin versions (^x.y.z at minimum), commit the lockfile and use `npm ci` in CI.")
                scripts = data.get("scripts") or {}
                for s in ("preinstall", "postinstall", "install"):
                    if s in scripts and re.search(r"(curl|wget|http)", str(scripts[s])):
                        self.add("DEP002", "high", "supply-chain", f"Install script downloads remote code ({s})", rel, 1,
                                 f"{s}: {scripts[s]}", "CWE-494", A08, "Remove network calls from install hooks; vendor or verify artifacts.")
            except (ValueError, AttributeError):
                pass
        elif name in ("requirements.txt", "pyproject.toml", "Pipfile"):
            for line in text.splitlines():
                m = re.match(r"\s*\"?([A-Za-z0-9_.\-\[\]]+)", line)
                if m and not line.strip().startswith(("#", "[")):
                    deps.add(m.group(1).split("[")[0].lower())
            if name == "requirements.txt":
                unpinned = [l.strip() for l in text.splitlines()
                            if l.strip() and not l.strip().startswith(("#", "-")) and not re.search(r"(==|~=|@|>=)", l)]
                if unpinned:
                    self.add("DEP003", "low", "supply-chain", f"{len(unpinned)} unpinned Python requirement(s)", rel, 1,
                             ", ".join(unpinned[:6]), "CWE-1104", A03,
                             "Pin exact versions (pip-tools / uv / poetry lock) and audit with pip-audit.")
        elif name in ("Gemfile", "composer.json", "go.mod", "Cargo.toml", "pom.xml", "build.gradle", "pubspec.yaml"):
            for k in ("rails", "laravel", "spring-boot", "gin-gonic", "actix-web", "axum", "flutter", "symfony", "sinatra"):
                if k in text.lower():
                    self.frameworks.add({"rails": "Rails", "laravel": "Laravel", "spring-boot": "Spring Boot",
                                         "gin-gonic": "Gin", "actix-web": "Actix", "axum": "Axum",
                                         "flutter": "Flutter", "symfony": "Symfony", "sinatra": "Sinatra"}[k])
        for d in deps:
            if d.lower() in FRAMEWORK_HINTS:
                self.frameworks.add(FRAMEWORK_HINTS[d.lower()])

    # ---- main scan
    def scan(self):
        for full, rel in self.walk():
            lang = classify(full)
            if lang is None:
                continue
            text = self.read(full)
            if text is None:
                continue
            if "nocap-ignore-file" in "\n".join(text.splitlines()[:5]):
                continue
            self.files_scanned += 1
            if lang not in ("md", "json", "yaml", "conf", "xml"):
                self.lang_counts[lang] += 1
            self.detect_deps(rel, text)
            if lang == "sql":
                self.sql_text.append(text)
            if lang == "docker":
                self.check_dockerfile(rel, text)
            lines = text.splitlines()
            is_doc = lang == "md"
            for rule in RULES:
                if lang not in rule["langs"]:
                    continue
                if is_doc and rule["category"] != "secrets":
                    continue
                if rule["files"] and not rule["files"].search(rel):
                    continue
                multiline = rule["id"] in ("BAAS003", "MOB003")
                if multiline:
                    for m in rule["regex"].finditer(text):
                        ln = text.count("\n", 0, m.start()) + 1
                        self.add(rule["id"], rule["severity"], rule["category"], rule["title"], rel, ln,
                                 m.group(0).replace("\n", " "), rule["cwe"], rule["owasp"], rule["fix"])
                    continue
                if rule["id"] in ("WEB003", "IAC001", "IAC002"):
                    for m in rule["regex"].finditer(text):
                        if rule["filter"] and not rule["filter"](m):
                            continue
                        ln = text.count("\n", 0, m.start()) + 1
                        line = lines[ln - 1] if ln - 1 < len(lines) else ""
                        if "nocap-ignore" in line:
                            continue
                        self.add(rule["id"], rule["severity"], rule["category"], rule["title"], rel, ln,
                                 line.strip(), rule["cwe"], rule["owasp"], rule["fix"])
                    continue
                for i, line in enumerate(lines, 1):
                    if len(line) > 2000:
                        continue
                    m = rule["regex"].search(line)
                    if not m:
                        continue
                    if rule["filter"] and not rule["filter"](m):
                        continue
                    if "nocap-ignore" in line:
                        tag = line.split("nocap-ignore", 1)[1].strip()
                        if not tag or tag.split()[0].strip(":,") in ("", rule["id"]):
                            continue
                    snippet = line.strip()
                    if rule["category"] == "secrets":
                        s = m.group(0)
                        snippet = snippet.replace(s, s[:6] + "…[redacted " + str(len(s)) + " chars]")
                    self.add(rule["id"], rule["severity"], rule["category"], rule["title"], rel, i,
                             snippet, rule["cwe"], rule["owasp"], rule["fix"])
        self.project_checks()
        return self

    def check_dockerfile(self, rel, text):
        if not re.search(r"^\s*USER\s+(?!root\b|0\b)\S+", text, re.M | re.I):
            self.add("IAC011", "medium", "container", "Container runs as root (no non-root USER)", rel, 1,
                     "no USER instruction", "CWE-250", A02,
                     "Add a dedicated user: RUN adduser -D app && USER app (or USER node / USER nonroot for distroless).")

    def exists(self, *cands):
        for c in cands:
            if os.path.exists(os.path.join(self.root, c)):
                return c
        return None

    def project_checks(self):
        root_files = set(os.listdir(self.root))
        gi = os.path.join(self.root, ".gitignore")
        gi_text = ""
        if os.path.exists(gi):
            with open(gi, encoding="utf-8", errors="replace") as fh:
                gi_text = fh.read()
        env_files = [f for f in root_files if f.startswith(".env") and not f.endswith((".example", ".sample", ".template", ".dist"))]
        if not gi_text:
            self.add("HYG001", "medium", "hygiene", "No .gitignore — secrets and build output may be committed", ".gitignore", 0,
                     "missing", "CWE-538", A02, "Add a .gitignore covering .env*, keys, build output and dependency folders.")
        if env_files and not re.search(r"^\s*\.env", gi_text, re.M):
            self.add("HYG002", "critical", "secrets", ".env file present but not git-ignored", env_files[0], 0,
                     ", ".join(env_files), "CWE-538", A02,
                     "Add `.env*` (and `!.env.example`) to .gitignore, run `git rm --cached .env`, rotate every secret in it.")
        if env_files and not any(f.endswith((".example", ".sample", ".template")) for f in root_files):
            self.add("HYG003", "low", "hygiene", "No .env.example documenting required configuration", ".env.example", 0,
                     "missing", "CWE-1059", A02, "Commit a .env.example with every variable name and a safe placeholder value.")
        for eco, locks in LOCKFILES.items():
            if eco == "Node.js" and not self.node_has_deps:
                continue
            if eco in self.manifests and not self.exists(*locks):
                self.add("HYG004", "medium", "supply-chain", f"{eco} project without a lockfile", "/", 0,
                         f"expected one of: {', '.join(locks)}", "CWE-1104", A03,
                         "Commit the lockfile so builds are reproducible and dependency audits are meaningful.")
        if not self.exists(".github/dependabot.yml", ".github/dependabot.yaml", "renovate.json", ".renovaterc", ".github/renovate.json"):
            self.add("HYG005", "low", "supply-chain", "No automated dependency updates (Dependabot/Renovate)", "/", 0,
                     "missing", "CWE-1104", A03, "Enable Dependabot or Renovate plus security alerts.")
        has_tests = any(re.search(r"(^|/)(tests?|__tests__|spec|e2e|cypress|playwright)(/|$)|(\.|_)(test|spec)\.\w+$|^test_.*\.py$|_test\.go$",
                                  f) for f in self.all_files)
        if not has_tests:
            self.add("HYG006", "medium", "quality", "No automated tests found", "/", 0, "missing", "CWE-1164", A06,
                     "Add unit tests for business logic and integration tests for auth/permissions — especially negative cases (user A cannot read user B's data).")
        if not self.exists(".github/workflows", ".gitlab-ci.yml", "azure-pipelines.yml", ".circleci", "Jenkinsfile", "bitbucket-pipelines.yml"):
            self.add("HYG007", "low", "quality", "No CI pipeline", "/", 0, "missing", "CWE-1127", A08,
                     "Run tests, lint, dependency audit and `nocap` on every pull request.")
        if "Supabase" in (self.manifests | self.frameworks) and self.sql_text:
            sql = "\n".join(self.sql_text).lower()
            tables = len(re.findall(r"create\s+table", sql))
            rls = len(re.findall(r"enable\s+row\s+level\s+security", sql))
            if tables and rls < tables:
                self.add("BAAS004", "high", "access", f"{tables - rls} of {tables} tables may lack Row Level Security", "supabase/", 0,
                         f"create table: {tables}, enable RLS: {rls}", "CWE-284", A01,
                         "Run `alter table <t> enable row level security;` for every table and add owner-scoped policies.")

    # ---- results
    def docs_status(self):
        return {k: bool(self.exists(*v)) for k, v in EXPECTED_DOCS.items()}

    def score(self):
        per_rule = Counter()
        penalty = 0
        for f in self.findings:
            key = f["rule"]
            per_rule[key] += 1
            if per_rule[key] <= 3:  # cap noisy rules
                penalty += SEV_WEIGHT[f["severity"]]
        security = max(0, 100 - penalty)
        docs = self.docs_status()
        doc_score = round(100 * sum(docs.values()) / len(docs))
        overall = round(0.7 * security + 0.3 * doc_score)
        sev = Counter(f["severity"] for f in self.findings)
        if sev["critical"]:
            overall = min(overall, 49)
        elif sev["high"]:
            overall = min(overall, 79)
        grade = ("A+" if overall >= 95 else "A" if overall >= 85 else "B" if overall >= 70 else
                 "C" if overall >= 55 else "D" if overall >= 40 else "F")
        return {"overall": overall, "grade": grade, "verdict": VERDICT[grade], "security": security, "docs": doc_score, "by_severity": dict(sev)}

    def stack(self):
        langs = [l for l, _ in self.lang_counts.most_common()]
        return {"languages": langs, "platforms": sorted(self.manifests), "frameworks": sorted(self.frameworks)}

    def recommendations(self):
        st = self.stack()
        rec = {"checklists": ["checklists/security/OWASP_TOP10_2025.md", "checklists/security/VIBE_CODING_TOP25.md",
                              "checklists/quality/DESIGN_QUALITY.md"], "compliance": []}
        lang_map = {"js": "JAVASCRIPT_TYPESCRIPT", "py": "PYTHON", "java": "JAVA_KOTLIN", "go": "GO", "php": "PHP",
                    "rb": "RUBY", "cs": "CSHARP_DOTNET", "rs": "RUST", "c": "C_CPP", "swift": "SWIFT_IOS",
                    "dart": "DART_FLUTTER", "sql": "SQL_DATABASES", "sol": "SOLIDITY"}
        for l in st["languages"]:
            if l in lang_map:
                rec["checklists"].append(f"checklists/languages/{lang_map[l]}.md")
        allp = set(st["platforms"]) | set(st["frameworks"])
        if allp & {"Express", "NestJS", "Fastify", "Hono", "FastAPI", "Flask", "Django", "Spring Boot", "Gin", "Rails", "Laravel"}:
            rec["checklists"].append("checklists/security/OWASP_API_TOP10_2023.md")
        if allp & {"React", "Next.js", "Vue", "Nuxt", "Svelte", "SvelteKit", "Angular"}:
            rec["checklists"].append("checklists/platforms/WEB_FRONTEND.md")
        if allp & {"React Native", "Expo", "Flutter", "Flutter/Dart", "Swift"} or "swift" in st["languages"]:
            rec["checklists"].append("checklists/platforms/MOBILE.md")
        if allp & {"Docker", "Docker Compose", "Helm"} or "tf" in self.lang_counts:
            rec["checklists"].append("checklists/platforms/CLOUD_CONTAINERS_IAC.md")
        if allp & set(SENSITIVE_DATA["ai"]):
            rec["checklists"].append("checklists/security/OWASP_LLM_TOP10_2025.md")
            rec["compliance"].append("checklists/compliance/EU_AI_ACT.md")
        if allp & {"Supabase", "Firebase"}:
            rec["checklists"].append("checklists/platforms/BAAS_SUPABASE_FIREBASE.md")
        if allp & set(SENSITIVE_DATA["payments"]):
            rec["compliance"].append("checklists/compliance/PCI_DSS_4.md")
        rec["compliance"] += ["checklists/compliance/GDPR.md", "checklists/compliance/INDIA_DPDP.md",
                              "checklists/compliance/WCAG_2_2_ACCESSIBILITY.md"]
        rec["checklists"] = list(dict.fromkeys(rec["checklists"]))
        return rec


# --------------------------------------------------------------------------- #
# Output
# --------------------------------------------------------------------------- #
VERDICT = {
    "A+": "it's giving secure ✨ (no cap)", "A": "solid, no cap 💪", "B": "mid but fixable 🛠️",
    "C": "kinda sus 👀", "D": "red flags everywhere 🚩", "F": "cooked 💀 — fix the criticals first",
}
GRADE_COLOR = {"A+": "#16a34a", "A": "#22c55e", "B": "#84cc16", "C": "#eab308", "D": "#f97316", "F": "#dc2626"}


def badge_svg(score):
    label, value = "NoCap", f"{score['grade']} · {score['overall']}/100"
    lw, vw = 74, 8 + 7 * len(value)
    color = GRADE_COLOR[score["grade"]]
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{lw + vw}" height="20" role="img" aria-label="{label}: {value}">
<linearGradient id="s" x2="0" y2="100%"><stop offset="0" stop-color="#bbb" stop-opacity=".1"/><stop offset="1" stop-opacity=".1"/></linearGradient>
<clipPath id="r"><rect width="{lw + vw}" height="20" rx="3" fill="#fff"/></clipPath>
<g clip-path="url(#r)"><rect width="{lw}" height="20" fill="#24123d"/><rect x="{lw}" width="{vw}" height="20" fill="{color}"/><rect width="{lw + vw}" height="20" fill="url(#s)"/></g>
<g fill="#fff" text-anchor="middle" font-family="Verdana,Geneva,DejaVu Sans,sans-serif" font-size="11">
<text x="{lw / 2}" y="14">{label}</text><text x="{lw + vw / 2}" y="14">{value}</text></g></svg>
"""


def markdown_report(sc: Scanner):
    s, st, docs, rec = sc.score(), sc.stack(), sc.docs_status(), sc.recommendations()
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    out = [f"# NoCap Report\n",
           f"> Generated {now} by NoCap Scanner v{VERSION} · {sc.files_scanned} files scanned\n",
           f"## Score: **{s['grade']} — {s['overall']}/100** · _{s['verdict']}_\n",
           "| Security | Documentation | Critical | High | Medium | Low | Info |",
           "|---|---|---|---|---|---|---|",
           f"| {s['security']}/100 | {s['docs']}/100 | {s['by_severity'].get('critical', 0)} | {s['by_severity'].get('high', 0)} | "
           f"{s['by_severity'].get('medium', 0)} | {s['by_severity'].get('low', 0)} | {s['by_severity'].get('info', 0)} |\n",
           "_Any critical finding caps the score at 49; any high finding caps it at 79._\n",
           "## Detected stack\n",
           f"- **Languages:** {', '.join(LANG_NAMES.get(l, l) for l in st['languages']) or 'n/a'}",
           f"- **Platforms:** {', '.join(st['platforms']) or 'n/a'}",
           f"- **Frameworks / services:** {', '.join(st['frameworks']) or 'n/a'}\n",
           "## Documentation coverage\n",
           "| Document | Status |", "|---|---|"]
    out += [f"| {k} | {'✅' if v else '❌ missing'} |" for k, v in docs.items()]
    out.append("\n> Generate missing docs: open your AI assistant and say **`nocap docs`** (or paste `MASTER_PROMPT.md`).\n")
    out.append("## Findings\n")
    if not sc.findings:
        out.append("No findings from automated rules. 🎉 Now run the manual checklists below — scanners cannot see logic flaws.\n")
    grouped = defaultdict(list)
    for f in sc.findings:
        grouped[f["severity"]].append(f)
    icons = {"critical": "🟥", "high": "🟧", "medium": "🟨", "low": "🟦", "info": "⬜"}
    for sev in SEV_ORDER:
        if not grouped[sev]:
            continue
        out.append(f"### {icons[sev]} {sev.capitalize()} ({len(grouped[sev])})\n")
        by_rule = defaultdict(list)
        for f in grouped[sev]:
            by_rule[(f["rule"], f["title"])].append(f)
        for (rid, title), items in by_rule.items():
            first = items[0]
            out.append(f"#### `{rid}` {title}")
            out.append(f"_{first['cwe']} · {first['owasp']}_\n")
            for it in items[:25]:
                loc = f"{it['file']}:{it['line']}" if it["line"] else it["file"]
                snip = it["snippet"].replace("`", "'")
                out.append(f"- `{loc}` — `{snip}`")
            if len(items) > 25:
                out.append(f"- …and {len(items) - 25} more")
            out.append(f"\n**✅ Standard fix:** {first['fix']}\n")
    out.append("## Next: manual review checklists for your stack\n")
    out += [f"- [ ] `{c}`" for c in rec["checklists"]]
    out.append("\n## Compliance frameworks to review\n")
    out += [f"- [ ] `{c}`" for c in rec["compliance"]]
    out.append("\n## Also run (dependency CVEs need a live database)\n")
    out += ["- `npx osv-scanner -r .` or `osv-scanner scan source -r .` (all ecosystems)",
            "- `npm audit --omit=dev` · `pip-audit` · `bundle audit` · `composer audit` · `cargo audit` · `govulncheck ./...`",
            "- `gitleaks detect` (scans full git history for secrets)",
            "- Semgrep / CodeQL for deeper SAST, OWASP ZAP for DAST on a staging URL\n",
            "---", "_⚠️ **Disclaimer:** NoCap is a development aid, not a guarantee. A clean report or high score does **not** mean the software is "
            "secure or compliant. Final verification, testing and compliance are the user's own responsibility. Provided \"as is\" without "
            "warranty; the author accepts no liability. See TERMS.md._"]
    return "\n".join(out) + "\n"


def console_summary(sc: Scanner, color=True):
    s = sc.score()
    c = (lambda code, t: f"\033[{code}m{t}\033[0m") if color else (lambda code, t: t)
    sevc = {"critical": "1;31", "high": "31", "medium": "33", "low": "36", "info": "37"}
    print(c("1;35", "\n  ███╗   ██╗ ██████╗  ██████╗ █████╗ ██████╗ \n  ████╗  ██║██╔═══██╗██╔════╝██╔══██╗██╔══██╗\n  ██╔██╗ ██║██║   ██║██║     ███████║██████╔╝\n  ██║╚██╗██║██║   ██║██║     ██╔══██║██╔═══╝ \n  ██║ ╚████║╚██████╔╝╚██████╗██║  ██║██║     \n  ╚═╝  ╚═══╝ ╚═════╝  ╚═════╝╚═╝  ╚═╝╚═╝     ") + f"  v{VERSION}\n  {c('2', 'docs + security for AI-built apps. no cap.')}\n")
    st = sc.stack()
    names = [LANG_NAMES.get(l, l) for l in st["languages"]] + st["platforms"] + st["frameworks"]
    print(f"  Stack: {', '.join(dict.fromkeys(names)) or 'unknown'}")
    print(f"  Files scanned: {sc.files_scanned}\n")
    for f in sorted(sc.findings, key=lambda x: SEV_ORDER.index(x["severity"]))[:40]:
        loc = f"{f['file']}:{f['line']}" if f["line"] else f["file"]
        sev_label = c(sevc[f["severity"]], f["severity"].upper().ljust(8))
        print(f"  {sev_label} {f['rule']:<8} {f['title']}\n           {c('2', loc)}")
    if len(sc.findings) > 40:
        print(f"\n  …{len(sc.findings) - 40} more in the report")
    print(f"\n  Score: {c('1', s['grade'] + ' ' + str(s['overall']) + '/100')}  (security {s['security']}, docs {s['docs']})  {s['verdict']}")
    print("  " + "  ".join(f"{k}:{s['by_severity'].get(k, 0)}" for k in SEV_ORDER))
    print(c("2", "  ⚠ Development aid only — final checks are your responsibility. No warranty. See TERMS.md") + "\n")


def main(argv=None):
    ap = argparse.ArgumentParser(prog="nocap", description="Security, hygiene & documentation audit for any codebase.")
    ap.add_argument("path", nargs="?", default=".")
    ap.add_argument("--out", default="NOCAP_REPORT.md", help="Markdown report path (relative to scanned path). '-' to skip.")
    ap.add_argument("--json", dest="json_out", help="Write machine-readable JSON results to this path.")
    ap.add_argument("--badge", help="Write an SVG score badge to this path.")
    ap.add_argument("--fail-on", default="none", choices=SEV_ORDER + ["none"], help="Exit 1 if a finding at/above this severity exists.")
    ap.add_argument("--min-severity", default="info", choices=SEV_ORDER, help="Hide findings below this severity.")
    ap.add_argument("--exclude", action="append", default=[], help="Glob to exclude (repeatable).")
    ap.add_argument("--no-color", action="store_true")
    ap.add_argument("--quiet", action="store_true")
    ap.add_argument("--list-rules", action="store_true")
    ap.add_argument("--version", action="version", version=f"nocap {VERSION}")
    a = ap.parse_args(argv)
    for stream in (sys.stdout, sys.stderr):  # Windows consoles: never crash on emoji / box characters
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass

    if a.list_rules:
        for r in RULES:
            print(f"{r['id']:<8} {r['severity']:<9} {r['category']:<14} {r['title']}")
        return 0
    if not os.path.isdir(a.path):
        print(f"error: {a.path} is not a directory", file=sys.stderr)
        return 2
    excludes = a.exclude + ([a.out] if a.out != "-" else [])
    sc = Scanner(a.path, excludes, a.min_severity).scan()
    if not a.quiet:
        console_summary(sc, color=not a.no_color and sys.stdout.isatty())
    if a.out != "-":
        p = a.out if os.path.isabs(a.out) else os.path.join(a.path, a.out)
        with open(p, "w", encoding="utf-8") as fh:
            fh.write(markdown_report(sc))
        if not a.quiet:
            print(f"  Report → {p}")
    if a.json_out:
        with open(a.json_out, "w", encoding="utf-8") as fh:
            json.dump({"version": VERSION, "score": sc.score(), "stack": sc.stack(), "docs": sc.docs_status(),
                       "recommendations": sc.recommendations(), "findings": sc.findings}, fh, indent=2)
    if a.badge:
        with open(a.badge, "w", encoding="utf-8") as fh:
            fh.write(badge_svg(sc.score()))
    if a.fail_on != "none":
        limit = SEV_ORDER.index(a.fail_on)
        if any(SEV_ORDER.index(f["severity"]) <= limit for f in sc.findings):
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
