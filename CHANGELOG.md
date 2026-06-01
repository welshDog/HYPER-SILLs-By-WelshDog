# 📋 HYPER-SILLs Vault — CHANGELOG

---

## [v2.2] — 2026-06-01 🟢 LINTER CLEAN

### 🔧 Fixed
- `scripts/skill_linter.py` bumped to **v2.2**
- `LEGACY_HEADER_PATTERN` regex updated to accept **DS-NNN prefix** alongside HS-NNN
  - Cleared **32 errors** in `dev/` folder instantly
- `dev/CORE_AGENT_METRICS_CONTRACT_v1.md` — fixed broken `depends_on: HS-070` → corrected to `HS-019` (OBSERVABLE_AGENT_OPERATIONS)
  - Cleared the **final 1 error**

### 📊 Before / After
| Metric | Before | After |
|---|---|---|
| Errors | 36 | **0** ✅ |
| Warnings | 56 | 51 |
| Files | 90 | 90 |
| Circular deps | 0 | 0 |

### 🎯 Linter Status: PASSED ✅

---

## [v2.1] — 2026-05-26

### 🔧 Fixed
- Legacy header regex now tolerates emoji prefix (e.g. `# 🛠️ HS-114 —`)
- GoS validation: detects broken HS-NNN cross-references
- Circular dependency detection across vault
- Warns when `skill_id` in frontmatter doesn't match filename HS-NNN
- Warns on skills with no `provides` (graph dead-ends)

---

## [v2.0] — 2026-05-20

### ✨ Added
- Graph-of-Skills (GoS) validation layer
- `depends_on`, `provides`, `related`, `graph_notes` field checks
- Vault-wide ID discovery + broken reference detection
- Circular dependency detection

---

## [v1.0] — 2026-05-01

### ✨ Added
- Initial vault linter
- YAML frontmatter validation
- Required headings check
- Category + difficulty validation
- File naming convention check
