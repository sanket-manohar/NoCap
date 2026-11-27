# Dart / Flutter — Security & Standards Checklist

## Checks and standard fixes
- [ ] **Secure storage** → `flutter_secure_storage`; never SharedPreferences for tokens
- [ ] **Secrets** → no API keys in Dart code or `--dart-define` for real secrets (extractable); use a backend
- [ ] **Transport** → HTTPS only; Android network security config; iOS ATS; pinning via `http_certificate_pinning` where needed
- [ ] **Obfuscation** → `flutter build --obfuscate --split-debug-info` (raises cost, not a security control)
- [ ] **Firebase** → security rules + App Check; never rely on client-side checks
- [ ] **WebView** → restrict JavaScript channels; validate navigation
- [ ] **Dependencies** → `pubspec.lock` committed; `dart pub outdated`; review package publishers

## Tools
MobSF, `dart analyze`, OWASP MASVS/MASTG.
