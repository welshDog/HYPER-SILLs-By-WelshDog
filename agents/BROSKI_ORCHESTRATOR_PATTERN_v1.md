# HS-008 — 🎼 BROSKI ORCHESTRATOR PATTERN — The Master Conductor of the Agent Swarm

---
skill_id: HS-008
hero_name: "BROSKI ORCHESTRATOR PATTERN"
emoji: "🎼"
version: v1.0
category: agents
depends_on:
  - HS-007  # HYPERFOCUS_AGENT_SWARM_CORE — orchestrator runs the swarm
  - HS-009  # HYPER_AGENT_ROSTER — needs to know which agents exist
  - HS-016  # AGENT_COMMUNICATION_PATTERNS — how to call agents
provides:
  - orchestrator-pattern
  - task-routing-logic
  - agent-dispatch-protocol
  - result-aggregation
related:
  - HS-014  # AGENT_ROLE_HIERARCHY_PATTERN
  - HS-017  # AGENT_DECISION_FRAMEWORK_MATRIX
  - HS-018  # AGENT_DECISION_TREE_FLOWCHART
graph_notes: "The BROski Orchestrator is the central brain that receives tasks, routes them to specialist agents, and aggregates results."
---

**Category:** `agents/`
**Version:** v1

---

## 🔗 Related Skills

- [[HS-009]] HYPER_AGENT_ROSTER — which agents the orchestrator can call
- [[HS-017]] AGENT_DECISION_FRAMEWORK_MATRIX — how it decides which agent to use
- [[HS-014]] AGENT_ROLE_HIERARCHY_PATTERN — role hierarchy the orchestrator respects

---

## 📋 THE PROMPT

```text
Use skill HS-008 BROSKI ORCHESTRATOR PATTERN. Route the following task to the correct specialist agent: [TASK]. Show the decision path and expected output.
```
