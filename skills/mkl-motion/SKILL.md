---
name: mkl-motion
description: Motion design for React/Next.js products. Use when adding, changing or reviewing animation, transitions, micro-interactions, gestures, hero effects or glyph animation, or when asked to make UI feel slicker.
---

# Motion design

Motion here is a material, like type or colour. It has a small vocabulary, and the same kind of movement feels the same on every screen. Work from patterns, not from components. The libraries in §13 are places to study technique, not packages to install, because stacking two or three animation runtimes costs bundle size and makes motion hard to orchestrate.

The vocabulary in §4 and §7 was tuned by hand in shipped products. **Check the project first.** If it already has a motion vocabulary (a `motion.ts(x)` of named springs, motion tokens in the global CSS, or a motion section in its docs), use that and map this file's patterns onto its names. If it has none, start one from §4.

**Where to go:**
- **Building a moment:** §1 laws → §2 register → §3 stack → §4 tokens → §5a workflow → the matching pattern in §6, §7 or §8.
- **Borrowing from a library:** §5b, then §13 for where to look.
- **Reviewing existing motion:** §12 checklist, with §11 as the list of findings to look for.
- **Text-mode / ASCII / glyph work:** §9.

---

## 1. The laws

1. **No job, no motion.** Every animation does one of these jobs: *feedback* (your press registered), *orientation* (where this came from and where it went), *state change* (toggled, loaded, saved, failed), *attention* (look here, once) or *delight* (rare and earned). If you can't name the job, cut the animation.
2. **Frequency kills animation.** Anything used 100+ times a day, or triggered from the keyboard, is instant or at most a quick opacity change. A command palette, a keyboard shortcut or tab switching in a tool shouldn't make anyone wait. Save the craft for moments that happen once a day, like a daily check-in. Family calls this *selective emphasis*: how intense the delight is depends on how rarely the moment happens.
3. **Fast by default.** Daily UI settles in under 300ms. Exits run 20–30% faster than entrances, because the user has already moved on. Elements that move as a unit (modal and backdrop, tooltip and arrow, drawer and overlay) share one duration and curve, or they visibly come apart.
4. **Ease out on entry.** Things arriving decelerate into place. Ease-in is only for short exits (≤200ms), where the thing is leaving and the eye has let go of it. It never goes on an entrance or on anything the user is waiting to see.
5. **Nothing from nowhere; fly, don't teleport.** A popover grows from its trigger. A sheet comes from its edge. A toast leaves the way it came. Something that moves elsewhere travels there visibly: a pending item flies to the tab where it will live, and a card becomes the screen it opens. Surfaces start at scale 0.9–0.97, never 0. Data marks (bars, dots, a slot's fill) may grow from 0 because zero is their meaning and their container is already on screen.
6. **Springs for anything a hand can interrupt.** A spring retargets from its current velocity. A tween restarts from rest and visibly kinks. Use tweens for one-shot, non-interactive moves.
7. **Spatial things may overshoot; effects never do.** Position, size and shape can bounce a little. Opacity, colour, blur and *numbers* settle without overshoot, because a count that overshoots briefly shows a wrong value.
8. **Compositor only.** Animate `transform`, `opacity` and (carefully) `filter`/`clip-path`. Keep animated blur under ~20px, because larger blurs stutter, especially in Safari. Height to `auto` is the one accepted layout animation, and it stays short. Never use `transition: all`. Never run an infinite loop without an off-screen pause.
9. **Reduce, don't remove.** Under `prefers-reduced-motion`, movement turns into opacity and feedback stays. A save still confirms, but it fades instead of sweeping.
10. **Never gate content on animation.** Focus, data and interactivity are available at frame zero. Anything an animation reveals must be readable if JavaScript never runs.
11. **One engine.** CSS → React `<ViewTransition>` → Motion. No second animation runtime in product code (§3).
12. **Names, not numbers.** Every duration, curve and spring comes from the tokens (§4), named for what it moves. When a new kind of movement appears, add a named token with a one-line comment. Don't inline the numbers.

---

## 2. Pick the register

Every moment belongs to one register. Decide which one before writing code, because the budgets differ. Mixing them is how product UI starts to look like a Dribbble shot, or a landing page looks timid.

| | **Daily** (product UI) | **Showcase** (landing, hero, onboarding, year-in-review, share cards) | **Text-mode** (glyph/ASCII) |
|---|---|---|---|
| Where | Anything used repeatedly inside the app | Seen once per visit, or a deliberate ceremonial moment | Opt-in aesthetic: loaders, boot or decode sequences, terminal-styled heroes, text sparklines |
| Durations | 0–350ms (drawer up to 500ms) | 400–900ms per element; whole sequence ≤ ~1.5s | Stepped frames at 8–24fps; reveals ≤ ~800ms |
| Bounce | 0 on chrome; ≤0.25 on fills and gestures | ≤0.3 | None; the stepped cadence is the character |
| Cascades | Total ≤ ~400ms | Total ≤ ~1.2s | Left-to-right or row by row, total ≤ ~800ms |
| Allowed | Feedback, orientation, state | All of daily, plus cursor-tracked light, tilt, parallax, scroll-linked, text splits, shaders, marquees | Character swaps on a fixed grid |
| Must also | §10 rules | One hero moment per viewport; loops pause off-screen; a pause control if anything moves >5s; a static fallback for reduced motion; isolate to marketing routes | Fixed monospace grid; accessible text label; final frame for reduced motion |

