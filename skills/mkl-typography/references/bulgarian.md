# Bulgarian

Bulgarian is one of Mike's shipping locales (yesterday ships `bg`). Most fonts and tools get it wrong in ways nobody sees until a Bulgarian reader does.

## 1. Letterforms

Bulgarian lowercase follows handwriting: more ascenders and descenders, and Latin-like shapes. Most fonts draw Russian forms by default, which look more like small capitals. The letters that differ include д, л, ж, в, г, т, к and ю.

**You need both `lang="bg"` and a font with `locl` for `cyrl`/`BGR`.**
- `font-feature-settings: "locl" 1` does nothing on its own. `locl` is already on; the language the browser passes to the shaper comes from `lang`.
- To force the forms regardless of `lang`, use a font that is Bulgarian by default, a font with a Bulgarian stylistic set (self-hosted, because Google strips sets), or a custom build.

**Known results, as served by Google (Oct 2026). These are proof of each route, not a catalogue:**

| Font | Bulgarian forms | Route |
|---|---|---|
| Sofia Sans | Yes | Bulgarian by default |
| Source Serif 4 | Yes | `locl` (also `ss01` when self-hosted) |
| Montserrat | Yes | `locl` |
| Geist | **No** | No Cyrillic `locl` |
| Literata | **No** | No Cyrillic `locl` |
| Roboto | **No** | Requested since about 2016 |
| Apple system fonts (iOS) | Reported no | A system-font stack falls back to Russian forms |

Check any other font with `scripts/font-check.py`, then render the test string in the browser:

> Жълтата дюля беше щастлива, че пухът, който цъфна, замръзна като гьон.

Compare it with and without `lang="bg"`. Figma never shows the Bulgarian forms, so mock-ups mislead.

```css
/* self-hosted Source Serif 4: force Bulgarian forms even where lang is missing */
@font-feature-values "Source Serif 4" { @styleset { bulgarian: 1; } }
.serif-bg { font-variant-alternates: styleset(bulgarian); }
```

## 2. Breaking and hyphenation

- **Safari and iOS Safari have no Bulgarian hyphenation dictionary** (through 27.2). Chrome, Edge and Firefox do. Set Bulgarian ragged right, never justified: `:lang(bg) p { hyphens: auto; text-align: start; }`.
- **One-letter words don't end a line:** в, с, и, а, о, у bind to the next word with U+00A0. Use a build step, because hand-typed `&nbsp;` doesn't survive editors. Run it on text nodes outside `code` and `pre`:

```js
const NB = " ";
const UNIT = String.raw`(?:%|°C|€|лв\.?|г\.|км|кг|мин|ч|см|мм|м|kg|km|m|cm|mm|min|h|s|ms|KB|MB|GB)`;
const rules = {
  any: [[new RegExp(String.raw`(\d)\s+(${UNIT})(?![\p{L}\p{N}])`, "gu"), `$1${NB}$2`]],
  bg: [[/(?<=^|[\s(„"«])([ВвСсИиАаОоУу])\s+/gu, `$1${NB}`]],
};
export function bindSpaces(text, lang = "") {
  const extra = rules[lang.toLowerCase().split("-")[0]] ?? [];
  for (const [re, to] of [...rules.any, ...extra]) text = text.replace(re, to);
  return text;
}
```

The rule handles runs too ("и в града"). Units bind only when they stand alone ("5 мин", not "5 минути").

## 3. Conventions

Confirm these with Mike's house style before shipping:
- **Quotes** „…“ (low-9 opening, high-6 closing). Chromium's `quotes: auto` for `bg` uses „“ at both levels. For nesting, use ‚‘: `:lang(bg) q { quotes: "„" "“" "‚" "‘"; }`.
- **Dash:** use a spaced dash for a break in a sentence. The en dash ("думи – думи") is common on screen. Formal Bulgarian typesetting often uses a spaced em dash (тире). Pick one per product and keep it (open question; the 2026-10-22 test used the en dash).
- **Numbers:** a decimal comma, with a space as the thousands separator: 1 234 567,89. `Intl.NumberFormat('bg-BG')` may not group four-digit numbers, so check its output.
- **Dates:** 22.10.2026 г., with a no-break space before "г.".

## 4. Generated images

Satori (`next/og`) has no Bulgarian `locl`. Use a font whose default Cyrillic is Bulgarian (Sofia Sans), or turn on a Bulgarian stylistic set with `font-feature-settings` from a full, self-hosted file. Check the rendered PNG.
