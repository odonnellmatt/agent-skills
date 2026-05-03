#!/usr/bin/env python3
"""Audit a skill's trigger description for collisions with other skills.

Semantic overlap between two skill descriptions is the failure mode the
main SKILL.md warns about most loudly: when two skills sound alike, the
selector's activation accuracy between them degrades sharply. This script
turns that warning into an automated check.

The audit uses lexical Jaccard similarity over content-bearing tokens
(lowercased alphanumerics, minus a small stopword list) as a dependency-
free proxy for semantic overlap. It is a first-pass filter, not a verdict:

    - A WARN verdict means "two or more descriptions share enough vocabulary
      that you should look at them."
    - A PASS verdict does NOT prove semantic distinctness — two descriptions
      can share zero content words and still collide semantically (e.g.,
      "summarize a paper" vs. "condense an article"). Always eyeball the
      top-N neighbours.

Usage:
    # Audit a skill against all others under ${CODEX_HOME:-~/.codex}/skills/
    python scripts/audit_trigger_collisions.py /path/to/new-skill

    # Use a different library root
    python scripts/audit_trigger_collisions.py /path/to/new-skill \
        --library ~/custom/skills

    # Tighten or loosen the overlap threshold (default 0.25)
    python scripts/audit_trigger_collisions.py /path/to/new-skill \
        --threshold 0.15

    # Increase how many nearest neighbours are always reported
    python scripts/audit_trigger_collisions.py /path/to/new-skill --top 20

Output: JSON to stdout. Exit code 0 on PASS, 2 on WARN, 1 on usage error.
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path

DEFAULT_LIBRARY = Path(os.environ.get("CODEX_HOME", str(Path.home() / ".codex"))) / "skills"

# Low-signal words stripped before comparison. Deliberately narrow — we
# want to keep rare, domain-specific terms since they carry most of the
# signal. Adding too many words here can hide real collisions.
STOPWORDS = {
    "a", "an", "and", "or", "but", "if", "then", "else", "the", "of", "in",
    "on", "at", "to", "for", "with", "by", "from", "as", "is", "are", "was",
    "were", "be", "been", "being", "this", "that", "these", "those", "it",
    "its", "use", "uses", "used", "using", "when", "whenever", "while",
    "user", "users", "wants", "want", "also", "triggers", "trigger", "do",
    "not", "skill", "skills", "via", "like", "such", "any", "all", "other",
    "new", "create", "creates", "creating", "build", "builds", "building",
    "please", "can", "will", "may", "should", "must", "you", "your", "so",
    "into", "over", "under", "only", "than", "then", "per", "one", "two",
    "three", "many", "some", "more", "most", "file", "files", "tool", "tools",
}


def extract_description(skill_md: Path) -> str:
    """Return the YAML `description:` field from a SKILL.md, or empty string."""
    try:
        content = skill_md.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""

    if not content.startswith("---"):
        return ""

    parts = content.split("---", 2)
    if len(parts) < 3:
        return ""

    frontmatter = parts[1]

    # Block form:  description: >
    #                multi
    #                line
    block = re.search(
        r'description:\s*>[^\n]*\n((?:[ \t]+[^\n]*\n?)+)',
        frontmatter,
    )
    if block:
        raw = block.group(1)
    else:
        # Inline form:  description: single line text
        inline = re.search(r'description:\s*(.+)', frontmatter)
        raw = inline.group(1) if inline else ""

    return re.sub(r"\s+", " ", raw).strip()


def extract_name(skill_md: Path) -> str:
    """Return the YAML `name:` field, or the parent directory name."""
    try:
        content = skill_md.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return skill_md.parent.name

    match = re.search(r'^name:\s*([^\n]+)$', content, re.MULTILINE)
    if match:
        return match.group(1).strip()
    return skill_md.parent.name


def tokenize(text: str) -> set[str]:
    """Extract content-bearing tokens. Lowercase alphanumerics, 3+ chars, minus stopwords."""
    lowered = text.lower()
    tokens = re.findall(r"[a-z][a-z0-9\-]{2,}", lowered)
    return {t for t in tokens if t not in STOPWORDS}


def jaccard(a: set[str], b: set[str]) -> float:
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Audit a skill's description for trigger collisions.",
    )
    parser.add_argument(
        "skill_path",
        help="Path to the skill directory being audited (must contain SKILL.md)",
    )
    parser.add_argument(
        "--library",
        default=str(DEFAULT_LIBRARY),
        help="Root directory containing other skills to compare against "
             "(default: ${CODEX_HOME:-~/.codex}/skills)",
    )
    parser.add_argument(
        "--threshold",
        type=float,
        default=0.25,
        help="Jaccard overlap above which a collision is flagged (default: 0.25)",
    )
    parser.add_argument(
        "--top",
        type=int,
        default=10,
        help="How many nearest neighbours to always report (default: 10)",
    )
    args = parser.parse_args()

    target_dir = Path(args.skill_path).expanduser().resolve()
    target_md = target_dir / "SKILL.md"

    if not target_md.exists():
        print(json.dumps({
            "error": True,
            "message": f"No SKILL.md found at {target_md}",
            "suggestion": "Pass a path to a directory that contains SKILL.md",
        }, indent=2))
        return 1

    target_desc = extract_description(target_md)
    target_name = extract_name(target_md)
    target_tokens = tokenize(target_desc)

    if not target_tokens:
        print(json.dumps({
            "error": True,
            "message": "Could not extract a usable description from the target SKILL.md",
            "suggestion": "Ensure SKILL.md has a 'description:' field in its YAML frontmatter",
        }, indent=2))
        return 1

    library_root = Path(args.library).expanduser().resolve()
    if not library_root.is_dir():
        print(json.dumps({
            "error": True,
            "message": f"Library root not found: {library_root}",
            "suggestion": "Pass --library to point at the skills directory",
        }, indent=2))
        return 1

    comparisons = []
    for other_md in library_root.rglob("SKILL.md"):
        try:
            if other_md.resolve() == target_md.resolve():
                continue
        except OSError:
            continue
        other_desc = extract_description(other_md)
        other_tokens = tokenize(other_desc)
        overlap = jaccard(target_tokens, other_tokens)
        if overlap == 0.0:
            continue
        shared = sorted(target_tokens & other_tokens)
        comparisons.append({
            "skill_name": extract_name(other_md),
            "skill_path": str(other_md.parent),
            "jaccard": round(overlap, 4),
            "shared_tokens": shared[:20],
        })

    comparisons.sort(key=lambda c: c["jaccard"], reverse=True)

    collisions = [c for c in comparisons if c["jaccard"] >= args.threshold]
    top_neighbours = comparisons[: args.top]

    if collisions:
        verdict = "WARN"
        message = (
            f"{len(collisions)} skill(s) exceed the collision threshold "
            f"({args.threshold}). Review the shared tokens and either tighten "
            f"the description, add negative triggers, or rename the skill."
        )
    else:
        verdict = "PASS"
        message = (
            f"No skills in {library_root} exceed the collision threshold "
            f"({args.threshold}). A PASS does not prove semantic distinctness — "
            f"spot-check the top_neighbours list for synonyms and paraphrase."
        )

    result = {
        "error": False,
        "target_skill": target_name,
        "target_path": str(target_dir),
        "target_tokens_sample": sorted(target_tokens)[:20],
        "library_root": str(library_root),
        "threshold": args.threshold,
        "verdict": verdict,
        "message": message,
        "collisions": collisions,
        "top_neighbours": top_neighbours,
    }

    print(json.dumps(result, indent=2))
    return 0 if verdict == "PASS" else 2


if __name__ == "__main__":
    sys.exit(main())
