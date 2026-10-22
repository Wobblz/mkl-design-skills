# Fonts: loading, axes, dark mode, forced colours, generated images

## 1. Loading without invisible text or a jump

| `font-display` | Block | Swap | Use for |
|---|---|---|---|
| `swap` | 0ms | Forever | Brand and display faces that must appear |
| `optional` | ~100ms | None (skipped if late; used next visit) | Body text when layout stability matters most |
| `fallback` | ~100ms | ~3s | A middle ground |

web.dev recommends `optional` for body text when performance comes first and `swap` for brand faces. Without `font-display`, browsers hide text for up to about 3 seconds while the font loads.

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
  unicode-range: U+0301, U+0400-045F, U+0490-0491, U+04B0-04B1, U+2116;
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

The fallback metrics above match what `next/font` generates for Inter over Arial. Regenerate them for your font.

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
}
```

A Google Fonts `@import url(...)` must come before `@import "tailwindcss"`.

Tailwind also supports `--font-sans--font-feature-settings`, but its preflight applies that on `html`, which is the global `font-feature-settings` this skill warns against (`references/opentype.md` §1). Set features on the components that need them instead.

`next/font/google` downloads from the Google Fonts API, whose files drop stylistic sets, character variants, `case`, `zero`, small caps and oldstyle figures (SKILL.md §5). If the design needs them, self-host the full font with `next/font/local`.

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

## 4. Forced colours

Windows contrast themes replace the page's colours with the user's palette. `@media (forced-colors: active)` detects it (Chrome 89, Firefox 89, Safari 16). Font, size and spacing survive; colour, shadows and gradients don't, so typography has to carry the hierarchy on its own.

What's replaced (MDN):
- **`color`, `background-color` and `text-decoration-color`** become system colours. Emphasis, link state or a highlighted term shown only by colour disappears. Keep underlines on links in prose, and mark emphasis with style or weight, not colour alone.
- **`text-shadow` and `box-shadow` become `none`.** Halos on text over images and shadow-only focus rings vanish. Use `outline` for focus: `outline: 2px solid transparent` becomes visible because its colour is forced.
- **Gradient `background-image` is dropped.** Gradient text (`background-clip: text; color: transparent`) shows as plain text in the forced colour, which is the right result.
- **Text over images** gets a backplate drawn by the browser, so it stays legible.

Use the media query only for small fixes, with system colours (`CanvasText`, `LinkText`, `Highlight`, `ButtonText`). Don't build a second design. `forced-color-adjust: none` opts an element out (Chrome and Firefox; not Safari) and removes the backplate; keep it for colour swatches and logos, never for text.

```css
@media (forced-colors: active) {
  .badge   { border: 1px solid CanvasText; }   /* the background colour that marked it is gone */
  .callout { border-inline-start: 3px solid CanvasText; }
}
```

Test in Chrome DevTools: Rendering → Emulate CSS media feature `forced-colors: active`.

## 5. Text in generated images (`next/og`, Satori)

`ImageResponse` in Next.js renders with Satori, a separate layout engine with its own CSS subset. Typography that works on the page can fail in the share image. From the Satori README (Oct 2026):

- **Variable fonts render at their default instance**, usually Regular. Pass one static file per weight and style you use.
- **Pass the full font file**, not a Google-served subset, if the image needs stylistic sets, small caps or oldstyle figures (SKILL.md §5).
- **Features:** `font-variant-*` maps to the font's OpenType features, and `font-feature-settings` works. `@font-feature-values` isn't supported (so `font-variant-alternates` only does `historical-forms`), and small caps aren't synthesized.
- **`textWrap: balance` and `pretty` only apply to text with no inline elements**, and `pretty` is approximated. Keep the headline one text node, or break it by hand.
- **No Bulgarian locale.** Satori's `lang` handling covers CJK and a few other scripts, not Bulgarian, so don't count on `locl`. Use a font whose default Cyrillic is Bulgarian, or turn on its Bulgarian stylistic set with `font-feature-settings`. Check the rendered image.
- **It's a fixed frame** (typically 1200×630), so the display register and Tschichold's canon for fixed frames apply (`references/size-measure-leading.md` §6). Sizes are px, which is fine here: nobody zooms an image.

```tsx
// app/opengraph-image.tsx
const [regular, bold] = await Promise.all([
  readFile(join(process.cwd(), 'assets/SourceSerif4-Regular.otf')),
  readFile(join(process.cwd(), 'assets/SourceSerif4-Bold.otf')),
])
return new ImageResponse(<div style={{ fontFamily: 'Source Serif 4', fontFeatureSettings: '"ss01" 1' }}>{title}</div>, {
  ...size,
  fonts: [
    { name: 'Source Serif 4', data: regular, weight: 400, style: 'normal' },
    { name: 'Source Serif 4', data: bold, weight: 700, style: 'normal' },
  ],
})
```
