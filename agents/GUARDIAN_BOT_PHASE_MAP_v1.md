# HS-038 — 🛡️ GUARDIAN BOT PHASE MAP — Guardian Bot Phase Map (P1→P3c)

## What it Does
Complete phase-by-phase map of the Server Guardian Discord auto-manager. Shows what's live, what's built, and how each phase escalates moderation safely.

## When To Use
- Building new Guardian phases
- Debugging Guardian behaviour
- Understanding the escalation ladder before touching mod logic
- Verifying P3c veto-gate is working correctly

## THE PHASE MAP
```
SERVER GUARDIAN PHASE MAP:

P1 — Reactive (LIVE ✅ May 16)
  → auto-role on join
  → /hyperfocus_setup (admin, idempotent layout build)
  → Trigger: member joins server

P2 — Digest (LIVE ✅ May 16)
  → weekly DM to Lyndz
  → Core aggregates 7-day data from Postgres
  → /digest (admin) + weekly auto-DM
  → Trigger: scheduled weekly

P3a — Auto-mod (LIVE ✅ May 16)
  → structural spam detect → reversible timeout
  → all actions audited to mod_actions table
  → NEVER permanent without human review
  → Trigger: message pattern detection

P3b — Raid Lock (LIVE ✅ May 16)
  → join-flood detection → channel lock
  → restart-safe reconciler
  → /raid-unlock /raid-status commands
  → Trigger: join rate threshold exceeded

P3c — Veto-Ban (BUILT ✅, smoke pending)
  → 3 strikes in 7 days → DM + mod-log buttons
  → 1-hour veto window
  → BAN ONLY on explicit APPROVE click
  → Silence = downgrade to long timeout (NEVER auto-ban)
  → Trigger: strike counter hits 3

⚠️ SACRED RULE: ban/kick NEVER fully autonomous
⚠️ P3c = veto-gated only — human must approve
⚠️ One Door: bot detects, Core decides + persists, bot renders

Active cogs (loaded by cogs/bot.py):
  moderation  → passive auto-mod (spam/blocklist → timeout)
  welcome     → passive on-join welcome + auto-role
  digest      → /digest admin + weekly auto-DM
```

## Related Skills
- HS-031 V2.4 Sacred Rules
- HS-085 THE FIVE WARDS Mandatory Agent Guardrails
- HS-077 CONSENT GUARDIAN User Agency Approval Gate

---
*Source: HyperCode-V2.4 CLAUDE.md §7 | Category: agents/*
