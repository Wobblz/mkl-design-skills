---
name: mkl-typography
description: Web typography for laying out text. Use when setting or reviewing type on a page or in product UI, including type scales, line length, line-height, vertical rhythm, tracking, OpenType features, tabular figures, hyphenation, line breaks, hanging punctuation, optical alignment, drop caps, font loading, or text in Bulgarian and other languages.
---

# Typography

Typography here means setting text, not drawing fonts. Printers have solved most layout problems over five centuries: how long a line should be, how much space a heading needs, when to hyphenate, how to make a quote mark hang. Bringhurst's *The Elements of Typographic Style* is the canon. Tschichold's *The Form of the Book* covers page proportions. Butterick and Rutter carried both onto the screen. This skill keeps only the rules that turn into CSS today, with the browser support that decides whether you need a fallback.

**Check the project first.** If it already has type tokens (a Tailwind `@theme` with `--text-*`, a `typography.css`, a prose component, a design-system scale), work inside them and map these rules onto their names. Only introduce new tokens when nothing exists.

**Check the font second.** CSS can ask for small caps, oldstyle figures, a stylistic set or Bulgarian forms, but only the font decides whether they exist. Inspect it before recommending a feature (§5).

**Where to go:**
- **Setting up type for a new project or page:** §1 laws → §2 register → §4 workflow → `references/size-measure-leading.md` → `references/rhythm.md`.
- **Long-form article, docs or research page:** `references/rhythm.md`, then `references/line-breaking.md` and `references/optical.md`.
- **Product UI, tables and numbers:** `references/ui-and-tables.md`, then `references/opentype.md`.
- **Non-English text, Bulgarian, quotes and dashes:** `references/language.md`.
- **Fonts flashing, shifting or looking wrong in dark mode:** `references/fonts.md`.
- **Reviewing existing typography:** §7 checklist, with §6 as the list of findings to look for.
- **Where a rule came from:** `references/sources.md`.

---

## 1. The laws

1. **Typography serves the text.** Bringhurst's first principle. Every choice should make the words easier to read or easier to find. Decoration that costs reading is wrong in body text, whatever it does for a hero.
2. **Measure, leading and size are one decision.** A longer line needs more leading, a larger size needs less, and a smaller size needs a shorter line. Change one and re-check the other two. Long-form body text sits around 60–75 characters at line-height 1.5–1.6 (`references/size-measure-leading.md`).
3. **Space shows structure.** Space above a heading is about twice the space below it, so the heading belongs to what follows. Paragraphs are separated by space *or* an indent, never both. Blocks that interrupt the text (figures, quotes, code) get more space than paragraphs (`references/rhythm.md`).
4. **Rhythm comes from the line, not a grid.** Spacing is a multiple of the body line-height (`rlh`, once the root size and line-height match the body text), so the page has a pulse. A locked baseline grid fights mixed sizes, images and zoom on the web, so don't build one for scrolling pages.
5. **Tracking follows size and case.** Body lowercase gets zero. Capitals and small caps get +5–10%. Large display type gets slightly negative tracking. Never letterspace lowercase body text to fill a line.
6. **Real glyphs, not fakes.** Use the font's own small caps, figures, fractions and ligatures, not browser imitations. Turn off faux small caps (`font-synthesis-small-caps: none`) and use proper characters: “curly quotes”, the ellipsis …, en and em dashes, the minus −, the multiplication sign × (`references/language.md`).
7. **Numbers that change or line up are tabular.** Tables, timers, prices, counters and chart axes use `font-variant-numeric: tabular-nums lining-nums`. Running prose uses proportional figures (`references/ui-and-tables.md`).
8. **`lang` is a typesetting setting.** It picks localized glyphs (Bulgarian forms), the hyphenation dictionary, the quote marks and the casing rules. Set it on `<html>` and on every passage in another language.
9. **Edges are optical, not mathematical.** A heading that starts with T, O or “ looks indented next to body text, even when its box is aligned. Hang punctuation, hang list markers and pull large round or diagonal capitals into the margin (`references/optical.md`).
10. **Break lines like a compositor.** Balance headings, avoid one-word last lines, hyphenate prose but never headings or UI, keep numbers with their units, and only justify when hyphenation works for that language (`references/line-breaking.md`).
11. **Text never waits and never jumps.** Fonts load without invisible text and without a visible reflow when they swap (`references/fonts.md`).
12. **The reader's settings win.** Size in `rem`, never cap fluid type below 2× its base, keep text containers free of fixed heights, and survive WCAG's text-spacing override (§3).
13. **Use high-level properties and named values.** Use `font-variant-*` before `font-feature-settings`, `font-weight` before `font-variation-settings`, and tokens before raw numbers. Low-level settings replace each other instead of combining, which silently drops features.

---

## 2. Pick the register

