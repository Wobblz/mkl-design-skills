# Sources and provenance

## Books (the canon)

| Book | Author | Take |
|---|---|---|
| *The Elements of Typographic Style* (1992, 4th ed. 2012) | Robert Bringhurst | The rules: measure, leading, tracking caps, small caps, figures, hanging punctuation, rhythm. Rutter's webtypography.net applies it to the web chapter by chapter |
| *The Form of the Book* (English ed. 1991) | Jan Tschichold | Page proportions and the margin canon (`references/size-measure-leading.md` §6) |
| *The New Typography* (1928) | Jan Tschichold | Asymmetric layout and hierarchy by space and weight |
| *Practical Typography* (online) | Matthew Butterick | Line length, line spacing, paragraph and heading space, characters. practicaltypography.com |
| *Web Typography* (2017) | Richard Rutter | The canon translated to CSS. webtypography.net is the free companion |
| *Detail in Typography* | Jost Hochuli | Letter, word and line spacing at the micro level |
| *Thinking with Type* | Ellen Lupton | Hierarchy and grids, a good primer |

*The Elements of Typographic Style* is often misattributed to Tschichold. It is Bringhurst's.

## Specs and support data

- CSS Fonts Level 4, CSS Text Level 3/4, CSS Inline Level 3 (`text-box-trim`), CSS Values (units): w3.org/TR.
- MDN (developer.mozilla.org) and its data, @mdn/browser-compat-data. This skill used version 8.1.7 (2026-10-22).
- web-features and webstatus.dev for Baseline status. This skill used web-features 3.43.0 (published 2026-10-15).
- caniuse.com, including its per-language hyphenation tables.
- WCAG 2.2 Understanding documents: 1.4.4 Resize Text, 1.4.8 Visual Presentation, 1.4.10 Reflow, 1.4.12 Text Spacing.
- Microsoft's OpenType feature registry, for what each feature tag means.

## Practitioners and articles

| Source | Take |
|---|---|
| Tim Brown, "More Meaningful Typography" (A List Apart, 2011) | Modular scales |
| Utopia (utopia.fyi), Trys Mudford and James Gilyead | Fluid type and space scales; the `clamp()` formula |
| Maxwell Barvian, "Addressing Accessibility Concerns With Using Fluid Type" (Smashing, Nov 2023), and fluid.style | The 2.5× rule for zoom-safe fluid type |
| Adrian Roselli, "Responsive Type and Zoom" (updated Oct 2025) | Fluid type failures and the 2× cap rule |
| rsms.me/inter, and the archived Inter 3 dynamic metrics page (d.rsms.me/inter-website/v3/dynmetrics/) | Inter's features and its tracking formula |
| WebKit blog: "Better typography with text-wrap pretty" (2025), line-height units | `pretty` in Safari; `lh` units |
| Chrome for Developers: `text-wrap: pretty`, `text-box-trim` (2025), font fallbacks | Chrome behaviour; fallback metric overrides |
| web.dev, font best practices | `font-display`, preload, subsetting |
| Every Layout, "The Stack"; Andy Bell, flow utility (Piccalilli) | `* + *` spacing |
| Vincent Bernat, "CSS & vertical rhythm" (Apr 2026) | `rlh`-based rhythm |
| Zell Liew, on vertical rhythm | Paragraph gap below one line |
| Krista Radoeva, "Cyrillic script variations and the importance of localisation" (MyFonts) | Bulgarian versus Russian forms |
| Martin Metodiev, "Bulgarian Cyrillic on the web" (Medium, 2025) | Fonts and techniques for Bulgarian forms |
| github.com/nedyo/langbg | Bulgarian `locl` testing, Figma's missing language support |
| Adam Argyle, nerdy.dev (Nov 2025); CSS-Tricks, "Dark mode and variable fonts" (2020) | Grade and weight in dark mode |
| Typeset (npm `typeset`) | Build-time hanging punctuation, optical margin values, soft hyphens |
| ModernCSS, "Container Query Units and Fluid Typography"; web.dev, container queries in action | `cqi` type with a `rem` term; containers resolve against the nearest ancestor |
| MDN, `<meta name="text-scale">`; Josh Tumath, "Let's fix the web's text size" (Jul 2026) | OS text scaling on the web, and its Chromium-only support |
| MDN, `forced-colors` | Which properties are forced, backplates, `forced-color-adjust` |
| Satori README (vercel/satori, Oct 2026) | What `next/og` supports: default instance only for variable fonts, `textWrap` limits, locales |
| MDN, MathML fonts guide; MathML Core (W3C CR) | Math fonts with a MATH table; native MathML in all engines |

