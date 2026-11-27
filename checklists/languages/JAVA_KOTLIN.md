# Java / Kotlin (Spring Boot, Jakarta EE, Ktor, Android backend) — Security & Standards Checklist

## Checks and standard fixes
- [ ] **SQL** → `PreparedStatement`, JPA named params, Spring Data derived queries; never concatenate into `createQuery`/`createNativeQuery`
- [ ] **Spring Security** → `SecurityFilterChain` with `authorizeHttpRequests` deny-by-default; `@PreAuthorize` with ownership checks (`@PostAuthorize` / custom `PermissionEvaluator`)
- [ ] **CSRF** → keep enabled for cookie sessions; disable only for stateless token APIs
- [ ] **Deserialisation** → no `ObjectInputStream` on untrusted data; Jackson without default typing; `ObjectInputFilter` if unavoidable
- [ ] **XXE** → `factory.setFeature("http://apache.org/xml/features/disallow-doctype-decl", true)`
- [ ] **Command execution** → `ProcessBuilder` with fixed command + validated args
- [ ] **Crypto** → `SecureRandom`; AES/GCM/NoPadding; `BCryptPasswordEncoder`/`Argon2PasswordEncoder`; never `Cipher.getInstance("AES")` (defaults to ECB)
- [ ] **Validation** → Bean Validation (`@Valid`, `@NotBlank`, `@Size`) on DTOs; never bind entities directly (mass assignment)
- [ ] **Actuator** → expose only `health`/`info`; secure the rest
- [ ] **Logging** → Log4j ≥ 2.17.1; no user input in log patterns; mask PII
- [ ] **Templates** → Thymeleaf `th:text` (escaped), avoid `th:utext`
- [ ] **Dependencies** → Maven/Gradle dependency locking; OWASP Dependency-Check; Gradle verification metadata

## Tools
SpotBugs + FindSecBugs, Semgrep, CodeQL, OWASP Dependency-Check, detekt (Kotlin).
