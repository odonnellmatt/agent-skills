# Master Skill Template

Use this template when creating the top-level SKILL.md for a complex workflow.
Replace all `[PLACEHOLDER]` values with actual content.

---

```yaml
---
name: [workflow-name-lowercase-hyphens]
description: >
  A complete, [N]-phase, [N]-gate agent skillset for [domain description].
  Covers [list phases]. Enforces [standards/frameworks]. Contains [N]
  composable skills orchestrated by a master controller with automated
  feedback loops. Use when the user wants to [trigger phrases]. Also
  triggers on [alternative phrases]. Do NOT use for [negative triggers].
---
```

```markdown
# [Workflow Name]

## Quick Start

- **Start new**: Say "[start trigger phrase]"
- **Resume**: Say "Continue my [workflow]" or "What's next?"
- **Single skill**: Invoke any skill by name for standalone use

## Entry Point

The **master controller** is `[orchestrator-skill-name]`. Always start there
for end-to-end workflows.

## Complete Skill Inventory ([N] Skills)

### Phase 1 — [Phase Name] ([N] skills)
| # | Skill File | Purpose |
|---|-----------|---------|
| 1 | `[skill-name].md` | [What it does] |
| 2 | `[skill-name].md` | [What it does] |

### Phase 2 — [Phase Name] ([N] skills)
| # | Skill File | Purpose |
|---|-----------|---------|
| 3 | `[skill-name].md` | [What it does] |

[... repeat for all phases ...]

### Support Skills ([N] skills — available at any phase)
| # | Skill File | Purpose |
|---|-----------|---------|
| N | `[orchestrator].md` | Master controller — chains all skills, enforces gates |
| N | `[gate-verifier].md` | Gate enforcement mechanism |
| N | `[progress-tracker].md` | State, metrics, decision log |
| N | `[feedback-router].md` | Route issues back to correct phase/skill |
| N | `[state-schema].md` | Persistent JSON state schema |

## Quality Gates

| Gate | Phase Transition | Key Checks |
|------|-----------------|------------|
| QG1 | [Phase 1] → [Phase 2] | [Specific measurable criteria] |
| QG2 | [Phase 2] → [Phase 3] | [Specific measurable criteria] |
| QG3 | [Phase 3] → [Phase 4] | [Specific measurable criteria] |
[... repeat for all gates ...]

## Feedback Loop System

When an issue is detected at **any phase**, the `[feedback-router]`
automatically identifies the correct upstream skill and routes back.
The pipeline never silently proceeds with known issues.

## State Persistence

Project state is persisted as JSON (see `[state-schema].md`) and auto-saved
at every gate transition. This enables cross-session continuity.

## Error Handling

| Error | Cause | Recovery |
|-------|-------|----------|
| [Error 1] | [Cause] | [Recovery action] |
| [Error 2] | [Cause] | [Recovery action] |

## Gotchas

Non-obvious pitfalls the agent must self-correct for. List only what pushes the
agent out of its default behaviour — skip anything the foundation model already knows.

- [Specific historical mistake or edge case and how to avoid it]
- [Domain convention that looks wrong to a general LLM but is correct in this workflow]
- [Subtle handoff or format requirement that has caused past failures]

## Memory Integration

- Save user domain expertise and preferences on first discovery
- Save validated feedback corrections to prevent repeated mistakes
- Never save ephemeral workflow state to long-term memory
```
