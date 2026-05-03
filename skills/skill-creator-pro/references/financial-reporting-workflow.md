# Domain Accelerator: Financial Reporting & Compliance

## Table of Contents

1. [Overview](#overview)
2. [Applicable Workflow Types](#applicable-workflow-types)
3. [Financial Report Pipeline](#financial-report-pipeline)
4. [Compliance Audit Pipeline](#compliance-audit-pipeline)
5. [Quality Gate Definitions](#quality-gate-definitions)
6. [Two-Zone Split for Finance](#two-zone-split)
7. [Regulatory Framework Integration](#regulatory-framework-integration)
8. [Common Failure Modes](#common-failure-modes)

---

## Overview

Financial workflows have zero tolerance for numerical errors and strict regulatory
requirements. The Two-Zone Architecture is paramount here — every calculation must
be script-locked, and the LLM must never be allowed to "round," "estimate," or
"adjust" any financial figure.

**Recommended architecture:** Plan-and-Execute with deterministic calculation
scripts and Evaluator-Optimizer for narrative sections.

**Critical principle:** Financial figures are sacred. The LLM interprets and
narrates; scripts calculate. No exceptions.

---

## Applicable Workflow Types

| Workflow | Complexity | Phases | Key Challenge |
|----------|-----------|--------|---------------|
| Quarterly/annual financial report | High | 7-8 | Numerical accuracy, cross-reference consistency |
| Regulatory compliance audit | Very High | 8-10 | Framework adherence, evidence documentation |
| Investment analysis report | Medium-High | 6-7 | Multi-source data synthesis, bias management |
| Budget planning & forecasting | Medium | 5-6 | Assumption documentation, scenario modeling |
| Risk assessment report | High | 6-8 | Quantitative rigor, threshold management |
| ESG/sustainability report | Medium-High | 6-7 | Multi-framework compliance (GRI, SASB, TCFD) |
| Due diligence report | Very High | 8-10 | Comprehensive coverage, red flag detection |

---

## Financial Report Pipeline

### Phase Architecture

```
Phase 1: Data Collection & Validation (3 skills)
    ↓ QG1: All data sources loaded, schema validated, checksums verified
Phase 2: Calculation & Metrics (3 skills)
    ↓ QG2: All ratios calculated, cross-footed, variance within tolerance
Phase 3: Comparative Analysis (2 skills)
    ↓ QG3: Period-over-period and peer comparisons complete, anomalies flagged
Phase 4: Narrative Drafting (3 skills)
    ↓ QG4: All sections drafted, figures match calculations, tone appropriate
Phase 5: Compliance Verification (2 skills)
    ↓ QG5: Regulatory checklist passed, disclosures complete
Phase 6: Review & Delivery (2 skills)
    ↓ QG6: Human sign-off, output formatted correctly
```

### Sub-Skill Inventory

| # | Skill | Purpose | Zone |
|---|-------|---------|------|
| 1 | `data-ingester` | Load financial data from sources (API, CSV, database) | Deterministic |
| 2 | `data-validator` | Schema validation, missing value detection, sanity checks | Deterministic |
| 3 | `cross-footer` | Verify totals = sum of components across all tables | Deterministic |
| 4 | `ratio-calculator` | Calculate all financial ratios (P/E, ROE, margins, etc.) | Deterministic |
| 5 | `variance-analyzer` | Period-over-period variance calculation | Deterministic |
| 6 | `trend-detector` | Statistical trend analysis, anomaly detection | Deterministic |
| 7 | `peer-comparator` | Benchmark against industry/peer data | Deterministic |
| 8 | `narrative-drafter` | Write executive summary, analysis, outlook | Reasoning |
| 9 | `table-generator` | Format financial tables with proper accounting conventions | Deterministic |
| 10 | `chart-generator` | Create charts and visualizations | Deterministic |
| 11 | `compliance-checker` | Verify against regulatory framework requirements | Mixed |
| 12 | `disclosure-generator` | Generate required disclosures and footnotes | Mixed |
| 13 | `report-assembler` | Assemble final report from template | Deterministic |
| 14 | `final-reviewer` | Present for human approval | Reasoning |

---

## Compliance Audit Pipeline

### Phase Architecture

```
Phase 1: Scope Definition (2 skills)
    ↓ QG1: Audit scope, framework, and criteria defined
Phase 2: Evidence Collection (3 skills)
    ↓ QG2: All evidence items collected and cataloged
Phase 3: Control Testing (3 skills)
    ↓ QG3: Controls tested, exceptions documented
Phase 4: Findings & Risk Assessment (2 skills)
    ↓ QG4: Findings rated, remediation recommended
Phase 5: Report Drafting (2 skills)
    ↓ QG5: Report complete, all findings supported by evidence
Phase 6: Review & Issuance (2 skills)
    ↓ QG6: QA review passed, management response obtained
```

---

## Quality Gate Definitions

### QG2: Post-Calculation Gate (Financial Report)

**Automated (Deterministic — NO LLM involvement):**
- [ ] All balance sheet items cross-foot (Assets = Liabilities + Equity)
- [ ] Income statement totals are internally consistent
- [ ] Cash flow statement reconciles to balance sheet cash changes
- [ ] All ratios calculated without division-by-zero errors
- [ ] Variance calculations match expected formulas
- [ ] No NaN, Inf, or null values in any output field
- [ ] All figures rounded to standard precision (2 decimal places for currency)

**Script enforcement:**
```bash
python scripts/cross_foot_validator.py --input data/financials.json
```
The script output is authoritative. If it reports a mismatch, there IS a mismatch.
Do not investigate whether the script might be wrong — re-check the input data.

### QG5: Compliance Gate

**Automated:**
- [ ] All required regulatory sections present
- [ ] All mandatory disclosures included
- [ ] Footnote numbering is sequential and complete
- [ ] No restricted terms used without proper context

**Human Review:**
- [ ] Disclosures are substantive (not boilerplate)
- [ ] Risk language is appropriate and not misleading
- [ ] Forward-looking statements include safe harbor language

---

## Two-Zone Split

### Absolutely Deterministic (Script-Locked)

| Task | Rationale |
|------|-----------|
| All arithmetic operations | Financial accuracy is non-negotiable |
| Ratio calculations | Must be formula-exact, reproducible |
| Cross-footing | Balance sheet equation must hold perfectly |
| Variance computation | Period-over-period must be mathematically exact |
| Currency conversion | Must use exact exchange rates, not estimates |
| Tax calculations | Regulatory precision required |
| Rounding | Must follow accounting standards (not LLM judgment) |
| Table formatting | Accounting conventions (parentheses for negatives, etc.) |

### Reasoning Zone

| Task | Rationale |
|------|-----------|
| Executive summary writing | Requires contextual framing |
| Variance explanation | "Revenue increased 12% due to..." requires interpretation |
| Risk narrative | Requires judgment about materiality and likelihood |
| Outlook/forecast narrative | Requires synthesizing multiple indicators |
| Peer comparison interpretation | "Company X outperforms because..." |
| Disclosure drafting | Requires legal/regulatory judgment |

### Enforcement Language

```markdown
## Critical Financial Constraint

All numerical values in the report MUST come from script output.
The LLM must NEVER:
- Round or truncate financial figures
- Estimate or approximate calculations
- "Correct" values that seem wrong
- Convert currencies without the script
- Calculate percentages mentally
- Interpolate between data points

If a figure appears incorrect, re-run the calculation script with
corrected inputs. Do not manually adjust the output.

WHY: A single rounded percentage in a financial report can trigger
regulatory scrutiny, restatement requirements, and loss of stakeholder
trust. There is no acceptable margin of error for financial calculations.
```

---

## Regulatory Framework Integration

Skills should reference the applicable framework's specific requirements:

| Framework | Domain | Key Requirements |
|-----------|--------|-----------------|
| IFRS | International financial reporting | Specific disclosure requirements per standard |
| US GAAP | US financial reporting | Revenue recognition, lease accounting, etc. |
| SOX (Sarbanes-Oxley) | US public company compliance | Internal controls, management assertions |
| Basel III/IV | Banking | Capital adequacy ratios, liquidity coverage |
| GRI Standards | Sustainability reporting | Materiality assessment, stakeholder engagement |
| SASB | Industry-specific sustainability | Industry-specific metrics and disclosures |
| TCFD | Climate risk | Governance, strategy, risk management, metrics |

---

## Common Failure Modes

| Failure | Cause | Prevention |
|---------|-------|------------|
| Rounding errors compound | LLM rounds intermediate values | All math in scripts |
| Cross-foot doesn't balance | Data entry error in source | Automated cross-foot check |
| Stale comparison data | Prior period data not refreshed | Data freshness check at ingestion |
| Misleading narrative | LLM overstates positive trends | Narrative must reference specific figures |
| Missing disclosure | Template didn't include required item | Regulatory checklist at gate |
| Currency mismatch | Mixed currencies without conversion | Currency normalization script |
| Forward-looking without caveat | Legal risk | Safe harbor language checker |
| Percentage base error | Denominator confusion (YoY vs QoQ) | Explicit formula documentation |
