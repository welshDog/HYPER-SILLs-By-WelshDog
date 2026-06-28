# HS-028 — 📖 SDK PRIMER — HyperAgent SDK Agents README
**Version:** 1.0


---
skill_id: HS-028
hero_name: "SDK PRIMER"
emoji: "📖"
version: v1.0.0
status: ACTIVE
category: agents
depends_on:
  - HS-125  # THE GRAND CODEX — master context gives the 5-repo map SDK sits in
provides:
  - sdk-ecosystem-map
  - agent-interface-standard
  - write-once-deploy-anywhere
related:
  - HS-016  # BRAIN PRIMER — brain sits at same ecosystem layer
  - DS-016  # SDK_PUBLISH_WORKFLOW — publish workflow for SDK changes
  - DS-017  # HYPERAGENT_SDK_PUBLISH_SKILL — SDK publish skill details
graph_notes: "Orientation for HyperAgent-SDK — the shared agent interface standard that connects all 5 ecosystem repos."
---
**Category:** Agents / SDK Architecture
**Rescued From:** [HyperAgent-SDK](https://github.com/welshDog/HyperAgent-SDK) — `.agents/AGENTS.md`

> HyperAgent-SDK is the **shared agent interface standard** for the entire Hyperfocus z0ne ecosystem. Write agents once, deploy anywhere across all 5 repos.

---

## 🏗️ Ecosystem Position

```
HyperCode-V2.4 (backend / wallet authority)
    ↕
Hyper-Vibe-Coding-Course (frontend / earns XP + BROski$)
    ↕
BROskiPets-LLM-dNFT (reads progress → unlocks pets)
    ↕
HyperAgent-SDK (shared agent interface) ⬅️ YOU ARE HERE
    ↕
BROski-Obsidian-Brain (meta-layer / living knowledge vault)
```

---

## 🛠️ Skills Available (Antigravity)

| Skill | Purpose |
|---|---|
| `hyperagent-sdk-publish` | Build, test, version, publish SDK to npm |

---

## 🔧 Tools & Connections

- **npm** — Package publishing target
- **TypeScript / JavaScript** — Primary SDK language
- **Jest** — Test runner
- **GitHub Actions** — CI on PRs
- **HyperCode-V2.4** — Primary consumer (backend)
- **Hyper-Vibe-Coding-Course** — Primary consumer (frontend)

---

## 🚀 Boot Into Hyperfocus Mode

1. Read `CLAUDE.md` — master brain, sacred rules, architecture
2. Read `CLAUDE_CONTEXT.md` — current context snapshot
3. Check `.agents/skills/` — available skills
4. Ask: **"What are we shipping first today?"**

---

## 📜 Sacred Rules (never break)

- Short sentences — no walls of text
- **Bold key info**
- PowerShell first for commands
- Bullet points over paragraphs
- **Add, don't remove** — never break existing interface contracts

---

## 🏆 Major Wins So Far

- Shared agent interface standard defined ✅
- SDK consumed across HyperCode-V2.4 + Course ✅
- SDK publish skill ready ✅

*Rescued from HyperAgent-SDK — HYPER-SKILLs Vault by WelshDog 🐕⚡*
