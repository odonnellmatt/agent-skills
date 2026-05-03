#!/usr/bin/env python3
"""Validate the structure and completeness of a complex skill directory.

Checks directory structure, SKILL.md frontmatter, line counts, reference
file integrity, zone classification coverage, and quality gate definitions.

Usage:
    python scripts/validate_skill.py /path/to/skill-directory

Output: JSON with validation results and actionable suggestions.
"""

import json
import os
import re
import sys
from pathlib import Path


def validate_directory_structure(skill_path: Path) -> list[dict]:
    """Check that the skill directory follows the expected structure."""
    issues = []

    # Required: SKILL.md
    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        issues.append({
            "severity": "critical",
            "check": "directory_structure",
            "message": "Missing required SKILL.md file",
            "suggestion": "Create SKILL.md with YAML frontmatter and workflow instructions"
        })

    # Optional but expected directories
    expected_dirs = {
        "references": "Reference documentation loaded Just-in-Time",
        "scripts": "Deterministic execution scripts",
        "assets": "Templates, examples, and format specifications"
    }
    for dir_name, purpose in expected_dirs.items():
        dir_path = skill_path / dir_name
        if not dir_path.exists():
            issues.append({
                "severity": "info",
                "check": "directory_structure",
                "message": f"Optional directory '{dir_name}/' not found",
                "suggestion": f"Consider adding for {purpose}"
            })
        elif not any(dir_path.iterdir()):
            issues.append({
                "severity": "warning",
                "check": "directory_structure",
                "message": f"Directory '{dir_name}/' exists but is empty",
                "suggestion": "Add content or remove the empty directory"
            })

    return issues


def validate_frontmatter(skill_path: Path) -> list[dict]:
    """Validate YAML frontmatter in SKILL.md."""
    issues = []
    skill_md = skill_path / "SKILL.md"

    if not skill_md.exists():
        return issues

    content = skill_md.read_text()

    # Check frontmatter exists
    if not content.startswith("---"):
        issues.append({
            "severity": "critical",
            "check": "frontmatter",
            "message": "SKILL.md does not start with YAML frontmatter (---)",
            "suggestion": "Add YAML frontmatter with 'name' and 'description' fields"
        })
        return issues

    # Extract frontmatter
    parts = content.split("---", 2)
    if len(parts) < 3:
        issues.append({
            "severity": "critical",
            "check": "frontmatter",
            "message": "YAML frontmatter not properly closed (missing second ---)",
            "suggestion": "Ensure frontmatter is enclosed between two --- lines"
        })
        return issues

    frontmatter = parts[1]

    # Check required fields
    if "name:" not in frontmatter:
        issues.append({
            "severity": "critical",
            "check": "frontmatter",
            "message": "Missing 'name' field in frontmatter",
            "suggestion": "Add name: [skill-name-lowercase-hyphens]"
        })

    if "description:" not in frontmatter:
        issues.append({
            "severity": "critical",
            "check": "frontmatter",
            "message": "Missing 'description' field in frontmatter",
            "suggestion": "Add description with trigger phrases and negative triggers"
        })
    else:
        # Check description quality
        desc_match = re.search(r'description:\s*>?\s*\n(.*?)(?=\n\w|\n---)', frontmatter, re.DOTALL)
        if desc_match:
            desc = desc_match.group(1)
            if len(desc) < 50:
                issues.append({
                    "severity": "warning",
                    "check": "frontmatter",
                    "message": "Description is very short (< 50 chars)",
                    "suggestion": "Add trigger phrases and negative triggers for accurate activation"
                })
            if "do not" not in desc.lower() and "don't" not in desc.lower():
                issues.append({
                    "severity": "warning",
                    "check": "frontmatter",
                    "message": "Description lacks negative triggers",
                    "suggestion": "Add 'Do NOT use for...' to prevent false activations"
                })

    return issues


def validate_line_count(skill_path: Path) -> list[dict]:
    """Check that SKILL.md is within recommended limits."""
    issues = []
    skill_md = skill_path / "SKILL.md"

    if not skill_md.exists():
        return issues

    lines = skill_md.read_text().splitlines()
    line_count = len(lines)

    if line_count > 500:
        issues.append({
            "severity": "warning",
            "check": "line_count",
            "message": f"SKILL.md is {line_count} lines (recommended: <500)",
            "suggestion": "Move detailed content to references/ files with clear pointers"
        })
    elif line_count > 300:
        issues.append({
            "severity": "info",
            "check": "line_count",
            "message": f"SKILL.md is {line_count} lines (approaching 500 limit)",
            "suggestion": "Consider splitting if content grows further"
        })

    return issues


