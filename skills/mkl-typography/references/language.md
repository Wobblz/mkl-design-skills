# Language and characters

## 1. What `lang` does

The `lang` attribute is a typesetting setting, not just metadata. It does four jobs:

1. **Localized glyphs.** It tells the text shaper which language the text is in, so the font's `locl` feature can swap in local forms: Bulgarian and Serbian Cyrillic, Polish kreska accents, Romanian comma-below ș and ț, Dutch IJ, and others.
2. **Hyphenation.** `hyphens: auto` uses the dictionary for the element's language, and does nothing without one (`references/line-breaking.md`).
3. **Quotation marks.** `quotes: auto` (the default) and `<q>` pick the language's marks.
4. **Casing.** `text-transform` follows language rules: Turkish and Azerbaijani i → İ, Greek uppercase drops accents (not in Safari), Dutch ij → IJ (not in Chrome).

Rules:
- Set `<html lang="…">` on every page.
- Mark every passage in another language with its own `lang`: a quote, a product name, a citation, a language switcher label.
- Use `:lang(xx)` in CSS for per-language rules. It matches inherited language, unlike `[lang="xx"]`.
- Language-dependent behaviour (casing, quote mappings) was not re-tested for this skill (Oct 2026); render real strings in the browsers you ship to.

## 2. Bulgarian Cyrillic

Bulgarian has its own Cyrillic letterforms, different from the Russian ones most fonts show by default. Bulgarian lowercase follows handwriting: more ascenders and descenders, Latin-like shapes and one-sided serifs. Russian lowercase looks more like small capitals. The letters that differ include д, л, ж, в, г, т, к and ю, among others.

**How to get them:**
- **`lang="bg"` plus a font that has `locl` for Bulgarian** (`cyrl` script, `BGR` language). Both are needed.
- **`font-feature-settings: "locl" 1` does nothing on its own.** `locl` is already on; which forms it picks depends on the language the browser passes to the shaper, which comes from `lang`.
- **Forcing Bulgarian forms regardless of `lang`** takes one of: a font whose default Cyrillic is Bulgarian, a font that offers the forms as a stylistic set, or a custom build of the font.
- **Small caps** should follow the Bulgarian forms too. Render `font-variant-caps: small-caps` with `lang="bg"` and check before using small caps in Bulgarian text.

**Fonts (checked Oct 2026; not a catalogue, just proof of each route):**
- Bulgarian forms by default: Sofia Sans.
- Through `locl` with `lang="bg"`: Source Serif 4, Montserrat. The `locl` survives in Google-served files.
- Through a stylistic set as well: Source Serif 4 `ss01` ("Cyrillic: Bulgarian alternates"), and bBoxType's Fira Sans 4.3 builds. Google's Fira Sans has no Bulgarian forms. Stylistic sets are stripped from Google-served files, so this route needs a self-hosted full font.
- **No Bulgarian forms:** Roboto (the request has been open since about 2016). Apple's system fonts on iOS are reported to render Bulgarian with Russian forms, so a system-font stack falls back to Russian shapes.
- Google-served files kept the Bulgarian `locl` for Source Serif 4 and Montserrat (Oct 2026), but one user found another Google-served font missing its localisation. Test the actual served file.

**Checking a font:** inspect it for `locl` under `cyrl`/`BGR` (SKILL.md §5), then render a test string such as "Жълтата дюля беше щастлива, че пухът, който цъфна, замръзна като гьон." with and without `lang="bg"` and compare д, л, в, ж, т, ю.

**Design tools:** Figma does not pass the text language to its shaper, so mock-ups show Russian forms while the browser shows Bulgarian ones. Review Bulgarian typography in the browser.

**Hyphenation:** Chrome and Edge (87+) and Firefox hyphenate Bulgarian. **Safari and iOS Safari don't** (no Bulgarian dictionary through Safari 27.2). Set Bulgarian ragged right, or insert soft hyphens at build time.

