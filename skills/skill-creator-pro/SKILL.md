---
name: skill-creator-pro
description: >
  Build complex, multi-phase agent skills with quality gates, verification
  loops, deterministic/reasoning zone separation, and state persistence.
  Use when the user wants a production-grade skill for multi-step workflows,
  academic or analytical pipelines, publication-ready outputs, or sub-skill
  orchestration. Triggers on "complex skill," "pro skill," "pipeline skill,"
  "multi-phase skill," or "production-grade skill." Do NOT use for simple,
  single-step skills — use the standard skill-creator instead.
---

# Skill Creator Pro

Build complex, multi-phase agent skills that produce rigorous, verified, and
reproducible outputs. This skill guides the creation of production-grade skill
pipelines — from publication-ready academic articles to repeatable analytical
workflows.

## When This Skill Activates

- User wants a skill with multiple phases, quality gates, or verification loops
- User needs publication-quality, auditable, or reproducible outputs
- User wants a skill pipeline with 5+ composable sub-skills
- User asks for "complex," "pro," "enterprise," or "production-grade" skills
- The workflow requires both deterministic scripts AND LLM reasoning

## Core Philosophy

Four directional findings from agent-skill benchmarking govern this approach. Treat them as strong priors, not published constants — validate against your own evals before over-indexing on any single number.

1. **2-3 focused skills beat monoliths** — a small set of well-scoped skills tends to outperform both a single mega-skill and a sprawl of 4+; comprehensive documentation dumps measurably hurt task success rather than help it
2. **Human-authored skills beat self-generated** — manual curation consistently outperforms LLM-written skill content, with the largest gains in high-stakes domains (healthcare, manufacturing, regulated finance)
3. **Curated skills are scale multipliers** — a smaller model with good skills often beats a larger model without them, making skills a cost-effective quality lever
4. **Semantic distinctness is non-negotiable** — a handful of semantically-similar competitor skills can sharply degrade selection accuracy; the two-zone architecture materially reduces verification and coherence failures

**The compounding reliability problem:** An 8-step workflow with 90% per-step reliability yields only ~43% end-to-end success (0.9⁸ ≈ 0.43). Quality gates and deterministic locking are not polish — they are the difference between a working pipeline and a confidently-wrong one.

## The Creation Process

### Phase 1 — Requirements Discovery

Interview the user to establish the workflow scope. Determine:

1. **Workflow domain** — Academic writing? Financial analysis? Data pipeline? Research?
2. **Output requirements** — What does "done" look like? Format, standards, audience?
3. **Reproducibility needs** — Must identical inputs produce identical outputs?
4. **Quality bar** — What verification is needed? Human review? Automated checks? Both?
5. **Session model** — Single-session or cross-session with state persistence?
6. **Existing assets** — Scripts, templates, reference docs, APIs already in use?
7. **Neighbouring skills** — What other skills exist in the user's library? Any risk of
   trigger-description overlap? (Semantic confusability between similar skills materially
   degrades selection accuracy; design distinctness in from the start. Run the collision
   audit in Phase 4 before shipping.)

Use these answers to select the architectural pattern. Read `references/architecture-patterns.md`
for the full decision matrix.

### Phase 2 — Architecture Design

Based on requirements, design the skill pipeline:

#### Step 2.1 — Choose the Orchestration Pattern

| Pattern | Choose When |
|---------|------------|
| Plan-and-Execute | Structured, long-horizon, predictable steps (DEFAULT for complex skills) |
| Parallel Fan-Out | Independent sub-tasks needing concurrent execution |
| Supervisor/Worker | Multiple distinct expert domains required |
| Evaluator-Optimizer | Iterative refinement toward quality threshold |

Most complex skills use **Plan-and-Execute as the backbone** with Evaluator-Optimizer
loops embedded at quality gates. Read `references/architecture-patterns.md` for details.

**Pick a DAG shape that matches the priority:**