def validate_references(skill_path: Path) -> list[dict]:
    """Check that referenced files actually exist."""
    issues = []
    skill_md = skill_path / "SKILL.md"

    if not skill_md.exists():
        return issues

    content = skill_md.read_text()

    # Find references to files in references/, scripts/, assets/
    file_refs = re.findall(r'`(?:references|scripts|assets)/([^`]+)`', content)

    for ref in file_refs:
        for prefix in ["references", "scripts", "assets"]:
            ref_path = skill_path / prefix / ref
            if ref_path.exists():
                break
        else:
            # Check all three directories
            found = False
            for prefix in ["references", "scripts", "assets"]:
                if (skill_path / prefix / ref).exists():
                    found = True
                    break
            if not found:
                issues.append({
                    "severity": "warning",
                    "check": "reference_integrity",
                    "message": f"Referenced file not found: {ref}",
                    "suggestion": f"Create the file or fix the reference in SKILL.md"
                })

    return issues


def validate_zone_classification(skill_path: Path) -> list[dict]:
    """Check that step headers are classified by zone.

    Per-step zone classification typically lives in the sub-skill files, not
    in the master SKILL.md. Scan every top-level *.md in the skill directory
    so the check runs where classification actually matters.

    Accepts Deterministic, Reasoning, Judgment, Mixed, Automated, or Script
    as valid zone labels (Judgment is the documented third category in
    references/two-zone-architecture.md for per-workflow cases).
    """
    issues = []

    md_files = sorted(skill_path.glob("*.md"))
    if not md_files:
        return issues

    zone_keywords = [
        'deterministic', 'reasoning', 'judgment', 'mixed', 'automated', 'script'
    ]

    for md_file in md_files:
        content = md_file.read_text()
        steps = re.findall(r'###?\s+Step\s+[\d.]+[:\s]+(.+)', content)
        if not steps:
            continue

        unclassified = []
        for step in steps:
            step_lower = step.lower()
            if not any(kw in step_lower for kw in zone_keywords):
                unclassified.append(step.strip())

        if unclassified:
            issues.append({
                "severity": "info",
                "check": "zone_classification",
                "file": md_file.name,
                "message": (
                    f"{md_file.name}: {len(unclassified)} of {len(steps)} "
                    f"steps lack zone classification"
                ),
                "suggestion": (
                    "Label each step header as (Deterministic), (Reasoning), "
                    "(Judgment), or (Mixed) for clarity"
                ),
                "unclassified_steps": unclassified[:5],
            })

    return issues


def validate_quality_gates(skill_path: Path) -> list[dict]:
    """Check that quality gates are defined."""
    issues = []
    skill_md = skill_path / "SKILL.md"

    if not skill_md.exists():
        return issues

    content = skill_md.read_text().lower()

    if "quality gate" not in content and "qg1" not in content:
        issues.append({
            "severity": "warning",
            "check": "quality_gates",
            "message": "No quality gates found in SKILL.md",
            "suggestion": "Define quality gates between phases with pass criteria and failure routing"
        })

    if "feedback" not in content and "route back" not in content:
        issues.append({
            "severity": "warning",
            "check": "feedback_loops",
            "message": "No feedback loop mechanism found",
            "suggestion": "Add a feedback routing system so issues route to the correct upstream skill"
        })

    return issues


def validate_error_handling(skill_path: Path) -> list[dict]:
    """Check that error handling is defined."""
    issues = []
    skill_md = skill_path / "SKILL.md"

    if not skill_md.exists():
        return issues

    content = skill_md.read_text().lower()

    if "error" not in content and "failure" not in content:
        issues.append({
            "severity": "warning",
            "check": "error_handling",
            "message": "No error handling section found",
            "suggestion": "Add known failure modes, causes, and recovery actions"
        })

    return issues