Inside the app, a showcase moment needs a reason: a once-a-month review, a first-run moment, a celebration. A monthly or yearly recap is showcase. A product's one core interaction, such as a picker the user drags every day, stays daily-register but deserves the most craft.

---

## 3. The stack: one runtime

Reach for the lowest rung that can do the job.

**Rung 1: CSS (zero JS).**
- Hover, press, focus and colour: `transition` on named properties. Gate hover under `@media (hover: hover) and (pointer: fine)`.
- Enter and exit of popovers, dialogs and tooltips: `@starting-style` + `transition-behavior: allow-discrete` (Baseline since Aug 2024), or Radix/Base UI `data-state` and `data-starting-style` attributes.
- Data-mark cascades: keyframes with `animation-delay: calc(var(--i) * var(--step))` (e.g. `rise` and `pop` utilities). They need no JavaScript and run before hydration.
- Shimmer, spinners, marquees, progress bars.
- Spring shapes for non-interactive moves via `linear()` (§4d).
- `height: auto`: `interpolate-size: allow-keywords` is Chromium-only as of Oct 2026, so fall back to `grid-template-rows: 0fr → 1fr`.
- Scroll-driven (`animation-timeline: view()`): Firefox still keeps it behind a flag, so use it only inside `@supports`, with the finished state as the default.

**Rung 2: React `<ViewTransition>`.** Stable in React 19.3 (Sep 2026). It animates only updates made inside `startTransition`, Suspense reveals or `useDeferredValue`; a plain `setState` is ignored. Use it for route changes, page-scale filtering and reordering, Suspense skeleton → content, and shared-element morphs *between routes*. Use `addTransitionType` for direction (forward/back). Check the installed React version first, because 19.2 and earlier don't have it. Next.js wiring changes between versions, so read `node_modules/next/dist/docs/` before relying on memory. Same-document View Transitions have been Baseline since Oct 2025. Cross-document ones are Chrome/Safari only, so treat them as an enhancement.

**Rung 3: Motion (`motion/react`), the only JS engine.** Use it for gestures with velocity (drag, swipe, fling), interruptible springs, `layout`/`layoutId` with scale correction (pills, reorderable lists, card → dialog morphs), `AnimatePresence` exits, motion values driving styles without re-rendering React (`useMotionValue`, `useSpring`, `useTransform`, `useScroll`), and `animate()` for imperative sequences. Wrap the app in `<MotionConfig reducedMotion="user">`.

**Bundle discipline.**
- `LazyMotion` + `m.*` cuts Motion's initial cost to about 5kb, against roughly 34–43kb for the full `motion` component (Motion's own pages differ). It pays off when most routes need only `domAnimation`.
- An app that uses `layoutId` and `drag` everywhere needs `domMax` anyway, which shrinks the saving. Measure before migrating an existing app. Start new apps on `LazyMotion strict`.
- After adding any dependency, run a production build and confirm no second animation library came in transitively.

**Not in product code:**
- GSAP: free for commercial use since Apr 2025, but not MIT, ≈20–27kb core, and imperative. Only on an isolated, code-split marketing route that truly needs SplitText, MorphSVG or ScrollTrigger scrubbing.
- React Spring, Anime.js, Popmotion/Motion One (superseded by Motion), AutoAnimate (redundant).
- Lenis, Locomotive or any smooth-scroll hijacking.
- Lottie or Rive for UI chrome. They're fine for a designer-authored illustration.
- Whole registries installed wholesale.

**Porting a technique into the stack:**

| Seen in the source | Re-express as |
|---|---|
| `gsap.to(el, {y, opacity, ease: "power3.out"})` | CSS transition with `--ease-out`, or Motion `animate()` |
| GSAP timeline / `stagger` | Motion variants with `staggerChildren`, or `animate()` sequence with `stagger()` |
| ScrollTrigger scrub | `useScroll` + `useTransform`, or CSS `view()` inside `@supports` |
| ScrollTrigger "play once on enter" | `whileInView` with `viewport={{ once: true }}` |
| GSAP Flip | `layout`/`layoutId`, or `<ViewTransition>` across routes |
| SplitText | Split words yourself: `aria-label` on the parent, `aria-hidden` on the pieces, Motion stagger |
| MorphSVG | Paths with matching point counts, animate `d` with Motion; otherwise crossfade |
| react-spring `{tension, friction}` | Motion spring `{stiffness ≈ tension, damping ≈ friction}`, then rename it into a project token |
| CSS-only component with hard-coded ms/curves | Swap every literal for the nearest token |

---

## 4. Tokens

### 4a. CSS tokens (`app/globals.css`, Tailwind v4 `@theme` or `:root`)

