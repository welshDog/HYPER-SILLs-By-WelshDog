# Deploying HYPER-SILLs MCP Server

Serves all **123 skills** over **streamable-HTTP** so remote hosts (Railway/Render)
and the **Perplexity MCP connector** can discover + call them live.

Verified in a clean venv: `pip install -r requirements.txt` → `python mcp_server.py --http`
→ `GET /health` 200, MCP endpoint at `/mcp`.

## Current Production Deployment (verified 2026-07-25)

- **Target**: Railway, project `sincere-strength`, service `HYPER-SILLs-By-WelshDog`.
- **Region**: `sfo` only, 1 replica (`multiRegionConfig: {"sfo": {"numReplicas": 1}}`). No second region is configured — treat any note about `sfo`+`iad` multi-region as an in-progress goal, not a shipped state, until `get-service-config` shows both.
- **Health check path**: `/health` — confirmed live, returns 200 with skill/category counts and search-backend status.
- **Restart policy**: `ON_FAILURE`, max 3 retries (per `railway.json`).
- **HTTPS/TLS**: enabled (standard Railway `*.up.railway.app` domain, `hyper-sills-by-welshdog-production.up.railway.app`).
- **Auto-deploy from `main`**: enabled (service source is `welshDog/HYPER-SILLs-By-WelshDog` on branch `main`).
- **Statelessness**: **not yet true** — the service still has a volume mounted at `/data`. If/when multi-region is actually rolled out, that volume needs to come off first (Railway won't run a region-locked attached volume across multiple regions); if a shared cache is still needed at that point, move it to S3-compatible object storage instead of an attached volume.
- **IPv6 egress**: currently disabled on the service config.
- **Observability**: `Prometheus` and `grafana` services are deployed and live in the same Railway project (both originally had zero deployments and crash-looped on missing admin credentials until those were set). Prometheus is reachable at its public Railway domains behind Basic Auth; internally at `prometheus.railway.internal:9090`. Grafana is reachable at its public Railway domain, `/api/health` returns `{"database":"ok"}`. A Prometheus datasource is wired up in Grafana (proxy access, Basic Auth) and its connection test passes (`"Successfully queried the Prometheus API."`). **HYPER-SILLs app metrics are now scraped**: the app exposes `GET /metrics` (no auth — private-network only), Prometheus's scrape config was updated via its `PROMETHEUS_CONFIG_B64` env var to add a `hyper-sills` job at `hyper-sills-by-welshdog.railway.internal:8080`, and the target shows `health: "up"` with `up{job="hyper-sills"}` queryable from Grafana Explore. Only default process/platform/GC metrics are exposed so far — no custom application metrics (tool-call counts, latency, etc.) yet. Admin credentials for both services are set as Railway environment variables; they are intentionally not written in this file.
- **`/metrics`**: `GET /metrics` on the HYPER-SILLs service itself — Prometheus text format via `prometheus_client`, no auth, mirrors the `/health` route pattern in `mcp_server.py`. Scraped by Prometheus every 15s.

## Files that make this work
- `requirements.txt` — runtime deps (`mcp` pulls starlette + uvicorn + sse-starlette + httpx)
- `Procfile` — `web: python mcp_server.py --http`
- `railway.json` — NIXPACKS builder, start command, `healthcheckPath: /health`
- `.python-version` — pins Python 3.12
- `mcp_server.py --http` — reads `$PORT` (Railway injects it) + `$HOST` (default 0.0.0.0)

## Deploy to Railway (one time)

```bash
# 1. Log in (interactive — opens a browser)
railway login

# 2. From this repo dir, create + link a project
cd HYPER-SILLs-By-WelshDog
railway init                     # name it e.g. hyper-sills-mcp

# 3. Deploy the current directory (no git push needed)
railway up

# 4. Give it a public URL
railway domain                   # prints https://<something>.up.railway.app
```

Railway auto-injects `PORT`; the server binds it and serves `/health` (used as the
healthcheck) and the MCP endpoint at `/mcp`.

### Smoke-test the live deploy
```bash
curl https://<your-domain>.up.railway.app/health
# -> {"status":"ok","service":"hyper-sills-mcp","skills":123,
#     "search_backend":{"index":"local:all-MiniLM-L6-v2",
#                       "query":"local:sentence-transformers","dense_active":true}, ...}
```
`search_backend.dense_active` is the honest tell: `true` = real dense embeddings;
`false` = the server fell back to TF-IDF (the embedding deps didn't install, or the
prebuilt index is missing). The model warms on the first `/mcp` semantic call, so
that one request is slower; everything after is fast.

```bash
curl https://<your-domain>.up.railway.app/metrics
# -> Prometheus text format (python_gc_objects_collected_total, etc.), no auth needed.
```
This is what Prometheus scrapes (job `hyper-sills`, every 15s, over the private network —
see the Observability line above). If this 404s, the deploy predates the `/metrics` route.

## Wire into Perplexity

1. Go to **perplexity.ai/computer/connectors** → add a custom MCP connector.
2. URL: `https://<your-domain>.up.railway.app/mcp`
3. Save. All 6 tools (`search_skills`, `semantic_search`, `load_skill`,
   `get_skill_graph`, `recommend_for_task`, `list_skills_by_category`) are now
   callable from every Perplexity chat.

## Redeploy after changes
```bash
railway up        # local dir, OR
git push          # if you connect the GitHub repo in the Railway dashboard
```

## Notes
- `--sse` flag falls back to the deprecated SSE transport if a host needs it.
- The project is developed with `uv` (see `pyproject.toml` + `uv.lock`);
  `requirements.txt` is only a deploy artifact for pip-based hosts.
- **Dense embeddings on the host:** `requirements.txt` pins CPU-only
  `torch` + `sentence-transformers` so the deployed server runs real semantic
  search (not TF-IDF). This makes the build heavier (~1 GB image) and the first
  semantic query slower (model download + load); trade accepted for sharp search.
  The prebuilt `vector-store/skill_index.json` is committed (un-ignored) so the
  host only embeds the live query, never rebuilds all 123 vectors on boot.
- **Regenerating after editing skills:** edit frontmatter (incl. `problem_keywords`),
  then `python scripts/generate_registry.py` → `python scripts/embed_skills.py`.
  Never hand-edit `skills-registry.json` or `skill_index.json` — they're generated.
