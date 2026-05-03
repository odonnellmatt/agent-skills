# Quality Gate Template

Use this template for each quality gate in a complex workflow.
Replace all `[PLACEHOLDER]` values.

---

```markdown
# Quality Gate [N]: [Phase A] → [Phase B]

## Purpose
Verify that [Phase A] outputs meet the minimum requirements before
[Phase B] begins. Prevents error propagation downstream.

## Automated Checks

Run the gate validation script:
```bash
python scripts/gate_[N]_validator.py \
  --input [path to Phase A outputs] \
  --criteria [path to criteria config]
```

The script validates:
- [ ] [Criterion 1 — specific, measurable, e.g., "All required fields populated"]
- [ ] [Criterion 2 — specific, measurable, e.g., "N >= minimum threshold"]
- [ ] [Criterion 3 — specific, measurable, e.g., "Schema validation passes"]

Script output:
```json
{
  "gate": "QG[N]",
  "status": "pass | fail",
  "checks": [
    {"name": "[criterion]", "passed": true, "value": "[actual]", "threshold": "[required]"},
    {"name": "[criterion]", "passed": false, "value": "[actual]", "threshold": "[required]",
     "failure_detail": "[Specific explanation of what failed and why]"}
  ],
  "overall_pass": true,
  "timestamp": "[ISO-8601]"
}
```

## Human Review Items

Present the following to the user for approval:
- [ ] [Subjective criterion 1 — what to look for, why it matters]
- [ ] [Subjective criterion 2 — what to look for, why it matters]

Format the review request as:
"Phase [A] is complete. [Brief summary of what was accomplished].
 Before proceeding to [Phase B], please review:
 1. [Item] — [context for what to evaluate]
 2. [Item] — [context for what to evaluate]
 Approve to proceed, or note any concerns."

## Pass Criteria

ALL automated checks must pass AND human approval must be received.
Both conditions are required — neither alone is sufficient.

## On Failure

### Automated Check Failures
| Failed Check | Route To | Feedback |
|-------------|----------|----------|
| [Criterion 1] | [Upstream skill name] | "[Specific remediation instructions]" |
| [Criterion 2] | [Upstream skill name] | "[Specific remediation instructions]" |

### Human Rejection
- Log the rejection reason in the state file
- Route to [appropriate upstream skill] with the user's feedback
- Do NOT re-prompt for approval on unchanged content

## State Update

On pass:
```json
{
  "quality_gates": {
    "QG[N]": {
      "status": "passed",
      "checked_at": "[timestamp]",
      "automated_results": {"[criterion]": true, "[criterion]": true},
      "human_approved": true,
      "notes": "[Any user comments]"
    }
  },
  "progress": {
    "current_phase": [N+1],
    "gates_passed": ["QG1", "...", "QG[N]"]
  }
}
```
```
