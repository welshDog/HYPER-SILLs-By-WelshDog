# HS-094 — 6-Sprint Production Roadmap (with KPI Gates) 🚀

**Category:** `dev/`
**Source:** HyperCode-V2.4 — `agents/🧬 The Full Confirmed Hyper Agent Roster` §3
**Version:** v1

---

## 🤔 What It Does

The canonical 12-week (six 2-week sprints) plan for taking an agent system from "manifests written" to "72h soak passing". Each sprint has a hard **KPI gate** — you don't advance until the gate is green. Use as a template when planning a new ecosystem rollout or a major version bump.

---

## 🗺️ The 6 Sprints

| Sprint | Weeks | Goal | KPI Gate |
|---|---|---|---|
| 🟢 1 | 1–2 | Life plan YAML for every agent (`agents/*/life_plan.yaml`) | All agents respond `<200ms` on `/health` |
| 🟡 2 | 3–4 | Redis pub/sub event bus + dependency graph wired | 3-agent swarm forms in `<500ms` |
| 🟡 3 | 5–6 | LangGraph goal-decomposition + Redis priority queue | 100 tasks, **zero deadlocks** |
| 🔴 4 | 7–8 | BROski$ reward ledger + play mini-games in Terminal | 1 agent earns BROski$ **autonomously** |
| 🔴 5 | 9–10 | LLM-swap interface + Alembic schema migrations | Swap GPT→Claude→Mistral **zero-downtime** ✅ |
| 🔥 6 | 11–12 | 72h soak test + docs portal + governance ledger | Coherence ≥ 0.9, uptime 99.9% |

> Colour = risk tier (🟢 low → 🔥 hardest).

---

## ✅ Acceptance Criteria (every agent must pass on Sprint 6 gate)

- [ ] Latency p95 < 200ms on all API calls
- [ ] Uptime ≥ 99.9% over 7-day window
- [ ] Conversation coherence score ≥ 0.9
- [ ] Collaborative task success ≥ 95% on multi-agent benchmarks
- [ ] Zero secrets in repo (`.secrets.baseline` clean)
- [ ] All containers pass OWASP Dependency-Check

These map 1:1 to the contract test suite ([[HS-092]]).

---

## 🚦 KPI-Gate Discipline

A sprint **does not close** until its KPI is hit on real metrics — no "we'll fix it in the next sprint" carry-overs. This is what stops V0.x rot.

```
Sprint complete ?
  ├─ KPI green       → close, retro, plan next sprint
  ├─ KPI yellow      → extend sprint by 1 week, no new scope
  └─ KPI red 2 weeks → escalate to architecture review, may
                       redesign before continuing
```

---

## 🎯 First-Win Quickstart

```bash
# Sprint 1 starter
mkdir -p agents/life-plans
# Drop in HS-090 template, copy per agent (~20 min/each)
git add agents/life-plans/
git commit -m "feat: 🦅 Hyper Agent Life Plans v2.0 — all 22 agents"
git push origin main
```

Once `/health` returns < 200ms across all agents → Sprint 1 done, move to Sprint 2.

---

## 🧩 Related Skills

- [[HS-090]] Universal Life Plan YAML — Sprint 1 deliverable
- [[HS-092]] Agent Contract Test Suite — Sprint 6 acceptance harness
- [[HS-093]] Continuous Learning Loop — Sprint 6 governance ledger lives here
- [[HS-089]] Hyper Agent Roster — the agents this roadmap rolls out
- [[HS-076]] Pre-Commit Testing Checklist — CI gate per sprint
