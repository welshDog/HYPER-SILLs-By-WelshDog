# WHATS_DONE.md -- HYPER-SILLs-By-WelshDog

> Single source of truth. Check this before building ANYTHING.
> Last updated: 2026-09-04

## 2026-09-04 (latest) — Live MCP service revived after 10-day outage; full dependency freeze

**The service was 502 from 2026-08-19 21:15 UTC to 2026-09-04 00:49 UTC (10 days).**

- **Root cause:** `requirements.txt` had `mcp>=1.0.0` with no ceiling. A routine
  rebuild (triggered by a docs-only commit, `4f8c4a0`) resolved `mcp 2.0.0`,
  which removed `mcp.server.fastmcp`. `mcp_server.py` crashed at
  `from mcp.server.fastmcp import FastMCP` before binding a port → healthcheck
  failed 6/6 → Railway had already torn down the last good deployment
  (`1b2677d5`, 2026-07-25) to promote the new one → hard 502. Verified via
  build logs, `get-service-config`, and the July-25 success build log.
- **Fix — PR #18, merged `eaa7ca8`:**
  - `requirements.txt` is now a **complete exact freeze** — all 62 packages at
    the versions from the last successful build (`1b2677d5`), read from that
    build log. `mcp==1.28.1` (last 1.x before 2.0.0). This is the file Railpack
    installs, so what deploys == what's pinned. **No `requirements-lock.txt`** —
    one file, or drift comes back.
  - `scripts/smoke_test.py` (new) — `py_compile` + `import mcp_server` asserting
    the 123-skill vault loads. Self-skips on a bare checkout (no runtime deps),
    so it never blocks a docs push.
  - `scripts/git_pre_push_lint.sh` now runs the smoke test after the linter.
  - `.github/workflows/smoke-test.yml` (new) — same check, but
    `workflow_dispatch`-only (Actions still billing-locked; same as
    `skill-lint.yml`). Flip the `push` trigger when billing is restored.
  - `scripts/install_git_hooks.py` — fixed a pre-existing cp1252
    `UnicodeEncodeError` on the ✅ in its output (Windows console).
- **Live-verified after redeploy (`bb0c6dc8`, SUCCESS):** `/health` → 200,
  `"skills":123`, `dense_active:true` (MiniLM, not TF-IDF); `/metrics` → real
  Prometheus exposition; `/mcp` → 406 to bare GET (correct).
- **Housekeeping:** closed stale draft PRs #9 (logging_config only; observability
  shipped on main) and #16 (parallel `prometheus_metrics.py`; superseded by
  `e4b45f0`/`6e6972b`). #17 (Railway-agent's own fix draft) closed — superseded
  by #18.
- **Still open (deferred to a repo-hygiene pass, NOT done here):**
  - `pyproject.toml` still has `mcp>=1.0.0`; `uv.lock` is stale (names the
    project `hyper-brain-ops`, tracks only `python-dotenv`). Local-dev parity
    (requirements.txt vs pyproject) is an undecided design question.
  - Railway deploy/crash **notifications are not yet configured** — dashboard
    task (account email + a `sincere-strength` project webhook to Discord).
  - `docs/FULL STATUS REPORT HYPER-SILLs MCP Service Recovery` — loose incident
    note (no extension, spaces in name); fold into `docs/` properly or delete.
  - README still says "120 skills" (actual 123); committed `.zip` artifacts;
    7 `NEXT_SESSION_HANDOVER_*` files; `railway.json` says NIXPACKS but the
    service is on RAILPACK V3.

## 2026-07-25 — HYPER-SILLs instrumented; Prometheus now actually scrapes it

Follow-up to the section directly below, which left HYPER-SILLs unscraped on purpose (its
`/health` endpoint is JSON, not Prometheus exposition format, and no scrape job pointed at it).
Closed that gap end to end, verified at every step rather than assumed:

- **`mcp_server.py` is not FastAPI** — corrected assumption from the task brief. It builds a
  `mcp.server.fastmcp.FastMCP` instance (Starlette-based ASGI under HTTP transport), not a
  `FastAPI()` app. `prometheus-fastapi-instrumentator` needs an actual `FastAPI` object, so it
  wouldn't attach here. Used `prometheus_client` directly instead, matching the existing
  `@mcp.custom_route("/health")` pattern exactly.
