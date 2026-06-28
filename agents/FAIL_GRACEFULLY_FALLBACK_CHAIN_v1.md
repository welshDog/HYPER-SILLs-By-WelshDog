# HS-006 — 🪂 FAIL GRACEFULLY FALLBACK CHAIN — Never Crash Hard, Always Have a Plan B

---
skill_id: HS-006
hero_name: "FAIL GRACEFULLY FALLBACK CHAIN"
emoji: "🪂"
version: v1.0.0
status: ACTIVE
category: agents
depends_on:
  - HS-003  # AGENT_LIFECYCLE_STATE_MACHINE — fallback is a lifecycle state
  - HS-004  # FIVE_MANDATORY_GUARDRAILS — guardrails define what triggers fallback
provides:
  - fallback-chain-pattern
  - graceful-degradation
  - error-recovery-steps
related:
  - HS-005  # HEALER_CIRCUIT_BREAKER_PROTOCOL
  - HS-019  # OBSERVABLE_AGENT_OPERATIONS
  - HS-020  # COST_OPTIMISATION_AUTO_PATTERN
graph_notes: "Defines the 3-level fallback chain (retry → degrade → safe-mode) used by every agent that can fail."
---

**Category:** `agents/`
**Version:** v1

---

## 🔗 Related Skills

- [[HS-005]] HEALER_CIRCUIT_BREAKER_PROTOCOL — healer kicks in after fallback exhausted
- [[HS-019]] OBSERVABLE_AGENT_OPERATIONS — log every fallback event

---

## 📋 THE PROMPT

```text
Use skill HS-006 FAIL GRACEFULLY FALLBACK CHAIN. Agent [AGENT_NAME] just hit error [ERROR]. Walk through the 3-level fallback chain.
```
