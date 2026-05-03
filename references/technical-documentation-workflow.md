# Domain Accelerator: Product & Technical Documentation

## Table of Contents

1. [Overview](#overview)
2. [Applicable Workflow Types](#applicable-workflow-types)
3. [API Documentation Pipeline](#api-documentation-pipeline)
4. [Product Requirements Document Pipeline](#prd-pipeline)
5. [Technical Architecture Document Pipeline](#architecture-doc-pipeline)
6. [Quality Gate Definitions](#quality-gate-definitions)
7. [Two-Zone Split for Documentation](#two-zone-split)
8. [Common Failure Modes](#common-failure-modes)

---

## Overview

Technical documentation skills must produce living documents that remain accurate
as the underlying system evolves. The core challenge is deriving documentation from
authoritative sources (code, APIs, schemas) rather than the LLM's potentially stale
training data.

**Recommended architecture:** Plan-and-Execute with heavy deterministic extraction
from source code/APIs, and Evaluator-Optimizer for narrative sections.

**Critical principle:** Documentation must be derived from the actual system, not
from the LLM's general knowledge. Verify every API endpoint, parameter, and behavior
against live sources.

---

## Applicable Workflow Types

| Workflow | Complexity | Phases | Key Challenge |
|----------|-----------|--------|---------------|
| API reference documentation | Medium-High | 5-6 | Endpoint completeness, example accuracy |
| Product requirements document (PRD) | Medium | 5-6 | Stakeholder alignment, completeness |
| Technical architecture document | High | 6-7 | Accuracy to current state, decision rationale |
| User guide / onboarding docs | Medium | 4-5 | Audience-appropriate complexity |
| Runbook / operational procedures | Medium | 5-6 | Actionability, error handling coverage |
| Migration guide | Medium-High | 5-6 | Step accuracy, rollback procedures |
| Changelog / release notes | Low-Medium | 3-4 | Completeness from git history |
| SDK/library documentation | High | 6-7 | Code example validity, cross-platform coverage |

---

## API Documentation Pipeline

### Phase Architecture

```
Phase 1: API Discovery (3 skills)
    ↓ QG1: All endpoints identified, schemas extracted from source
Phase 2: Endpoint Documentation (3 skills)
    ↓ QG2: Each endpoint documented with params, responses, examples
Phase 3: Guide Writing (2 skills)
    ↓ QG3: Getting started, authentication, error handling guides drafted
Phase 4: Example Validation (2 skills)
    ↓ QG4: All code examples tested, request/response pairs verified
Phase 5: Review & Publish (2 skills)
    ↓ QG5: Technical review complete, formatting correct
```

### Sub-Skill Inventory

| # | Skill | Purpose | Zone |
|---|-------|---------|------|
| 1 | `endpoint-discoverer` | Parse OpenAPI/Swagger specs or scan route files | Deterministic |
| 2 | `schema-extractor` | Extract request/response schemas | Deterministic |
| 3 | `auth-documenter` | Document authentication and authorization flows | Mixed |
| 4 | `endpoint-documenter` | Write description, parameters, responses for each endpoint | Mixed |
| 5 | `example-generator` | Generate request/response examples | Mixed |
| 6 | `error-catalog-builder` | Document all error codes and responses | Mixed |
| 7 | `quickstart-writer` | Write getting-started guide | Reasoning |
| 8 | `guide-writer` | Write conceptual guides (auth, pagination, webhooks) | Reasoning |
| 9 | `example-tester` | Execute examples against live/mock API, verify responses | Deterministic |
| 10 | `response-validator` | Compare documented responses to actual API behavior | Deterministic |
| 11 | `doc-formatter` | Format for target platform (Markdown, Docusaurus, etc.) | Deterministic |
| 12 | `technical-reviewer` | Present for engineering team review | Reasoning |

---

## PRD Pipeline

### Phase Architecture

```
Phase 1: Problem Definition (2 skills)
    ↓ QG1: Problem statement, user personas, and success metrics defined
Phase 2: Requirements Gathering (3 skills)
    ↓ QG2: Functional/non-functional requirements complete, prioritized
Phase 3: Solution Design (2 skills)
    ↓ QG3: Solution approach, trade-offs, and dependencies documented
Phase 4: Specification Writing (2 skills)
    ↓ QG4: User stories, acceptance criteria, edge cases documented
Phase 5: Review & Alignment (2 skills)
    ↓ QG5: Stakeholder sign-off
```

### Sub-Skill Inventory

| # | Skill | Purpose | Zone |
|---|-------|---------|------|
| 1 | `problem-framer` | Define problem statement, target users, impact | Reasoning |
| 2 | `persona-builder` | Create user personas with goals and pain points | Reasoning |
| 3 | `requirement-gatherer` | Elicit and categorize requirements (MoSCoW) | Reasoning |
| 4 | `constraint-identifier` | Identify technical, business, and regulatory constraints | Reasoning |
| 5 | `metric-definer` | Define measurable success criteria and KPIs | Mixed |
| 6 | `solution-architect` | Document solution approach and alternatives considered | Reasoning |
| 7 | `dependency-mapper` | Map dependencies on other teams, services, APIs | Mixed |
| 8 | `story-writer` | Write user stories with acceptance criteria | Reasoning |
| 9 | `edge-case-cataloger` | Enumerate edge cases and error states | Mixed |
| 10 | `prd-assembler` | Assemble final document from template | Mixed |
| 11 | `stakeholder-reviewer` | Present for cross-functional review | Reasoning |

---

## Architecture Doc Pipeline

### Phase Architecture

```
Phase 1: System Survey (3 skills)
    ↓ QG1: Current architecture captured from code/infra, not memory
Phase 2: Decision Documentation (2 skills)
    ↓ QG2: ADRs (Architecture Decision Records) drafted for key decisions
Phase 3: Diagram Generation (2 skills)
    ↓ QG3: Component, sequence, and deployment diagrams created
Phase 4: Writing (2 skills)
    ↓ QG4: All sections drafted, consistent with diagrams
Phase 5: Review (2 skills)
    ↓ QG5: Engineering review and approval
```

---

## Quality Gate Definitions

### QG2: Endpoint Documentation Gate (API Docs)

**Automated:**
- [ ] Every endpoint in OpenAPI spec has a corresponding documentation section
- [ ] All required parameters documented with types and descriptions
- [ ] All response codes documented (200, 400, 401, 403, 404, 500 minimum)
- [ ] At least one request example per endpoint
- [ ] At least one response example per endpoint

**Human Review:**
- [ ] Descriptions are clear to the target developer audience
- [ ] Examples are realistic (not trivial placeholder data)
- [ ] Error handling guidance is practical

### QG4: Example Validation Gate

**Automated (Deterministic):**
- [ ] All code examples parse without syntax errors
- [ ] All cURL examples are syntactically valid
- [ ] Request/response pairs match documented schemas
- [ ] All referenced endpoints exist in the API spec

**Enforcement:**
```markdown
Every code example MUST be tested. Do not publish untested examples.

Run: `python scripts/test_examples.py --docs output/api-reference/`

The script extracts code blocks, executes them against the mock API server,
and validates responses match documented schemas.

WHY: Incorrect API examples are the #1 developer complaint about documentation.
A single wrong parameter name wastes hours of developer time.
```

---

## Two-Zone Split

| Deterministic | Reasoning |
|--------------|-----------|
| OpenAPI spec parsing | Writing conceptual explanations |
| Schema extraction | Describing use cases and workflows |
| Example syntax validation | Choosing what to emphasize |
| Response validation against spec | Writing getting-started narrative |
| Endpoint coverage checking | Framing trade-offs in ADRs |
| Code block syntax checking | User persona creation |
| Link/reference validation | Acceptance criteria writing |
| Diagram-to-code consistency | Problem statement framing |

---

## Common Failure Modes

| Failure | Cause | Prevention |
|---------|-------|------------|
| Undocumented endpoint | New endpoint not in spec | Auto-discover from route files |
| Wrong parameter type | Manual transcription error | Extract directly from schema |
| Broken example | API changed, docs didn't | Automated example testing |
| Stale architecture description | Docs lag behind code | Derive from current codebase |
| Missing error code | Uncommon errors not documented | Extract from error handler source |
| Audience mismatch | Too technical or too basic | Persona-driven content framing |
| Internal jargon | Domain terms unexplained | Glossary generation from defined terms |
| Diagram-text inconsistency | Diagram shows X, text says Y | Cross-validation check |
