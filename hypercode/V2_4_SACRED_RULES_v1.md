# HS-031 — 🔴 V2.4 SACRED RULES — V2.4 Sacred Rules (20 Rules)
**Category:** hypercode
**Version:** 1.0

> *"Never debate. Never break. These are the load-bearing walls of HyperCode V2.4."*

---

## 🎯 What It Does
The complete set of 20 sacred rules for HyperCode-V2.4. Paste into any session working on the core backend to instantly prevent the most common catastrophic mistakes.

## 🌍 Why It Exists
Every rule here was learned the hard way. Breaking any one of them can take down containers, corrupt data, or expose secrets.

## ⚙️ How To Use
1. Paste at start of any V2.4 session
2. AI treats these as hard constraints — not suggestions
3. If AI tries to break one, flag it immediately
problem_keywords:
  - v2.4 rules
  - sacred rules
  - hypercode rules
  - 20 rules

---

## 📋 THE PROMPT

```
You are working on HyperCode-V2.4. Apply ALL of these rules — no exceptions, no debate:

✔ docker-ce-cli — NEVER docker.io for socket agents
✔ from app.X import Y — NEVER from backend.app.X
✔ FastAPI public routes — BEFORE auth-gated routes
✔ Stripe webhook — rate-limit EXEMPT, always (NEVER add rate limiting)
✔ data-net + obs-net — internal: true, never external
✔ .env files — NEVER committed to git
✔ Commits — feat: fix: docs: chore: only
✔ Trivy target — 0 CRITICAL per image
✔ Import style — absolute imports, sys.path.insert at top
✔ Python indent — 4 spaces, NEVER 3, NEVER mixed
✔ Redis DB split — DB 1 = cache, DB 2 = rate limits. NEVER mix.
✔ hypercore healthcheck — use localhost NOT 127.0.0.1 (IPv6 fix)
✔ Supabase ↔ V2.4 — NEVER merge schemas
✔ Guardian moderation — ban/kick NEVER fully autonomous (P3c = veto-gated only)
✔ NemoClaw/Guardian — bot detects, Core decides + persists, bot renders (One Door)
✔ Prometheus config — monitoring/prometheus/prometheus.yml = ACTIVE. Root = STALE
✔ minio — on both data-net AND obs-net — correct, intentional
✔ Alembic — up to 015. If missing: alembic stamp <prev> → upgrade head
✔ Socket-proxy split — main=read-only, healer proxy=write (CONTAINERS+POST+PING)
✔ Security headers — frontend/vercel.json (NOT repo root)

[INPUT: describe the V2.4 task]
```

---

## ✅ Example
**Input:** "Add rate limiting to the Stripe webhook"
**Output:** AI flags: "SACRED RULE: Stripe webhook is rate-limit EXEMPT always — adding rate limiting would break it."

## 🔗 Related Skills
- HS-030 — HyperFocus Master Constitution
- HS-032 — Course Sacred Rules
- HS-037 — Architecture Quick Ref

---
*HYPER-SKILLs Vault — welshDog 🐕🏴󠁧󠁢󠁷󠁬󠁳󠁧⚡*
