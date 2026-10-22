# Emphasis, code and maths in prose

Three kinds of text that interrupt reading text and need their own rules. Spacing around them is in `references/rhythm.md`. Inline code's family and x-height matching are in `references/ui-and-tables.md` §2.

## 1. Emphasis

Bringhurst's advice is to change as little as possible: one level of emphasis inside reading text, usually italic. Bold is for scanning: UI, key terms a reader hunts for in docs, warnings.

- **Italic for stress in prose; bold for things to find.** Never both at once, never underline (on the web an underline means a link), never colour alone (it disappears in forced colours and fails WCAG 1.4.1).
- **Emphasis inside italic is roman.** `em em, blockquote em, i em { font-style: normal; }` when the surrounding text is italic.
- **Inside a bold heading**, emphasis is italic or nothing.
- **Bold must look bold.** Body 400 against 500 doesn't read as emphasis; use 600–700 against 400. Light-on-dark text needs the same gap after the dark-mode weight drop (`references/fonts.md` §3).
- **No all-caps or letter-spaced emphasis** in running text. Capitals for acronyms belong in small caps (`references/opentype.md` §4).
- **Load the real italic and bold files.** Faux styles are covered by `font-synthesis` (`references/opentype.md` §4).

**Pick the element by meaning, then style it.** The styles can match; the semantics can't be swapped.

| Element | Means | Default style |
|---|---|---|
| `<em>` | Stress that changes the sentence's meaning | Italic |
| `<strong>` | Importance, seriousness, urgency | Bold (600–700) |
| `<i>` | Different voice: foreign words (with `lang`), technical terms, ship names, thoughts | Italic |
| `<b>` | Draw attention without importance: keywords, lead-ins | Bold, or small caps for a lead-in |
| `<cite>` | Title of a work | Italic |

**Cyrillic italics are different letters.** Italic и, т, д, г and п take cursive shapes (и looks like a Latin u, т like an m), and Bulgarian `locl` only applies in italic if the italic file has it. Render italic and bold-italic Bulgarian with `lang="bg"` before choosing a font for a Bulgarian product.

## 2. Code blocks

Code isn't reflowed like prose: a line break can change meaning, so measure and wrapping work differently.

- **Size:** match the body's x-height with `font-size-adjust: from-font`, or set code around 0.875–0.9em. Line-height 1.4–1.5, slightly tighter than prose.
- **Measure:** 80–100 characters fits most code. Let blocks break out wider than the text column when the layout allows (`references/rhythm.md` §4).
- **Scroll by default:** `white-space: pre; overflow-x: auto`. Make the scroll container focusable (`tabindex="0"`) so keyboard users can scroll it. Wrap with `white-space: pre-wrap` only where wrapping can't change meaning: logs, prose-like config, terminal output.
- **`tab-size: 2`** (or the project's indent). Baseline everywhere.
- **No hyphenation, no `text-wrap: pretty`, no ligatures** unless the font is a deliberate programming-ligature face (`references/opentype.md` §3).
- **Line numbers come from CSS counters**, right-aligned in tabular figures, with `user-select: none` so copying the code skips them.
- **Inline code with a background:** use no vertical padding, so lines don't push apart, and `box-decoration-break: clone` (with `-webkit-` for Safari) so each wrapped piece keeps its padding and radius.

```css
pre {
  font-family: var(--font-mono); font-size-adjust: from-font;
  line-height: 1.45; tab-size: 2;
  white-space: pre; overflow-x: auto;
  font-variant-ligatures: none; hyphens: manual;
}
pre.wrap { white-space: pre-wrap; overflow-wrap: anywhere; }
:not(pre) > code {
  padding: 0 0.25em; border-radius: 0.25em;
  -webkit-box-decoration-break: clone; box-decoration-break: clone;
}
```

## 3. Maths

MathML renders natively in all three engines (Chrome 109+, Firefox, Safari), with screen-reader support. Use it as the output even when authors write TeX.

- **Author in TeX, ship MathML.** Convert at build time (Temml, KaTeX with `output: 'mathml'`, MathJax). Don't ship equations as images or SVG only: they can't be read aloud, zoomed or copied.
- **Use a font with an OpenType MATH table.** Stretchy brackets, radicals and sub/superscript positions come from it, not from CSS. `font-family: math` picks the system's math font (Chrome 109, Firefox 149, Safari 26.2): Cambria Math on Windows, STIX Two Math on macOS 13+, often nothing usable on Android. For consistent rendering, self-host one.
- **Match the body face.** Choose a math font whose colour and x-height sit with the text: a sibling if the family has one (Fira Sans with Fira Math), Latin Modern Math with Computer Modern-like serifs, STIX Two Math with Times-like serifs, Libertinus Math with Libertinus. Compare `x` and digits side by side at body size.
- **Inline maths must not open the leading.** Keep it at body size in compact style (`math-style: compact`, the inline default). Write inline fractions with a slash (a/b), not stacked.
- **Display maths:** `<math display="block">`, wrapped in a scroll container with `overflow-x: auto`. Never shrink a long equation to fit.
- **Equation numbers** come from CSS counters, set at the end of the line in tabular figures: `(2)`.

```css
@font-face { font-family: "Fira Math"; src: url(/fonts/FiraMath-Regular.woff2) format("woff2"); }
math { font-family: "Fira Math", math; }
.equation { overflow-x: auto; display: grid; grid-template-columns: 1fr auto; align-items: center; }
.equation::after { counter-increment: eq; content: "(" counter(eq) ")"; font-variant-numeric: tabular-nums; }
```
