# Resilience Patterns

## Table of Contents

1. [The Resilience Triad](#the-resilience-triad)
2. [Retry Patterns](#retry-patterns)
3. [Fallback Chains](#fallback-chains)
4. [Circuit Breakers](#circuit-breakers)
5. [Error Handling Design](#error-handling-design)
6. [Idempotency Requirements](#idempotency-requirements)
7. [Failure Mode Catalog](#failure-mode-catalog)

---

## The Resilience Triad

Every complex skill must implement three defensive layers:

```
Request → [Retry Logic] → [Fallback Chain] → [Circuit Breaker] → Response
              ↓                   ↓                   ↓
         Transient errors    Complete failures    Extended outages
         (retry same path)   (try alternative)    (block, protect system)
```

---

## Retry Patterns

### Exponential Backoff with Jitter

```
Attempt 1: immediate
Attempt 2: wait base * 2^1 + random(0, base)  → ~2-4 seconds
Attempt 3: wait base * 2^2 + random(0, base)  → ~4-8 seconds
Attempt 4: STOP — escalate to fallback
```

Jitter prevents thundering herd (all retries hitting at the same time).

### Idempotency-Aware Retries

**Safe to retry (idempotent):**
- Reading data from APIs or databases
- Running calculation scripts
- Validation checks
- Search queries

**NOT safe to retry without safeguards:**
- Sending emails or messages
- Creating database records
- Financial transactions
- Publishing content
- Any operation with side effects

For non-idempotent operations, implement one of:
1. **Idempotency keys** — unique request IDs that prevent duplicate processing
2. **Check-before-retry** — verify the operation hasn't already completed
3. **Two-phase commit** — separate "prepare" from "commit"

### Implementation in SKILL.md

```markdown
## Error Recovery: API Call Failure

If the data retrieval script fails:
1. Check the error type from the script's JSON output
2. If `error_type` is "rate_limit" or "timeout":
   - Wait 5 seconds, retry once
   - If retry fails, wait 30 seconds, retry once more
   - If still failing, report to user with the error details
3. If `error_type` is "authentication":
   - Do NOT retry — report to user immediately
4. If `error_type` is "data_not_found":
   - Do NOT retry — log as expected empty result and continue
```

---

## Fallback Chains

When the primary path fails completely:

```
Primary: Current reasoning model for complex synthesis
    ↓ fails (timeout, rate limit)
Fallback 1: Smaller fallback reasoning model
    ↓ fails
Fallback 2: Cached/template response from previous successful run
    ↓ not available
Fallback 3: Graceful degradation message to user
    "Unable to complete synthesis. Data has been collected and saved to
     [path]. You can re-run when the service recovers, or manually review
     the raw data at [path]."
```

### Fallback Design Principles

1. **Each fallback must be independent** — Don't share failure modes
2. **Preserve progress** — Never lose completed work when falling back
3. **Be transparent** — Tell the user which fallback was used and why
4. **Log everything** — Record which fallback activated for post-mortem

### Implementation in SKILL.md

```markdown
## Fallback Strategy

### For LLM reasoning steps:
- Primary: Use current model with full context
- Fallback: Use current model with reduced context (summary only)
- Last resort: Skip reasoning, present raw data with note to user

### For external API calls:
- Primary: Live API call
- Fallback: Cached data from last successful call (with staleness warning)
- Last resort: Report unavailability, suggest manual lookup

### For script execution:
- Primary: Run script normally
- Fallback: Run with --safe-mode flag (reduced functionality)
- Last resort: Report script failure with full error output
```

---

## Circuit Breakers

Prevent cascading failures when a dependency is down:

```
CLOSED (normal)
    ↓ failure threshold crossed (e.g., 5 failures in 60 seconds)
OPEN (blocking)
    ↓ cooldown period (e.g., 30 seconds)
HALF-OPEN (probing)
    ↓ probe succeeds → CLOSED
    ↓ probe fails → OPEN (reset cooldown)
```

### When to Use Circuit Breakers in Skills

- Skills that call external APIs (search databases, data providers)
- Skills that depend on other running services (LightRAG, MCP servers)
- Multi-step workflows where one failing dependency would waste tokens on doomed steps

### Implementation

```markdown
## External API Health Check

Before executing the database search step:
1. Run a lightweight health check: `python scripts/health_check.py --service [NAME]`
2. If health check fails:
   - Log the failure with timestamp
   - Check if this is the 3rd+ consecutive failure
   - If yes: skip this data source, note it as unavailable, continue with others
   - If no: retry after 10 seconds
3. If health check succeeds: proceed normally
```

---

## Error Handling Design

### Script Error Output Standard

All scripts in the skill must return structured errors:

```json
{
  "error": true,
  "error_type": "validation_error | rate_limit | timeout | auth_error | data_not_found | script_error",
  "message": "Human-readable description of what went wrong",
  "context": {
    "step": "data_retrieval",
    "input_file": "data/query.json",
    "line_number": 42
  },
  "suggestion": "Actionable suggestion for recovery",
  "recoverable": true,
  "retry_after_seconds": null
}
```

### Error Classification Table

| Error Type | Retry? | Fallback? | User Alert? |
|-----------|--------|-----------|-------------|
| `rate_limit` | Yes (with backoff) | If retries exhausted | Only if all retries fail |
| `timeout` | Yes (once) | If retry fails | Only if fallback fails |
| `auth_error` | No | No | Immediately |
| `validation_error` | No (fix input) | No | With suggestion |
| `data_not_found` | No | Use cached data | If no cache available |
| `script_error` | No | No | Immediately with full output |

### Error Handling Section in Sub-Skills

```markdown
## Error Handling

### Known Failure Modes

| Error | Cause | Recovery |
|-------|-------|----------|
| `API_RATE_LIMIT` | Too many requests | Wait `retry_after_seconds`, retry once |
| `SOURCE_NOT_FOUND` | Broken URL | Log warning, skip source, continue |
| `VALIDATION_FAIL` | Data doesn't match schema | Report specific field failures |
| `THRESHOLD_NOT_MET` | Quality below minimum | Route to upstream skill with feedback |

### Escalation Protocol
If an error persists after recovery attempts:
1. Save all progress to state file
2. Present the user with:
   - What failed and why (from error JSON)
   - What was attempted to recover
   - Options: retry, skip and continue, manual intervention, abort
3. Wait for user decision before proceeding
```

---

## Idempotency Requirements

### Why Idempotency Matters

Because LLMs are non-deterministic, agent workflows will inevitably fail and require
retries. If your scripts have side effects, retrying can cause:
- Duplicate database entries
- Double-sent emails
- Repeated API charges
- Corrupted state files

### Idempotency Checklist for Scripts

- [ ] Running the script twice with same input produces same output
- [ ] No database writes (or writes are upserts with unique keys)
- [ ] No message sending (or messages are deduplicated)
- [ ] No file creation without existence checks
- [ ] State file updates are atomic (write to temp, then rename)
- [ ] No reliance on system time for deterministic outputs (accept timestamp param)

---

## Failure Mode Catalog

### Infrastructure Failures

| Failure | Impact | Mitigation |
|---------|--------|------------|
| API timeout | Step hangs | Timeout limits, retry with backoff |
| API rate limit | Step blocked | Exponential backoff, queue management |
| Service outage | Dependency unavailable | Circuit breaker, fallback chain |
| Network partition | Cannot reach external services | Cached data, graceful degradation |
| Disk full | Cannot write output | Check disk space before long operations |

### Logic Failures

| Failure | Impact | Mitigation |
|---------|--------|------------|
| Infinite loop | Agent stuck | Max iteration limits, progress detection |
| Context drift | Agent forgets objective | Re-anchor to plan every N steps |
| Hallucinated data | False information in output | Verification gates, source cross-checks |
| Wrong tool selection | Incorrect script executed | Clear tool descriptions, semantic routing |
| State corruption | Workflow cannot resume | Atomic state writes, backup before update |

### Quality Failures

| Failure | Impact | Mitigation |
|---------|--------|------------|
| Below-threshold output | Gate blocks progress | Evaluator-optimizer loop (max 3 cycles) |
| Inconsistent output | Sections contradict each other | Cross-section consistency checker |
| Missing coverage | Key topics not addressed | Coverage checklist at quality gate |
| Style violations | Unpublishable formatting | Deterministic style checker script |

---

## Related References

- `two-zone-architecture.md` — Script idempotency requirements for Deterministic Zone
- `quality-gates.md` — Gate failures trigger resilience patterns (retry, fallback, reroute)
- `memory-management.md` — State persistence enables recovery after failures
- `architecture-patterns.md` — Pattern-specific failure modes and recovery strategies