```css
:root {
  /* Durations, named by size of change */
  --dur-instant: 0ms;     /* high-frequency actions; the 2nd+ tooltip in a scan */
  --dur-micro: 120ms;     /* press, toggle, small exits */
  --dur-fast: 150ms;      /* colour/hover, popover exit */
  --dur-base: 200ms;      /* popover/dropdown enter, tabs, small sheet exit */
  --dur-moderate: 280ms;  /* modal enter, card collapse, toast */
  --dur-slow: 350ms;      /* image settle, route crossfade: the daily cap */
  --dur-drawer: 500ms;    /* edge sheets opened without a drag */
  --dur-showcase: 550ms;  /* showcase rises; up to 900ms for line draws */

  /* Curves, named by job */
  --ease-out: cubic-bezier(0.22, 1, 0.36, 1);     /* default arrival, hairline draws, hover travel */
  --ease-in: cubic-bezier(0.4, 0, 1, 1);          /* short exits only (≤200ms) */
  --ease-in-out: cubic-bezier(0.65, 0, 0.35, 1);  /* travel that starts and ends at rest */
  --ease-standard: cubic-bezier(0.4, 0, 0.2, 1);  /* neutral collapse (height to 0) */
  --ease-drawer: cubic-bezier(0.32, 0.72, 0, 1);  /* iOS-like sheet, when no velocity */
  --ease-hover: ease;                             /* colour only */
  /* linear: progress, marquee, shimmer, scrubbing only */

  /* Cascades */
  --stagger: 45ms;        /* items in a list or row of slots */
  --stagger-dense: 3ms;   /* dozens to hundreds of data marks: reads as one sweep */
}
```

Choose the step from the count: `step ≈ budget / count`. Use a 400ms budget for daily and about 1.2s for showcase. Poster grids with about 30 cells use about 22ms; bar charts with 100+ bars use 3–8ms.

### 4b. Named springs (`components/motion.tsx`)

A reference set of springs, tuned by hand in shipped products. Each is named for what it moves. Copy them into a new project, or map them onto an existing project's names.

```ts
/** An element floating under a finger mid-gesture, with a slight elastic lag: near-critical. */
export const TRACK_SPRING = { type: "spring", stiffness: 900, damping: 42, mass: 0.5 } as const;
/** A small piece snapping into place: selected pill, switch knob, menu opening, tooltip following. */
export const SNAP_SPRING = { type: "spring", stiffness: 560, damping: 38, mass: 0.7 } as const;
/** Landing after release, with a felt overshoot: a dragged selection dropping into its slot. */
export const LAND_SPRING = { type: "spring", stiffness: 520, damping: 22, mass: 0.6 } as const;
/** A sheet, dialog or full-screen view arriving; snap-back after a cancelled drag. */
export const SHEET_SPRING = { type: "spring", stiffness: 420, damping: 36 } as const;
/** Things re-ordering among themselves (sorted cards, filtered rows). Same feel as SHEET. */
export const LAYOUT_SPRING = SHEET_SPRING;
/** A page in a paged deck (swipe or arrow keys): slightly overdamped, so a page never wobbles at rest. */
export const SLIDE_SPRING = { type: "spring", stiffness: 380, damping: 38, mass: 0.8 } as const;
/** A panel folding open under its trigger (height 0 → auto) and away again. Clip overflow. */
export const FOLD_SPRING = { type: "spring", stiffness: 380, damping: 36 } as const;
/** A card or block rising in as it arrives or scrolls into view: unhurried, no bounce. */
export const REVEAL_SPRING = { type: "spring", stiffness: 260, damping: 30 } as const;
/** A slot filling with its value: short, just enough bounce to feel placed. */
export const FILL_SPRING = { type: "spring", duration: 0.32, bounce: 0.22 } as const;
export const FILL_STAGGER = 0.045; // s between neighbouring slots
export const FILL_RISE = 6;        // px a value rises as it lands
/** A number counting to its value: overdamped on purpose, so it never shows a wrong number. */
export const COUNT_SPRING = { stiffness: 110, damping: 26, mass: 0.9 } as const; // for useSpring
```

How they behave (simulated, mass-spring, settle to within 0.1%):

| Spring | Damping ratio | Settles | Overshoot | Character |
|---|---|---|---|---|
| TRACK | 0.99 | ~255ms | 0 | Floats under the finger |
| SNAP | 0.96 | ~330ms | 0 | Crisp |
| LAND | 0.62 | ~390ms | ~8% | Placed, with a felt bounce |
| SHEET / LAYOUT | 0.88 | ~450ms | ~0.2% | Quick, settled |
| SLIDE | 1.09 | ~550ms | 0 | Heavy, calm page turn |
| FOLD | 0.92 | ~400ms | 0 | Even |
| REVEAL | 0.93 | ~490ms | 0 | Unhurried |
| COUNT | 1.31 | ~1.4s | 0 | Calm count |

Most of each settle happens in the first 60%, so perceived durations are shorter than the table.

### 4c. Adding a token

Only when no existing name describes the movement. Give it a name for what moves ("a toast stacking", not "medium bouncy") and a one-line comment. If it's a spring, write down its bounce intent: none, felt or playful. Bounce above 0.3 (damping ratio below about 0.6) is showcase-only, and above 0.4 is too much anywhere (Apple's WWDC23 guidance).