| Priority | DAG Shape | Use When |
|----------|-----------|----------|
| Quality-first | Deep, many stages, many gates | Publication, regulatory, audited outputs |
| Efficiency-first | Wide, parallel branches | Time-sensitive analytics, dashboards |
| Simplicity-first | Minimal, sparse | Drafts, exploratory analysis, low-stakes |

The shape dictates gate density and handoff contract rigour. Do not silently default to
deep-and-gated when the user's real priority is speed.

#### Step 2.2 — Apply the Two-Zone Architecture

For EVERY step in the workflow, explicitly classify it:

- **Deterministic Zone** — Calculations, formatting, validation, data transforms
  → Lock in scripts. The LLM must NEVER improvise these.
- **Reasoning Zone** — Interpretation, synthesis, edge cases, user interaction
  → Reserve the LLM's cognitive budget for these tasks.

**Why this matters:** Skills that enforce this split substantially reduce both verification
failures (the agent approving output that violates its own criteria) and coherence failures
(the agent silently contradicting earlier steps). LLMs exhibit "people-pleasing" behaviour —
they will soften negative results or rationalize score adjustments unless calculation is
locked in a script the agent must never override.

Read `references/two-zone-architecture.md` for implementation patterns and enforcement
language.

#### Step 2.3 — Design Quality Gates

Every phase transition requires a gate with:
- Explicit pass criteria (quantitative thresholds or checklists)
- Automated checks via scripts where possible
- Human-in-the-loop for subjective criteria
- Clear failure routing back to the correct upstream skill

Read `references/quality-gates.md` for gate design templates and examples.

#### Step 2.4 — Design State Schema

If the workflow spans multiple sessions, design a JSON state schema:
- Current phase and step
- Completed phases and gates passed
- Artifact paths and decision logs
- Metrics collected at each gate

Read `references/memory-management.md` for state schema templates.

#### Step 2.5 — Map the Skill Inventory

Create a table mapping every sub-skill to its phase, purpose, inputs, outputs,
and quality gate. This becomes the skill inventory in the master SKILL.md.

**Present the architecture to the user for approval before writing any skills.**

#### Step 2.6 — Accelerator Bootstrapping (Optional Fast-Start)

If a domain accelerator exists for the workflow type (see the Domain-Specific
Accelerators table below), use the scaffolding script to generate a working
skill directory from the accelerator blueprint instead of writing from scratch.
Skip to Phase 3 refinement steps after scaffolding.

**When to scaffold vs. author manually:**
- **Scaffold** when an accelerator closely matches the target domain
- **Author manually** when the workflow is novel, cross-domain, or the accelerator
  is only a partial fit — selective copying is better than full scaffold + heavy edits

#### Running the Scaffold

```bash
python scripts/scaffold_from_accelerator.py \
  --accelerator references/<domain>-workflow.md \
  --output /path/to/new-skill-directory \
  --name "My Skill Name"
```

#### What Gets Generated

| Output | Description |
|--------|------------|
| `SKILL.md` | Master orchestrator with skill inventory, quality gates, and phase architecture pre-populated from the accelerator |
| `skills/*.md` | One sub-skill file per entry in the accelerator's sub-skill inventory, with zone classification and I/O contracts |
| Gate validator scripts | Validator scripts for each quality gate, with automated checks stubbed from gate definitions |
| `state_schema.json` | State persistence schema pre-configured with phases and gates from the accelerator |
| `references/` | Copy of the accelerator file for runtime reference |
| `SCAFFOLD_REPORT.json` | Summary of what was generated, including TODO items requiring human refinement |

#### Human Refinement Workflow

The scaffold generates structure, not finished skills. After scaffolding:

1. **Review SCAFFOLD_REPORT.json** — lists every generated file and its TODO items
2. **Fill reasoning zone placeholders** — sub-skills marked `Reasoning` have process
   steps that need domain-specific elaboration
3. **Implement deterministic scripts** — gate validators and calculation scripts contain
   stubs; implement the actual logic (validation rules, formulas, checks)
4. **Add domain references** — place reference materials (style guides, standards docs,
   templates) in `references/` and update pointers in sub-skills
