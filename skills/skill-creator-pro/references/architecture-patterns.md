# Architecture Patterns for Complex Skills

## Table of Contents

1. [Pattern Selection Decision Matrix](#pattern-selection-decision-matrix)
2. [Plan-and-Execute](#plan-and-execute)
3. [Parallel Fan-Out](#parallel-fan-out)
4. [Supervisor/Worker](#supervisorworker)
5. [Evaluator-Optimizer](#evaluator-optimizer)
6. [ReAct](#react)
7. [Blackboard System](#blackboard-system)
8. [Event-Driven](#event-driven)
9. [Hybrid Compositions](#hybrid-compositions)
10. [The Reliability Compounding Problem](#the-reliability-compounding-problem)
11. [Single-Agent with Skills vs Multi-Agent](#single-agent-vs-multi-agent)

---

## Pattern Selection Decision Matrix

| Requirement | Recommended Pattern |
|-------------|-------------------|
| Structured, predictable multi-step workflow | Plan-and-Execute |
| Independent sub-tasks needing speed | Parallel Fan-Out |
| Multiple distinct expert domains | Supervisor/Worker |
| Iterative refinement to quality bar | Evaluator-Optimizer |
| Exploratory, solution path unknown | ReAct |
| Massive heterogeneous data environments | Blackboard |
| Scalable, fault-tolerant microservices | Event-Driven |
| Publication-ready academic writing | Plan-and-Execute + Evaluator-Optimizer |
| Repeatable analytical pipeline | Plan-and-Execute + Parallel Fan-Out |

---

## Plan-and-Execute

**How it works:** A Planner agent generates a comprehensive step-by-step roadmap upfront.
An Executor agent sequentially carries out each step. This decouples strategy from execution.

**Reliability:** Benchmarked at ~92% success rate vs ReAct's ~85% on complex tasks. The plan
itself is a reviewable artifact that humans can inspect before irreversible actions.

**When it fails:** If the environment changes mid-execution or an initial assumption was wrong.
Mitigate with explicit re-planning loops at each quality gate.

**Implementation pattern:**
```
Planner Agent → Generate step-by-step plan
                     ↓
Human Review → Approve/modify plan
                     ↓
Executor Agent → Execute step 1 → Gate check → Execute step 2 → ...
                     ↓ (if gate fails)
Re-planner → Adjust remaining steps based on what was learned
```

**Best for complex skills because:** It produces an explicit, auditable plan that serves as
both the execution guide and the documentation of methodology. This is critical for
reproducibility in academic and analytical workflows.

---

## Parallel Fan-Out

**How it works:** An orchestrator identifies independent sub-tasks and dispatches them to
specialized agents simultaneously. A synthesizer agent merges results.

**When to use:** Time-sensitive analysis, multi-domain research, any task where sub-components
don't depend on each other.

**Implementation pattern:**
```
Orchestrator → Identify independent sub-tasks
                     ↓
    ┌────────────────┼────────────────┐
    ↓                ↓                ↓
Agent A          Agent B          Agent C
(Domain 1)       (Domain 2)       (Domain 3)
    ↓                ↓                ↓
    └────────────────┼────────────────┘
                     ↓
              Synthesizer Agent → Merged output
```

**Conflict resolution:** When parallel agents return conflicting results, the synthesizer
must flag the conflict for human review rather than silently choosing one interpretation.

---

## Supervisor/Worker

**How it works:** A central supervisor receives tasks, decomposes them, routes to specialized
workers, and aggregates outputs. Workers only see their assigned sub-task.

**Trade-offs:** Strong context isolation (workers only see what they need), but back-and-forth
routing adds latency and token costs. Best when domain expertise genuinely requires
specialized agent configurations.

**Context isolation benefit:** Each worker operates with a clean context window focused
entirely on its specialty, preventing cross-contamination of domain-specific reasoning.

---

## Evaluator-Optimizer

**How it works:** A generator produces output. A separate evaluator scores it against a
rubric. If below threshold, the evaluator sends specific feedback to the generator for
revision. The cycle repeats until the quality bar is met or max iterations reached.

**Critical parameters:**
- Maximum iteration limit (typically 3) — diminishing returns after this
- Quality threshold — must be explicit and measurable
- Escalation protocol — what happens when max iterations are exhausted

**Implementation:**
```
Generator → Draft output
                ↓
Evaluator → Score against rubric (7 dimensions, 25 sub-dimensions)
                ↓
          Passes threshold? ──YES──→ Proceed to next phase
                ↓ NO
          Specific feedback with line references
                ↓
          Return to Generator (iteration N+1)
                ↓
          Max iterations? ──YES──→ Escalate to human review
```

---

## ReAct

**How it works:** Iterative Thought → Action → Observation loop. The agent reasons about
the current state, selects a tool, executes it, observes the result, and repeats.

**Best for:** Exploratory tasks, troubleshooting, when the solution path is unknown.

**Failure modes:** Susceptible to looping and drifting. Must implement:
- Maximum iteration limits
- No-progress detection (stuck doing the same action repeatedly)
- Token budgets (hard ceiling on total consumption)
- Goal re-anchoring (re-read the original objective every N steps)

**Caution for complex skills:** ReAct alone is insufficient for structured workflows.
Use it within specific sub-skills where exploration is genuinely needed, not as the
backbone of the overall pipeline.

---

## Blackboard System

**How it works:** A main agent posts requests to a shared knowledge base (the
"blackboard"). Specialized helper agents or workers independently monitor the
board and volunteer solutions if they have relevant expertise. No centralized
routing is needed.

**When to use:** Massive, heterogeneous environments (data lakes, multi-source research)
where the orchestrator cannot know every agent's capabilities upfront.

**Reliability data:** Improves end-to-end task success rates in complex data discovery
by up to 57% compared to traditional hierarchical routing.

---

## Event-Driven

**How it works:** Agents communicate through a message broker (e.g., Kafka) instead of
direct API calls. Each agent listens to specific event topics, processes data, and
emits output events.

**Benefits:** Asynchronous, scalable, fault-tolerant. Agents can be added, removed, or
restarted without breaking the system.

**When to use:** Enterprise-scale systems requiring high availability and independent
scaling of components.

---

## Hybrid Compositions

Most complex skills combine patterns:

### Academic Writing (Recommended)
```
Plan-and-Execute (backbone)
  + Parallel Fan-Out (literature search across databases)
  + Evaluator-Optimizer (section-by-section quality review)
  + Supervisor/Worker (specialized agents for search, writing, review)
```

### Analytical Pipeline (Recommended)
```
Plan-and-Execute (backbone)
  + Parallel Fan-Out (multi-domain analysis)
  + Evaluator-Optimizer (data quality verification)
```

### Research and Synthesis (Recommended)
```
Supervisor/Worker (orchestrate specialists)
  + Parallel Fan-Out (concurrent data gathering)
  + Evaluator-Optimizer (synthesis quality loops)
```

---

## The Reliability Compounding Problem

Agent workflows are sequential chains of non-deterministic LLM calls.
Failure rates multiply at every step.

| Per-Step Reliability | 4 Steps | 8 Steps | 12 Steps | 20 Steps |
|---------------------|---------|---------|----------|----------|
| 99% | 96.1% | 92.3% | 88.6% | 81.8% |
| 95% | 81.5% | 66.3% | 54.0% | 35.8% |
| 90% | 65.6% | 43.0% | 28.2% | 12.2% |

**To maintain >90% end-to-end across 12 steps, each step needs >99.1% reliability.**

Achieve this through:
1. Deterministic locking (remove LLM from steps that don't need reasoning)
2. Verification gates (catch failures between steps)
3. Retry with exponential backoff (recover from transient errors)
4. Fallback chains (alternative execution paths)
5. Circuit breakers (prevent cascading failures)

---

## Single-Agent vs Multi-Agent

### When Single-Agent with Skills Is Sufficient

Single-agent with skills (SAS) can replace multi-agent systems when:
- The workflow is serializable (sequential, no information loss)
- Agents share common history without hidden private states
- They rely on a homogeneous underlying model

**Efficiency gains:** 54% token reduction, 50% latency reduction vs multi-agent.

### When Multi-Agent Is Required

- Tasks requiring parallel sampling
- Hidden private information between roles
- Adversarial debate (proponent vs. opponent)
- More than 50-100 skills (cognitive scaling limit / phase transition)

### The Cognitive Scaling Limit

As the skill library grows, LLM skill-selection accuracy degrades non-linearly.
Accuracy remains stable up to ~50-100 skills, then drops precipitously.

**Mitigation:** Hierarchical routing — group skills into broad categories, breaking
selection into coarse-to-fine sub-decisions.

---

## Related References

- `two-zone-architecture.md` — Classify each pattern component as Deterministic or Reasoning
- `quality-gates.md` — Gate design for phase transitions within each pattern
- `resilience-patterns.md` — Error handling and retry strategies for pattern execution
- `memory-management.md` — State persistence across pattern steps and sessions
