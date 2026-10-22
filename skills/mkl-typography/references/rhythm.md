# Vertical rhythm

Rhythm is the distance between things: a heading and its first paragraph, one paragraph and the next, the last paragraph and the end of the article. Get these right and a page reads as structured before anyone reads a word. Get them wrong and no font will save it.

The web version of rhythm is not a baseline grid. Mixed sizes, images, embeds and user zoom break any locked grid. It is a small set of spacing tokens, each a multiple of the body line-height, applied by the relationship between neighbouring elements.

## 1. What good editorial sites actually do

Measured on 2026-10-22 with Playwright and Chromium at 1440px and 390px widths. Gaps are box to box, so they include half-leading. Many major news sites (NYT, New Yorker, FT, Bloomberg, Medium, Substack, OpenAI) could not be reached from the research environment, so these figures rest on fewer sites than intended. Re-measure them when you can.

| Site [evidence] | Body size / line-height | Measure (desktop) | Paragraph gap | Above ÷ below h2 | Figure gap ÷ paragraph gap |
|---|---|---|---|---|---|
| Anthropic research [measured live] | 16.4px / 1.53 | 624px, ~80 characters | 24px = 0.96 lines | 48 / 24 = 2.0 | 2.7 desktop, 2.0 mobile |
| Distill [rendered from source] | 17px / 1.7 | 704px, ~85 characters | 1em = 0.59 lines | 49 / 24 = 2.0 | 2.5 |
| Tufte CSS [rendered from source] | 21px / 1.43 | 693px, ~80 characters | 21px = 0.7 lines | 1.5 (3.9 at a section start) | 2.1 |
| The Guardian [read from source] | 17px / 1.4 | 620px | 12px = 0.5 lines | large (inferred) | 1.0 |
| arXiv HTML (ar5iv) [read from source] | 16px / 1.5 | 832px | 24px = 1.0 line | ~1.7 (inferred) | — |

What they share:

- **Paragraph gap: 0.5–1.0 × the body line-height.** Only gwern.net, among the sites examined, indents paragraphs (2.5em) instead.
- **Space above a heading is about 2× the space below it.** The heading binds to its section.
- **Figures, blockquotes, code and rules get 2–2.7× the paragraph gap.** The Guardian is the exception, spacing figures like paragraphs.
- **Captions and notes are 0.75–0.85 × the body size.**
- **The end of an article gets 3–4 lines** before the next region.
- **Lists follow one of two schools:** items spaced like paragraphs (Anthropic, Distill), or nearly touching (Tufte, Guardian). Either way, the list as a whole takes the paragraph gap before and after.
- **Desktop measures run long (80–88 characters)**, offset by generous leading (1.43–1.7). Measure and leading are one decision.

## 2. The spacing table

Express every gap in `rlh` (the root line-height), so spacing follows the body leading even inside a heading with its own tighter line-height. Set the root line-height to the body leading.

| Between | Gap | Why |
|---|---|---|
| Paragraph → paragraph | 0.6–1.0 rlh (default 0.75) | Clearly a new thought, still one text. Butterick: 50–100% of the body size |
| Paragraph → paragraph, indent model | 0, with `text-indent: 1–1.5em` | The indent marks the break. Never indent the first paragraph after a heading or break |
| Anything → h2 | 2 rlh (≈ 2 × paragraph gap, or more) | Separates sections |
| Anything → h3 | 1.5 rlh | Weaker break than h2 |
| h2 → h3 directly | 0.75 rlh | They belong together |
| Heading → its first paragraph | 0.5 rlh (≤ 1 × paragraph gap) | Binds the heading to its text |
| Title → standfirst / dek | 0.5 rlh | One unit |
| Standfirst → byline / meta | 1 rlh | |
| Meta → first paragraph | 1.5–2 rlh | Start of the text proper |
| Paragraph → list, list → paragraph | Paragraph gap | A list is part of the flow |
| List item → list item | 0.25 rlh (tight) or paragraph gap (when items are sentences) | Choose one school per site |
| Nested list | 0.25 rlh above | |
| Paragraph → figure, figure → paragraph | 2 rlh (≈ 2–2.7 × paragraph gap) | An interruption needs air |
| Figure image → caption | 0.5–0.65 rlh | Caption belongs to the image |
| Paragraph → blockquote / pull quote / code / table / hr | 1.5–2 rlh | |
| Section break (`hr`, asterism ⁂ or space) | 2–3 rlh total | A pause, not a new section |
| Last paragraph → end of article | 3–4 rlh | Ends the piece clearly |
| Footnotes / endnotes block | 3 rlh above, notes 0.25–0.5 rlh apart | Separate apparatus |
| First child of the article | 0 above | The container's padding handles it |

Butterick's rule of thumb also holds: "the best way to emphasize a heading is by putting space above and below." Size and weight come second.

## 3. The CSS

Production sites put the margin on the *start* of the element that follows another (`* + *`), not on both sides. This avoids margin collapsing surprises and lets each relationship be targeted.