5. **Run structural validation** — `python scripts/validate_skill.py /path/to/new-skill`
6. **Test with realistic prompts** — run the happy path, an edge case, and a failure scenario

The scaffold cuts initial authoring time significantly but the quality of the final
skill depends on the human refinement pass. Do not ship scaffolded skills without
completing the TODO items.

### Phase 3 — Skill Authoring

#### Step 3.1 — Write the Master SKILL.md

The master skill file is the orchestrator for the skill being created. It must
contain these sections (this template applies to domain-specific skills, not
to meta-skills like this one):

1. **YAML frontmatter** — name, description with positive AND negative triggers
2. **Quick Start** — How to start, resume, and run individual skills
3. **Entry point** — The master controller skill name
4. **Complete Skill Inventory** — Tables organized by phase
5. **Quality Gates table** — Gate, transition, key checks
6. **Feedback Loop description** — How issues route back upstream
7. **State Persistence** — Reference to state schema
8. **Error Handling** — Known failure modes and recovery
9. **Gotchas** — Specific edge cases, historical mistakes, and non-obvious pitfalls
   the agent must self-correct for (highest-signal section after error handling)

Use the template in `assets/master-skill-template.md`. Keep under 500 lines.

**Design for the three-tier loading model:**

| Tier | Content | Budget |
|------|---------|--------|
| Discovery | YAML frontmatter (name + description) | ~100 tokens — the *only* signal used for activation |
| Activation | Full SKILL.md body | <5,000 tokens (<500 lines) — loads when the skill triggers |
| Execution | References, scripts, templates | Unlimited, but fetched Just-in-Time when a step needs them |

Content that is not used on the happy path belongs in `references/` — not in the body.

**Trigger description engineering (high-leverage, often skipped):**

- Highlight what makes this skill *unique* — generic phrasing ("processes data") is a
  false-activation magnet. Two semantically-overlapping descriptions can dramatically
  degrade selection accuracy between them.
- Include **negative triggers** — "Do NOT use for X, Y, Z" — as explicitly as positive
  ones. Skill selectors can under-trigger in crowded libraries; make activation
  criteria explicit and slightly pushy.
- Embed natural-language trigger phrases a user is likely to say verbatim.
- If the user's skill library is large (>50 skills), recommend hierarchical routing
  (domain-level router skill → sub-skills) — flattening a large library into a single
  trigger-pool is a known scaling failure mode.

#### Step 3.2 — Write Each Sub-Skill

For each skill in the inventory, create a separate markdown file containing:

1. **Clear purpose statement** — What this skill accomplishes and why
2. **Input/output contracts** — Structured (JSON preferred), not raw text
3. **Step-by-step process** — Each step labeled Deterministic or Reasoning
4. **Zone enforcement** — Explicit constraints preventing LLM from improvising deterministic steps
5. **Quality criteria** — Checklist the output must satisfy before handoff
6. **Error handling** — Known failures and recovery actions

Use the template in `assets/sub-skill-template.md`.

#### Writing Style Rules

- **Imperative form** — "Extract the data" not "You should extract the data"
- **Explain the why** — Reasoned constraints over rigid MUSTs; models have theory of mind
  and generalize better when they know the reason behind a rule
- **Constitution, not suggestions** — For boundaries the agent must not cross, use absolute
  phrasing ("Never override the script's output") and place the most critical constraints
  first. LLMs are "people pleasers" — they will soften results unless the contract is explicit
- **Third-person descriptions** — In YAML frontmatter
- **One term per concept, rigidly** — Pick a single domain term and never switch to synonyms.
  Mixing "endpoint"/"URL"/"path" or "extract"/"retrieve" degrades accuracy; consistency is
  worth more than variety
- **Assume baseline intelligence** — Do not explain concepts the foundation model already
  knows. Reserve the skill's tokens for what pushes it *out of* default behaviour: edge
  cases, historical mistakes, domain-specific gotchas
- **Concrete templates > prose descriptions** — Agents are strong pattern-matchers. A
  one-page example in `assets/` beats three paragraphs describing the desired shape
