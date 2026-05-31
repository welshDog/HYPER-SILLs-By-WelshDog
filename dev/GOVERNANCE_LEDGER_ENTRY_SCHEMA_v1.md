# DS-025 — 📒 GOVERNANCE LEDGER ENTRY SCHEMA — Audit Trail for Every Decision

---
skill_id: DS-025
hero_name: "GOVERNANCE LEDGER ENTRY SCHEMA"
emoji: "📒"
version: v1.0
category: dev
depends_on:
  - DS-010  # CODE_STYLE_STANDARDS — schema follows naming conventions
provides:
  - governance-schema
  - audit-trail-pattern
  - decision-log-format
related:
  - DS-012  # TRUTH_VS_CLAIM_AUDIT
  - HS-019  # OBSERVABLE_AGENT_OPERATIONS
  - DS-008  # CORE_AGENT_METRICS_CONTRACT
graph_notes: "Schema for governance ledger entries — records every significant agent decision with timestamp, actor, and rationale."
---

**Category:** `dev/`
**Version:** v1

## 📋 THE PROMPT
```text
Use skill DS-025 GOVERNANCE LEDGER ENTRY SCHEMA. Log decision [DECISION] with actor [AGENT] at [TIMESTAMP].
```
