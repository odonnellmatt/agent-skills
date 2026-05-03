# Domain Accelerator: Business Intelligence & Reporting

## Table of Contents

1. [Overview](#overview)
2. [Applicable Workflow Types](#applicable-workflow-types)
3. [Executive Dashboard Pipeline](#executive-dashboard-pipeline)
4. [Market Research Report Pipeline](#market-research-pipeline)
5. [Quality Gate Definitions](#quality-gate-definitions)
6. [Two-Zone Split for BI](#two-zone-split)
7. [Visualization Standards](#visualization-standards)
8. [Common Failure Modes](#common-failure-modes)

---

## Overview

Business intelligence skills must transform raw data into actionable insights while
maintaining absolute numerical accuracy. The challenge is presenting complex data
in accessible formats without distorting the underlying truth.

**Recommended architecture:** Plan-and-Execute with Parallel Fan-Out for multi-source
data gathering, and deterministic calculation/visualization scripts.

**Critical principle:** Every insight must trace to specific data. Narratives must
be grounded in calculated metrics, not LLM general knowledge.

---

## Applicable Workflow Types

| Workflow | Complexity | Phases | Key Challenge |
|----------|-----------|--------|---------------|
| Executive dashboard design | Medium-High | 5-6 | KPI selection, visual hierarchy |
| Market research report | High | 7-8 | Multi-source synthesis, trend validation |
| Competitive intelligence brief | Medium | 5-6 | Source reliability, bias awareness |
| KPI framework design | Medium | 4-5 | Metric alignment with strategy |
| Customer analytics report | Medium-High | 6-7 | Segmentation rigor, privacy compliance |
| Sales pipeline analysis | Medium | 5-6 | Forecasting accuracy, pipeline health |
| Operational efficiency report | Medium | 5-6 | Benchmark selection, metric normalization |
| Board presentation preparation | High | 6-7 | Executive audience, data storytelling |

---

## Executive Dashboard Pipeline

### Phase Architecture

```
Phase 1: Requirements & KPI Selection (3 skills)
    ↓ QG1: KPIs aligned with strategic objectives, data sources identified
Phase 2: Data Integration (3 skills)
    ↓ QG2: All data sources connected, schemas validated, refresh cadence set
Phase 3: Metric Calculation (2 skills)
    ↓ QG3: All KPIs calculated correctly, benchmarks established
Phase 4: Visualization Design (3 skills)
    ↓ QG4: Charts appropriate for data type, accessible, not misleading
Phase 5: Narrative & Annotations (2 skills)
    ↓ QG5: Key insights highlighted, context provided
Phase 6: Review & Deployment (2 skills)
    ↓ QG6: Stakeholder approval, refresh schedule confirmed
```

### Sub-Skill Inventory

| # | Skill | Purpose | Zone |
|---|-------|---------|------|
| 1 | `stakeholder-interviewer` | Elicit information needs and decision contexts | Reasoning |
| 2 | `kpi-selector` | Select and define KPIs aligned with strategy | Reasoning |
| 3 | `data-source-mapper` | Identify and validate data sources for each KPI | Mixed |
| 4 | `data-connector` | Build data integration queries/pipelines | Deterministic |
| 5 | `schema-validator` | Validate data types, ranges, completeness | Deterministic |
| 6 | `refresh-scheduler` | Configure automated data refresh cadence | Deterministic |
| 7 | `metric-calculator` | Calculate all KPIs with exact formulas | Deterministic |
| 8 | `benchmark-builder` | Establish targets, thresholds, and comparators | Mixed |
| 9 | `chart-type-selector` | Select appropriate visualization for each metric | Reasoning |
| 10 | `visualization-builder` | Generate charts following best practices | Mixed |
| 11 | `accessibility-checker` | Verify color contrast, labels, alt text | Deterministic |
| 12 | `insight-narrator` | Write narrative annotations for key findings | Reasoning |
| 13 | `context-provider` | Add explanatory notes, caveats, data quality flags | Reasoning |
| 14 | `dashboard-assembler` | Assemble layout with visual hierarchy | Mixed |
| 15 | `stakeholder-reviewer` | Present for approval | Reasoning |

---

## Market Research Pipeline

### Phase Architecture

```
Phase 1: Research Scope (2 skills)
    ↓ QG1: Market definition, research questions, methodology defined
Phase 2: Data Collection (4 skills, parallel)
    ↓ QG2: All sources gathered, reliability assessed
Phase 3: Analysis (3 skills)
    ↓ QG3: Market sizing calculated, segments defined, trends validated
Phase 4: Competitive Landscape (2 skills)
    ↓ QG4: Competitors mapped, positioning analyzed
Phase 5: Insights & Recommendations (2 skills)
    ↓ QG5: Insights grounded in data, recommendations actionable
Phase 6: Report Assembly (2 skills)
    ↓ QG6: Report reviewed, methodology transparent
```

---

## Quality Gate Definitions

### QG3: Metric Calculation Gate (Dashboard)

**Automated (Deterministic):**
- [ ] All KPI formulas documented and calculated by script
- [ ] Metric values within plausible ranges (no negative revenue, percentages 0-100)
- [ ] Year-over-year calculations use correct base periods
- [ ] No division-by-zero errors in ratio calculations
- [ ] Totals equal sum of components (cross-foot check)
- [ ] Sample sizes sufficient for statistical significance (where applicable)

### QG4: Visualization Gate

**Automated:**
- [ ] Chart types match data characteristics (no pie charts for >7 categories)
- [ ] Y-axis starts at zero for bar charts (or explicit justification if not)
- [ ] Color palette is colorblind-accessible
- [ ] All axes labeled with units
- [ ] No 3D effects that distort perception

**Human Review:**
- [ ] Visual hierarchy guides attention to most important metrics
- [ ] Dashboard tells a coherent data story
- [ ] No chart could be interpreted as misleading

---

## Two-Zone Split

| Deterministic | Reasoning |
|--------------|-----------|
| KPI calculation | KPI selection and prioritization |
| Market size computation | Market definition and scoping |
| Growth rate calculation | Trend interpretation |
| Revenue/profit metrics | Strategic implication analysis |
| Statistical significance tests | Insight narrative writing |
| Benchmark comparison | Recommendation generation |
| Chart rendering | Chart type selection |
| Data validation and profiling | Executive summary writing |
| Refresh schedule execution | Stakeholder communication |

---

## Visualization Standards

### Chart Type Selection Guide

| Data Type | Recommended Chart | Avoid |
|-----------|------------------|-------|
| Part-to-whole (≤6 categories) | Stacked bar, treemap | Pie charts >7 slices |
| Trend over time | Line chart | Area chart (obscures overlap) |
| Comparison across categories | Horizontal bar | Vertical bar with long labels |
| Distribution | Histogram, box plot | Pie chart |
| Correlation | Scatter plot | Dual-axis line chart |
| Geographic | Choropleth, bubble map | 3D globe |
| KPI status | Bullet chart, gauge | Traffic light (colorblind issue) |

### Visualization Anti-Patterns

| Anti-Pattern | Why It's Wrong | Alternative |
|-------------|---------------|-------------|
| Truncated Y-axis | Exaggerates small changes | Start at zero or use explicit annotation |
| Dual Y-axis | Implies false correlation | Two separate charts |
| 3D charts | Distorts perception | 2D always |
| Rainbow color schemes | Not colorblind-safe, no hierarchy | Sequential or diverging palettes |
| Chart junk | Reduces data-ink ratio | Minimize non-data elements |
| Unlabeled axes | Ambiguous interpretation | Always label with units |

---

## Common Failure Modes

| Failure | Cause | Prevention |
|---------|-------|------------|
| Wrong metric formula | Ambiguous KPI definition | Document exact formula before calculation |
| Stale data presented | Refresh failed silently | Freshness indicator on every dashboard |
| Misleading visualization | Y-axis manipulation, wrong chart type | Visualization review gate |
| Vanity metrics | Metrics that look good but don't inform decisions | Strategy-aligned KPI selection |
| Simpson's paradox | Aggregated trend reverses in segments | Segment-level analysis alongside aggregate |
| Survivorship bias | Only analyzing successful cases | Include failure/churn data explicitly |
| Correlation ≠ causation | Narrative implies causation without evidence | Explicit causal language audit |
| Missing context | Numbers without benchmarks or trends | Always include comparison and context |
