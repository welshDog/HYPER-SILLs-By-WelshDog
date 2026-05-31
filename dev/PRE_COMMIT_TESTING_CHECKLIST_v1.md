# DS-005 — 🔒 PRE COMMIT TESTING CHECKLIST — Never Push Broken Code Again

---
skill_id: DS-005
hero_name: "PRE COMMIT TESTING CHECKLIST"
emoji: "🔒"
version: v1.0
category: dev
depends_on:
  - DS-010  # CODE_STYLE_STANDARDS — lint must pass
  - DS-006  # TEST_PYRAMID_FOUR_LEVELS — tests must pass
provides:
  - pre-commit-gates
  - commit-block-rules
  - ci-checklist
related:
  - DS-001  # AGENT_CONTRACT_TEST_SUITE
  - DS-009  # PREFLIGHT_CHECKS_SYSTEM
  - DS-003  # NEW_AGENT_BUILD_CHECKLIST
graph_notes: "Pre-commit gate checklist — lint, tests, secret scan, type check. Hard blocks for set-state-in-effect and committed secrets."
---

**Category:** `dev/`
**Version:** v1

## 📋 THE PROMPT
```text
Use skill DS-005 PRE COMMIT TESTING CHECKLIST. Run all pre-commit gates on [FILES_CHANGED].
```
