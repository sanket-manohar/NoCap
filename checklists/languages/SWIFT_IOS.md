# Swift / iOS / macOS — Security & Standards Checklist

## Checks and standard fixes
- [ ] **Secure storage** → Keychain (`kSecAttrAccessibleWhenUnlockedThisDeviceOnly`); never UserDefaults for tokens
- [ ] **Transport** → keep ATS on; no `NSAllowsArbitraryLoads`; certificate pinning for high-risk apps
- [ ] **Secrets** → no API keys in the binary/Info.plist — they are extractable; proxy through your backend
- [ ] **WebViews** → `WKWebView` only; limit `WKScriptMessageHandler` exposure; validate URLs
- [ ] **Deep links / Universal links** → validate all parameters; never perform sensitive actions without confirmation
- [ ] **Logging** → no PII in `print`/`os_log` (use `privacy: .private`)
- [ ] **Biometrics** → LocalAuthentication bound to Keychain items (`.biometryCurrentSet`), not a boolean check
- [ ] **Data protection** → file protection `.completeUnlessOpen`/`.complete`; exclude sensitive files from backups

## Tools
MobSF, SwiftLint, Xcode static analyzer, OWASP MASVS/MASTG.
