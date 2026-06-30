# HS-007 — 🐝 HYPERFOCUS AGENT SWARM CORE — How the Whole Swarm Thinks Together

---
skill_id: HS-007
hero_name: "HYPERFOCUS AGENT SWARM CORE"
emoji: "🐝"
version: v1.0.0
status: ACTIVE
category: agents
depends_on:
  - HS-001  # ANATOMY_OF_AN_AGENT — swarm is made of agents
  - HS-002  # SIX_LAWS_OF_AGENTS — laws govern swarm behaviour
  - HS-003  # AGENT_LIFECYCLE_STATE_MACHINE — swarm manages agent lifecycles
provides:
  - swarm-coordination-pattern
  - agent-swarm-architecture
  - task-delegation-protocol
  - swarm-consensus-logic
related:
  - HS-008  # BROSKI_ORCHESTRATOR_PATTERN
  - HS-009  # HYPER_AGENT_ROSTER
  - HS-016  # AGENT_COMMUNICATION_PATTERNS
graph_notes: "Top-level swarm architecture — defines how 39+ agents coordinate, delegate, and reach consensus across the HyperFocus ecosystem."
problem_keywords:
  - multiple agents
  - agent swarm
  - coordinate agents
  - swarm core

---

**Category:** `agents/`
**Version:** v1

---

## 🔗 Related Skills

- [[HS-008]] BROSKI_ORCHESTRATOR_PATTERN — the orchestrator that runs the swarm
- [[HS-009]] HYPER_AGENT_ROSTER — full list of agents in the swarm
- [[HS-016]] AGENT_COMMUNICATION_PATTERNS — how swarm agents talk to each other

---

## 📋 THE PROMPT

```text
Use skill HS-007 HYPERFOCUS AGENT SWARM CORE. Coordinate the swarm to handle task: [TASK]. Assign to appropriate specialist agents using the delegation protocol.
```
