# UI text and tables

Product UI is read in glances, not paragraphs. The goals are scanning, stable layout and numbers you can compare.

## 1. Roles

- **Name roles by job**, not size: `label`, `body`, `caption`, `title`, `metric`, `code`. A role is size + line-height + weight + tracking (+ figures).
- **Few roles, clear steps.** Adjacent roles must differ visibly in size or weight; 13px and 14px with the same weight is not a hierarchy.
- **Body 14–16px, labels 12–14px.** 12px and below only for metadata, never for anything the user must act on. Keep small text at weight 400 or more.
- **Line-height 1.4–1.45 for UI body**, 1.25–1.3 for tables and compact UI, 1.2 for single-line controls.
- **Sentence case for labels and buttons.** Title Case reads as shouting in UI and breaks across languages.
- **Caps labels (eyebrows, table headers, tags):** use `text-transform: uppercase` on lowercase source text, track +0.06–0.1em, and add `"case" 1` so punctuation sits at cap height. Keep them short.

## 2. Mixing families in UI

When a product needs a second family for code, data or headings:

- **Prefer the family's own relatives.** Many families ship a mono, a serif or condensed widths designed to sit together (same x-height, same proportions). They pair without tuning.
- **Otherwise match x-heights** with `font-size-adjust: from-font` (Baseline 2024) or an explicit value, so inline code doesn't look bigger or smaller than the text around it.
- **Use the width axis (`wdth`) or a condensed style** for dense tables and narrow sidebars instead of shrinking the size. Set it with `font-stretch` (for example `87.5%`), not `font-variation-settings`.

```css
code, kbd, samp { font-family: var(--font-mono); font-size-adjust: from-font; }
.table-dense    { font-stretch: 87.5%; }
```

## 3. Tables

Tables are where typography does the most work in UI.

**Figures and alignment:**
- **Every numeric column is `tabular-nums lining-nums`.** Without it, columns don't line up and sums can't be compared at a glance.
- **Right-align numbers, left-align text.** Align each column's header the same way as its data.
- **Keep the same number of decimals in a column.** Format with `Intl.NumberFormat` and `minimumFractionDigits` / `maximumFractionDigits`.
- **Decimal alignment:** `text-align: "."` is in the spec but no browser ships it (Oct 2026). With tabular figures, right alignment and fixed decimals, the points line up on their own. For mixed precision, split integer and fraction into two cells, or pad with U+2007 FIGURE SPACE, which is exactly one tabular digit wide.
- **Units go in the header** ("Price, €" or "Size (MB)"), not repeated in every cell. When a unit must be in the cell, keep it attached with a no-break space.
- **Negative numbers use the real minus sign** U+2212 (−), which matches the width of +. `Intl.NumberFormat` already outputs it in some locales; check.
- **Thousands separators:** use the locale's. In tables for locales that group with a space (Bulgarian, French and others), use U+2007 or U+202F so digits stay aligned and groups don't break across lines.

**Rows and spacing:**
- Row padding 0.5–0.75rem vertical for comfortable tables; 0.25–0.375rem for dense ones. Line-height 1.25–1.3.
- **Use horizontal rules or zebra striping, not both.** Thin rules (1px at reduced contrast) separate rows; vertical rules are rarely needed when alignment is right.
- **Headers:** a weight step or small caps-style labels, not a bigger size. Sticky headers on long tables.
- **Wide tables scroll inside their own box** (`overflow-x: auto`) with the first column sticky, never the page.
- **Wrap long text cells**; truncate only identifiers, and provide the full value in a tooltip or expandable cell.

```css
table           { font-variant-numeric: tabular-nums lining-nums; border-collapse: collapse; }
th, td          { padding-block: 0.5rem; padding-inline: 0.75rem; line-height: 1.3; }
:is(th, td).num { text-align: end; }
th              { font-weight: 600; text-align: start; }
th.num          { text-align: end; }
tbody tr + tr   { border-block-start: 1px solid var(--rule); }
```

## 4. Numbers that change

- **Timers, counters, prices, progress values, live metrics:** tabular figures, so the text doesn't jitter as digits change.
- **Reserve width** for the longest value with `min-inline-size` in `ch` (here `ch` is exactly right, because tabular digits share the width of "0").
- **Don't switch to a monospace font** to get stable numbers. Tabular figures in the UI font do it without changing the look.
- **Animated numbers** (rolling digits): see mkl-motion. They need tabular figures too.

```css
.metric { font-variant-numeric: tabular-nums; min-inline-size: 7ch; text-align: end; }
```

## 5. Buttons, badges, chips

- **Trim half-leading** so the label looks centred with equal padding: `text-box: trim-both cap alphabetic` (Chrome 133, Safari 18.2, Firefox 154). Older browsers keep normal leading, which is harmless.
- **Icons sized to the cap height** (`height: 1cap`) line up with the label (`references/optical.md`).
- **One line, no hyphenation, no wrapping** for button labels: `white-space: nowrap`. Design the button to fit the longest translation instead.

## 6. Truncation

- **Single line:** `overflow: hidden; text-overflow: ellipsis; white-space: nowrap`, with the full text available (tooltip, `title`, expand, or a detail view). Ellipsis truncation with no way to reveal the text fails WCAG 1.4.12 under the text-spacing override.
- **Multi-line:** `display: -webkit-box; -webkit-box-orient: vertical; -webkit-line-clamp: 3; overflow: hidden`, which works in all three engines despite the prefix, plus a "more" control. Unprefixed `line-clamp` is only in Safari Technology Preview (Oct 2026).
- **Never truncate** prices, totals, dates, or anything the user must compare.
- **Truncate in the middle** for file names and paths where the end matters (do it in JS; CSS can't).
- **No fixed heights** on text containers. Let them grow.

## 7. Form text

- **Labels above fields**, 0.25–0.5rem gap, in the label role. Placeholders are not labels.
- **Input text at 16px or more on mobile**, or iOS Safari zooms the page on focus.
- **Numeric inputs:** tabular figures, right-aligned when they sit in a column, `inputmode="decimal"` for the keyboard.
- **Help and error text** in the caption role, directly under the field, at the same left edge.
