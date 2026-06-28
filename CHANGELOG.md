# 📋 HYPER-SILLs Vault — CHANGELOG

---

## [v3.0] — 2026-06-28 🚀 DISTRIBUTION + DISCOVERY + ND-UX

### ✨ Added — Distribution & Reach
- **Claude Code plugin marketplace** — `.claude-plugin/marketplace.json` + `plugins/hyper-sills-vault/`
  (plugin.json bundles the MCP server; `/skill-find`, `/skill-load`, `/skill-recommend` commands).
  Install: `/plugin marketplace add welshDog/HYPER-SILLs-By-WelshDog` → `/plugin install hyper-sills-vault`.
- **Format bridge** — `scripts/export_claude_skills.py` exports all skills to the portable
  agentskills.io / Claude Code `SKILL.md` format (`--format`, `--pack`, `--category`).
- **MCP Resources surface** — `skills://index` + `skill://HS-NNN` (tracks Skills-over-MCP / SEP-2640),
  added to `mcp_server.py` alongside the existing tools.
- **OCI publishing** — `.github/workflows/publish-skills.yml` pushes skills as OCI artifacts on release.

### ✨ Added — Discovery Intelligence
- **Semantic search** — `scripts/embed_skills.py` + `scripts/search_skills.py` (local TF-IDF, zero deps);
  `semantic_search` MCP tool (keyword fallback) + `hyper_brain_ops.py skill-search`.
- **Trigger engine** — `scripts/trigger_engine.py` + `packs/*/manifest.yaml` (auto-suggest packs from context).
- **Learning loop** — `.skill-memory/` + `scripts/skill_memory.py`; `sills_session_end.py` records used
  skill IDs from the transcript; `hyper_brain_ops.py analyze-skill-usage`.

### ✨ Added — ND-First Experience
- **Mercy messages** — no-blame "skill not found" / fallback responses across the MCP server.
- **Body-double mode** — `scripts/body_double.py` (presence + gentle nudges + session logging).
- **Progress tracker** — `scripts/progress_tracker.py` + `progress-tracker.yaml` + `skill-progress` command.
- **Skill constellation** — `scripts/generate_skill_map.py` → Mermaid map (`docs/skill-map.md`).

### ✨ Added — Content & Freshness
- 4 new 2026-tech skills: **HS-128 PLUGIN FORGE**, **HS-129 SKILLS-OVER-MCP**,
  **HS-130 OCI SKILL SHIP**, **HS-131 THE NESTED SWARM**.
- **YouTube rebalance** — **HS-132 THUMBNAIL DUELIST**, **HS-133 SHORTS ALCHEMIST**,
  **HS-134 SIGNAL-TO-SCRIPT LOOP** (youtube 1 → 4). Vault 89 → **96 skills**.
- **Semantic versioning + lifecycle** — `status:` (DRAFT/REVIEW/ACTIVE/DEPRECATED/ARCHIVED) and semver
  flow from frontmatter → registry (`generate_registry.py`) → linter validation (`skill_linter.py`).

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
