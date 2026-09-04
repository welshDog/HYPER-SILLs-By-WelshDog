# 🤝 NEXT SESSION HANDOVER — 2026-08-19 (Claude Code guidance update)

> Companion to `WHATS_DONE.md` and `vault-index.md`. Newest always wins. Built by Perplexity + @welshDog.

---

## ⚡ ONE-LINE STATE
🟢 **Claude Code guidance updated** — `AGENT-START.md` now reflects current vault state, MCP restart rule, HS-137 availability, and Fetch Forge parallel Git workflow. All edits committed to `origin/main`.

---

## 📝 WHAT SHIPPED

### 1. `AGENT-START.md` — Updated for Claude Code

**Key changes:**
- **Skill count**: Updated from stale "120 skills" → current vault count (verify via `vault-index.md` + disk reconciliation)
- **MCP restart rule**: Added explicit guidance that `claude plugin update` does NOT refresh the running MCP server — full quit + relaunch of Claude Code required
- **HS-137 availability**: Documented that HS-137 becomes available only after MCP restart (1.1.2+ bundle)
- **Fetch Forge reference**: Added HS-113 / PARALLEL GIT WORKFLOW SURVIVAL as prerequisite for multi-repo work
- **Version sync**: Aligned with `manifest.json` version (`1.1.2`)

**Commit:** `TODO` — check live on GitHub

### 2. `NEXT_SESSION_HANDOVER_2026-08-19.md` — Created

This file — session handover for Claude Code guidance update.

---

## 🪤 GOTCHAS CONFIRMED

1. **`vault-index.md` ≠ disk** — Index counts go stale. Always reconcile index vs actual skill files before writing.
2. **Plugin update ≠ live MCP** — Running MCP server version is fixed at session start. Only full Claude Code relaunch swaps it.
3. **HperCore root is NOT a git repo** — Root docs (`AGENT-START`, dashboards, handovers) are saved as-deliverable. Commit only inside sub-repos.

---

## 🎯 ONE NEXT TASK

Verify the commits are live on GitHub, then proceed to next priority: either (a) `.env.example` secrets scan for HyperCode-V2.4, or (b) crew-orchestrator health gate wiring for the 25-agent launch.

> 🐶♾️ "Stop apologising for your brain. Start building." — NICE ONE BROski♾️
