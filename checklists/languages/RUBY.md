# Ruby (Rails, Sinatra) — Security & Standards Checklist

## Checks and standard fixes
- [ ] **SQL** → `where(email: v)` or `where('email = ?', v)`; never `#{}` in SQL; `sanitize_sql` for `order`
- [ ] **Mass assignment** → strong params `params.require(:user).permit(:name)`; never `permit!`
- [ ] **XSS** → ERB escapes by default; avoid `raw`/`html_safe` on user data; `sanitize` helper
- [ ] **CSRF** → `protect_from_forgery with: :exception`; don't skip `verify_authenticity_token`
- [ ] **Command execution** → `system('cmd', arg)` array form; avoid backticks with input
- [ ] **Deserialisation** → no `Marshal.load` on untrusted data; `YAML.safe_load`
- [ ] **Authorisation** → Pundit/CanCanCan with `verify_authorized` after_action; scope queries `current_user.posts.find(id)`
- [ ] **Secrets** → Rails credentials / env; `config.force_ssl = true`
- [ ] **Redirects** → `redirect_to` with `allow_other_host: false` (Rails 7+)
- [ ] **Dependencies** → `Gemfile.lock`; `bundle audit`

## Tools
Brakeman, bundler-audit, RuboCop, Semgrep.