## Measured sites (Oct 2026)

Spacing in `references/rhythm.md` comes from live measurement on 2026-10-22 with Playwright and Chromium at 1440px and 390px, one or two long articles per site:
- **News and magazines:** The Guardian (an opinion column and a sectioned explainer), The New Yorker (two magazine features).
- **Research and brand blogs:** anthropic.com research, openai.com (two posts), distill.pub, transformer-circuits.pub.
- **Essays and newsletters:** Works in Progress (two essays), Every, Substack (Astral Codex Ten, Noahpinion), Craig Mod, The Pudding, Practical Typography (desktop only; the mobile run timed out).
- **Read from source code, earlier:** Tufte CSS, FT Origami, arXiv HTML (ar5iv-css), gwern.net.

Not measured: NYT (DataDome bot wall), Bloomberg (PerimeterX bot wall), Medium (Cloudflare challenge) and the FT (paywall; only the subscribe page renders). The New Yorker's mobile run hit its metered paywall partway through the article, so its mobile figures cover the opening only. Stripe Press publishes books rather than articles and was skipped.

## Tools

- **Font inspection:** Wakamai Fondue (wakamaifondue.com), FontDrop (fontdrop.info), FontGauntlet (fontgauntlet.com), fontTools (`ttx`, `pyftsubset`).
- **Scales:** Utopia (utopia.fyi), fluid.style/type. Also popular, not re-checked: typescale.com, modularscale.com, fluid-type-scale.com.
- **Fallback metrics:** Capsize (seek-oss/capsize), fontaine (unjs/fontaine), `next/font`.
- **Text spacing test:** the WCAG 1.4.12 text-spacing bookmarklet (Steve Faulkner's is the usual one).

## Neighbouring agent skills (Oct 2026)

About fifteen agent skills or rule sets touch typography. They're useful, but none covers optical letter alignment, cross-browser hanging bullets and quotes, `lang`/`locl` with Cyrillic forms, `@font-feature-values`, or measured editorial spacing.

- **Impeccable `typeset`** (pbakaus/impeccable): directional critique plus a detector script. Complements this skill's review; don't load both for the same edit, as their dark-mode advice conflicts (it says add weight).
- **Anthropic `frontend-design`:** names Bringhurst but gives no type CSS.
- **Vercel Web Interface Guidelines, Rauno's interfaces:** curly quotes, tabular figures, `balance`/`pretty`, ellipsis. Absorbed here.
- **Community typography skills** (simongonzalezdc `web-typography`, profpowell `vanilla-breeze`, petekp, mblode `typography-audit`, ehmo `typecraft-guide`): real CSS for scales and features, but several state stale support (`text-wrap: pretty` in Firefox, `hyphenate-limit-lines`), claim `hanging-punctuation` hangs bullets, or set `font-feature-settings` globally. Borrowed from them: mblode's rule to confirm the font ships a feature before flagging it, and to give a location for every finding; simongonzalezdc's decision order.

## Still unverified (Oct 2026)

Carry these as unverified until checked:
- Bringhurst's classical size scale, against the book.
- The `text-wrap: balance` line limit in Chromium (sources say 4 or 6).
- Whether `next/font/google` serves the same feature-stripped files as the Google Fonts API (very likely, since it uses the API; not tested directly). Google-served files were checked: `locl` kept, stylistic sets and small caps stripped.
- Bulgarian quote, number and date conventions against an official source (BAS Institute for Bulgarian Language).
- Bulgarian forms in fonts not listed in `references/language.md`.
- Whether an explicit `line-height` removes vertical font-swap shift in Safari.

## Provenance

- **Research:** a deep-research pass on 2026-10-22 covering the canon, editorial spacing, type scales, OpenType and `lang`, line breaking and optical alignment, font loading and accessibility, and existing agent skills. Support data from @mdn/browser-compat-data 8.1.7 and web-features 3.43.0, spot-checked again while drafting.
- **Scope:** shaped with the author: rules over catalogues (no font lists, no pairing guide), CSS-first with small dependency-free helpers, Bulgarian as a first-class case.
- Facts that change over time (browser support, tool versions) are marked Oct 2026. Re-check them when they matter.
