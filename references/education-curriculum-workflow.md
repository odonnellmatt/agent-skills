# Domain Accelerator: Education & Curriculum Design

## Table of Contents

1. [Overview](#overview)
2. [Applicable Workflow Types](#applicable-workflow-types)
3. [Curriculum Design Pipeline](#curriculum-design-pipeline)
4. [Assessment Creation Pipeline](#assessment-creation-pipeline)
5. [Quality Gate Definitions](#quality-gate-definitions)
6. [Two-Zone Split for Education](#two-zone-split)
7. [Pedagogical Frameworks](#pedagogical-frameworks)
8. [Common Failure Modes](#common-failure-modes)

---

## Overview

Education and curriculum design skills must produce materials that are pedagogically
sound, appropriately scaffolded, and aligned with measurable learning outcomes. The
core challenge is ensuring constructive alignment — learning outcomes, activities,
and assessments must be coherent and mutually reinforcing.

**Recommended architecture:** Plan-and-Execute with Evaluator-Optimizer loops for
content quality and Maker-Checker on assessment validity.

**Critical principle:** Every learning activity and assessment item must trace to a
specific learning outcome. Bloom's taxonomy level must be consistently applied.

---

## Applicable Workflow Types

| Workflow | Complexity | Phases | Key Challenge |
|----------|-----------|--------|---------------|
| Full course/curriculum design | Very High | 8-10 | Constructive alignment, scaffolding |
| Assessment/exam creation | High | 6-7 | Validity, reliability, Bloom's alignment |
| Lesson plan generation | Medium | 4-5 | Timing, engagement, differentiation |
| Learning pathway design | High | 6-8 | Prerequisite mapping, adaptive branching |
| Training program design (corporate) | Medium-High | 5-7 | Skill gap analysis, ROI measurement |
| E-learning module creation | Medium-High | 5-6 | Interactivity, accessibility |
| Rubric development | Medium | 4-5 | Inter-rater reliability, criterion clarity |
| Accreditation documentation | High | 7-8 | Standards mapping, evidence compilation |

---

## Curriculum Design Pipeline

### Phase Architecture

```
Phase 1: Needs Analysis (3 skills)
    ↓ QG1: Learner profile defined, skill gaps identified, constraints documented
Phase 2: Learning Outcomes (2 skills)
    ↓ QG2: Outcomes measurable, Bloom's-classified, appropriately leveled
Phase 3: Content Architecture (3 skills)
    ↓ QG3: Modules sequenced, prerequisites mapped, workload balanced
Phase 4: Activity Design (3 skills)
    ↓ QG4: Activities aligned to outcomes, varied pedagogies, scaffolded
Phase 5: Assessment Design (3 skills)
    ↓ QG5: Assessments aligned to outcomes, rubrics developed, validity checked
Phase 6: Materials Development (3 skills)
    ↓ QG6: Content developed, reviewed for accuracy and accessibility
Phase 7: Evaluation Framework (2 skills)
    ↓ QG7: Course evaluation instruments designed, feedback loops planned
Phase 8: Review & Accreditation (2 skills)
    ↓ QG8: Peer review, standards compliance, final approval
```

### Sub-Skill Inventory

| # | Skill | Purpose | Zone |
|---|-------|---------|------|
| 1 | `needs-analyzer` | Analyze target audience, prerequisites, constraints | Reasoning |
| 2 | `skill-gap-identifier` | Map current vs desired competencies | Mixed |
| 3 | `context-surveyor` | Document delivery mode, resources, time constraints | Reasoning |
| 4 | `outcome-writer` | Write measurable learning outcomes using Bloom's taxonomy | Reasoning |
| 5 | `bloom-classifier` | Classify outcomes by cognitive level (1-6) | Mixed |
| 6 | `module-sequencer` | Order topics for progressive complexity | Reasoning |
| 7 | `prerequisite-mapper` | Define prerequisite relationships between modules | Mixed |
| 8 | `workload-calculator` | Estimate student workload hours per module | Deterministic |
| 9 | `activity-designer` | Design learning activities aligned to outcomes | Reasoning |
| 10 | `scaffolding-planner` | Design progressive skill-building sequences | Reasoning |
| 11 | `pedagogy-selector` | Select teaching methods (lecture, PBL, flipped, etc.) | Reasoning |
| 12 | `assessment-designer` | Create formative and summative assessments | Mixed |
| 13 | `rubric-developer` | Develop criterion-referenced rubrics with levels | Mixed |
| 14 | `item-validator` | Validate assessment items for Bloom's alignment and clarity | Mixed |
| 15 | `content-developer` | Write/curate learning materials | Reasoning |
| 16 | `accessibility-checker` | Verify UDL compliance and accessibility | Deterministic |
| 17 | `example-problem-generator` | Generate worked examples and practice problems | Mixed |
| 18 | `evaluation-designer` | Design course evaluation instruments | Reasoning |
| 19 | `feedback-loop-planner` | Plan continuous improvement cycle | Reasoning |
| 20 | `alignment-auditor` | Verify constructive alignment across all components | Deterministic |
| 21 | `peer-reviewer` | Present for subject matter expert review | Reasoning |

---

## Assessment Creation Pipeline

### Phase Architecture

```
Phase 1: Assessment Blueprint (2 skills)
    ↓ QG1: Outcomes mapped, Bloom's levels specified, item counts defined
Phase 2: Item Development (3 skills)
    ↓ QG2: Items written, distractors validated, Bloom's alignment verified
Phase 3: Rubric Development (2 skills)
    ↓ QG3: Rubrics developed, criteria clear, inter-rater reliability planned
Phase 4: Quality Assurance (2 skills)
    ↓ QG4: Items reviewed for bias, clarity, difficulty balance
Phase 5: Assembly & Review (2 skills)
    ↓ QG5: Assessment assembled, peer reviewed, approved
```

### Sub-Skill Inventory

| # | Skill | Purpose | Zone |
|---|-------|---------|------|
| 1 | `blueprint-builder` | Create assessment specification table (outcome × Bloom's × items) | Mixed |
| 2 | `weight-allocator` | Distribute marks across outcomes proportionally | Deterministic |
| 3 | `mcq-generator` | Generate multiple-choice items with validated distractors | Mixed |
| 4 | `open-response-generator` | Generate short-answer and essay prompts | Reasoning |
| 5 | `practical-task-designer` | Design performance-based assessment tasks | Reasoning |
| 6 | `rubric-builder` | Build analytic rubrics with observable criteria | Mixed |
| 7 | `exemplar-generator` | Create sample responses at each rubric level | Reasoning |
| 8 | `bias-reviewer` | Review items for cultural, gender, and language bias | Reasoning |
| 9 | `difficulty-balancer` | Ensure distribution across difficulty levels | Deterministic |
| 10 | `assessment-assembler` | Compile final assessment document with instructions | Mixed |
| 11 | `answer-key-generator` | Generate marking guide with model answers | Mixed |

---

## Quality Gate Definitions

### QG2: Learning Outcomes Gate

**Automated:**
- [ ] All outcomes use measurable action verbs (not "understand" or "know")
- [ ] Each outcome classified to a Bloom's taxonomy level
- [ ] Distribution across Bloom's levels is appropriate for course level
  (introductory: heavier lower levels; advanced: heavier higher levels)
- [ ] No duplicate outcomes

**Human Review:**
- [ ] Outcomes are achievable within the time/resource constraints
- [ ] Outcomes represent genuine value to the learner
- [ ] Level of challenge is appropriate for the target audience

**Enforcement:**
```markdown
Learning outcomes MUST be written using Bloom's taxonomy action verbs:

| Level | Acceptable Verbs | NOT Acceptable |
|-------|-----------------|----------------|
| 1 Remember | Define, list, recall, identify | Know, understand |
| 2 Understand | Explain, describe, classify, summarize | Appreciate, learn |
| 3 Apply | Solve, demonstrate, implement, use | Be familiar with |
| 4 Analyze | Compare, contrast, differentiate, examine | Think about |
| 5 Evaluate | Justify, critique, assess, argue | Be aware of |
| 6 Create | Design, construct, develop, formulate | Have experience |

Run: `python scripts/bloom_classifier.py --outcomes output/outcomes.json`
The script validates verb usage and classifies each outcome.
```

### QG5: Assessment Alignment Gate

**Automated (Deterministic):**
- [ ] Every learning outcome has at least one assessment item
- [ ] Every assessment item maps to at least one learning outcome
- [ ] Bloom's level of assessment items matches or exceeds outcome level
- [ ] Mark distribution across outcomes is proportional to importance/time
- [ ] Total marks sum correctly
- [ ] Time allocation is realistic (estimated time ≤ available time)

**Human Review:**
- [ ] Assessment is fair and free from bias
- [ ] Difficulty distribution is appropriate
- [ ] Instructions are clear and unambiguous

---

## Two-Zone Split

| Deterministic | Reasoning |
|--------------|-----------|
| Bloom's verb classification | Learning outcome writing |
| Workload hour calculation | Activity design |
| Constructive alignment matrix | Scaffolding design |
| Mark distribution and totals | Content creation |
| Difficulty level distribution | Teaching method selection |
| Prerequisite dependency validation | Feedback narrative |
| Accessibility compliance checking | Rubric criteria definition |
| Time allocation calculation | Pedagogy rationale |
| Outcome coverage tracking | Differentiation strategies |

---

## Pedagogical Frameworks

### Constructive Alignment (Biggs)

The foundational framework. All three components must align:

```
Learning Outcomes ←→ Teaching/Learning Activities ←→ Assessment
```

Verify alignment with a matrix:

| Outcome | Bloom's | Activities | Assessment | Weight |
|---------|---------|------------|------------|--------|
| LO1: [verb + content] | Apply | Lab exercise, tutorial | Practical exam Q1-3 | 25% |
| LO2: [verb + content] | Analyze | Case study, discussion | Essay question A | 30% |

### Bloom's Taxonomy (Revised)

Ensure cognitive progression through the course:

```
Level 6: Create     ← Advanced/capstone activities
Level 5: Evaluate   ← Critical analysis assignments
Level 4: Analyze    ← Comparison and examination tasks
Level 3: Apply      ← Problem-solving exercises
Level 2: Understand ← Explanatory activities
Level 1: Remember   ← Foundational recall tasks
```

### Universal Design for Learning (UDL)

| Principle | Implementation |
|-----------|---------------|
| Multiple means of engagement | Choice in topics, collaborative + individual options |
| Multiple means of representation | Text + visual + audio + interactive |
| Multiple means of action/expression | Written + oral + practical assessment options |

---

## Common Failure Modes

| Failure | Cause | Prevention |
|---------|-------|------------|
| Constructive misalignment | Assessment tests different skills than outcomes | Alignment matrix at gate |
| "Understand" outcomes | Non-measurable verb used | Bloom's verb validation script |
| Content without purpose | Activity not linked to any outcome | Coverage tracking at every gate |
| Assessment overload | Too many high-stakes assessments | Workload calculation, balance check |
| Bloom's ceiling too low | Advanced course only tests recall | Bloom's level distribution audit |
| Cultural bias in items | Items assume specific cultural knowledge | Bias review at quality gate |
| Inaccessible materials | Missing alt text, poor contrast, no captions | Automated accessibility checker |
| No formative assessment | Only summative, no learning feedback | Formative checkpoint requirements |
| Prerequisite gap | Module assumes knowledge not yet taught | Prerequisite dependency validation |
| Time overrun | Activities take longer than allocated | Workload estimation with buffer |
