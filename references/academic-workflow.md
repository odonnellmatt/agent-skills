# Domain Accelerator: Publication-Ready Academic Workflows

## Table of Contents

1. [Overview](#overview)
2. [Phase Architecture](#phase-architecture)
3. [Sub-Skill Inventory](#sub-skill-inventory)
4. [Quality Gate Definitions](#quality-gate-definitions)
5. [Reference Verification Protocol](#reference-verification-protocol)
6. [Academic Standards Enforcement](#academic-standards-enforcement)
7. [Output Format Options](#output-format-options)
8. [Common Failure Modes](#common-failure-modes)

---

## Overview

Academic writing skills produce publication-ready manuscripts that are rigorous, verified,
and editable. The workflow enforces methodological standards, citation integrity, and
structural compliance while keeping the final output human-editable (not locked PDFs).

**Recommended architecture:** Plan-and-Execute backbone with Evaluator-Optimizer loops
at each section and Parallel Fan-Out for literature search.

**Key constraint:** The output must be verifiable. Every claim must trace to a cited source.
Every calculation must be reproducible via script. Every formatting choice must comply
with stated standards.

---

## Phase Architecture

```
Phase 1: Research Planning (3 skills)
    ↓ QG1: Question structured, methodology justified, outline approved
Phase 2: Literature Discovery (4 skills)
    ↓ QG2: Search documented, ≥N sources identified, coverage verified
Phase 3: Analysis and Argumentation (3 skills)
    ↓ QG3: Methods appropriate, claims evidenced, counter-arguments addressed
Phase 4: Manuscript Drafting (5 skills)
    ↓ QG4: Sections reviewed by critic, internally consistent, word count met
Phase 5: Verification and Polish (4 skills)
    ↓ QG5: References verified, standards checked, rejection risk assessed
Phase 6: Output Generation (2 skills)
    ↓ QG6: Format correct, human final approval
```

---

## Sub-Skill Inventory

### Phase 1 — Research Planning

| # | Skill | Purpose | Zone |
|---|-------|---------|------|
| 1 | `research-question-formulator` | Structure question using PICO/CIMO/SPIDER | Reasoning |
| 2 | `methodology-selector` | Select and justify review type and analytical approach | Reasoning |
| 3 | `outline-generator` | Generate section-by-section outline with word targets | Reasoning |

### Phase 2 — Literature Discovery

| # | Skill | Purpose | Zone |
|---|-------|---------|------|
| 4 | `search-string-builder` | Construct Boolean strings for target databases | Mixed |
| 5 | `database-searcher` | Execute searches (parallel across sources) | Deterministic |
| 6 | `results-aggregator` | Merge, deduplicate, standardize results | Deterministic |
| 7 | `literature-synthesizer` | Thematic analysis of identified sources | Reasoning |

### Phase 3 — Analysis and Argumentation

| # | Skill | Purpose | Zone |
|---|-------|---------|------|
| 8 | `evidence-extractor` | Extract key findings, methods, data from sources | Mixed |
| 9 | `argument-builder` | Construct logical arguments from evidence | Reasoning |
| 10 | `counter-argument-mapper` | Identify and address opposing evidence/views | Reasoning |

### Phase 4 — Manuscript Drafting

| # | Skill | Purpose | Zone |
|---|-------|---------|------|
| 11 | `abstract-writer` | Draft structured abstract (background, methods, results, conclusion) | Reasoning |
| 12 | `introduction-writer` | Draft intro (context, gap, contribution, structure) | Reasoning |
| 13 | `methods-writer` | Draft methods (reproducible detail) | Mixed |
| 14 | `results-writer` | Draft results (findings, tables, figures) | Mixed |
| 15 | `discussion-writer` | Draft discussion (interpretation, implications, limitations) | Reasoning |

### Phase 5 — Verification and Polish

| # | Skill | Purpose | Zone |
|---|-------|---------|------|
| 16 | `reference-verifier` | Cross-check every citation against sources | Deterministic |
| 17 | `academic-standards-enforcer` | 12-point writing standards audit | Mixed |
| 18 | `consistency-checker` | Cross-section consistency (numbers, claims, terminology) | Deterministic |
| 19 | `rejection-risk-auditor` | Pre-submission quality assessment | Mixed |

### Phase 6 — Output Generation

| # | Skill | Purpose | Zone |
|---|-------|---------|------|
| 20 | `document-formatter` | Generate output in target format (docx/md/LaTeX) | Deterministic |
| 21 | `final-reviewer` | Present for human approval, log sign-off | Reasoning |

---

## Quality Gate Definitions

### QG1: Planning → Literature Discovery

**Automated:**
- [ ] Research question follows selected framework (all components defined)
- [ ] Methodology selection includes justification
- [ ] Outline contains all required sections with word targets

**Human Review:**
- [ ] Research question is novel and worth pursuing
- [ ] Methodology is appropriate for the research question
- [ ] Outline structure serves the argument

### QG2: Literature Discovery → Analysis

**Automated:**
- [ ] Search strings documented for each database
- [ ] ≥ configured minimum number of relevant sources identified
- [ ] Deduplication complete (no DOI duplicates)
- [ ] Source metadata complete (author, year, title, journal for all entries)

**Human Review:**
- [ ] Search coverage is adequate (no obvious gaps in databases)
- [ ] Source quality is acceptable (not dominated by grey literature)

### QG3: Analysis → Drafting

**Automated:**
- [ ] Evidence extracted from all included sources
- [ ] All claims in argument map link to specific source evidence
- [ ] No unsupported claims (evidence column not empty)

**Human Review:**
- [ ] Analytical approach is appropriate for the data
- [ ] Arguments are logically sound
- [ ] Counter-arguments are fairly represented

### QG4: Drafting → Verification

**Automated:**
- [ ] Word count within target range
- [ ] All required sections present
- [ ] All figures/tables referenced in text
- [ ] All in-text citations have reference list entries
- [ ] No orphan references

**Human Review:**
- [ ] Writing quality is publication-standard
- [ ] Arguments flow logically
- [ ] Tone is appropriate for target journal/audience

### QG5: Verification → Output

**Automated:**
- [ ] All references verified against source library
- [ ] 12-point academic standards checklist passed
- [ ] Cross-section consistency check passed
- [ ] Rejection risk score ≥ 85%

**Human Review:**
- [ ] Final read-through approval

### QG6: Output → Delivery

**Automated:**
- [ ] Output file generated successfully in requested format
- [ ] File opens correctly and formatting is intact

**Human Review:**
- [ ] Final sign-off for submission/sharing

---

## Reference Verification Protocol

Every citation must be deterministically verified:

```python
# reference_verifier.py — Deterministic script
for each in_text_citation:
    1. Find matching entry in reference library (by author+year)
    2. Verify: author names match exactly
    3. Verify: year matches
    4. Verify: title matches (fuzzy, threshold 90%)
    5. Verify: the claim made in-text is supported by the cited passage
    6. Flag any reference with confidence < 95%

Output:
{
    "total_citations": 87,
    "verified": 82,
    "flagged": 3,
    "missing": 2,
    "details": [
        {"citation": "Smith (2024)", "issue": "Year mismatch: source says 2023",
         "location": "Section 3, paragraph 2", "severity": "high"}
    ]
}
```

**Critical rule:** Do NOT auto-correct flagged references. Present them to the user.
A silently corrected reference may cite a work the author hasn't read.

---

## Academic Standards Enforcement

### The 12-Point Checklist (Deterministic Where Possible)

| # | Standard | Check Method |
|---|----------|-------------|
| 1 | No first-person (unless discipline allows) | Script: regex scan |
| 2 | All abbreviations defined at first use | Script: track first occurrence |
| 3 | All figures/tables referenced in text | Script: cross-reference |
| 4 | Consistent tense (past: methods/results, present: discussion) | LLM review |
| 5 | Hedged language for unproven claims | LLM review |
| 6 | No unsupported superlatives | Script: keyword scan |
| 7 | "Significant" used only statistically | LLM review |
| 8 | All equations numbered and referenced | Script: cross-reference |
| 9 | Ethical considerations addressed | LLM review |
| 10 | Limitations section is substantive | LLM review (word count + content) |
| 11 | Data availability statement present | Script: section check |
| 12 | Conflict of interest declaration present | Script: section check |

---

## Output Format Options

| Format | Use Case | Editable? |
|--------|----------|-----------|
| `.docx` (Word) | Journal submission, collaborative editing | Yes |
| `.md` (Markdown) | Version control, plain-text workflows | Yes |
| `.tex` (LaTeX) | Technical journals, complex formatting | Yes |
| `.txt` (Plain text) | Maximum portability | Yes |

All formats must preserve: headings, citations, tables, figure references.
The output is always editable — never produce locked or read-only formats.

---

## Common Failure Modes

| Failure | Cause | Prevention |
|---------|-------|------------|
| Fabricated citations | LLM invents plausible-sounding references | Reference verification script |
| Citation-claim mismatch | LLM attributes wrong finding to right source | Evidence-claim mapping check |
| Methodology drift | Methods section describes different approach than what was done | Cross-reference with Phase 1 decisions |
| Superficial limitations | "This study has limitations" without substance | Minimum word count + content evaluation |
| Inconsistent terminology | Same concept called different things across sections | Terminology glossary in state |
| Section contradictions | Results say X, discussion implies not-X | Cross-section consistency checker |
| Passive voice overuse | Academic ≠ unreadable | Style checker with threshold |
| Missing hedging | "X causes Y" when evidence only shows correlation | Claim-strength auditor |
