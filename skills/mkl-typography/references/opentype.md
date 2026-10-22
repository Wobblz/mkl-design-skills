# OpenType features

A font carries more than its default glyphs: ligatures, several sets of figures, fractions, real small caps, alternate letters, language forms. CSS switches them on, but only if the font has them. Inspect the font first (SKILL.md §5).

## 1. High-level properties first

Use the `font-variant-*` longhands. They cascade and combine: setting `font-variant-numeric` on a table cell doesn't touch the ligature setting it inherited.

`font-feature-settings` is all-or-nothing per declaration. A child's `font-feature-settings: "tnum"` silently drops an inherited `"ss01"`. Low-level settings also win over the high-level properties when they conflict.

| Want | High-level property | Low-level tag |
|---|---|---|
| Standard / contextual ligatures | `font-variant-ligatures: common-ligatures contextual` (default on) | `liga`, `clig`, `calt` |
| Discretionary ligatures | `font-variant-ligatures: discretionary-ligatures` | `dlig` |
| No ligatures | `font-variant-ligatures: none` | |
| Tabular / proportional figures | `font-variant-numeric: tabular-nums` / `proportional-nums` | `tnum` / `pnum` |
| Lining / oldstyle figures | `font-variant-numeric: lining-nums` / `oldstyle-nums` | `lnum` / `onum` |
| Slashed zero | `font-variant-numeric: slashed-zero` | `zero` |
| Fractions | `font-variant-numeric: diagonal-fractions` / `stacked-fractions` | `frac` / `afrc` |
| Ordinals (1st, 2º) | `font-variant-numeric: ordinal` | `ordn` |
| Small caps | `font-variant-caps: small-caps` | `smcp` |
| Capitals to small caps | `font-variant-caps: all-small-caps` | `c2sc` + `smcp` |
| Superscript / subscript glyphs | `font-variant-position: super` / `sub` | `sups` / `subs` |
| Stylistic sets, character variants, swashes | `font-variant-alternates` + `@font-feature-values` | `ss01`–`ss20`, `cv01`–`cv99`, `swsh` |
| Case-sensitive punctuation | none | `case` |
| Stylistic alternates | `font-variant-alternates: stylistic(name)` | `salt` |
| Capital spacing | none | `cpsp` |

Support (Oct 2026): `font-variant-numeric` Baseline Widely available since 2022; `font-variant-alternates` and `@font-feature-values` Baseline Newly available since March 2023 (Chrome 111, Firefox 34, Safari 16.2 for `styleset()` and `character-variant()`). `font-variant-position` is not Baseline.

Use `font-feature-settings` only for tags with no high-level form (`case`, `cpsp`, a bare `cvNN`), scope it narrowly, and compose it through custom properties so features don't erase each other:

```css
:root { --ff-case: "case" 0; --ff-ss: "ss01" 0; }
/* every element that changes a tag re-declares the full list */
:root, .eyebrow, .brand { font-feature-settings: var(--ff-case), var(--ff-ss); }
.eyebrow { --ff-case: "case" 1; }
.brand   { --ff-ss: "ss01" 1; }
```

The re-declaration matters: `font-feature-settings` inherits as a computed value, so children of `:root` don't re-read the custom properties unless the property is declared on them again.

Don't put `font-feature-settings: "kern" 1, "liga" 1, "calt" 1` on `body`. Those features are already on, and the inherited low-level setting overrides high-level properties further down: `code { font-variant-ligatures: none }` stops working because the inherited `"liga" 1` wins. Any component that sets its own `font-feature-settings` also replaces the whole list. Inter's site recommends `"liga" 1, "calt" 1` as a fix for Chrome; if you copy it, scope it to the elements that need it.

## 2. Figures

| Context | Setting | Why |
|---|---|---|
| Tables, timers, counters, prices, chart axes, live numbers | `tabular-nums lining-nums` | Columns line up and changing numbers don't jitter |
| Running prose in a sans | Default (usually proportional lining) | Even colour |
| Running prose in a serif with `onum` | `oldstyle-nums proportional-nums` | Figures sit like lowercase letters and don't shout |
| All-caps headings and labels | `lining-nums` | Oldstyle figures look wrong next to capitals |
| Codes, IDs, serials where 0/O matters | `slashed-zero tabular-nums` | Disambiguation |

- Inter's tabular figures keep the same width across weights, so a number can turn bold on hover or selection without moving.
- **Many UI sans faces have no oldstyle figures** (Inter among them). `oldstyle-nums` does nothing there.
- **Apply `diagonal-fractions` only to a span around the fraction.** On a whole paragraph, `frac` also turns dates like 1/2/2026 into fractions.
- Tables and number alignment: `references/ui-and-tables.md`.

## 3. Ligatures

- **Leave `liga` and `calt` on.** They are the default; turning them off makes text worse in most fonts.
- **`dlig` only in display type**, and only after checking what the font's discretionary set does.
- **Code:** `font-variant-ligatures: none` on `code`, `pre`, `kbd`, unless the font is a deliberate programming-ligature face (their ligatures live in `calt`). Make programming ligatures a user preference.
- **Tracked text loses its ligatures.** Any non-zero `letter-spacing` disables `liga` and `clig`. That's right for tracked capitals.

