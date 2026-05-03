# Domain Accelerator: Thesis & Dissertation Workflows

## Table of Contents

1. [Overview](#overview)
2. [Thesis Structure Variants](#thesis-structure-variants)
3. [Phase Architecture](#phase-architecture)
4. [Sub-Skill Inventory](#sub-skill-inventory)
5. [Quality Gate Definitions](#quality-gate-definitions)
6. [Chapter-Level Coherence Protocol](#chapter-level-coherence-protocol)
7. [Supervisor Feedback Integration](#supervisor-feedback-integration)
8. [Viva / Defense Preparation](#viva--defense-preparation)
9. [Institutional Compliance](#institutional-compliance)
10. [Common Failure Modes](#common-failure-modes)

---

## Overview

A doctoral thesis/dissertation is the longest sustained academic writing
project most researchers undertake — typically 80,000–100,000 words (monograph)
or a collection of 3-5 papers bridged by a wrapper (by-publication). The
accelerator supports both models across multiple phases and institutional review
stages.

**Recommended architecture:** Plan-and-Execute with cross-session state
persistence (chapters span months), Evaluator-Optimizer loops per chapter, and
a global coherence checker that operates across chapters.

**Critical constraint:** The thesis is not one large draft. It is a set of
interdependent chapters whose arguments must cohere while each chapter also
stands alone to some degree. The accelerator enforces this dual requirement.

---

## Thesis Structure Variants

| Model | Structure | When Suitable |
|-------|-----------|---------------|
| Traditional monograph | Intro → Lit review → Methods → Results (1-3 ch) → Discussion → Conclusion | Single coherent study program |
| Thesis by publication | Wrapper → Published/submitted papers as chapters → Synthesis | STEM; disciplines valuing publications |
| Hybrid | Framework chapters + paper chapters | Common compromise |
| Practice-based | Artifact + exegesis | Creative disciplines |
| Three-essay (economics) | Three self-contained essays with shared theme | Economics, some social sciences |

The protocol step loads the institution's regulations and selects the template.

---

## Phase Architecture

```
Phase 1: Scoping and Proposal (3 skills)
    ↓ QG1: Research programme, timeline, structure approved by supervisor
Phase 2: Per-Chapter Development (5 skills × N chapters)
    ↓ QG2 (per chapter): Chapter draft passes supervisor milestone
Phase 3: Cross-Chapter Integration (4 skills)
    ↓ QG3: Thread of argument verified, redundancy removed, voice consistent
Phase 4: Front / Back Matter and Compliance (4 skills)
    ↓ QG4: Abstract, TOC, references, compliance documents complete
Phase 5: Examiner-Ready Polish (3 skills)
    ↓ QG5: Institutional formatting met, readiness for examination
Phase 6: Viva / Defense Preparation (3 skills)
    ↓ QG6: Defense brief assembled, rehearsed, weak points mapped
```

---

## Sub-Skill Inventory

### Phase 1 — Scoping and Proposal

| # | Skill | Purpose | Zone |
|---|-------|---------|------|
| 1 | `programme-scoper` | Define research programme, questions, contribution | Reasoning |
| 2 | `thesis-structure-selector` | Select monograph / by-publication / hybrid | Reasoning |
| 3 | `thesis-timeline-builder` | Chapter-level plan across submission deadline | Deterministic |

### Phase 2 — Per-Chapter Development

Each chapter runs through these five skills:

| # | Skill | Purpose | Zone |
|---|-------|---------|------|
| 4 | `chapter-outliner` | Chapter-specific outline with role-in-thesis statement | Reasoning |
| 5 | `chapter-drafter` | Full draft per outline | Reasoning |
| 6 | `chapter-self-critic` | Apply chapter rubric before supervisor review | Reasoning |
| 7 | `chapter-reviser` | Revise from self-critique and supervisor feedback | Reasoning |
| 8 | `chapter-freezer` | Lock chapter with version, log decisions | Deterministic |

### Phase 3 — Cross-Chapter Integration

| # | Skill | Purpose | Zone |
|---|-------|---------|------|
| 9 | `thread-of-argument-checker` | Verify overall argument flows chapter-to-chapter | Reasoning |
| 10 | `redundancy-detector` | Find repeated exposition across chapters | Deterministic |
| 11 | `terminology-normalizer` | Enforce glossary consistency | Deterministic |
| 12 | `cross-reference-builder` | Insert chapter cross-refs where arguments connect | Reasoning |

### Phase 4 — Front / Back Matter and Compliance

| # | Skill | Purpose | Zone |
|---|-------|---------|------|
| 13 | `abstract-writer-thesis` | 300-500 word abstract (or institution limit) | Reasoning |
| 14 | `toc-list-generator` | ToC, list of figures, list of tables, list of abbreviations | Deterministic |
| 15 | `reference-consolidator` | Merge chapter references, deduplicate, verify | Deterministic |
| 16 | `compliance-statements-writer` | Acknowledgments, contribution statements, ethics, AI disclosure | Reasoning |

### Phase 5 — Examiner-Ready Polish

| # | Skill | Purpose | Zone |
|---|-------|---------|------|
| 17 | `institutional-formatter` | Apply institution-specific format (margins, fonts, pagination) | Deterministic |
| 18 | `final-proofer` | Line-level proofing | Reasoning |
| 19 | `examiner-readiness-auditor` | Simulate examiner read-through; flag weaknesses | Reasoning |

### Phase 6 — Viva / Defense Preparation

| # | Skill | Purpose | Zone |
|---|-------|---------|------|
| 20 | `defense-brief-builder` | One-page summary, key contributions, weak points | Reasoning |
| 21 | `question-bank-builder` | Anticipated questions by chapter + general | Reasoning |
| 22 | `mock-viva-runner` | Role-play viva with adversarial and friendly examiners | Reasoning |

---

## Quality Gate Definitions

### QG1: Proposal → Chapter Work

**Automated:**
- [ ] Research questions stated, scoped, and owner-chapters assigned
- [ ] Structure selected with institutional compliance note
- [ ] Timeline covers all chapters with supervisor-review buffer

**Human Review:**
- [ ] Supervisor approval recorded
- [ ] Ethics clearance in progress or not required

### QG2 (Per Chapter): Draft → Lock

**Automated:**
- [ ] Chapter has: role-in-thesis statement, word count within target, all claims cited
- [ ] Self-critique logged with issues + resolutions
- [ ] Supervisor feedback integrated (addressed or justified decline)
- [ ] Version snapshot saved

**Human Review:**
- [ ] Supervisor signs off on chapter milestone

### QG3: Integration

**Automated:**
- [ ] Thread-of-argument table built: each chapter's input → output → next chapter's input
- [ ] Redundant passages flagged across chapters
- [ ] Terminology glossary applied; variant terms flagged
- [ ] Cross-references inserted and reciprocal

**Human Review:**
- [ ] The thesis reads as one argument, not a collection of notes

### QG4: Front/Back Matter

**Automated:**
- [ ] Abstract within word limit
- [ ] Every figure and table listed
- [ ] References deduplicated; no orphan citations
- [ ] Required statements present (originality, contribution, AI-usage disclosure, ethics)

**Human Review:**
- [ ] Abstract accurately represents the thesis

### QG5: Examiner-Ready

**Automated:**
- [ ] Institutional format applied (margins, fonts, line spacing, pagination)
- [ ] Page count meets institutional min/max (if any)
- [ ] Figure/table numbering consistent
- [ ] Hyperlinks and cross-references resolve

**Human Review:**
- [ ] Read-through by PI/advisor
- [ ] No "TODO" or placeholder text remains

### QG6: Viva / Defense

**Automated:**
- [ ] Defense brief ≤ 1 page
- [ ] Question bank covers each chapter + general methodology + contribution
- [ ] Mock viva completed with ≥2 examiner personas (field expert, methodologist)

**Human Review:**
- [ ] Candidate able to articulate contribution in 2 minutes without notes

---

## Chapter-Level Coherence Protocol

Every chapter declares its role in a machine-readable block:

```json
{
  "chapter_id": "4",
  "title": "Empirical study: X in Context Y",
  "role_in_thesis": "Provides first empirical evidence for RQ2; feeds discussion chapter 6",
  "inputs_from_prior_chapters": ["Ch.2 theoretical framing", "Ch.3 methodology"],
  "outputs_to_later_chapters": ["Ch.6 discussion integrates with Ch.5"],
  "key_claims": [
    {"claim": "...", "evidence_ref": "Section 4.3.1, Table 4.2"},
    {"claim": "...", "evidence_ref": "Section 4.4, Figure 4.7"}
  ],
  "word_target": 15000,
  "word_actual": 14280,
  "status": "locked"
}
```

The thread-of-argument checker validates that every chapter's outputs are
consumed by a later chapter, and every input is supplied by an earlier one.

---

## Supervisor Feedback Integration

Supervisor feedback arrives in batches. The revision tracker forces explicit
decisions for each comment:

```json
{
  "feedback_id": "SV-2024-11-03-007",
  "chapter": "4",
  "comment": "The operationalization of X is under-justified given the literature in Ch.2",
  "status": "addressed",
  "resolution": "Added §4.2.3 linking operationalization to Ch.2 §2.4; cited 3 additional sources",
  "version_introduced": "4.7"
}
```

Declined comments require written rationale; nothing silently ignored.

---

## Viva / Defense Preparation

The defense brief should enable the candidate to:
- State the contribution in 30 seconds
- Walk the examiners through the thread of argument in 5 minutes
- Defend methodological choices with alternatives considered
- Acknowledge limitations and propose follow-on work

**Question bank categories:**
- Motivation & contribution (for every chapter)
- Methodological defense (data, sample, analysis, validity, ethics)
- Theoretical positioning (engagement with rival frameworks)
- Specific claims the candidate is weakest on (identified by examiner-readiness-auditor)
- Broader significance (impact, policy, future research)

---

## Institutional Compliance

| Requirement | Source | Validator |
|-------------|--------|-----------|
| Word count limits | Institution regulations | Deterministic counter |
| Originality declaration | Institution | Required section check |
| Contribution statement | Institution / funder | Required section check |
| AI usage disclosure | Emerging requirement | Required section check |
| Copyright for reproduced material | Copyright holders | Permissions log |
| Ethics statement | IRB / REC | Required section check |
| Embargo / open access election | Institution | Election recorded |
| Thesis binding or digital submission | Institution | Format validator |

Each institution varies — the institutional-formatter pulls from a per-
institution profile file.

---

## Common Failure Modes

| Failure | Cause | Prevention |
|---------|-------|------------|
| Chapters written as silos | No cross-chapter architecture | QG3 integration gate |
| Last-chapter panic | No early discussion/conclusion outline | Outline all chapters at Phase 1 |
| Supervisor feedback lost | Emails accumulate without tracking | Revision tracker forces status per comment |
| Redundant literature review | Every chapter re-reviews similar ground | Redundancy detector |
| Inconsistent terminology | Years of drafting drifts vocabulary | Terminology glossary enforced |
| Abstract drift | Written first, never updated | Abstract re-checked against final chapters at QG4 |
| Over-length submission | Institutional limit breached | Word count validator |
| Contribution unclear | Candidate can't state it concisely | Defense brief tests the elevator pitch |
| Weak points not anticipated | Candidate surprised in viva | Examiner-readiness-auditor surfaces weakness list |
| Reference list inconsistencies | Different citation styles across chapters | Reference consolidator normalizes |
| Figures/tables renumber inconsistently | Manual numbering across long drafts | Deterministic numbering at Phase 4 |
| AI usage undisclosed | Emerging institutional requirement missed | Compliance-statements-writer flags AI disclosure |
| Thesis-by-publication: wrapper too thin | Assumes papers speak for themselves | Wrapper explicitly synthesises across papers |