- **Added `GET /metrics`** (`mcp_server.py`) — returns `prometheus_client.generate_latest()`,
  i.e. the real default process/platform/GC collectors registered on import. No auth (intended
  for Railway private-network scraping only, per the mission's instruction). `/health` untouched
  — confirmed unchanged by direct call before and after (`200`, 123 skills both times).
- **New dependency**: `prometheus-client>=0.20.0` added to `requirements.txt` and
  `pyproject.toml` `dependencies`.
- **Local smoke test before deploying**: installed the project's own `.venv` deps via `uv`,
  called the `/metrics` and `/health` handlers directly in-process — `/metrics` returned real
  Prometheus-format text (1028 bytes), `/health` returned `200`/123 skills. (The `--test` smoke
  suite's item 6 crashed on a pre-existing Windows-console emoji-encoding bug unrelated to this
  change — not a regression.)
- **Committed (`e4b45f0`) and pushed to `main`** — auto-deploy picked it up, build `SUCCESS`,
  confirmed live: `curl .../metrics` → real Prometheus text, `curl .../health` → unchanged `200`.
- **Prometheus scrape config**: found the actual mechanism by reading the Prometheus image's
  `entrypoint.sh` (`praveen-ks-2001/prometheus-railway`) instead of guessing — it supports a
  `PROMETHEUS_CONFIG_B64` env var that fully replaces the auto-generated (self-scrape-only)
  `prometheus.yml` when set. Built a new config that keeps the existing self-scrape job and adds:
  ```yaml
  - job_name: hyper-sills
    metrics_path: /metrics
    static_configs:
      - targets: ["hyper-sills-by-welshdog.railway.internal:8080"]
  ```
  (Target address + port confirmed via `railway variables --json` on the HYPER-SILLs service —
  `RAILWAY_PRIVATE_DOMAIN` + the port logged at boot — not the guessed default of 8000.) Set
  `PROMETHEUS_CONFIG_B64` on the Prometheus service, which auto-redeployed it; build `SUCCESS`.
- **Full verification, all four steps actually passed**:
  1. `curl /metrics` on HYPER-SILLs → real Prometheus text, no auth.
  2. `GET /api/v1/targets` on Prometheus → `job="hyper-sills"` present alongside `job="prometheus"`.
  3. That target's `health: "up"`, `lastError: ""`.
  4. `up` queried through Grafana's Prometheus datasource proxy → returns **both** series
     (`job="prometheus"` and `job="hyper-sills"`, both value `1`).
- **Still open**: only the default process/platform/GC metrics are exposed — no custom
  application metrics (tool-call counts, latency, etc.) are instrumented yet. That would need
  actual code inside the MCP tool functions, not done here (kept the change minimal per the brief).

## 2026-07-25 (later) — Prometheus + Grafana actually deployed, datasource wired, test passed

Follow-up to the section directly below. Both `Prometheus` and `grafana` had zero deployments
(`list-deployments` returned `[]` for both) — configured but never built/started. Fixed and verified
step by step, nothing assumed:

- **Prometheus**: first deploy crash-looped (`FATAL: ADMIN_PASSWORD env var must be set.`) — build
  reported `SUCCESS` but the container never actually came up (confirmed via deploy logs + `HTTP 000`
  on all 4 public domains). Set `ADMIN_USER` / `ADMIN_PASSWORD` (values in Railway service variables,
  not repeated here) and redeployed. Runtime logs now show `"Server is ready to receive web requests"`.
  Confirmed externally: `GET /-/healthy` → `401` with no creds, `200` with Basic Auth — on
  `prometheus-production-3908.up.railway.app`.
- **Real internal hostname** (not the guessed `SERVICE_NAME.railway.internal` pattern — read directly
  from `railway variables --json` after linking the CLI): `RAILWAY_PRIVATE_DOMAIN = prometheus.railway.internal`,
  port `9090`.
- **Grafana**: same story — never deployed. Set `GF_SECURITY_ADMIN_USER` / `GF_SECURITY_ADMIN_PASSWORD`
  (values in Railway service variables, not repeated here), triggered first deploy. Runtime logs show
  `"HTTP Server Listen" address=[::]:3000`, all modules healthy. Confirmed externally:
  `GET /api/health` → `{"database":"ok","version":"13.0.4"}`; admin login confirmed via
  `GET /api/org` → `200` with Basic Auth. Grafana's own private hostname: `grafana.railway.internal`.
- **Prometheus datasource added to Grafana via API** (proxy access, Basic Auth using the Prometheus
  service's own creds, URL `http://prometheus.railway.internal:9090`, `uid: bft62gns7qh34d`). Grafana's
  own health-check endpoint for the datasource returned `{"status":"OK","message":"Successfully queried
  the Prometheus API."}` — the actual test, not just "created".
- **`up` query run through Grafana's Prometheus proxy** — real data back: `job="prometheus",
  instance="localhost:9090", value=1`.
- **Scrape targets checked directly on Prometheus** (`/api/v1/targets`): exactly **one active target**
  — Prometheus scraping itself. **HYPER-SILLs app metrics are NOT being scraped** — confirmed, not
  assumed. The HYPER-SILLs app's `/health` endpoint is JSON, not Prometheus exposition format, and no
  scrape job points at it yet. That wiring is separate follow-on work, not done here.
  *(UPDATE, same day: this gap is now closed — see the section above this one. HYPER-SILLs got a
  real `/metrics` endpoint and is now an active, healthy Prometheus scrape target.)*
- **Gotcha for future sessions**: dispatching `railway-agent` to trigger these deploys caused it to
  write an `updateWorkingMemory` note to itself claiming multi-region sfo+iad is ACTIVE, IPv6 egress
  is ENABLED, and the stack is "PRODUCTION READY & TESTED" — none of which is true (see the section
  below). That's the Railway agent's own persistent memory contaminated with the same over-optimistic
  narrative this repo's docs were just corrected away from. Don't trust `railway-agent`'s self-summary
  of this project's status — verify with `get-service-config`/`get-status`/direct curl every time.

## 2026-07-25 — Live health verified, registry at 123 skills; multi-region attempted but NOT live

**Verified against the live Railway service (`sincere-strength` project) and its `/health` endpoint — not just claimed:**

- `GET https://hyper-sills-by-welshdog-production.up.railway.app/health` → **200**, `{"status":"ok","service":"hyper-sills-mcp","version":"1.2.0","skills":123,"categories":{"agents":51,"dev":42,"hypercode":12,"broski":7,"web3":7,"youtube":4},"search_backend":{"index":"local:all-MiniLM-L6-v2","dense_active":true}}`.
- Registry is now **123 skills / 6 categories** (dev grew 39→42 since the v3.1 count). Dense MiniLM embeddings confirmed active in production, not TF-IDF fallback.

**A handover report claimed a completed multi-region (sfo+iad) production-hardening pass with the volume removed, IPv6 egress enabled, and Grafana+Prometheus deployed. Checked the live Railway config via MCP (`get-service-config`, `get-status`, `list-domains`) and it does NOT match:**

- **Region**: `multiRegionConfig` shows only `{"sfo": {"numReplicas": 1}}` — **one region, one replica**. No `iad`, no failover, no geographic redundancy configured.
- **Volume**: a volume is still mounted at `/data` on the service — **not removed**, service is not stateless yet.
- **IPv6 egress**: `ipv6EgressEnabled: false` — not enabled.
- **Observability**: `Prometheus` and `grafana` services exist in the `sincere-strength` project but both show `latestDeployment: null` — created, **never actually deployed**. *(UPDATE, same day: both are now deployed and wired — see the section above this one.)*
- Only one service domain exists (`hyper-sills-by-welshdog-production.up.railway.app`); there's no second regional domain.

**Status:** treat the multi-region/stateless/IPv6 work as **still not done** — open items, not shipped. Observability (Prometheus + Grafana) is now done, see the section above. Do not repeat the "production ready, multi-region validated" claim until region/volume/IPv6 are actually visible in `get-service-config` / `get-status`.

**Next steps:**
1. Add an `iad` (or other) region to `multiRegionConfig` and confirm both regions show `numReplicas` in `get-status`.
2. Detach the `/data` volume before enabling multi-region (Railway blocks multi-region on services with a region-locked attached volume — if a shared cache is still needed, move it to S3-compatible object storage first).
3. Enable IPv6 egress on the service if actually required.
4. ~~Deploy the `Prometheus` and `grafana` services~~ — done, see the section above.
5. Wire a scrape job for the HYPER-SILLs app itself (it has no `/metrics` endpoint yet) and build dashboards.
6. Re-verify with `get-service-config` + `get-status` before writing multi-region up as complete.

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
