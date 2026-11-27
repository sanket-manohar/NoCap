# PHP (Laravel, Symfony, WordPress, vanilla) — Security & Standards Checklist

## Checks and standard fixes
- [ ] **SQL** → PDO prepared statements with `PDO::ATTR_EMULATE_PREPARES=false`; Eloquent/Doctrine bindings; never `$_GET` in queries
- [ ] **XSS** → Blade `{{ }}` / Twig auto-escape; avoid `{!! !!}`; `htmlspecialchars($v, ENT_QUOTES, 'UTF-8')`
- [ ] **Command execution** → avoid `exec/system/shell_exec`; `escapeshellarg` as last resort; Symfony Process with arg arrays
- [ ] **File inclusion** → never include paths from input; `allow_url_include=Off`
- [ ] **Deserialisation** → `json_decode`; `unserialize($s, ['allowed_classes' => false])` if unavoidable
- [ ] **Mass assignment** → Laravel `$fillable` allow-list; never `$guarded = []`
- [ ] **Passwords** → `password_hash(PASSWORD_ARGON2ID)` / `password_verify`
- [ ] **Sessions** → `session.cookie_httponly=1`, `cookie_secure=1`, `cookie_samesite=Lax`, `session_regenerate_id(true)` on login
- [ ] **Config** → `display_errors=Off`, `expose_php=Off`, `APP_DEBUG=false`, `.env` outside web root
- [ ] **Uploads** → `finfo` MIME check, random names, store outside public dir
- [ ] **WordPress** → nonces (`wp_verify_nonce`), capability checks (`current_user_can`), `$wpdb->prepare`, `esc_html/esc_attr/esc_url`
- [ ] **Dependencies** → `composer.lock` committed; `composer audit`

## Tools
PHPStan/Psalm (taint analysis), Semgrep, `composer audit`, WPScan for WordPress.
