# Rust — Security & Standards Checklist

## Checks and standard fixes
- [ ] **unsafe** → minimise; document invariants with `// SAFETY:`; test with Miri; `#![forbid(unsafe_code)]` where possible
- [ ] **SQL** → sqlx `query!`/bind params, Diesel; never `format!` into SQL
- [ ] **Panics** → avoid `unwrap()`/`expect()` on external input in servers; return `Result`
- [ ] **Integer overflow** → `checked_*`/`saturating_*` for untrusted arithmetic
- [ ] **TLS** → rustls; never `danger_accept_invalid_certs(true)`
- [ ] **Web (axum/actix)** → extractor-based validation (`validator` crate), body size limits, tower middleware for auth/rate limit/timeouts
- [ ] **Crypto** → RustCrypto/ring/`argon2` crate; `rand::rngs::OsRng` for secrets
- [ ] **Dependencies** → `cargo audit`, `cargo deny` (licences, advisories, bans), `Cargo.lock` committed for binaries

## Tools
`cargo audit`, `cargo deny`, `cargo clippy -- -D warnings`, Miri, cargo-fuzz.
