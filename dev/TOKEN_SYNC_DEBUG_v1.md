# 🔑 DS-030 — TOKEN SYNC DEBUG — Fix Broken Auth Tokens Without Panicking

---
skill_id: DS-030
hero_name: "TOKEN SYNC DEBUG"
emoji: "🔑"
version: v1.0
category: dev
depends_on:
  - DS-009  # PREFLIGHT_CHECKS_SYSTEM
provides:
  - token-debug-steps
  - auth-sync-protocol
  - env-var-token-fix
related:
  - DS-014  # CROSS_REPO_SYNC
  - DS-018  # OBSIDIAN_GIT_VAULT
  - HS-019  # OBSERVABLE_AGENT_OPERATIONS
graph_notes: "Debug guide for broken tokens — Discord, Stripe, Supabase, GitHub. Never commit secrets, always rotate and re-sync."
---

**Category:** `dev/`
**Version:** v1

## 📋 THE PROMPT
```text
Use skill DS-030 TOKEN SYNC DEBUG. Debug broken [TOKEN_TYPE] token for [SERVICE] — walk through rotation and re-sync.
```
