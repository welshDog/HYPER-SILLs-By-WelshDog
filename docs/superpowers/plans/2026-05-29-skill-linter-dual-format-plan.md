# Skill Linter Dual-Format Support Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Update `scripts/skill_linter.py` to validate both legacy skills and YAML-template skills without breaking CI.

**Architecture:** Detect YAML frontmatter near file top; if present, use strict YAML + heading validation. Otherwise validate legacy skill structure.

**Tech Stack:** Python 3.11, GitHub Actions.

---

### Task 1: Add legacy validation path

**Files:**
- Modify: `scripts/skill_linter.py`

- [ ] **Step 1: Add format detection helper**
  - A helper that checks for a frontmatter start `---` in the first non-empty line, and a closing `---` shortly after.

- [ ] **Step 2: Implement `lint_legacy_file(...)`**
  - Header check: `^#\\s+HS-\\d{3,}\\b`
  - Required fields: `**Category:**`, `**Version:**`
  - Prompt presence: accept `## 🤖 THE PROMPT` or `## 🔮 Prompt Block` or a prompt heading + fenced code block.

- [ ] **Step 3: Update `lint_file(...)` branching**
  - If YAML frontmatter exists → current strict checks
  - Else → legacy checks
  - Keep filename convention warnings for both paths.

- [ ] **Step 4: Run linter locally**

Run: `python scripts/skill_linter.py`  
Expected: exit code 0 (warnings allowed)

- [ ] **Step 5: Commit**

```bash
git add scripts/skill_linter.py
git commit -m "fix: support legacy skill format in linter"
```

### Task 2: Commit spec/plan docs + push

**Files:**
- Add: `docs/superpowers/specs/2026-05-29-skill-linter-dual-format-design.md`
- Add: `docs/superpowers/plans/2026-05-29-skill-linter-dual-format-plan.md`

- [ ] **Step 1: Commit docs**

```bash
git add docs/superpowers/specs/2026-05-29-skill-linter-dual-format-design.md docs/superpowers/plans/2026-05-29-skill-linter-dual-format-plan.md
git commit -m "docs: add dual-format linter spec"
```

- [ ] **Step 2: git fetch + rebase + push**

```bash
git fetch
git pull --rebase
git push
```

