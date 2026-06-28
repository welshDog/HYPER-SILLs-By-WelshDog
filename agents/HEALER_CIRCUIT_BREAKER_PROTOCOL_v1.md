# HS-005 — 💊 HEALER CIRCUIT BREAKER PROTOCOL — Auto-Recovery for Broken Agents

---
skill_id: HS-005
hero_name: "HEALER CIRCUIT BREAKER PROTOCOL"
emoji: "💊"
version: v1.0.0
status: ACTIVE
category: agents
depends_on:
  - HS-003  # AGENT_LIFECYCLE_STATE_MACHINE — healer responds to error states
  - HS-006  # FAIL_GRACEFULLY_FALLBACK_CHAIN — fallback chain feeds healer
provides:
  - circuit-breaker-pattern
  - auto-recovery-sequence
  - health-check-protocol
  - self-healing-agent
related:
  - HS-012  # GUARDIAN_WATCHDOG_MONITOR
  - HS-013  # GUARDIAN_WATCHDOG_POST_LAUNCH
  - HS-019  # OBSERVABLE_AGENT_OPERATIONS
graph_notes: "Circuit breaker pattern — open on N failures, half-open after cooldown, closed on recovery. Powers the self-healing swarm."
---

**Category:** `agents/`
**Version:** v1

---

## 🔗 Related Skills

- [[HS-012]] GUARDIAN_WATCHDOG_MONITOR — watchdog triggers the healer
- [[HS-019]] OBSERVABLE_AGENT_OPERATIONS — metrics feed the circuit breaker

---

## 📋 THE PROMPT

```text
Use skill HS-005 HEALER CIRCUIT BREAKER PROTOCOL. Apply circuit breaker logic to agent [AGENT_NAME] which has failed [N] times. Current state: [STATE].
```
