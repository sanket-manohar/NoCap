# Web Frontend Checklist (React, Next.js, Vue, Svelte, Angular, static sites)

## Security
- [ ] No secrets in client code or public env vars. Run `grep -r "sk_\|secret\|private" .next/static dist/` after a build to check
- [ ] Strict **Content-Security-Policy** (nonce/hash-based `script-src`, `object-src 'none'`, `base-uri 'self'`, `frame-ancestors 'none'`)
- [ ] HSTS, `X-Content-Type-Options: nosniff`, `Referrer-Policy`, `Permissions-Policy`
- [ ] No `dangerouslySetInnerHTML` / `v-html` / `innerHTML` with untrusted data (or DOMPurify first)
- [ ] Session tokens in HttpOnly cookies, not localStorage
- [ ] Third-party scripts minimised, loaded with SRI where possible, and covered by the CSP
- [ ] Production source maps not publicly served
- [ ] Open-redirect-safe navigation (`?next=` validated as a relative path)
- [ ] `target="_blank"` links use `rel="noopener noreferrer"`
- [ ] Clickjacking prevented (`frame-ancestors`)
- [ ] Authorisation never relies on hidden UI. The API enforces it

## Accessibility (WCAG 2.2 AA)
- [ ] Every interactive element is keyboard-reachable with a visible focus indicator that isn't obscured
- [ ] Semantic HTML first, ARIA only when needed. Form inputs have labels
- [ ] Contrast ≥ 4.5:1 for text and ≥ 3:1 for UI components
- [ ] Target size ≥ 24×24 CSS px
- [ ] `prefers-reduced-motion` respected. No auto-playing content longer than 5 s without controls
- [ ] Alt text on images. Captions for video

## Performance (Core Web Vitals)
- [ ] LCP < 2.5 s, INP < 200 ms, CLS < 0.1
- [ ] Images optimised (`next/image`, AVIF/WebP, explicit sizes). Fonts self-hosted with `font-display: swap`
- [ ] Code-splitting. JS budget enforced in CI

## SEO & robustness
- [ ] Meta tags, sitemap, robots.txt (and robots.txt doesn't reveal sensitive paths)
- [ ] Error boundaries plus friendly 404/500 pages
- [ ] Privacy-respecting analytics with consent where required

**Tools:** Lighthouse, axe DevTools / `@axe-core/playwright`, securityheaders.com, Mozilla Observatory, CSP Evaluator.
