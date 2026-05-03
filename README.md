# agent-skills

A curated library of production-grade agent skills for AI coding assistants
and LLM-powered workflows. Each skill is a structured instruction set that
extends an AI agent's capabilities for a specific domain or workflow type.

---

## Skills

| Skill | Description |
|---|---|
| [`skill-creator-pro`](./skills/skill-creator-pro/) | Build complex, multi-phase agent skill pipelines with quality gates, two-zone architecture, deterministic locking, and cross-session state persistence |

---

## What is an agent skill?

An agent skill is a folder of structured instructions that tells an AI agent
how to perform a specific, complex workflow — reliably and reproducibly.

Each skill contains at minimum a `SKILL.md` with YAML frontmatter (`name`,
`description`) that the agent reads to decide whether to activate the skill
for a given request. When activated, it loads the full instructions and any
supporting files from `references/`, `scripts/`, and `assets/` as needed.

### Typical skill layout

```
skill-name/
├── SKILL.md              # Required — frontmatter + instructions
├── README.md             # Documentation
├── agents/               # Agent interface configs
├── references/           # Domain knowledge, loaded on demand
├── scripts/              # Deterministic Python scripts
└── assets/               # Templates and format specifications
```

---

## Using these skills

Clone the repo and place the skills you want in your agent's skill library
directory. For Codex/Antigravity, this is `~/.codex/skills/`.

```bash
git clone https://github.com/odonnellmatt/agent-skills.git
cp -r agent-skills/skills/skill-creator-pro ~/.codex/skills/
```

Each skill activates automatically when your prompt matches its trigger
description in the `SKILL.md` frontmatter.

---

## Requirements

- Python 3.9+ (for skills that include automation scripts)
- No external Python dependencies — all scripts use the standard library only
