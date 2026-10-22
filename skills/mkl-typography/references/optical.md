# Optical alignment

A box aligned to a mathematical edge doesn't always look aligned. Round letters, diagonal letters, quote marks and bullets carry their own white space, so a line that starts with one looks indented. Print compositors fixed this with hanging punctuation and optical margin alignment. On the web, Safari does part of it, and the rest is CSS tricks and a small build step.

Support figures are from @mdn/browser-compat-data 8.1.7 (Oct 2026).

## 1. Hanging punctuation

An opening quote at the start of a paragraph or blockquote should sit in the margin, so the letters align with the text edge.

- **`hanging-punctuation` works only in Safari** (partial since Safari 10, full since 26.5 in May 2026, when straight quotes started hanging too). Chrome and Firefox have no support.
- Use it inside `@supports` as an enhancement, plus a fallback class added at build time for paragraphs that start with a quote.
- **Only hang where the margin has room.** On a phone with the text close to the screen edge, the quote would be clipped. Turn the fallback off below the width where the column has a gutter.

Pull values from the Typeset project (tune per font): double quotes −0.46em, single quotes −0.27em, « about −0.3em.

```css
@supports (hanging-punctuation: first) {
  .prose :is(p, blockquote, li) { hanging-punctuation: first allow-end last; }
}
@supports not (hanging-punctuation: first) {
  .hang-dq { text-indent: -0.46em; }    /* “ " „ */
  .hang-sq { text-indent: -0.27em; }    /* ‘ ' ‚ */
  .hang-gm { text-indent: -0.3em; }     /* « */
}
@media (max-width: 40em) {
  .hang-dq, .hang-sq, .hang-gm { text-indent: 0; }
}
```

```js
// build step or client-side for CMS content: tag blocks that open with a quote
const CLASS = { '“': 'hang-dq', '"': 'hang-dq', '„': 'hang-dq', '‘': 'hang-sq', "'": 'hang-sq', '‚': 'hang-sq', '«': 'hang-gm' }
for (const el of document.querySelectorAll('.prose :is(p, blockquote)')) {
  const c = CLASS[el.textContent.trimStart()[0]]
  if (c) el.classList.add(c)
}
```

`allow-end` lets a full stop or comma at the end of a line hang into the right margin, which evens out a justified edge. It only matters in Safari.

## 2. Hanging lists

Bullets and numbers should hang in the margin, so the list text aligns with the paragraph text above and below. **`hanging-punctuation` never moves list markers.**

- **Simple version:** remove the list's start padding and keep markers outside. Markers then sit to the left of the text edge.
- **When there's no gutter** (phones, cards), put the padding back, or the markers are clipped.
- **Numbers line up on the right** (so 9. and 10. align on the full stop) with tabular figures and custom counters.
- **`::marker` is limited in Safari** to `color` and `font-size`, so use `::before` counters for anything more.
- **Removing native markers can strip list semantics** in VoiceOver. Add `role="list"` to a `ul`/`ol` that uses `list-style: none`.

```css
.prose :is(ul, ol)  { padding-inline-start: 0; list-style-position: outside; }
.prose li::marker   { color: var(--muted); }                 /* Safari-safe */
@media (max-width: 40em) { .prose :is(ul, ol) { padding-inline-start: 1.25em; } }

/* full control: right-aligned tabular numbers hanging in the margin */
.prose ol.hang               { list-style: none; counter-reset: item; padding-inline-start: 0; }
.prose ol.hang > li          { position: relative; counter-increment: item; }
.prose ol.hang > li::before  {
  content: counter(item) ".";
  position: absolute; inset-inline-end: 100%; padding-inline-end: 0.5em;
  font-variant-numeric: tabular-nums;
}
```

```html
<ol class="hang" role="list">…</ol>
```

`@counter-style` (Baseline Widely available since March 2026) defines custom numbering, for example Cyrillic letters for Bulgarian sub-lists. `text-indent: hanging` became Baseline in March 2026 and suits hanging-indent bibliographies.

## 3. Optical margin alignment of letters

No browser does optical margin alignment (the glyph protrusion InDesign and pdfTeX apply to every line). At display sizes, a heading that starts with T, V, W, Y, A, O, C, G or Q, or with a quote, looks indented next to body text below it.

