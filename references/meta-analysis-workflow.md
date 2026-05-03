# Domain Accelerator: Meta-Analysis Workflows

## Table of Contents

1. [Overview](#overview)
2. [Phase Architecture](#phase-architecture)
3. [Sub-Skill Inventory](#sub-skill-inventory)
4. [Quality Gate Definitions](#quality-gate-definitions)
5. [Effect-Size Computation Protocol](#effect-size-computation-protocol)
6. [Heterogeneity and Model Selection](#heterogeneity-and-model-selection)
7. [Publication Bias Assessment](#publication-bias-assessment)
8. [Sensitivity and Subgroup Analysis](#sensitivity-and-subgroup-analysis)
9. [Reporting Standards](#reporting-standards)
10. [Common Failure Modes](#common-failure-modes)

---

## Overview

A meta-analysis statistically pools results across studies to estimate an overall
effect. It builds on a systematic review (identification, screening, extraction)
and adds quantitative synthesis. Reporting follows **PRISMA 2020** plus
**MOOSE** (for observational meta-analyses) with tool-specific reporting for the
statistical model (e.g., **metafor**, **Review Manager**, **meta** in R).

**Key architectural constraint:** All statistical operations live in the
**Deterministic Zone**. The LLM never computes effect sizes, confidence intervals,
or heterogeneity metrics — scripts do. The LLM interprets, contextualizes, and
writes prose.

**Recommended architecture:** Plan-and-Execute backbone with a deterministic
statistical core and Evaluator-Optimizer loops on interpretation sections.

---

## Phase Architecture

```
Phase 1: Systematic Review Foundation (reuse SLR pipeline)
    ↓ QG1: Inclusion set finalized, PICO locked
Phase 2: Effect-Size Extraction (4 skills)
    ↓ QG2: All studies have extractable effect data or documented exclusion
Phase 3: Statistical Synthesis (5 skills)
    ↓ QG3: Model justified, heterogeneity assessed, forest plot generated
Phase 4: Bias and Robustness (4 skills)
    ↓ QG4: Publication bias assessed, sensitivity analyses complete
Phase 5: Interpretation and Reporting (4 skills)
    ↓ QG5: PRISMA 2020 + MOOSE items addressed, results traceable to scripts
```

---

## Sub-Skill Inventory

### Phase 1 — Systematic Review Foundation

Reuse the SLR pipeline through full-text screening. Meta-analysis imposes stricter
extraction requirements: every included study needs usable quantitative data.

### Phase 2 — Effect-Size Extraction

| # | Skill | Purpose | Zone |
|---|-------|---------|------|
| 1 | `effect-type-selector` | Select effect metric (SMD, OR, RR, HR, correlation) with rationale | Reasoning |
| 2 | `raw-data-extractor` | Extract means, SDs, sample sizes, events, or slopes | Mixed |
| 3 | `effect-size-computer` | Compute effect sizes + variances from raw data | Deterministic |
| 4 | `data-imputation-handler` | Apply documented imputation for missing SDs (with sensitivity flag) | Deterministic |

### Phase 3 — Statistical Synthesis

| # | Skill | Purpose | Zone |
|---|-------|---------|------|
| 5 | `model-selector` | Choose fixed vs random effects with justification | Reasoning |
| 6 | `pooled-estimator` | Run model (DerSimonian-Laird, REML, Hartung-Knapp) | Deterministic |
| 7 | `heterogeneity-assessor` | Compute Q, I², τ², 95% prediction interval | Deterministic |
| 8 | `forest-plot-generator` | Generate publication-quality forest plot | Deterministic |
| 9 | `subgroup-analyzer` | Pre-registered subgroup and moderator analyses | Deterministic |

### Phase 4 — Bias and Robustness

| # | Skill | Purpose | Zone |
|---|-------|---------|------|
| 10 | `risk-of-bias-assessor` | RoB 2.0 (trials) or ROBINS-I (observational) per study | Mixed |
| 11 | `publication-bias-tester` | Funnel plot, Egger test, trim-and-fill, PET-PEESE | Deterministic |
| 12 | `sensitivity-analyzer` | Leave-one-out, influence diagnostics, alternative models | Deterministic |
| 13 | `grade-assessor` | GRADE certainty-of-evidence rating per outcome | Mixed |

### Phase 5 — Interpretation and Reporting

| # | Skill | Purpose | Zone |
|---|-------|---------|------|
| 14 | `results-interpreter` | Draft results prose referencing script outputs | Reasoning |
| 15 | `clinical-significance-framer` | Contextualize magnitude (MCID, NNT, etc.) | Reasoning |
| 16 | `prisma-moose-checker` | PRISMA 2020 + MOOSE item coverage | Deterministic |
| 17 | `reproducibility-package-builder` | Bundle scripts, data, seeds for replication archive | Deterministic |

---

## Quality Gate Definitions

### QG1: SLR Foundation → Effect Extraction

**Automated:**
- [ ] All included studies have PICO tags populated
- [ ] Population/Intervention/Comparator/Outcome consistent with protocol
- [ ] Study designs compatible with intended pooling strategy

**Human Review:**
- [ ] Sufficient clinical/conceptual homogeneity to pool

### QG2: Effect Extraction → Synthesis

**Automated:**
- [ ] Every included study has either extractable data or documented exclusion reason
- [ ] Effect sizes and variances computed by script (no hand-calculated values)
- [ ] Imputation rules applied consistently and flagged for sensitivity analysis
- [ ] Duplicate study populations (same cohort reported twice) identified

**Human Review:**
- [ ] Effect-size selection is appropriate to outcome type
- [ ] Units reconciled across studies (no mg/mL vs μg/mL mix)

### QG3: Synthesis → Bias Assessment

**Automated:**
- [ ] Model choice (fixed/random) documented with rationale
- [ ] Pooled estimate, 95% CI, heterogeneity statistics all present
- [ ] Forest plot generated and includes weights, CIs, pooled diamond
- [ ] Subgroup analyses limited to pre-registered contrasts

**Human Review:**
- [ ] If I² > 75%, does pooling still make sense?

### QG4: Bias → Reporting

**Automated:**
- [ ] RoB / ROBINS-I score recorded per study
- [ ] Funnel plot generated if ≥10 studies
- [ ] ≥2 publication bias tests run if ≥10 studies
- [ ] Leave-one-out sensitivity run and influential studies flagged
- [ ] GRADE table produced for each outcome

**Human Review:**
- [ ] Bias conclusions consistent across tests (if divergent, investigated)

### QG5: Reporting → Delivery

**Automated:**
- [ ] PRISMA 2020 27-item checklist complete
- [ ] MOOSE checklist complete (observational studies)
- [ ] Reproducibility package: data + code + environment lockfile present
- [ ] Every numeric claim in prose traces to a script output hash

**Human Review:**
- [ ] Interpretation avoids over-claiming significance
- [ ] Limitations section addresses heterogeneity, bias, and imputation

---

## Effect-Size Computation Protocol

**Critical rule:** The LLM never computes pooled estimates or effect sizes. All
computation is performed by `effect_size_computer.py` with explicit formulas:

```python
# For continuous outcomes — Hedges' g with small-sample correction
def hedges_g(m1, sd1, n1, m2, sd2, n2):
    s_pooled = sqrt(((n1-1)*sd1**2 + (n2-1)*sd2**2) / (n1+n2-2))
    d = (m1 - m2) / s_pooled
    J = 1 - 3/(4*(n1+n2-2) - 1)
    g = J * d
    var_g = J**2 * ((n1+n2)/(n1*n2) + d**2/(2*(n1+n2)))
    return {"g": g, "var": var_g, "se": sqrt(var_g)}
```

Every returned value is stamped with:
- Formula used (method id)
- Input provenance (study_id, table/figure/text location)
- Script version hash

The manuscript's methods section must reference these method IDs.

---

## Heterogeneity and Model Selection

| Scenario | Model | Rationale |
|----------|-------|-----------|
| Identical studies, same population | Fixed effect | Assumes single true effect |
| Clinical/methodological variation expected | Random effects (REML) | Assumes distribution of true effects |
| Small number of studies (< 5) | Hartung-Knapp-Sidik-Jonkman | Better CI coverage for small k |
| Prediction needed for future setting | Random effects + prediction interval | Report 95% PI alongside CI |

Heterogeneity metrics reported together (never I² alone):
- Cochran Q + df + p-value
- I² with 95% CI
- τ² (estimate + method)
- 95% prediction interval

---

## Publication Bias Assessment

Run if ≥10 studies. Single tests are underpowered; use a battery:

| Test | What It Detects | Minimum k |
|------|-----------------|-----------|
| Funnel plot (visual) | Asymmetry | 10 |
| Egger's regression | Small-study effects | 10 |
| Begg-Mazumdar rank correlation | Rank asymmetry | 10 |
| Trim-and-fill | Imputed missing studies | 10 |
| PET-PEESE | Adjusted effect under selection | 20 |
| Selection models (Copas) | Formal missingness model | 20 |

Disagreement between tests is itself a finding — report all, don't cherry-pick.

---

## Sensitivity and Subgroup Analysis

**Pre-registered only.** Post-hoc subgroups are flagged as exploratory and
require explicit language in the manuscript.

Standard sensitivity analyses:
- Leave-one-out influence analysis
- Alternative effect-size metric (e.g., OR vs RR for binary)
- Fixed vs random effects comparison
- Imputed vs complete-case analysis
- Exclusion of high-risk-of-bias studies

---

## Reporting Standards

| Standard | Applies To | Items |
|----------|-----------|-------|
| PRISMA 2020 | All systematic reviews with meta-analysis | 27 |
| MOOSE | Meta-analyses of observational studies | 35 |
| PRISMA-IPD | Individual participant data meta-analyses | 27+ extensions |
| GRADE | Certainty of evidence per outcome | Rating + rationale |

---

## Common Failure Modes

| Failure | Cause | Prevention |
|---------|-------|------------|
| LLM computes pooled effect | Zone discipline broken | Hard constraint: stats only via script |
| Pooling clinically heterogeneous studies | No pre-specified pooling plan | QG1 locks PICO; QG3 human review |
| Garden-of-forking-paths subgroup analyses | Unregistered exploratory mining | QG3 blocks non-registered subgroups |
| Over-interpreting small effects | Focusing on p-values over magnitude | Clinical-significance-framer step |
| Double-counting overlapping cohorts | Same population reported in multiple papers | Phase 2 duplicate-cohort check |
| Funnel plot misinterpreted | Asymmetry attributed to bias automatically | Egger test + clinical judgment required |
| Missing SDs filled silently | No flag for imputed values | Imputation handler tags affected studies |
| Forest plot without weights | Plot generated manually | Deterministic plot script enforces weights + CIs |
| Claims of "no effect" from p > 0.05 | Absence of evidence ≠ evidence of absence | Language audit in interpreter |
