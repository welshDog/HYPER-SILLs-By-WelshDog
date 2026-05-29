# Skill Metadata Auto-Fix Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Auto-fix legacy skill metadata so the vault lints cleanly (or close to clean) with minimal manual edits.

**Architecture:** Create a small script that inserts missing `Category` and `Version` under the HS header and adds a minimal prompt code block when no code blocks exist.

**Tech Stack:** Python, Markdown, git.

---

### Task 1: Add the auto-fix script

**Files:**
- Create: `scripts/fix_legacy_skill_metadata.py`

- [ ] **Step 1: Add script (idempotent)**
  - Skip YAML-frontmatter files.
  - Insert missing `**Category:**` + `**Version:**`.
  - Append `## 📋 THE PROMPT` + fenced `text` block if the file has no fenced code blocks.

- [ ] **Step 2: Run script**

Run: `python scripts/fix_legacy_skill_metadata.py`  
Expected: prints `Updated N files`

- [ ] **Step 3: Run linter**

Run: `python scripts/skill_linter.py`  
Expected: exit code 0 with fewer warnings

### Task 2: Commit and push

**Files:**
- Modify: `agents/**/*.md`, `dev/**/*.md`, `broski/**/*.md`, `youtube/**/*.md`, `hypercode/**/*.md` (as touched by the script)
- Create: `docs/superpowers/specs/2026-05-29-skill-metadata-autofix-design.md`
- Create: `docs/superpowers/plans/2026-05-29-skill-metadata-autofix-plan.md`

- [ ] **Step 1: Commit**

```bash
git add scripts/fix_legacy_skill_metadata.py docs/superpowers/specs/2026-05-29-skill-metadata-autofix-design.md docs/superpowers/plans/2026-05-29-skill-metadata-autofix-plan.md agents dev broski youtube hypercode
git commit -m "chore: auto-fix legacy skill metadata"
```

- [ ] **Step 2: git fetch + push**

```bash
git fetch
git push
```

