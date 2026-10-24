---
name: mkl-typography
description: Mike's web typography defaults, traps and checks. Use when setting or reviewing type on a page or in product UI, choosing fonts, a type scale, line-height, tracking, figures and numbers, dark-mode weights, font loading, OG images, or text in Bulgarian.
---

# Typography

This skill holds what general typography knowledge doesn't: the defaults Mike uses in his own products (yesterday and gh-dashboard), the traps that only show up in the served font file or in a real browser, and scripts that check them. The craft itself (measure, leading, hierarchy, real quotes and dashes, `text-wrap`, tabular figures in tables, WCAG zoom and text spacing) is assumed. Apply it as usual. Where this file and the textbook disagree, this file wins.

**Check the project first.** If it already has type tokens (a Tailwind `@theme` with `--text-*`, a `typography.css`, a design-system scale), work inside them. The defaults below are for a project with nothing yet, or for filling gaps.

**Where to go:**
- **New project or page:** §1, then copy from `references/defaults.md`.
- **Long-form article or docs column:** `references/editorial-rhythm.md` (measured spacing from 13 sites).
- **Bulgarian text:** `references/bulgarian.md`.
- **Any feature, alternate or language form you're about to rely on:** run `scripts/font-check.py` on the served file first (§3).
- **Reviewing:** run `scripts/type-lint.sh`, then go through §2 as the list of findings.

---

## 1. Defaults

These are Mike's taste, from his shipped apps. Use them unless the project says otherwise.

**Families: one sans does almost everything.**
- **Geist for all text, figures included.** Pick a neutral grotesque that stays out of the way of the data and the colour.
- **Mono only for data or code, never for prose.** In gh-dashboard Geist Mono sets only branch names. In yesterday it sets only digits in dense places (calendar squares, stats, axis labels). Don't preload it: it isn't what the first paint needs.
- **A serif only for display moments that should feel personal rather than utilitarian:** the wordmark, page titles, the big date. yesterday uses Playfair Display at weight 400 only, with a Cyrillic cut so Bulgarian titles keep the same voice. Load its italic with `preload: false` if only one page uses it.
- No font pairing beyond that. Three roles at most: sans, mono for data or code, an optional display serif.

**Scale: product sizes, not editorial sizes.**
- **Body is 15px (`0.9375rem`)**, not 17–21px. These are apps read in glances.
- **About a 1.25 ratio. Every step is a triplet** of size, line-height and tracking, defined as Tailwind v4 sub-tokens (`--text-title--letter-spacing`). gh-dashboard's steps:

  | Token | Size / line-height | Tracking |
  |---|---|---|
  | `label` | 12 / 16 | 0 |
  | `small` | 13 / 20 | 0 |
  | `body` | 15 / 24 | 0 |
  | `lead` | 17 / 26 | 0 |
  | `title` | 20 / 26 | −0.015em |
  | `heading` | 24 / 30 | −0.025em |
  | `figure` | 30 / 34 | −0.02em |
  | display (utility) | `clamp(3.25rem, 1.75rem + 5vw, 5.5rem)` / 0.95 | −0.04em, semibold, proportional figures |

- **Dense charts and calendars get steps below Tailwind's own:** `4xs` 9px, `3xs` 10px, `2xs` 11px, only for labels inside a drawing.
- **Tracking tightens as size grows** and stays 0 at body size and below. Display serif sizes use `tracking-tight` and `leading-none`.
- **Labels are quiet, not shouting.** A column label is `label` size, `--faint` colour, medium weight. No uppercase eyebrows by default. A section opens with its name set as a `title`, with no label above it.

