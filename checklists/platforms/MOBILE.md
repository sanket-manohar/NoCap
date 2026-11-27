# Mobile Checklist (iOS, Android, React Native, Flutter, Expo)

Based on **OWASP MASVS v2** (STORAGE, CRYPTO, AUTH, NETWORK, PLATFORM, CODE, RESILIENCE, PRIVACY).

- [ ] **No secrets in the app binary.** Anything shipped can be extracted. Proxy third-party APIs through your backend
- [ ] Tokens kept in Keychain / Android Keystore (EncryptedSharedPreferences, `expo-secure-store`, `flutter_secure_storage`)
- [ ] HTTPS only: ATS enabled (iOS), `usesCleartextTraffic=false` plus a Network Security Config (Android)
- [ ] Certificate pinning for high-risk apps (banking, health), with a backup pin and a rotation plan
- [ ] Release builds: `debuggable=false`, logging stripped, obfuscation (R8/ProGuard)
- [ ] `allowBackup=false` or backup rules exclude sensitive data
- [ ] Exported Android components (`exported=true`) protected by permissions. Intents validated
- [ ] Deep links and universal links validated. No sensitive action from a link without confirmation
- [ ] WebViews: no JS bridges to untrusted content, file access disabled
- [ ] Biometrics tied to a cryptographic key (Keychain/Keystore), not a boolean
- [ ] Screenshot/recents protection for sensitive screens (`FLAG_SECURE`)
- [ ] Server enforces all authorisation. The client is fully attacker-controlled
- [ ] App attestation for abuse-prone APIs (Play Integrity, App Attest, Firebase App Check)
- [ ] Privacy: permissions requested just-in-time, App Store privacy labels / Play Data safety form accurate, tracking consent (ATT)
- [ ] Forced-update mechanism for critical security fixes

**Tools:** MobSF, OWASP MASTG test cases, Frida/objection (for testing your own app), Android Lint, Xcode analyzer.
