# WHATS_DONE.md -- HYPER-SILLs-By-WelshDog

> Single source of truth. Check this before building ANYTHING.
> Last updated: 2026-06-28

## v3.3 Search & Recommend Quality (2026-06-28) -- DONE, do not redo

Fixed the three search/recommend weaknesses (Perplexity review + live testing):

- **`recommend_for_task` now uses the semantic engine** (`scripts/search_skills.semantic_search`)
  instead of flat keyword-overlap counts. Scores are real cosine floats (e.g. 0.39/0.33/0.31),
  no longer all `2`; top result for "self-healing docker agent" is now **HS-103 HEALER'S CHORUS**
  (was the weaker MIRROR OATH). Keyword scoring kept as fallback, but **normalised 0..1** (not flat ints).
- **Tags + keywords enriched** in `generate_registry.py` (`enrich_tags_keywords()`): each skill gets
  its frontmatter `provides` slugs as tags + top content-frequency `keywords` (search-only, hidden).
  `search_skills` now matches these → **"docker" hits 5 skills (was 0)**, "graph dependency" hits 2.
- **`version` surfaced** in `search_skills` + `recommend_for_task` results.
- **Honest backend label** — `semantic_search`/`recommend` now report the *real* engine
  (`tfidf` / `local:…` / `openai:…`) via `search_skills.active_backend()`, not a hardcoded "semantic".
  The old label misled (Railway runs **tfidf** — `requirements.txt` has no sentence-transformers, by
  design: lean/free/fast, good for 120 skills). To upgrade to dense later: add `openai` to
  `requirements.txt` + set `OPENAI_API_KEY` (the `openai` backend is already wired, no torch needed).
- Registry regenerated (still 120/6-cat), plugin bundle rebuilt (373 KB). **Requires `railway up`** to
  go live. NOTE: Railway builds the vector index on-the-fly (tfidf) from the deployed registry.

## v3.2 Bridge + HTTP Transport (2026-06-28) -- DONE, do not redo

**The Hyper Merge bridge is now LIVE, not just declared.**

- **HTTP transport added** to `mcp_server.py`: `python mcp_server.py --http` serves **streamable-http** (the current standard; SSE deprecated but available via `--sse`) on `$PORT` (default 8000), host `$HOST` (default 0.0.0.0). stdio is still the default for local IDE wiring. Verified live: `/mcp` returns 406 to a bare GET (correct — needs MCP Accept headers).
- **`/health` endpoint** (`@mcp.custom_route`) — the manifest declared `health_check: /health` but the server never served it. Now returns `{"status":"ok","service":"hyper-sills-mcp","version":"1.1.0","skills":120,"categories":{...}}`. Verified live → HTTP 200. Fail-soft (503 on registry error, never crashes the probe).
- **Deploy files**: `Procfile` (`web: python mcp_server.py --http`) + `railway.json` (NIXPACKS, startCommand `--http`, `healthcheckPath: /health`). Railway/Render one-command deploy → public URL → paste into Perplexity's MCP connector. `mcp>=1.0.0` (pyproject) pulls starlette+uvicorn.
- **Bridge wired into HyperAgent-SDK**: ran `hyper-agent registry build ../HYPER-SILLs-By-WelshDog --strict` → SDK `registry.json` now lists `hyper-sills-mcp` as a **verified** agent (badges: verified, mcp-ready, multi-tool, hyper-coder, elite, health-checked, featured; level 5; port 3350). Replaced the 4 throwaway template scaffolds (correct — production registry = real agents). Manifest passes `hyper-agent validate` (1 passed, 0 failed, mcp ✓).
- **SDK `registry build` upgraded** to accept **multiple paths** (`build <repoA> <repoB> ...`) so one ecosystem registry can span all 5 repos as they add manifests. Fixed a latent arg-parse bug (the `--out` value leaked in as a phantom path) via a new `positionalArgs()` helper. `node --check` clean.
- **Still TODO** (handover): rate-limit on Redis DB 2; `SILLS_EMBED_BACKEND` env var; bundle pre-deploy step; wire other 4 repos' manifests into the registry.

## v3.1 Registry Reconciliation (2026-06-28) -- DONE, do not redo

**The 96 → 120 fix.** The registry undercounted: `generate_registry.py` builds the registry by parsing only the `## ✅ RESCUED SKILLS` table in `vault-index.md`, and **24 real on-disk skills lived in the stale `CATALOGUED` section** (no file-link column) → silently absent from the registry, MCP server, and the `manifest.json` bridge. Promoted all 24 to proper RESCUED rows. **Registry now 120 skills / 6 categories** (was 96 / 4): agents 51, dev 39, hypercode 12, broski 7, web3 7, youtube 4. The whole `hypercode/` (12) and `web3/` (7 BROskiPets/dNFT) packs are now live + queryable over MCP.

- **Two id namespaces (don't confuse):** registry IDs come from vault-index.md (what MCP serves); in-file frontmatter `skill_id` is the GoS-graph id and is *intentionally* different for some skills (e.g. THE FIVE WARDS = registry HS-085 / GoS HS-004). Do NOT "fix" the generator to read frontmatter skill_id — it would renumber ~30 dev skills and break the registry.
- **Dup files resolved:** archived `hypercode/V24_SACRED_RULES_v1.md` (kept `V2_4_SACRED_RULES`, HS-031) and `hypercode/AI_BEHAVIOUR_RULES_v1.md` (kept `AI_BEHAVIOUR_RULES_TOOL_MATRIX`, HS-035) → `_archive/`.
- **GoS bug fixed:** `dev/CORE_AGENT_METRICS_CONTRACT_v1.md` frontmatter `skill_id` was `HS-105` but its H1 + 6 inbound `depends_on` edges use `DS-008`; set frontmatter to `DS-008` so those edges resolve (verified via `get_skill_graph('DS-001')`).
- **Safety net added:** `generate_registry.py` now runs `reconcile_disk()` after every build — warns loudly if any skill `.md` on disk has no registry row. Currently **clean** (disk 120 ↔ registry 120). This is what would have caught the original bug.
- **The 24 promoted skills carry `status: rescued`** (they're legacy files lacking v3.0 GoS/semver frontmatter). That's accurate, not a bug. Bulk frontmatter backfill of legacy skills is still the open debt (see below) — do NOT invent `depends_on` edges hastily.
- Updated to match: `README.md` (120/6-cat table + architecture), `manifest.json` (description + tool category lists), `mcp_server.py` (instructions + category docstrings). No `skills-bundle.json` exists, so MCP reads `skills-registry.json` directly — changes are already live. `vault-index.md` RESCUED header + stats say 120. Linter: 0 errors.

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
