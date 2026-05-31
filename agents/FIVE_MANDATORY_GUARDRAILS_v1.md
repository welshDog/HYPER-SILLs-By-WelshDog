# HS-004 — 🛡️ FIVE MANDATORY GUARDRAILS — The Hard Stops Every Agent Must Respect

---
skill_id: HS-004
hero_name: "FIVE MANDATORY GUARDRAILS"
emoji: "🛡️"
version: v1.0
category: agents
depends_on:
  - HS-002  # SIX_LAWS_OF_AGENTS — guardrails enforce the laws
provides:
  - guardrail-validation
  - hard-stop-patterns
  - agent-safety-contract
related:
  - HS-003  # AGENT_LIFECYCLE_STATE_MACHINE
  - HS-011  # TIER_PROTECTION_RULES
  - HS-015  # USER_AGENCY_APPROVAL_GATE
graph_notes: "Five non-negotiable hard stops that block any agent from crossing safety boundaries — plug into every agent's decision path."
---

**Category:** `agents/`
**Version:** v1

---

## 🔗 Related Skills

- [[HS-002]] SIX_LAWS_OF_AGENTS — the laws these guardrails enforce
- [[HS-011]] TIER_PROTECTION_RULES — tier-based access guardrails
- [[HS-015]] USER_AGENCY_APPROVAL_GATE — human approval as a guardrail

---

## 📋 THE PROMPT

```text
Use skill HS-004 FIVE MANDATORY GUARDRAILS. Check if the following action violates any of the 5 hard stops: [ACTION].
```