Decide which register a block of text belongs to before setting it. The budgets differ, and most mistakes come from applying one register's rules to another.

| | **Reading** (articles, docs, research, long product copy) | **UI** (product chrome, forms, tables, dashboards) | **Display** (headlines, heroes, covers, pull quotes) |
|---|---|---|---|
| Size | Body 17–21px at desktop, never below 16px | 13–16px roles; 12px only for metadata | Fluid; set by layout |
| Measure | 60–75 characters (`max-inline-size: 33em` is a good start) | Set by the component; truncate with care | 8–25 characters per line is typical |
| Line-height | 1.5–1.6 | 1.4–1.45; tables and compact UI 1.25–1.3 | 1.0–1.15 |
| Tracking | 0 | 0, small labels +0.01–0.02em, caps labels +0.06–0.1em | −0.01 to −0.03em, tuned by eye |
| Figures | Proportional (oldstyle in serif text if the font has them) | Tabular lining | Lining, proportional |
| Wrapping | `text-wrap: pretty`, hyphenation on | No hyphenation; `nowrap` or truncation decided per field | `text-wrap: balance`, no hyphenation |
| Rhythm | Full flow system (`references/rhythm.md`) | `gap` and the spacing scale; `text-box-trim` on components | Space around the block; optical edge alignment |
| Allowed extras | Drop caps, small-caps lead-ins, sidenotes, hanging punctuation | Stylistic sets for clarity (disambiguated 1/l/I, slashed zero) | Discretionary ligatures, swashes, alternates, manual kerning |

A docs site is reading register in the article column and UI register in the sidebar and table of contents. A dashboard is UI register, except an onboarding or empty-state headline, which is display.

---

## 3. Platform baseline (Oct 2026)

Support checked against @mdn/browser-compat-data 8.1.7 and web-features 3.43.0 on 2026-10-22 (Chrome 156, Firefox 158, Safari 27). Re-check anything marked partial before relying on it.

**Use freely (Baseline):** `rem`/`em`/`ch`/`ic`, `lh`/`rlh` units (Widely available May 2026), `cap` unit (Widely June 2026), `clamp()`, `font-variant-ligatures`, `-numeric`, `-caps` and `-alternates` with `@font-feature-values` (`font-variant-position` is not Baseline), `font-synthesis-small-caps`, `font-kerning`, `font-size-adjust` (2024), `hyphens` and `hyphenate-character` (Widely March 2026), `text-wrap: balance` (2024), `text-wrap: stable`, `text-align-last`, `overflow-wrap: anywhere`, `@counter-style`, `text-underline-offset`, `text-decoration-thickness`, `text-decoration-skip-ink`, `::first-letter`, `::first-line`.

**Use with a fallback:**

| Feature | Works in | Missing in | Fallback |
|---|---|---|---|
| `text-box-trim` / `text-box-edge` | Chrome 133, Safari 18.2, Firefox 154 | Inline elements in Chrome | Normal half-leading; harmless |
| `text-wrap: pretty` | Chrome 117 (last 4 lines only), Safari 26 (whole paragraph) | Firefox | Build-time no-break space before the last word |
| `initial-letter` | Chrome 110; Safari as `-webkit-initial-letter` (integers only on iOS) | Firefox | `::first-letter` float |
| `hanging-punctuation` | Safari (full since 26.5) | Chrome, Firefox | Negative `text-indent` on a class |
| `hyphenate-limit-chars` | Chrome 109, Firefox 137 | Safari | Ignored safely |
| `text-justify` | Chrome 145, Firefox | Safari | Don't depend on it |
| `ascent-override` and friends | Chrome 87, Firefox 89 | Safari (through 27.2) | `size-adjust` (Safari 17+) plus unitless `line-height` |
| `::marker` styling | Full in Chrome, Firefox | Safari: `color` and `font-size` only | `::before` counters |
| Hyphenation dictionaries | Vary by language and engine | e.g. Bulgarian in Safari, Polish in Chrome | Build-time soft hyphens, or ragged right |

**Don't use:** `hyphenate-limit-lines`, `-zone`, `-last` (no stable browser), `text-align: "."` decimal alignment (no browser), `block-step` (mostly unsupported), `font-variation-settings` for weight, width or slant, a global `font-feature-settings: "kern", "liga", "calt"` on `body` (redundant, and it blocks later features), `text-rendering: optimizeLegibility` on long text (performance), `-webkit-font-smoothing` as a dark-mode fix.

