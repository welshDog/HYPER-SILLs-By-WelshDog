# HS-008 — 🎼 BROSKI ORCHESTRATOR PATTERN — The Master Conductor of the Agent Swarm

---
skill_id: HS-008
hero_name: "BROSKI ORCHESTRATOR PATTERN"
emoji: "🎼"
version: v1.0.0
status: ACTIVE
category: agents
depends_on:
  - HS-007  # HYPERFOCUS_AGENT_SWARM_CORE — orchestrator runs the swarm
  - HS-009  # HYPER_AGENT_ROSTER — needs to know which agents exist
provides:
  - orchestrator-pattern
  - task-routing-logic
  - agent-dispatch-protocol
  - result-aggregation
related:
  - HS-083  # THE THREE VOICES — comms patterns the orchestrator applies
  - HS-067  # THE THRONE LADDER — role hierarchy governs orchestrator authority
  - HS-075  # THE CHOICE MATRIX — decision framework for delegate vs. execute
  - HS-087  # THE BRANCHING PATH — decision tree routes tasks from the orchestrator
graph_notes: "The BROski Orchestrator is the central brain that receives tasks, routes them to specialist agents, and aggregates results."
problem_keywords:
  - route tasks
  - dispatch
  - orchestrate
  - delegate to agents
  - orchestrator

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
