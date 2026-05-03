# Domain Accelerator: Scoping Review Workflows (JBI / PRISMA-ScR)

## Table of Contents

1. [Overview](#overview)
2. [When to Use a Scoping Review](#when-to-use-a-scoping-review)
3. [Phase Architecture](#phase-architecture)
4. [Sub-Skill Inventory](#sub-skill-inventory)
5. [Quality Gate Definitions](#quality-gate-definitions)
6. [PCC Framework Enforcement](#pcc-framework-enforcement)
7. [Concept Mapping Protocol](#concept-mapping-protocol)
8. [PRISMA-ScR Reporting](#prisma-scr-reporting)
9. [Common Failure Modes](#common-failure-modes)

---

## Overview

A scoping review *maps* the extent, range, and nature of evidence on a topic — it
does not answer a narrow effectiveness question or pool effect sizes. The
authoritative methodology is the **JBI Scoping Review framework** (Peters et al.,
2020), reported using **PRISMA-ScR** (Tricco et al., 2018).

**Key distinctions from a systematic review:**
- Broad research question, not focused on intervention effectiveness
- No critical appraisal of included studies (optional, not required)
- Synthesis is descriptive/conceptual, not statistical
- Uses **PCC** (Population/Concept/Context) not PICO
- Iterative search — refinement is expected as concepts emerge

**Recommended architecture:** Plan-and-Execute with iterative refinement loop
between Phase 2 (search) and Phase 3 (charting) to accommodate concept evolution.

---

## When to Use a Scoping Review

| Scenario | Scoping Review Fits? |
|----------|---------------------|
| Mapping evidence in an emerging field | Yes |
| Identifying research gaps for future SLRs | Yes |
| Clarifying a concept or definitional ambiguity | Yes |
| Determining feasibility of a future systematic review | Yes |
| Answering "does X work?" questions | No — use an SLR or meta-analysis |
| Pooling quantitative effects | No — use meta-analysis |
| Theory-building from qualitative evidence | No — use meta-synthesis |

---

## Phase Architecture

```
Phase 1: Scoping and Protocol (4 skills)
    ↓ QG1: PCC defined, protocol registered (OSF or similar)
Phase 2: Iterative Search and Selection (5 skills)
    ↓ QG2: Search documented, PRISMA-ScR flow counts verified
Phase 3: Data Charting (3 skills)
    ↓ QG3: Charting form piloted, ≥20% double-charted for agreement
Phase 4: Synthesis and Mapping (3 skills)
    ↓ QG4: Concept map produced, gap analysis complete
Phase 5: Reporting (3 skills)
    ↓ QG5: PRISMA-ScR 22-item checklist passed
```

---

## Sub-Skill Inventory

### Phase 1 — Scoping and Protocol

| # | Skill | Purpose | Zone |
|---|-------|---------|------|
| 1 | `pcc-formulator` | Structure question via Population / Concept / Context | Reasoning |
| 2 | `scoping-objectives-drafter` | Draft broad objective + specific sub-objectives | Reasoning |
| 3 | `eligibility-criteria-builder` | Define inclusion by PCC dimensions (liberal, not restrictive) | Reasoning |
| 4 | `jbi-protocol-generator` | Generate JBI-compliant protocol for OSF registration | Mixed |

### Phase 2 — Iterative Search and Selection

| # | Skill | Purpose | Zone |
|---|-------|---------|------|
| 5 | `three-step-search-builder` | JBI three-step search (limited → analyze terms → refine) | Mixed |
| 6 | `multi-database-searcher` | Parallel search of bibliographic + grey literature sources | Deterministic |
| 7 | `grey-literature-searcher` | Targeted grey literature (government, thesis, reports) | Mixed |
| 8 | `dual-reviewer-screener` | Title/abstract then full-text, dual reviewer with conflict log | Mixed |
| 9 | `prisma-scr-flow-generator` | Generate PRISMA-ScR flow diagram | Deterministic |

### Phase 3 — Data Charting

| # | Skill | Purpose | Zone |
|---|-------|---------|------|
| 10 | `charting-form-designer` | Design iterative charting form (pilot then refine) | Reasoning |
| 11 | `charting-pilot-runner` | Pilot on 5-10 studies, calculate agreement, refine form | Mixed |
| 12 | `data-charter` | Extract data per finalized form | Deterministic |

### Phase 4 — Synthesis and Mapping

| # | Skill | Purpose | Zone |
|---|-------|---------|------|
| 13 | `descriptive-summarizer` | Numerical/tabular summary of evidence distribution | Deterministic |
| 14 | `concept-mapper` | Build concept map: themes, sub-themes, relationships | Reasoning |
| 15 | `gap-analyzer` | Identify under-researched areas and methodological gaps | Reasoning |

### Phase 5 — Reporting

| # | Skill | Purpose | Zone |
|---|-------|---------|------|
| 16 | `prisma-scr-checker` | Verify all 22 PRISMA-ScR items reported | Deterministic |
| 17 | `scoping-manuscript-drafter` | Draft manuscript per JBI reporting structure | Reasoning |
| 18 | `stakeholder-consulter` | Optional — validate findings with stakeholders (JBI step 6) | Reasoning |

---

## Quality Gate Definitions

### QG1: Protocol → Search

**Automated:**
- [ ] PCC components all defined (Population, Concept, Context)
- [ ] Objectives include one broad + ≥2 specific sub-objectives
- [ ] Eligibility criteria derived from PCC (no orphan criteria)
- [ ] Protocol registered (OSF ID or equivalent recorded)

**Human Review:**
- [ ] Question is genuinely mapping-oriented, not effectiveness-oriented
- [ ] Scope is neither too narrow (use SLR) nor unmanageably broad

### QG2: Search → Charting

**Automated:**
- [ ] Three-step search documented with refinements logged
- [ ] ≥2 bibliographic databases + grey literature sources searched
- [ ] PRISMA-ScR flow numbers reconcile (identified - duplicates - excluded = included)
- [ ] Every exclusion at full-text has a recorded reason

**Human Review:**
- [ ] Search iteration captured emerging terminology
- [ ] Grey literature sources appropriate to domain

### QG3: Charting → Synthesis

**Automated:**
- [ ] Charting form piloted on ≥5 sources
- [ ] Double-charting performed on ≥20% with agreement metric recorded
- [ ] Charting form finalized and locked before full charting
- [ ] No charting fields blank for included studies

**Human Review:**
- [ ] Charting depth matches the specific sub-objectives
- [ ] Inter-charter disagreements resolved with documented rationale

### QG4: Synthesis → Reporting

**Automated:**
- [ ] Descriptive summary includes: year, country, study design, PCC distributions
- [ ] Concept map has themes + sub-themes + relationship labels
- [ ] Gap analysis identifies ≥3 distinct gap categories

**Human Review:**
- [ ] Concept map reflects the evidence, not pre-held views
- [ ] Gaps are research-actionable, not merely descriptive

### QG5: Reporting → Delivery

**Automated:**
- [ ] PRISMA-ScR 22-item checklist all marked addressed with location
- [ ] Protocol deviations documented
- [ ] Reference list matches citations (no orphans)

**Human Review:**
- [ ] Stakeholder consultation performed if claimed
- [ ] Manuscript tone consistent with mapping (avoids effectiveness claims)

---

## PCC Framework Enforcement

Every eligibility criterion must map to exactly one PCC dimension:

```json
{
  "population": {
    "description": "Adults aged 18+ in community settings",
    "inclusion": ["adults 18+", "community-dwelling"],
    "exclusion": ["hospital inpatient samples"]
  },
  "concept": {
    "description": "Digital health interventions for mental wellbeing",
    "inclusion": ["app-based", "web-based", "wearable-delivered"],
    "exclusion": ["SMS-only reminders without content"]
  },
  "context": {
    "description": "High-income country settings, 2015-present",
    "inclusion": ["OECD country", "post-2015"],
    "exclusion": ["LMIC", "pre-2015"]
  }
}
```

**Script check:** `pcc_validator.py` ensures no eligibility criterion is orphaned
from a PCC dimension and no PCC dimension is left undefined.

---

## Concept Mapping Protocol

Scoping reviews are defined by their concept map. The deterministic zone produces
a distribution summary; the reasoning zone interprets and builds the conceptual
structure.

**Deterministic outputs (script-generated):**
- Count by year, country, study design, population type
- Co-occurrence matrix of concepts across studies
- Methodology distribution table

**Reasoning outputs (LLM-generated, cited):**
- Theme labels and definitions
- Sub-theme hierarchy
- Relationships between themes (e.g., *enables*, *conflicts with*, *depends on*)
- Narrative interpretation of the map

**Critical constraint:** Every theme must link to ≥2 source studies. Every
relationship claim must cite evidence. The script flags single-source themes.

---

## PRISMA-ScR Reporting

The 22-item PRISMA-ScR checklist is verified deterministically. Reference:
Tricco AC et al. (2018) *Ann Intern Med* 169:467-473.

Key items the checker enforces:

| Item | Check |
|------|-------|
| 1 — Title identifies as scoping review | Regex scan |
| 4 — Objectives state PCC | Script compares to Phase 1 output |
| 6 — Eligibility criteria stated | Section presence + PCC mapping |
| 8 — Search documented with dates | Date fields populated in protocol |
| 9 — Selection process | Flow diagram present |
| 11 — Data charting process described | Pilot + agreement reported |
| 14 — Synthesis approach described | Not statistical pooling — descriptive only |
| 17 — Results per objective | Each objective has matched results section |
| 22 — Funding and conflicts disclosed | Section presence check |

---

## Common Failure Modes

| Failure | Cause | Prevention |
|---------|-------|------------|
| Scope creep mid-review | Iterative search drifts from PCC | Lock PCC at QG1; changes require documented amendment |
| Effectiveness claims | LLM defaults to "X works better than Y" | Claim-strength auditor rejects causal language |
| Missing grey literature | Relies only on bibliographic databases | QG2 requires ≥1 grey source |
| No concept map | Produces only a table of studies | QG4 blocks until map exists with relationships |
| Narrow like an SLR | Question written for effectiveness, not mapping | QG1 human review checks mapping intent |
| PRISMA-ScR items silently skipped | Reviewer assumes irrelevance | Script requires explicit "N/A + reason" rather than blank |
| Charting form changes unlogged | Iterative refinement not tracked | Version every form change with timestamp |
| Stakeholder step claimed but not done | Step 6 optional, often faked | If claimed, require consultation notes as artifact |
