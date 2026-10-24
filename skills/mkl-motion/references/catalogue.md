# Reference catalogue (Oct 2026)

Study these; don't depend on them. **Runtime** says what you'd inherit if you copied code.

**Engines and platform**

| Name | URL | Use for | Note |
|---|---|---|---|
| Motion | motion.dev | The one JS engine | MIT; Motion+ is paid (one-time per developer on Solo; teams and Pro are yearly). v14 since Oct 2026 |
| React `<ViewTransition>` | react.dev/blog/2026/09/09/react-19-3 | Route and Suspense transitions | Stable in 19.3; DOM only |
| View Transitions API | developer.mozilla.org/docs/Web/API/View_Transition_API | Underlying platform | Same-document Baseline Oct 2025 |
| CSS entry animations | web.dev/blog/baseline-entry-animations | `@starting-style`, `allow-discrete` | Baseline 2024 |
| GSAP | gsap.com | Marketing-route exceptions only | Free incl. plugins since Apr 2025; custom licence, not MIT |

**Component collections, ordered from daily to showcase**

| Name | URL | Runtime | Steal | Caveat |
|---|---|---|---|---|
| Animate UI | animate-ui.com | Motion | Animated Radix/Base UI/React Aria primitives (dialog, tabs, tooltip): the daily chrome | v2 ships as an npm package; copy techniques, not the dependency |
| Motion UI | motion.dev/ui | Motion | Tokenised "feel" themes, MotionScore performance grading, a "calm" reduced-motion mode | Paid (Motion+) |
| Motion Primitives | motion-primitives.com | Motion | Morphing dialog (card → dialog via `layoutId`), text effects, infinite slider | MIT, still beta |
| Cult UI | cult-ui.com | Motion + Base UI | Dynamic Island, glowing "halo" form controls, shader heroes | Some pieces are niche |
| Smooth UI | smoothui.dev | Mostly Motion | Dynamic Island, Siri Orb, morph toggles, number flow | Leans showcase despite the name |
| React Bits | reactbits.dev | Varies: Motion, GSAP, three | Text effects, Code Slots (the slot-fill source), creative backgrounds | MIT + Commons Clause; check every component's deps |
| Fancy Components | fancycomponents.dev | Motion (+ physics lib in places) | Typography play: variable-font hover, text rotate, scramble, physics text | Activity not re-verified |
| Aceternity UI | ui.aceternity.com | Motion | Spotlight, lit borders, parallax, 3D cards, beams | Often lacks reduced-motion support; free + paid |
| Skiper UI | skiper-ui.com | Motion + GSAP | The most polished per component of the paid kits | Paid; attribution on free items; two runtimes, so mine only |
| Paper Shaders | github.com/paper-design/shaders | Its own WebGL | Mesh gradients, grain, liquid metal as React components | The one acceptable showcase dependency, isolated |

Skipped as redundant: Magic UI (Aceternity does it with more flair), Kokonut, Eldora, Syntax, Animata, uiverse, Hover.dev.

**Specialists**

| Name | URL | Steal |
|---|---|---|
| Sonner | github.com/emilkowalski/sonner | Stacked, interruptible toasts; swipe out the way they came |
| Vaul | github.com/emilkowalski/vaul | Drawer drag thresholds and curve. The repo says it's unmaintained, so learn the technique and don't adopt it new |
| NumberFlow | number-flow.barvian.me | Per-digit rolling with stable widths (React/Vue/Svelte) |
| cmdk | github.com/dip/cmdk | Restraint: a high-frequency surface with almost no motion |

**Specs and writing**

| Source | URL | Take |
|---|---|---|
| Emil Kowalski | animations.dev · emilkowal.ski · emilkowal.ski/skill | Frequency rule, curves, review method; his published agent skill is the nearest template to this file |
| Rauno Freiberg | rauno.me · devouringdetails.com | Interaction details, gesture feel |
| Josh W. Comeau | joshwcomeau.com | Springs and CSS transitions explained |
| NN/g | nngroup.com/articles/animation-duration | 100–500ms range; exits shorter than entrances |
| Material 3 (Expressive) | m3.material.io/styles/motion/overview/how-it-works | Spatial vs effects springs |
| Apple WWDC23 "Animate with springs" | developer.apple.com/videos/play/wwdc2023/10158 | Duration and bounce parameters; caution above 0.4 bounce |
| IBM Carbon | carbondesignsystem.com/elements/motion/overview | Productive vs expressive registers; 70–700ms scale |
| Atlassian | atlassian.design/foundations/motion | Semantic motion tokens (e.g. `motion.popup.enter`) |
| Glyph Kit | glyph-kit.traykov.cc | Text-first figures and motion timelines (SKILL.md §9) |
| Benji Taylor, *Family Values* (2024) | benji.org/family-values | The essay behind Family's fluid feel: gradual revelation, "fly instead of teleport", selective emphasis, dynamic trays, text morphing |
| Rauno, Web Interface Guidelines | rauno.me/interfaces | Interaction rules, including no extraneous animation on frequent, low-novelty actions |
| Jhey Tompkins | codepen.io/jh3y | Pure-CSS motion experiments; the ceiling of what CSS alone can do |

**Inspiration and study hubs** (browse for ideas, then extract with SKILL.md §5b)

| Hub | URL | What's there | Caveat |
|---|---|---|---|
| Codrops Creative Hub | tympanus.net/codrops/hub | Open-source demos and tutorials with code; collections for typography, hover, cursor, state-to-state, scroll-driven, grids, WebGL | Mostly Three.js, GLSL and GSAP: showcase register, so study it rather than copy it. Typography, hover and state-to-state carry over to a CSS + Motion stack best |
| Design Spells | designspells.com | ~340 "spells": micro-interactions, transitions and easter eggs from real apps, tagged by type and app | Recordings, not code; use for the *why* and the choreography |
| 60fps | 60fps.design | Library of iOS and web app animations as native-frame-rate video, filterable by context | Its MCP server (shot search, motion breakdowns) is a paid add-on |
| Awwwards | awwwards.com | Award-site inspiration and curated UI-animation collections | Showcase register only; rarely shows how it was built |

**Tools**
- Linear easing generator (linear-easing-generator.netlify.app, by Jake Archibald and Adam Argyle): turns any JS easing or SVG curve into `linear()`. It's a GUI alternative to SKILL.md §4d.
- cubic-bezier.com: drag a curve and compare it against another while it plays.

**Neighbouring agent skills** (don't load them alongside this one; they overlap and their numbers differ slightly)
- Vercel's `web-animation-design` (github.com/vercel-labs/open-agents) and Emil's own skill are both based on *Animations on the Web*. This file already absorbs their rules, with a named vocabulary, the stack and the registers on top.
