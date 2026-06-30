# HS-059 — 🗺️ THE CARTOGRAPHER — Complete Ecosystem Inventory

**Category:** hypercode
**Version:** 1.0

> *"Every repo, every purpose, one paste. Know the whole map before you move."*

---

## 🎯 What It Does

The full HyperFocus Zone repo + service inventory — paste it to give an AI instant
awareness of the 5-repo ecosystem and what each part owns.

## 🌍 Why It Exists

Work spans 5 repos. Without the map, an AI edits the wrong repo, duplicates a
feature, or misses that something already exists.

## ⚙️ How To Use

Paste at session start when work touches more than one repo, or when deciding
*where* a feature belongs.
problem_keywords:
  - ecosystem inventory
  - what services exist
  - full map
  - cartographer

---

## 📋 THE PROMPT

```
HyperFocus Zone — 5-repo ecosystem (aggregator root: H:\HYPERFOCUSZONE\HperCore):

| Repo | Owns | Stack |
|---|---|---|
| HyperCode-V2.4 | Core backend, ~30 containers, 9 agents, control plane | Python/FastAPI/Docker/LangGraph/CrewAI |
| Hyper-Vibe-Coding-Course | Course + HyperLabs funnel | Supabase + Vercel + Stripe (TEST) |
| HyperAgent-SDK | npm agent framework @w3lshdog/hyper-agent | TypeScript |
| BROskiPets-LLM-dNFT | Web3 dNFT pet game (Base Sepolia 84532) | Solidity + LLM + wagmi |
| BROski-Obsidian-Brain | Second Brain vault (PARA + GitHub bridge) | Obsidian + Python |

Control plane (HyperCode-V2.4, all live):
  HyperFlow mission graphs · Safety Shepherd (:8096) · Identity Agent +
  governance_ledger (mig 018) · Mission Graph dashboard panel (:8088 /flows).

Sacred: Supabase <-> V2.4 schemas NEVER merge. Each repo has its own CLAUDE.md.
```

## ✅ Example

> "Where does pet rarity logic go?" → `BROskiPets-LLM-dNFT` (web3), surfaced via
> the Course `/pets` page — NOT HyperCode-V2.4 backend.

## 🔗 Related Skills

[[EXTERNAL_INTEGRATIONS_MAP_v1]] · [[ARCHITECTURE_QUICK_REF_v1]] · [[MILESTONE_TRACKER_TEMPLATE_v1]]
