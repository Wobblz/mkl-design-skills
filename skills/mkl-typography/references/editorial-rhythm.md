# Editorial rhythm (measured)

Use this for a long-form column: an article, docs, a research page, a review or recap written as prose. Product UI uses the spacing tokens in `defaults.md` instead.

The numbers below are not from a textbook. They were measured live on 2026-10-22 (raw data in the project files under `typography/measurements/2026-10-22/`). Spacing is a multiple of the body line-height (`rlh`), placed on the start of the element that follows.

## 1. What good editorial sites actually do

Measured live on 2026-10-22 with Playwright and Chromium at 1440px and 390px widths, one or two long articles per site. Gaps are box to box, so they include half-leading, and are given in body lines (gap ÷ body line-height). NYT, Bloomberg and Medium served bot walls and the FT served its paywall, so they are not in the table.

| Site | Body size / line-height (desktop → mobile) | Measure, desktop | Paragraph gap | Above ÷ below heading | Figure gap ÷ paragraph gap | End of article |
|---|---|---|---|---|---|---|
| The Guardian | 17px / 1.4, same on mobile | 620px, ~75 ch | 0.5 lines | h2: rule + 1.1 lines above, ~0 below | — | 1.0 line |
| The New Yorker | 21px / 1.5, same on mobile | 640px, ~74 ch | 0.5 lines | no subheads | 3.0 (1.5 lines) | 4 lines |
| Practical Typography | 21.8px / 1.45 | 652px, ~74 ch | 0.7 lines | no subheads | — | — |
| Distill, Transformer Circuits | 17 → 14px / 1.7 → 1.6 | 704px, ~85 ch | 0.6 lines | h3: 57 / 20 = 2.85; h2 starts a section after a rule (152 / 24) | 2.5 | 3.5–6 lines |
| Works in Progress | 18px / 1.5, same on mobile | 728px, ~85 ch | 0.75 lines | h3: 50 / 20 = 2.5 | 1.5 | — |
| Every | 20 → 18px / 1.5 | 736px, ~83 ch | 0.67 lines | h2: 30 / 12 = 2.5 | 1.0 above, 3.5 below | — |
| Substack (Astral Codex Ten, Noahpinion) | 19 → 17px / 1.6 | 728px, ~82–87 ch | 0.66 lines | h2: 31 / 19 = 1.6 | 1.6 | 1.7 lines |
| OpenAI | 17px / 1.65, same on mobile | 676px, ~90 ch | 0.86 lines | h2: 64 / 24 = 2.7 | 2.7 above, 3.7 below | 2.3 lines |
| Anthropic research | 16.4 → 15px / 1.53 | 624px, ~85–90 ch | 0.96 lines | h3: 48 / 24 = 2.0 | 2.7 desktop, 2.0 mobile | 3.8 lines |
| Craig Mod | 20 → 17.6px / 1.5 | 746px, ~85 ch | 1.0 line | no subheads | 0.5 | 2.2 lines |
| The Pudding | 20 → 18px / 1.55 | 650px, ~56 ch | 1.0 line | h2: 80 / 20 = 4.0; h3: 32 / 12 = 2.7 | — | 3.9 lines |

What they share:

- **Paragraph gap: 0.5–1.0 × the body line-height, median about 0.7.** News and magazine sites sit at the tight end (Guardian, New Yorker 0.5), newsletters and essays in the middle (Substack, Every, Butterick, Works in Progress 0.66–0.75), brand research blogs at the loose end (OpenAI, Anthropic, Craig Mod, Pudding 0.86–1.0). Only gwern.net, among sites examined, indents paragraphs (2.5em) instead.
- **Space above a heading is 2–3× the space below it, median 2.5.** Six of eight measured heading levels fall between 2.0 and 2.85. Substack's default (1.6) and the Pudding's h2 (4.0) are the outliers, and the Guardian replaces space with a rule above its h2s. The heading binds to its section either way.
- **In absolute terms, about 2 lines above a heading and 0.65–0.85 lines below** (OpenAI 2.3 / 0.86, Distill 2.0 / 0.7, Anthropic 1.9 / 0.96, Works in Progress 1.85 / 0.74, Pudding 2.6 / 0.65). Every and Substack go tighter, about 1 line above.
- **Figures get 1.5–3× the paragraph gap.** Brand and research sites sit at 2.5–2.7; newsletters at 1–1.6. Several sites give more space below a figure than above it (OpenAI, Every), because the caption ends the interruption.
- **Captions are 0.75–0.85 × the body size** (Distill 0.77, Substack 0.74, OpenAI 0.82) and sit 0.25–0.65 lines below the image. Anthropic keeps captions at body size in its sans.
- **Blockquotes are spaced like paragraphs on newsletters** (Substack, Craig Mod) and like figures on magazines (New Yorker 1.5 lines).
- **List items nearly touch on most sites: 0.25–0.3 lines** (Substack, OpenAI, Pudding, Transformer Circuits), some closer to 0.1 (Every, Distill). Butterick spaces items like paragraphs. The list as a whole takes the paragraph gap before and after.
- **The end of an article gets 2–4 lines**, more on research sites (Distill up to 6). The Guardian is the exception at one line, because its tag list follows directly.
- **Desktop measures run long: 74–90 characters.** The three sites at 74–75 (Guardian, New Yorker, Butterick) are the classic print-led ones; tech and research sites run 83–90 with looser leading (1.5–1.7). Only the Pudding stays near the textbook 56. Measure and leading are one decision.
- **On phones, half the sites drop body size by 1–3px and half keep it.** Mobile measures land at 35–51 characters. Spacing in px stays fixed, so in line terms it grows slightly as the type shrinks.

