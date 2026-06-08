# HS-121 — 🔄 SELF IMPROVEMENT 5-LOOP — Self-Improvement 5-Loop Logic
**Category:** agents
**Version:** 1.0


---
skill_id: HS-121
hero_name: "LOOP FORGE"
emoji: "🔄"
version: v1.0
category: agents
depends_on:
  - HS-043  # LOOP MASTER — this code implements the 5-loop reference
  - HS-003  # AGENT_LIFECYCLE_STATE_MACHINE — loop fires within the lifecycle
provides:
  - self-improvement-code
  - loop-implementation
  - autonomous-metric-check
  - observation-store-pattern
related:
  - HS-040  # GOALKEEPER — goalkeeper uses this loop implementation
  - HS-093  # NIGHT TENDER — nightly scheduler runs this loop
graph_notes: "Python code companion to HS-043 LOOP MASTER — implement all 5 loops in any agent background task runner."
---
## What it Does
The universal 5-step self-improvement loop used by all learning agents in the HyperFocus ecosystem. Every agent that improves over time uses this pattern.

## When To Use
- Building any agent with learning/adaptation capability
- Adding self-improvement to an existing agent
- Reviewing why an agent isn’t improving as expected

## THE LOOP
```
SELF-IMPROVEMENT 5-LOOP:

Loop 1 — OBSERVE
  → Collect raw outcome data from last N runs
  → No filtering, no judgment — just facts
  → Store in: observations table / Redis stream

Loop 2 — ANALYSE
  → Pattern match: what failed? what succeeded?
  → Group by: task_type, time_of_day, complexity
  → Output: insight_report (JSON)

Loop 3 — HYPOTHESISE
  → Generate 1-3 improvement hypotheses
  → Each hypothesis: {problem, proposed_change, expected_gain}
  → Rank by expected_gain DESC

Loop 4 — EXPERIMENT
  → Apply top hypothesis to next N runs (shadow mode first)
  → Shadow = run both old + new, compare outputs
  → Only promote if delta > threshold

Loop 5 — VALIDATE + COMMIT
  → Measure actual gain vs expected
  → If gain confirmed → commit change to agent config
  → If not → log, discard hypothesis, back to Loop 1

SACRED RULES:
  - NEVER promote in Loop 4 without shadow testing
  - NEVER skip human review for changes that affect user output
  - Consent Guardian (HS-077) applies to any user-facing change
  - All loop outputs logged to governance ledger (HS-095)

CYCLE CADENCE:
  - Lightweight agents: every 24h (NIGHT TENDER pattern HS-093)
  - Heavy agents: every 7d sprint
  - Trigger on: error_rate > 5% OR performance drop > 10%
```

## Related Skills
- HS-040 GOALKEEPER Self-Improving Agent
- HS-093 NIGHT TENDER Nightly Learning Loop
- HS-095 THE LEDGER LAW Governance Ledger

---
*Source: HyperCode-V2.4 | Category: agents/*