def validate_required_sections(skill_path: Path) -> list[dict]:
    """Check that SKILL.md contains all recommended master sections."""
    issues = []
    skill_md = skill_path / "SKILL.md"

    if not skill_md.exists():
        return issues

    content = skill_md.read_text()

    recommended_sections = {
        "Quick Start": "Add a ## Quick Start section showing how to start, resume, and invoke individual skills",
        "Entry Point": "Add a ## Entry Point section naming the master controller skill",
        "Skill Inventory": "Add a ## Complete Skill Inventory or ## Skill Inventory section listing all sub-skills by phase",
        "Quality Gate": "Add a ## Quality Gates section with gate transitions and key checks",
        "State Persistence": "Add a ## State Persistence section referencing the JSON state schema",
    }

    for section, suggestion in recommended_sections.items():
        # Check for section heading (case-insensitive, flexible formatting)
        pattern = re.compile(rf'^##\s+.*{re.escape(section)}', re.MULTILINE | re.IGNORECASE)
        if not pattern.search(content):
            issues.append({
                "severity": "info",
                "check": "required_sections",
                "message": f"Recommended section not found: '{section}'",
                "suggestion": suggestion,
            })

    return issues


def validate_sub_skills(skill_path: Path) -> list[dict]:
    """Check sub-skill files if they exist."""
    issues = []

    md_files = list(skill_path.glob("*.md"))
    # Exclude SKILL.md itself
    sub_skills = [f for f in md_files if f.name != "SKILL.md"]

    for sub in sub_skills:
        content = sub.read_text()

        # Check for basic structure
        if "## Purpose" not in content and "## Inputs" not in content:
            issues.append({
                "severity": "info",
                "check": "sub_skill_structure",
                "message": f"Sub-skill '{sub.name}' may lack standard structure (Purpose, Inputs, Outputs)",
                "suggestion": "Use the sub-skill template from assets/sub-skill-template.md"
            })

    return issues


def count_files(skill_path: Path) -> dict:
    """Count files by type."""
    counts = {
        "skill_md": 1 if (skill_path / "SKILL.md").exists() else 0,
        "sub_skills": len([f for f in skill_path.glob("*.md") if f.name != "SKILL.md"]),
        "references": len(list((skill_path / "references").glob("*"))) if (skill_path / "references").exists() else 0,
        "scripts": len(list((skill_path / "scripts").glob("*"))) if (skill_path / "scripts").exists() else 0,
        "assets": len(list((skill_path / "assets").glob("*"))) if (skill_path / "assets").exists() else 0,
    }
    counts["total"] = sum(counts.values())
    return counts


def main():
    if len(sys.argv) < 2:
        print(json.dumps({
            "error": True,
            "message": "Usage: python validate_skill.py /path/to/skill-directory",
            "suggestion": "Provide the path to the skill directory to validate"
        }, indent=2))
        sys.exit(1)

    skill_path = Path(sys.argv[1]).resolve()

    if not skill_path.is_dir():
        print(json.dumps({
            "error": True,
            "message": f"Not a directory: {skill_path}",
            "suggestion": "Provide a path to a directory containing SKILL.md"
        }, indent=2))
        sys.exit(1)

    # Run all validations
    all_issues = []
    all_issues.extend(validate_directory_structure(skill_path))
    all_issues.extend(validate_frontmatter(skill_path))
    all_issues.extend(validate_line_count(skill_path))
    all_issues.extend(validate_references(skill_path))
    all_issues.extend(validate_zone_classification(skill_path))
    all_issues.extend(validate_quality_gates(skill_path))
    all_issues.extend(validate_error_handling(skill_path))
    all_issues.extend(validate_required_sections(skill_path))
    all_issues.extend(validate_sub_skills(skill_path))

    # Count issues by severity
    severity_counts = {"critical": 0, "warning": 0, "info": 0}
    for issue in all_issues:
        severity_counts[issue["severity"]] += 1

    # Determine overall status
    if severity_counts["critical"] > 0:
        overall = "FAIL"
    elif severity_counts["warning"] > 0:
        overall = "PASS_WITH_WARNINGS"
    else:
        overall = "PASS"

    result = {
        "error": False,
        "skill_path": str(skill_path),
        "skill_name": skill_path.name,
        "overall_status": overall,
        "file_counts": count_files(skill_path),
        "issue_counts": severity_counts,
        "issues": all_issues
    }

    print(json.dumps(result, indent=2))
    sys.exit(0 if overall != "FAIL" else 1)


if __name__ == "__main__":
    main()
