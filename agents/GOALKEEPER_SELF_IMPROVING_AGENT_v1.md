# HS-040 — 🦅 GOALKEEPER — GoalKeeper Self-Improving Agent Setup
**Category:** agents
**Version:** 1.0

> *"An agent that tracks its own goals, measures its own progress, and improves itself."*

---

## 🎯 What It Does
Sets up the GoalKeeper agent pattern — a self-improving agent that maintains goal state, measures progress against KPIs, and triggers improvement loops automatically.

## 🌍 Why It Exists
Most agents are reactive. GoalKeeper is proactive — it knows what "done" looks like and pushes toward it without being asked.

## ⚙️ How To Use
1. Paste when building or configuring the goal_keeper agent
2. Fill in `[GOAL]` and `[KPI_METRICS]`
3. Deploy as a standalone container in the agent swarm

---

## 📋 THE PROMPT

```
Set up a GoalKeeper self-improving agent with:

GOAL: [GOAL — e.g. "Keep course completion rate above 80%"]
KPI METRICS: [KPI_METRICS — e.g. "completion_rate, active_students, drop_off_point"]

AGENT BEHAVIOUR:
1. MEASURE — Query metrics every [INTERVAL] (default: 1 hour)
2. COMPARE — Actual vs target KPI
3. GAP DETECT — If gap > threshold, trigger improvement action
4. IMPROVE — Run improvement action from action registry
5. LOG — Record result to goal_keeper_log table
6. REPEAT — Back to step 1

IMPROVEMENT ACTIONS (register what this agent can do):
- alert_lyndz(message) — DM via Discord bot
- trigger_catch_stragglers() — activate student re-engagement
- adjust_difficulty(module_id, direction) — up/down
- flag_for_review(metric, value) — human decision needed

SELF-IMPROVEMENT RULE:
Agent may SUGGEST changes to its own action registry.
Agent may NEVER modify its own goal or KPI thresholds without human approval.

Output: FastAPI endpoint at /goal-keeper/status + /goal-keeper/trigger
```

---

## 🔗 Related Skills
- HS-041 — MetricsEngine Integration
- HS-043 — Self-Improvement 5-Loop Logic
- HS-044 — A/B Testing Framework

---
*HYPER-SKILLs Vault — welshDog 🐕🏴󠁧󠁢󠁷󠁬󠁳󠁧⚡*
