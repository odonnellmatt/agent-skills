# Domain Accelerator: Cybersecurity Assessment

## Table of Contents

1. [Overview](#overview)
2. [Applicable Workflow Types](#applicable-workflow-types)
3. [Threat Modeling Pipeline](#threat-modeling-pipeline)
4. [Vulnerability Assessment Pipeline](#vulnerability-assessment-pipeline)
5. [Incident Response Playbook Pipeline](#incident-response-playbook-pipeline)
6. [Quality Gate Definitions](#quality-gate-definitions)
7. [Two-Zone Split for Security](#two-zone-split)
8. [Common Failure Modes](#common-failure-modes)

---

## Overview

Cybersecurity assessment skills must be thorough without creating false confidence.
The key risk is missing a vulnerability or threat vector because the skill's coverage
was incomplete. Skills must systematically enumerate attack surfaces rather than
relying on the LLM's ad-hoc recollection.

**Recommended architecture:** Plan-and-Execute with structured enumeration frameworks
(STRIDE, MITRE ATT&CK) and deterministic scanning at validation gates.

**Critical principle:** Use established threat frameworks for systematic coverage.
Do not rely on the LLM to "think of" all attack vectors — enumerate them.

**Authorization context:** These skills are designed for authorized security testing,
defensive security, penetration testing engagements, and educational contexts only.

---

## Applicable Workflow Types

| Workflow | Complexity | Phases | Key Challenge |
|----------|-----------|--------|---------------|
| Threat modeling (STRIDE/PASTA) | High | 6-8 | Complete attack surface enumeration |
| Vulnerability assessment report | High | 7-8 | Finding validation, false positive reduction |
| Security architecture review | Medium-High | 5-7 | Defense-in-depth analysis |
| Incident response playbook | Medium | 5-6 | Actionable runbooks, escalation clarity |
| Compliance gap analysis (SOC 2, ISO 27001) | High | 7-8 | Evidence mapping, control coverage |
| Penetration test report | High | 6-8 | Finding reproducibility, risk scoring |
| Security policy drafting | Medium | 4-6 | Completeness, regulatory alignment |

---

## Threat Modeling Pipeline

### Phase Architecture

```
Phase 1: System Decomposition (3 skills)
    ↓ QG1: Architecture diagram reviewed, data flows mapped, trust boundaries defined
Phase 2: Threat Enumeration (3 skills)
    ↓ QG2: All STRIDE categories covered per component, ATT&CK techniques mapped
Phase 3: Vulnerability Analysis (2 skills)
    ↓ QG3: Each threat assessed for likelihood and impact, no categories skipped
Phase 4: Mitigation Design (2 skills)
    ↓ QG4: Countermeasures defined for all high/critical threats
Phase 5: Residual Risk Assessment (2 skills)
    ↓ QG5: Residual risks documented, accepted risks explicitly acknowledged
Phase 6: Report & Review (2 skills)
    ↓ QG6: Human security team review and sign-off
```

### Sub-Skill Inventory

| # | Skill | Purpose | Zone |
|---|-------|---------|------|
| 1 | `architecture-decomposer` | Parse architecture docs, identify components and interactions | Mixed |
| 2 | `data-flow-mapper` | Map data flows between components, identify trust boundaries | Mixed |
| 3 | `asset-classifier` | Classify assets by sensitivity and criticality | Reasoning |
| 4 | `stride-enumerator` | Systematically apply STRIDE to each component and data flow | Mixed |
| 5 | `attack-tree-builder` | Build attack trees for high-value targets | Reasoning |
| 6 | `attck-mapper` | Map threats to MITRE ATT&CK techniques and sub-techniques | Mixed |
| 7 | `likelihood-assessor` | Score threat likelihood using DREAD or CVSS base metrics | Mixed |
| 8 | `impact-analyzer` | Assess business impact of each threat scenario | Reasoning |
| 9 | `countermeasure-designer` | Design mitigations mapped to specific threats | Reasoning |
| 10 | `control-gap-finder` | Identify gaps in current security controls | Mixed |
| 11 | `residual-risk-calculator` | Calculate residual risk after mitigations | Deterministic |
| 12 | `risk-acceptance-documenter` | Document accepted risks with justification | Reasoning |
| 13 | `threat-model-reporter` | Generate comprehensive threat model document | Mixed |
| 14 | `review-facilitator` | Present findings for security team review | Reasoning |

---

## Vulnerability Assessment Pipeline

### Phase Architecture

```
Phase 1: Scope Definition (2 skills)
    ↓ QG1: Assets in scope, rules of engagement defined
Phase 2: Discovery & Scanning (3 skills)
    ↓ QG2: All in-scope assets scanned, raw findings collected
Phase 3: Finding Validation (2 skills)
    ↓ QG3: False positives eliminated, findings confirmed reproducible
Phase 4: Risk Scoring (2 skills)
    ↓ QG4: CVSS scores calculated, business context applied
Phase 5: Remediation Planning (2 skills)
    ↓ QG5: Prioritized remediation plan with owners and timelines
Phase 6: Report Generation (2 skills)
    ↓ QG6: Report reviewed by security team
```

---

## Incident Response Playbook Pipeline

### Phase Architecture

```
Phase 1: Scenario Definition (2 skills)
    ↓ QG1: Incident types defined, scope documented
Phase 2: Response Procedure (3 skills)
    ↓ QG2: Step-by-step procedures for each scenario, roles assigned
Phase 3: Communication Templates (2 skills)
    ↓ QG3: Internal/external comms templates drafted, legal reviewed
Phase 4: Testing & Tabletop (2 skills)
    ↓ QG4: Tabletop exercise run, gaps identified
Phase 5: Finalization (2 skills)
    ↓ QG5: Playbook approved, distribution plan set
```

---

## Quality Gate Definitions

### QG2: Threat Enumeration Gate

**Automated:**
- [ ] All 6 STRIDE categories addressed for every component that crosses a trust boundary
- [ ] Coverage matrix complete (components × STRIDE categories, no empty cells)
- [ ] All identified threats have a unique identifier
- [ ] MITRE ATT&CK technique IDs are valid (format T####.###)

**Human Review:**
- [ ] Threat descriptions are realistic and specific (not generic)
- [ ] No obvious attack vectors missing
- [ ] Trust boundary definitions are accurate

**Enforcement:**
```markdown
The STRIDE enumeration must be SYSTEMATIC, not ad-hoc. For each component
that crosses a trust boundary, explicitly address ALL six categories:
- Spoofing: Can an attacker impersonate a legitimate entity?
- Tampering: Can data be modified in transit or at rest?
- Repudiation: Can actions be denied without proof?
- Information Disclosure: Can data leak to unauthorized parties?
- Denial of Service: Can the component be made unavailable?
- Elevation of Privilege: Can permissions be escalated?

If a category is not applicable, explicitly state "N/A — [reason]".
Do not leave categories blank or skip them.

WHY: Ad-hoc threat identification consistently misses 30-40% of attack
vectors. Systematic enumeration using STRIDE ensures coverage.
```

### QG4: Risk Scoring Gate

**Automated:**
- [ ] CVSS scores calculated for all confirmed findings
- [ ] CVSS vector strings are syntactically valid
- [ ] Risk ratings derived from scores match the correct severity bands
- [ ] No findings without a risk rating

**Human Review:**
- [ ] Business context adjustments to CVSS scores are justified
- [ ] Critical findings are genuinely critical (not inflated)

---

## Two-Zone Split

| Deterministic | Reasoning |
|--------------|-----------|
| CVSS score calculation | Threat scenario description |
| MITRE ATT&CK ID validation | Likelihood assessment |
| Coverage matrix generation | Attack tree construction |
| Finding deduplication | Countermeasure design |
| Scan output parsing | Business impact interpretation |
| Risk score computation | Remediation prioritization |
| Template compliance checking | Communication drafting |
| STRIDE category tracking | Residual risk acceptance justification |

---

## Common Failure Modes

| Failure | Cause | Prevention |
|---------|-------|------------|
| Missed attack vector | Ad-hoc enumeration instead of systematic | STRIDE coverage matrix enforcement |
| False positive in report | Unvalidated scanner output | Manual validation step |
| Generic threat description | "SQL injection is a risk" without context | Require component-specific scenarios |
| Outdated ATT&CK references | Using old technique IDs | Validate ATT&CK IDs against current framework |
| Missing remediation owner | Findings without accountability | Owner field required for every remediation |
| Scope creep | Assessment expanded beyond authorization | Rules of engagement check at gate |
| Severity inflation | Everything marked "Critical" | CVSS calculation enforced by script |
| Copy-paste findings | Generic text reused across assessments | Context-specific evidence required |
