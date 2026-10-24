# mkl-design-skills

Opinionated design skills for AI coding agents. Each skill turns design craft into rules an agent can follow and a reviewer can check: principles, named tokens, a pattern catalogue, anti-patterns and a review checklist. The skills teach patterns, not copied components, so a project ends up with one coherent vocabulary instead of five libraries' worth of defaults.

## Skills

| Skill | What it covers |
|---|---|
| [`mkl-motion`](skills/mkl-motion/SKILL.md) | Motion for React/Next.js products, on by default: interactions, loading, numbers, disclosure and confirmations all move unless there's a reason not to. It defines three registers (daily UI, showcase, text-mode) and a one-runtime stack (CSS → View Transitions → Motion), named spring tokens with measured behaviour, a pattern catalogue with reduced-motion fallbacks, a review checklist, and a catalogue of libraries to study rather than install. |
| [`mkl-typography`](skills/mkl-typography/SKILL.md) | Typography taste and traps, not the textbook. It holds house defaults (one sans, a 1.25 scale of size, line-height and tracking triplets, two number voices, a dark-mode weight step-down, named spacing), the traps that only show in served font files or the browser (stripped OpenType features, missing Bulgarian forms, `ch` versus tabular digits), and scripts that check a font file and grep a project for them. |

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

- **Taste over textbook.** A skill keeps what an agent wouldn't do on its own: house defaults, known traps and runnable checks. General craft is assumed.
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