```html
<html lang="bg">
  …
  <p lang="en">An English sentence inside Bulgarian text.</p>
</html>
```
```css
:lang(bg) body { font-family: "Sofia Sans", system-ui, sans-serif; }
:lang(bg) p    { hyphens: auto; text-align: start; }     /* no Safari dictionary: never justify */

/* self-hosted Source Serif 4: force Bulgarian forms even where lang is missing */
@font-feature-values "Source Serif 4" { @styleset { bulgarian: 1; } }
.serif-bg { font-variant-alternates: styleset(bulgarian); }
```

**Bulgarian conventions** (standard orthography, but not checked against an official source for this skill; confirm before shipping):
- Quotes „…“ (low-9 opening, high-6 closing): `:lang(bg) q { quotes: "„" "“" "‚" "‘"; }`. Chromium's `quotes: auto` for `bg` uses „“ at both levels; the nested ‚‘ above is a common choice, so confirm the house style.
- Decimal comma, space as the thousands separator: 1 234 567,89. Check `Intl.NumberFormat('bg-BG')` output, which may not group four-digit numbers.
- Dates as 22.10.2026 г., with a no-break space before "г.".
- Dash with spaces for parenthetical breaks: "думи – думи".
- Don't end a line with one-letter words (в, с, и, а, о, у); bind them to the next word with a no-break space (`references/line-breaking.md`).

## 3. Other languages, briefly

- **Serbian and Macedonian** have their own Cyrillic forms (italic б, г, д, п, т especially); same mechanism: `lang="sr"` / `lang="mk"` plus `locl`.
- **Ukrainian** uses ґ, є, і, ї; check coverage. **Russian** is the default most fonts draw.
- **Polish** acute (kreska) is steeper than the generic acute in fonts with a `PLK` `locl`.
- **Romanian** needs comma-below ș ț (U+0219, U+021B), not cedilla ş ţ.
- **Turkish:** `text-transform: uppercase` maps i to İ only with `lang="tr"`.
- **German:** `text-transform: uppercase` turns ß into SS; capital ẞ exists but browsers don't use it by default.
- **French:** a no-break space before : and inside « », and a narrow no-break space (U+202F) before ; ! ? (many publishers now use the narrow one everywhere). CSS doesn't add them; put them in the content.
- **CJK:** `text-spacing-trim` and `text-autospace` handle punctuation width and spacing between CJK and Latin. `text-spacing-trim` is Chrome-only (123+) as of Oct 2026.

## 4. Characters

Use the real character, typed or inserted by a build step (a smart-quotes plugin such as `remark-smartypants`), never an ASCII stand-in.

| Use | Character | Not | Notes |
|---|---|---|---|
| Quotes (English) | “ ” and ‘ ’ | " and ' | `quotes` handles `<q>`; content needs the real glyphs |
| Apostrophe | ’ (U+2019) | ' | Same glyph as the closing single quote |
| Ranges, "to" | – en dash (U+2013) | - | 9–5, pages 10–12, no spaces in English |
| Break in a sentence | — em dash (U+2014), or spaced en dash | -- | House style: closed em dash (US) or spaced en dash (UK, Bulgarian) |
| Hyphen | - | | Compound words only |
| Minus | − (U+2212) | - | Same width as + |
| Multiplication, dimensions | × (U+00D7) | x | 1920 × 1080 |
| Ellipsis | … (U+2026) | ... | |
| Feet/inches, minutes/seconds | ′ ″ (U+2032, U+2033) | ' " | 5′ 11″ |
| Degree | ° | º (ordinal) | 21 °C (SI) |
| No-break space | U+00A0 | space | Number and unit, initials, "No. 5" |
| Narrow no-break space | U+202F | | French punctuation, thousands groups |
| Figure space | U+2007 | | Pads numbers in tables to one digit's width |
| Thin space | U+2009 | | Around em dashes in some styles; breakable |
| Soft hyphen | U+00AD (`&shy;`) | | Allowed break point; shows a hyphen only if it breaks |
| No-break hyphen | U+2011 | | Phone numbers, compound names that mustn't split |
| Word joiner | U+2060 | | Prevents a break without adding space |

Code, terminal output and anything copied into a shell keep straight quotes and hyphens. Turn the smart-quotes step off inside `code` and `pre`.
