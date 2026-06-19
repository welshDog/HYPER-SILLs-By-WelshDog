# HS-064 — ⚡ THE QUICK HAND — Dev Commands Cheat Sheet

**Category:** dev
**Version:** 1.0

> *"The exact commands that actually work in this stack — copy, don't guess."*

---

## 🎯 What It Does

The canonical command set for HyperCode V2.4 + Course dev loops — the ones that
work, with the footguns flagged.

## 🌍 Why It Exists

Wrong command = wasted cycles (raw compose misses files; `npm run dev` is wrong
for the course). One sheet = right first time.

## ⚙️ How To Use

Paste at the start of any hands-on session.

---

## 📋 THE PROMPT

```
HyperCode V2.4 + Course — commands that work:

# Env preflight (V2.4) — ALWAYS before up:
python scripts/env_check.py --core --secrets

# Compose (canonical wrapper — 4-file set; NEVER raw compose):
.\hyperlaunch.ps1 up -d                          # always-on
.\hyperlaunch.ps1 --profile agents up -d         # + agents
.\hyperlaunch.ps1 build <svc> ; .\hyperlaunch.ps1 up -d <svc>   # rebuild+recreate
.\hyperlaunch.ps1 ps | logs -f <svc>

# Core:
pytest backend/tests/ -q
docker exec hypercode-core alembic current        # ALWAYS before numbering a migration
docker exec hypercode-core alembic upgrade head    # alembic dir is volume-mounted
curl http://localhost:8000/health

# Course (repo root):
npm run dev:frontend        # NOT npm run dev
npx tsc --noEmit && npx eslint . && npm run build
npm run test:e2e            # Playwright — use it, never "human must test"

# Git: git fetch before push. NEVER force-push. NEVER --no-verify.
```

## ✅ Example

> Rebuilt core for migration 018 → `hyperlaunch.ps1 build hypercode-core` then
> `up -d hypercode-core` → entrypoint runs `alembic upgrade head` on boot.

## 🔗 Related Skills

[[CONTAINER_STACK_REFERENCE_v1]] · [[PORT_NETWORK_MAP_v1]] · [[DATABASE_SCHEMA_REFERENCE_v1]]
