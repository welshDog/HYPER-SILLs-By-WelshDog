# HS-089 — 🗺️ THE GRAND ROSTER — Hyper Agent Roster (22 Confirmed + 5 Expansion)

**Category:** `agents/`
**Source:** HyperCode-V2.4 — `agents/🧬 The Full Confirmed Hyper Agent Roster`
**Version:** v1

---

## 🤔 What It Does

The canonical map of every confirmed agent in the HyperCode V2.0/V2.4 ecosystem — name, path, role, and the 5 "future agents" earmarked for expansion. Use as the lookup table when wiring a new dependency or asking "do we have an agent that already does X?".

> Wider scope than [[HS-079]] (6 specialists) — that one's the Bible's worker crew; this is the full repo-wide roster including infra, meta, and business agents.

---

## ✅ Confirmed Agents (22, live in `agents/`)

| 🤖 Agent | Path | Role |
|---|---|---|
| 🦅 Agent X / Architect | `agents/architect` | Meta-architect — spawns + evolves all agents |
| 🧠 Brain / Memory | `agents/memory` | Cognitive core + cross-session memory |
| 🛠️ DevOps Engineer | `agents/05-devops-engineer` | CI/CD + Evolutionary Pipeline |
| 🩺 Healer | `agents/healer` | Self-healing, crash recovery |
| 🎭 Crew Orchestrator | `agents/crew-orchestrator` | Swarm dispatcher + lifecycle manager |
| 🖥️ Frontend Specialist | `agents/01-frontend-specialist` | React/Next.js UI layer |
| ⚙️ Backend Specialist | `agents/02-backend-specialist` | FastAPI routes + business logic |
| 🗄️ Database Architect | `agents/03-database-architect` | PostgreSQL schema + migrations |
| 🧪 QA Engineer | `agents/04-qa-engineer` | Tests, chaos, coverage |
| 🔐 Security Engineer | `agents/06-security-engineer` | OWASP, secrets, auth |
| 🏛️ System Architect | `agents/07-system-architect` | Big-picture design decisions |
| 📋 Project Strategist | `agents/08-project-strategist` | OKR planning + BROski$ gamification |
| ✍️ Tips Writer | `agents/09-tips-tricks-writer` | Auto-docs, living research paper |
| 💬 BROski Bot | `agents/broski-bot` | Discord + economy manager |
| ⚡ Super Hyper BROski | `agents/super-hyper-broski-agent` | Solo rapid-deploy mega-agent |
| 🐉 NemoClaw | `agents/broski-nemoclaw-agent` *(now `agents/nemoclaw-agent`)* | Wildcard + creative edge cases — code-health "Alive" sidecar, port 8099 |
| 🏭 Agent Factory | `agents/agent-factory` | Spawn-on-demand template engine |
| 🧱 Base Agent | `agents/base-agent` | Universal parent class all agents inherit |
| 🎛️ Dashboard | `agents/dashboard` | Real-time Next.js Mission Control |
| 🚦 Throttle Agent | `agents/throttle-agent` | Rate limiting + cost guards |
| 🏢 Business Agent | `agents/business` | Revenue + BROski$ economy logic |
| 💻 Coder Agent | `agents/coder` | Autonomous code generation |

---

## 🔮 Future Agents (5 — expansion pack)

Flagged by HyperCode docs as the missing squad members. Build slots reserved.

| 🤖 Agent | Purpose |
|---|---|
| 🎨 Creative Agent | AI art gen, 3D print prep, HyperFocus Zone visuals |
| 🔬 Research Agent | Live web intelligence scraping, feeds living docs |
| 💰 Revenue Agent | BROski$ economy monitor, monetisation plays |
| 🌍 Community Agent | GitHub issues auto-triage, open-source contributions |
| ⚛️ Quantum Scout | Experiments with quantum-compiler builds |

---

## 🪜 Hierarchy Cheat-Sheet

```
Meta layer:        Agent X (spawn) ─ Base Agent (inherit) ─ Agent Factory (template)
Coordinator:       Crew Orchestrator
Memory:            Brain
Self-healing:      Healer
Worker crew (6):   Frontend · Backend · DB Architect · QA · Security · System Architect
Business crew:     Project Strategist · Business · Tips Writer
Bot layer:         BROski Bot · Super Hyper BROski · NemoClaw
Infra:             DevOps · Throttle · Dashboard · Coder
```

---

## 🧩 Related Skills

- [[HS-067]] Agent Role Hierarchy Pattern — manager/worker/validator tiers
- [[HS-079]] Specialist Agent Role Definitions — the 6 worker specialists in CAN/CANNOT detail
- [[HS-090]] Universal Life Plan YAML v2.0 — every agent here inherits this spec
- [[HS-091]] Top-Tier Agent Identity Cards — deep cards for Agent X, Brain, Healer, Crew Orchestrator, Security