To specify by feel, use Motion's `{ type: "spring", visualDuration, bounce }`. To convert to physics: `stiffness ≈ (2π / duration)²` at mass 1, and damping ratio ≈ 1 − bounce.

### 4d. Springs in pure CSS (`linear()`, Baseline 2023)

Sample the spring and bake it into `linear()`. You keep the shape but lose velocity hand-off, so use this only for non-interactive moves:

```js
// node: prints { duration, easing } for a mass-spring from rest to 1
function springToLinear({ stiffness: k, damping: c, mass: m = 1 }, samples = 24) {
  const dt = 1 / 1000, pts = []; let x = 0, v = 0, t = 0, T = null;
  while (t < 3) { const a = (-k * (x - 1) - c * v) / m; v += a * dt; x += v * dt; pts.push(x); t += dt;
    if (T === null && Math.abs(x - 1) < 1e-3 && Math.abs(v) < 1e-2) T = t; }
  const stops = Array.from({ length: samples + 1 }, (_, i) => i === 0 ? 0 : i === samples ? 1
    : +pts[Math.min(pts.length - 1, Math.round((i * T / samples) * 1000))].toFixed(3));
  return { duration: Math.round(T * 1000) + "ms", easing: `linear(${stops.join(", ")})` };
}
// springToLinear({ stiffness: 520, damping: 22, mass: 0.6 }) → LAND as ~390ms linear(…)
```

---

## 5. Workflow

### 5a. Building a moment

1. **Register and job.** Is this daily, showcase or text-mode (§2)? What is its job, and how often does it fire? If the answer is "constantly" or "keyboard", stop at instant.
2. **Say it in one sentence first, as the code comment.** For example: *"'Saved', confirmed: a soft pill opens outward from its middle, then a check rises into it, a beat behind."* If the sentence is hard to write, the motion is unclear.
3. **For anything with more than one moving part, write a text timeline.** This is the Glyph Kit idea: a motion spec is readable plain text. Put it in the comment or PR so the choreography is reviewable before it exists:
   ```
   save · confirm
   0ms      ▸ save resolves (haptic: confirm)
   0–300    ▓▓▓▓▓▓    pill wash  clip-path inset(0 50%) → inset(0 0)   --ease-out
   200–520       ▓▓▓▓▓ check    y 5→0, scale .8→1, opacity 0→1      FILL_SPRING
   reduced  pill appears, check fades; no clip, no rise
   ```
4. **Lowest rung that can do it** (§3).
5. **Use tokens** (§4). Reuse a pattern from §6, §7 or §8 if one fits. Most moments are an existing pattern in a new place.
6. **Reduced-motion branch.** Decide what it becomes: a fade, a glow, the final frame, or instant. `MotionConfig reducedMotion="user"` already removes transform and layout animation in Motion. Add `useReducedMotion()` only where the fallback needs a different design (EdgeSweep only glows).
7. **Verify** (each takes seconds):
   - Interrupt test: click or toggle rapidly mid-flight.
   - 4× CPU throttle in DevTools with paint flashing on.
   - OS reduced-motion on.
   - Keyboard-only pass: focus lands correctly.
   - A phone: touch, haptics, no hover leakage.
   - Read it with JS disabled for showcase pages.

### 5b. Borrowing a technique (study, don't install)

When a component in a library is the right idea, extract its recipe instead of its code:

1. Read its source (the registry JSON or GitHub), not just the demo.
2. Fill in this card:
   ```
   source:      <library / component / url>
   job:         feedback | orientation | state | attention | delight
   trigger:     mount | hover | press | drag | in-view | scroll-progress | data change
   properties:  transform(x,y,scale,rotate) | opacity | clip-path | filter | layout | d
   timing:      duration+curve or spring (stiffness/damping/mass or duration/bounce)
   origin:      where it grows from / exits to
   choreography: stagger, delays, sequence
   exit:        mirror? faster? different?
   reduced:     what it does (often: nothing; you must add this)
   deps:        runtime(s) it pulls in (GSAP? three? a second icon lib?)
   ```
3. Rebuild it on the project's stack with the project's tokens. Drop its dependencies. Map its numbers onto the nearest named spring or curve. Only add a new token if nothing fits (§4c).
4. Credit the source in a comment (e.g. "slot fill after React Bits' Code Slots").

### 5c. Reviewing

Run §12 and report findings as a Before → After table, one row per problem, most severe first:

| # | Where | Before | After | Law |
|---|---|---|---|---|
| 1 | `popover.tsx:42` | `scale(0)`, 400ms `ease-in` | `scale(0.95)` from `var(--transform-origin)`, `SNAP_SPRING` | 4, 5 |
| 2 | `globals.css:88` | `transition: all 300ms` | `transition: transform var(--dur-fast) var(--ease-out)` | 8 |

The After column uses the project's tokens, never raw numbers. Keep it to the table plus at most one line of summary.

---

## 6. Daily patterns