```css
:root { line-height: 1.55; }       /* body leading; 1rlh now equals one body line */

.prose > * + *               { margin-block-start: var(--flow, 0.75rlh); }
.prose > :is(h2)             { --flow: 2rlh; }
.prose > :is(h3, h4)         { --flow: 1.5rlh; }
.prose > h2 + h3             { --flow: 0.75rlh; }
.prose > :is(h2, h3, h4) + * { --flow: 0.5rlh; }

.prose > :is(figure, pre, table, blockquote, hr, aside),
.prose > :is(figure, pre, table, blockquote, hr, aside) + * { --flow: 2rlh; }

.prose li + li               { margin-block-start: 0.25rlh; }   /* tight school */
.prose li > :is(ul, ol)      { margin-block-start: 0.25rlh; }
.prose figcaption            { margin-block-start: 0.6rlh; font-size: 0.8em; line-height: 1.45; }
.prose > :last-child         { margin-block-end: 3rlh; }

/* indent model instead of space: */
.prose--indented > p + p     { --flow: 0; text-indent: 1.5em; }
```

Notes:
- **Grid containers don't collapse margins.** Anthropic and Distill set the article as a CSS grid, so margins add. With start-only margins that's predictable. In normal flow, start-only margins also avoid collapse problems.
- **Drop a figure's trailing gap before a heading**, or the heading's space adds to it. Anthropic does this with `.media-column:has(+ .post-heading) { margin-bottom: 0 }`.
- **Don't route a unit fallback through `var()`.** The usual "declare `1em`, then `1rlh`" fallback fails inside a custom property: an unsupported unit makes the property invalid at computed-value time and the gap becomes zero. `rlh` is Baseline Widely available (May 2026), so you no longer need the fallback. If you must support older browsers, use `@supports (margin: 1rlh)`.
- **Spacing in `rlh` or `em` keeps the ratios when the type scale is fluid.** Spacing in px drifts: Anthropic's 24px gap is 0.96 lines on desktop and 1.05 on mobile.
- **`text-box-trim` belongs to components, not prose.** Use it on cards, callouts and buttons (`references/optical.md`). None of the measured sites trims article text.

Tailwind v4: put the flow rules in a `@layer components` block for `.prose`, or set `--flow` per element with arbitrary properties. The official typography plugin uses em-based margins on both sides; if the project uses it, override its spacing with the table above instead of fighting it element by element.

## 4. Research-paper and long-form layouts

Research sites (Distill, Tufte CSS, arXiv HTML, gwern.net, Anthropic's research posts) add a few patterns:

- **A centred text column with breakout figures.** Name the grid lines (`[full-start] … [text-start] … [text-end] … [full-end]`) and let figures span wider tracks. Distill uses `.l-page` and `.l-screen`; Tufte's `figure.fullwidth` spans 90%.
- **Captions stay at text width even when the figure breaks out.** Distill measured a 1440px figure with a 704px caption.
- **Sidenotes in the margin** at about 0.8× body size, line-height 1.3–1.5, with a gutter of 3–4em. Below about 760px they become a tap-to-open inline note (Tufte) or move to the end. Footnotes become hover notes plus an end list (Distill, Anthropic).
- **Display maths gets little extra space** (about 0.4–0.65rem) and scrolls sideways on narrow screens rather than shrinking.
- **Wide tables and code scroll inside their own box** with `overflow-x: auto`, never the page.

```css
.article {
  display: grid;
  grid-template-columns:
    [full-start] minmax(1rem, 1fr)
    [wide-start] minmax(0, 8rem)
    [text-start] minmax(0, 33em) [text-end]
    minmax(0, 8rem) [wide-end]
    minmax(1rem, 1fr) [full-end];
}
.article > *          { grid-column: text; }
.article > .wide      { grid-column: wide; }
.article > .full      { grid-column: full; }
.article figcaption   { max-inline-size: 33em; }
```

## 5. Rhythm in UI

Product UI doesn't use a prose flow. Use the spacing scale and `gap`:

- **Group by proximity.** Label to its field 0.25–0.5rem, field to field 1–1.5rem, group to group 2–3rem. The ratio between levels matters more than the numbers.
- **Use `gap` in flex and grid**, not margins on children.
- **Trim half-leading** on text inside padded components with `text-box: trim-both cap alphabetic`, so padding looks equal above and below (`references/optical.md`).
- **Section headings in settings pages and forms** follow the same 2:1 rule as prose: more space above than below.

## 6. Mobile

- Reduce the large gaps, not the small ones. Paragraph gaps stay the same in `rlh`. Figure gaps drop from about 2.7× to 2× the paragraph gap (Anthropic: 64px → 48px).
- Keep the 2:1 heading ratio.
- Reading columns on phones run 40–55 characters at 16–18px. Don't shrink the body text to fit more.
- Side padding of at least 1rem, so hanging punctuation and markers have somewhere to go (`references/optical.md`).
