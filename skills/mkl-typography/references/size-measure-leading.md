# Size, measure, leading, tracking

## 1. Building a type scale

Don't prescribe sizes from memory. Pick a method, generate the scale, and give each step a name for its role.

| Method | How it works | Use for | Source |
|---|---|---|---|
| **Modular** | One ratio (1.125, 1.2, 1.25, 1.333, 1.5, 1.618) applied to one or two base sizes | Editorial and marketing pages with a clear hierarchy | Tim Brown, "More Meaningful Typography" (A List Apart, 2011) |
| **Fluid modular** | Two modular scales, a small one at a small viewport and a larger one at a large viewport, interpolated with `clamp()` | Responsive reading and marketing pages | Utopia (utopia.fyi) |
| **Stepped roles** | Hand-tuned fixed sizes, each paired with a line-height (and tracking) | Product UI | Apple HIG, Material 3, IBM Carbon, Tailwind |

**Rules:**
- **Reading and marketing:** a fluid modular scale, about 1.2 at ~360px rising to 1.25–1.333 at ~1240–1500px. Five steps up from the body and two down covers most sites.
- **Product UI:** 8–13 named roles (for example `caption`, `label`, `body-sm`, `body`, `title-sm`, `title`, `headline`, `display`). Carbon splits a "productive" set (14px base, dense) from an "expressive" set (16px base, fluid display sizes). Do the same if the product has both dashboards and marketing pages.
- **Every step is a triplet:** size, line-height and tracking. Never one global line-height.
- **Round to whole pixels at reading sizes** if text looks blurry, but not at display sizes.
- **Tim Brown called his values "educated suggestions".** Deviate when the content needs it, and write down why.

Reference stepped scales (as of Oct 2026):

| System | Body | Small | Large display |
|---|---|---|---|
| Apple iOS (default Dynamic Type) | Body 17/22pt | Footnote 13/18, Caption 12/16 | Large Title 34/41 |
| Material 3 | bodyLarge 16/24 | bodySmall 12/16 | displayLarge 57/64 |
| IBM Carbon | body-01 14/20 (productive), body-02 16/24 | label-01 12/16 | display-04, fluid up to 156px / 1.05 |
| Tailwind v4 | `text-base` 1rem / 1.5 | `text-xs` 0.75rem / 1.33 | `text-9xl` 8rem / 1 |

**Generators** (checked Oct 2026 unless noted):
- **Utopia** (utopia.fyi/type/calculator): fluid type and space scales, output as `--step-n` custom properties. The most complete method.
- **fluid.style/type** (Maxwell Barvian): fluid type with a zoom-safety check against WCAG 1.4.4.
- typescale.com, modularscale.com and fluid-type-scale.com: popular, not re-checked for this skill.

### Fluid type, the formula

Utopia's interpolation, for a step that is `MinSize` at `MinWidth` and `MaxSize` at `MaxWidth` (all in rem, with 1rem = 16px for the widths):

```
slope        = (MaxSize − MinSize) / (MaxWidth − MinWidth)
intercept    = MinSize − slope × MinWidth
font-size    = clamp(MinSize rem, intercept rem + (slope × 100) vw, MaxSize rem)
```

Example: 1rem at 320px to 2rem at 1440px gives `clamp(1rem, 0.7143rem + 1.4286vw, 2rem)`. Regenerate values with the tool rather than copying examples.

```css
:root {
  --step--1: clamp(0.9375rem, 0.9119rem + 0.1136vw, 1rem);
  --step-0:  clamp(1.125rem, 1.0739rem + 0.2273vw, 1.25rem);
  --step-1:  clamp(1.35rem, 1.2631rem + 0.3864vw, 1.5625rem);
  --step-4:  clamp(2.3328rem, 2.0387rem + 1.3072vw, 3.0518rem);
}
```

### Fluid type and zoom

Browser zoom scales `rem` and `px` but not `vw`. A step that grows mostly with `vw` can't reach 200% when zoomed, which fails WCAG 1.4.4.

- **Always include a `rem` term** in the preferred value. `clamp(1.5rem, 5vw, 3rem)` is a guaranteed failure (WCAG failure F94).
- **Keep each step's maximum at or below 2.5× its minimum** (Barvian, Smashing Magazine, Nov 2023).
- **Never cap text below 2× its base size** (Adrian Roselli, updated Oct 2025). He notes no fluid method is guaranteed safe, so test at 200% zoom.