- **Correct only at about 48px and above**, where the error is more than a pixel. At body sizes leave it.
- **Pull the first glyph into the margin** by an amount relative to the size. Typeset's starting values: T V W Y −0.07em, O C G Q −0.04em, A −0.03em. Tune per font by placing the heading over the body text and adjusting until the stems line up.
- **Single-line headings:** shift the whole heading with `margin-inline-start`.
- **Multi-line headings:** only the first line starts with that letter, so wrap the first glyph in a span and shift the span. Keep the word whole for screen readers (shift with margin, don't split the word into separate text nodes that change reading).
- **Lines after a wrap** can start with any letter. No maintained library adjusts every wrapped line in the browser; if it matters (a poster-like hero), set the line breaks by hand.

```js
// display headings only; values from Typeset, tune per font
const PULL = { T: .07, V: .07, W: .07, Y: .07, A: .03, O: .04, C: .04, G: .04, Q: .04, '“': .46, '"': .46, '‘': .27, "'": .27, '«': .3 }
for (const h of document.querySelectorAll('h1, h2, .display')) {
  const first = h.textContent.trimStart()[0]
  if (PULL[first] && parseFloat(getComputedStyle(h).fontSize) >= 48) {
    h.style.marginInlineStart = `-${PULL[first]}em`
  }
}
```

Run it at build time where the content is static (a rehype plugin that adds a class), and at runtime only for CMS headings. Re-run after fonts load, since the font size can change.

**Related edge corrections:**
- **Large numerals** in a stat block can need the same check: a leading 1 or 7 often carries more side space than 0 or 8 (especially with tabular figures).
- **Icons beside a heading** are aligned to the cap height, not the box (§5).
- **Display text and body text** should share an optical left edge. Check it at full size, not zoomed out.

## 4. Drop caps and initials

- **`initial-letter`** sinks a capital over N lines and aligns it to the cap height and baseline. Unprefixed in Chrome 110+. Safari needs `-webkit-initial-letter` (since Safari 9) and iOS accepts integers only. **Firefox has no support.** `initial-letter-align` has shipped nowhere.
- **Fallback:** a floated `::first-letter`. It can't align to the cap height exactly, so tune its size and offsets per font.
- **Use them only on the first paragraph of long-form articles**, and only when that paragraph is longer than the drop.
- **Integer values only:** `3` for a three-line drop, `3 1` for a raised cap (three lines tall, sitting on the first line).
- **A leading quote is part of `::first-letter`**, so “ is enlarged with the letter. Style it deliberately or hang it.
- **Prefer the pseudo-element to a `<span>`**, which can split the word for screen readers.
- **A small-caps lead-in** on the rest of the first line pairs well: `::first-line` with `font-variant-caps`.

```css
.prose > p:first-of-type::first-letter {
  float: inline-start;
  font-size: calc(3 * 1lh / 0.72);   /* 0.72 ≈ the font's cap-height ratio; tune */
  line-height: 1;
  margin-inline-end: 0.08em;
  margin-block-start: 0.06em;
  font-weight: 700;
}
@supports (initial-letter: 3) or (-webkit-initial-letter: 3) {
  .prose > p:first-of-type::first-letter {
    float: none; font-size: inherit; line-height: inherit; margin: 0 0.08em 0 0;
    -webkit-initial-letter: 3;
    initial-letter: 3;
  }
}
.prose > p:first-of-type::first-line { font-variant-caps: small-caps; letter-spacing: 0.04em; }
```

## 5. Vertical optical alignment

**`text-box-trim`** removes the half-leading above the cap height and below the baseline, so text inside a padded box looks centred and spacing can be set with `gap` alone. Support: Safari 18.2 (Dec 2024), Chrome 133 (Feb 2025), Firefox 154 (Aug 2026). Trimming inline elements works in Firefox and partly in Safari, not Chrome. Older browsers keep normal leading, which is harmless.

- **Use it on components:** buttons, badges, chips, cards, callouts, captions, and headings that must align with the top of an image.
- **Not on prose.** Article rhythm is built from line-heights; none of the measured editorial sites trims article text.
- **`trim-both cap alphabetic`** is the common setting. Use `ex` instead of `cap` to centre lowercase-heavy labels.

```css
:is(.btn, .badge, .chip)                 { text-box: trim-both cap alphabetic; }
:is(.card, .callout) > :first-child      { text-box: trim-start cap alphabetic; }
:is(.card, .callout) > :last-child       { text-box: trim-end cap alphabetic; }
```

**Units:**
- `cap` (cap height, Widely available since June 2026): size inline icons with `height: 1cap` so they match capitals.
- `ex` (x-height): align lowercase-height elements.
- `lh` and `rlh` (line-height, Widely since May 2026): rhythm (`references/rhythm.md`).
- `ic` (CJK advance): measure in CJK.

```css
.icon-inline { block-size: 1cap; inline-size: auto; vertical-align: 0; }   /* sits on the baseline, top at cap height */
```

**Overshoot is deliberate.** Round letters (O, C, S) extend slightly past the baseline and cap height so they look the same size as flat letters. Don't correct it when aligning to a grid or an icon; align to the flat letters.

## 6. Underlines

`text-underline-offset`, `text-decoration-thickness` and `text-decoration-skip-ink` are Baseline. Set them in `em` so underlines scale with headings (percentage thickness needs Safari 17.4+). The values below are unsourced starting points; tune per font.

```css
a {
  text-decoration-line: underline;
  text-decoration-thickness: max(1px, 0.0625em);
  text-underline-offset: 0.18em;
  text-decoration-skip-ink: auto;
}
```
