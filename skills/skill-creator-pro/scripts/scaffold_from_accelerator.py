#!/usr/bin/env python3
"""Scaffold a complete skill directory from a domain accelerator blueprint.

Parses an accelerator reference file to extract:
- Phase architecture
- Sub-skill inventory (name, purpose, zone)
- Quality gate definitions
- Two-zone split
- Common failure modes

Then generates:
- Master SKILL.md with full skill inventory and gate tables
- Individual sub-skill .md files from the sub-skill template
- Quality gate validator scripts (one per gate)
- State schema JSON customized to the workflow
- A scaffold report showing what was generated and what needs human authoring

Usage:
    python scripts/scaffold_from_accelerator.py \
        --accelerator references/cybersecurity-assessment-workflow.md \
        --output /path/to/new-skill-directory \
        --name "Cybersecurity Assessment" \
        [--templates /path/to/assets/]

Output: A complete skill directory ready for human refinement.
"""

import argparse
import json
import os
import re
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path


def parse_accelerator(accelerator_path: Path) -> dict:
    """Parse an accelerator reference file into structured data."""
    content = accelerator_path.read_text()

    result = {
        "title": "",
        "overview": "",
        "sub_skills": [],
        "quality_gates": [],
        "two_zone": {"deterministic": [], "reasoning": []},
        "failure_modes": [],
        "phases": [],
    }

    # Extract title from first H1
    title_match = re.search(r'^# Domain Accelerator:\s*(.+)$', content, re.MULTILINE)
    if title_match:
        result["title"] = title_match.group(1).strip()

    # Extract overview section
    overview_match = re.search(
        r'## Overview\s*\n(.*?)(?=\n## )', content, re.DOTALL
    )
    if overview_match:
        result["overview"] = overview_match.group(1).strip()

    # Extract sub-skill inventory tables
    # Pattern: | # | Skill | Purpose | Zone |
    skill_pattern = re.compile(
        r'\|\s*(\d+)\s*\|\s*`([^`]+)`\s*\|\s*([^|]+)\|\s*([^|]+)\|'
    )
    for match in skill_pattern.finditer(content):
        result["sub_skills"].append({
            "number": int(match.group(1)),
            "name": match.group(2).strip(),
            "purpose": match.group(3).strip(),
            "zone": match.group(4).strip(),
        })

    # Extract phases — they appear inside code fences as "Phase N: Name (N skills)"
    # Also try markdown header format as fallback: "### Phase N — Name (N skills)"
    code_phase_pattern = re.compile(
        r'^Phase\s+(\d+)\s*[:\-—–]\s*(.+?)(?:\s*\((\d+)\s*skills?(?:,\s*parallel[^)]*)?'
        r'\))?$',
        re.MULTILINE,
    )
    for match in code_phase_pattern.finditer(content):
        result["phases"].append({
            "number": int(match.group(1)),
            "name": match.group(2).strip(),
            "skill_count": int(match.group(3)) if match.group(3) else 0,
        })

    # Fallback: try markdown header format
    if not result["phases"]:
        md_phase_pattern = re.compile(
            r'###\s*Phase\s+(\d+)\s*[—–\-:]\s*(.+?)(?:\s*\((\d+)\s*skills?\))?$',
            re.MULTILINE,
        )
        for match in md_phase_pattern.finditer(content):
            result["phases"].append({
                "number": int(match.group(1)),
                "name": match.group(2).strip(),
                "skill_count": int(match.group(3)) if match.group(3) else 0,
            })

    # Deduplicate phases by number (some accelerators have multiple pipelines
    # with overlapping phase numbers — keep the first occurrence per number,
    # but also capture all pipelines)
    seen_phases = set()
    unique_phases = []
    for phase in result["phases"]:
        key = phase["number"]
        if key not in seen_phases:
            seen_phases.add(key)
            unique_phases.append(phase)
    result["phases"] = unique_phases

    # Extract inline quality gate descriptions from phase architecture code blocks
    # Format: ↓ QG1: description text
    inline_gates = {}
    inline_gate_pattern = re.compile(
        r'↓\s*QG(\d+)\s*:\s*(.+?)$', re.MULTILINE
    )
    for match in inline_gate_pattern.finditer(content):
        gate_num = int(match.group(1))
        gate_desc = match.group(2).strip()
        if gate_num not in inline_gates:
            inline_gates[gate_num] = {
                "name": gate_desc[:80],
                "checks": [c.strip() for c in gate_desc.split(',') if c.strip()],
            }

    # Extract detailed quality gate definitions (### QG sections with checklists)
    detailed_gates = {}
    gate_section = re.search(r'## Quality Gate Definitions(.*?)(?=\n## |\Z)', content, re.DOTALL)
    if gate_section:
        gate_text = gate_section.group(1)
        gate_headers = re.finditer(
            r'###\s*QG(\d+)\s*:?\s*(.+?)(?=\n###|\n## |\Z)', gate_text, re.DOTALL
        )
        for gh in gate_headers:
            gate_num = int(gh.group(1))
            gate_name = gh.group(2).split('\n')[0].strip()
            gate_body = gh.group(2).strip()

            checks = re.findall(r'- \[ \]\s*(.+)', gate_body)
            detailed_gates[gate_num] = {
                "name": gate_name,
                "checks": checks,
            }

    # Merge: prefer detailed definitions, fall back to inline descriptions
    all_gate_nums = sorted(set(list(inline_gates.keys()) + list(detailed_gates.keys())))
    for num in all_gate_nums:
        if num in detailed_gates:
            result["quality_gates"].append(detailed_gates[num])
        elif num in inline_gates:
            result["quality_gates"].append(inline_gates[num])

    # Extract two-zone split table
    zone_section = re.search(r'## Two-Zone Split.*?\n(.*?)(?=\n## |\Z)', content, re.DOTALL)
    if zone_section:
        zone_text = zone_section.group(1)
        # Look for two-column table rows
        zone_rows = re.findall(r'\|\s*([^|]+)\|\s*([^|]+)\|', zone_text)
        for row in zone_rows:
            left = row[0].strip()
            right = row[1].strip()
            # Skip header rows
            if left.startswith('--') or left.lower() in ('deterministic', 'always deterministic'):
                continue
            if left and right and left != 'Deterministic' and right != 'Reasoning':
                result["two_zone"]["deterministic"].append(left)
                result["two_zone"]["reasoning"].append(right)

    # Extract failure modes table
    failure_section = re.search(r'## Common Failure Modes\s*\n(.*?)(?=\n## |\Z)', content, re.DOTALL)
    if failure_section:
        failure_text = failure_section.group(1)
        failure_rows = re.findall(r'\|\s*([^|]+)\|\s*([^|]+)\|\s*([^|]+)\|', failure_text)
        for row in failure_rows:
            failure = row[0].strip()
            cause = row[1].strip()
            prevention = row[2].strip()
            if failure.startswith('--') or failure.lower() == 'failure':
                continue
            if failure and cause and prevention:
                result["failure_modes"].append({
                    "failure": failure,
                    "cause": cause,
                    "prevention": prevention,
                })

    return result


