# 🔬 DS-012 — TRUTH VS CLAIM AUDIT — Is What Claude Said Actually True?

---
skill_id: DS-012
hero_name: "TRUTH VS CLAIM AUDIT"
emoji: "🔬"
version: v1.0
category: dev
depends_on:
  - DS-011  # CROSS_REFERENCE_BEFORE_WRITING
provides:
  - claim-verification
  - truth-audit-checklist
  - ai-output-validation
related:
  - DS-025  # GOVERNANCE_LEDGER_ENTRY_SCHEMA
  - DS-011  # CROSS_REFERENCE_BEFORE_WRITING
graph_notes: "Audit protocol to verify AI claims against GitHub, Supabase, and WHATS_DONE before acting on them."
---

**Category:** `dev/`
**Version:** v1

## 📋 THE PROMPT
```text
Use skill DS-012 TRUTH VS CLAIM AUDIT. Verify this claim: [CLAIM] — check against actual codebase state.
```
