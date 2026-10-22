# Line breaking

Compositors spent centuries deciding where lines end. Browsers now do some of it well, some of it in one engine only, and some of it not at all. Support figures are from @mdn/browser-compat-data 8.1.7 and web-features 3.43.0 (Oct 2026).

## 1. Hyphenation

`hyphens: auto` and `hyphenate-character` have been Baseline Widely available since March 2026 (Chrome 88 desktop, Firefox 43, Safari 17 unprefixed; `-webkit-hyphens` since Safari 5.1). They need **a correct `lang` and a dictionary for that language in that browser**, and dictionary coverage varies:

| Language | Chrome | Firefox | Safari |
|---|---|---|---|
| English, French, Spanish, German (reformed), Danish, Norwegian, Portuguese, Croatian, Hungarian | ✓ (87) | ✓ | ✓ |
| Italian, Dutch, Swedish, Russian, Ukrainian | ✓ (112) | ✓ | ✓ |
| Czech | ✓ (112) | ✓ (130) | ✓ |
| Polish, Finnish, Catalan, Turkish | ✗ | ✓ | ✓ |
| **Bulgarian**, Slovenian, Estonian | ✓ (87) | ✓ | ✗ |
| Slovak, Lithuanian | ✓ (112) | ✓ | ✗ |
| Greek, Latvian, Belarusian | ✓ | ✗ | ✗ |

Chrome numbers are the desktop versions that added the dictionary. Look up any other language in BCD's `css.properties.hyphens.language_*` entries.

**Rules:**
- **Hyphenate running prose only:** paragraphs, list items, definitions, captions.
- **Never hyphenate** headings, buttons, labels, navigation, table headers, code, URLs, names or brand names.
- **Limit short fragments:** `hyphenate-limit-chars: 6 3 3` (word at least 6 characters, at least 3 before and 3 after the break). Chrome 109+, Firefox 137+; Safari ignores it.
- **Don't use** `hyphenate-limit-lines`, `hyphenate-limit-zone` or `hyphenate-limit-last`. None has shipped in a stable browser.
- **For a language a browser can't hyphenate**, insert soft hyphens (`&shy;`) at build time (for example with the Typeset npm package or a hyphenation library and a rehype plugin), or set the text ragged.
- **Long compound words in narrow columns** (German, Finnish, Bulgarian) need hyphenation more than a wider measure.

```css
.prose :is(p, li, dd, figcaption) {
  -webkit-hyphens: auto;
  hyphens: auto;
  hyphenate-limit-chars: 6 3 3;
}
:is(h1, h2, h3, h4, h5, h6, nav, button, label, th, code, pre, kbd, a[href^="http"]) { hyphens: manual; }
```

## 2. Justification

Justified text looks orderly in print because compositors hyphenate, adjust word spacing within limits and rework paragraphs. Browsers do less.

**Justify only when all of these hold:**
- Hyphenation works for that language in every target browser.
- The measure is about 60 characters or wider.
- `text-wrap: pretty` is on.
- It is long-form reading text, not UI.

Otherwise set ragged right (`text-align: start`). WCAG 1.4.8 (AAA) asks for unjustified text. `text-justify` (Chrome 145+, Firefox) is not in Safari; `inter-character` is for CJK only. `text-align-last` is Baseline.

## 3. `text-wrap`

| Value | Use on | Support (Oct 2026) | What it does |
|---|---|---|---|
| `balance` | Headings, captions, pull quotes, short teasers | Baseline since May 2024 (Chrome 114, Firefox 121, Safari 17.5) | Evens line lengths in short blocks. Engines cap it at a few lines (sources disagree: 4 or 6 in Chromium, 10 in Firefox), so say "short blocks only" |
| `pretty` | Paragraphs and list items | Chrome 117+, Safari 26+; **not Firefox** | Chrome reworks the last four lines to avoid a one-word last line and stacked hyphens. Safari evaluates the whole paragraph: better rag, fewer hyphens, no short last lines |
| `stable` | Editable text, `contenteditable`, textareas | Chrome 130, Firefox 121, Safari 17.5 | Earlier lines don't re-wrap while the user types |

