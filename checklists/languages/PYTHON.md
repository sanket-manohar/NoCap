# Python (Django, Flask, FastAPI, scripts, ML) — Security & Standards Checklist

## Checks and standard fixes
- [ ] **SQL** → ORM or DB-API params `cursor.execute(sql, (v,))`; never f-strings/%/.format; avoid `.raw()`/`.extra()` with input
- [ ] **Command execution** → `subprocess.run([...], shell=False, check=True, timeout=…)`; no `os.system`
- [ ] **Deserialisation** → no `pickle`/`marshal`/`shelve` on untrusted data; `yaml.safe_load`; `torch.load(weights_only=True)`; prefer safetensors
- [ ] **Validation** → pydantic models (FastAPI), Django forms/serializers, marshmallow
- [ ] **Django settings** → `DEBUG=False`, real `ALLOWED_HOSTS`, `SECURE_SSL_REDIRECT`, `SESSION_COOKIE_SECURE`, `CSRF_COOKIE_SECURE`, `SECURE_HSTS_SECONDS`; run `manage.py check --deploy`
- [ ] **Flask** → never `debug=True` in prod; `SECRET_KEY` from env; Flask-WTF CSRF; Flask-Talisman for headers
- [ ] **FastAPI** → dependencies for auth (`Depends(get_current_user)`), per-object checks, `CORSMiddleware` allow-list, response models to avoid over-exposure
- [ ] **Templates** → Jinja2 autoescape on; avoid `|safe`/`mark_safe` on user data
- [ ] **Crypto** → `secrets` module for tokens; `argon2-cffi`/`bcrypt`/Django default PBKDF2+; `cryptography` AESGCM/Fernet
- [ ] **HTTP clients** → `requests` with `timeout=`, never `verify=False`; SSRF allow-list
- [ ] **XML** → `defusedxml`
- [ ] **Files** → `werkzeug.utils.secure_filename`, size limits, store outside static dirs
- [ ] **Temp files** → `tempfile.NamedTemporaryFile`/`mkstemp`, not `mktemp`
- [ ] **Dependencies** → pin with uv/poetry/pip-tools; `pip-audit`; verify package names on PyPI
- [ ] **Asserts** → never use `assert` for security checks (stripped with -O)

## Correct pattern
```python
# ✅ FastAPI: auth dependency + ownership check + parameterised ORM query
@router.get("/notes/{note_id}", response_model=NoteOut)
def read_note(note_id: UUID, user: User = Depends(current_user), db: Session = Depends(get_db)):
    note = db.scalar(select(Note).where(Note.id == note_id, Note.owner_id == user.id))
    if note is None:
        raise HTTPException(status_code=404)
    return note
```

## Tools
Bandit, Semgrep, pip-audit, Ruff (`S` rules = flake8-bandit), mypy/pyright, Django `check --deploy`.
