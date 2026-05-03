# Domain Accelerator: Repeatable Analytical Pipelines

## Table of Contents

1. [Overview](#overview)
2. [Applicable Workflow Types](#applicable-workflow-types)
3. [Analytical Pipeline Design](#analytical-pipeline-design)
4. [Quality Gate Definitions](#quality-gate-definitions)
5. [Two-Zone Split](#two-zone-split)
6. [Repeatability Requirements](#repeatability-requirements)
7. [Deterministic Pipeline Pattern](#deterministic-pipeline-pattern)
8. [State Variables for Execution Ordering](#state-variables)
9. [Reproducibility Logging](#reproducibility-logging)
10. [Parallel Analysis Pattern](#parallel-analysis-pattern)
11. [Report Assembly Pattern](#report-assembly-pattern)
12. [Common Failure Modes](#common-failure-modes)

---

## Overview

Analytical pipeline skills produce repeatable, auditable reports from data. The
core challenge is ensuring that deterministic calculations are locked in scripts
while reserving LLM reasoning for interpretation only — any LLM improvisation on
numbers silently corrupts results.

**Recommended architecture:** Plan-and-Execute with Parallel Fan-Out for
independent analyses and Evaluator-Optimizer for narrative quality.

**Critical principle:** Same inputs must produce same outputs. All calculations
are script-driven. The LLM never recalculates, rounds, or adjusts script output.

---

## Applicable Workflow Types

| Workflow | Complexity | Phases | Key Challenge |
|----------|-----------|--------|---------------|
| Repeatable analytics report | Medium-High | 6-7 | Reproducibility, number integrity |
| Multi-domain analysis | High | 7-8 | Parallel fan-out, conflict resolution |
| Statistical analysis pipeline | Medium | 5-6 | Reproducibility, test selection |
| KPI tracking dashboard | Medium | 5-6 | Metric calculation lockdown |
| Benchmarking study | Medium-High | 6-7 | Comparison methodology, normalization |
| Trend analysis report | Medium | 5-6 | Time-series integrity, projection rigor |

---

## Analytical Pipeline Design

### Phase Architecture

```
Phase 1: Data Acquisition (2 skills)
    ↓ QG1: All sources retrieved, schemas validated, hashes logged
Phase 2: Data Preparation (2 skills)
    ↓ QG2: Data cleaned, transforms documented, record counts reconciled
Phase 3: Computation (2 skills)
    ↓ QG3: All metrics calculated by script, results validated, hashes match
Phase 4: Analysis & Interpretation (3 skills)
    ↓ QG4: Interpretation grounded in script output, no fabricated numbers
Phase 5: Report Assembly (2 skills)
    ↓ QG5: Template-driven assembly, reproducibility metadata attached
Phase 6: Review & Delivery (2 skills)
    ↓ QG6: Human review approved, report delivered with audit trail
```

### Sub-Skill Inventory

| # | Skill | Purpose | Zone |
|---|-------|---------|------|
| 1 | `data-retriever` | Retrieve data from sources with exact query logging | Deterministic |
| 2 | `schema-validator` | Validate source schemas and log input hashes | Deterministic |
| 3 | `data-cleaner` | Apply rule-based cleaning transformations | Deterministic |
| 4 | `record-reconciler` | Reconcile row counts across transformations | Deterministic |
| 5 | `metric-calculator` | Execute all calculations with defined formulas | Deterministic |
| 6 | `statistical-tester` | Run statistical tests with reproducible parameters | Deterministic |
| 7 | `result-interpreter` | Interpret script output in domain context | Reasoning |
| 8 | `anomaly-explainer` | Explain anomalies and flag risks from computed data | Reasoning |
| 9 | `narrative-writer` | Generate report narrative grounded in script output | Reasoning |
| 10 | `report-assembler` | Assemble report from template with data and narrative | Mixed |
| 11 | `reproducibility-logger` | Generate audit trail with hashes and versioning | Deterministic |
| 12 | `review-coordinator` | Present report for human review and approval | Reasoning |
| 13 | `delivery-packager` | Package final report with reproducibility metadata | Mixed |

---

## Quality Gate Definitions

### QG1: Post-Acquisition Gate

**Automated:**
- [ ] All data sources successfully retrieved
- [ ] Input schemas match expected specification
- [ ] Row counts within expected ranges
- [ ] Input hashes logged for reproducibility
- [ ] No API errors or partial responses

### QG3: Post-Computation Gate

**Automated:**
- [ ] All metric formulas executed without errors
- [ ] Results within plausible ranges (no negative counts, percentages 0-100)
- [ ] Output hashes logged and match deterministic expectation
- [ ] Statistical tests completed with valid p-values
- [ ] No division-by-zero or NaN values in output

**Human Review:**
- [ ] Metric definitions align with business requirements
- [ ] Edge cases handled appropriately

### QG5: Post-Assembly Gate

**Automated:**
- [ ] All template sections populated (no empty placeholders)
- [ ] Numerical values in narrative match script output exactly
- [ ] Reproducibility metadata attached (run ID, hashes, versions)
- [ ] Report structure matches template specification

**Human Review:**
- [ ] Narrative accurately reflects the data
- [ ] Recommendations are grounded and actionable
- [ ] Report is suitable for the target audience

---

## Two-Zone Split

| Deterministic | Reasoning |
|--------------|-----------|
| Data retrieval and API calls | Result interpretation |
| Data cleaning and transformation | Anomaly explanation |
| Metric calculation | Narrative generation |
| Statistical tests | Recommendation formulation |
| Hash computation and logging | Executive summary writing |
| Record count reconciliation | Risk and opportunity framing |
| Template-driven report assembly | Contextual comparison to benchmarks |
| Schema validation | Report tone and audience adaptation |

---

## Repeatability Requirements

An analytical skill is "repeatable" when:

1. **Same inputs → same outputs** — Deterministic calculations never vary
2. **LLM reasoning is bounded** — Operates on fixed data, not fabricated context
3. **Process is documented** — Every step logged with inputs, outputs, parameters
4. **State is recoverable** — Any intermediate state can be reconstructed from logs
5. **Versions are tracked** — Script versions, model versions, data versions all recorded

---

## Common Failure Modes

| Failure | Cause | Prevention |
|---------|-------|------------|
| Non-reproducible results | LLM recalculated or rounded script output | Strict enforcement: LLM cites script values verbatim |
| Fabricated statistics | LLM generated plausible numbers from training data | All numbers must trace to script output |
| Missing audit trail | Hashes and versions not logged | Reproducibility logger runs at every step |
| Schema drift undetected | Source schema changed between runs | Schema validation at acquisition gate |
| Stale comparison data | Benchmarks outdated | Benchmark versioning with freshness checks |
| Report structure drift | LLM improvised new sections | Template-driven assembly enforced |
| Parallel analysis conflict | Two analyses reached contradictory conclusions | Merge script flags conflicts for explicit resolution |
| Partial data delivered | Pipeline failed mid-run but partial output used | All-or-nothing: gate blocks partial output |

---

## Deterministic Pipeline Pattern

### Implementation Template

```markdown
## Analytical Pipeline: [Domain]

### Step 1: Data Retrieval (Deterministic)
```bash
python scripts/fetch_data.py --source [SOURCE] --params [PARAMS] --output data/raw.json
```
Script outputs: structured JSON with metadata (timestamp, source, query params)

**Reproducibility:** The script logs the exact API call, parameters, and response
metadata. Re-running with same parameters produces same data (for point-in-time
snapshots, the timestamp is part of the parameters).

### Step 2: Data Cleaning (Deterministic)
```bash
python scripts/clean_data.py --input data/raw.json --config config/cleaning_rules.json --output data/clean.json
```

Cleaning rules are defined in config, not improvised:
- Missing value handling: [strategy]
- Outlier detection: [method and threshold]
- Type coercion: [rules]
- Deduplication: [criteria]

### Step 3: Calculation (Deterministic)
```bash
python scripts/calculate.py --input data/clean.json --metrics config/metrics.json --output data/results.json
```

All metrics defined in config file. The script NEVER invents additional metrics.
The LLM NEVER recalculates or adjusts any value from this output.

### Step 4: Interpretation (Reasoning Zone)
Read `data/results.json`. For each metric:
- Explain what it means in the current context
- Compare to benchmarks (from `references/benchmarks.json`)
- Identify trends, anomalies, and implications
- Flag risks and opportunities

**Constraint:** All numerical values cited in the interpretation MUST come from
the script output. Do not round, adjust, or recalculate any figure.

### Step 5: Report Assembly (Deterministic Template)
```bash
python scripts/assemble_report.py --data data/ --interpretation output/interpretation.md --template templates/report.md --output output/final_report.md
```

The template defines structure. The interpretation fills narrative sections.
Fixed data (tables, charts, metrics) come from scripts. Narrative comes from LLM.
```

---

## State Variables

Use explicit state variables to enforce execution ordering:

```json
{
  "pipeline_state": {
    "DATA_RETRIEVED": false,
    "DATA_CLEANED": false,
    "CALCULATIONS_COMPLETE": false,
    "VALIDATION_PASSED": false,
    "INTERPRETATION_COMPLETE": false,
    "REPORT_ASSEMBLED": false
  },
  "prerequisites": {
    "DATA_CLEANED": ["DATA_RETRIEVED"],
    "CALCULATIONS_COMPLETE": ["DATA_CLEANED"],
    "VALIDATION_PASSED": ["CALCULATIONS_COMPLETE"],
    "INTERPRETATION_COMPLETE": ["VALIDATION_PASSED"],
    "REPORT_ASSEMBLED": ["INTERPRETATION_COMPLETE"]
  }
}
```

**Enforcement rule:** Before executing any step, check that all prerequisite
state variables are `true`. If any prerequisite is `false`, HALT and report
which step needs to run first. Do not proceed with assumptions or defaults.

---

## Reproducibility Logging

Every pipeline run must produce a reproducibility log:

```json
{
  "run_id": "uuid",
  "timestamp": "2026-04-13T14:00:00Z",
  "pipeline_version": "2.1.0",
  "model": "current-reasoning-model",
  "inputs": {
    "data_source": "OpenAlex API",
    "query": "machine learning AND healthcare",
    "date_range": "2020-01-01 to 2026-04-13",
    "config_hash": "sha256:abc123"
  },
  "steps": [
    {
      "step": 1,
      "name": "data_retrieval",
      "script": "fetch_data.py v1.3",
      "input_hash": "sha256:def456",
      "output_hash": "sha256:ghi789",
      "duration_ms": 2340,
      "status": "success",
      "records_processed": 847
    },
    {
      "step": 2,
      "name": "data_cleaning",
      "script": "clean_data.py v1.1",
      "input_hash": "sha256:ghi789",
      "output_hash": "sha256:jkl012",
      "duration_ms": 450,
      "status": "success",
      "records_in": 847,
      "records_out": 823,
      "records_dropped": 24,
      "drop_reasons": {"duplicate": 18, "missing_required": 6}
    }
  ],
  "total_tokens": 12847,
  "total_cost_usd": 0.42,
  "total_duration_ms": 45000,
  "deterministic_steps_reproducible": true,
  "output_hash": "sha256:xyz789"
}
```

### Verification Protocol

To verify reproducibility:
1. Re-run all deterministic scripts with the same inputs
2. Compare output hashes — they must match exactly
3. The LLM reasoning steps may vary in phrasing but should reach the same conclusions
4. Log any discrepancies for investigation

---

## Parallel Analysis Pattern

For multi-domain analysis, use parallel fan-out:

```markdown
## Step 3: Multi-Domain Analysis (Parallel)

Spawn the following analyses simultaneously:

### 3a: [Domain A] Analysis
```bash
python scripts/analyze_domain_a.py --input data/clean.json --output data/domain_a.json
```

### 3b: [Domain B] Analysis
```bash
python scripts/analyze_domain_b.py --input data/clean.json --output data/domain_b.json
```

### 3c: [Domain C] Analysis
```bash
python scripts/analyze_domain_c.py --input data/clean.json --output data/domain_c.json
```

### 3d: Merge Results
After all parallel analyses complete:
```bash
python scripts/merge_analyses.py --inputs data/domain_*.json --output data/merged.json
```

**Conflict handling:** If Domain A and Domain C produce contradictory findings,
the merge script flags the conflict. The LLM interpretation step must explicitly
address the conflict rather than silently choosing one side.
```

---

## Report Assembly Pattern

### Template-Driven Assembly

The report template defines the structure. Data fills the fixed sections.
LLM narrative fills the interpretation sections.

```markdown
# [Report Title]
Generated: {{timestamp}}
Pipeline: {{pipeline_version}}

## Executive Summary
{{LLM_EXECUTIVE_SUMMARY}}

## Data Overview
| Metric | Value |
|--------|-------|
{{SCRIPT_METRICS_TABLE}}

## Detailed Analysis

### [Domain A]
{{LLM_DOMAIN_A_INTERPRETATION}}

#### Supporting Data
{{SCRIPT_DOMAIN_A_TABLE}}

### [Domain B]
{{LLM_DOMAIN_B_INTERPRETATION}}

## Key Findings
{{LLM_KEY_FINDINGS}}

## Recommendations
{{LLM_RECOMMENDATIONS}}

## Methodology
{{SCRIPT_METHODOLOGY_LOG}}

## Reproducibility
Run ID: {{run_id}}
Data hash: {{input_hash}}
Output hash: {{output_hash}}
```

**The template guarantees structure.** The LLM cannot skip sections, reorder content,
or remove the reproducibility footer. Scripts cannot be replaced by LLM improvisation.
