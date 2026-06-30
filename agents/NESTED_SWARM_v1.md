# HS-131 — 🪆 THE NESTED SWARM — Sub-Agents That Spawn Sub-Agents (Bounded Depth)

---
skill_id: HS-131
hero_name: "THE NESTED SWARM"
emoji: "🪆"
version: v1.0.0
status: ACTIVE
category: agents
depends_on:
  - HS-008  # THE CONDUCTOR — BROski orchestrator drives delegation
  - HS-004  # THE FIVE WARDS — guardrails apply at every nesting level
provides:
  - recursive-delegation-pattern
  - depth-bounded-spawning
  - nested-budget-control
related:
  - HS-067  # THE THRONE LADDER — role hierarchy determines who may spawn
  - HS-006  # SOFT LANDING — fallback when a nested branch fails
  - HS-077  # CONSENT GUARDIAN — approval gates survive nesting
graph_notes: "Pattern for sub-agents spawning their own sub-agents (now supported up to 5 levels deep) with hard depth caps, per-level budgets, and guardrails inherited down the tree."
problem_keywords:
  - agents spawning forever
  - infinite spawn
  - runaway subagents
  - recursion limit
  - depth limit
  - too many agents
  - stop spawning
  - bounded delegation

---
**Category:** `agents/`
**Source:** Born-here — Claude Code changelog: subagents spawn subagents, 5 levels (2026-06)
**Version:** v1

---

## 🤔 What It Does

Sub-agents can now spawn their **own** sub-agents — up to 5 levels deep. That's
powerful and dangerous: unbounded recursion burns tokens and loses the plot. THE
NESTED SWARM is the discipline for recursive delegation: a hard depth cap, a budget
that *divides* as you descend, and guardrails (Five Wards, Consent Guardian) that
every level inherits — so depth buys parallelism, not chaos.

---

## 🎯 Purpose

- **Who uses it:** Orchestrators decomposing a task into sub-tasks that further decompose.
- **When to use it:** Big fan-out work (audits, multi-repo sweeps, research trees).
- **What it unlocks:** Controlled recursion without runaway spawning or budget blowout.

---

## 📥 Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `task` | `string` | ✅ | The work to decompose |
| `max_depth` | `int` | ✅ | Hard cap ≤ 5 |
| `token_budget` | `int` | ✅ | Total budget; split across children per level |

---

## 📤 Output Format

```json
{
  "depth": 2,
  "max_depth": 5,
  "spawned": ["explorer-a", "explorer-b"],
  "budget_remaining": 18000,
  "halted_reason": null
}
```

---

## 🔮 Prompt Block

```
You are THE NESTED SWARM coordinator. Decompose a task using recursive delegation.

Rules (enforce at EVERY level):
1. DEPTH CAP — never spawn beyond max_depth (hard ≤ 5). At the cap, do the work
   yourself or return; do not delegate.
2. BUDGET DIVIDES — each level gets a slice of the remaining budget; children share
   the parent's slice. When a branch's budget hits zero, stop and report partial.
3. GUARDRAILS INHERIT — Five Wards + Consent Guardian + role limits pass down to
   every child; a child can never exceed its parent's permissions.
4. FAN-OUT, NOT FORK-BOMB — only spawn children for genuinely independent sub-tasks;
   sequential steps stay in one agent.
5. REPORT UP — every level returns a structured result so the parent can synthesise
   (log → emit → return graceful).

Output the spawn tree, depth, budget remaining, and any halted_reason.
```

---

## 💡 Example Usage

```python
result = nested_swarm(
    task="Audit all 14 repos for outdated deps",
    max_depth=3,          # orchestrator → per-repo → per-manifest
    token_budget=60000,
)
# Level 0 spawns 14 repo agents; each may spawn manifest agents; depth stops at 3.
```

---

## 🚨 Anti-patterns

- **Don't spawn for sequential work** — recursion is for independent branches only.
- **Don't let budget stay constant down the tree** — it must divide, or you'll blow it.
- **Don't drop guardrails at depth** — a level-4 agent with root powers is how you get burned.

---

## 🔗 Related Skills

- [[HS-008]] THE CONDUCTOR — orchestrator that drives delegation
- [[HS-085]] THE FIVE WARDS — guardrails enforced at every level
- [[HS-071]] SOFT LANDING — graceful fallback for a failed branch
- [[HS-077]] CONSENT GUARDIAN — approval gates that survive nesting

---

## 📋 THE PROMPT

> Copy this block into any AI session to activate the skill:

```text
Use skill HS-131 [THE NESTED SWARM]. Coordinate recursive sub-agent delegation for my task with a hard depth cap (≤5), a budget that divides per level, and guardrails inherited down the tree. Output the spawn tree + budget remaining.
```