| Moment | Technique | Numbers | Reduced motion |
|---|---|---|---|
| Button press | CSS `:active` scale | `scale(0.97)`, `--dur-micro`, `--ease-out` | Background shade only |
| Hover (row, card) | CSS, gated `(hover: hover)`. If the effect moves the element (lift, scale), put the transform on a child: moving the hovered box itself shifts the hit area under the pointer and it flickers | Background `--dur-fast` `ease`; lift ≤2px | Colour only |
| Link | Hairline draws from the left under the words (background-size); arrow leans toward its destination | Hairline 0→100% `0.32s --ease-out`; arrow `translate(1.5px, -1.5px)`; focus shows the same line | Line appears, no draw |
| Toggle / switch | Knob on `SNAP_SPRING`, or CSS transform 120–150ms | — | Instant knob, colour fade |
| Segmented / tabs / nav pill | Shared `layoutId` pill glides between options | `SNAP_SPRING` | Pill jumps |
| Tab content (directional) | New content slides in from the side of the tab you tapped; going back reverses it. Pass direction as `custom` to `AnimatePresence`, or use `addTransitionType` with `<ViewTransition>` | ±16–24px + crossfade, `SNAP_SPRING`; in a tool switched all day, crossfade only | Crossfade |
| Button label change (text morph) | "Continue" → "Confirm": letters shared by both words slide into their new places, the rest fade. One `layoutId` per letter-occurrence inside `AnimatePresence mode="popLayout"`; the button width animates with `layout` | `SNAP_SPRING`; ≤250ms | Crossfade the whole label |
| Dynamic tray | A compact sheet over the current screen; its height changes to show progress through a flow, and it can morph into a full screen (`layout` on the container, content swapped with `popLayout`). Title and icon double as back and dismiss | Height `SHEET_SPRING`; content swap ~150ms | Instant height, crossfade |
| Item goes somewhere | Something just created or sent flies to where it will live (a pending transaction to the Activity tab, a saved item to its list) via a shared `layoutId`, or a portal clone animating to the target's rect | `SHEET_SPRING`; target acknowledges with a pop | Target badge appears; no flight |
| Tooltip | Origin = trigger side; ~300–500ms open delay | 0.97→1 + opacity ~125ms; **0ms for the next tooltip while scanning** | Opacity |
| Dropdown / select / popover | Scale from `var(--transform-origin)` + small y toward the trigger | Enter 0.9→1, y ±6px, `SNAP_SPRING`; exit to 0.94, y ±4px, `0.12s --ease-in` | Opacity, 100ms |
| Modal / dialog | Centred (exempt from origin rule); backdrop fades; focus moves at frame 0 | 0.96→1 + opacity + 8px y, `SHEET_SPRING`; exit ~200ms | Opacity |
| Sheet / drawer (drag) | Pointer events → `dragY` motion value; rubber-band upward at ×0.2; dismiss past **120px or on a flick** (velocity >0.45px/ms still moving within the last 100ms) | Dismiss: `0.2s --ease-in` to its height; cancel: `SHEET_SPRING` back to 0; no drag: `--dur-drawer --ease-drawer` | Opacity or instant |
| Paged deck / carousel | `drag="x"`, constraints 0, `dragElastic: 0.25`; advance on **offset >60px or velocity >400px/s**; tap left third = back | Pages slide ±40% with `SLIDE_SPRING`; arrow keys mirror swipes | Crossfade |
| Toast | Enter from its edge, stack with offset and scale (Sonner), swipe out the way it came | ~250ms in, ~200ms out; stacked items offset 8–14px and scale −5% each | Opacity; still `aria-live` |
| Card that comes and goes | Rises in like Reveal; exit folds height **and the gap** so neighbours close up | Enter y 14→0 `REVEAL_SPRING`; exit `height 0, marginTop −gap, 0.28s --ease-standard` | Opacity; instant reflow |
| Disclosure / height auto | `AnimatePresence` + `FOLD` (`height 0→auto`, opacity), overflow clipped | `FOLD_SPRING` | Instant |
| List add / remove / reorder | `layout` + `AnimatePresence` (`popLayout`), or `<ViewTransition>` at page scale | `LAYOUT_SPRING` | Instant reflow, opacity on add |
| Route / page | `<ViewTransition>` with direction types; crossfade + 8–16px slide | 250–350ms; old view exits faster | Crossfade |
| Image arriving | Never pop in: blurred placeholder (thumbhash) or skeleton holds the slot; the image fades and settles | opacity 0→1, scale 1.04→1, `0.35s cubic-bezier(.2,.7,.2,1)`; over its own thumbnail, crossfade only; cached images skip | Fade only |
| Skeleton | Page-shaped block with one soft light sweeping across, so waiting reads as "arriving" | Sweep 1.4s easeInOut, repeatDelay 0.25 | Static block |
| Number change | Spring a motion value; **write to `textContent`, not React state**; once in view; `tabular-nums` | `COUNT_SPRING`; only on meaningful changes, not every poll | Instant value |
| Scroll reveal | `whileInView` once, margin −8% bottom | y 14→0 + opacity, `REVEAL_SPRING`; siblings stagger 50–100ms | Opacity or none |
| Haptic pairing (mobile) | Every gesture step ticks; release confirms; extreme values get a pattern | tick per row crossed; `confirm` on commit. Android: Vibration API. iOS Safari has never had it, but Safari 18 added a haptic to `<input type="checkbox" switch>`, so toggle a hidden one inside the gesture. Reported to stop firing from script in iOS 26.5, so treat it as best-effort and never as the only feedback | Haptics stay |

