# C / C++ — Security & Standards Checklist

## Checks and standard fixes
- [ ] **Unsafe functions** → ban `gets`, `strcpy`, `strcat`, `sprintf`, `scanf("%s")`; use `fgets`, `snprintf`, `strlcpy`, `std::string`, `std::span`
- [ ] **Format strings** → literal formats only: `printf("%s", s)`
- [ ] **Memory** → RAII/smart pointers (`std::unique_ptr`), bounds-checked containers (`.at()`), no manual `new/delete`
- [ ] **Integer overflow** → check before arithmetic for sizes; use `size_t`; `__builtin_mul_overflow`
- [ ] **Compiler hardening** → `-Wall -Wextra -Werror -O2 -D_FORTIFY_SOURCE=3 -fstack-protector-strong -fPIE -pie -Wl,-z,relro,-z,now`
- [ ] **Sanitisers in CI** → ASan, UBSan, MSan, TSan; fuzz parsers with libFuzzer/AFL++
- [ ] **Command execution** → avoid `system()`/`popen()`; `execve` with fixed path and args
- [ ] **Guidelines** → SEI CERT C/C++, C++ Core Guidelines, MISRA (embedded)

## Tools
clang-tidy, cppcheck, CodeQL, Coverity, sanitizers, libFuzzer/AFL++.
