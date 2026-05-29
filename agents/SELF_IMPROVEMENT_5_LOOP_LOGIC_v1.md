# HS-043 — 🔄 LOOP MASTER — Self-Improvement 5-Loop Logic
**Category:** agents
**Version:** 1.0

> *"The agent doesn't wait to be told to improve. It runs this loop on its own."*

---

## 🎯 What It Does
The 5-loop self-improvement pattern used across HyperFocus agents. Gives any agent the ability to measure its own performance, identify gaps, and trigger improvement actions autonomously.

## 🌍 Why It Exists
Stateless agents plateau. Looping agents compound. This pattern is what makes the difference between a tool and an autonomous system.

## ⚙️ How To Use
1. Paste when implementing autonomous improvement logic in any agent
2. Define `[METRIC]`, `[THRESHOLD]`, and `[IMPROVE_ACTION]`
3. Wire the loop to the agent's background task runner

---

## 📋 THE PROMPT

```
Implement 5-loop self-improvement logic for agent: [AGENT_NAME]

LOOP 1 — OBSERVE
  Collect: [METRIC] every [INTERVAL]
  Store to: metrics_log table
  Schema: {agent_id, metric_name, value, timestamp}

LOOP 2 — EVALUATE
  Compare: current [METRIC] vs threshold [THRESHOLD]
  If below threshold: flag for improvement
  If above threshold: log success, continue

LOOP 3 — HYPOTHESISE
  Generate improvement hypothesis:
  "If I change [PARAM] from [A] to [B], [METRIC] should improve by [X%]"
  Log hypothesis to improvement_log

LOOP 4 — EXPERIMENT
  Run [IMPROVE_ACTION] for [TEST_DURATION]
  A/B split if possible (see HS-044)
  Measure delta vs baseline

LOOP 5 — LEARN
  If delta positive: adopt change, update agent config
  If delta negative: rollback, log failure, try next hypothesis
  NEVER adopt change without measuring delta first
  Human approval required for: config changes above [RISK_THRESHOLD]

SACRED RULE: Agent may improve its METHODS. Never its GOALS.
```

---

## 🔗 Related Skills
- HS-040 — GOALKEEPER (Self-Improving Agent)
- HS-044 — A/B Testing Framework
- HS-045 — Cost Optimisation Auto-Pattern

---
*HYPER-SKILLs Vault — welshDog 🐕🏴󠁧󠁢󠁷󠁬󠁳󠁧⚡*