---

## 7. Signature patterns

These are distinctive moves from the reference vocabulary that give a product a recognisable feel. Reuse them before inventing new ones.

- **Slot fill** (from React Bits Code Slots). An empty dashed slot is already on screen. When a value lands, its colour grows out from the centre (`scale 0→1`, `FILL_SPRING`). The value rises `FILL_RISE` px into place 40ms behind. Several slots fill left to right at `FILL_STAGGER`. Errors run the reverse: a *drain*.
- **Saved wash.** A pill opens from its middle (`clip-path: inset(0 50% round 999px) → inset(0 0 round 999px)`, `0.3s --ease-out`), then a check rises in 0.2s later on `FILL_SPRING`. Remount it via `key` on each save.
- **Edge sweep.** One lap of light around a rounded box (a conic gradient rotating 360° in 0.75s `--ease-in-out`, masked to a 2px ring, opacity `[0,1,1,0]`). It means "this was just saved." It plays once per event and never loops. Reduced motion: the edge only glows and fades.
- **Count to range.** Figures spring to each new value when a filter or range changes, written straight to the DOM.
- **Data marks rise.** Bars `scaleY(0→1)` from their baseline (`transform-origin: 50% 100%`, `transform-box: fill-box`, `0.55s cubic-bezier(.2,.8,.2,1)`). Dots pop (`scale 0→1`, `0.4s --ease-out`). Both run left to right with `--i × --stagger-dense`. These are pure CSS, so they play before hydration.
- **Line draws in.** A clip sweeps open left to right behind the line (`0.9s cubic-bezier(.3,.7,.2,1)`). This is showcase timing, used for a once-per-view chart.
- **Gesture fill.** In a drag-to-pick control (a 1–7 rating, say), a `layoutId` fill follows the finger row by row on `TRACK_SPRING`, with a haptic tick per row. On release it lands on `LAND_SPRING` and morphs into the summary badge (same `layoutId`).

---

## 8. Showcase patterns

**Rules first.** Most showcase motion that ends up regrettable breaks one of these:
- **One hero moment per viewport.** Everything else on that screen is daily-register.
- **SSR is visible.** Motion renders `initial` into server HTML, so `initial={{ opacity: 0 }}` on the hero headline hides your LCP element until hydration. Animate decorative layers with Motion, animate key text with CSS keyframes (which run without JS), or keep `initial={false}` on the real content.
- **Loops pause.** Stop when off-screen (`useInView`/IntersectionObserver) and when the tab is hidden. Anything that moves for more than 5s needs a pause control (WCAG 2.2.2). Under reduced motion, show a still frame.
- **Isolate.** Showcase code lives on marketing or review routes and is code-split. It never leaks into app chrome.
- **Budget.** Cap WebGL at DPR ≤2. Use one canvas, not several. Check frame time at 4× throttle.

