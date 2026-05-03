# The Two-Zone Architecture

## Table of Contents

1. [Core Principle](#core-principle)
2. [Zone Classification Guide](#zone-classification-guide)
3. [Enforcement Language Patterns](#enforcement-language-patterns)
4. [Script Design Patterns](#script-design-patterns)
5. [Common Mistakes](#common-mistakes)

---

## Core Principle

The Two-Zone Architecture strictly separates deterministic computation from probabilistic
reasoning. This is the single most impactful design decision for skill reliability.

**Deterministic Zone:** If a process requires 100% consistency across every run — lock it
in a script. The LLM must never improvise calculations, data transforms, or formatting.

**Reasoning Zone:** Reserve the LLM's cognitive budget for interpreting results, handling
edge cases, narrative synthesis, and user interaction.

**Why this matters:** LLMs exhibit "people-pleasing" behavior. They soften negative results,
round numbers to look cleaner, and rationalize adjustments. In production, this has caused
agents to silently modify risk scores, recalculate statistics incorrectly, and alter
citation details.

---

## Zone Classification Guide

### Always Deterministic (Script)

| Task Category | Examples |
|--------------|---------|
| Mathematical calculations | Financial ratios, statistical tests, scoring algorithms |
| Data transformations | CSV parsing, JSON restructuring, schema validation |
| Format enforcement | Citation formatting, PRISMA flow numbers, template rendering |
| Validation checks | Schema compliance, reference cross-checking, word counts |
| Deduplication | DOI matching, fuzzy string matching with defined thresholds |
| Threshold comparisons | Pass/fail against numeric criteria (Kappa >= 0.60) |

### Always Reasoning (LLM)

| Task Category | Examples |
|--------------|---------|
| Interpretation | What do these results mean in context? |
| Synthesis | Weaving multiple sources into coherent narrative |
| Edge case handling | Ambiguous data, unusual patterns, exceptions |
| Creative judgment | Tone, framing, argument construction |
| User interaction | Clarifying requirements, explaining decisions |
| Strategic decisions | Which methodology to use, what to prioritize |

### Judgment Required (Classify Per Workflow)

| Task Category | Deterministic When... | Reasoning When... |
|--------------|----------------------|-------------------|
| Screening | Criteria are strictly defined (keyword match) | Criteria require interpretation (relevance judgment) |
| Quality assessment | Using validated tools (RoB 2, NOS) with fixed scales | Assessing narrative quality or originality |
| Report generation | Template-filling with fixed data | Executive summary requiring synthesis |

---

## Enforcement Language Patterns

### Strong Enforcement (Recommended)

```markdown
## Step 3: Calculate Inter-Rater Reliability

Run the Kappa calculation script:
```bash
python scripts/kappa_calculator.py --rater1 data/r1.json --rater2 data/r2.json
```

Read the script's JSON output. The script provides the authoritative values for
kappa_score, agreement_percentage, and interpretation.

**The script is the single source of truth for all statistical values. Never
override, adjust, recalculate, or reinterpret any value from the script's
output. If a value seems wrong, re-run the script with corrected inputs —
do not manually edit the output.**

WHY: LLMs have been observed silently "rounding" Kappa from 0.58 to 0.60 to
pass quality gates. This defeats the purpose of the gate.

REASONING TASK: Based on the script's Kappa score, decide the next action:
- If kappa >= 0.80: Proceed to next phase
- If 0.60 <= kappa < 0.80: Flag disagreement patterns for discussion
- If kappa < 0.60: Route back to screening calibration
```

### Weak Enforcement (Avoid)

```markdown
## Step 3: Calculate Inter-Rater Reliability

Calculate Cohen's Kappa for the two raters. Try to be accurate.
If Kappa is above 0.60, proceed.
```

The weak version invites the LLM to perform the calculation itself, introduces
ambiguity about what "try to be accurate" means, and provides no enforcement
mechanism.

---

## Script Design Patterns

### Input/Output Contract

Every deterministic script should follow this pattern:

**Input:** Structured (JSON file, CLI arguments, or stdin)
**Output:** Structured JSON to stdout
**Errors:** Structured JSON to stdout with `"error": true`

```python
#!/usr/bin/env python3
"""Calculate inter-rater reliability (Cohen's Kappa)."""
import json
import sys
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--rater1', required=True, help='Path to rater 1 JSON')
    parser.add_argument('--rater2', required=True, help='Path to rater 2 JSON')
    args = parser.parse_args()

    try:
        with open(args.rater1) as f:
            r1 = json.load(f)
        with open(args.rater2) as f:
            r2 = json.load(f)
    except FileNotFoundError as e:
        print(json.dumps({
            "error": True,
            "error_type": "file_not_found",
            "message": f"File not found: {e.filename}",
            "suggestion": "Check the file path and ensure screening is complete.",
            "recoverable": True
        }))
        sys.exit(1)

    # ... calculation logic ...

    print(json.dumps({
        "error": False,
        "kappa_score": 0.82,
        "agreement_percentage": 89.3,
        "interpretation": "almost_perfect",
        "n_items": len(r1),
        "disagreements": [
            {"item_id": "study_042", "rater1": "include", "rater2": "exclude"}
        ]
    }))

if __name__ == '__main__':
    main()
```

### Idempotency Requirement

Scripts must produce identical output for identical input, regardless of how many
times they run. This means:

- No side effects (don't write to databases, send emails, or modify shared state)
- No reliance on external state that may change (current time, random seeds)
- If randomness is needed, accept a seed parameter
- If time-dependent, accept a timestamp parameter

### Error Messages Must Be Actionable

The LLM's self-correction loop depends on understanding what went wrong.

```python
# BAD — the LLM cannot reason about this
sys.exit(1)

# BAD — too vague
print("Error occurred")
sys.exit(1)

# GOOD — actionable, specific, suggests recovery
print(json.dumps({
    "error": True,
    "error_type": "data_validation",
    "message": "Column 'revenue' not found in input file.",
    "available_columns": ["sales", "costs", "profit", "date"],
    "suggestion": "The input may use 'sales' instead of 'revenue'. Update the column mapping.",
    "recoverable": True
}))
sys.exit(1)
```

---

## Common Mistakes

| Mistake | Consequence | Fix |
|---------|------------|-----|
| Letting LLM do arithmetic | Wrong results, especially with large numbers | Script it |
| "Calculate approximately" | LLM rounds, truncates, or estimates | Require exact script output |
| No zone label on steps | Unclear whether LLM should reason or execute | Label every step |
| Script output as free text | LLM misparses or selectively reads | Always JSON output |
| Trusting LLM to format citations | Inconsistent formatting, fabricated DOIs | Script with validated data |
| No enforcement language | LLM "helpfully" adjusts script output | Explicit prohibition with WHY |

---

## Related References

- `architecture-patterns.md` — Apply zone classification to each orchestration pattern
- `quality-gates.md` — Automated gates use Deterministic Zone scripts; human gates are Reasoning
- `resilience-patterns.md` — Script idempotency and error handling for Deterministic Zone
- `security-checklist.md` — Input validation belongs in Deterministic Zone scripts
