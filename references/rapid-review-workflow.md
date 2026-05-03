# Domain Accelerator: Rapid Review Workflows

## Table of Contents

1. [Overview](#overview)
2. [When to Use a Rapid Review](#when-to-use-a-rapid-review)
3. [Phase Architecture](#phase-architecture)
4. [Sub-Skill Inventory](#sub-skill-inventory)
5. [Quality Gate Definitions](#quality-gate-definitions)
6. [Methodological Concessions Ledger](#methodological-concessions-ledger)
7. [Time-Box Enforcement](#time-box-enforcement)
8. [Reporting Standards](#reporting-standards)
9. [Common Failure Modes](#common-failure-modes)

---

## Overview

A rapid review accelerates systematic review methodology to deliver evidence
within weeks, not months, for time-sensitive decisions (policy, emerging
outbreaks, urgent clinical questions). The authoritative methodologies are the
**Cochrane Rapid Reviews Methods Group** guidance (Garritty et al., 2021) and
**WHO Rapid Reviews** practical guide.

**Core principle:** A rapid review is not a lower-quality SLR — it is a *transparent
set of concessions* to SLR methodology, each documented with rationale and
expected impact on bias. Transparency is what distinguishes it from an
inadequate SLR.

**Recommended architecture:** Plan-and-Execute with strict time-boxing and a
mandatory concessions ledger tracked across phases.

---

## When to Use a Rapid Review

| Driver | Rapid Review Appropriate? |
|--------|-------------------------|
| Emerging public health emergency | Yes |
| Policy decision within weeks | Yes |
| Clinical guideline update under deadline | Yes |
| Funder requires evidence summary in < 3 months | Yes |
| Topic with no urgency | No — do a full SLR |
| Definitive effectiveness claim for major policy | Caution — rapid review informs, full SLR confirms |

---

## Phase Architecture

```
Phase 1: Scoping and Concessions Plan (3 skills)
    ↓ QG1: Question focused, concessions pre-registered with justification
Phase 2: Targeted Search (3 skills)
    ↓ QG2: Search time-boxed, coverage gaps explicitly acknowledged
Phase 3: Streamlined Screening (3 skills)
    ↓ QG3: Single-reviewer screening + verification sample meets agreement threshold
Phase 4: Streamlined Extraction and Appraisal (3 skills)
    ↓ QG4: Extraction complete, risk-of-bias rated, concessions logged
Phase 5: Synthesis and Rapid Reporting (3 skills)
    ↓ QG5: Concession impact discussed, limitations transparent
```

---

## Sub-Skill Inventory

### Phase 1 — Scoping and Concessions Plan

| # | Skill | Purpose | Zone |
|---|-------|---------|------|
| 1 | `rapid-question-narrower` | Narrow PICO tightly — rapid reviews must be focused | Reasoning |
| 2 | `concessions-planner` | Pre-register which SLR steps will be streamlined and why | Reasoning |
| 3 | `stakeholder-aligner` | Confirm scope and timeline with requesting decision-maker | Reasoning |

### Phase 2 — Targeted Search

| # | Skill | Purpose | Zone |
|---|-------|---------|------|
| 4 | `core-database-searcher` | Search 1-2 priority databases (not comprehensive) | Deterministic |
| 5 | `date-and-language-limiter` | Apply date/language limits with impact estimate | Deterministic |
| 6 | `targeted-grey-sourcer` | Targeted, not exhaustive, grey literature | Mixed |

### Phase 3 — Streamlined Screening

| # | Skill | Purpose | Zone |
|---|-------|---------|------|
| 7 | `single-reviewer-screener` | Single-reviewer screen with structured criteria | Mixed |
| 8 | `verification-sample-checker` | Second-reviewer verifies 20-25% sample for agreement | Mixed |
| 9 | `prisma-flow-generator-rapid` | PRISMA flow with rapid-review annotations | Deterministic |

### Phase 4 — Streamlined Extraction and Appraisal

| # | Skill | Purpose | Zone |
|---|-------|---------|------|
| 10 | `focused-extractor` | Extract only decision-relevant fields (minimal form) | Deterministic |
| 11 | `abbreviated-rob-assessor` | Use abbreviated RoB or key-domain subset | Mixed |
| 12 | `extraction-verifier-sample` | Second-reviewer verifies ~20% of extractions | Mixed |

### Phase 5 — Synthesis and Rapid Reporting

| # | Skill | Purpose | Zone |
|---|-------|---------|------|
| 13 | `narrative-synthesizer-rapid` | Narrative synthesis (pooling only if pre-justified) | Reasoning |
| 14 | `concession-impact-analyzer` | Discuss how each concession may bias the findings | Reasoning |
| 15 | `decision-brief-drafter` | Deliver a decision-maker-oriented brief + full report | Reasoning |

---

## Quality Gate Definitions

### QG1: Scoping → Search

**Automated:**
- [ ] PICO is narrow (single population, ≤3 interventions, primary outcome specified)
- [ ] Concessions ledger exists with ≥1 entry per streamlined step
- [ ] Each concession has: rationale, SLR-equivalent step, expected bias direction
- [ ] Timeline and deliverables confirmed with stakeholder

**Human Review:**
- [ ] Question is genuinely rapid-review-appropriate (not just an under-resourced SLR)
- [ ] Concessions are defensible given the deadline

### QG2: Search → Screening

**Automated:**
- [ ] Search limited to pre-specified databases
- [ ] Date and language limits documented with justification
- [ ] Search time budget not exceeded (hours logged)
- [ ] Every limiter entered as a concession ledger row

**Human Review:**
- [ ] Omitted sources unlikely to contain paradigm-shifting evidence

### QG3: Screening → Extraction

**Automated:**
- [ ] Single-reviewer screening complete
- [ ] ≥20% verification sample screened by second reviewer
- [ ] Agreement ≥ acceptable threshold (Cohen's κ ≥ 0.6 or percent agreement ≥ 90%)
- [ ] Disagreements resolved and logged

**Human Review:**
- [ ] If agreement below threshold: escalate to dual screening (loses rapid status)

### QG4: Extraction → Synthesis

**Automated:**
- [ ] Extraction complete for all included studies
- [ ] RoB rated (even if abbreviated)
- [ ] ≥20% verification sample re-extracted by second reviewer with agreement logged

**Human Review:**
- [ ] Extraction fields sufficient for the decision the review informs

### QG5: Synthesis → Delivery

**Automated:**
- [ ] Concession impact analysis present — one paragraph per concession
- [ ] Limitations section explicitly lists every concession
- [ ] Decision brief ≤ 4 pages with key findings + uncertainty flagged
- [ ] Full report references PRISMA items with rapid-review annotations

**Human Review:**
- [ ] Decision-maker can act on this without over-interpreting
- [ ] Language hedges appropriately for the evidence strength

---

## Methodological Concessions Ledger

The concessions ledger is the central artifact distinguishing a rapid review from
an inadequate SLR. Every deviation from full SLR methodology is recorded:

```json
{
  "concession_id": "RR-2024-07-C3",
  "slr_equivalent": "Dual independent title/abstract screening",
  "rapid_approach": "Single reviewer with 20% verification sample",
  "rationale": "Timeline requires screening throughput of 200/day; dual screening infeasible",
  "expected_bias": "Slight increase in false-negative exclusions at screening",
  "mitigation": "Verification sample with κ ≥ 0.6 required before proceeding",
  "observed_impact": "κ = 0.71 on 120-record verification sample; no systematic exclusions detected",
  "timestamp": "2024-07-15T14:23:00Z"
}
```

Every phase adds to this ledger. The final report contains it as an appendix.

---

## Time-Box Enforcement

Each phase has a pre-registered time budget. Exceeding the budget triggers a
decision point, not silent overrun:

| Phase | Typical Budget (weeks) | Overrun Action |
|-------|------------------------|----------------|
| Scoping | 0.5 | Stakeholder re-confirmation |
| Search | 1.0 | Narrow limits further or accept partial coverage |
| Screening | 2.0 | Increase single-reviewer proportion or extend |
| Extraction + Appraisal | 1.5 | Reduce extraction fields |
| Synthesis + Reporting | 1.0 | Produce interim brief while finalizing |

**Budget overruns become concessions.** If a phase runs over, document why, what
was cut, and the impact on bias.

---

## Reporting Standards

| Standard | Use |
|----------|-----|
| PRISMA 2020 (with rapid-review annotations) | Main reporting backbone |
| Cochrane Rapid Reviews checklist | Methodological adequacy |
| PRISMA-Rapid (emerging) | When finalized |
| Decision brief format (2-4 pages) | Stakeholder-facing deliverable |

The rapid review delivers **two artifacts**: a full report (transparent methods)
and a decision brief (actionable summary). Both cite the concessions ledger.

---

## Common Failure Modes

| Failure | Cause | Prevention |
|---------|-------|------------|
| "Rapid" used to mean "low-effort" | Concessions not justified, just convenient | QG1 requires rationale per concession |
| Scope creep mid-review | Stakeholder expands question | Locked scope at QG1; changes trigger re-timeline |
| Undeclared concessions | Reviewer skips SLR steps without logging | Every skipped step requires ledger entry |
| Single reviewer with no verification | Claimed rigor without the check | QG3 blocks without verification sample |
| Narrative synthesis masquerading as meta-analysis | Pooling heterogeneous studies informally | Pooling requires explicit pre-justification |
| Timeline overrun hidden | Review quietly becomes an under-resourced SLR | Phase budgets reported in final document |
| Decision brief over-claims | Summary drops the uncertainty hedging | Brief must reference concession impact section |
| Missing grey literature where it matters | Policy topics need grey sources | Targeted grey step is not optional for policy questions |