**Numbers come in two voices, and only two** (yesterday's rule; gh-dashboard follows the same split):
- `figure`: data such as ratings, averages, deltas, axis ticks and calendar dates. Tabular, and in mono where squares and columns must line up.
- `nums`: a count inside a sentence ("12 of 30 days rated"). The text face with `lining-nums tabular-nums`.
- Big display numbers stay **proportional**. Tabular is for numbers that line up or tick over.

**Dark mode steps weight down by 50:** `--font-weight-medium: 450` and `--font-weight-semibold: 550` under the dark theme. Body stays at 400, because small text doesn't go lighter than that. Light on dark reads heavier, so never add weight.

**Base layer (copy it):** `font-synthesis: none` on `body`. `text-wrap: balance` on `h1`–`h3` and `pretty` on `p`. Links get `text-underline-offset: 0.2em` and `text-decoration-thickness: 1px`, with the hairline that draws in on hover (see mkl-motion). `::selection` inverts fg and canvas. `-webkit-font-smoothing: antialiased` on `html` is fine here: Mike likes the lighter rendering. Just don't count it as a dark-mode weight fix.

**Spacing: a 4px grid with one named token per relationship**, not per size: `hint` 4, `inline` 8, `stack` 12, `row`/`title`/`section` 16, `card`/`gutter` 20, `page` 24, `stage` 32. Inside-card padding grows from 640px. A raw number is allowed only inside a component's own drawing. Marketing pages breathe on a larger, raw rhythm on purpose. The full annotated block is in `references/defaults.md`.

**Bulgarian is a first-class locale.** Set `lang` on `<html>` from the active locale, and pick fonts that pass the Bulgarian check (§2, `references/bulgarian.md`).

---

## 2. Traps

Each of these has shipped or nearly shipped. They are invisible in code review and in Figma, and only show in the served file or the browser.

1. **Google Fonts, Fontsource and `next/font/google` strip features.** Served files keep `locl`, `tnum`, `pnum`, `frac` and `calt`. They drop `ss01`–`ss20`, `cv01`–`cv99`, `case`, `zero`, `smcp`/`c2sc`, `onum`, `sups`, `ordn` and `dlig` (checked Oct 2026 on Inter, Fira Sans, Source Serif 4, Montserrat, Literata and Geist). So `oldstyle-nums`, `all-small-caps` and `slashed-zero` silently do nothing, or worse, the browser fakes small caps. **Fix:** self-host the full font (`next/font/local`), or design without the feature. When subsetting yourself, pass `pyftsubset --layout-features='*'`.
2. **No small caps? Don't fake them, and don't leave bare capitals.** Set acronyms (BDZ, EU, NASA) as capitals at about `0.9em` with `letter-spacing: 0.05em`, and turn synthesis off (`font-synthesis: none`).
3. **Many fonts have no Bulgarian `locl`.** With `lang="bg"` they still draw Russian forms. Failing as served by Google (Oct 2026): **Geist, Literata, Roboto**. Passing: Source Serif 4 and Montserrat (via `locl`), and Sofia Sans (Bulgarian by default). Apple's system fonts on iOS are reported to draw Russian forms. Geist is the default sans here, so a Bulgarian reading surface needs the check every time: accept Russian forms in UI, or pick a font that passes for reading text.
4. **Figma never shows Bulgarian forms.** It doesn't pass the text language to its shaper. Judge Bulgarian in the browser only.
5. **Geist lacks U+2007, U+2009, U+202F and U+2011.** Figure-space padding, thin spaces and narrow no-break spaces fall back to another font, with another width. To pad a number, use an invisible `<span aria-hidden="true" class="invisible">0</span>` (or `.0`) in the same font instead.
6. **`1ch` is not one tabular digit** unless the font says so. Geist's `0` is 663 units but its tabular `0` is 600. Reserve width for a ticking number with a measured hidden span of the longest value, not `ch` arithmetic. `font-check.py` prints both widths.
7. **A display serif that defaults to old-style figures** (Playfair Display) needs `lining-nums` on `.font-serif` for dates like 26.09.2025. **Then `tabular-nums` alone cancels it:** `font-variant-numeric` is one property, so a later `tabular-nums` replaces `lining-nums` and the old-style figures come back. Always write the pair: `lining-nums tabular-nums`.
8. **Geist has default proportional digits.** Every ticking or aligned number needs `tabular-nums` set explicitly. The rolling number pattern in mkl-motion needs it too.
9. **Preload order.** `next/font` preloads every font you call by default. A mono used far down the page gets fetched ahead of the sans every line uses. Set `preload: false` on secondary families and on an italic used by one page.
10. **Load only the weights you use.** A variable font from Google with a `200 900` axis for two families, plus a third for a logo, is a heavy page. Trim the axis range in the URL or `weight` option to what the CSS uses.
11. **Motion's `initial={{ opacity: 0 }}` on a server-rendered headline hides text until hydration.** Your LCP text is blank. Animate key text with a CSS keyframe instead (mkl-motion has the `enter` utility).
12. **`next/og` (Satori) renders a variable font at its default instance** and has no Bulgarian `locl`. Pass one static file per weight, from the full font if the image needs alternates, and use a font whose default Cyrillic is Bulgarian.
13. **Safari can't hyphenate Bulgarian** (no dictionary through Safari 27.2). Set Bulgarian ragged right and never justify it. Chrome and Firefox do hyphenate it.
14. **Bulgarian one-letter words** (в, с, и, а, о, у) must not end a line. Bind them to the next word with U+00A0, using a build step (`references/bulgarian.md`).
15. **`font-variation-settings: "wght"`** overrides `font-weight` wherever it appears, so it breaks `<strong>` and every weight utility. Use `font-weight` with in-between values (450, 550).
16. **`font-feature-settings` on `body`** gets wiped by the first component that sets its own. Scope it to the element.
17. **A `vw`-only middle term in `clamp()`** stops text growing with zoom. Keep a `rem` term in it, as the display utility does.

---

## 3. Checks

All three are cheap. Run them before saying a feature works.

**What the served font really has.** Run it on the file the browser gets: `.next/static/media/*.woff2` after a build, the Fontsource file, or a `fonts.gstatic.com` URL (get it from the CSS API with a browser User-Agent).
```
pip install fonttools brotli
python3 scripts/font-check.py .next/static/media/*.woff2
```
It prints each feature (✓/✗), the variable axes, which script and language pairs carry `locl` (with a plain "Bulgarian forms: yes/NO"), the characters from §2 that are missing, and whether `1ch` matches the tabular digit width.

**Grep the project for the traps:**
```
bash scripts/type-lint.sh path/to/project
```
Each hit is a lead, not a verdict. Read the line first.

**In the browser** (Playwright works headless):
- Render "Жълтата дюля беше щастлива, че пухът, който цъфна, замръзна като гьон." with and without `lang="bg"`. If д, л, в, ж, т, ю don't change, the font has no Bulgarian forms.
- Toggle dark mode and confirm the medium and semibold steps actually change: the computed `font-weight` should be 450 or 550.
- At 200% zoom, confirm the display figure grows.
- Load with JavaScript disabled, and confirm the headline and figures are visible.

---

## 4. Reviewing

Report findings as a Before → After table, most severe first, with a file and line for every row. Confirm with `font-check.py` before flagging a feature as missing or working.

| # | Where | Before | After | Trap |
|---|---|---|---|---|
| 1 | `layout.tsx:12` | `Literata` from `next/font/google`, `lang="bg"` | Source Serif 4 (has `cyrl/BGR`), or self-hosted Literata with `locl` | 3 |
| 2 | `stats.tsx:40` | `font-serif tabular-nums` | `font-serif` + `lining-nums tabular-nums` | 7 |

Lead with the one or two differences a person can actually see. A rule-backed pass on an app that's already good mostly fixes invisible things, so say that up front.
