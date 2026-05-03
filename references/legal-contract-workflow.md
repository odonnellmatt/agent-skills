# Domain Accelerator: Legal & Contract Analysis

## Table of Contents

1. [Overview](#overview)
2. [Applicable Workflow Types](#applicable-workflow-types)
3. [Contract Review Pipeline](#contract-review-pipeline)
4. [Regulatory Compliance Pipeline](#regulatory-compliance-pipeline)
5. [Quality Gate Definitions](#quality-gate-definitions)
6. [Two-Zone Split for Legal](#two-zone-split)
7. [Risk Classification Framework](#risk-classification-framework)
8. [Common Failure Modes](#common-failure-modes)

---

## Overview

Legal workflows demand precision, completeness, and defensibility. Every finding
must be traceable to specific contract language or regulatory text. The agent must
never fabricate clause references, hallucinate legal precedent, or omit material
risks.

**Recommended architecture:** Plan-and-Execute with Maker-Checker verification
on every finding. Parallel Fan-Out for multi-document analysis.

**Critical principle:** Every assertion must cite specific clause numbers, page
references, or regulatory sections. Ungrounded legal conclusions are dangerous.

---

## Applicable Workflow Types

| Workflow | Complexity | Phases | Key Challenge |
|----------|-----------|--------|---------------|
| Contract review & redlining | High | 6-7 | Clause-level analysis, risk identification |
| Regulatory compliance mapping | Very High | 8-10 | Multi-framework cross-reference |
| Due diligence analysis | Very High | 8-10 | Comprehensive coverage across domains |
| Policy drafting | Medium-High | 5-6 | Internal consistency, regulatory alignment |
| Litigation document review | High | 6-8 | Volume management, privilege detection |
| IP portfolio analysis | Medium | 5-6 | Claim mapping, freedom-to-operate |
| Privacy impact assessment | Medium-High | 6-7 | Multi-regulation (GDPR, CCPA, etc.) |

---

## Contract Review Pipeline

### Phase Architecture

```
Phase 1: Document Ingestion (2 skills)
    ↓ QG1: Document parsed, structure mapped, parties identified
Phase 2: Clause Extraction (2 skills)
    ↓ QG2: All clauses classified, standard vs non-standard identified
Phase 3: Risk Analysis (3 skills)
    ↓ QG3: All risks identified, classified, grounded in specific language
Phase 4: Comparative Analysis (2 skills)
    ↓ QG4: Deviations from standard terms documented
Phase 5: Recommendation Drafting (2 skills)
    ↓ QG5: Recommendations prioritized, alternative language proposed
Phase 6: Report & Redline (2 skills)
    ↓ QG6: Human review and approval
```

### Sub-Skill Inventory

| # | Skill | Purpose | Zone |
|---|-------|---------|------|
| 1 | `document-parser` | Extract text, preserve structure, identify sections | Deterministic |
| 2 | `party-identifier` | Identify all parties, defined terms, effective dates | Mixed |
| 3 | `clause-classifier` | Classify clauses by type (indemnity, liability, IP, etc.) | Reasoning |
| 4 | `standard-comparator` | Compare against standard clause library | Mixed |
| 5 | `risk-identifier` | Identify legal risks in each clause | Reasoning |
| 6 | `obligation-extractor` | Extract all obligations, deadlines, conditions | Mixed |
| 7 | `financial-term-analyzer` | Analyze payment terms, penalties, caps | Deterministic |
| 8 | `deviation-reporter` | Document deviations from standard with severity | Mixed |
| 9 | `recommendation-drafter` | Draft alternative language, prioritize changes | Reasoning |
| 10 | `risk-matrix-generator` | Generate risk matrix with likelihood/impact scores | Mixed |
| 11 | `redline-generator` | Produce tracked-changes document | Deterministic |
| 12 | `summary-reporter` | Executive summary with key findings | Reasoning |

---

## Regulatory Compliance Pipeline

### Phase Architecture

```
Phase 1: Regulation Mapping (2 skills)
    ↓ QG1: Applicable regulations identified, requirements extracted
Phase 2: Current State Assessment (3 skills)
    ↓ QG2: Current practices documented, evidence collected
Phase 3: Gap Analysis (2 skills)
    ↓ QG3: All gaps identified, each traced to specific requirement
Phase 4: Risk Assessment (2 skills)
    ↓ QG4: Gaps risk-rated, remediation prioritized
Phase 5: Remediation Planning (2 skills)
    ↓ QG5: Action items defined, timelines set
Phase 6: Report & Governance (2 skills)
    ↓ QG6: Report approved, tracking mechanism established
```

---

## Quality Gate Definitions

### QG3: Risk Analysis Gate (Contract Review)

**Automated:**
- [ ] Every identified risk cites a specific clause number and quoted text
- [ ] Risk severity classification applied to all findings (Critical/High/Medium/Low)
- [ ] No findings without supporting contract language (zero ungrounded assertions)
- [ ] All obligation deadlines extracted and formatted as dates

**Human Review:**
- [ ] Risk severity classifications are appropriate
- [ ] No material risks were missed
- [ ] Interpretation of ambiguous language is reasonable

**Enforcement:**
```markdown
Every risk finding MUST include:
1. Clause reference (section number, page)
2. Exact quoted text from the contract
3. Risk description (what could go wrong)
4. Severity classification with rationale
5. Recommended action

Findings without exact quoted text are REJECTED. Do not summarize or
paraphrase the clause — quote it directly and cite the location.

WHY: Legal analysis without specific citations is unusable. Attorneys must
verify every finding against the source document. Paraphrased findings
cannot be verified and may misrepresent the actual contract language.
```

---

## Two-Zone Split

| Deterministic | Reasoning |
|--------------|-----------|
| Document parsing and text extraction | Interpreting clause intent |
| Clause boundary detection | Assessing risk severity |
| Deadline/date extraction | Drafting alternative language |
| Financial term calculation | Evaluating enforceability |
| Cross-reference validation | Identifying implicit obligations |
| Defined term resolution | Assessing interaction between clauses |
| Standard clause matching (exact/fuzzy) | Writing executive summary |
| Word/page counting | Prioritizing recommendations |

---

## Risk Classification Framework

### Severity Matrix

| Severity | Financial Impact | Operational Impact | Reputational Impact |
|----------|-----------------|-------------------|-------------------|
| **Critical** | >$1M or unlimited liability | Business continuity threat | Public/regulatory exposure |
| **High** | $100K-$1M | Significant disruption | Client relationship risk |
| **Medium** | $10K-$100K | Moderate inconvenience | Internal concern |
| **Low** | <$10K | Minimal impact | Negligible |

### Risk Categories

| Category | What to Look For |
|----------|-----------------|
| **Indemnification** | Unlimited indemnity, broad trigger events, no carve-outs |
| **Liability** | No cap, consequential damages included, no exclusions |
| **IP Rights** | Broad assignment, work-for-hire without limits, no license-back |
| **Termination** | Termination for convenience without notice, cure period absence |
| **Confidentiality** | Perpetual obligations, broad definition, no exceptions |
| **Data/Privacy** | GDPR obligations, data breach liability, processing restrictions |
| **Change of Control** | Assignment restrictions, consent requirements |
| **Governing Law** | Unfavorable jurisdiction, arbitration vs litigation |

---

## Common Failure Modes

| Failure | Cause | Prevention |
|---------|-------|------------|
| Fabricated clause reference | LLM invented section that doesn't exist | Clause verification against parsed document |
| Missed material risk | Clause buried in definitions or exhibits | Full document scanning, not just main body |
| Misquoted contract text | LLM paraphrased instead of quoting | Extraction from parsed document, not memory |
| Jurisdiction error | Applied wrong legal framework | Identify governing law clause first |
| Defined term confusion | "Company" means different things in different docs | Resolve defined terms before analysis |
| Exhibit/schedule ignored | Analysis only covered main agreement | Document structure mapping includes all attachments |
| Confidentiality breach | Included client-specific details in output | PII/sensitive data scanner at output |
| Stale template comparison | Standard terms outdated | Version-dated standard clause library |
