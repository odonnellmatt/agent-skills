# Domain Accelerator: Bibliometric & Scientometric Analysis Workflows

## Table of Contents

1. [Overview](#overview)
2. [Phase Architecture](#phase-architecture)
3. [Sub-Skill Inventory](#sub-skill-inventory)
4. [Quality Gate Definitions](#quality-gate-definitions)
5. [Data Source Selection](#data-source-selection)
6. [Analytical Techniques](#analytical-techniques)
7. [Visualization Requirements](#visualization-requirements)
8. [Reporting Standards](#reporting-standards)
9. [Common Failure Modes](#common-failure-modes)

---

## Overview

Bibliometric analysis uses quantitative techniques on metadata from scientific
publications to map the intellectual structure, social structure, and evolution
of a field. It answers questions like: *Who are the most influential authors?
What are the main thematic clusters? How has the field evolved?*

**Methodological references:** Donthu et al. (2021) *J Bus Res* on bibliometric
method selection; Aria & Cuccurullo (2017) on `bibliometrix` R package; van Eck &
Waltman on VOSviewer co-citation/co-occurrence mapping.

**Critical architectural principle:** Results are driven by metadata quality and
analytical choices. Document both exhaustively — different databases and different
normalization choices produce *different* field maps from the same topic.

**Recommended architecture:** Plan-and-Execute with a locked data snapshot and
parameter registry. All analyses run against a single frozen corpus.

---

## Phase Architecture

```
Phase 1: Scope and Protocol (3 skills)
    ↓ QG1: Field definition precise, database choice justified
Phase 2: Corpus Construction (4 skills)
    ↓ QG2: Corpus frozen, metadata quality validated, snapshot archived
Phase 3: Descriptive Analysis (3 skills)
    ↓ QG3: Performance metrics computed, outlier detection complete
Phase 4: Science Mapping (4 skills)
    ↓ QG4: Clustering parameters justified, stability checked
Phase 5: Interpretation and Reporting (3 skills)
    ↓ QG5: Every claim traces to a specific figure/table, limitations explicit
```

---

## Sub-Skill Inventory

### Phase 1 — Scope and Protocol

| # | Skill | Purpose | Zone |
|---|-------|---------|------|
| 1 | `field-definer` | Precisely define the field boundaries and research questions | Reasoning |
| 2 | `database-justifier` | Choose + justify Scopus / WoS / OpenAlex / Dimensions | Reasoning |
| 3 | `bibliometric-protocol-writer` | Protocol with query, filters, analysis plan, parameter choices | Reasoning |

### Phase 2 — Corpus Construction

| # | Skill | Purpose | Zone |
|---|-------|---------|------|
| 4 | `query-builder-bibliometric` | Construct database-specific queries with subject-area filters | Mixed |
| 5 | `metadata-harvester` | Export full records (authors, affiliations, refs, keywords) | Deterministic |
| 6 | `metadata-cleaner` | Deduplicate, disambiguate author names, normalize affiliations | Deterministic |
| 7 | `corpus-snapshot-archiver` | Freeze corpus with checksum + retrieval date | Deterministic |

### Phase 3 — Descriptive Analysis

| # | Skill | Purpose | Zone |
|---|-------|---------|------|
| 8 | `performance-analyzer` | Publications, citations, h-index by author/journal/country | Deterministic |
| 9 | `temporal-trends-analyzer` | Publication and citation trends over time | Deterministic |
| 10 | `productivity-laws-tester` | Lotka / Bradford / Zipf law fits with goodness-of-fit | Deterministic |

### Phase 4 — Science Mapping

| # | Skill | Purpose | Zone |
|---|-------|---------|------|
| 11 | `co-citation-mapper` | Co-citation network of cited references → intellectual base | Deterministic |
| 12 | `bibliographic-coupling-mapper` | Coupling network of source items → research fronts | Deterministic |
| 13 | `keyword-cooccurrence-mapper` | Author/index keyword co-occurrence → thematic clusters | Deterministic |
| 14 | `cluster-stability-checker` | Re-run clustering with varied parameters, report stability | Deterministic |

### Phase 5 — Interpretation and Reporting

| # | Skill | Purpose | Zone |
|---|-------|---------|------|
| 15 | `cluster-labeler` | Label clusters based on top terms and representative works | Reasoning |
| 16 | `field-narrative-builder` | Narrative of intellectual evolution, fronts, gaps | Reasoning |
| 17 | `bibliometric-reporter` | Manuscript structured for bibliometric reporting standards | Reasoning |

---

## Quality Gate Definitions

### QG1: Scope → Corpus

**Automated:**
- [ ] Field boundaries operationalized as a query string
- [ ] Database choice justified against ≥3 alternatives
- [ ] Research questions map to analytical techniques (table in protocol)
- [ ] Parameter choices pre-registered (clustering algorithm, thresholds)

**Human Review:**
- [ ] Field is genuinely bounded (not "everything about AI")

### QG2: Corpus → Descriptive

**Automated:**
- [ ] Corpus snapshot archived with checksum + retrieval date + query
- [ ] Deduplication complete (DOI + title+authors fuzzy match)
- [ ] Author disambiguation applied (OpenAlex ORCID, WoS DAIS, etc.)
- [ ] Missing metadata rates documented per field
- [ ] No records without year, authors, or title in included set

**Human Review:**
- [ ] Coverage matches the field's intellectual reach
- [ ] Non-English work appropriately represented (or exclusion justified)

### QG3: Descriptive → Mapping

**Automated:**
- [ ] All descriptive metrics computed by script from frozen corpus
- [ ] Outliers (e.g., mega-cited references) identified and flagged
- [ ] Temporal plots generated with consistent window choices

**Human Review:**
- [ ] Performance rankings look plausible to a domain expert

### QG4: Mapping → Interpretation

**Automated:**
- [ ] Network construction parameters documented (threshold, normalization)
- [ ] Clustering algorithm + resolution parameter recorded
- [ ] Stability check: clustering re-run with ≥2 parameter variations
- [ ] Network statistics reported (nodes, edges, density, modularity)

**Human Review:**
- [ ] Unstable clusters flagged and excluded from interpretation

### QG5: Interpretation → Delivery

**Automated:**
- [ ] Every narrative claim cites a figure, table, or cluster ID
- [ ] Limitations section addresses: database coverage, author disambiguation, language bias, lag effects
- [ ] Reproducibility package: query + snapshot + scripts + parameter file

**Human Review:**
- [ ] Cluster labels match domain understanding
- [ ] Narrative distinguishes intellectual base (co-cit) from research front (coupling)

---

## Data Source Selection

| Database | Strengths | Limitations |
|----------|-----------|-------------|
| Scopus | Broad disciplinary coverage, author disambiguation | Subscription; SSH under-represented |
| Web of Science (WoS) | Curated core collection, oldest continuous | Subscription; selective journal inclusion |
| OpenAlex | Free, 250M+ works, concept tagging | Metadata quality uneven per source |
| Dimensions | Grants, patents, clinical trials links | Subscription for full features |
| Google Scholar | Highest recall incl. grey literature | No bulk export, weak metadata, no deduplication |
| PubMed / MEDLINE | Biomedical depth | Biomedical-only |
| Lens.org | Patents + scholarly, free | Newer, coverage still growing |

**Single-database vs multi-database:** Multi-database improves coverage but
complicates deduplication and normalization. State the tradeoff explicitly.

---

## Analytical Techniques

| Technique | Answers | Output |
|-----------|---------|--------|
| Performance analysis | Who/what is influential? | Ranked tables |
| Citation analysis | What gets cited? | Most-cited works |
| Co-citation analysis | What intellectual traditions exist? | Cluster map of cited works |
| Bibliographic coupling | What are current research fronts? | Cluster map of source works |
| Co-authorship | Who collaborates? | Author / country / institution networks |
| Keyword co-occurrence | What themes exist? | Term clusters |
| Topic modeling (LDA, BERTopic) | What latent topics exist? | Topic distributions |
| Burst detection (Kleinberg) | What topics surged when? | Time-stamped term bursts |

**Critical rule:** The LLM never runs clustering or computes network metrics —
scripts using `bibliometrix`, `networkx`, `igraph`, or VOSviewer do. The LLM
interprets labeled outputs.

---

## Visualization Requirements

| Visualization | Purpose | Tooling |
|---------------|---------|---------|
| Network map | Co-citation / coupling / co-occurrence clusters | VOSviewer, Gephi, CiteSpace |
| Thematic map | Centrality × density quadrants | bibliometrix |
| Three-field plot | Authors × keywords × journals flows | bibliometrix |
| Historiograph | Citation lineage over time | HistCite, CiteSpace |
| Temporal overlay | Cluster evolution across time slices | VOSviewer overlay view |

Every figure caption must state: data source, date retrieved, corpus size after
filtering, method, threshold, clustering resolution.

---

## Reporting Standards

- Donthu et al. (2021) checklist for methodological transparency
- Aria & Cuccurullo (2017) — recommend `bibliometrix` script provenance
- Reproducibility package mandatory: query string, retrieval date, snapshot
  checksum, scripts, parameter files

---

## Common Failure Modes

| Failure | Cause | Prevention |
|---------|-------|------------|
| Different database → different field | Single database without acknowledgment | QG2 forces coverage discussion |
| Author disambiguation errors | Same author spelled differently | ORCID / DAIS matching enforced |
| Unstable clusters interpreted confidently | Clustering algorithm stochasticity | Stability check required at QG4 |
| Correlation→causation narrative | Citation patterns framed as influence | Reasoning zone restricted to describe/interpret |
| Predatory journal inclusion | No journal quality filter | Document inclusion criteria; justify or exclude |
| Missing self-citation check | Prolific authors dominate naturally | Optional self-citation filter documented |
| Temporal lag mistaken for decline | Recent work has fewer citations by construction | Normalization (per-year citations) or exclusion of recent N years |
| Keyword analysis dominated by method terms | Uncontrolled vocabulary mixing concepts + methods | Keyword curation step with exclusion list |
| Claims about individual researchers | H-index / single-author focus without context | Ethical and context hedging required |
| Overinterpreting weak clusters | Small clusters with < 5 items labeled | Minimum cluster size parameter enforced |