**Accessibility floor (WCAG 2.2):**
- Size type in `rem`. Don't set `html { font-size }` in px; leave it alone or use `%`.
- A fluid size's maximum must be no more than 2.5× its minimum, and never cap text below 2× its base, or 200% zoom fails (SC 1.4.4). Every `clamp()` includes a `rem` term.
- Text must survive line-height 1.5, paragraph spacing 2em, letter-spacing 0.12em and word-spacing 0.16em with nothing clipped (SC 1.4.12). No fixed heights on text containers, and no ellipsis without a way to read the full text.
- WCAG has no minimum font size. Keep body text at 16px or above and small text at weight 400 or more.
- Avoid long passages in all caps or italics. Justified text is an AAA failure (SC 1.4.8); set ragged right unless you have a reason.
- WCAG 3 is still a working draft (Sep 2026) with no contrast method chosen. Don't cite APCA for conformance.

---

## 4. Workflow

### 4a. Setting type for a project

1. **Inventory.** Read the existing tokens, global CSS, prose component and font loading. List the families, weights and features actually loaded, from the served file, not the font's specimen page.
2. **Inspect the font.** Open the font in Wakamai Fondue (wakamaifondue.com) or run `ttx -t GSUB font.woff2`, and note which features and axes exist: `smcp`, `c2sc`, `onum`, `tnum`, `frac`, `case`, `ss01`–`ss20`, `cv01`–`cv99`, `locl` languages, `opsz`, `GRAD`, `wdth`.
3. **Set `lang`** on `<html>`, and on every element in another language.
4. **Pick the register** for each surface (§2).
5. **Build the scale.** Choose a method: fluid modular for reading and marketing pages, stepped named roles for UI. Each step is a triplet of size, line-height and tracking (`references/size-measure-leading.md`).
6. **Set the measure** on the reading column, and re-check leading against it.
7. **Set the rhythm** with a flow system based on `rlh` (`references/rhythm.md`).
8. **Turn on features per role:** figures, small caps, ligatures, stylistic sets (`references/opentype.md`, `references/ui-and-tables.md`).
9. **Line breaking:** `balance` on headings, `pretty` and hyphenation on prose, and a build step for no-break spaces and hanging quotes (`references/line-breaking.md`, `references/optical.md`).
10. **Load fonts** without blocking or shifting (`references/fonts.md`).
11. **Verify:**
    - Long and short headings, one-word headings, the longest translated string.
    - 200% zoom and a 320px-wide viewport.
    - The WCAG text-spacing bookmarklet (SC 1.4.12).
    - Safari, Chrome and Firefox: the fallbacks in §3 really engage.
    - Slow 3G with the cache disabled: no invisible text, no visible jump.
    - Dark mode.
    - Real content in every language the product ships, including Bulgarian if it applies.

### 4b. Writing a rule

When a rule goes into the project's CSS, write the reason in one comment line, so a later edit doesn't undo it:

```css
/* Bringhurst 2.1.6: caps need 5–10% tracking */
.eyebrow { text-transform: uppercase; letter-spacing: 0.08em; }
```

### 4c. Reviewing

Run §7 and report findings as a Before → After table, one row per problem, most severe first. Give a file and line or a selector and computed value for every row; "looks off" is not a finding. Confirm the font ships a feature before flagging that it's missing.

| # | Where | Before | After | Law |
|---|---|---|---|---|
| 1 | `table.tsx:31` | Proportional figures in the price column | `font-variant-numeric: tabular-nums lining-nums`; right-aligned | 7 |
| 2 | `prose.css:12` | `p { margin: 1em 0; text-indent: 1.5em }` | Space only: `* + p { margin-block-start: 0.75rlh }` | 3 |
| 3 | `globals.css:4` | `html { font-size: 16px }` | Removed; sizes in `rem` | 12 |

---

## 5. Inspecting a font

Do this before promising any feature, alternate or language form.

- **Features:** Wakamai Fondue lists every OpenType feature, with a live preview and generated CSS. FontDrop and FontGauntlet do the same in other ways. Command line: `ttx -t GSUB -t GPOS font.woff2`, or `fonttools` in Python.
- **Language forms:** Look for `locl` under script `cyrl` and language `BGR` (Bulgarian), `SRB` (Serbian), `MKD` (Macedonian). Then render a test string with `lang="bg"` in the browser. Design tools may not apply `locl`: Figma does not pass the text language to its shaper, so mock-ups show Russian forms where the browser shows Bulgarian.
- **Served fonts lose features.** Files served by the Google Fonts API (and Fontsource, and very likely `next/font/google`, which uses the same API) keep `locl`, `tnum`, `pnum`, `frac` and `calt`, but drop stylistic sets, character variants, `case`, `zero`, small caps, oldstyle figures, `sups`, `ordn` and `dlig` (checked Oct 2026 on Inter, Fira Sans, Source Serif 4, Montserrat). For those features, self-host the full font file (`next/font/local`). When subsetting yourself with `pyftsubset`, pass `--layout-features='*'`.
- **Axes:** Note each variable axis and its range. Registered axes (`wght`, `wdth`, `slnt`, `ital`, `opsz`) map to `font-weight`, `font-stretch`, `font-style` and `font-optical-sizing`. Custom axes (`GRAD`, `XTRA`) need `font-variation-settings`.

