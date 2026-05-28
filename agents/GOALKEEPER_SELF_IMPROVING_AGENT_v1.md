# HS-040 — 🦅 GOALKEEPER — GoalKeeper Self-Improving Agent Setup

## What it Does
Blueprint for the GoalKeeper agent — a self-improving goal-tracking agent that monitors progress, adjusts targets, and feeds results back into the system loop.

## When To Use
- Building goal-tracking agents for any project
- Wiring up self-improvement feedback loops
- Setting up automated sprint reviews

## THE PROMPT
```
Build a GoalKeeper self-improving agent with:

CORE RESPONSIBILITIES:
  - Track active goals with status: ACTIVE / ACHIEVED / MISSED / DEFERRED
  - Score each goal 0-100 on completion
  - Emit goal events to the metrics stream
  - Feed miss-data back as learning input

SELF-IMPROVEMENT LOOP:
  1. OBSERVE → collect goal outcomes
  2. ANALYSE → find patterns in misses
  3. ADJUST → revise goal difficulty or cadence
  4. PROPOSE → suggest next sprint goals based on trend
  5. WAIT → human approves / rejects proposals

FASTAPI ENDPOINTS:
  GET  /goals           → list all active goals
  POST /goals           → create goal
  PUT  /goals/{id}      → update status/score
  GET  /goals/trends    → pattern analysis
  POST /goals/propose   → AI-proposed next goals

DATA MODEL:
  goal_id, title, target_date, status,
  score (0-100), miss_reason, created_at

SACRED RULES:
  - NEVER auto-accept AI proposals (human approves)
  - Consent Guardian pattern applies (HS-077)
  - Feed all outcomes to MetricsEngine (HS-041)
```

## Related Skills
- HS-041 METRICS ENGINE Integration
- HS-043 Self-Improvement 5-Loop Logic
- HS-077 CONSENT GUARDIAN

---
*Source: HyperCode-V2.4 agents/goal_keeper/ | Category: agents/*
