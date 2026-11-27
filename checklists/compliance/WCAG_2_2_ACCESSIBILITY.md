# WCAG 2.2 AA — Accessibility Checklist

WCAG 2.2 (W3C Recommendation, Oct 2023) is the reference for the **European Accessibility Act** (applies from 28 June 2025), US ADA case law,
Section 508 (WCAG 2.0 AA), and India's Rights of Persons with Disabilities Act/GIGW guidelines.

## POUR essentials
**Perceivable**
- [ ] Text alternatives for images and icons (1.1.1)
- [ ] Captions and transcripts for media (1.2.x)
- [ ] Semantic structure: headings, lists, landmarks, labelled form fields (1.3.1)
- [ ] Contrast: 4.5:1 for text, 3:1 for large text and UI components (1.4.3, 1.4.11)
- [ ] Content reflows at 320 px width and 200% zoom (1.4.10, 1.4.4)

**Operable**
- [ ] Everything works by keyboard. No keyboard traps (2.1.1, 2.1.2)
- [ ] Visible focus (2.4.7) and **focus not obscured** by sticky headers (2.4.11, new in 2.2)
- [ ] **Dragging movements** have a single-pointer alternative (2.5.7, new)
- [ ] **Target size ≥ 24×24 px** (2.5.8, new)
- [ ] Skip link. Logical focus order. Descriptive page titles and link text

**Understandable**
- [ ] Page language set (3.1.1). Consistent navigation
- [ ] **Consistent help** location (3.2.6, new)
- [ ] Form errors identified with suggestions (3.3.1, 3.3.3)
- [ ] **Redundant entry** avoided (3.3.7, new)
- [ ] **Accessible authentication**: no cognitive tests such as puzzles or transcription. Allow paste and password managers (3.3.8, new)

**Robust**
- [ ] Valid name/role/value for custom components. ARIA used correctly (4.1.2)
- [ ] Status messages announced (4.1.3)

**Tools:** axe-core / `@axe-core/playwright` in CI, Lighthouse, WAVE, keyboard-only testing, NVDA/VoiceOver smoke tests.
