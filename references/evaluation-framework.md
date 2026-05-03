# Evaluation and Benchmarking Framework

## Table of Contents

1. [The Evaluation Lifecycle](#the-evaluation-lifecycle)
2. [Test Case Design](#test-case-design)
3. [Assertion Design](#assertion-design)
4. [Outcome vs Trajectory Metrics](#outcome-vs-trajectory-metrics)
5. [LLM-as-Judge Evaluation](#llm-as-judge-evaluation)
6. [Three-Tier Rubric Design](#three-tier-rubric-design)
7. [Blind Comparison Protocol](#blind-comparison-protocol)
8. [Continuous Improvement Loop](#continuous-improvement-loop)

---

## The Evaluation Lifecycle

```
Write Skill Draft
      ↓
Create 3-5 Realistic Test Prompts
      ↓
Run With-Skill AND Baseline in parallel
      ↓
Draft Quantitative Assertions (while runs execute)
      ↓
Grade Assertions Against Outputs
      ↓
Aggregate Benchmarks (pass_rate, time, tokens)
      ↓
Human Reviews Qualitative Outputs
      ↓
Collect Feedback → Improve Skill → Repeat
```

---

## Test Case Design

### Coverage Requirements

For complex skills, design test cases covering:

| Category | Purpose | Example |
|----------|---------|---------|
| Happy path | Standard workflow execution | "Write a systematic review of AI in healthcare" |
| Edge case | Unusual inputs or conditions | "Only 3 relevant papers found in literature search" |
| Failure recovery | How the skill handles errors | "API rate limited during database search" |
| Resumption | Cross-session continuity | "Continue my review from yesterday" |
| Boundary | Testing limits | "Review with 200+ papers to screen" |

### Test Prompt Realism

Test prompts must be realistic. Not abstract requests but concrete, detailed scenarios:

```
BAD: "Write an academic paper"

GOOD: "I need to write a systematic literature review on the effectiveness
of mindfulness-based interventions for reducing anxiety in university
students. I want to target the Journal of Clinical Psychology. Focus on
RCTs published between 2018 and 2026. Use PRISMA guidelines and Harvard
referencing."
```

### Test Case Schema

```json
{
  "skill_name": "expert-complex-workflow",
  "evals": [
    {
      "id": 1,
      "name": "standard-slr-workflow",
      "prompt": "Full realistic prompt text...",
      "expected_output": "Description of what success looks like",
      "files": ["path/to/input/file.json"],
      "assertions": [],
      "tags": ["happy-path", "academic"]
    }
  ]
}
```

---

## Assertion Design

### Good Assertions Are Objectively Verifiable

```json
{
  "assertions": [
    {
      "text": "Output contains all required IMRaD sections",
      "type": "structural",
      "method": "script",
      "script": "scripts/check_sections.py"
    },
    {
      "text": "All in-text citations follow Harvard format (Author, Year)",
      "type": "formatting",
      "method": "script",
      "script": "scripts/check_citations.py"
    },
    {
      "text": "Word count between 6,000 and 10,000",
      "type": "quantitative",
      "method": "script",
      "script": "scripts/word_count.py"
    },
    {
      "text": "PRISMA flow diagram numbers are internally consistent",
      "type": "numerical_consistency",
      "method": "script",
      "script": "scripts/validate_prisma.py"
    },
    {
      "text": "Methods section provides sufficient detail for replication",
      "type": "qualitative",
      "method": "llm_judge",
      "rubric": "Could a competent researcher replicate this study from the methods section alone?"
    }
  ]
}
```

### Script-Based Assertions (Preferred)

For anything that can be checked programmatically, write and run a script.
Scripts are faster, more reliable, and reusable across iterations.

### LLM-Judge Assertions (When Necessary)

For subjective criteria that resist scripting:
- Writing quality
- Logical coherence
- Argument strength
- Narrative flow

Use specific, binary rubric questions (see Three-Tier Rubric Design below).

---

## Outcome vs Trajectory Metrics

| Metric Type | What It Measures | Key Metrics |
|-------------|-----------------|-------------|
| **Outcome** | Did the task succeed? | Task completion rate, output quality score |
| **Trajectory** | How did it get there? | Exact match, precision, recall |
| **Efficiency** | What did it cost? | Tokens consumed, wall-clock time, API calls |
| **Reliability** | How consistently? | Success rate across N runs, variance (stddev) |

### Trajectory Metrics Explained

- **trajectory_exact_match** — Did the agent follow the exact ideal sequence of steps?
- **trajectory_precision** — Were all actions the agent took necessary? (no wasted steps)
- **trajectory_recall** — Did the agent use all required tools/steps? (no missed steps)

### Measurement Protocol

Run each test case at least 3 times to measure variance. Report:
- Mean score ± standard deviation
- Min and max scores
- Any non-deterministic failures (passed sometimes, failed others)

---

## LLM-as-Judge Evaluation

### Bias Awareness

LLM judges exhibit systematic biases:
- **Position bias** — Favoring information presented earlier
- **Length bias** — Preferring longer outputs regardless of quality
- **Agreeableness bias** — Failing to be sufficiently critical
- Error rates can exceed 50% without mitigation

### Bias Mitigation

1. **Ensemble judging** — Use 3+ judge instances with randomized presentation order
2. **Majority vote** — Accept the majority judgment, not any single judge
3. **Minority veto for safety** — One judge flagging a safety issue overrides majority
4. **Specific rubric questions** — "Is this helpful?" → bad. "Does it provide
   actionable next steps? [Yes/No]" → good
5. **Zero temperature** — Reduce but don't eliminate randomness

### Calibration Target

The industry standard for production deployment:
**≥ 0.80 Spearman correlation between automated judge and human domain experts**

### Achieving High Correlation

1. Create a calibration set: 50-100 outputs scored by human experts
2. Run LLM judge on the same outputs
3. Calculate Spearman correlation
4. If < 0.80: refine rubric, add examples, adjust ensemble weights
5. Re-test until threshold met
6. Periodically re-calibrate as the skill evolves

---

## Three-Tier Rubric Design

For publication-quality evaluation:

### Level 1: Primary Dimensions (7)

1. Accuracy
2. Completeness
3. Coherence
4. Methodology
5. Citation Quality
6. Formatting
7. Originality

### Level 2: Sub-Dimensions (25)

```
Accuracy (4)
├── Factual correctness
├── Statistical validity
├── Source attribution accuracy
└── Claim-evidence alignment

Completeness (4)
├── Required section coverage
├── Topic coverage
├── Data coverage
└── Limitation acknowledgment

Coherence (3)
├── Logical flow
├── Cross-section consistency
└── Argument structure

Methodology (4)
├── Approach appropriateness
├── Procedural rigor
├── Reproducibility
└── Justification quality

Citation Quality (3)
├── Format compliance
├── Citation-claim matching
└── Source diversity

Formatting (4)
├── Structure compliance
├── Style guide adherence
├── Table/figure formatting
└── Reference list formatting

Originality (3)
├── Novel contribution
├── Critical analysis depth
└── Synthesis beyond summarization
```

### Level 3: Fine-Grained Criteria (Observable Yes/No)

```
Accuracy > Factual correctness:
  [ ] All numerical values match cited sources
  [ ] No claims lack supporting evidence
  [ ] Dates and author names verified against primary sources
  [ ] Statistical test names used correctly
  [ ] Effect sizes reported with confidence intervals where applicable

Accuracy > Claim-evidence alignment:
  [ ] Each claim in Results is supported by data presented
  [ ] Discussion interpretations don't exceed the evidence
  [ ] Causal language only used when warranted by study design
  [ ] Hedging language appropriate to evidence strength
```

---

## Blind Comparison Protocol

For rigorous A/B testing between skill versions:

1. **Prepare outputs** — Run Version A and Version B on same test cases
2. **Anonymize** — Label as "Output X" and "Output Y" (randomize assignment)
3. **Judge** — Independent judge agent evaluates both against rubric without
   knowing which is which
4. **Select winner** — Judge picks winner with detailed reasoning
5. **Analyze** — Analyzer agent investigates WHY the winner won
6. **De-anonymize** — Reveal which version was which
7. **Apply insights** — Use the analysis to improve the losing version

### When to Use Blind Comparison

- Marginal improvements where human review can't easily distinguish
- Controversial changes where bias might influence judgment
- Final validation before shipping a major version update

---

## Continuous Improvement Loop

```
Deploy Skill v1.0
      ↓
Monitor: success rate, user feedback, failure patterns
      ↓
Identify: which test cases fail most? what patterns emerge?
      ↓
Draft v1.1 with targeted improvements
      ↓
Run full eval suite: v1.1 vs v1.0
      ↓
Blind comparison if results are marginal
      ↓
Deploy v1.1 ONLY if measurably better
      ↓
Expand test set (add cases from production failures)
      ↓
Repeat
```

### Regression Prevention

When fixing an issue:
1. Add a test case that demonstrates the issue
2. Verify the fix passes the new test case
3. Verify all existing test cases still pass
4. The new test case becomes part of the permanent suite

---

## Related References

- `quality-gates.md` — Evaluation results inform gate pass/fail criteria
- `two-zone-architecture.md` — Script-based assertions are Deterministic; LLM-judge is Reasoning
- `resilience-patterns.md` — Test failure recovery and iterative improvement patterns
- `security-checklist.md` — Evaluation should include security-focused test cases