## 4. Small caps

Bringhurst: "Genuine small caps are not simply shrunken versions of the full caps." Faux small caps are too light and too narrow.

- **Acronyms in running text:** `font-variant-caps: all-small-caps` with `letter-spacing: 0.05em`. Write the acronym in capitals in the HTML (`<abbr>NASA</abbr>`) so it reads correctly with styles off.
- **Small-cap headings or lead-ins:** `font-variant-caps: small-caps`.
- **Stop the browser faking them:** `font-synthesis-small-caps: none` (Chrome 97, Firefox 111, Safari 16.4; Baseline Widely available since 2025). Then a font without `smcp` shows lowercase, which is easy to spot in review.
- **Check for `smcp` and `c2sc` separately.** Many UI sans faces have neither: Inter (3 and 4) has no `smcp` or `c2sc`, so its small caps are always synthesized unless synthesis is off. If the font lacks real small caps, use capitals at a smaller size step with tracking instead, or use another font for that role.
- **Bulgarian small caps** need a font whose small-cap glyphs follow the Bulgarian forms. Check them with `lang="bg"` (`references/language.md`).

```css
html { font-synthesis-small-caps: none; }
abbr { font-variant-caps: all-small-caps; letter-spacing: 0.05em; }
.prose > p:first-of-type::first-line { font-variant-caps: small-caps; letter-spacing: 0.04em; }
```

Also consider `font-synthesis-weight: none` and `font-synthesis-style: none`, but only when every weight and italic you use is actually loaded. Otherwise a missing bold renders as regular.

## 5. Stylistic sets, character variants and alternates

Stylistic sets have no standard meaning. Inter's `ss01` is open digits. Source Serif 4's `ss01` is "Cyrillic: Bulgarian alternates". Google's Fira Sans uses `ss01` for Pan-African Latin alternates, while bBoxType's newer Fira Sans 4.3 builds put Bulgarian forms there. Always read the font's documentation or inspect it.

Common uses:
- **Disambiguation in UI and code-adjacent text:** a set that distinguishes I, l and 1, and O and 0. Inter has `ss02` (disambiguation) and `ss04` (disambiguation without slashed zero); `cv11` is a single-storey a; `zero` gives the slashed zero.
- **A brand's preferred letterforms:** alternate a, g, y or R set once on the brand elements.
- **Display flourishes:** swashes and stylistic alternates on a headline, never in body text.
- **Language forms the font also offers as a set** (Source Serif 4 `ss01` for Bulgarian), to force them regardless of `lang`.

Name sets once with `@font-feature-values`, so components ask for a meaning instead of a number. If the font changes, only the mapping changes:

```css
@font-feature-values Inter {
  @styleset         { disambiguate: 2; open-digits: 1; }
  @character-variant { single-storey-a: 11; }
}
@font-feature-values "Source Serif 4" {
  @styleset { bulgarian: 1; }
}

.code-like  { font-variant-alternates: styleset(disambiguate); }
.brand      { font-variant-alternates: character-variant(single-storey-a); }
```

Value counts: `@styleset` takes several values; `@character-variant` takes one or two; `@swash`, `@ornaments`, `@annotation` and `@stylistic` take exactly one. Styleset numbers above 99 are ignored.

## 6. Superscripts and subscripts

The default `<sup>` shrinks a regular glyph and raises it with `vertical-align`, which pushes lines apart. If the font has `sups`:

```css
sup { font-variant-position: super; vertical-align: baseline; font-size: inherit; }
```

Only do this when the font has the glyphs; otherwise the text renders full size on the baseline. `font-synthesis-position` is Firefox-only (118+, Oct 2026), so don't rely on it to catch missing glyphs.

## 7. Case-sensitive forms

In all-caps text, brackets, hyphens, dashes, colons and the @ sit too low because they're designed for lowercase. `case` raises them to cap height:

```css
.caps, .eyebrow, button { font-feature-settings: "case" 1; }
```

Compose it through a custom property if the element also needs other low-level tags (§1).

## 8. Discovering features

- **Inspect the file the site actually serves**, not the font's specimen page. Google Fonts API and Fontsource files drop stylistic sets, character variants, `case`, `zero`, small caps, oldstyle figures and `dlig` (checked Oct 2026), so those features need a self-hosted full font.
- **Wakamai Fondue** (wakamaifondue.com): drop a font, see every feature and axis, copy the CSS.
- **FontDrop** (fontdrop.info) and **FontGauntlet** (fontgauntlet.com): glyph maps, features, axes.
- **fontTools:** `ttx -t GSUB font.woff2` lists substitution features and their languages; `pyftsubset` builds subsets (pass `--layout-features='*'` to keep everything).
- The font's own specimen page, for example rsms.me/inter for Inter's feature list.
