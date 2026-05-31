# DS-007 — 📊 TEST STATUS REPORT — Show Exactly Where Tests Pass and Fail

---
skill_id: DS-007
hero_name: "TEST STATUS REPORT"
emoji: "📊"
version: v1.0
category: dev
depends_on:
  - DS-006  # TEST_PYRAMID_FOUR_LEVELS — report covers all 4 levels
  - DS-008  # CORE_AGENT_METRICS_CONTRACT — test metrics follow contract
provides:
  - test-status-format
  - coverage-report-schema
  - test-health-dashboard
related:
  - DS-005  # PRE_COMMIT_TESTING_CHECKLIST
  - HS-019  # OBSERVABLE_AGENT_OPERATIONS
graph_notes: "Standardised test status report format — per-agent pass/fail, coverage %, and trend vs last sprint."
---

**Category:** `dev/`
**Version:** v1

## 📋 THE PROMPT
```text
Use skill DS-007 TEST STATUS REPORT. Generate a test status report for [COMPONENT] as of [DATE].
```
