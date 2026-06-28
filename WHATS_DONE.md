# WHATS_DONE.md -- HYPER-SILLs-By-WelshDog

> Single source of truth. Check this before building ANYTHING.
> Last updated: 2026-06-28

## v3.0 Upgrade (2026-06-28) -- ALL EXIST, do not rebuild

| Area | What shipped |
|---|---|
| Plugin marketplace | `.claude-plugin/marketplace.json` + `plugins/hyper-sills-vault/` (plugin.json bundles MCP server; `/skill-find` `/skill-load` `/skill-recommend` commands) |
| Format bridge | `scripts/export_claude_skills.py` -> agentskills.io / Claude Code `SKILL.md` (out to `dist/`, gitignored) |
| MCP Resources | `skills://index` + `skill://HS-NNN` in `mcp_server.py` (SEP-2640) + `semantic_search` tool + mercy messages |
| OCI publish | `.github/workflows/publish-skills.yml` (oras, on release) |
| Semantic search | `scripts/embed_skills.py` + `scripts/search_skills.py` — **pluggable backend** (`--backend auto/local/openai/tfidf`): local sentence-transformers `all-MiniLM-L6-v2` (384-dim, offline) → OpenAI (if key) → TF-IDF fallback. Cache in `vector-store/` (gitignored). MCP/CLI stdout kept clean for stdio transport |
| Trigger engine | `scripts/trigger_engine.py` + `packs/*/manifest.yaml` (3 packs) |
| Learning loop | `.skill-memory/` + `scripts/skill_memory.py`; recorded by `sills_session_end.py` |
| ND-UX | `scripts/body_double.py`, `scripts/progress_tracker.py` (+ `progress-tracker.yaml`), `scripts/generate_skill_map.py` (-> `docs/skill-map.md`) |
| New Brain Ops cmds | `skill-search`, `analyze-skill-usage`, `skill-progress` |
| New skills | HS-128 PLUGIN FORGE, HS-129 SKILLS-OVER-MCP, HS-130 OCI SKILL SHIP, HS-131 THE NESTED SWARM (vault now **93**) |
| Semver + lifecycle | `status:` + semver flow frontmatter -> `generate_registry.py` -> `skill_linter.py` validation |

**YouTube rebalance (2026-06-28):** youtube 1 → 4 skills — HS-132 THUMBNAIL DUELIST, HS-133 SHORTS ALCHEMIST, HS-134 SIGNAL-TO-SCRIPT LOOP (vault now **96**).

**CI fix (2026-06-28):** GitHub Actions is **billing-locked** for this account — the `skill-lint.yml` "Lint Skill Files" check failed at job-startup (0 steps, ~3s) on EVERY push/PR incl. main, regardless of code (linter passes clean locally). Fix: `skill-lint.yml` triggers changed to `workflow_dispatch`-only (stops false-red); real gate is now a **local pre-push hook** (`scripts/git_pre_push_lint.sh`, install via `python scripts/install_git_hooks.py`) — blocks push if `skill_linter.py` errors, override `git push --no-verify`. Re-enable the workflow's push/PR triggers when Actions billing returns. **Re-run the installer after a fresh clone** (hooks aren't cloned). Does NOT clobber the existing XP post-commit hook.
**Embedding backend (2026-06-28):** TF-IDF placeholder → **real dense embeddings**. `search_skills.py` now auto-resolves local sentence-transformers `all-MiniLM-L6-v2` (offline, free, 384-dim) → OpenAI (if `OPENAI_API_KEY`) → TF-IDF fallback. Optional deps in `pyproject.toml` extras (`embeddings`, `openai`); torch/sentence-transformers already installed in this env. `vector-store/skill_index.json` now stores dense vectors (~385KB). Local embedder silences HF progress/logs so MCP stdio stays clean.
**Still open:** bulk semver/status backfill of the legacy skills (new ones use it).
**Gotcha:** GoS `depends_on`/`related` must reference the *in-file* `skill_id:` (renumber aliases — e.g. PORTAL FORGE = DS-020, FIVE WARDS = HS-004), not the registry id, or the linter fails.

---
### Pre-v3.0 baseline

---

## Core Files (ALL EXIST -- do not rebuild)

| File | Size | What it is |
|---|---|---|
| `skills-registry.json` | 23KB | Full skills registry -- the crown jewel |
| `vault-index.md` | 33KB | Complete vault index |
| `HYPER_SKILLs_POWER_UPGRADE_MASTERPLAN_v1.md` | 30KB | Full upgrade masterplan |
| `SKILL.md` | 8.6KB | Core skill definition format |
| `AGENT-START.md` | 6.9KB | Agent onboarding instructions |
| `CHANGELOG.md` | 1.4KB | Change history |
| `pyproject.toml` + `uv.lock` | -- | Python project (uses uv) |

## Folder Structure (ALL EXIST)

| Folder | What it is |
|---|---|
| `agents/` | Agent config files |
| `broski/` | BROski-specific skill content |
| `content/` | Skills content library |
| `dev/` | Dev tools and scripts |
| `docs/` | Documentation |
| `hypercode/` | HyperCode integration skills |
| `output/` | Generated output |
| `scripts/` | Utility scripts |
| `templates/` | Skill templates |
| `youtube/` | YouTube content |

## PSAI + aish Integration (ADDED 2026-06-03)

| File | What it does |
|---|---|
| `skills_query.py` | Python CLI -- search/filter/recommend from skills-registry.json. Agent-callable. |
| `PSAI-Register-Tools.ps1` | Registers 7 skills tools as PSAI agent functions |
| `aish-mcp-config.json` | Wires aish to skills registry + HyperCode gateway + BROski Brain |

## The 7 PSAI Agent Tools

| Tool name | What it does |
|---|---|
| `search_skills` | Keyword search across registry |
| `filter_skills_by_level` | Filter by beginner/intermediate/advanced |
| `filter_skills_by_category` | Filter by category (python, docker, ai...) |
| `recommend_skills_for_task` | Best tool -- recommends skills for a task |
| `list_skill_categories` | Lists all top-level categories |
| `get_skills_registry_stats` | Registry stats (total, categories, size) |
| `search_skills_by_tag` | Filter by tag (mcp, psai, react...) |

## Session Handovers

| File | Date |
|---|---|
| `NEXT_SESSION_HANDOVER_2026-05-26.md` | May 26 |
| `NEXT_SESSION_HANDOVER_2026-06-01.md` | June 1 |

## DO NOT rebuild

- `skills-registry.json` -- massive, took time to build
- `vault-index.md` -- same
- Any folder structure -- already correct
- `pyproject.toml` -- uses uv, don't switch to pip
