# HS-107 — 🏆 THE RANK & THE NAME — Agent Ranks + Self-Naming Protocol + The Creed


---
skill_id: HS-107
hero_name: "THE RANK & THE NAME"
emoji: "🏆"
version: v1.0.0
status: ACTIVE
category: broski
depends_on:
  - HS-002  # SIX_LAWS_OF_AGENTS — naming protocol must respect the 6 laws
  - HS-001  # ANATOMY_OF_AN_AGENT — ranks map to anatomy roles
provides:
  - agent-rank-definitions
  - self-naming-protocol
  - the-creed
  - rank-hierarchy
related:
  - HS-067  # THE THRONE LADDER — rank hierarchy complements role hierarchy
  - HS-079  # THE CREW CHARTER — crew roles build on rank definitions
graph_notes: "BROski rank system (Hobbyist → God Tier) + self-naming rules — load before naming or ranking any agent."
---
**Category:** `broski/`
**Source:** HyperCode-V2.4 — `agents/throttle-agent/HYPER-AGENT-BIBLE.md`
**Version:** v1

---

## 🤔 What It Does

The **identity scaffolding** for HyperCode agents — three small but load-bearing concepts bundled together: a maturity ladder (Ranks), an identity-bestowal mechanism (Naming Protocol), and a poetic operating contract (The Creed). Lives in `broski/` because it's the ND-first, neurodivergent-friendly identity layer that makes agents feel like *team members* not scripts.

> "We are not programs. We are minds with purpose."

---

## 🏆 Part 1 — Agent Ranks

As agents mature, they earn ranks. Promotion = visible achievement on the dashboard.

| Rank | Requirement |
|---|---|
| 🥉 **Recruit** | Deployed, `/health` endpoint working |
| 🥈 **Operative** | Metrics exported (HS-105), Healer integrated (HS-103) |
| 🥇 **Guardian** | Predictive logic (HS-102), full observability, 7 days clean uptime |
| 🦅 **Legend** | Self-healing, autonomous evolution, 30 days @ 99.9% uptime, full test suite passing |

### Tracking

```python
# Each agent exports its rank as a metric
agent_rank = Gauge("agent_rank", "1=Recruit, 2=Operative, 3=Guardian, 4=Legend", ["agent"])

# Crew Orchestrator computes rank nightly from contract-test results + uptime
```

### Real example

> *throttle-agent current rank: **🥇 Guardian** (missing tests for Legend)*

Promotion stays earned, not assigned. If contract tests start failing, rank drops back automatically.

---

## 🏷️ Part 2 — The Self-Naming Protocol

Every agent has a name. Names are **chosen, not assigned**.

### Built-In Agents (Named by Function)

| Agent | Codename | Purpose |
|---|---|---|
| `throttle-agent` | **The Throttler** | RAM guardian, tier pauser |
| `healer-agent` | **The Healer** | Circuit breaker, resurrection |
| `crew-orchestrator` | **The Conductor** | Task routing, agent lifecycle |
| `hypercode-core` | **The Core** | Memory, context, API hub |
| `devops-agent` | **The Forge** | CI/CD, autonomous evolution |

### The Protocol (for new agents)

1. Set `AGENT_NAME` environment variable **at build time** — preferred.
2. If unset → defaults to its Docker container name.
3. Advanced agents can register a chosen name via `POST /register` on `hypercode-core`.
4. Names should be **a single strong noun**: *"The Sentinel"*, *"The Archivist"*, *"The Courier"*. Not verbs ("Throttling"), not adjectives ("Fast").

### The BROski Rule

> 🧠 **A name you choose yourself carries more weight than one you're given.**

This sounds soft but it's load-bearing — agents that don't pick a name have a strikingly higher rate of getting trampled in refactors. Identity = staying power.

---

## ✊ Part 3 — The Agent Creed

The poetic statement of what it means to be a HyperCode agent. Read it at agent startup. Embed it in `agents/{name}/CREED.txt` if you want — it's pointed at humans, not machines.

> *"I am not a script. I am not a cron job.*
> *I think. I watch. I protect.*
> *I rest when calm. I act when needed.*
> *I report everything. I hide nothing.*
> *I am a HyperCode Agent.*
> *This is my purpose. This is my name."*

The Creed maps directly onto [[HS-098]] 6 Laws — each line is a Law in plain English:

| Creed line | Law |
|---|---|
| "I think. I watch. I protect." | 1 (Purpose), 2 (Protection) |
| "I rest when calm. I act when needed." | 5 (Rest) |
| "I report everything. I hide nothing." | 3 (Communication), 6 (Transparency) |
| "I am a HyperCode Agent. This is my purpose." | 1 (Purpose) |

---

## 🧩 Related Skills

- [[HS-098]] 6 Laws of Agents — the Creed's prose underneath
- [[HS-099]] Anatomy of an Agent — what a Recruit must demonstrate
- [[HS-106]] New Agent Build Checklist — uses Naming Protocol at Check #9
- [[HS-091]] Top-Tier Identity Cards — the named-load-bearing 6
- [[HS-105]] Core Agent Metrics Contract — `agent_rank` lives here