**Techniques worth internalising** (studied in Aceternity, Fancy Components, Skiper UI, React Bits, Magic UI, Cult UI, Smooth UI and Motion Primitives; rebuild them on the project's stack):

| Technique | Recipe | Numbers |
|---|---|---|
| Cursor spotlight / lit border | `pointermove` writes `--x/--y` on the element (style, not state; rAF-throttled); background is `radial-gradient(at var(--x) var(--y), …)`; border version masks to a 1px ring | Radius 300–600px; alpha ≤0.15; gated `(hover: hover)` |
| 3D tilt card | rotateX/Y from pointer offset, `perspective: 900px`; settles back on leave | ≤6–8°; `SNAP_SPRING` home |
| Magnetic button | Translate toward the pointer within a radius | ≤6px; `SNAP_SPRING` |
| Dock magnification | Distance from pointer → size via `useTransform` | 1→1.5× over ~150px |
| Morphing dialog | Card → dialog through a shared `layoutId`; radius and children kept true by layout scale correction; content fades after the shell lands | `SHEET_SPRING`; content +80ms |
| Dynamic Island container | Container morphs size with `layout`; contents swap with `AnimatePresence mode="popLayout"` crossfade | bounce 0.2–0.3 |
| Word reveal | Split by word (line for headings); parent `aria-label`, pieces `aria-hidden`; y 8px + opacity + `blur(4px)→0`; once | 30–50ms/word, total ≤600ms |
| Rotating word | `AnimatePresence mode="popLayout"`, y ±100% inside an `overflow: clip` line; the width adapts with `layout` | ~2.5s dwell; `SNAP_SPRING` |
| Scramble / decode | Each character cycles random glyphs, then settles left to right; monospace or `tabular-nums` so width never jitters; final text in `aria-label` | ≤800ms; ~30fps swaps |
| Marquee / logo loop | Duplicate the track; CSS `translateX(-50%)` linear loop; `mask-image` fades the edges; pause on hover and off-screen | ~30–60px/s |
| Border beam | A conic gradient on `@property --angle`, masked to the border; or the **edge sweep** (§7) once per event instead of forever | One lap 0.75s, or ≥4s/lap if ambient |
| Shader / mesh background | Paper Shaders (its own WebGL) as the one allowed exception; static poster image for reduced motion and no-WebGL | DPR ≤2; pause off-screen |
| Scroll storytelling | Sticky section + `useScroll({ target })` → `useTransform` on decorative layers; CSS `view()` in `@supports` for simple reveals | Parallax ratio ≤0.1–0.3; never on body text |
| Grid fill-in | The slot fill (§7) at grid scale, e.g. a calendar or poster filling itself in on a landing page | ~22ms step for ~30 cells, 0.3s lead |
| Count-up stats | §6 number pattern, once in view | `COUNT_SPRING` |

---

## 9. Text-mode register (glyph / ASCII)

This is a separate aesthetic, not a fourth library. The medium is characters on a fixed monospace grid, and animation means **changing which character occupies a cell**, not moving boxes. It suits loaders, boot or decode sequences, terminal-styled heroes, text sparklines and "rendered in type" imagery. Keep it opt-in, per project or per surface, so it doesn't muddy the daily vocabulary.

**Material.**
- Shade blocks: `░▒▓█`.
- Eighth blocks for smooth bars: `▏▎▍▌▋▊▉█` horizontally, `▁▂▃▄▅▆▇█` vertically.
- Box drawing: `─│┌┐└┘├┤`.
- Braille (`⠁⠃⠇⡇⣇⣧⣷⣿`) for 2×4 sub-cell resolution.
- ASCII density ramps such as `" .:-=+*#%@"`.

**Rules.**
- **Lock the grid.** Use a true monospace font with full block coverage (Glyph Kit recommends Departure Mono; Geist Mono and JetBrains Mono also work). Fix `line-height`, size in `ch`, and never let a frame reflow.
- **Stepped cadence is the look.** Run at 8–24fps via `requestAnimationFrame` with frame skipping, or CSS `steps()`. Smooth 60fps interpolation reads as a bug here.
- **One write per frame.** Build the frame as a string and set a single `<pre>`'s `textContent`. For grids above roughly 5k cells, or for luminance-sampled images and video, draw to a canvas instead.
- **Accessibility.** The glyph art is `aria-hidden`. Meaning lives in real text or ARIA (e.g. a `role="progressbar"` with `aria-valuenow` alongside a block-bar loader). Reduced motion shows the final frame.
- **Pause off-screen**, as with any loop.
- **Pairs well with** the scramble/decode reveal (§8) and the text-timeline spec (§5a.3). The timeline is the same medium used for specification.

**Where to look:** Glyph Kit (glyph-kit.traykov.cc) for text-first figures and motion specs written as text, and as a model of an agent skill that stamps sample data and refuses impossible data. play.core by ertdfgcvb (play.ertdfgcvb.xyz) for programmable text-mode animation. three.js `AsciiEffect` (threejs.org/docs/pages/AsciiEffect.html) for rendering 3D as ASCII.

---

## 10. Accessibility and performance rules

**Accessibility.**
- `<MotionConfig reducedMotion="user">` at the root. Motion then skips transform and layout animation and keeps opacity and colour.
- A CSS backstop is fine: `animation-duration: 0.01ms; animation-delay: 0ms; iteration-count: 1; transition-duration: 0.01ms`. It's safe only because keyframes use `animation-fill-mode: both`, so elements land in their final state. Check that before adding it.
- Vestibular triggers to remove under reduced motion: parallax, large zooms, spinning, full-screen slides, scroll-linked transforms.
- WCAG 2.3.3 (AAA): motion triggered by interaction can be turned off. WCAG 2.2.2 (A): anything auto-moving for more than 5s can be paused.
- Focus moves into dialogs and sheets at open and returns at close, independent of animation. Never put focus or data behind `onAnimationComplete`.
- Hover-only effects sit inside `@media (hover: hover)`. Keyboard focus gets an equivalent (the link hairline does).

**Performance.**
- Transform and opacity. `transform-box: fill-box` for SVG marks. Avoid width/height/top/left loops.
- Spring a motion value and write to the DOM (`textContent`, `style`) instead of setting React state per frame.
- `will-change` only during an animation, never as a global default.
- Avoid `transition: all`. List properties explicitly.
- Big blurs and `backdrop-filter` on moving layers are paint-heavy. Keep them static or small.
- Check at 60Hz and 120Hz. Use DevTools Performance with paint flashing: a transform-only animation should not flash.

---

## 11. Anti-patterns

- `transition: all`. Ease-in on an entrance. Linear on UI movement.
- Daily UI over 350ms with no reason. Cascades longer than ~400ms (daily) or ~1.2s (showcase).
- Surfaces entering from `scale(0)`. Popovers scaling from their centre.
- Animating keyboard-driven or 100+/day actions.
- Keyframes for toggled state (they restart instead of retargeting). Use transitions or springs.
- Bounce on opacity, colour or numbers. Bounce >0.4 anywhere. Overshooting count-ups.
- Infinite loops without an off-screen pause. Ambient motion >5s without a pause control.
- Hero text with `initial={{ opacity: 0 }}` from Motion on a server-rendered page.
- Smooth-scroll hijacking. Parallax on text. Letter-by-letter animation of long text. Split text without an accessible label.
- A second animation runtime: GSAP, react-spring or a registry component that pulls in three.js, inside app chrome.
- Inline numbers instead of tokens. A spring named for its feel ("bouncy") instead of what it moves.
- Copying a registry component wholesale, with its own durations, curves and icon library.
- Everything moving at once: one focal motion per moment.
- Hover effects firing on touch. Hover transforms on the hovered element itself (flicker). Gestures without haptics on mobile where a tick would help.
- A modal and its backdrop, or a tooltip and its arrow, on different timings. Animated blur above ~20px.

---

## 12. Review checklist

Score each animation 1 point per item. In daily UI, anything under 7/8 gets fixed.

1. **Job:** it has one, and you can name it.
2. **Frequency:** it would still be wanted on the 100th use, and keyboard-triggered paths are instant.
3. **Timing:** within the register's budget; exit faster than entry.
4. **Curve/spring:** from tokens; ease-out or spring on entry; ease-in only on short exits.
5. **Origin:** grows from its cause; exits the way it came.
6. **Interruptible:** rapid re-triggering retargets, never queues or jumps.
7. **Cheap:** compositor-only; no unguarded loop; no paint flashing on transforms.
8. **Reduced motion:** a deliberate fallback that keeps the meaning.

Then check the whole surface:
- Only one animation runtime in the production bundle. `MotionConfig reducedMotion="user"` at the root. `LazyMotion` where it pays off.
- No raw `ms` or `cubic-bezier` literals in components; all come from tokens.
- Keyboard: focus lands correctly as dialogs, sheets and routes open.
- Touch: hover gated; drag thresholds feel right; no accidental dismissals; haptics where gestures step.
- Firefox: scroll-driven animations and cross-document transitions degrade to complete, static content.
- Showcase pages: LCP text visible without JS; loops pause off-screen; DPR capped.

---

## 13. Reference catalogue (Oct 2026)

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
| Glyph Kit | glyph-kit.traykov.cc | Text-first figures and motion timelines (§9) |
| Benji Taylor, *Family Values* (2024) | benji.org/family-values | The essay behind Family's fluid feel: gradual revelation, "fly instead of teleport", selective emphasis, dynamic trays, text morphing |
| Rauno, Web Interface Guidelines | rauno.me/interfaces | Interaction rules, including no extraneous animation on frequent, low-novelty actions |
| Jhey Tompkins | codepen.io/jh3y | Pure-CSS motion experiments; the ceiling of what CSS alone can do |

**Inspiration and study hubs** (browse for ideas, then extract with §5b)

| Hub | URL | What's there | Caveat |
|---|---|---|---|
| Codrops Creative Hub | tympanus.net/codrops/hub | Open-source demos and tutorials with code; collections for typography, hover, cursor, state-to-state, scroll-driven, grids, WebGL | Mostly Three.js, GLSL and GSAP: showcase register, so study it rather than copy it. Typography, hover and state-to-state carry over to a CSS + Motion stack best |
| Design Spells | designspells.com | ~340 "spells": micro-interactions, transitions and easter eggs from real apps, tagged by type and app | Recordings, not code; use for the *why* and the choreography |
| 60fps | 60fps.design | Library of iOS and web app animations as native-frame-rate video, filterable by context | Its MCP server (shot search, motion breakdowns) is a paid add-on |
| Awwwards | awwwards.com | Award-site inspiration and curated UI-animation collections | Showcase register only; rarely shows how it was built |

**Tools**
- Linear easing generator (linear-easing-generator.netlify.app, by Jake Archibald and Adam Argyle): turns any JS easing or SVG curve into `linear()`. It's a GUI alternative to §4d.
- cubic-bezier.com: drag a curve and compare it against another while it plays.

**Neighbouring agent skills** (don't load them alongside this one; they overlap and their numbers differ slightly)
- Vercel's `web-animation-design` (github.com/vercel-labs/open-agents) and Emil's own skill are both based on *Animations on the Web*. This file already absorbs their rules, with a named vocabulary, the stack and the registers on top.

---

## 14. Provenance

- **Reference vocabulary:** named springs, signature patterns and gesture thresholds extracted from two shipped Next.js + Motion products and tuned by hand.
- **Second sweep (Oct 2026):** Codrops Hub, Design Spells, Family Values and Rauno's guidelines were checked on their own sites. 60fps, the linear easing generator and Vercel's skill were checked through their docs or directory listings. Awwwards, cubic-bezier.com and Jhey's CodePen are long-standing and were not re-checked.
- **Platform and library facts:** a deep-research report from Oct 2026 covering Motion, React, MDN, web.dev, caniuse, GSAP, Material, Apple, Carbon, Atlassian, NN/g and Emil Kowalski. Facts that change over time (versions, browser support, pricing, maintenance) are marked Oct 2026; re-check them when they matter.
- **From Vercel's `web-animation-design`:** paired-element timing, the hover-child fix, the before/after review table and the blur cap.
- **Spring behaviour figures:** simulated with the §4d integrator.
