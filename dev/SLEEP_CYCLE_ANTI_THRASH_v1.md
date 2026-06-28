# 😴 DS-029 — SLEEP CYCLE ANTI THRASH — Stop Agents Waking Up Every 10 Seconds

---
skill_id: DS-029
hero_name: "SLEEP CYCLE ANTI THRASH"
emoji: "😴"
version: v1.0.0
status: ACTIVE
category: dev
depends_on:
  - DS-028  # PROGRESSIVE_HEALTH_WAIT
  - HS-003  # AGENT_LIFECYCLE_STATE_MACHINE
provides:
  - sleep-cycle-pattern
  - anti-thrash-rules
  - idle-agent-behaviour
related:
  - HS-005  # HEALER_CIRCUIT_BREAKER_PROTOCOL
  - HS-019  # OBSERVABLE_AGENT_OPERATIONS
graph_notes: "Anti-thrash sleep pattern for idle agents — prevents CPU waste and Discord rate limits from over-eager polling."
---

**Category:** `dev/`
**Version:** v1

## 📋 THE PROMPT
```text
Use skill DS-029 SLEEP CYCLE ANTI THRASH. Fix thrashing in agent [AGENT_NAME] — implement proper sleep/wake cycle.
```
