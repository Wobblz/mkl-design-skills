# mkl-design-skills

Opinionated design skills for AI coding agents. Each skill turns design craft into rules an agent can follow and a reviewer can check: principles, named tokens, a pattern catalogue, anti-patterns and a review checklist. The skills teach patterns, not copied components, so a project ends up with one coherent vocabulary instead of five libraries' worth of defaults.

## Skills

| Skill | What it covers |
|---|---|
| [`mkl-motion`](skills/mkl-motion/SKILL.md) | Motion for React/Next.js products. It covers when to animate and when not to. It defines three registers (daily UI, showcase, text-mode) and a one-runtime stack (CSS → View Transitions → Motion). It includes named spring tokens with measured behaviour, 46 patterns with reduced-motion fallbacks, a review checklist, and a curated catalogue of libraries to study rather than install. |
| [`mkl-typography`](skills/mkl-typography/SKILL.md) | Web typography for laying out text, from the print canon (Bringhurst, Tschichold, Butterick, Rutter) to CSS you can ship today. It covers three registers (reading, UI, display), type-scale methods, measure and leading, vertical rhythm measured on editorial sites, OpenType features and tabular figures, `lang` and Bulgarian Cyrillic forms, hyphenation and line breaking, hanging punctuation and optical alignment, drop caps, emphasis, code and maths, font loading, dark mode, forced colours and OG images, with dated browser support and a review checklist. |

More are on the way.

## Install

**Claude Code (plugin marketplace)**

```
/plugin marketplace add Wobblz/mkl-design-skills
/plugin install mkl-design-skills@mkl-design-skills
```

Skills load as `/mkl-design-skills:<skill>`, and Claude also picks them up automatically when a task matches.

**Any agent that supports skills ([skills CLI](https://github.com/vercel-labs/skills))**

```
npx skills add Wobblz/mkl-design-skills              # all skills
npx skills add Wobblz/mkl-design-skills@mkl-motion   # one skill
```

**By hand.** Copy a folder from `skills/` into your agent's skills directory (for Claude Code, `~/.claude/skills/`), or upload it as a custom skill in Claude.

## How these skills are written

- **One strong default.** Each rule gives a recommendation, and the alternatives are named only when they matter.
- **Patterns, not components.** Techniques are extracted from the best libraries and rebuilt on the project's own stack and tokens, so you never inherit a second runtime.
- **Project first.** A skill checks for the project's existing conventions and maps onto them before introducing its own.
- **Checked facts.** Anything that changes over time, such as browser support, versions, pricing or maintenance, is dated and was checked against primary sources. Numbers are measured or simulated, not guessed.
- **Credited.** Sources are named in each skill's reference section.
- **Compact where it counts.** Each `SKILL.md` stays under about 500 lines and routes to `references/*.md` files that the agent opens only when a task needs them, so a skill can go deep without loading everything every time.

## Adding a skill

1. Create `skills/mkl-<topic>/SKILL.md` with `name` and `description` frontmatter. The description should say when the skill applies. Put depth in `skills/mkl-<topic>/references/` and link it from `SKILL.md`.
2. Add `./skills/mkl-<topic>` to the `skills` array in `.claude-plugin/marketplace.json`.
3. Add a row to the table above.
4. Run `claude plugin validate .` before opening a PR.

## License

MIT. See [LICENSE](LICENSE). Referenced libraries, articles and guidelines belong to their authors; the skills link to them rather than reproducing them.
