# Deploying HYPER-SILLs MCP Server

Serves all **120 skills** over **streamable-HTTP** so remote hosts (Railway/Render)
and the **Perplexity MCP connector** can discover + call them live.

Verified in a clean venv: `pip install -r requirements.txt` → `python mcp_server.py --http`
→ `GET /health` 200, MCP endpoint at `/mcp`.

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
# -> {"status":"ok","service":"hyper-sills-mcp","skills":120,...}
```

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
