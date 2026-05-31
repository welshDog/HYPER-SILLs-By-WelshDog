# DS-016 — 🚢 SDK PUBLISH WORKFLOW — The Exact Steps to Ship an npm Package

---
skill_id: DS-016
hero_name: "SDK PUBLISH WORKFLOW"
emoji: "🚢"
version: v1.0
category: dev
depends_on:
  - DS-015  # PARALLEL_GIT_WORKFLOW_SURVIVAL — git hygiene first
  - DS-005  # PRE_COMMIT_TESTING_CHECKLIST — tests pass before publish
provides:
  - npm-publish-workflow
  - semver-bump-steps
  - package-release-protocol
related:
  - DS-017  # HYPERAGENT_SDK_PUBLISH_SKILL
  - DS-014  # CROSS_REPO_SYNC
graph_notes: "Generic npm SDK publish workflow — version bump, changelog, build, test, publish, git tag."
---

**Category:** `dev/`
**Version:** v1

## 📋 THE PROMPT
```text
Use skill DS-016 SDK PUBLISH WORKFLOW. Publish [PACKAGE_NAME] at version [VERSION] — walk through every step.
```
