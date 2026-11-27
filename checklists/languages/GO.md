# Go — Security & Standards Checklist

## Checks and standard fixes
- [ ] **SQL** → placeholders `db.QueryContext(ctx, "... $1", v)`; sqlc/GORM; never `fmt.Sprintf` SQL
- [ ] **Command execution** → `exec.CommandContext(ctx, "bin", args...)`; never `sh -c` with input
- [ ] **TLS** → never `InsecureSkipVerify: true`; `MinVersion: tls.VersionTLS12`
- [ ] **Randomness** → `crypto/rand`, not `math/rand`, for secrets
- [ ] **Templates** → `html/template` (auto-escape), not `text/template`, for HTML; avoid `template.HTML(userInput)`
- [ ] **HTTP server** → set `ReadHeaderTimeout`, `ReadTimeout`, `WriteTimeout`, `IdleTimeout`; `http.MaxBytesReader` for bodies
- [ ] **Path traversal** → `filepath.Clean` + prefix check, or `os.Root`/`fs.Sub` scoped FS
- [ ] **Concurrency** → run tests with `-race`; protect shared maps
- [ ] **Errors** → always check `err`; don't leak internals in responses
- [ ] **Dependencies** → `go mod tidy`, `go.sum` committed, `govulncheck ./...`

## Tools
`govulncheck`, `gosec`, `staticcheck`, `go vet`, Semgrep.