## 2. The spacing table

Express every gap in `rlh` (the root element's line-height), so spacing follows the body leading even inside a heading with its own tighter line-height. **`1rlh` equals one body line only when the root's font-size and line-height match the body text.** If body text is 18px, set `html { font-size: 112.5% }` (a percentage, so user font settings still scale it) and size everything else in `rem`, rather than setting 18px on `.prose` alone.

| Between | Gap | Why |
|---|---|---|
| Paragraph → paragraph | 0.5–1.0 rlh (default 0.75) | Clearly a new thought, still one text. Measured median 0.7; news sites 0.5, research blogs up to 1.0 |
| Paragraph → paragraph, indent model | 0, with `text-indent: 1–1.5em` | The indent marks the break. Never indent the first paragraph after a heading or break |
| Anything → h2 | 2 rlh (1.5–2.5; ≈ 2–3 × the gap below it) | Separates sections. Measured median about 2 lines above, ratio 2.5 |
| Anything → h3 | 1.25 rlh | Weaker break than h2 |
| h2 → h3 directly | 0.5 rlh | They belong together |
| h2 → its first paragraph | 0.75 rlh (≤ 1 × paragraph gap) | Binds the heading to its text; above : below ≈ 2.5 : 1 |
| h3 → its first paragraph | 0.5 rlh | Same 2–2.5 : 1 ratio |
| Title → standfirst / dek | 0.5 rlh | One unit |
| Standfirst → byline / meta | 1 rlh | |
| Meta → first paragraph | 1.5–2 rlh | Start of the text proper |
| Paragraph → list, list → paragraph | Paragraph gap | A list is part of the flow |
| List item → list item | 0.25 rlh (tight) or paragraph gap (when items are sentences) | Choose one school per site. Most measured sites use the tight one |
| Nested list | 0.25 rlh above | |
| Paragraph → figure, figure → paragraph | 2 rlh (1–2.5; ≈ 1.5–3 × paragraph gap) | An interruption needs air. Brand and research sites 2.5–2.7 × the paragraph gap, newsletters about 1.5 × |
| Figure image → caption | 0.25–0.65 rlh | Caption belongs to the image |
| Paragraph → blockquote / pull quote / code / table / hr | 1–2 rlh | A quoted paragraph inside an essay can take the paragraph gap (Substack, Craig Mod) |
| Section break (`hr`, asterism ⁂ or space) | 2–3 rlh total | A pause, not a new section |
| Last paragraph → end of article | 3–4 rlh | Ends the piece clearly. Measured 2–4 lines, research sites more |
| Footnotes / endnotes block | 3 rlh above, notes 0.25–0.5 rlh apart | Separate apparatus |
| First child of the article | 0 above | The container's padding handles it |

## 3. The CSS

Production sites put the margin on the *start* of the element that follows another (`* + *`), not on both sides. This avoids margin collapsing surprises and lets each relationship be targeted.

```css
:root { font-size: 112.5%; line-height: 1.55; }   /* root = body text (18px by default), so 1rlh = one body line */

.prose > *                   { --flow: initial; margin-block: 0; }  /* reset UA margins; stop nested .prose inheriting --flow */
.prose > * + *               { margin-block-start: var(--flow, 0.75rlh); }
.prose > h2                  { --flow: 2rlh; }
.prose > :is(h3, h4)         { --flow: 1.25rlh; }
.prose > h2 + *              { --flow: 0.75rlh; }
.prose > :is(h3, h4) + *     { --flow: 0.5rlh; }
.prose > h2 + h3             { --flow: 0.5rlh; }

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
- **`text-box-trim` belongs to components, not prose.** Use it on cards, callouts and buttons. None of the measured sites trims article text.

Tailwind v4: put the flow rules in a `@layer components` block for `.prose`, or set `--flow` per element with arbitrary properties. The official typography plugin uses em-based margins on both sides; if the project uses it, override its spacing with the table above instead of fighting it element by element.
