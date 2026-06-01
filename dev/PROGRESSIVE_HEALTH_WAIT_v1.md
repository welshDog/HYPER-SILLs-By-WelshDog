# ⏳ DS-028 — PROGRESSIVE HEALTH WAIT — Smart Retry With Backoff, Not Hammering

---
skill_id: DS-028
hero_name: "PROGRESSIVE HEALTH WAIT"
emoji: "⏳"
version: v1.0
category: dev
depends_on:
  - HS-005  # HEALER_CIRCUIT_BREAKER_PROTOCOL
  - HS-006  # FAIL_GRACEFULLY_FALLBACK_CHAIN
provides:
  - exponential-backoff-pattern
  - health-wait-sequence
  - retry-with-jitter
related:
  - DS-009  # PREFLIGHT_CHECKS_SYSTEM
  - HS-019  # OBSERVABLE_AGENT_OPERATIONS
graph_notes: "Progressive health wait with exponential backoff and jitter — used by healers and preflight checks."
---

**Category:** `dev/`
**Version:** v1

## 📋 THE PROMPT
```text
Use skill DS-028 PROGRESSIVE HEALTH WAIT. Add progressive backoff retry to [SERVICE] with max [N] attempts.
```
