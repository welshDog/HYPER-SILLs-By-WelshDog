# HS-060 — 🐳 FLEET ADMIRAL — Container Stack Reference

**Category:** dev
**Version:** 1.0

> *"~30 containers, grouped by profile. Know what's a daemon vs on-demand."*

---

## 🎯 What It Does

A grouped reference of the HyperCode V2.4 container fleet by compose profile, so
an AI brings up the right set and never counts on-demand one-offs as "down".

## 🌍 Why It Exists

A "52% error rate" panic was once just stopped on-demand orphans the roster
counted as down services. Knowing daemon vs on-demand prevents false alarms.

## ⚙️ How To Use

Paste before any `up`/`ps`/health work. Always launch via `hyperlaunch.ps1`
(the canonical 4-file set), never raw compose.

---

## 📋 THE PROMPT

```
HyperCode V2.4 container fleet (28 compose files; bring up via hyperlaunch.ps1):

Always-on (no profile): hypercode-core, postgres, redis, hypercode-ollama,
  celery-worker, registry, hyperhealth-api + the broski-economy consumer (own project).
Profiles:
  agents       → crew-orchestrator, mcp-server, dashboard, safety-shepherd, specialists, socket-proxies
  discord      → broski-bot
  brain-agents → agent-hyper-brain-core/mcp-bridge/focus-tracker (:3301-3303)
  observability→ prometheus, grafana, loki, tempo, pyroscope, exporters
  nemoclaw     → nemoclaw-agent (:8099)
On-demand (compose run, NOT daemons): project-strategist, one-shot obsidian-sync.

Rules:
  - `hyperlaunch.ps1 up -d` (4 files always). NEVER pass agents.yml (it's included).
  - On-demand orphans aren't "down" — `docker rm` exited debris before judging health.
```

## ✅ Example

> `hyperlaunch.ps1 --profile agents up -d` → orchestrator + dashboard +
> safety-shepherd come up together; project-strategist stays off (on-demand).

## 🔗 Related Skills

[[PORT_NETWORK_MAP_v1]] · [[DEV_COMMANDS_CHEAT_SHEET_v1]] · [[ARCHITECTURE_QUICK_REF_v1]]