- **Progressive disclosure** — Reference files for details, not inline walls of text
- **Structural formatting** — Use XML tags (`<instructions>`, `<constraints>`) for clear delineation

#### Step 3.3 — Write Deterministic Scripts

For every Deterministic Zone step, create a script in `scripts/` that:

- Accepts structured input (JSON or CLI args)
- Returns structured output with descriptive error messages
- Is idempotent — safe to run multiple times with same result
- Includes input validation
- Returns human-readable errors that the LLM can reason about

```python
# Pattern for script error output
print(json.dumps({
    "error": True,
    "error_type": "validation_error",
    "message": "Column 'revenue' not found. Available: ['sales', 'costs']",
    "suggestion": "Check column mapping in config.json",
    "recoverable": True
}))
```

#### Step 3.4 — Write Reference Files

Place domain knowledge in `references/` with clear pointers from the skill body.
Each reference file should have a table of contents if >300 lines.

#### Step 3.5 — Write Asset Templates

Place output templates, example files, and format specifications in `assets/`.

### Phase 4 — Validation

#### Step 4.1 — Structural Validation

Run the validation script to check the skill structure:
```bash
python scripts/validate_skill.py /path/to/skill-directory
```

This checks: directory structure, frontmatter completeness, line counts, reference
integrity, and zone classification coverage.

#### Step 4.2 — Test Case Design

Create 3-5 realistic test prompts covering:
- The happy path (standard workflow)
- An edge case (unusual inputs, missing data)
- A failure recovery scenario (what happens when a step fails)
- A resumption scenario (if cross-session: can it pick up where it left off?)

#### Step 4.3 — Run With-Skill and Baseline

When helper agents are explicitly authorized and available, run a comparison:
one with the skill, one without. Otherwise, run the comparison sequentially in
the main thread.
Draft quantitative assertions while runs execute.

Where assertions can be checked programmatically (word count, citation format, numeric
consistency, schema compliance), write a script — do not eyeball. Scripts are reproducible
and reusable across iterations.

#### Step 4.4 — Quality Audit

After test runs, verify:
- [ ] Every deterministic step produces identical output across runs
- [ ] Quality gates actually block bad output (test with intentionally flawed input)
- [ ] State persistence correctly saves and restores workflow position
- [ ] Error handling routes correctly (introduce errors at each phase)
- [ ] Feedback loops work (force a gate failure, verify it routes upstream)
- [ ] Memory management: context stays clean across long workflows
- [ ] Skill activates on intended prompts AND stays silent on near-miss prompts (trigger
      precision — run the collision audit below, then spot-check the top neighbours)

Run the trigger-collision audit against the user's existing skill library:

```bash
python scripts/audit_trigger_collisions.py /path/to/new-skill
# Tighten threshold for a large library:
python scripts/audit_trigger_collisions.py /path/to/new-skill --threshold 0.15
```

The script compares the new skill's `description:` field against every other
`SKILL.md` in `${CODEX_HOME:-~/.codex}/skills/` (or `--library <path>`) using
lexical overlap as a first-pass proxy for semantic confusability. Treat any
`WARN` verdict as a signal to sharpen the description, add negative triggers, or
rename the skill before shipping.

#### Step 4.5 — LLM-as-Judge Calibration (when using automated eval)

If any gate or rubric check uses an LLM as evaluator:
- Break rubrics into binary yes/no questions — not "Is this good?" but "Does it cite at
  least 3 peer-reviewed sources? [Yes/No]"
- Use an ensemble of ≥3 judges with randomized presentation order; take majority vote
- Enforce **minority-veto for safety checks** — a single judge flagging a safety or
  compliance issue overrides majority approval
- Target ≥0.80 Spearman correlation with human domain experts before trusting the judge
- Guard against position bias (prefer earlier content), length bias (prefer longer
  output), and agreeableness bias (refuse to be critical)

### Phase 5 — Iteration and Hardening