def generate_master_skill_md(data: dict, skill_name: str) -> str:
    """Generate the master SKILL.md from parsed accelerator data."""

    # Build skill name slug
    slug = re.sub(r'[^a-z0-9]+', '-', skill_name.lower()).strip('-')

    # Group skills by phase based on declared skill counts
    phase_skill_groups = {}
    skill_idx = 0
    remaining = len(data["sub_skills"])

    for phase in data["phases"]:
        count = phase.get("skill_count", 0)
        if count == 0:
            # Estimate: divide remaining skills evenly across remaining phases
            phases_left = len(data["phases"]) - list(p["number"] for p in data["phases"]).index(phase["number"])
            count = max(1, remaining // max(phases_left, 1))
        # Cap to available skills
        count = min(count, remaining)
        phase_skill_groups[phase["number"]] = []
        for _ in range(count):
            if skill_idx < len(data["sub_skills"]):
                phase_skill_groups[phase["number"]].append(data["sub_skills"][skill_idx])
                skill_idx += 1
                remaining -= 1

    # Handle remaining skills (from multi-pipeline accelerators)
    if skill_idx < len(data["sub_skills"]) and data["phases"]:
        last_phase = data["phases"][-1]["number"]
        for i in range(skill_idx, len(data["sub_skills"])):
            phase_skill_groups.setdefault(last_phase, []).append(data["sub_skills"][i])

    # Build inventory markdown
    inventory_sections = []
    for phase in data["phases"]:
        skills_in_phase = phase_skill_groups.get(phase["number"], [])
        section = f"### Phase {phase['number']} — {phase['name']} ({len(skills_in_phase)} skills)\n"
        section += "| # | Skill File | Purpose |\n"
        section += "|---|-----------|--------|\n"
        for s in skills_in_phase:
            section += f"| {s['number']} | `{s['name']}.md` | {s['purpose']} |\n"
        inventory_sections.append(section)

    inventory_text = "\n".join(inventory_sections)

    # Build quality gates table
    gate_rows = ""
    for i, gate in enumerate(data["quality_gates"], 1):
        gate_rows += f"| QG{i} | {gate['name']} | {'; '.join(gate['checks'][:3])} |\n"

    # Build error handling table
    error_rows = ""
    for fm in data["failure_modes"][:8]:
        error_rows += f"| {fm['failure']} | {fm['cause']} | {fm['prevention']} |\n"

    total_skills = len(data["sub_skills"])

    md = f"""---
name: {slug}
description: >
  A complete, {len(data['phases'])}-phase agent skillset for {data['title'].lower()}.
  Contains {total_skills} composable skills orchestrated by a master controller with
  quality gates and automated feedback loops. Use when the user wants to
  [ADD SPECIFIC TRIGGER PHRASES HERE].
  Do NOT use for [ADD NEGATIVE TRIGGERS HERE].
---

# {skill_name}

## Quick Start

- **Start new**: Say "Start a new {skill_name.lower()}"
- **Resume**: Say "Continue my {skill_name.lower()}" or "What's next?"
- **Single skill**: Invoke any skill by name for standalone use

## Entry Point

The **master controller** is `{slug}-orchestrator`. Always start there for
end-to-end workflows.

## Complete Skill Inventory ({total_skills} Skills)

{inventory_text}

### Support Skills (available at any phase)
| # | Skill File | Purpose |
|---|-----------|---------|
| {total_skills + 1} | `{slug}-orchestrator.md` | Master controller — chains all skills, enforces gates |
| {total_skills + 2} | `{slug}-gate-verifier.md` | Quality gate enforcement mechanism |
| {total_skills + 3} | `{slug}-progress-tracker.md` | State, metrics, decision log |
| {total_skills + 4} | `{slug}-feedback-router.md` | Route issues back to correct phase/skill |
| {total_skills + 5} | `{slug}-state-schema.md` | Persistent JSON state schema |

## Quality Gates

| Gate | Phase Transition | Key Checks |
|------|-----------------|------------|
{gate_rows}

## Feedback Loop System

When an issue is detected at **any phase**, the `{slug}-feedback-router`
automatically identifies the correct upstream skill and routes back.
The pipeline never silently proceeds with known issues.

## State Persistence

Project state is persisted as JSON (see `{slug}-state-schema.md`) and
auto-saved at every gate transition. This enables cross-session continuity.

## Error Handling

| Error | Cause | Recovery |
|-------|-------|----------|
{error_rows}

## Memory Integration

- Save user domain expertise and preferences on first discovery
- Save validated feedback corrections to prevent repeated mistakes
- Never save ephemeral workflow state to long-term memory
"""
    return md


def generate_sub_skill_md(skill: dict, workflow_name: str) -> str:
    """Generate a sub-skill .md file from parsed skill data."""

    zone_label = skill["zone"]
    if zone_label.lower() == "deterministic":
        zone_guidance = """### Step 1: Execute — Deterministic

Run the processing script:
```bash
python scripts/{script_name}.py --input [INPUT_PATH] --output [OUTPUT_PATH]
```

Read the script's JSON output. The script provides the authoritative values.
Never override, adjust, or recalculate any value from the script's output.

### Step 2: Validate — Deterministic

Verify the output against expected schema and constraints.
""".format(script_name=skill["name"].replace("-", "_"))
    elif zone_label.lower() == "reasoning":
        zone_guidance = """### Step 1: Analyze — Reasoning

Based on the inputs provided, analyze the relevant context.
Consider: [KEY FACTORS TO WEIGH — FILL IN DOMAIN-SPECIFIC GUIDANCE]

### Step 2: Generate — Reasoning

Produce the output following the quality criteria below.
Explain reasoning for any judgment calls.
"""
    else:
        zone_guidance = """### Step 1: Extract Data — Deterministic

Run the extraction/processing script:
```bash
python scripts/{script_name}.py --input [INPUT_PATH] --output [OUTPUT_PATH]
```

Read the script's JSON output. These values are authoritative.

### Step 2: Interpret Results — Reasoning

Based on the script output, apply domain judgment to:
- [INTERPRETATION TASK 1]
- [INTERPRETATION TASK 2]

### Step 3: Produce Output — Mixed

Combine deterministic data with reasoned interpretation into the final output.
""".format(script_name=skill["name"].replace("-", "_"))

    md = f"""# {skill['name'].replace('-', ' ').title()}

## Purpose

{skill['purpose']}

**Zone classification:** {zone_label}

## Inputs

| Input | Source | Required | Format |
|-------|--------|----------|--------|
| [INPUT_1] | [previous skill / user / state file] | Yes | JSON |
| [INPUT_2] | [configuration / user prompt] | No | Text |

## Process

{zone_guidance}

## Outputs

| Output | Format | Destination |
|--------|--------|-------------|
| [OUTPUT_1] | JSON | [next skill / state file / user] |
| [ARTIFACT_1] | Markdown | [output directory] |

## Quality Criteria

Before handing off to the next skill, verify:
- [ ] [CRITERION 1 — specific and measurable]
- [ ] [CRITERION 2 — specific and measurable]
- [ ] [CRITERION 3 — specific and measurable]

## Error Handling

| Error | Cause | Recovery |
|-------|-------|----------|
| [ERROR_TYPE] | [What causes it] | [Specific recovery action] |

## Constraints

- [CONSTRAINT WITH WHY — e.g., "Never recalculate script output because LLMs
  exhibit people-pleasing behavior that corrupts deterministic values"]
"""
    return md


def generate_state_schema(data: dict, slug: str) -> dict:
    """Generate a customized state schema from parsed accelerator data."""

    phases_completed_example = []
    gates = {}
    for i, phase in enumerate(data["phases"], 1):
        gates[f"QG{i}"] = {
            "status": "not_checked",
            "checked_at": None,
            "automated_results": {},
            "human_approved": False,
            "notes": None,
        }

    return {
        "$schema": "workflow-state-v1",
        "workflow": {
            "id": "[auto-generated UUID]",
            "type": slug,
            "title": f"[Human-readable title]",
            "created_at": "[ISO-8601 timestamp]",
            "last_updated": "[ISO-8601 timestamp]",
        },
        "progress": {
            "current_phase": 1,
            "current_step": "1.1",
            "phases_completed": [],
            "gates_passed": [],
            "status": "in_progress",
        },
        "artifacts": {
            "by_phase": {
                f"phase_{p['number']}": {} for p in data["phases"]
            },
            "primary_output": None,
        },
        "decisions": [],
        "quality_gates": gates,
        "metrics": {},
        "feedback_log": [],
        "configuration": {
            "output_format": "md",
            "quality_thresholds": {},
        },
        "session_log": [],
    }


def generate_gate_validator_script(gate: dict, gate_num: int) -> str:
    """Generate a quality gate validation script."""

    checks_code = ""
    for i, check in enumerate(gate["checks"]):
        safe_name = re.sub(r'[^a-z0-9_]', '_', check.lower()[:50]).strip('_')
        checks_code += f"""
    # Check {i + 1}: {check}
    checks.append({{
        "name": "{check[:80]}",
        "passed": True,  # TODO: implement actual validation logic
        "value": "NOT_IMPLEMENTED",
        "threshold": "DEFINE_THRESHOLD",
    }})
"""

    return f'''#!/usr/bin/env python3
"""Quality Gate {gate_num} Validator: {gate["name"]}

Auto-generated scaffold. TODO: implement actual validation logic for each check.

Usage:
    python scripts/gate_{gate_num}_validator.py --input [PATH] --criteria [PATH]
"""

import argparse
import json
import sys


def main():
    parser = argparse.ArgumentParser(description="Quality Gate {gate_num} Validator")
    parser.add_argument("--input", required=True, help="Path to phase output data")
    parser.add_argument("--criteria", help="Path to criteria configuration (optional)")
    args = parser.parse_args()

    checks = []
{checks_code}
    overall_pass = all(c["passed"] for c in checks)

    result = {{
        "gate": "QG{gate_num}",
        "status": "pass" if overall_pass else "fail",
        "checks": checks,
        "overall_pass": overall_pass,
        "timestamp": None,  # Set at runtime
    }}

    print(json.dumps(result, indent=2))
    sys.exit(0 if overall_pass else 1)


if __name__ == "__main__":
    main()
'''


def scaffold(accelerator_path: Path, output_path: Path, skill_name: str, templates_path: Path = None):
    """Main scaffolding function."""

    # Parse the accelerator
    data = parse_accelerator(accelerator_path)

    if not data["sub_skills"]:
        return {
            "error": True,
            "message": f"No sub-skills found in {accelerator_path.name}. Is this a valid accelerator file?",
            "suggestion": "Ensure the accelerator has sub-skill inventory tables with the format: | # | `skill-name` | Purpose | Zone |",
        }

    slug = re.sub(r'[^a-z0-9]+', '-', skill_name.lower()).strip('-')

    # Create directory structure
    output_path.mkdir(parents=True, exist_ok=True)
    (output_path / "scripts").mkdir(exist_ok=True)
    (output_path / "references").mkdir(exist_ok=True)
    (output_path / "assets").mkdir(exist_ok=True)
    (output_path / "state").mkdir(exist_ok=True)

    generated_files = []

    # 1. Generate master SKILL.md
    master_md = generate_master_skill_md(data, skill_name)
    (output_path / "SKILL.md").write_text(master_md)
    generated_files.append("SKILL.md")

    # 2. Generate sub-skill files
    for skill in data["sub_skills"]:
        filename = f"{skill['name']}.md"
        sub_md = generate_sub_skill_md(skill, skill_name)
        (output_path / filename).write_text(sub_md)
        generated_files.append(filename)

    # 3. Generate support skill stubs
    support_skills = [
        (f"{slug}-orchestrator.md", "Master controller — chains all skills, enforces quality gates, manages state."),
        (f"{slug}-gate-verifier.md", "Quality gate enforcement mechanism — runs automated checks and routes failures."),
        (f"{slug}-progress-tracker.md", "State management, metrics collection, decision logging, and progress dashboard."),
        (f"{slug}-feedback-router.md", "When issues are detected, identifies the correct upstream skill and routes back."),
    ]
    for filename, purpose in support_skills:
        stub = f"# {filename.replace('.md', '').replace('-', ' ').title()}\n\n## Purpose\n\n{purpose}\n\n## TODO\n\nThis is a scaffold stub. Implement the full skill logic.\n"
        (output_path / filename).write_text(stub)
        generated_files.append(filename)

    # 4. Generate state schema
    state_schema = generate_state_schema(data, slug)
    state_path = output_path / f"{slug}-state-schema.md"
    state_content = f"# State Schema: {skill_name}\n\n```json\n{json.dumps(state_schema, indent=2)}\n```\n"
    state_path.write_text(state_content)
    generated_files.append(f"{slug}-state-schema.md")

    # Also save as JSON in state/
    (output_path / "state" / "state_template.json").write_text(
        json.dumps(state_schema, indent=2)
    )
    generated_files.append("state/state_template.json")

    # 5. Generate quality gate validator scripts
    for i, gate in enumerate(data["quality_gates"], 1):
        script_content = generate_gate_validator_script(gate, i)
        script_path = output_path / "scripts" / f"gate_{i}_validator.py"
        script_path.write_text(script_content)
        os.chmod(script_path, 0o755)
        generated_files.append(f"scripts/gate_{i}_validator.py")

    # 6. Copy accelerator as reference
    (output_path / "references" / accelerator_path.name).write_text(
        accelerator_path.read_text()
    )
    generated_files.append(f"references/{accelerator_path.name}")

    # 7. Generate scaffold report
    todo_items = []
    for skill in data["sub_skills"]:
        todo_items.append(f"- [ ] **{skill['name']}.md** — Fill in inputs, process steps, outputs, quality criteria, error handling")
        if skill["zone"].lower() in ("deterministic", "mixed"):
            script_name = skill["name"].replace("-", "_")
            todo_items.append(f"  - [ ] Write `scripts/{script_name}.py` — deterministic execution script")

    for i, gate in enumerate(data["quality_gates"], 1):
        todo_items.append(f"- [ ] **scripts/gate_{i}_validator.py** — Implement actual validation logic (currently stubs)")

    todo_items.extend([
        f"- [ ] **{slug}-orchestrator.md** — Implement full orchestration logic",
        f"- [ ] **{slug}-gate-verifier.md** — Implement gate enforcement mechanism",
        f"- [ ] **{slug}-progress-tracker.md** — Implement state tracking",
        f"- [ ] **{slug}-feedback-router.md** — Implement feedback routing table",
        "- [ ] **SKILL.md** — Add specific trigger phrases and negative triggers to description",
        "- [ ] **SKILL.md** — Review and refine quality gate criteria",
        "- [ ] Run test cases and iterate",
    ])

    report = {
        "error": False,
        "skill_name": skill_name,
        "slug": slug,
        "source_accelerator": str(accelerator_path),
        "output_directory": str(output_path),
        "generated_files": generated_files,
        "file_count": len(generated_files),
        "sub_skills_scaffolded": len(data["sub_skills"]),
        "support_skills_scaffolded": len(support_skills) + 1,  # +1 for state schema
        "gate_validators_generated": len(data["quality_gates"]),
        "phases": len(data["phases"]),
        "status": "SCAFFOLD_COMPLETE",
        "next_steps": "All files are scaffolded with structure and placeholders. Human authoring needed for:",
        "todo": todo_items,
    }

    # Save report
    (output_path / "SCAFFOLD_REPORT.json").write_text(json.dumps(report, indent=2))
    generated_files.append("SCAFFOLD_REPORT.json")

    return report


def main():
    parser = argparse.ArgumentParser(
        description="Scaffold a complete skill directory from a domain accelerator blueprint."
    )
    parser.add_argument(
        "--accelerator", required=True,
        help="Path to the accelerator reference .md file"
    )
    parser.add_argument(
        "--output", required=True,
        help="Path to the output skill directory"
    )
    parser.add_argument(
        "--name", required=True,
        help="Human-readable name for the skill (e.g., 'Cybersecurity Assessment')"
    )
    parser.add_argument(
        "--templates",
        help="Path to the assets/ directory containing templates (optional)"
    )
    args = parser.parse_args()

    accelerator_path = Path(args.accelerator).resolve()
    output_path = Path(args.output).resolve()

    if not accelerator_path.exists():
        print(json.dumps({
            "error": True,
            "message": f"Accelerator file not found: {accelerator_path}",
            "suggestion": "Check the path. Available accelerators are in the references/ directory.",
        }, indent=2))
        sys.exit(1)

    templates_path = Path(args.templates).resolve() if args.templates else None

    result = scaffold(accelerator_path, output_path, args.name, templates_path)
    print(json.dumps(result, indent=2))
    sys.exit(0 if not result.get("error") else 1)


if __name__ == "__main__":
    main()
