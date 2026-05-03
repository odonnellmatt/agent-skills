# skill-creator-pro

> **Build production-grade, multi-phase agent skills** — with quality gates,
> two-zone architecture, deterministic locking, and cross-session state
> persistence.

`skill-creator-pro` is a meta-skill: a structured guide for creating *other*
complex skills. It takes you from a blank slate to a fully-scaffolded,
validated skill pipeline — complete with sub-skills, gate validators, state
schemas, and reference libraries — through a rigorous six-phase process.

Use it when your workflow is too complex for a simple one-shot skill.

---

## Table of Contents

1. [What it's good at](#what-its-good-at)
2. [What it's not great at](#what-its-not-great-at)
3. [Directory structure](#directory-structure)
4. [How to use the skill](#how-to-use-the-skill)
5. [The six-phase process](#the-six-phase-process)
6. [Domain accelerators](#domain-accelerators)
7. [Tooling reference](#tooling-reference)
8. [Core design principles](#core-design-principles)
9. [Anti-patterns](#anti-patterns)
10. [Requirements](#requirements)

---

## What it's good at

### Complex, multi-phase pipelines
Anything with 3+ sequential phases, quality checkpoints between them, and
outputs that must be reproducible. It excels here because it enforces the
**two-zone architecture** (deterministic steps locked in scripts, reasoning
steps owned by the LLM) and builds quality gates into the structure from the
start — not bolted on afterwards.

### High-stakes outputs that must be verified
Publication-ready documents, compliance reports, audited analytics,
regulatory submissions. The evaluator-optimizer loops and explicit gate
criteria mean the pipeline will not silently proceed past a bad result.

### Cross-session workflows
If a workflow spans multiple sessions or days, `skill-creator-pro` builds in
JSON state persistence so the agent can resume exactly where it left off,
with a full decision log of what was done and why.

### Domains with established accelerators
27 reference accelerators are bundled (see [Domain accelerators](#domain-accelerators)).
For these domains the scaffolding script generates the full directory
structure — SKILL.md, all sub-skill stubs, gate validator scripts, and a
state schema — in seconds. You then do a human refinement pass rather than
starting from scratch.

Covered domains include:

| Category | Domains |
|---|---|
| Academic research | Generic manuscript, scoping review, meta-analysis, rapid review, bibliometric analysis, qualitative meta-synthesis, umbrella review, thesis/dissertation |
| Applied research | Grant proposals, research & experiment design |
| Engineering | Software engineering, data engineering, DevOps & incident response, cybersecurity assessment |
| Business & analytics | Analytical pipelines, financial reporting, business intelligence, legal & contract analysis |
| Knowledge & content | Technical documentation, education & curriculum design |
| Cross-cutting | Resilience patterns, evaluation & benchmarking, security checklist |

### Trigger-collision detection
The bundled `audit_trigger_collisions.py` script scans your entire skills
library and flags any skill whose description overlaps too closely with the
new one. Two semantically-similar descriptions materially degrade selection
accuracy — this catches the problem before shipping.

---

## What it's not great at

### Simple, single-step skills
If the desired skill is a straightforward "do X given Y" with no phases,
no quality gates, and no need for deterministic scripts — this is massive
overkill. Use a simpler skill-creator instead. The overhead of six phases,
gate validators, and state schemas is not justified for single-step work.

### Fully automated skill generation
`skill-creator-pro` deliberately does **not** write finished skills for you.
Research consistently shows that LLM-generated skill content underperforms
human-authored content, especially in high-stakes domains. The scaffolding
script generates *structure and stubs*; the actual process steps, quality
criteria, and domain gotchas require a human authoring pass. Don't expect
to run it end-to-end without reviewing and filling in placeholders.

### Novel or cross-domain workflows without a matching accelerator
The accelerators are strong starting points for the 20 covered domains. For
genuinely novel workflows that don't fit any accelerator, or for workflows
that partially fit multiple accelerators, the scaffold becomes less useful —
you'll likely spend as much time editing the scaffold as you would authoring
manually. The skill guides you through manual authoring in that case, but
there's no shortcut.

### Workflows that evolve during execution
The Plan-and-Execute backbone is optimised for predictable, structured
workflows. If the workflow shape is genuinely unknown at the start — where
each step determines the next — a ReAct-based approach is better suited.
`skill-creator-pro` will flag this during requirements discovery (Phase 1)
and can scaffold around a ReAct sub-skill, but it's not its strongest fit.

### Guaranteeing agent selection accuracy in large skill libraries
The trigger-collision audit uses lexical Jaccard similarity as a proxy for
semantic overlap. It's a first-pass filter, not a verdict. Two descriptions
can share zero vocabulary and still collide semantically (e.g., "summarise a
paper" vs. "condense an article"). Always manually inspect the top-N
neighbours it reports — don't rely on a `PASS` result alone.

---

## Directory structure

```
skill-creator-pro/
├── SKILL.md                          # Master orchestrator — start here
│
├── agents/
│   └── openai.yaml                   # Agent interface config (display name, default prompt)
│
├── assets/                           # Templates for skill authoring
│   ├── master-skill-template.md      # Template for the top-level SKILL.md
│   ├── sub-skill-template.md         # Template for each sub-skill file
│   ├── quality-gate-template.md      # Template for quality gate definitions
│   └── state-schema-template.json    # Template for JSON state persistence
│
├── references/                       # JIT-loaded reference library (do not load all at once)
│   ├── architecture-patterns.md      # Orchestration pattern decision matrix + details
│   ├── two-zone-architecture.md      # Deterministic vs. reasoning zone split
│   ├── quality-gates.md              # Gate design patterns and examples
│   ├── memory-management.md          # Cross-session state persistence
│   ├── resilience-patterns.md        # Retry, backoff, circuit breaker patterns
│   ├── evaluation-framework.md       # Testing and benchmarking methodology
│   ├── security-checklist.md         # Pre-ship security audit checklist
│   └── [20 domain accelerators]      # Pre-built workflow blueprints per domain
│
└── scripts/
    ├── validate_skill.py             # Structural validation of any skill directory
    ├── scaffold_from_accelerator.py  # Generate a full skill directory from an accelerator
    └── audit_trigger_collisions.py   # Check for description overlap with existing skills
```

---

## How to use the skill

### Trigger phrases

Invoke the skill with any of the following:

```
"Build me a complex skill for [domain]"
"Create a pro skill pipeline for [workflow]"
"I need a multi-phase skill with quality gates"
"Build a production-grade skill for [use case]"
"Design a pipeline skill for [workflow]"
"Create an enterprise skill for [domain]"
```

Do **not** use this skill for simple, single-step skills — use a standard
skill-creator for those.

### Starting a new skill

Say something like:

```
Build me a complex skill for conducting systematic literature reviews,
with multiple phases, quality gates, Harvard referencing enforcement,
and DOCX export.
```

The skill will run Phase 1 (Requirements Discovery), interview you with
targeted questions, then present a proposed architecture for your approval
before writing anything.

### Skipping to scaffolding

If you already know your domain matches one of the 27 accelerators:

```
Scaffold a skill for [domain] using the [accelerator name] accelerator,
output to ~/my-skills/my-new-skill.
```

The scaffolding script will generate the full directory structure. You then
do a human refinement pass (review `SCAFFOLD_REPORT.json` for the TODO list).

### Running the scaffold script directly

```bash
python scripts/scaffold_from_accelerator.py \
  --accelerator references/scoping-review-workflow.md \
  --output ~/my-skills/my-scoping-review \
  --name "Scoping Review"
```

### Validating any skill directory

```bash
python scripts/validate_skill.py /path/to/your/skill-directory
```

Returns JSON with `overall_status` (`PASS`, `PASS_WITH_WARNINGS`, or `FAIL`)
and a list of issues with severities (`critical`, `warning`, `info`) and
actionable suggestions.

### Auditing trigger collisions

```bash
# Against the default library (~/.codex/skills/)
python scripts/audit_trigger_collisions.py /path/to/new-skill

# Against a custom library, with a tighter threshold
python scripts/audit_trigger_collisions.py /path/to/new-skill \
  --library ~/custom/skills \
  --threshold 0.15

# Show more neighbours
python scripts/audit_trigger_collisions.py /path/to/new-skill --top 20
```

Returns JSON with a `PASS` or `WARN` verdict and a ranked list of the most
similar skills in your library. Exit code: `0` on PASS, `2` on WARN.

---

## The six-phase process

| Phase | Name | Output |
|---|---|---|
| 1 | Requirements Discovery | Interview results; workflow scope confirmed |
| 2 | Architecture Design | Orchestration pattern, two-zone split, gate definitions, state schema, skill inventory — presented for approval |
| 3 | Skill Authoring | Master SKILL.md, sub-skill files, deterministic scripts, reference files, asset templates |
| 4 | Validation | Structural validation (`validate_skill.py`), test cases, with/without comparison, quality audit, trigger-collision audit |
| 5 | Iteration & Hardening | Lean prompts, bundled scripts, hardened error paths, optimised trigger descriptions |
| 6 | Security Review | Credential audit, input validation check, injection vector scan, least-privilege review |

The agent presents the Phase 2 architecture to you for approval before
writing a single file. You are in the loop at every gate.

---

## Domain accelerators

Accelerators are pre-built workflow blueprints for common complex domains.
They contain phase architecture, sub-skill inventories with zone
classifications, quality gate definitions, two-zone splits, and common
failure modes. The scaffold script parses them to generate a complete
starting directory.

| Workflow Type | Reference File |
|---|---|
| Generic academic manuscript | `academic-workflow.md` |
| Scoping review (JBI / PRISMA-ScR) | `scoping-review-workflow.md` |
| Meta-analysis (PRISMA + quantitative pooling) | `meta-analysis-workflow.md` |
| Rapid review (Cochrane / WHO, time-boxed) | `rapid-review-workflow.md` |
| Bibliometric & scientometric analysis | `bibliometric-analysis-workflow.md` |
| Qualitative meta-synthesis (ENTREQ) | `qualitative-meta-synthesis-workflow.md` |
| Umbrella review (JBI / PRIOR) | `umbrella-review-workflow.md` |
| Grant proposals (NIH / NSF / ERC / UKRI / Horizon) | `grant-proposal-workflow.md` |
| Thesis & dissertation | `thesis-dissertation-workflow.md` |
| Repeatable analytical pipelines | `analytical-pipeline.md` |
| Software engineering (migration, refactoring, review) | `software-engineering-workflow.md` |
| Financial reporting & compliance | `financial-reporting-workflow.md` |
| Data engineering & ETL pipelines | `data-engineering-workflow.md` |
| Legal & contract analysis | `legal-contract-workflow.md` |
| Cybersecurity assessment & threat modeling | `cybersecurity-assessment-workflow.md` |
| Product & technical documentation | `technical-documentation-workflow.md` |
| Research & experiment design | `research-experiment-workflow.md` |
| Business intelligence & reporting | `business-intelligence-workflow.md` |
| DevOps & incident response | `devops-incident-workflow.md` |
| Education & curriculum design | `education-curriculum-workflow.md` |

**Choosing a review accelerator:** route on the deliverable goal — pooling
effectiveness → meta-analysis; evidence mapping → scoping review; time-boxed
policy question → rapid review; synthesising existing reviews → umbrella
review; qualitative interpretive synthesis → qualitative meta-synthesis;
field mapping → bibliometric analysis. Use the generic `academic-workflow.md`
only for a standalone manuscript (primary study, theoretical paper,
commentary).

---

## Tooling reference

### `scripts/validate_skill.py`

Validates any skill directory's structure and completeness.

**Checks performed:**
- Directory structure (required `SKILL.md`, expected `references/`, `scripts/`, `assets/`)
- YAML frontmatter completeness (`name`, `description`, negative triggers present)
- Line count (warns if approaching the 500-line limit)
- Reference integrity (every file referenced in backtick paths actually exists)
- Zone classification (step headers labelled `Deterministic`, `Reasoning`, or `Judgment`)
- Quality gate presence
- Feedback loop presence
- Error handling section presence
- Required sections (`Quick Start`, `Entry Point`, `Skill Inventory`, `Quality Gates`, `State Persistence`)
- Sub-skill structure (if sub-skill `.md` files exist in the root)

**Output:** JSON to stdout. Exit code `0` on `PASS`/`PASS_WITH_WARNINGS`, `1` on `FAIL`.

---

### `scripts/scaffold_from_accelerator.py`

Generates a complete skill directory from a domain accelerator blueprint.

**What it generates:**
| Output | Description |
|---|---|
| `SKILL.md` | Master orchestrator pre-populated from the accelerator |
| `[skill-name].md` (× N) | One stub per sub-skill in the accelerator inventory |
| `[slug]-orchestrator.md` | Master controller stub |
| `[slug]-gate-verifier.md` | Gate enforcement stub |
| `[slug]-progress-tracker.md` | State tracking stub |
| `[slug]-feedback-router.md` | Feedback routing stub |
| `[slug]-state-schema.md` | State persistence schema (also saved as `state/state_template.json`) |
| `scripts/gate_N_validator.py` | One gate validator script per quality gate (stubs) |
| `references/[accelerator].md` | Copy of the accelerator for runtime reference |
| `SCAFFOLD_REPORT.json` | Summary of generated files and full TODO checklist |

**After scaffolding:** review `SCAFFOLD_REPORT.json`, fill in the TODO items
(domain-specific process steps, gate logic, deterministic scripts), run
`validate_skill.py`, then test with realistic prompts.

---

### `scripts/audit_trigger_collisions.py`

Compares a skill's `description:` field against all other `SKILL.md` files in
a library using lexical Jaccard similarity.

**Verdicts:**
- `PASS` — no skills exceed the overlap threshold (default 0.25). Not a
  guarantee of semantic distinctness; manually check the top-N neighbours.
- `WARN` — one or more skills exceed the threshold. Sharpen the description,
  add negative triggers, or rename before shipping.

**Exit codes:** `0` on `PASS`, `2` on `WARN`, `1` on usage error.

---

## Core design principles

Four empirical findings govern the skill's approach (treat as strong priors,
validate against your own evals):

1. **2–3 focused skills beat monoliths** — a well-scoped set outperforms both
   a mega-skill and a sprawl of 4+. Comprehensive documentation dumps hurt
   task success.
2. **Human-authored skills beat LLM-generated** — manual curation outperforms
   auto-generated skill content, with the largest gains in high-stakes domains.
3. **Curated skills are scale multipliers** — a smaller model with good skills
   often beats a larger model without them.
4. **Semantic distinctness is non-negotiable** — semantically-similar
   descriptions degrade selection accuracy sharply.

**The compounding reliability problem:** An 8-step workflow at 90% per-step
reliability yields only ~43% end-to-end success (`0.9⁸ ≈ 0.43`). Quality
gates and deterministic locking are the difference between a working pipeline
and a confidently-wrong one.

---

## Anti-patterns

Things the skill is explicitly designed to prevent — and that you should
avoid when building skills with it:

- **Monolithic mega-skills** — split at 500 lines
- **LLM self-generating skill content** — scaffolds structure, humans author process
- **Comprehensive documentation dumps** — move detail to `references/`, load JIT
- **Overlapping trigger descriptions** — run `audit_trigger_collisions.py` before shipping
- **LLMs doing calculations** — lock arithmetic and data transforms in deterministic scripts
- **Skipping quality gates** — errors compound exponentially across steps
- **Raw text handoffs between skills** — use structured JSON contracts
- **Skipping idempotency on retry-prone steps** — duplicate side-effects (double-charges, duplicate emails) are the classic production failure mode
- **Caching human approvals for high-stakes actions** — always require fresh consent
- **Proceeding silently past known issues** — halt or route back; never continue quietly

---

## Requirements

- Python 3.9+ (for the three scripts in `scripts/`)
- No external dependencies — all scripts use the Python standard library only
- Skills library at `~/.codex/skills/` (or set `CODEX_HOME` env variable to override)
