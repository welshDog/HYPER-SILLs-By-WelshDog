# 🧪 DS-001 — AGENT CONTRACT TEST SUITE — Verify Every Agent Keeps Its Promises

---
skill_id: DS-001
hero_name: "AGENT CONTRACT TEST SUITE"
emoji: "🧪"
version: v1.0
category: dev
depends_on:
  - HS-001  # ANATOMY_OF_AN_AGENT
  - DS-008  # CORE_AGENT_METRICS_CONTRACT
provides:
  - agent-contract-testing
  - output-validation
  - integration-test-pattern
related:
  - DS-005  # PRE_COMMIT_TESTING_CHECKLIST
  - DS-006  # TEST_PYRAMID_FOUR_LEVELS
  - HS-004  # FIVE_MANDATORY_GUARDRAILS
graph_notes: "Contract tests for every agent — validates inputs, outputs, and side effects match the anatomy spec."
---

**Category:** `dev/`
**Version:** v1

## 🔗 Related Skills
- [[HS-001]] ANATOMY_OF_AN_AGENT
- [[DS-005]] PRE_COMMIT_TESTING_CHECKLIST
- [[DS-006]] TEST_PYRAMID_FOUR_LEVELS

## 📋 THE PROMPT
```text
Use skill DS-001 AGENT CONTRACT TEST SUITE. Write contract tests for agent [AGENT_NAME] — validate inputs, outputs, and error handling.
```