### Fluid type inside components

Viewport steps suit page-level type: the article body, page headlines. A component that sits in a sidebar on one page and the main column on another needs type that follows its own width. Container query units (`cqi`; Chrome 105, Firefox 110, Safari 16) do that.

- **Declare the container on the layout region** (`main`, `.sidebar`, `.card-grid`), not on the text. An element can't size against itself; `cqi` resolves against the nearest ancestor container.
- **Without a container, `cqi` falls back to small-viewport units**, so one token still works at page level.
- **`container-type: inline-size` ignores the element's content** when computing its width. A container inside a flex row or a shrink-to-fit box can collapse to zero; give it a width or let it stretch.
- **Same zoom rules as `vw`:** keep a `rem` term and the 2.5× ratio. Use the Utopia formula with container widths in place of viewport widths and `cqi` in place of `vw`.
- **Use it for display and card titles, not body text.** Reading text should be one size across the page wherever it sits.

```css
main, .sidebar, .card-grid { container-type: inline-size; }
.card__title { font-size: clamp(1.125rem, 0.9rem + 2.5cqi, 1.75rem); }
```

### The OS text size (`<meta name="text-scale">`)

Mobile browsers ignore the system text-size setting by default and resize text with their own heuristics. `<meta name="text-scale" content="scale">` opts in: the root `medium` size follows the OS setting, so everything in `rem` scales with it. Chromium 146+ only and still experimental; Firefox and Safari ignore the tag (Oct 2026). It is law 12 carried through to the OS.

- **Add it only when the page is `rem` throughout:** no px root size, no px font sizes, and breakpoints in `rem` (`@media (width > 35rem)`), so layouts drop to one column as text grows.
- **Test at the platform's maximum scale**, which runs from 200% to over 300% on mobile.
- **It turns off the browser's mobile text auto-sizing**, so text that relied on it must be sized properly.
- **Don't also use `env(preferred-text-scale)`.** Using both applies the scale twice (MDN).

```html
<meta name="text-scale" content="scale">
```

### Tailwind v4

Define the scale as `--text-*` tokens with paired sub-tokens:

```css
@theme {
  --text-body: 1.0625rem;
  --text-body--line-height: 1.55;
  --text-display: 3rem;
  --text-display--line-height: 1.05;
  --text-display--letter-spacing: -0.02em;
}
```

## 2. Measure (line length)

- **Bringhurst:** "The 66-character line (counting both letters and spaces) is widely regarded as ideal." Anything from 45 to 75 characters is satisfactory for single-column text set in a serif at text size. For multi-column work, 40–50 characters.
- **Butterick:** 45–90 characters, or 2–3 lowercase alphabets per line as a quick test.
- **Rutter:** `33em` gives about 66 characters, because an average character is about 0.5em wide. It scales with text zoom.
- **WCAG 1.4.8 (AAA):** no more than 80 characters.
- **What editorial sites do (measured Oct 2026):** 74–90 characters on desktop. The print-led ones (Guardian, New Yorker, Butterick) sit at 74–75; tech and research sites run 83–90 with leading of 1.5–1.7 (`references/rhythm.md` §1). Past 75, raise the leading; past 90, narrow the column.

The `ch` trap: `1ch` is the advance width of the "0" glyph, not an average character. In most proportional fonts "0" is wider than the average letter, so `66ch` sets more than 66 characters. Start with `max-inline-size: 33em`, or 60–65ch, then count real characters on a real paragraph.

```css
.prose { max-inline-size: 33em; margin-inline: auto; }   /* inline-size works in vertical writing too */
.prose :is(h1, h2) { max-inline-size: 24ch; }            /* measured in the heading's own size: ~20–25 characters */
```

- **Phones:** 40–55 characters at 16–18px. Don't shrink the text to fit more.
- **CJK:** use the `ic` unit (the width of 水). `max-inline-size: 35ic` is a starting point, not a sourced ideal.
- **Languages with long words** (German, Finnish, Bulgarian and other Cyrillic text) need working hyphenation more than a wider measure (`references/line-breaking.md`).

## 3. Leading (line-height)

