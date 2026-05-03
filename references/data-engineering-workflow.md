# Domain Accelerator: Data Engineering & ETL Pipelines

## Table of Contents

1. [Overview](#overview)
2. [Applicable Workflow Types](#applicable-workflow-types)
3. [ETL Pipeline Design Skill](#etl-pipeline-design)
4. [Data Quality Framework](#data-quality-framework)
5. [Quality Gate Definitions](#quality-gate-definitions)
6. [Two-Zone Split for Data Engineering](#two-zone-split)
7. [Monitoring and Observability](#monitoring-and-observability)
8. [Common Failure Modes](#common-failure-modes)

---

## Overview

Data engineering skills automate the design, validation, and monitoring of data
pipelines. The core challenge is ensuring data quality across transformations —
a subtle schema drift or null handling change can silently corrupt downstream
analytics for weeks before detection.

**Recommended architecture:** Plan-and-Execute with heavy deterministic validation
at every transformation step and Parallel Fan-Out for independent data streams.

**Critical principle:** Data quality checks are not optional post-processing — they
are embedded at every transformation boundary.

---

## Applicable Workflow Types

| Workflow | Complexity | Phases | Key Challenge |
|----------|-----------|--------|---------------|
| ETL/ELT pipeline design | High | 7-8 | Schema evolution, idempotency |
| Data migration | Very High | 8-10 | Zero data loss, validation at scale |
| Data quality audit | Medium-High | 5-6 | Comprehensive profiling, anomaly detection |
| Schema design & evolution | Medium | 4-5 | Backward compatibility, migration scripts |
| Data catalog creation | Medium | 5-6 | Completeness, business glossary alignment |
| Pipeline monitoring setup | Medium | 4-5 | Alert thresholds, SLA definition |
| Data lakehouse architecture | High | 7-8 | Layer design, access patterns, governance |

---

## ETL Pipeline Design

### Phase Architecture

```
Phase 1: Source Profiling (3 skills)
    ↓ QG1: All sources profiled, schemas documented, quality baselined
Phase 2: Pipeline Architecture (2 skills)
    ↓ QG2: DAG designed, dependencies mapped, idempotency strategy defined
Phase 3: Transformation Logic (3 skills)
    ↓ QG3: All transforms defined, tested with sample data, edge cases handled
Phase 4: Quality Framework (2 skills)
    ↓ QG4: Quality checks embedded at every boundary, thresholds defined
Phase 5: Orchestration & Scheduling (2 skills)
    ↓ QG5: DAG implemented, scheduling configured, retry logic defined
Phase 6: Monitoring & Alerting (2 skills)
    ↓ QG6: Dashboards built, alerts configured, runbook written
Phase 7: Documentation & Handoff (2 skills)
    ↓ QG7: Pipeline documented, operational handoff complete
```

### Sub-Skill Inventory

| # | Skill | Purpose | Zone |
|---|-------|---------|------|
| 1 | `source-profiler` | Analyze source schemas, volumes, distributions | Deterministic |
| 2 | `quality-baseliner` | Establish data quality baselines (nulls, ranges, patterns) | Deterministic |
| 3 | `schema-documenter` | Generate schema documentation with lineage | Mixed |
| 4 | `dag-designer` | Design transformation DAG with dependencies | Reasoning |
| 5 | `idempotency-strategist` | Define idempotent load patterns (upsert, merge, etc.) | Reasoning |
| 6 | `transform-builder` | Write transformation logic (SQL, Python, Spark) | Mixed |
| 7 | `edge-case-handler` | Define null handling, type coercion, dedup rules | Mixed |
| 8 | `sample-data-tester` | Run transforms against sample data, validate output | Deterministic |
| 9 | `quality-check-embedder` | Insert Great Expectations / dbt tests at boundaries | Deterministic |
| 10 | `threshold-definer` | Set alert thresholds based on baseline statistics | Mixed |
| 11 | `orchestrator-configurer` | Generate Airflow/Dagster/Prefect DAG code | Mixed |
| 12 | `retry-configurator` | Define retry, timeout, and failure handling policies | Reasoning |
| 13 | `dashboard-builder` | Create monitoring dashboards | Mixed |
| 14 | `runbook-writer` | Write operational runbook for on-call team | Reasoning |
| 15 | `pipeline-documenter` | Generate pipeline documentation with lineage diagrams | Mixed |
| 16 | `handoff-coordinator` | Create operational handoff package for support team | Reasoning |

---

## Data Quality Framework

### The 6 Dimensions of Data Quality

Every quality gate should assess relevant dimensions:

| Dimension | What It Measures | Check Method |
|-----------|-----------------|-------------|
| **Completeness** | Missing values, required fields | Script: null counts, pattern checks |
| **Accuracy** | Values match reality | Script: range checks, cross-reference |
| **Consistency** | Same fact represented same way everywhere | Script: cross-table validation |
| **Timeliness** | Data arrives within expected window | Script: timestamp comparison |
| **Uniqueness** | No unintended duplicates | Script: duplicate detection |
| **Validity** | Values conform to defined format/rules | Script: regex, enum, type checks |

### Quality Check Template

```python
# data_quality_check.py — runs at every transformation boundary
checks = {
    "completeness": {
        "required_fields_populated": "SELECT COUNT(*) WHERE {field} IS NULL",
        "threshold": 0,  # zero nulls in required fields
    },
    "accuracy": {
        "values_in_range": "SELECT COUNT(*) WHERE {field} NOT BETWEEN {min} AND {max}",
        "threshold": 0,
    },
    "uniqueness": {
        "no_duplicates": "SELECT COUNT(*) - COUNT(DISTINCT {key}) FROM {table}",
        "threshold": 0,
    },
    "consistency": {
        "foreign_key_valid": "SELECT COUNT(*) FROM {table} WHERE {fk} NOT IN (SELECT {pk} FROM {ref})",
        "threshold": 0,
    }
}
```

---

## Quality Gate Definitions

### QG1: Post-Profiling Gate

**Automated:**
- [ ] All source schemas captured and documented
- [ ] Row counts within expected ranges
- [ ] Data type distributions profiled
- [ ] Null percentages baselined per column
- [ ] Sample data extracted for testing

### QG3: Post-Transformation Gate

**Automated:**
- [ ] Output schema matches target specification
- [ ] Row counts reconcile (input rows = output rows ± expected filter/dedup)
- [ ] All quality checks pass on sample data
- [ ] No data type coercion warnings
- [ ] Edge cases handled (nulls, empty strings, boundary values)

**Human Review:**
- [ ] Transformation logic is correct for business rules
- [ ] Edge case handling aligns with business requirements

### QG5: Post-Orchestration Gate

**Automated:**
- [ ] DAG compiles and validates without errors
- [ ] All task dependencies are acyclic (no circular dependencies)
- [ ] Retry policies configured for each task
- [ ] Timeout values set for each task
- [ ] Idempotent re-run produces identical output

---

## Two-Zone Split

| Deterministic | Reasoning |
|--------------|-----------|
| Schema profiling and comparison | Choosing transformation approach |
| Row count reconciliation | Designing DAG architecture |
| Data quality checks | Defining business rules for edge cases |
| Null/duplicate detection | Writing runbook narratives |
| Type validation | Selecting orchestration tool |
| Checksum comparison | Alert threshold interpretation |
| Sample data testing | Documentation writing |
| DAG compilation/validation | Debugging strategy for failures |

---

## Monitoring and Observability

### Pipeline Health Dashboard

```
┌─────────────────────────────────────────────┐
│ Pipeline: [name]           Status: [●/○/◐]  │
├─────────────────────────────────────────────┤
│ Last Run: [timestamp]      Duration: [time] │
│ Records In: [N]            Records Out: [N] │
│ Quality Score: [%]         Failures: [N]    │
├─────────────────────────────────────────────┤
│ Data Freshness: [age]      SLA: [met/miss]  │
│ Schema Changes: [N]        Alerts: [N]      │
└─────────────────────────────────────────────┘
```

### Alert Definitions

| Alert | Condition | Severity |
|-------|-----------|----------|
| Pipeline failure | Task exits with non-zero code | Critical |
| SLA breach | Pipeline duration > threshold | High |
| Row count anomaly | Count deviates > 2σ from baseline | Warning |
| Schema drift | Source schema changed from expected | Critical |
| Quality threshold breach | Any quality check fails | High |
| Data freshness | Source data older than expected | Warning |

---

## Common Failure Modes

| Failure | Cause | Prevention |
|---------|-------|------------|
| Silent data loss | Filter removed valid records | Row count reconciliation at every step |
| Schema drift | Source changed without notice | Schema comparison at ingestion |
| Duplicate records | Non-idempotent load | Upsert patterns, dedup at boundary |
| Type coercion error | Implicit cast changed values | Explicit type checking |
| Timezone confusion | Mixed UTC/local timestamps | Normalize to UTC at ingestion |
| Null propagation | Null in calculation produces null chain | Null handling rules at every transform |
| Stale data served | Pipeline failed but old data still visible | Freshness checks, SLA alerts |
| Runaway backfill | Retry without idempotency creates duplicates | Idempotent operations only |
