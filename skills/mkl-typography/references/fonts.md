# Fonts: loading, axes, dark mode

## 1. Loading without invisible text or a jump

| `font-display` | Block | Swap | Use for |
|---|---|---|---|
| `swap` | 0ms | Forever | Brand and display faces that must appear |
| `optional` | ~100ms | None (skipped if late; used next visit) | Body text when layout stability matters most |
| `fallback` | ~100ms | ~3s | A middle ground |

web.dev recommends `optional` for body text when performance comes first and `swap` for brand faces. Without `font-display`, Chromium and Firefox hide text for up to 3 seconds, and Safari can hide it indefinitely.

**Rules:**
- **WOFF2 only.** Self-host or use a build tool that does (`next/font`, Fontsource). Self-hosting is not automatically faster, but it removes a connection and keeps fonts under your cache rules.
- **Ship only what you use:** the weights and styles in the tokens, and the subsets the content needs. A variable font replaces several static weights, but check the file size against two or three statics.
- **Split by script with `unicode-range`**, for example Latin and Cyrillic in separate files. The browser only downloads a subset when the page uses its characters.
- **Preload one or two faces** used above the fold. Preload ignores `unicode-range`, so preload the exact subset file. Fonts are CORS requests: `<link rel="preload" as="font" type="font/woff2" crossorigin>`.
- **Metric-matched fallback:** a second `@font-face` that wraps a local system font and adjusts its metrics, so the swap doesn't move text.
  - `size-adjust` works in Chrome, Firefox and Safari 17+.
  - `ascent-override`, `descent-override` and `line-gap-override` work in Chrome 87+ and Firefox 89+, **not in any stable Safari** (through 27.2, Oct 2026).
  - Set an explicit unitless `line-height` on text so the line box doesn't depend on the font's ascent and descent. That should remove most vertical shift in Safari too (reasoned, not yet measured).
  - Generate the values with Capsize or fontaine, or let `next/font` do it.
- **`font-size-adjust: from-font`** (Baseline 2024) keeps the x-height constant when a fallback renders, so text doesn't visibly shrink or grow.

```css
@font-face {
  font-family: "Inter";
  src: url(/fonts/inter-latin.woff2) format("woff2");
  font-weight: 100 900;
  font-display: optional;
  unicode-range: U+0000-00FF, U+0131, U+0152-0153, U+02C6, U+02DA, U+02DC, U+2000-206F, U+20AC, U+2122, U+2212;
}
@font-face {
  font-family: "Inter";
  src: url(/fonts/inter-cyrillic.woff2) format("woff2");
  font-weight: 100 900;
  font-display: optional;
  unicode-range: U+0400-045F, U+0490-0491, U+04B0-04B1, U+2116;
}
@font-face {
  font-family: "Inter Fallback";
  src: local("Arial");
  size-adjust: 107.4%;
  ascent-override: 90.2%;
  descent-override: 22.48%;
  line-gap-override: 0%;
}
body { font-family: "Inter", "Inter Fallback", system-ui, sans-serif; line-height: 1.5; }
```

The fallback metrics above are Chrome's published example for Inter over Arial. Regenerate them for your font.

Check subset files keep the features you need (`locl`, `tnum`, stylistic sets): SKILL.md §5.

### Next.js (`next/font`, docs as of Sep 2026)

- Self-hosts Google fonts at build time; the browser makes no requests to Google.
- Defaults: `display: 'swap'`, `preload: true`, `adjustFontFallback: true` for Google fonts (`'Arial'` for local fonts; `'Times New Roman'` or `false` also allowed).
- Only the weight axis ships unless you list others: `axes: ['opsz', 'wdth', 'GRAD']`.
- List `subsets` (for example `['latin', 'cyrillic']`). Preloading with no subsets gives a warning.
- Define each font once in a shared module; every loader call creates a separate instance.
- Preloading follows where you call the font (page, layout or root layout).

```ts
// app/fonts.ts
import { Inter, Source_Serif_4 } from 'next/font/google'
export const sans  = Inter({ subsets: ['latin', 'cyrillic'], variable: '--font-inter', axes: ['opsz'] })
export const serif = Source_Serif_4({ subsets: ['latin', 'cyrillic'], variable: '--font-source-serif', display: 'optional' })
```

### Tailwind v4

Fonts are `--font-*` theme tokens. Point them at the `next/font` variables with `@theme inline`, and put per-family feature defaults in sub-tokens:

```css
@import "tailwindcss";
@theme inline {
  --font-sans: var(--font-inter);
  --font-serif: var(--font-source-serif);
  --font-sans--font-feature-settings: "cv11" 1;
}
```

A Google Fonts `@import url(...)` must come before `@import "tailwindcss"`.

## 2. Variable axes

Use the registered axes through their high-level properties. `font-variation-settings` overrides those properties wherever it appears in the cascade, so `"wght" 600` there breaks `<strong>` and every weight utility.

| Axis | Property | Use |
|---|---|---|
| `wght` | `font-weight` | Weight, including in-between values (350, 450) |
| `wdth` | `font-stretch` (`87.5%`, `condensed`) | Condensed for dense UI and narrow columns; extended for display. `font-width` is the newer name, not in Chrome yet (Oct 2026) |
| `slnt`, `ital` | `font-style: oblique 10deg` / `italic` | Slant and italic |
| `opsz` | `font-optical-sizing: auto` (the default) | The font adapts its design to the size: sturdier and looser at small sizes, finer and tighter at large ones |
| `GRAD`, `XTRA`, custom | `font-variation-settings` | Grade changes apparent weight without changing width |

- **Keep `font-optical-sizing: auto`.** Only override it to force a display cut at a small size for effect.
- **Declare the weight range in `@font-face`** (`font-weight: 100 900`) or the browser won't use in-between weights.
- **Compose custom axes** through one custom property each, re-declared on the elements that change them (same pattern as feature settings in `references/opentype.md`).
- **Axis tags are case-sensitive.** Registered axes are lowercase, custom axes uppercase.
- **Check the actual axis ranges** in the font (Wakamai Fondue) before using values; ranges differ between fonts and versions.

```css
:root { --grad: 0; }
:root, .hover-grade { font-variation-settings: "GRAD" var(--grad); }
.hover-grade:hover  { --grad: 50; }       /* heavier on hover without reflow */
.table-dense        { font-stretch: 87.5%; }
```

## 3. Dark mode

Light text on a dark background looks heavier than the same weight on light (the irradiation illusion). Compensate by **reducing** perceived weight:

- **Fonts with a `GRAD` axis:** lower the grade a little (for example −25). Width doesn't change, so nothing reflows.
- **Other variable fonts:** lower `font-weight` by 50–100 (500 → 400, 400 → 350).
- **Static fonts:** leave them. A 350 weight in a static family snaps to the nearest file, usually 400 or 300.
- **Don't go thin.** Light weights at small sizes break up on dark backgrounds; keep small text at 400 or more.

Some agent skills advise *adding* weight in dark mode; the sources found point the other way. Extra tracking or leading for dark mode has no primary source; don't add it by default.

`-webkit-font-smoothing: antialiased` is non-standard and macOS-only. It makes light-on-dark text look lighter, which some designers like, but it isn't a cross-platform fix and does nothing on Windows or Linux.

```css
@media (prefers-color-scheme: dark) {
  :root        { --grad: -25; }                /* fonts with GRAD */
  .var-no-grad { font-weight: 350; }           /* variable fonts without GRAD */
}
```

If the site has a theme toggle, apply the same rules under the toggle's selector (for example `[data-theme="dark"]`) as well as the media query.
