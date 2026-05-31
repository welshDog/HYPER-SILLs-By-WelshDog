# HS-019 — 👁️ OBSERVABLE AGENT OPERATIONS — If You Can't See It, You Can't Fix It

---
skill_id: HS-019
hero_name: "OBSERVABLE AGENT OPERATIONS"
emoji: "👁️"
version: v1.0
category: agents
depends_on:
  - HS-003  # AGENT_LIFECYCLE_STATE_MACHINE — observes state transitions
  - HS-005  # HEALER_CIRCUIT_BREAKER_PROTOCOL — feeds metrics to circuit breaker
provides:
  - observability-pattern
  - agent-metrics-schema
  - structured-logging
  - prometheus-integration
  - trace-context
related:
  - HS-006  # FAIL_GRACEFULLY_FALLBACK_CHAIN
  - HS-012  # GUARDIAN_WATCHDOG_MONITOR
  - HS-020  # COST_OPTIMISATION_AUTO_PATTERN
graph_notes: "Observability layer for all agents — structured logs, Prometheus metrics, trace IDs. Required by the guardian and healer agents."
---

**Category:** `agents/`
**Version:** v1

---

## 🔗 Related Skills

- [[HS-012]] GUARDIAN_WATCHDOG_MONITOR — watchdog reads these metrics
- [[HS-005]] HEALER_CIRCUIT_BREAKER_PROTOCOL — circuit breaker reads failure metrics
- [[HS-020]] COST_OPTIMISATION_AUTO_PATTERN — cost metrics feed optimisation

---

## 📋 THE PROMPT

```text
Use skill HS-019 OBSERVABLE AGENT OPERATIONS. Add observability to agent [AGENT_NAME]: structured logs, Prometheus counter, and trace context.
```