- Don't use `balance` on paragraphs: it leaves the right edge ragged in a way that looks like a mistake.
- `pretty` has a performance cost on very long elements (thousands of lines), not on normal articles.
- Safari's `pretty` can narrow a whole paragraph so it looks different from its neighbours (noted by John Gruber, 2025). Check pages with a short paragraph next to a long one.

```css
:is(h1, h2, h3, h4, blockquote, figcaption, .teaser) { text-wrap: balance; }
:is(p, li, dd)                                          { text-wrap: pretty; }
[contenteditable], textarea                             { text-wrap: stable; }
```

## 4. Runts, widows and orphans

- **A runt** (one short word alone on the last line of a paragraph) is the screen problem. `text-wrap: pretty` fixes it in Chrome and Safari. For Firefox, a build step can replace the last space in each paragraph with a no-break space when the last two words are short.
- **`widows` and `orphans` don't help on screen.** They only apply to fragmentation: print, multi-column layout and page breaks. Firefox doesn't support them at all.
- **Print stylesheets:** set `widows: 2; orphans: 2` and `break-after: avoid` on headings so a heading never ends a page.

## 5. Keeping things together

Bind with a no-break space (U+00A0, `&nbsp;`) or a narrow one (U+202F):

- A number and its unit: 10 kg, 5 min, 100 €, 21 °C.
- Initials and names: J. R. R. Tolkien.
- Abbreviations and what follows: No. 5, p. 12, fig. 3, § 4.
- Dates: 22 October, 22.10.2026 г.
- One-letter words at line end, in Slavic languages: Bulgarian в, с, и, а, о, у; similar rules in Czech, Slovak and Polish. Scope the rule with `lang`.
- Short phrases that must not split in UI ("Sign in"): `white-space: nowrap` on the span.

A build step (rehype or a CMS filter) is the reliable way to do this. Hand-typing `&nbsp;` doesn't survive editors.

```js
// text transform for a rehype plugin or CMS filter; run on text nodes outside code/pre
const NB = '\u00A0'
const UNIT = String.raw`(?:%|‰|°C|°F|€|\$|£|лв\.?|г\.|км|кг|мин|ч|см|мм|м|kg|g|mg|km|m|cm|mm|ml|l|min|h|s|ms|KB|MB|GB|TB|px|pt)`
const rules = {
  any: [
    [new RegExp(String.raw`(\d)\s+(${UNIT})(?![\p{L}\p{N}])`, 'gu'), `$1${NB}$2`],
    [/(?<![\p{L}])(No\.|no\.|p\.|pp\.|[Ff]ig\.|§)\s+(?=[\p{N}\p{L}])/gu, `$1${NB}`],
  ],
  bg: [[/(?<=^|[\s(„"«])([ВвСсИиАаОоУу])\s+/gu, `$1${NB}`]],
}
export function bindSpaces(text, lang = '') {
  const extra = rules[lang.toLowerCase().split('-')[0]] ?? []
  for (const [re, to] of [...rules.any, ...extra]) text = text.replace(re, to)
  return text
}
```

Tested on English and Bulgarian samples: units bind only when they stand alone ("5 min", not "5 minutes"), runs of one-letter words bind ("и в града"), and a missing `lang` is handled. Treat it as a starting point and test it against real content, since a CMS will find every edge case.

## 6. Long strings

- **URLs and long identifiers:** `overflow-wrap: anywhere` (Baseline 2022) breaks them only when necessary, and also lets the element shrink in flex and grid so it doesn't overflow its container. Prefer it to `break-word`.
- **`word-break: break-all`** only for hashes, keys and code, where any break is fine.
- **`<wbr>`** after `/`, `.` and `?` in displayed URLs gives nicer break points.
- **`word-break: auto-phrase`** is Chrome-only (119+) and affects only Japanese and Korean.
- **`line-break: strict`** controls CJK punctuation breaking.

```css
.prose        { overflow-wrap: anywhere; }
.hash, .token { word-break: break-all; font-variant-numeric: tabular-nums slashed-zero; }
```
