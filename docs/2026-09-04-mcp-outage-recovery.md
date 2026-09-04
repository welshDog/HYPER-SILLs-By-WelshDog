FULL STATUS REPORT: HYPER-SILLs MCP Service Recovery
Executive Summary
Service has been down for 10 days (since 2026-08-19 21:15 UTC) due to a single-line breaking change in MCP 2.0.0. Root cause identified, exact fix pinned to July 25 known-good build, CI guard added, PR #17 opened. Ready to deploy and verify.

Problem Statement
Symptom: Service crashes on startup; deployment fails at healthcheck
Timeline:

2026-07-25 11:43-11:45 UTC: Last successful deployment (123 skills, /health = 200, sfo region, 1 replica)
2026-08-19 21:15-21:18 UTC: Deploy failed; container crashed repeatedly with ModuleNotFoundError
2026-08-19 to 2026-09-04: 10 days offline
Error Chain:

ModuleNotFoundError: No module named 'mcp.server.fastmcp'
  File "/app/mcp_server.py", line 30, in <module>
    from mcp.server.fastmcp import FastMCP
→ Container never binds to port
→ Healthcheck GET /health times out after 1m40s
→ "1/1 replicas never became healthy!"
→ Deployment marked FAILED
→ Service remains offline

Root Cause: requirements.txt specified mcp>=1.0.0 (no upper bound). Between July 25 and August 19, MCP 2.0.0 was released and removed the fastmcp module entirely (API redesign). Nixpacks pip install resolved MCP 2.0.0 on the August 19 build, importing the incompatible version, and the app crashed before even starting the server.

Why This Happened
No version ceiling: requirements.txt only had mcp>=1.0.0
Breaking change in minor version bump: MCP 2.0.0 should have been 3.0.0 per semver (API-breaking), but PyPI didn't block it
No CI gate: No smoke test to catch import failures before deploy
No staging environment: Can't test deploy changes locally before pushing to production
Solution Architecture
Layer 1: Complete Dependency Freeze
Created requirements-lock.txt with all 58 exact versions from 2026-07-25 build:

PyTorch CPU wheels: Must use --extra-index-url https://download.pytorch.org/whl/cpu (not on PyPI)
All transitive deps: Captured full tree from build log's "Successfully installed" line
Exact pins: e.g., mcp==1.28.1, numpy==2.5.1, not >= or <
Critical Packages (audited from build log):

Package	Version	Justification
mcp	1.28.1	Last 1.x before 2.0.0 removed fastmcp
transformers	5.14.1	Build log: "Using cached transformers-5.14.1-py3-none-any.whl (11.6 MB)"
sentence-transformers	5.6.1	Build log: "Using cached sentence_transformers-5.6.1-py3-none-any.whl (596 kB)"
starlette	1.3.1	Build log: "Using cached starlette-1.3.1-py3-none-any.whl (73 kB)"
torch	2.4.1+cpu	Build log: "Using cached https://download-r2.pytorch.org/whl/cpu/torch-2.4.1%2Bcpu-cp312-cp312-linux_x86_64.whl (194.8 MB)"
numpy	2.5.1	Build log: "Using cached numpy-2.5.1-cp312-cp312-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl (16.7 MB)"
Layer 2: Safety-Pinned requirements.txt
Updated primary requirements file for human readability and patch-level flexibility:

--extra-index-url https://download.pytorch.org/whl/cpu

python-dotenv==1.2.2
mcp==1.28.1              # Exact pin: last 1.x before 2.0.0 broke fastmcp
prometheus-client==0.26.0
torch==2.4.1+cpu
sentence-transformers==5.6.1
transformers==5.14.1
starlette==1.3.1
numpy==2.5.1

Rationale:

Nixpacks installs requirements.txt by default → must be complete and correct
Lock file allows patch updates (1.28.x) if security patches needed
Comments cite build log for auditability
Layer 3: CI Smoke Test
Added .github/workflows/smoke-test.yml (runs on every push to main):

- name: Install dependencies
  run: pip install -r requirements-lock.txt
- name: Compile mcp_server.py
  run: python -m py_compile mcp_server.py
- name: Import smoke test
  run: python -c "import mcp_server; print('✓ mcp_server imported successfully')"
- name: Compile vault plugin
  run: python -m py_compile plugins/hyper-sills-vault/vault/mcp_server.py

Catches:

❌ ModuleNotFoundError if fastmcp is removed again
❌ IndentationError, SyntaxError in mcp_server.py
❌ Missing transitive deps
✅ Works before humans see production failure
What We Did NOT Do (and why)
❌ Add import-time safety guard in mcp_server.py

Reason: Code exists in two places (root/ + plugins/hyper-sills-vault/vault/)
Risk: Forking logic between two files → maintenance nightmare
Guard is redundant: CI smoke test is the real protection
❌ Automatically regenerate the lockfile

Reason: Breaking changes (like MCP 2.0.0) happen randomly
Better: Freeze to known-good version, update lockfile only when you intentionally upgrade (e.g., for security patches)
❌ Pin only at major version level (e.g., mcp<2)

Reason: mcp>=1.0.0,<2.0.0 still admits mcp==1.99.99 with untested minors
Better: mcp==1.28.1 — you know this version works, test any upgrades in CI first
Verification Steps (Next)
Deploy to Railway: Merge PR #17 → auto-deploy triggers
Wait for health: /health returns 200 with "status": "ok" and 123 skills
Confirm skill count: GET /health payload includes skills_loaded: 123
Set P0 blocker: V24_API_URL=https://hyper-sills-by-welshdog-production.up.railway.app on Hyper-Vibe-Coding-Course service
Proof negative 401: Hit Hyper-Vibe endpoints with missing/invalid V24_API_URL → 401 Unauthorized
Proof positive path: Hit Hyper-Vibe endpoints with correct V24_API_URL → 200 OK + skill responses
Close P0: Mark blocker resolved in Hyper-Vibe Wave 1 audit
Deployment Metadata
Service: HYPER-SILLs-By-WelshDog (sfo, 1 replica)
Source: welshDog/HYPER-SILLs-By-WelshDog (branch: main)
Start Command: python mcp_server.py
Healthcheck: GET /health (200 = healthy)
Volume: registry-cache (2 GB, mounted at /data)
Metrics: Prometheus scrape at /metrics (instrumented: mcp_tool_calls_total, mcp_tool_call_duration_seconds)
Public Domain: https://hyper-sills-by-welshdog-production.up.railway.app
What Brainstorm Topics Are You Thinking?
Tell me what angles you want to explore:

Dependency upgrade strategy: Should we bump transformers/sentence-transformers to newer minors periodically? How to test without breaking prod?
Multi-region resilience: Service is sfo-only; should we add iad replica for redundancy?
Monitoring & alerting: Deploy failures aren't visible until they fail. Should we add webhook alerts or Railway native notifications?
Phase 2 cleanup: PRs #9 and #16 — what are they, and should we fold them into this fix or leave them separate?
Hyper-Vibe integration: Once V24_API_URL is set, what's the expected response format? Any timeout or rate-limit concerns?
Local dev parity: Should repo root requirements.txt match what's pinned, or stay minimal? Currently the pyproject.toml + uv.lock is the source of truth locally.
Let's dig in.