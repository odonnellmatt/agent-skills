# Quality Gates and Verification Loops

## Table of Contents

1. [Gate Design Principles](#gate-design-principles)
2. [Gate Architecture Template](#gate-architecture-template)
3. [Maker-Checker Pattern](#maker-checker-pattern)
4. [Multi-Layered Guardrails](#multi-layered-guardrails)
5. [Feedback Loop Routing](#feedback-loop-routing)
6. [Human-in-the-Loop Checkpoints](#human-in-the-loop-checkpoints)
7. [Example Gate Implementations](#example-gate-implementations)

---

## Gate Design Principles

Every quality gate must satisfy five requirements:

1. **Explicit pass criteria** — Quantitative thresholds or checklist items, never vague
2. **Automated where possible** — Run a script for objective criteria, not an LLM judgment
3. **Human review for subjective criteria** — Pause and surface progress for approval
4. **Failure routing** — Clear instructions for what happens when a gate fails
5. **No silent pass-through** — The pipeline MUST halt or route back on known issues

### Why Gates Matter Mathematically

Without gates, an error at step 3 propagates silently through steps 4-12 and
contaminates the final output. With gates, the error is caught at step 3 and
routed back for correction. The cost of fixing at step 3 is dramatically lower
than fixing at step 12 (when the error has compounded through 9 downstream steps).

---

## Gate Architecture Template

```markdown
## Quality Gate [N]: [Phase A] → [Phase B]

### Automated Checks (run before human review)
```bash
python scripts/gate_[N]_validator.py --input [path] --criteria [path]
```

Script validates:
- [ ] [Specific measurable criterion 1]
- [ ] [Specific measurable criterion 2]
- [ ] [Specific measurable criterion 3]

### Human Review Items
Present the following to the user for approval:
- [ ] [Subjective criterion 1 — what to look for]
- [ ] [Subjective criterion 2 — what to look for]

### Pass Criteria
ALL automated checks must pass AND human approval received.

### On Failure
- If [criterion 1] fails → Route to [specific upstream skill] with feedback: "[what to fix]"
- If [criterion 2] fails → Route to [specific upstream skill] with feedback: "[what to fix]"
- If human rejects → Present rejection reason, route to [appropriate skill]
```

---

## Maker-Checker Pattern

Separate generation from evaluation using distinct agent roles or sequential steps:

```
MAKER (Generator)                    CHECKER (Evaluator)
─────────────────                    ────────────────────
Generate Section N                   Evaluate against rubric:
following outline                    - Factual accuracy
and style guide                      - Methodological rigor
         │                           - Format compliance
         └──── Draft ────────────→   - Logical coherence
                                     - Completeness
         ┌──── Feedback ─────────    
         │                           Verdict:
    Revise based on                  PASS → proceed
    specific feedback                FAIL → return with specifics
         │
         └──── Revised Draft ───→    Re-evaluate
                                     (max 3 cycles)
                                     
                                     Still failing after 3?
                                     → Escalate to human
```

### Implementation in SKILL.md

```markdown
## Step 5: Write Methods Section (Maker-Checker)

### 5a — Draft (Reasoning Zone)
Write the Methods section following the approved outline from Phase 1.
Include: search strategy, screening process, quality assessment approach,
data extraction method, and synthesis technique.

### 5b — Review (Automated + Reasoning)
Run structural validation:
```bash
python scripts/section_validator.py --section methods --draft output/methods.md
```

Then evaluate the draft against these criteria:
1. Does the search strategy specify exact databases and date ranges?
2. Are inclusion/exclusion criteria operationalized (not vague)?
3. Is the quality assessment tool named and justified?
4. Would another researcher be able to replicate this process?

### 5c — Revision Protocol
If any criterion fails:
- Return the draft to Step 5a with specific feedback citing which criterion failed
- Include the exact text that needs revision and why
- Maximum 3 revision cycles
- After 3 cycles: present current draft to user with flagged issues for manual resolution

WHY max 3 cycles: Empirical testing shows diminishing returns. If the core issue
isn't resolved by iteration 3, it typically requires human domain judgment.
```

---

## Multi-Layered Guardrails

```
Layer 1: INPUT VALIDATION
├── Block out-of-scope requests before processing
├── Validate data formats and schemas
└── Check required fields and parameters

Layer 2: TOOL GATE
├── Validate script parameters before execution
├── Constrain blast radius (read-only where possible)
└── Enforce rate limits on external API calls

Layer 3: REASONING GUARDRAILS
├── Re-anchor to original objective every N steps
├── Check for logical consistency in outputs
└── Detect hallucination patterns (claims without sources)

Layer 4: OUTPUT VALIDATION
├── Schema compliance check
├── Scan for PII or restricted information
├── Verify all citations/references exist
└── Run deterministic quality metrics

Layer 5: DELIVERY GATE
├── Final format validation
├── Human approval for publication/sharing
└── Audit trail completeness check
```

---

## Feedback Loop Routing

When an issue is detected at any phase, automatically identify and route back to
the correct upstream skill. The pipeline must never silently proceed with known issues.

### Routing Decision Table Template

| Issue Detected At | Issue Type | Route To | Feedback |
|-------------------|-----------|----------|----------|
| Synthesis | Insufficient data coverage | Data Extraction | "Missing data for [topic]. Extract from [specific studies]." |
| Writing | Citation not in reference library | Search phase | "Reference [X] not found. Verify or replace." |
| Quality gate | Kappa below threshold | Screening calibration | "Agreement on [criteria] is low. Recalibrate." |
| Verification | Inconsistent numbers | Data extraction | "Table 3 totals don't match PRISMA flow." |

### Implementation Pattern

```markdown
## Feedback Loop Router

When the quality gate verifier or any downstream skill detects an issue:

1. Classify the issue type (data gap, quality failure, format error, logic error)
2. Identify the responsible upstream skill using the routing table
3. Package the issue as structured feedback:
   ```json
   {
     "issue_type": "data_gap",
     "detected_at": "synthesis",
     "route_to": "data-extractor",
     "feedback": "Missing outcome data for studies S12, S15, S23",
     "severity": "blocking",
     "gate_affected": "QG5"
   }
   ```
4. Re-invoke the upstream skill with this feedback appended to its input
5. After the upstream skill completes, re-run the failed gate check
```

---

## Human-in-the-Loop Checkpoints

### When HITL Is Mandatory

- Irreversible actions (publishing, sending, deleting)
- Subjective quality judgments (is this argument convincing?)
- Methodology decisions (which analytical approach to use)
- Conflict resolution (contradictory evidence from sources)
- Final approval before delivery

### When HITL Is Optional

- Structural validation (can be automated)
- Format checking (script-based)
- Intermediate progress updates (informational only)

### HITL Implementation

```markdown
## Human Review Checkpoint

### What to Present
- Current phase and step
- Summary of work completed since last checkpoint
- Specific items requiring human judgment
- Recommended action with reasoning

### How to Present
Format as a concise decision point:
"Phase 3 complete. 42 studies screened, 18 included. Kappa = 0.78 (substantial).
Three borderline cases need your input: [list with context for each].
Approve to proceed to quality assessment, or flag specific concerns."

### After Approval
Log the approval with timestamp and any modifications the user requested.
Update state schema. Proceed to next phase.

### After Rejection
Log the rejection reason. Route to the appropriate upstream skill with the
user's feedback. Do not re-prompt for approval on the same content without
making the requested changes.
```

---

## Example Gate Implementations

### Academic Writing — Gate Between Drafting and Verification

```markdown
## QG5: Drafting → Verification

### Automated Checks
```bash
python scripts/manuscript_validator.py --manuscript output/draft.md
```

Validates:
- [ ] Word count within target range (6,000-10,000)
- [ ] All required sections present (Abstract, Introduction, Methods, Results, Discussion, Conclusion)
- [ ] All figures/tables referenced in text
- [ ] All in-text citations have corresponding reference list entries
- [ ] No orphan references (in list but not cited in text)

### Human Review
- [ ] Arguments flow logically from evidence to conclusions
- [ ] Tone is appropriate for target journal
- [ ] Limitations section is substantive (not perfunctory)
- [ ] Contribution to the field is clearly articulated

### Pass: ALL automated checks pass AND human approval
### Fail: Route to manuscript-drafter with specific feedback
```

### Analytical Pipeline — Gate Between Calculation and Interpretation

```markdown
## QG3: Calculation → Interpretation

### Automated Checks
```bash
python scripts/calculation_validator.py --results data/calculations.json
```

Validates:
- [ ] All required metrics calculated (no nulls)
- [ ] Values within plausible ranges (no negative percentages, ratios > 0)
- [ ] Checksums match (totals equal sum of components)
- [ ] Calculation reproducible (re-run script, compare output hashes)

### Pass: ALL automated checks pass (no human review needed for math)
### Fail: Route to calculation script with error details
```

---

## Related References

- `two-zone-architecture.md` — Automated gate checks must be Deterministic Zone scripts
- `architecture-patterns.md` — Gates sit between phases in Plan-and-Execute patterns
- `memory-management.md` — Gate results should be saved to state for cross-session continuity
- `resilience-patterns.md` — Gate failures trigger retry/fallback routing