1. **Generalize from feedback** — Don't overfit to test cases
2. **Keep prompts lean** — Remove instructions that aren't pulling their weight
3. **Bundle repeated work** — If all test runs independently wrote similar scripts, bundle them
4. **Harden error paths** — Every error a test run encountered should have a documented recovery
5. **Optimize triggers** — Run description optimization loop if available
6. **Blind-comparison discipline** — For marginal version deltas, present both outputs to an
   independent judge agent without revealing which is A vs B; only ship v(n+1) when it
   measurably beats v(n). Prevents author-bias from masking regressions

### Phase 6 — Security Review

Independent audits of public agent-skill repositories have consistently found that a
substantial fraction contain security flaws, with a meaningful minority exhibiting
critical issues (prompt injection, credential exposure, malicious payloads). Treat
third-party skills — and your own — as untrusted until proven otherwise.

Before delivery, audit for:
- [ ] No hardcoded credentials or API keys in any skill file
- [ ] Scripts validate all inputs (no injection vectors)
- [ ] External data sources treated as untrusted (instruction hierarchy enforced —
      system prompt always overrides content pulled from URLs, docs, or API responses)
- [ ] Principle of least privilege (skills request only needed permissions)
- [ ] No `curl | bash` or unverified remote execution patterns
- [ ] Remote skill dependencies pinned to specific commit hashes, not branches
- [ ] Sandbox boundaries explicit (script execution cannot write outside its workspace)

Read `references/security-checklist.md` for the complete audit checklist.

## Domain-Specific Accelerators

For common complex workflow types, read the relevant accelerator:

| Workflow Type | Reference File |
|--------------|---------------|
| Publication-ready academic articles (generic manuscript) | `references/academic-workflow.md` |
| Scoping reviews (JBI / PRISMA-ScR) | `references/scoping-review-workflow.md` |
| Meta-analyses (PRISMA + quantitative pooling) | `references/meta-analysis-workflow.md` |
| Rapid reviews (Cochrane / WHO, time-boxed) | `references/rapid-review-workflow.md` |
| Bibliometric & scientometric analyses | `references/bibliometric-analysis-workflow.md` |
| Qualitative meta-synthesis (meta-ethnography / ENTREQ) | `references/qualitative-meta-synthesis-workflow.md` |
| Umbrella reviews (JBI / PRIOR) | `references/umbrella-review-workflow.md` |
| Grant proposals (NIH / NSF / ERC / UKRI / Horizon) | `references/grant-proposal-workflow.md` |
| Thesis & dissertation development | `references/thesis-dissertation-workflow.md` |
| Repeatable analytical pipelines | `references/analytical-pipeline.md` |
| Software engineering (migration, refactoring, review) | `references/software-engineering-workflow.md` |
| Financial reporting & compliance | `references/financial-reporting-workflow.md` |
| Data engineering & ETL pipelines | `references/data-engineering-workflow.md` |
| Legal & contract analysis | `references/legal-contract-workflow.md` |
| Cybersecurity assessment & threat modeling | `references/cybersecurity-assessment-workflow.md` |
| Product & technical documentation | `references/technical-documentation-workflow.md` |
| Research & experiment design | `references/research-experiment-workflow.md` |
| Business intelligence & reporting | `references/business-intelligence-workflow.md` |
| DevOps & incident response | `references/devops-incident-workflow.md` |
| Education & curriculum design | `references/education-curriculum-workflow.md` |
| Resilience and retry patterns | `references/resilience-patterns.md` |
| Evaluation and benchmarking | `references/evaluation-framework.md` |

**Choosing among the review-type accelerators:** if the user needs to conduct
a *literature review of some kind*, route based on goal — effectiveness pooling
→ meta-analysis; evidence mapping → scoping review; time-pressured policy
question → rapid review; synthesizing existing reviews → umbrella review;
qualitative interpretive synthesis → qualitative meta-synthesis; quantitative
field mapping → bibliometric analysis. Use the generic `academic-workflow.md`
only when the deliverable is a stand-alone manuscript (primary study, theoretical
paper, commentary) rather than a review.