---

## 6. Anti-patterns

- **Space and indent together** on paragraphs. Pick one.
- **Equal space above and below a heading**, or more below than above. The heading floats between sections.
- **One global line-height** for every size. Headlines at 1.5 fall apart; body at 1.1 is unreadable.
- **`66ch` as "66 characters".** `ch` is the width of "0", which is wider than an average letter, so `66ch` sets more than 66 characters.
- **Letterspaced lowercase**, or tracked text that silently lost its ligatures (any non-zero `letter-spacing` disables optional ligatures).
- **All caps without tracking**, or typed capitals in the HTML instead of `text-transform`.
- **Faux small caps** and faux bold or italic from missing font files.
- **Proportional figures in a table or a timer**, so numbers jitter or columns don't line up.
- **`font-feature-settings` on `body`** that a component's own `font-feature-settings` later wipes out.
- **`font-variation-settings: "wght" 600`**, which breaks `<strong>` and every weight utility.
- **Hyphenated headings, buttons or labels**, or `hyphens: auto` without `lang`.
- **Justified text without working hyphenation**, which opens rivers, especially in Safari on languages it can't hyphenate.
- **`text-wrap: balance` on paragraphs.** It only works on short blocks and leaves ragged gaps on the right.
- **Straight quotes, `--` for dashes, three dots for an ellipsis**, `x` for ×, a hyphen for a minus sign.
- **Assuming `widows`/`orphans` fix screen paragraphs.** They only apply to print, columns and pages.
- **`hanging-punctuation` as the whole solution.** It only works in Safari, and it never moves list markers.
- **Fluid type with a `vw`-only term**, or a max more than 2.5× the min.
- **Fixed-height text containers** that clip at 200% zoom or under the text-spacing override.
- **Adding weight for dark mode.** Light text on dark looks heavier; reduce weight or grade instead.
- **A baseline grid snapped with JavaScript** on a scrolling page.

---

## 7. Review checklist

Score 1 point per item for each text surface. A reading surface under 9/10 gets fixed.

1. **Register:** the surface has one, and its budgets from §2 are met.
2. **Scale:** every size comes from a named step, with paired line-height and tracking.
3. **Measure:** reading columns are 60–75 characters, checked with real text, not `ch` arithmetic.
4. **Rhythm:** spacing comes from a flow system in `rlh`; headings sit closer to what follows than to what precedes.
5. **Paragraphs:** space or indent, never both; first paragraph after a heading is not indented.
6. **Figures:** tabular lining figures wherever numbers change or line up; proportional in prose.
7. **Glyphs:** real quotes, dashes, ellipsis, minus and ×; no faux small caps or faux bold.
8. **Language:** `lang` is set everywhere it should be; localized forms and hyphenation appear in the browser.
9. **Breaks:** headings balanced, prose `pretty`, no hyphenated headings, numbers kept with units, no one-word last line in prose.
10. **Edges and access:** quotes and markers hang where there's room; text survives 200% zoom, the text-spacing override and font swap.

Then check the whole project:
- Fonts load with no invisible text and no visible reflow; only used weights and subsets ship.
- No `font-feature-settings` or `font-variation-settings` where a high-level property exists.
- Firefox gets the fallbacks for `pretty`, `initial-letter` and hanging punctuation. Safari gets them for hyphenation dictionaries and metric overrides.
- Dark mode reduces weight or grade, or leaves static fonts alone.

---

## 8. What lives where

| File | Covers |
|---|---|
| `references/size-measure-leading.md` | Type-scale methods and generators, fluid type and zoom, measure, line-height, tracking, kerning, Tschichold's page canon |
| `references/rhythm.md` | Vertical rhythm: measured editorial spacing, element-by-element spacing, the flow CSS, sidenotes and wide figures |
| `references/opentype.md` | Ligatures, figures, fractions, small caps, stylistic sets and character variants, `@font-feature-values`, composing feature settings |
| `references/ui-and-tables.md` | UI text roles, labels and caps, tables, numeric alignment, buttons and badges, truncation |
| `references/language.md` | `lang`, `locl`, Bulgarian forms, quotes, dashes and other characters, number and date conventions, hyphenation dictionaries |
| `references/line-breaking.md` | Hyphenation, justification, `text-wrap`, runts, widows, no-break spaces, long strings |
| `references/optical.md` | Hanging punctuation, hanging lists, optical margin alignment, drop caps, `text-box-trim`, `cap` units, icons in text |
| `references/fonts.md` | Font loading and CLS, metric-matched fallbacks, `next/font` and Tailwind v4, variable axes, dark-mode compensation |
| `references/sources.md` | Books, specs, practitioners, tools, neighbouring agent skills, and provenance |
