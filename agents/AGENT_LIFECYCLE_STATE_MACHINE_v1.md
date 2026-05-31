# HS-003 — 🔄 AGENT LIFECYCLE STATE MACHINE — Every Agent's Journey from Boot to Retire

---
skill_id: HS-003
hero_name: "AGENT LIFECYCLE STATE MACHINE"
emoji: "🔄"
version: v1.0
category: agents
depends_on:
  - HS-001  # ANATOMY_OF_AN_AGENT — agent must exist before it has a lifecycle
  - HS-002  # SIX_LAWS_OF_AGENTS — laws govern state transitions
provides:
  - agent-state-transitions
  - lifecycle-management
  - agent-boot-sequence
  - agent-retire-protocol
related:
  - HS-005  # HEALER_CIRCUIT_BREAKER_PROTOCOL
  - HS-006  # FAIL_GRACEFULLY_FALLBACK_CHAIN
  - HS-012  # GUARDIAN_WATCHDOG_MONITOR
graph_notes: "State machine for agent lifecycle — boot, idle, active, error, healing, retired. Required by orchestrators and guardian agents."
---

**Category:** `agents/`
**Version:** v1

---

## 🔗 Related Skills

- [[HS-005]] HEALER_CIRCUIT_BREAKER_PROTOCOL — healer activates on error state
- [[HS-006]] FAIL_GRACEFULLY_FALLBACK_CHAIN — fallback chain for failed transitions
- [[HS-012]] GUARDIAN_WATCHDOG_MONITOR — watchdog monitors state health

---

## 📋 THE PROMPT

```text
Use skill HS-003 AGENT LIFECYCLE STATE MACHINE. Manage an agent's state transition from [current_state] to [target_state] following the canonical lifecycle.
```