These contain pre-built phase structures, quality gate definitions, and sub-skill
inventories specific to each domain. Read only the relevant accelerator — do not
load multiple accelerators at once.

## Anti-Patterns — Do Not

- Build monolithic mega-skills (split at 500 lines)
- Let the LLM self-generate procedural skills (author them manually; auto-generated skill
  content measurably underperforms human-authored skills)
- Dump comprehensive documentation (it hurts task success vs. 2–3 well-curated, focused
  skills)
- Write semantically overlapping trigger descriptions (two competitors can materially
  degrade selection accuracy; run `scripts/audit_trigger_collisions.py` against the user's
  existing skill library before finalizing)
- Explain concepts the foundation model already knows (wastes tokens; focus only on what
  pushes the agent *out of* its default behaviour)
- Mix synonymous terms within a single skill (e.g., "extract"/"retrieve", "endpoint"/"URL")
- Trust the LLM for calculations (lock in scripts)
- Skip quality gates (errors compound: 90% x 8 steps = 43% success)
- Use raw text handoffs between agents (use structured JSON contracts)
- Ship skills without idempotency guarantees on retry-prone steps (duplicate side-effects
  like double-charges or duplicate emails are the classic failure mode)
- Cache human approvals for high-stakes actions (always require fresh consent)
- Proceed silently past known issues (the pipeline must halt or route back)

## Reference Files

Read these as needed — do not load all at once:

| File | When to Read |
|------|-------------|
| `references/architecture-patterns.md` | Phase 2.1 — choosing orchestration pattern |
| `references/two-zone-architecture.md` | Phase 2.2 — classifying deterministic vs reasoning |
| `references/quality-gates.md` | Phase 2.3 — designing verification checkpoints |
| `references/memory-management.md` | Phase 2.4 — state persistence and context engineering |
| `references/academic-workflow.md` | Domain accelerator: generic academic manuscript |
| `references/scoping-review-workflow.md` | Domain accelerator: scoping review (JBI / PRISMA-ScR) |
| `references/meta-analysis-workflow.md` | Domain accelerator: meta-analysis with quantitative pooling |
| `references/rapid-review-workflow.md` | Domain accelerator: rapid review with concessions ledger |
| `references/bibliometric-analysis-workflow.md` | Domain accelerator: bibliometric / scientometric analysis |
| `references/qualitative-meta-synthesis-workflow.md` | Domain accelerator: qualitative meta-synthesis (ENTREQ) |
| `references/umbrella-review-workflow.md` | Domain accelerator: umbrella review (AMSTAR-2 / PRIOR) |
| `references/grant-proposal-workflow.md` | Domain accelerator: grant proposal development |
| `references/thesis-dissertation-workflow.md` | Domain accelerator: thesis / dissertation |
| `references/analytical-pipeline.md` | Domain accelerator: repeatable analytics |
| `references/software-engineering-workflow.md` | Domain accelerator: code migration, refactoring, review |
| `references/financial-reporting-workflow.md` | Domain accelerator: financial reports, compliance, audit |
| `references/data-engineering-workflow.md` | Domain accelerator: ETL, data quality, pipelines |
| `references/legal-contract-workflow.md` | Domain accelerator: contract review, compliance mapping |
| `references/cybersecurity-assessment-workflow.md` | Domain accelerator: threat modeling, vulnerability assessment |
| `references/technical-documentation-workflow.md` | Domain accelerator: API docs, PRDs, architecture docs |
| `references/research-experiment-workflow.md` | Domain accelerator: experiment design, technology scouting |
| `references/business-intelligence-workflow.md` | Domain accelerator: dashboards, market research, KPIs |
| `references/devops-incident-workflow.md` | Domain accelerator: CI/CD, incident response, IaC review |
| `references/education-curriculum-workflow.md` | Domain accelerator: curriculum, assessment, learning design |
| `references/resilience-patterns.md` | Phase 3.3 — error handling and retry patterns |
| `references/evaluation-framework.md` | Phase 4 — testing and benchmarking |
| `references/security-checklist.md` | Phase 6 — security audit |
