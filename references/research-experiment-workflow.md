# Domain Accelerator: Research & Experiment Design

## Table of Contents

1. [Overview](#overview)
2. [Applicable Workflow Types](#applicable-workflow-types)
3. [Experiment Design Pipeline](#experiment-design-pipeline)
4. [Technology Scouting Pipeline](#technology-scouting-pipeline)
5. [Quality Gate Definitions](#quality-gate-definitions)
6. [Two-Zone Split for Research](#two-zone-split)
7. [Statistical Rigor Requirements](#statistical-rigor)
8. [Common Failure Modes](#common-failure-modes)

---

## Overview

Research and experiment design skills must ensure methodological rigor, statistical
validity, and reproducibility. The key challenge is preventing the LLM from
generating plausible-sounding but methodologically flawed experimental designs.

**Recommended architecture:** Plan-and-Execute with Maker-Checker verification on
methodology choices and deterministic statistical calculations.

**Critical principle:** All statistical methods, sample sizes, and analytical plans
must be justified before data collection. Post-hoc methodology changes require
explicit documentation and justification (pre-registration principle).

---

## Applicable Workflow Types

| Workflow | Complexity | Phases | Key Challenge |
|----------|-----------|--------|---------------|
| A/B test design & analysis | Medium | 5-6 | Power analysis, statistical validity |
| User research study design | Medium-High | 6-7 | Bias control, sample representativeness |
| ML model evaluation framework | High | 7-8 | Metric selection, benchmark rigor |
| Patent/prior art analysis | Medium | 5-6 | Comprehensive search, claim mapping |
| Technology scouting report | Medium-High | 6-7 | Landscape completeness, trend detection |
| Competitive analysis | Medium | 5-6 | Multi-source synthesis, bias awareness |
| Grant proposal writing | High | 7-8 | Methodology justification, significance argument |
| Literature-informed hypothesis generation | Medium | 4-5 | Evidence grounding, novelty assessment |

---

## Experiment Design Pipeline

### Phase Architecture

```
Phase 1: Research Question & Hypotheses (2 skills)
    ↓ QG1: Hypotheses are testable, variables operationalized
Phase 2: Methodology Selection (2 skills)
    ↓ QG2: Design justified, threats to validity addressed
Phase 3: Statistical Planning (3 skills)
    ↓ QG3: Power analysis complete, tests selected, alpha set
Phase 4: Procedure Design (2 skills)
    ↓ QG4: Protocol detailed enough for replication
Phase 5: Materials & Instruments (2 skills)
    ↓ QG5: All measures validated, data collection tools ready
Phase 6: Pre-Registration Document (2 skills)
    ↓ QG6: Pre-registration complete, deviations require justification
Phase 7: Analysis Plan (2 skills)
    ↓ QG7: Complete analytical plan documented before data collection
```

### Sub-Skill Inventory

| # | Skill | Purpose | Zone |
|---|-------|---------|------|
| 1 | `hypothesis-formulator` | Generate testable hypotheses from research question | Reasoning |
| 2 | `variable-operationalizer` | Define IVs, DVs, controls with measurement methods | Mixed |
| 3 | `design-selector` | Select experimental design (between/within/mixed/factorial) | Reasoning |
| 4 | `validity-threat-analyzer` | Identify internal/external validity threats and mitigations | Reasoning |
| 5 | `power-analyzer` | Calculate required sample size for target power | Deterministic |
| 6 | `test-selector` | Select appropriate statistical tests based on design and data type | Mixed |
| 7 | `alpha-correction-planner` | Plan for multiple comparisons (Bonferroni, FDR, etc.) | Deterministic |
| 8 | `protocol-writer` | Write detailed step-by-step procedure | Reasoning |
| 9 | `consent-form-drafter` | Draft informed consent and ethics materials | Reasoning |
| 10 | `instrument-validator` | Document psychometric properties of selected measures | Mixed |
| 11 | `data-collection-designer` | Design data collection instruments and procedures | Mixed |
| 12 | `prereg-document-builder` | Compile pre-registration document (AsPredicted/OSF format) | Mixed |
| 13 | `analysis-plan-writer` | Document complete analytical plan pre-data | Reasoning |
| 14 | `analysis-script-generator` | Generate analysis scripts (R/Python) from plan | Mixed |

---

## Technology Scouting Pipeline

### Phase Architecture

```
Phase 1: Landscape Definition (2 skills)
    ↓ QG1: Domain boundaries defined, key categories established
Phase 2: Source Discovery (3 skills)
    ↓ QG2: Academic, patent, and industry sources searched systematically
Phase 3: Technology Mapping (2 skills)
    ↓ QG3: Technologies categorized, maturity assessed (TRL)
Phase 4: Trend Analysis (2 skills)
    ↓ QG4: Trends identified with evidence, not speculation
Phase 5: Opportunity Assessment (2 skills)
    ↓ QG5: Opportunities rated, feasibility and risk assessed
Phase 6: Report & Recommendations (2 skills)
    ↓ QG6: Report reviewed, actionable recommendations delivered
```

---

## Quality Gate Definitions

### QG3: Statistical Planning Gate

**Automated (Deterministic):**
- [ ] Power analysis script produces required sample size
  ```bash
  python scripts/power_analysis.py --effect-size [d] --alpha [α] --power [1-β] --design [type]
  ```
- [ ] Selected statistical test matches the data type and design
  (e.g., not using t-test for non-normal data without justification)
- [ ] Alpha level explicitly stated (not assumed)
- [ ] Multiple comparison correction planned if >1 hypothesis

**Human Review:**
- [ ] Effect size assumption is justified (from prior research or pilot)
- [ ] Chosen design adequately controls confounding variables
- [ ] Statistical approach is appropriate for the research question

**Enforcement:**
```markdown
The power analysis script calculates the minimum sample size. This number
is the floor — the study CANNOT proceed with fewer participants without
documented justification and re-analysis of expected power.

Do not "round down" or "estimate" sample sizes. The script output is
the requirement.

WHY: Underpowered studies waste resources and produce unreliable results.
A study with 60% power has a 40% chance of missing a real effect, leading
to false null conclusions.
```

### QG6: Pre-Registration Gate

**Automated:**
- [ ] All sections of pre-registration template completed
- [ ] Hypotheses are specific and falsifiable
- [ ] Primary and secondary outcomes distinguished
- [ ] Exclusion criteria defined before data collection
- [ ] Analysis plan matches statistical planning from Phase 3

**Human Review:**
- [ ] Pre-registration is honest (doesn't hide flexibility)
- [ ] Deviations protocol is clear (what triggers a deviation, how to document)

---

## Two-Zone Split

| Deterministic | Reasoning |
|--------------|-----------|
| Power analysis calculation | Research question formulation |
| Sample size computation | Hypothesis generation |
| Alpha correction (Bonferroni) | Design selection and justification |
| Effect size calculation | Validity threat identification |
| Randomization sequence generation | Protocol narrative writing |
| Statistical test assumptions check | Consent form drafting |
| TRL (Technology Readiness Level) scoring | Trend interpretation |
| Patent search query execution | Opportunity assessment |
| Citation counting and h-index | Strategic recommendation |

---

## Statistical Rigor Requirements

### Pre-Data Collection

| Requirement | Implementation |
|------------|----------------|
| Sample size justified | Power analysis script with stated assumptions |
| Variables operationalized | Explicit measurement definitions |
| Statistical tests selected | Based on design, data type, and assumptions |
| Alpha level stated | Pre-specified, not post-hoc |
| Multiple comparison correction | Bonferroni, Holm, or FDR as appropriate |
| Exclusion criteria | Defined before data collection |
| Analysis plan | Complete script written before data |

### Post-Data Collection

| Requirement | Implementation |
|------------|----------------|
| Assumption checking | Normality, homogeneity, independence tests (scripted) |
| Effect size reported | With confidence intervals (scripted) |
| Exact p-values reported | Not just "p < 0.05" (scripted) |
| Deviations documented | Any changes from pre-registration explicitly noted |
| Data availability | Raw data and analysis scripts preserved |

---

## Common Failure Modes

| Failure | Cause | Prevention |
|---------|-------|------------|
| Underpowered study | Sample size guessed, not calculated | Mandatory power analysis script |
| HARKing | Hypothesis adjusted after seeing results | Pre-registration enforcement |
| P-hacking | Multiple analyses until "significant" | Analysis plan locked before data |
| Wrong statistical test | Test doesn't match data assumptions | Test selection decision tree |
| Missing confound | Variable not controlled | Structured validity threat analysis |
| Cherry-picked metrics | Only favorable outcomes reported | Primary/secondary outcomes pre-specified |
| Unreplicable protocol | Insufficient procedural detail | Replication audit at gate |
| Fabricated prior research | LLM invents supporting citations | Reference verification (same as academic) |
