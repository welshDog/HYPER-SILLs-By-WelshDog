# 🛫 DS-009 — PREFLIGHT CHECKS SYSTEM — Boot Sequence Validation Before Any Agent Runs

---
skill_id: DS-009
hero_name: "PREFLIGHT CHECKS SYSTEM"
emoji: "🛫"
version: v1.0
category: dev
depends_on:
  - HS-003  # AGENT_LIFECYCLE_STATE_MACHINE
  - DS-010  # CODE_STYLE_STANDARDS
provides:
  - preflight-check-sequence
  - boot-validation
  - dependency-health-check
  - env-var-validation
related:
  - DS-005  # PRE_COMMIT_TESTING_CHECKLIST
  - DS-003  # NEW_AGENT_BUILD_CHECKLIST
  - HS-005  # HEALER_CIRCUIT_BREAKER_PROTOCOL
graph_notes: "Preflight system — validates env vars, dependency health, Docker containers, and secrets before any agent boots."
---

**Category:** `dev/`
**Version:** v1

## 📋 THE PROMPT
```text
Use skill DS-009 PREFLIGHT CHECKS SYSTEM. Run preflight checks for [AGENT_NAME] before boot.
```
