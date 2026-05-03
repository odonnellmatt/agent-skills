# Sub-Skill Template

Use this template for each individual skill within a complex workflow.
Replace all `[PLACEHOLDER]` values with actual content.

---

```markdown
# [Skill Name]

## Purpose

[1-2 sentences: What this skill accomplishes and why it matters in the
larger workflow. Include the phase it belongs to.]

## Inputs

| Input | Source | Required | Format |
|-------|--------|----------|--------|
| [input_name] | [previous skill / user / state file] | Yes | JSON |
| [input_name] | [user prompt / config] | No | Text |

## Process

### Step 1: [Step Name] — [Deterministic / Reasoning / Judgment]

[Instructions for this step.]

[If Deterministic:]
```bash
python scripts/[script_name].py --input [path] --output [path]
```

Read the script's JSON output. The script provides the authoritative values
for [list fields]. Never override or recalculate these values.

[If Reasoning:]
Based on the data from Step 1, [describe the reasoning task].
Consider: [key factors to weigh].

### Step 2: [Step Name] — [Deterministic / Reasoning / Judgment]

[...]

### Step N: [Step Name] — [Deterministic / Reasoning / Judgment]

[...]

## Outputs

| Output | Format | Destination |
|--------|--------|-------------|
| [output_name] | JSON | [next skill / state file / user] |
| [artifact_name] | Markdown | [output directory] |

## Quality Criteria

Before handing off to the next skill, verify:
- [ ] [Specific, measurable criterion 1]
- [ ] [Specific, measurable criterion 2]
- [ ] [Specific, measurable criterion 3]

## Error Handling

| Error | Cause | Recovery |
|-------|-------|----------|
| [error_type] | [what causes it] | [specific recovery action] |
| [error_type] | [what causes it] | [specific recovery action] |

## Gotchas

Edge cases and prior mistakes specific to this skill. Only list what the agent
would not figure out from the process above.

- [Non-obvious edge case and the correct handling]
- [Input shape that looks valid but must be rejected]

## Constraints

- [Explicit constraint 1 with WHY explanation]
- [Explicit constraint 2 with WHY explanation]
```
