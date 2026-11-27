# C# / .NET (ASP.NET Core, Blazor, MAUI) — Security & Standards Checklist

## Checks and standard fixes
- [ ] **SQL** → EF Core LINQ / `FromSqlInterpolated`; `SqlParameter`; never `FromSqlRaw($"…{input}")`
- [ ] **Authorisation** → `[Authorize]` globally (`FallbackPolicy`), resource-based `IAuthorizationService` for ownership
- [ ] **Anti-forgery** → `[ValidateAntiForgeryToken]` / auto-validation for cookie auth
- [ ] **Deserialisation** → System.Text.Json; never BinaryFormatter (removed in .NET 9); no `TypeNameHandling.All`
- [ ] **XSS** → Razor encodes by default; avoid `Html.Raw` on user input
- [ ] **Crypto** → `RandomNumberGenerator`; `AesGcm`; ASP.NET Identity hasher; Data Protection API for tokens
- [ ] **TLS** → never return `true` from `ServerCertificateCustomValidationCallback`; `UseHsts()`, `UseHttpsRedirection()`
- [ ] **Secrets** → User Secrets (dev), Azure Key Vault / env in prod; not in `appsettings.json`
- [ ] **Validation** → DataAnnotations / FluentValidation on DTOs; `[ApiController]` auto 400
- [ ] **Rate limiting** → built-in `AddRateLimiter` (.NET 7+)
- [ ] **Dependencies** → `dotnet list package --vulnerable`; lock files (`RestorePackagesWithLockFile`)

## Tools
Roslyn analyzers + `SecurityCodeScan`, Semgrep, CodeQL, `dotnet list package --vulnerable`.
