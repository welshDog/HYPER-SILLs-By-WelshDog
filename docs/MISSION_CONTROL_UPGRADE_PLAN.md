# 🎮 Mission Control Upgrade Plan
> Built by welshDog + Perplexity AI — 2026-06-07
> Stop apologising for your brain. Start building.

---

## Current State

| What | Status |
|---|---|
| Catch Stragglers overlay | ✅ LIVE — commits 00aa770, ceadad2, c5b36c2 |
| Express API + React panel base | ✅ EXISTS |
| CatchStragglers.jsx | ✅ EXISTS — not yet wired into main panel |
| catchstragglers router (FastAPI) | ❌ Not registered in main.py |
| DISCORD_BOT_TOKEN (Vercel) | ❌ Not added to env vars |
| mcevents event sourcing | ❌ TODO |
| Live dashboard UI panels | ❌ TODO |

---

## Build Order (ranked by impact)

### ⚡ Phase 1 — Wire What Exists (~90 min, 1 session)
Quick wins. Connect the pieces that are already built.

1. Mount `CatchStragglers.jsx` into the Mission Control main panel
2. Register `catchstragglers` router in FastAPI `main.py`
3. Add `DISCORD_BOT_TOKEN` to Vercel env vars (do in dashboard — never commit)
4. Smoke test: send a real DM via the panel, confirm delivery

**Claude Code boot prompt for Phase 1:**
```
Hey Claude. New session. Here's my context:

Project: WelshDog-Mission-Control
Goal today: Wire Phase 1 — connect existing pieces into 
            working Mission Control dashboard
Output I need:
  1) CatchStragglers.jsx mounted in main React panel
  2) catchstragglers router registered in FastAPI main.py
  3) DISCORD_BOT_TOKEN confirmed in Vercel env vars
  4) Everything pushed to GitHub

Stack: Express API, React frontend (Vite patterns)
Sacred rules:
  - DISCORD_BOT_TOKEN in .env ONLY — never committed
  - broski-bot: discord.py==2.4.0
  - Bot entrypoint: python -u -m cogs.bot (NEVER python main.py)
  - npm run dev:frontend (NEVER npm run dev)
  - git fetch origin before any push

DO NOT touch: .env files, running containers, HyperCode stack
Read CLAUDE.md and WHATSDONE.md before suggesting anything.

CatchStragglers.jsx exists — just needs wiring into main panel.
Commits already live: 00aa770, ceadad2, c5b36c2

Split into:
1) Claude Code tasks (file edits, routing, git)
2) Vercel env tasks (I do these in dashboard)
3) Decisions only I can make

Numbered checklist. Max 5 items. No waffle.
```

---

### 🏗️ Phase 2 — mcevents Event Sourcing (~2 hrs, 1 session)

Every action in your ecosystem emits a stored, replayable event.

**Event examples:**
```json
{ "type": "straggler_dm_sent", "userId": "...", "timestamp": "...", "channel": "discord" }
{ "type": "payment_received", "amount": 49, "tier": "pro", "userId": "..." }
{ "type": "container_health_change", "name": "github-sync", "status": "healthy" }
```

**Why it matters:**
- Replay any moment in your ecosystem
- Full audit trail
- Powers all live dashboard panels from a single stream
- Foundation for agent observability

**Claude Code boot prompt for Phase 2:**
```
Hey Claude. New session.

Project: WelshDog-Mission-Control
Goal today: Build mcevents event sourcing foundation
Output I need:
  1) mcevents table/store — append-only event log
  2) emit() helper — callable from any service
  3) At minimum: straggler_dm_sent + container_health_change events wired
  4) API endpoint: GET /mcevents/recent (last 20 events)
  5) Everything pushed to GitHub

Sacred rules apply. apply_migration only — never db push.
Read CLAUDE.md and WHATSDONE.md first.
```

---

### 🎮 Phase 3 — Live Dashboard UI (~2 hrs, 1 session)

Four WebSocket-powered panels. Updates every 5 seconds.

```
┌─────────────────┬──────────────────┐
│  🐳 CONTAINERS  │  💰 REVENUE      │
│  41/41 healthy  │  £XX today       │
│  Live status    │  Last payment    │
├─────────────────┼──────────────────┤
│  🎓 STRAGGLERS  │  ⚡ LIVE EVENTS  │
│  3 at risk      │  mcevents stream │
│  DM sent: 12    │  Last 10 events  │
└─────────────────┴──────────────────┘
```

**Neurodivergent-first design:**
- Focus Mode toggle — one panel only, zero clutter
- One big number per panel
- Green / Amber / Red only — no guessing
- Zero auto-play animations unless enabled
- High contrast, chunked layout

---

### 💻 Phase 4 — IDE Integration (after Phase 1-3 are live)

- Connect hyper-agents-ide to Mission Control event stream
- IDE watches mcevents — surfaces relevant alerts inline
- Agent health visible without leaving the editor
- Claude Code sessions can emit events into the stream

---

## Sacred Rules (never break in this repo)

| Rule | Why |
|---|---|
| `DISCORD_BOT_TOKEN` in `.env` only | Never commit secrets |
| `discord.py==2.4.0` | Never py-cord |
| Bot entrypoint: `python -u -m cogs.bot` | Never `python main.py` |
| `npm run dev:frontend` | Never `npm run dev` |
| `git fetch origin` before any push | Auto-commits are running |
| `docker-ce-cli` only | Never docker.io |

---

## Session End Checklist

- [ ] All changes pushed to GitHub
- [ ] `NEXT_SESSION_HANDOVER_DATE.md` created and pushed
- [ ] `WHATSDONE.md` updated
- [ ] Tell Bro the first task for next session (one sentence)
- [ ] Celebrate the wins 🎉

---

*Built by welshDog + Perplexity AI · Llanelli, Wales 🏴󠁧󠁢󠁷󠁬󠁳󠁥*
*Stop apologising for your brain. Start building.*
