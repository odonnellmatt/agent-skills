# Domain Accelerator: Grant Proposal Development Workflows

## Table of Contents

1. [Overview](#overview)
2. [Funder Variants](#funder-variants)
3. [Phase Architecture](#phase-architecture)
4. [Sub-Skill Inventory](#sub-skill-inventory)
5. [Quality Gate Definitions](#quality-gate-definitions)
6. [Specific Aims Page Protocol](#specific-aims-page-protocol)
7. [Scoring Rubric Alignment](#scoring-rubric-alignment)
8. [Budget and Budget-Justification Protocol](#budget-and-budget-justification-protocol)
9. [Compliance and Required Documents](#compliance-and-required-documents)
10. [Common Failure Modes](#common-failure-modes)

---

## Overview

A grant proposal must persuade a review panel that the proposed project is
significant, innovative, feasible, and led by a capable team — under rigid
word/page/format constraints, enforced compliance requirements, and
funder-specific scoring rubrics.

**Recommended architecture:** Plan-and-Execute backbone with Evaluator-Optimizer
loops tuned to the funder's scoring rubric. Every major section is drafted, then
critiqued against the rubric, then revised.

**Critical constraint:** Page/word/format limits are deterministic and hard. The
Deterministic Zone enforces them. The Reasoning Zone never rewrites them away.

---

## Funder Variants

The accelerator adapts to the target funder's structure:

| Funder | Key Sections | Distinctive Requirements |
|--------|-------------|--------------------------|
| NIH (R01, R21, K-series) | Specific Aims, Research Strategy (Significance, Innovation, Approach) | Human subjects, rigor & reproducibility, authentication of key resources |
| NSF | Project Summary (Overview / Intellectual Merit / Broader Impacts), Project Description | Broader Impacts mandatory, data management plan |
| ERC (StG/CoG/AdG) | B1 (extended synopsis, CV, track record), B2 (scientific proposal) | Risk & feasibility section, ground-breaking nature |
| Horizon Europe | Excellence / Impact / Implementation | Work packages, deliverables, milestones, consortium |
| UKRI (Responsive Mode) | Case for Support, Pathways to Impact | Justification of resources narrative |
| Wellcome | Research Question + Approach, Team | Commitment to open research practices |
| Private foundations | Variable; often LOI → full proposal | Mission alignment, often narrower format |

The protocol step detects funder from input and loads the matching template.

---

## Phase Architecture

```
Phase 1: Opportunity Analysis (3 skills)
    ↓ QG1: Fit confirmed, scoring rubric loaded, timeline built backward from deadline
Phase 2: Idea Development (4 skills)
    ↓ QG2: Specific Aims (or equivalent) passes 1-page panel test
Phase 3: Research Plan Drafting (5 skills)
    ↓ QG3: Approach passes feasibility and rigor checks
Phase 4: Supporting Sections (5 skills)
    ↓ QG4: Budget, biosketches, DMP, facilities, compliance documents complete
Phase 5: Rubric-Aligned Review (3 skills)
    ↓ QG5: Mock-panel score meets funder threshold
Phase 6: Compliance and Submission (3 skills)
    ↓ QG6: All funder format rules validated; submission package assembled
```

---

## Sub-Skill Inventory

### Phase 1 — Opportunity Analysis

| # | Skill | Purpose | Zone |
|---|-------|---------|------|
| 1 | `opportunity-analyzer` | Parse FOA/call text, extract scope, eligibility, budget limits | Mixed |
| 2 | `fit-scorer` | Score PI/institution fit against call priorities | Reasoning |
| 3 | `submission-timeline-builder` | Backward-plan with institutional review and internal deadlines | Deterministic |

### Phase 2 — Idea Development

| # | Skill | Purpose | Zone |
|---|-------|---------|------|
| 4 | `problem-statement-crafter` | Articulate the problem, gap, and why now | Reasoning |
| 5 | `aims-drafter` | Draft 2-4 Specific Aims (or equivalent) | Reasoning |
| 6 | `conceptual-framework-builder` | Build figure + narrative of the conceptual model | Reasoning |
| 7 | `aims-page-compiler` | Assemble Specific Aims page and verify one-page limit | Deterministic |

### Phase 3 — Research Plan Drafting

| # | Skill | Purpose | Zone |
|---|-------|---------|------|
| 8 | `significance-writer` | Significance section — why this matters | Reasoning |
| 9 | `innovation-writer` | Innovation section — what's new | Reasoning |
| 10 | `approach-writer` | Approach per aim — rigor, reproducibility, timelines | Reasoning |
| 11 | `preliminary-data-curator` | Assemble preliminary data figures and captions | Mixed |
| 12 | `rigor-reproducibility-auditor` | Authenticate reagents, describe RRIDs, SABV | Mixed |

### Phase 4 — Supporting Sections

| # | Skill | Purpose | Zone |
|---|-------|---------|------|
| 13 | `budget-builder` | Build budget per funder categories with rates | Deterministic |
| 14 | `budget-justifier` | Prose justification for each budget line | Reasoning |
| 15 | `biosketch-compiler` | Build NIH/NSF biosketches per current format | Deterministic |
| 16 | `dmp-author` | Data management plan per funder policy | Reasoning |
| 17 | `facilities-resources-writer` | Describe available resources and environment | Reasoning |

### Phase 5 — Rubric-Aligned Review

| # | Skill | Purpose | Zone |
|---|-------|---------|------|
| 18 | `rubric-critic` | Score draft against funder rubric, identify weaknesses | Reasoning |
| 19 | `mock-panel-simulator` | Role-play reviewer critiques from multiple perspectives | Reasoning |
| 20 | `revision-tracker` | Map each critique to a concrete revision | Deterministic |

### Phase 6 — Compliance and Submission

| # | Skill | Purpose | Zone |
|---|-------|---------|------|
| 21 | `format-validator` | Verify page/word/font/margin per funder rules | Deterministic |
| 22 | `required-documents-checker` | Check every required document is present | Deterministic |
| 23 | `submission-packager` | Produce final submission-ready package | Deterministic |

---

## Quality Gate Definitions

### QG1: Opportunity → Idea

**Automated:**
- [ ] FOA/call reference stored with retrieval date
- [ ] Scoring rubric loaded
- [ ] Eligibility verified (PI, institution, career stage, country)
- [ ] Budget ceiling and duration recorded
- [ ] Timeline built backward from deadline with ≥1 internal review milestone

**Human Review:**
- [ ] Fit is genuine, not stretched to claim relevance
- [ ] Timeline is achievable

### QG2: Idea → Research Plan

**Automated:**
- [ ] Aims count matches funder convention (NIH R01: 2-3, K: 2-3, etc.)
- [ ] Each aim has hypothesis, rationale, and approach summary
- [ ] Aims page fits one page with required font/margin
- [ ] Conceptual figure exists with caption

**Human Review:**
- [ ] Aims are independent but synergistic (not stacked dependencies)
- [ ] A single failed aim does not collapse the entire project

### QG3: Research Plan → Supporting Sections

**Automated:**
- [ ] Each aim has: design, methods, analysis plan, timeline, expected outcomes, pitfalls, alternatives
- [ ] Sample size / power justification present where applicable
- [ ] Preliminary data figures referenced in text with ID
- [ ] Rigor and reproducibility elements addressed (NIH) or equivalent
- [ ] Word/page counts within funder limits

**Human Review:**
- [ ] Alternative strategies are substantive, not boilerplate
- [ ] Methods match the skills of the proposed team

### QG4: Supporting → Review

**Automated:**
- [ ] Budget reconciles: totals, indirect rate, subawards
- [ ] Budget justification covers every line item
- [ ] Biosketches in current funder format (NIH: current biosketch; NSF: current biographical sketch)
- [ ] DMP addresses all funder-required elements
- [ ] Facilities and equipment described for every listed site

**Human Review:**
- [ ] Budget is defensible (neither padded nor unrealistically lean)

### QG5: Review → Submission

**Automated:**
- [ ] Rubric score computed with per-criterion rationale
- [ ] Each mock critique mapped to a revision status (addressed / declined with rationale)
- [ ] Revised draft passes rubric re-score ≥ threshold

**Human Review:**
- [ ] Mock critiques include friendly and hostile reviewer personas
- [ ] Revisions haven't introduced new weaknesses

### QG6: Submission → Delivery

**Automated:**
- [ ] Format validator: page count, font, margins, line spacing per funder rules
- [ ] All required documents present with correct filenames
- [ ] Attachment naming conforms to funder schema
- [ ] Submission checklist fully marked

**Human Review:**
- [ ] Final read-through approval by PI
- [ ] Institutional sign-offs collected

---

## Specific Aims Page Protocol

The NIH Specific Aims page (or equivalent) is the single most predictive
element of success. Target structure:

```
Paragraph 1 — Significance + gap (the problem in the world)
Paragraph 2 — Long-term goal + overall objective + central hypothesis + rationale
Paragraph 3 — Specific Aims (2-3), each with hypothesis + approach summary
Paragraph 4 — Innovation + expected outcomes + positive impact
```

**Deterministic checks:**
- Fits in one page with funder-specified font and margins
- ≥2 and ≤4 aims
- Every aim begins with verb phrase (*Determine...*, *Test...*, *Develop...*)
- Hypothesis statement present for hypothesis-driven aims

**Reasoning evaluations (rubric critic):**
- Significance: is the problem compelling?
- Innovation: genuinely new, or incremental?
- Feasibility: can this team do this with these resources?
- Independence of aims: does failure of aim 1 invalidate aims 2-3?

---

## Scoring Rubric Alignment

Each funder has a scoring framework. Example NIH criteria:

| Criterion | Scored 1-9 | Anchor |
|-----------|-----------|--------|
| Significance | Yes | Important problem, advances field if successful |
| Investigator(s) | Yes | Appropriately trained, productive, collaborative |
| Innovation | Yes | Shifts paradigm, novel methods/concepts |
| Approach | Yes | Rigorous, feasible, addresses pitfalls |
| Environment | Yes | Facilities support project, collaborators |
| Overall Impact | Narrative | Aggregate likelihood of sustained influence |

The rubric critic produces a weighted score + per-criterion critique. Mock-panel
simulator role-plays ≥3 reviewer personas (champion / skeptic / methodologist).

---

## Budget and Budget-Justification Protocol

```python
# budget_builder.py — Deterministic
{
    "personnel": [
        {"role": "PI", "effort_months": 3.0, "base_salary": 180000,
         "fringe_rate": 0.30, "total": ...}
    ],
    "equipment": [...],
    "travel": [...],
    "other_direct": [...],
    "subawards": [...],
    "indirect_cost_rate": 0.625,
    "indirect_base": "MTDC",  # modified total direct costs
    "totals": {"direct": ..., "indirect": ..., "total": ...}
}
```

Every line must have corresponding justification prose. The budget justifier
writes prose only for line items present in the budget — no orphan
justifications, no unjustified lines.

---

## Compliance and Required Documents

Typical NIH R01 submission package (example):

| Document | Source |
|----------|--------|
| Cover letter | Institution / PI |
| Project Summary (abstract) | Aims-summary derived |
| Project Narrative (public) | Plain-language summary |
| Specific Aims | Phase 2 output |
| Research Strategy | Phase 3 output |
| Bibliography & References Cited | Citation manager export |
| Biosketches (PI + all senior personnel) | Phase 4 output |
| Budget + Justification | Phase 4 output |
| Facilities & Other Resources | Phase 4 output |
| Equipment | Phase 4 output |
| Human Subjects / Vertebrate Animals / Select Agents | If applicable |
| Data Management and Sharing Plan | Phase 4 output |
| Authentication of Key Biological / Chemical Resources | If applicable |
| Letters of Support | Collaborators |

The required-documents checker matches the funder's exact list and fails if any
item is missing or misfiled.

---

## Common Failure Modes

| Failure | Cause | Prevention |
|---------|-------|------------|
| Over-length pages | Writing-first approach | Format validator runs on every draft |
| Aims too dependent | Aim 2 needs Aim 1's result | QG2 reviews independence |
| Weak significance framing | Jumps to methods without problem framing | Dedicated significance section |
| Innovation claimed, not substantiated | Lists methods without novelty argument | Innovation writer requires contrast with status quo |
| Preliminary data missing for key aims | Reviewers distrust feasibility | Preliminary-data curator flags aims without data |
| Budget-justification mismatch | Lines in budget lack justification prose | Script cross-checks line ↔ prose mapping |
| Biosketch wrong format | Uses outdated NIH format | Compiler pulls current template |
| DMP generic | Copy-pasted boilerplate | DMP author follows funder-specific required elements |
| Ignored rubric | Writes to general quality, not funder criteria | Rubric critic scored before submission |
| Hostile reviewer wins | Mock panel only simulates friendly reviewers | Mock-panel requires skeptic persona |
| Missed compliance attachment | Humans often forget human-subjects / DMP / etc. | Required-documents checker blocks QG6 |
| Deadline crunch cuts review | No internal-review milestone | Timeline built backward with mandatory buffers |
