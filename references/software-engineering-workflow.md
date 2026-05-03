# Domain Accelerator: Software Engineering Workflows

## Table of Contents

1. [Overview](#overview)
2. [Applicable Workflow Types](#applicable-workflow-types)
3. [Code Migration Pipeline](#code-migration-pipeline)
4. [Codebase Refactoring Pipeline](#codebase-refactoring-pipeline)
5. [Automated Code Review Pipeline](#automated-code-review-pipeline)
6. [Quality Gate Definitions](#quality-gate-definitions)
7. [Two-Zone Split for Software Engineering](#two-zone-split)
8. [Common Failure Modes](#common-failure-modes)

---

## Overview

Software engineering workflows demand strict correctness, backward compatibility, and
test coverage. The key challenge is that code changes have cascading effects — a refactor
in one module can break consumers across the entire codebase.

**Recommended architecture:** Plan-and-Execute backbone with Parallel Fan-Out for
independent modules, and deterministic validation (tests, linting, type-checking)
at every gate.

**Critical principle:** The agent must never ship code that hasn't passed automated
tests. Tests are the ultimate deterministic check.

---

## Applicable Workflow Types

| Workflow | Complexity | Phases | Key Challenge |
|----------|-----------|--------|---------------|
| Code migration (framework/language) | Very High | 8-10 | Preserving behavior across paradigm shift |
| Large-scale refactoring | High | 6-8 | Maintaining backward compatibility |
| Automated code review | Medium | 4-5 | Balancing thoroughness with false positives |
| API design and documentation | Medium | 5-6 | Consistency across endpoints |
| Test suite generation | Medium | 4-5 | Coverage without brittleness |
| Dependency upgrade | Medium | 5-6 | Breaking change detection |
| Performance optimization | High | 6-7 | Measurement before/after with statistical rigor |

---

## Code Migration Pipeline

### Phase Architecture

```
Phase 1: Discovery & Planning (3 skills)
    ↓ QG1: Full dependency map, migration plan approved
Phase 2: Compatibility Analysis (2 skills)
    ↓ QG2: Breaking changes cataloged, migration paths defined
Phase 3: Incremental Migration (4 skills)
    ↓ QG3: Each module migrated, unit tests passing
Phase 4: Integration Verification (3 skills)
    ↓ QG4: Integration tests passing, no regressions
Phase 5: Performance Validation (2 skills)
    ↓ QG5: Performance benchmarks within thresholds
Phase 6: Documentation & Cleanup (2 skills)
    ↓ QG6: Migration guide complete, deprecated code removed
```

### Sub-Skill Inventory

| # | Skill | Purpose | Zone |
|---|-------|---------|------|
| 1 | `codebase-analyzer` | Map dependencies, imports, call graphs | Deterministic |
| 2 | `migration-planner` | Generate ordered migration plan with rollback points | Reasoning |
| 3 | `compatibility-checker` | Identify API surface changes, breaking changes | Deterministic |
| 4 | `module-migrator` | Transform code module-by-module | Mixed |
| 5 | `test-adapter` | Update tests for new framework/language | Mixed |
| 6 | `integration-tester` | Run full test suite, report failures | Deterministic |
| 7 | `performance-benchmarker` | Before/after performance comparison | Deterministic |
| 8 | `migration-documenter` | Generate migration guide and changelog | Reasoning |

---

## Codebase Refactoring Pipeline

### Phase Architecture

```
Phase 1: Analysis (2 skills)
    ↓ QG1: Code smells identified, refactoring plan approved
Phase 2: Preparation (2 skills)
    ↓ QG2: Test coverage sufficient for safe refactoring
Phase 3: Incremental Refactoring (3 skills)
    ↓ QG3: Each refactoring step passes tests
Phase 4: Verification (2 skills)
    ↓ QG4: All tests pass, no behavior changes
Phase 5: Review & Documentation (2 skills)
    ↓ QG5: Human review approved, docs updated
```

### Sub-Skill Inventory

| # | Skill | Purpose | Zone |
|---|-------|---------|------|
| 1 | `code-smell-detector` | Static analysis: complexity, duplication, coupling | Deterministic |
| 2 | `refactoring-planner` | Prioritize refactorings, define safe ordering | Reasoning |
| 3 | `coverage-analyzer` | Measure test coverage, identify gaps | Deterministic |
| 4 | `test-gap-filler` | Generate tests for uncovered critical paths | Mixed |
| 5 | `extract-method-refactorer` | Apply extract method/class patterns | Mixed |
| 6 | `rename-refactorer` | Safe renames across codebase with reference updates | Deterministic |
| 7 | `dependency-decoupler` | Reduce coupling between modules | Mixed |
| 8 | `regression-runner` | Full test suite + behavior comparison | Deterministic |
| 9 | `changelog-generator` | Document what changed and why | Reasoning |

---

## Automated Code Review Pipeline

### Phase Architecture

```
Phase 1: Static Analysis (2 skills)
    ↓ QG1: Linting, type-checking, security scan complete
Phase 2: Logic Review (2 skills)
    ↓ QG2: Logic issues identified, severity classified
Phase 3: Architecture Review (2 skills)
    ↓ QG3: Pattern compliance, dependency direction verified
Phase 4: Report Generation (1 skill)
    ↓ QG4: Review report complete, actionable
```

### Sub-Skill Inventory

| # | Skill | Purpose | Zone |
|---|-------|---------|------|
| 1 | `static-analyzer` | Run linters, type checkers, security scanners | Deterministic |
| 2 | `complexity-scorer` | Calculate cyclomatic complexity, cognitive complexity | Deterministic |
| 3 | `logic-reviewer` | Identify potential bugs, edge cases, race conditions | Reasoning |
| 4 | `security-reviewer` | OWASP checks, injection vectors, auth issues | Mixed |
| 5 | `architecture-reviewer` | Pattern compliance, SOLID principles, dependency direction | Reasoning |
| 6 | `review-report-generator` | Prioritized findings with code suggestions | Mixed |

---

## Quality Gate Definitions

### QG: Post-Migration Module Gate

**Automated (Deterministic):**
- [ ] All unit tests pass (`pytest` / `jest` / `go test` exit code 0)
- [ ] Type checker passes (no new type errors)
- [ ] Linter passes (no new violations)
- [ ] No import cycle regressions
- [ ] Test coverage >= pre-migration coverage

**Human Review:**
- [ ] Code is idiomatic for the target framework
- [ ] Error handling follows new framework conventions

### QG: Post-Refactoring Gate

**Automated (Deterministic):**
- [ ] All existing tests still pass (zero regressions)
- [ ] No behavioral changes detected (output comparison)
- [ ] Complexity metrics improved (or unchanged)
- [ ] No new linter warnings introduced

**Human Review:**
- [ ] Refactored code is more readable
- [ ] Naming conventions are clear and consistent

---

## Two-Zone Split

| Always Deterministic | Always Reasoning |
|---------------------|-----------------|
| Running tests | Deciding refactoring priority |
| Linting and type-checking | Interpreting code smell significance |
| Calculating complexity metrics | Designing new abstractions |
| Dependency graph generation | Writing meaningful commit messages |
| Coverage measurement | Explaining changes in review comments |
| Performance benchmarking | Judging architectural appropriateness |
| Import analysis | Identifying edge cases in logic |

---

## Common Failure Modes

| Failure | Cause | Prevention |
|---------|-------|------------|
| Silent behavior change | Refactoring altered semantics | Before/after output comparison tests |
| Test suite rot | Tests coupled to implementation details | Assert behavior, not implementation |
| Incomplete migration | Some modules skipped | Module tracking in state with completion flags |
| Performance regression | New code is slower | Benchmark at gate with threshold |
| Circular dependency introduced | Refactoring created new cycle | Dependency graph check at gate |
| Breaking public API | Changed function signature | API surface diff at gate |
