# Domain Accelerator: DevOps & Incident Response

## Table of Contents

1. [Overview](#overview)
2. [Applicable Workflow Types](#applicable-workflow-types)
3. [CI/CD Pipeline Design Skill](#cicd-pipeline)
4. [Incident Response Automation](#incident-response)
5. [Infrastructure-as-Code Review Pipeline](#iac-review)
6. [Quality Gate Definitions](#quality-gate-definitions)
7. [Two-Zone Split for DevOps](#two-zone-split)
8. [Common Failure Modes](#common-failure-modes)

---

## Overview

DevOps skills automate the design and validation of infrastructure, deployment
pipelines, and incident response procedures. The core challenge is that
infrastructure changes affect production systems — a misconfigured pipeline or
faulty runbook can cause outages.

**Recommended architecture:** Plan-and-Execute with heavy deterministic validation
(linting, dry-runs, policy checks) and Parallel Fan-Out for independent service reviews.

**Critical principle:** Infrastructure changes must be validated before application.
Dry-run everything. Test in staging. Verify rollback procedures work.

---

## Applicable Workflow Types

| Workflow | Complexity | Phases | Key Challenge |
|----------|-----------|--------|---------------|
| CI/CD pipeline design | High | 6-7 | Stage ordering, secret management, rollback |
| Incident response runbook | Medium-High | 5-6 | Actionability, decision tree completeness |
| Infrastructure-as-Code review | Medium-High | 5-6 | Policy compliance, drift detection |
| SLA/SLO framework design | Medium | 4-5 | Metric selection, error budget management |
| Disaster recovery plan | High | 7-8 | RTO/RPO definition, test coverage |
| Capacity planning | Medium | 5-6 | Forecasting accuracy, growth modeling |
| Post-incident review (PIR/RCA) | Medium | 4-5 | Root cause analysis, blameless culture |
| Monitoring & alerting design | Medium | 5-6 | Signal-to-noise ratio, alert fatigue prevention |

---

## CI/CD Pipeline Design

### Phase Architecture

```
Phase 1: Requirements & Constraints (2 skills)
    ↓ QG1: Build targets, deployment targets, compliance requirements defined
Phase 2: Pipeline Architecture (3 skills)
    ↓ QG2: Stage design, parallelism strategy, secret management plan approved
Phase 3: Stage Implementation (4 skills, parallel where independent)
    ↓ QG3: Each stage configured, linted, dry-run validated
Phase 4: Integration & Testing (2 skills)
    ↓ QG4: Full pipeline runs successfully on test branch
Phase 5: Rollback & Recovery (2 skills)
    ↓ QG5: Rollback tested, recovery procedures documented
Phase 6: Documentation & Handoff (2 skills)
    ↓ QG6: Pipeline documented, team trained
```

### Sub-Skill Inventory

| # | Skill | Purpose | Zone |
|---|-------|---------|------|
| 1 | `requirement-gatherer` | Elicit build, test, deploy, and compliance requirements | Reasoning |
| 2 | `constraint-identifier` | Identify infrastructure, security, and cost constraints | Reasoning |
| 3 | `stage-designer` | Design pipeline stages with dependency ordering | Mixed |
| 4 | `parallelism-optimizer` | Identify stages that can run concurrently | Mixed |
| 5 | `secret-manager` | Design secret injection and rotation strategy | Reasoning |
| 6 | `build-stage-configurator` | Configure build stage (compilation, dependencies) | Mixed |
| 7 | `test-stage-configurator` | Configure test stages (unit, integration, e2e) | Mixed |
| 8 | `security-scan-configurator` | Configure SAST/DAST/dependency scanning | Mixed |
| 9 | `deploy-stage-configurator` | Configure deployment (blue-green, canary, rolling) | Mixed |
| 10 | `pipeline-linter` | Validate pipeline syntax and configuration | Deterministic |
| 11 | `dry-run-executor` | Execute pipeline in dry-run mode | Deterministic |
| 12 | `rollback-designer` | Design and test rollback procedures | Mixed |
| 13 | `recovery-tester` | Execute rollback, verify system state | Deterministic |
| 14 | `pipeline-documenter` | Write operational documentation | Reasoning |
| 15 | `runbook-generator` | Generate on-call runbook for common failures | Reasoning |

---

## Incident Response

### Phase Architecture

```
Phase 1: Scenario Catalog (2 skills)
    ↓ QG1: Incident types cataloged, severity definitions established
Phase 2: Response Procedures (3 skills)
    ↓ QG2: Step-by-step procedures for each scenario, decision trees complete
Phase 3: Communication Plans (2 skills)
    ↓ QG3: Templates drafted for internal/external/customer comms
Phase 4: Automation (2 skills)
    ↓ QG4: Automated detection and initial response scripts tested
Phase 5: Testing & Validation (2 skills)
    ↓ QG5: Tabletop exercise completed, gaps addressed
```

### Key Runbook Structure

```markdown
## Incident: [Type]

### Severity Classification
- SEV1: [criteria] — Response within [time]
- SEV2: [criteria] — Response within [time]
- SEV3: [criteria] — Response within [time]

### Detection
- Alert source: [monitoring system]
- Key indicators: [specific metrics/thresholds]
- False positive signals: [how to distinguish real vs false]

### Immediate Response (First 5 Minutes)
1. [ ] Acknowledge alert in [system]
2. [ ] Verify incident is real (check [specific dashboards])
3. [ ] Classify severity using criteria above
4. [ ] If SEV1/SEV2: Page [team/person]
5. [ ] Create incident channel: #inc-[date]-[topic]

### Diagnosis Decision Tree
- Symptom A observed?
  - YES → Check [specific system], run [diagnostic command]
    - Root cause X? → Apply [fix], verify with [check]
    - Root cause Y? → Apply [fix], verify with [check]
  - NO → Check [other system]

### Remediation Steps
[Specific, copy-paste-ready commands and procedures]

### Post-Incident
1. [ ] Verify recovery metrics are normal
2. [ ] Send all-clear communication
3. [ ] Schedule post-incident review within 48 hours
4. [ ] Create follow-up tickets for preventive measures
```

---

## IaC Review

### Phase Architecture

```
Phase 1: Code Analysis (3 skills)
    ↓ QG1: All IaC files scanned, linted, policy-checked
Phase 2: Security Review (2 skills)
    ↓ QG2: No security misconfigurations, secrets not hardcoded
Phase 3: Cost Analysis (2 skills)
    ↓ QG3: Cost estimate generated, budget impact assessed
Phase 4: Drift Detection (2 skills)
    ↓ QG4: Planned changes vs actual state compared
Phase 5: Change Plan & Review (2 skills)
    ↓ QG5: Change plan approved, rollback tested
```

---

## Quality Gate Definitions

### QG3: Stage Validation Gate (CI/CD)

**Automated (Deterministic):**
- [ ] Pipeline syntax validates (`yamllint`, platform-specific linter)
- [ ] Dry-run completes without errors
- [ ] All referenced secrets exist in secret manager
- [ ] No hardcoded credentials in pipeline configuration
- [ ] Stage dependencies form a valid DAG (no cycles)
- [ ] Timeout values set for all stages

**Human Review:**
- [ ] Stage ordering makes logical sense
- [ ] Deployment strategy appropriate for the service
- [ ] Rollback procedure is realistic and tested

### QG5: Rollback Validation Gate

**Automated (Deterministic):**
- [ ] Rollback script executes successfully in staging
- [ ] Post-rollback health checks pass
- [ ] Database migration rollback tested (if applicable)
- [ ] State is consistent after rollback (no orphaned resources)

**Human Review:**
- [ ] Data loss implications documented and acceptable
- [ ] Rollback time is within SLA requirements
- [ ] Communication plan covers rollback scenario

---

## Two-Zone Split

| Deterministic | Reasoning |
|--------------|-----------|
| Pipeline syntax linting | Stage ordering design |
| Dry-run execution | Deployment strategy selection |
| Secret existence checking | Incident severity classification |
| Policy compliance scanning | Communication template drafting |
| Cost estimation | Decision tree construction |
| Drift detection | Root cause hypothesis |
| Health check execution | Runbook narrative writing |
| Rollback script execution | Post-incident analysis |
| Alert threshold calculation | SLO/error budget strategy |

---

## Common Failure Modes

| Failure | Cause | Prevention |
|---------|-------|------------|
| Pipeline breaks on merge | Untested stage interaction | Full pipeline dry-run at gate |
| Secret exposure | Hardcoded credential | Automated secret scanning |
| Incomplete rollback | Database schema can't reverse | Rollback testing at gate |
| Alert fatigue | Too many low-signal alerts | Alert tuning with signal/noise analysis |
| Runbook outdated | System changed, runbook didn't | Version-link runbook to service version |
| Wrong incident severity | Vague classification criteria | Explicit, measurable severity definitions |
| Cascading failure | No circuit breaker in pipeline | Stage isolation and timeout limits |
| Config drift undetected | Manual changes not captured | Regular drift detection scans |
