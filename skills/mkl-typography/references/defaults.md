# Defaults to copy

These come from Mike's shipped apps, gh-dashboard (`app/globals.css`, `app/layout.tsx`) and yesterday (`app/globals.css`, `app/layout.tsx`). Copy them into a project with no type system yet, then rename tokens to fit the project. Keep the comments: they record why each choice was made, so a later edit doesn't quietly undo it.

## Fonts (`app/layout.tsx`)

```tsx
import { Geist, Geist_Mono, Playfair_Display } from "next/font/google";

// UI text: a neutral, modern grotesque that stays out of the way of the data and its colours.
const geist = Geist({ variable: "--font-geist", subsets: ["latin", "latin-ext", "cyrillic"] });

// Numbers in dense places (or code) only. Only digits are drawn in it, so only
// the Latin file, and not preloaded: the sans every line uses comes first.
const geistMono = Geist_Mono({ variable: "--font-geist-mono", subsets: ["latin"], preload: false });

// Display only: the wordmark, page titles, the big date. One weight, with a Cyrillic cut.
const displaySerif = Playfair_Display({
  variable: "--font-display-serif",
  subsets: ["latin", "latin-ext", "cyrillic"],
  weight: "400",
  style: "normal",
});

// <html lang={INTL_LOCALE[locale]} className={`${geist.variable} ${geistMono.variable} ${displaySerif.variable}`}>
```

Leave out the serif when the product has no personal moments. gh-dashboard has none and uses Geist alone.

## Tokens (`app/globals.css`, Tailwind v4)

```css
@import "tailwindcss";

/*
 * Type: one sans for everything, figures included. A 1.25 scale on a 15px
 * body; each step carries its size, line-height and tracking. Figures are
 * proportional in sentences and the big numbers, tabular where they line up
 * or tick over. Mono is for data or code only. Spacing on a 4px grid.
 */
@theme {
  --font-sans: var(--font-geist), ui-sans-serif, system-ui, sans-serif;
  --font-mono: var(--font-geist-mono), ui-monospace, monospace;
  --font-serif: var(--font-display-serif);

  /* Below Tailwind's own steps: labels on dense charts and calendar squares only. */
  --text-4xs: 0.5625rem;
  --text-3xs: 0.625rem;
  --text-2xs: 0.6875rem;

  --text-label: 0.75rem;
  --text-label--line-height: 1rem;
  --text-small: 0.8125rem;
  --text-small--line-height: 1.25rem;
  --text-body: 0.9375rem;
  --text-body--line-height: 1.5rem;
  --text-lead: 1.0625rem;
  --text-lead--line-height: 1.625rem;
  --text-title: 1.25rem;
  --text-title--line-height: 1.625rem;
  --text-title--letter-spacing: -0.015em;
  --text-heading: 1.5rem;
  --text-heading--line-height: 1.875rem;
  --text-heading--letter-spacing: -0.025em;
  --text-figure: 1.875rem;
  --text-figure--line-height: 2.125rem;
  --text-figure--letter-spacing: -0.02em;

  /*
   * Spacing: one named step per kind of relationship, on a 4px grid, so the
   * same relationship is spaced the same everywhere. A raw number only inside
   * a component's own drawing (a badge, a chart), never between blocks.
   *   hint     4   a heading and the line that explains it
   *   inline   8   side-by-side controls; a small label and what it labels
   *   stack   12   blocks inside a card; items in a list; an icon and its text
   *   row     16   a label and the control across from it
   *   title   16   a card's heading and the content below
   *   section 16   card to card (a ruled single-sheet layout uses 48–72 instead)
   *   card    20   inside a card (24 from 640px)
   *   gutter  20   the page's sides (40 from 768px on desktop layouts)
   *   page    24   a page's title and its first card
   *   stage   32   between the parts of a page standing on its own
   * Marketing pages breathe on a larger, raw rhythm on purpose.
   */
  --spacing-hint: 0.25rem;
  --spacing-inline: 0.5rem;
  --spacing-stack: 0.75rem;
  --spacing-row: 1rem;
  --spacing-title: 1rem;
  --spacing-section: 1rem;
  --spacing-card: 1.25rem;
  --spacing-gutter: 1.25rem;
  --spacing-page: 1.5rem;
  --spacing-stage: 2rem;
}

@media (min-width: 40rem) {
  :root { --spacing-card: 1.5rem; }
}

/* Light on dark reads heavier, so medium and semibold come down 50. Body stays at 400. */
:root[data-theme="dark"] {
  --font-weight-medium: 450;
  --font-weight-semibold: 550;
}

html {
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

body {
  font-family: var(--font-sans);
  font-synthesis: none;
}

::selection { background: var(--fg); color: var(--canvas); }

@layer base {
  h1, h2, h3 { text-wrap: balance; }
  p { text-wrap: pretty; }
  a { text-underline-offset: 0.2em; text-decoration-thickness: 1px; }
  /* The display serif draws old-style figures by default; dates in titles read better on the line. */
  .font-serif { font-variant-numeric: lining-nums; }
}

/*
 * Numbers come in two voices, and only two:
 * - `figure` for data (ratings, deltas, axis ticks, calendar dates): mono, tabular.
 * - `nums` for a count inside a sentence: the text face with tabular digits.
 *   Lining too, or on the serif tabular-nums alone would bring back old-style figures.
 */
@utility figure { font-family: var(--font-mono); font-variant-numeric: tabular-nums; }
@utility nums { font-variant-numeric: lining-nums tabular-nums; }

/*
 * The display figure: proportional digits, tight, heavy enough to lead.
 * 52px on a phone to 88px from 1200px wide; the rem term keeps it growing
 * when the page is zoomed.
 */
@utility display {
  font-size: clamp(3.25rem, 1.75rem + 5vw, 5.5rem);
  line-height: 0.95;
  letter-spacing: -0.04em;
  font-weight: var(--font-weight-semibold, 600);
  font-variant-numeric: proportional-nums;
}

/* A section's first line: its name, set as a heading, with no label above it. */
@utility section-title {
  font-size: var(--text-title);
  line-height: var(--text-title--line-height);
  letter-spacing: var(--text-title--letter-spacing);
  font-weight: var(--font-weight-medium, 500);
}

/* Small column headings and axis text. */
@utility col-label {
  font-size: var(--text-label);
  line-height: var(--text-label--line-height);
  color: var(--faint);
  font-weight: var(--font-weight-medium, 500);
}
```

## Display serif in use (yesterday)

- Page titles: `font-serif text-3xl tracking-tight`, or `leading-tight` when it wraps.
- The big date or hero number: `font-serif text-5xl leading-none tracking-tight`, up to `text-[6rem]` on a single-moment screen.
- Wordmark: the serif's italic, on the landing and sign-in pages only.
- Never for body, labels or buttons.
