# Memory Management and State Persistence

## Table of Contents

1. [The Memory Hierarchy](#the-memory-hierarchy)
2. [State Schema Design](#state-schema-design)
3. [Context Engineering Strategies](#context-engineering-strategies)
4. [Preventing Context Rot](#preventing-context-rot)
5. [Cross-Session Continuity](#cross-session-continuity)
6. [Memory Integration Patterns](#memory-integration-patterns)

---

## The Memory Hierarchy

Complex skills operate across four memory timescales. Each requires different
implementation:

| Type | Scope | Lives In | Survives Context Reset? |
|------|-------|----------|------------------------|
| Working memory | Current reasoning step | LLM context window | No |
| Short-term state | Current session | Variables, structured objects | Partial (via compaction) |
| Mid-term state | Cross-session workflow | Persisted JSON state files | Yes |
| Long-term memory | Cross-project | File-based memory (MEMORY.md) | Yes |

### Working Memory (Context Window)

The LLM's active context. Precious and finite. As it fills, the model suffers from
"context rot" — degraded recall and reasoning, especially for information in the middle.

**Budget:** Keep the active context as small as possible. Load only what the current
step needs.

### Short-Term State (Session Variables)

Structured objects that persist within a session regardless of context rotation:
- Current phase and step
- Decisions made so far
- Accumulated metrics

These act as structured short-term memory that remains intact as the context window fills.

### Mid-Term State (Persisted Files)

JSON state files that persist across sessions:
- Full workflow progress
- All artifacts and their paths
- Complete decision log with rationale
- Quality gate results

### Long-Term Memory (MEMORY.md System)

Cross-project user preferences and domain expertise:
- User's writing style preferences
- Feedback corrections (validated approaches)
- Domain expertise level
- External system references

---

## State Schema Design

### Complete State Schema Template

```json
{
  "$schema": "workflow-state-v1",
  "workflow": {
    "id": "uuid-generated-at-creation",
    "type": "workflow-type-identifier",
    "title": "Human-readable workflow title",
    "created_at": "ISO-8601 timestamp",
    "last_updated": "ISO-8601 timestamp"
  },
  "progress": {
    "current_phase": 1,
    "current_step": "1.2",
    "phases_completed": [],
    "gates_passed": [],
    "status": "in_progress"
  },
  "artifacts": {
    "by_phase": {
      "phase_1": {
        "outline": {"path": "output/outline.md", "created_at": "timestamp"},
        "protocol": {"path": "output/protocol.md", "created_at": "timestamp"}
      }
    },
    "primary_output": null
  },
  "decisions": [
    {
      "id": 1,
      "timestamp": "ISO-8601",
      "phase": 1,
      "step": "1.1",
      "decision": "Selected narrative synthesis over meta-analysis",
      "rationale": "Heterogeneous study designs preclude statistical pooling",
      "alternatives_considered": ["meta-analysis", "framework-based synthesis"],
      "approved_by": "human"
    }
  ],
  "quality_gates": {
    "QG1": {
      "status": "passed",
      "checked_at": "timestamp",
      "automated_results": {"protocol_complete": true, "criteria_defined": true},
      "human_approved": true,
      "notes": "User approved with minor revision to exclusion criteria"
    }
  },
  "metrics": {},
  "feedback_log": [
    {
      "timestamp": "ISO-8601",
      "detected_at": "phase_3",
      "routed_to": "phase_2",
      "issue": "Missing database coverage",
      "resolution": "Added IEEE Xplore search",
      "resolved_at": "timestamp"
    }
  ],
  "configuration": {
    "output_format": "docx",
    "citation_style": "Harvard",
    "target_journal": null,
    "quality_thresholds": {
      "kappa_minimum": 0.60,
      "prisma_minimum_percent": 90
    }
  }
}
```

### State Update Protocol

1. **Auto-save at every gate transition** — Never rely on end-of-session saves
2. **Immutable decision log** — Append-only, never modify past entries
3. **Artifact paths are relative** — Enables portability across machines
4. **Include checksums for deterministic outputs** — Enables reproducibility verification

---

## Context Engineering Strategies

### Progressive Disclosure (Three-Tier Loading)

```
Tier 1: DISCOVERY (~100 tokens)
  Only YAML frontmatter loaded at startup
  Agent decides whether to activate based on name + description

Tier 2: ACTIVATION (<5,000 tokens)
  Full SKILL.md body loaded when skill triggers
  Contains workflow structure, steps, and pointers to references

Tier 3: EXECUTION (unlimited, loaded JiT)
  Reference files, scripts, templates loaded only when needed
  Each reference file loaded individually, not all at once
```

### Semantic Tool Selection

When a skill involves many tools or scripts, don't inject all tool schemas at once:

1. Embed tool descriptions as vectors
2. At each step, retrieve only the 3-5 most relevant tools
3. This reduces tool-related tokens by 91-99.6%
4. Fewer tools actually IMPROVE selection accuracy (92.1% precision at K=1)

### Context Window Budget Allocation

For a typical complex skill step:

| Component | Token Budget | Notes |
|-----------|-------------|-------|
| System prompt + skill instructions | 2,000-3,000 | Cached, doesn't change |
| Current step instructions | 500-1,000 | From active sub-skill |
| Reference data (JiT loaded) | 1,000-3,000 | Only what this step needs |
| State summary | 200-500 | Condensed from full state |
| Working space for reasoning | 3,000-5,000 | Leave room for the model to think |

---

## Preventing Context Rot

### Symptoms of Context Rot

- Agent forgets constraints stated earlier in the conversation
- Output contradicts decisions made in previous phases
- Agent re-asks questions already answered
- Narrative structure drifts across long document generation
- Agent invents facts not present in any source

### Mitigation Strategies

**1. Helper-Agent Delegation**
When helper agents are explicitly authorized and available, delegate deep work:
- Helper agent receives only the context it needs for its specific task
- Helper agent does extensive work (may consume 50,000+ tokens)
- Helper agent returns only a condensed summary (1,000-2,000 tokens)
- Orchestrator's context stays clean

**2. Context Compaction**
When nearing context limits:
- Summarize critical details from the conversation so far
- Clear raw tool outputs that have been processed
- Initiate a new context window with the distilled summary
- Re-read the state file to restore full awareness

**3. Structural Anchoring for Long Documents**
When generating long outputs (academic papers, reports):
- Maintain an outline document
- Re-read the outline before generating each new section
- After each section, update a "sections completed" summary
- This prevents drift even as context windows rotate

**4. Structured Note-Taking**
The agent writes progress notes to a persistent file:
```markdown
# Workflow Notes — [Title]

## Phase 1 Complete
- Research question: [formulated question]
- Methodology: narrative synthesis (see decision log entry #1)
- Key constraint: focus on studies from 2020-2026

## Phase 2 In Progress
- Searched: PubMed, Scopus, Web of Science
- Remaining: IEEE Xplore, Google Scholar
- Current hit count: 847 results before dedup
```

---

## Cross-Session Continuity

### Resumption Protocol

When the user says "continue" or "resume":

1. Read the state file: `state/workflow_state.json`
2. Load the current phase's sub-skill
3. Read workflow notes if they exist
4. Present a brief status summary to the user:
   "Resuming your [workflow type]. You're at Phase [N], Step [X].
    Last completed: [description]. Next: [description]. Ready to proceed?"
5. Wait for user confirmation before executing

### Session Handoff

If a workflow will be continued by a different agent instance:

1. Ensure state file is fully up-to-date
2. Write a handoff note in the workflow notes file:
   ```
   ## Session Handoff — [timestamp]
   Current state: Phase 3, Step 3.2
   In progress: Full-text screening, 12 of 47 papers reviewed
   Blocking issues: None
   Next action: Continue screening from paper #13
   ```
3. All artifacts must be saved to defined paths (not in-memory)

---

## Memory Integration Patterns

### What to Save to Long-Term Memory

| Save This | Memory Type | Example |
|-----------|------------|---------|
| User domain expertise | user | "User has 15 years of meta-analysis experience" |
| Validated feedback | feedback | "Don't use passive voice in Methods sections" |
| Preferred tools/frameworks | user | "User prefers Harvard over APA citations" |
| External system locations | reference | "Team tracks tasks in Linear project RESEARCH" |

### What NOT to Save to Long-Term Memory

- Current workflow progress (use state files)
- Specific task details (use state files)
- Debugging information (ephemeral)
- Anything derivable from the code or git history
- Anything already documented in CLAUDE.md files

### Memory-Informed Skill Behavior

When memories exist that affect skill behavior:

```markdown
## Step: Write Introduction

Before writing, check long-term memory for:
- User's writing style preferences (formal vs. accessible)
- Previous feedback on introductions (common corrections)
- Target audience information

Adapt tone and structure accordingly, but do not mention
that you are using memory — just apply the preferences naturally.
```

---

## Related References

- `architecture-patterns.md` — Complex patterns require state persistence across steps
- `quality-gates.md` — Gate transition results should be saved to state schema
- `two-zone-architecture.md` — State updates from scripts are Deterministic; LLM summaries are Reasoning
- `resilience-patterns.md` — State enables recovery after failures and session interruptions
