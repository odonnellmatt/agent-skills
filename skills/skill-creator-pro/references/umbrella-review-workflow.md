# Domain Accelerator: Umbrella Review Workflows

## Table of Contents

1. [Overview](#overview)
2. [When to Use an Umbrella Review](#when-to-use-an-umbrella-review)
3. [Phase Architecture](#phase-architecture)
4. [Sub-Skill Inventory](#sub-skill-inventory)
5. [Quality Gate Definitions](#quality-gate-definitions)
6. [AMSTAR-2 Appraisal Protocol](#amstar-2-appraisal-protocol)
7. [Primary-Study Overlap Analysis](#primary-study-overlap-analysis)
8. [Evidence Statement Construction](#evidence-statement-construction)
9. [Reporting Standards](#reporting-standards)
10. [Common Failure Modes](#common-failure-modes)

---

## Overview

An umbrella review — also called an *overview of reviews* or *review of reviews* —
synthesizes findings from existing systematic reviews and meta-analyses on
related questions. It sits at the top of the evidence pyramid when the review
literature is mature.

**Authoritative methodologies:** JBI Umbrella Reviews framework (Aromataris et
al., 2015), Cochrane Overviews of Reviews, PRIOR reporting guideline (Gates et
al., 2022).

**Key distinctions:**
- Unit of analysis is the review, not the primary study
- Quality appraisal uses AMSTAR-2, ROBIS, or equivalent review-level tools
- Primary-study overlap across reviews must be quantified (CCA, corrected
  covered area)
- Findings often conflict between reviews — umbrella reviews interpret, not merely
  aggregate

**Recommended architecture:** Plan-and-Execute with dual-appraisal at QG3 and a
mandatory overlap quantification step before synthesis.

---

## When to Use an Umbrella Review

| Scenario | Umbrella Review Fits? |
|----------|---------------------|
| Multiple SLRs exist on related questions | Yes |
| Guideline development synthesizing review evidence | Yes |
| Reconciling conflicting SLR findings | Yes |
| Broad intervention with many sub-populations reviewed separately | Yes |
| Single SLR covers the question adequately | No — cite it, don't redo it |
| Primary studies abundant but reviews absent | No — conduct an SLR |

---

## Phase Architecture

```
Phase 1: Scope and Protocol (3 skills)
    ↓ QG1: Unit of analysis = review, question justifies umbrella
Phase 2: Review Identification (3 skills)
    ↓ QG2: Reviews identified, duplicates / updated versions resolved
Phase 3: Review Appraisal (3 skills)
    ↓ QG3: AMSTAR-2 applied in dual independent mode
Phase 4: Overlap Analysis (2 skills)
    ↓ QG4: Primary-study overlap quantified (CCA), conflict map drawn
Phase 5: Synthesis and Evidence Statements (3 skills)
    ↓ QG5: Evidence statements with certainty ratings, conflicts addressed
Phase 6: Reporting (2 skills)
    ↓ QG6: PRIOR checklist complete
```

---

## Sub-Skill Inventory

### Phase 1 — Scope and Protocol

| # | Skill | Purpose | Zone |
|---|-------|---------|------|
| 1 | `umbrella-question-formulator` | Define at the review level (PICO per review) | Reasoning |
| 2 | `eligibility-builder-umbrella` | Eligibility criteria targeting SLR-type publications | Reasoning |
| 3 | `umbrella-protocol-writer` | PRIOR + JBI-compliant protocol, register | Mixed |

### Phase 2 — Review Identification

| # | Skill | Purpose | Zone |
|---|-------|---------|------|
| 4 | `review-searcher` | Search with review-type filters (e.g., Cochrane, Epistemonikos) | Deterministic |
| 5 | `review-version-resolver` | Identify updates and withdrawn versions | Deterministic |
| 6 | `umbrella-prisma-flow-generator` | Flow diagram tailored to reviews | Deterministic |

### Phase 3 — Review Appraisal

| # | Skill | Purpose | Zone |
|---|-------|---------|------|
| 7 | `amstar2-appraiser` | AMSTAR-2 16-item appraisal with critical-item logic | Mixed |
| 8 | `dual-reviewer-consolidator` | Reconcile dual-reviewer appraisal disagreements | Mixed |
| 9 | `review-quality-summariser` | Confidence summary per review (critically low / low / moderate / high) | Deterministic |

### Phase 4 — Overlap Analysis

| # | Skill | Purpose | Zone |
|---|-------|---------|------|
| 10 | `primary-study-matrix-builder` | Build matrix of reviews × primary studies | Deterministic |
| 11 | `overlap-quantifier` | Compute Corrected Covered Area (CCA) by outcome | Deterministic |

### Phase 5 — Synthesis and Evidence Statements

| # | Skill | Purpose | Zone |
|---|-------|---------|------|
| 12 | `conflict-mapper` | Map agreeing vs conflicting review findings | Reasoning |
| 13 | `evidence-statement-builder` | Construct evidence statements per outcome | Reasoning |
| 14 | `certainty-rater` | Assign certainty (often GRADE or ConQual) | Reasoning |

### Phase 6 — Reporting

| # | Skill | Purpose | Zone |
|---|-------|---------|------|
| 15 | `prior-checker` | PRIOR 56-item checklist | Deterministic |
| 16 | `umbrella-manuscript-drafter` | Manuscript with review-level reporting | Reasoning |

---

## Quality Gate Definitions

### QG1: Protocol → Identification

**Automated:**
- [ ] Question states the unit of analysis is reviews, not primary studies
- [ ] PICO defined at review level (e.g., populations covered by reviews)
- [ ] Protocol registered (PROSPERO)
- [ ] Eligibility criteria for review type explicit (SLR, meta-analysis, scoping, etc.)

**Human Review:**
- [ ] Sufficient review literature exists to justify an umbrella review

### QG2: Identification → Appraisal

**Automated:**
- [ ] ≥2 databases searched, including review-indexing sources
- [ ] Review version resolution applied (one version per review, latest unless justified)
- [ ] Flow diagram reconciles counts
- [ ] Metadata complete per included review

**Human Review:**
- [ ] Coverage captures the important reviews of the domain

### QG3: Appraisal → Overlap

**Automated:**
- [ ] AMSTAR-2 (or ROBIS) applied to every included review
- [ ] Dual independent appraisal complete
- [ ] Disagreements resolved with logged rationale
- [ ] Overall confidence rating assigned per review

**Human Review:**
- [ ] Critically low confidence reviews flagged with implications for synthesis

### QG4: Overlap → Synthesis

**Automated:**
- [ ] Primary-study × review matrix built
- [ ] CCA computed per outcome
- [ ] CCA interpretation reported (slight: <5%, moderate: 5-10%, high: 10-15%, very high: >15%)
- [ ] Conflict map shows which reviews agree / disagree per outcome

**Human Review:**
- [ ] High overlap appropriately handled (avoid double-counting)

### QG5: Synthesis → Reporting

**Automated:**
- [ ] Every evidence statement cites contributing reviews with quality tag
- [ ] Certainty rating assigned per statement
- [ ] Conflicts explicitly discussed (not averaged away)
- [ ] Results tables show: outcome, reviews, direction, magnitude, certainty

**Human Review:**
- [ ] Interpretation acknowledges the cumulative uncertainty of review-of-review

### QG6: Reporting → Delivery

**Automated:**
- [ ] PRIOR items all addressed
- [ ] Limitations cover: review quality variability, overlap, primary-study bias propagation
- [ ] Funding / conflicts declared

**Human Review:**
- [ ] Final document avoids claims stronger than the underlying reviews

---

## AMSTAR-2 Appraisal Protocol

AMSTAR-2 has **7 critical items** that materially affect overall confidence:

| Item | Description |
|------|-------------|
| 2 | Protocol registered before review |
| 4 | Adequate literature search |
| 7 | Justification of excluded studies |
| 9 | Risk of bias assessment of individual studies |
| 11 | Appropriate statistical methods |
| 13 | Consideration of risk of bias in interpretation |
| 15 | Assessment of publication bias |

**Overall confidence rules:**

| Criticism | Critical Flaws | Non-critical Weaknesses | Overall |
|-----------|---------------|------------------------|---------|
| None | 0 | 0–1 | High |
| None | 0 | >1 | Moderate |
| One | 1 | any | Low |
| Multiple | >1 | any | Critically low |

Dual independent appraisal is mandatory, with disagreements resolved via
discussion or third reviewer. Each judgment carries a written rationale.

---

## Primary-Study Overlap Analysis

**Corrected Covered Area (CCA)** quantifies primary-study overlap across reviews:

```
CCA = (N − r) / (r × c − r)

Where:
  N = total number of primary-study occurrences across included reviews
  r = number of unique primary studies
  c = number of included reviews
```

| CCA | Interpretation |
|-----|---------------|
| 0–5% | Slight overlap |
| 6–10% | Moderate overlap |
| 11–15% | High overlap |
| >15% | Very high overlap |

High overlap indicates that reviews largely summarize the same primary evidence —
synthesis must avoid double-counting and consider using the most up-to-date
review as the anchor.

---

## Evidence Statement Construction

Every evidence statement includes:

```json
{
  "statement_id": "ES-07",
  "outcome": "Hospital readmission rates at 30 days",
  "direction": "favors intervention",
  "magnitude": "RR 0.82, 95% CI 0.74-0.91 (median across reviews)",
  "supporting_reviews": [
    {"id": "R-02", "amstar2": "High", "contribution": "large primary study set"},
    {"id": "R-05", "amstar2": "Moderate", "contribution": "adult population"}
  ],
  "conflicting_reviews": [
    {"id": "R-08", "amstar2": "Low", "direction": "no effect",
     "explanation": "Narrow population subset"}
  ],
  "certainty": "Moderate",
  "certainty_rationale": "Consistent direction across high-quality reviews; heterogeneity in magnitude; one divergent review of lower quality.",
  "cca_for_outcome": "7% — moderate overlap"
}
```

---

## Reporting Standards

- **PRIOR** (Gates et al., 2022) — 56 reporting items
- **JBI Umbrella Reviews** chapter (Aromataris et al.) — JBI-endorsed methodology
- Supplementary: AMSTAR-2 or ROBIS scores per review, CCA tables, conflict maps

---

## Common Failure Modes

| Failure | Cause | Prevention |
|---------|-------|------------|
| Double-counting primary studies | Overlap unquantified | QG4 requires CCA |
| Confidence inflation | Review-level findings treated as equivalent to primary evidence | Certainty rater downgrades for cumulative uncertainty |
| Conflict averaging | Opposing findings summarized as "mixed" without analysis | Conflict mapper names each disagreement |
| Outdated reviews dominating | Older reviews carry weight despite newer ones | Version-resolver enforces recency + completeness checks |
| Review quality ignored | AMSTAR-2 done but not used in synthesis | Evidence statements weighted by AMSTAR-2 tier |
| Scoping masquerading as umbrella | Includes scoping reviews and narratives ambiguously | Eligibility criteria explicit on review types |
| Primary-study appraisal redundancy | Re-appraising primary studies inside an umbrella | Unit of analysis locked at review level |
| PRIOR items skipped | Treated as optional | Deterministic checker enforces explicit N/A with rationale |
| Claims stronger than underlying reviews | Synthesis imports confidence not in sources | QG6 human review audits language strength |
