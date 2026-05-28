# HS-038 — 🛡️ PHASE WARDEN — Guardian Bot Phase Map (P1→P3c)

> *"Server Guardian: the autonomous Discord mod system. Know every phase before touching it."*

---

## 🎯 What It Does
The complete phase map for the HyperFocus Server Guardian — the Discord auto-moderation system. P1 through P3c, what's live, what's built, what's pending.

## 🌍 Why It Exists
Guardian handles real bans and real users. Touching it without knowing the phase map = risk of autonomous bans or broken moderation.

## ⚙️ How To Use
1. Paste before any Discord bot or moderation work
2. AI understands the One Door pattern and phase boundaries

---

## 📋 THE PROMPT

```
You are working on Server Guardian — HyperFocus Discord auto-moderation. Know these phases:

P1 REACTIVE — LIVE ✅
  auto-role on join + /hyperfocus_setup (admin, idempotent)

P2 DIGEST — LIVE ✅
  Weekly DM to Lyndz — Core aggregates 7 days from Postgres
  Command: /digest (admin)

P3a AUTO-MOD — LIVE ✅
  Structural spam detection → reversible timeout
  All actions audited to mod_actions table
  NEVER permanent without human review

P3b RAID LOCKDOWN — LIVE ✅
  Join-flood detection → channel lock
  Restart-safe reconciler
  Commands: /raid-unlock /raid-status

P3c VETO-BAN — BUILT (smoke test pending) 🛡️
  3 strikes / 7 days → DM + mod-log buttons
  1-hour veto window
  BAN ONLY on explicit APPROVE click
  Silence = downgrade to long timeout (NEVER auto-ban)

ONE DOOR PATTERN:
  Bot detects → Core decides + persists → Bot renders
  ALL actions go through Core POST /api/v1/discord/actions
  NEVER bot-direct actions bypassing Core

SACRED RULE:
  ban/kick NEVER fully autonomous — P3c = veto-gated ONLY

[INPUT: describe the Guardian/moderation task]
```

---

## 🔗 Related Skills
- HS-068 — THE CONDUCTOR (Orchestrator Pattern)
- HS-077 — CONSENT GUARDIAN (User Agency Approval Gate)

---
*HYPER-SKILLs Vault — welshDog 🐕🏴󠁧󠁢󠁷󠁬󠁳󠁧⚡*