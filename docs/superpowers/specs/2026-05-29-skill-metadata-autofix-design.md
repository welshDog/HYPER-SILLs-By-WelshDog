# Skill Metadata Auto-Fix — Design

## Goal

Remove linter warnings across legacy skill files by automatically:

1. Inserting missing `**Category:**` and `**Version:**` lines under the `# HS-###` header.
2. Adding a minimal prompt code block to legacy files that contain no fenced code blocks.

## Non-Goals

- No conversion to YAML/frontmatter format.
- No rewriting of the actual skill content beyond adding missing metadata/prompt scaffolding.

## Approach

- Add `scripts/fix_legacy_skill_metadata.py`:
  - Skips YAML-frontmatter skills.
  - Finds the first `# HS-###` header and inserts missing metadata underneath it.
  - Derives:
    - `Category` from folder name (agents/dev/broski/youtube/hypercode)
    - `Version` from filename suffix `_vN.md` → `N.0`
  - If a file has no fenced code blocks (` ``` `), append:
    - `## 📋 THE PROMPT` (only if no prompt heading exists)
    - a minimal fenced `text` prompt block.

## Acceptance Criteria

- `python scripts/skill_linter.py` exits 0 with significantly fewer warnings.
- Auto-fix script is safe to re-run (idempotent for already-correct files).

