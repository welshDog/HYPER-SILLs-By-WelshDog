# Skill Linter Dual-Format Support — Design

## Goal

Make `scripts/skill_linter.py` validate both:

1. **New template** skills (YAML frontmatter + section headings), and
2. **Legacy** skills already present in the vault (`# HS-### — ...` header + `**Category:**` + `**Version:**` + prompt section).

This prevents CI from flagging the entire vault as invalid while enabling gradual migration to the new template.

## Current Problem

- The repository contains many legacy-format skill files.
- The current linter treats missing YAML frontmatter and the new required headings as hard errors, causing CI to fail for legacy files.

## Approach

### Format detection

- If the file starts with a YAML frontmatter block (`---` … `---`) within the first 30 lines:
  - Run the existing strict frontmatter + heading checks.
- Otherwise:
  - Run legacy checks.

### Legacy checks (minimum viable)

- Header: first non-empty line matches `^#\s+HS-\d{3,}\b`
- Contains `**Category:**`
- Contains `**Version:**`
- Contains a prompt section, accepted if any of these are present:
  - `## 🤖 THE PROMPT`
  - `## 🔮 Prompt Block`
  - A fenced code block following a heading containing `PROMPT`

### Reporting

- Preserve the current linter’s errors/warnings format and exit codes.
- Keep filename warnings as warnings (not errors).

## Acceptance Criteria

- `python scripts/skill_linter.py` exits 0 for valid legacy skills.
- YAML-template skills continue to be validated with current strict rules.

