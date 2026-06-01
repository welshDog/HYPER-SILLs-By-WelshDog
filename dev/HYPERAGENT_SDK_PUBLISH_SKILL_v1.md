# 📦 DS-017 — HYPERAGENT SDK PUBLISH SKILL — Ship @w3lshdog/hyper-agent to npm

---
skill_id: DS-017
hero_name: "HYPERAGENT SDK PUBLISH SKILL"
emoji: "📦"
version: v1.0
category: dev
depends_on:
  - DS-016  # SDK_PUBLISH_WORKFLOW
  - DS-015  # PARALLEL_GIT_WORKFLOW_SURVIVAL
provides:
  - npm-publish-steps
  - sdk-version-bump
  - package-release-checklist
related:
  - DS-014  # CROSS_REPO_SYNC
  - DS-019  # FASTAPI_AGENT_API_STANDARDS
graph_notes: "Step-by-step publish flow for @w3lshdog/hyper-agent — bump, build, test, publish, tag."
---

**Category:** `dev/`
**Version:** v1

## 📋 THE PROMPT
```text
Use skill DS-017 HYPERAGENT SDK PUBLISH SKILL. Publish version [VERSION] of @w3lshdog/hyper-agent to npm.
```