- **Unitless, always.** `line-height: 1.5`, not `24px` or `1.5em`, so children inherit the ratio, not a fixed length.
- **Butterick:** 120–145% of the size. Published systems run higher at reading sizes.
- **Leading falls as size rises.** Published systems converge on about 1.5 at 16px, 1.25 at 32px and 1.1 at 60px and above (Material 3 57/64 = 1.12, Carbon display 1.05–1.11, Tailwind 1.0 from 48px).
- **Leading rises with measure.** A long line needs more leading so the eye finds the next line. The measured editorial sites with 80+ character lines use 1.43–1.7.
- **Large x-height faces need more leading** (Butterick).
- **Cyrillic and accented text** with tall diacritics or descenders (й, ё, Ё) needs a little more leading than English in the same font, especially in display sizes at 1.0–1.1. Test with real strings.

Starting values:

| Role | Line-height |
|---|---|
| Long-form body | 1.5–1.6 |
| UI body | 1.4–1.45 |
| Compact UI, tables | 1.25–1.3 |
| h3–h4 | 1.2 |
| h1–h2 | 1.1–1.15 |
| Display ≥ 48px | 1.0–1.05 |
| Captions, notes | 1.35–1.45 |

## 4. Tracking (letter-spacing)

- **Write it in `em`**, so it scales with the size.
- **Body lowercase: 0.** Bringhurst: "Don't letterspace the lower case without a reason."
- **Capitals and small caps: +5–10% of the size** (Bringhurst 2.1.6), so `letter-spacing: 0.05–0.1em`. More for small sizes, less for large.
- **Small UI text (11–13px): slightly positive**, about +0.01–0.02em.
- **Display: slightly negative**, about −0.01 to −0.03em, tuned by eye per font.
- **Fonts with a published tracking curve:** use it. Inter 3's formula is `tracking = −0.0223 + 0.185 × e^(−0.1745 × size)` in em (archived at d.rsms.me/inter-website/v3/dynmetrics/), giving about +0.005em at 11px, −0.011em at 16px and −0.022em at 48px. It predates Inter 4's `opsz` axis, which now does part of this work. Apple's system fonts track automatically at every size. Fonts with an `opsz` axis adjust spacing per size themselves, so they need less manual tracking.
- **Letter-spacing disables optional ligatures** (`liga`, `clig`). That's usually right for tracked caps. If a tracked line needs ligatures, turn them back on with `font-feature-settings`.
- **Never letterspace Arabic** or other connected scripts.

```css
.eyebrow     { text-transform: uppercase; letter-spacing: 0.08em; font-size: var(--step--1); }
abbr         { font-variant-caps: all-small-caps; letter-spacing: 0.05em; }
.display     { letter-spacing: -0.025em; }
:lang(ar)    { letter-spacing: 0; }
```

## 5. Kerning

- **`font-kerning: normal`**, not `auto`: some browsers turn kerning off at small sizes under `auto`.
- **`text-rendering: optimizeLegibility`** is non-standard. Use it on headlines only. MDN warns against it for long text because of the performance cost. `geometricPrecision` is for SVG.
- **Hand-kern only fixed display copy** (a logo-like headline, a hero), with spans around the pair. Manual kerning breaks when the text comes from a CMS, gets translated or falls back to another font.

## 6. Tschichold's page canon

The Van de Graaf construction that Tschichold popularised sets margins at 1/9 and 2/9 of the page. On a 2:3 page, inner : top : outer : bottom = 2 : 3 : 4 : 6, and the text block has the page's proportions.

Scrolling web pages have no bottom margin to balance, so apply the canon only to **fixed frames:** `@page` print stylesheets, slides, posters, hero frames and paged readers.

For scrolling layouts, keep two ideas from it:
- **Put more space on the trailing side than the binding side.** For a left-aligned reading column: `grid-template-columns: 1fr minmax(0, 33em) 2fr`.
- **Leave more space after a block than before it**, as the canon leaves more at the bottom than the top.

```css
/* a true 2:3 page (140 × 210mm): inner = width/9, top = height/9, outer = 2·width/9, bottom = 2·height/9 → 2:3:4:6.
   On A-series pages (1:1.414) the same ninths give the canon's construction but not the 2:3:4:6 ratio. */
@page        { size: 140mm 210mm; }
@page :right { margin: calc(210mm / 9) calc(140mm * 2 / 9) calc(210mm * 2 / 9) calc(140mm / 9); }
@page :left  { margin: calc(210mm / 9) calc(140mm / 9) calc(210mm * 2 / 9) calc(140mm * 2 / 9); }
```
