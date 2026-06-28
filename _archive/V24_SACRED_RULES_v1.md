# HS-031 — 🔴 V2.4 SACRED RULES — V2.4 Sacred Rules (20 Rules)
**Category:** hypercode
**Version:** 1.0

## What it Does
20 non-negotiable rules for working inside HyperCode-V2.4. These are load-bearing — break one and you break the stack.

## When To Use
- Before ANY commit to HyperCode-V2.4
- When an AI suggests something that feels wrong
- Code review checklist for V2.4 changes

## THE RULES
```
V2.4 SACRED RULES — never debate, never break:

✔ docker-ce-cli          — NEVER docker.io for socket agents
✔ from app.X import Y    — NEVER from backend.app.X
✔ FastAPI public routes   — BEFORE auth-gated routes
✔ Stripe webhook          — rate-limit EXEMPT always (NEVER add rate limiting)
✔ data-net + obs-net      — internal: true, never external
✔ .env files              — NEVER committed to git
✔ Commits                 — feat: fix: docs: chore: only
✔ Trivy target            — 0 CRITICAL per image
✔ Import style            — absolute imports, sys.path.insert at top
✔ Python indent           — 4 spaces, NEVER 3, NEVER mixed
✔ Redis DB split          — DB 1 = cache, DB 2 = rate limits. NEVER mix.
✔ hypercore healthcheck   — use localhost NOT 127.0.0.1 (IPv6 fix)
✔ Supabase ↔ V2.4         — NEVER merge schemas
✔ Guardian moderation     — ban/kick NEVER fully autonomous (P3c = veto-gated only)
✔ NemoClaw/Guardian       — bot detects, Core decides + persists, bot renders (One Door)
✔ Prometheus config       — monitoring/prometheus/prometheus.yml = ACTIVE. Root = STALE
✔ minio                   — on both data-net AND obs-net — correct, intentional
✔ Alembic                 — up to 015. If missing: alembic stamp <prev> → upgrade head
✔ Socket-proxy split      — main=read-only, healer proxy=write (CONTAINERS+POST+PING)
✔ Security headers        — frontend/vercel.json (NOT repo root)
```

## Related Skills
- HS-030 HyperFocus Master Constitution
- HS-032 Course Sacred Rules
- HS-048 Preflight Checks System

---
*Source: HyperCode-V2.4 CLAUDE.md §6a | Category: hypercode/*
