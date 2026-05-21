# HS-096 — 🗓️ THE LONG MARCH — 4-Phase / 8-Sprint Production Roadmap (Alternative Cadence)

**Category:** `dev/`
**Source:** HyperCode-V2.4 — `agents/🦅 HYPER AGENT LIFE PLANS — MASTER ARCHITECTURE` §3
**Version:** v1

---

## 🤔 What It Does

A **16-week / 8-sprint / 4-phase** rollout plan for an agent ecosystem. Slower cadence than [[HS-094]] (which is 12-week / 6-sprint). Use this when the team has less capacity, when the system is bigger than 22 agents, or when each phase needs a hard "stop, validate, reset" checkpoint before advancing.

> **Pick one — don't run both.** HS-094 = ship fast. HS-096 = ship methodically.

---

## 🗺️ The 4 Phases

```
PHASE 1 — Foundation        (Weeks 1–4)   ← schema + identity
PHASE 2 — Collaboration     (Weeks 5–8)   ← swarm comms
PHASE 3 — Intelligence      (Weeks 9–12)  ← reasoning + economy
PHASE 4 — Future-Proof      (Weeks 13–16) ← extensibility + learning
```

Each phase is **2 sprints (4 weeks)** with a phase-exit KPI gate.

---

## 📅 The 8 Sprints

| Sprint | Phase | Weeks | Goal | Phase-Exit KPI |
|---|---|---|---|---|
| 1 | Foundation | 1–2 | Life plan YAML scaffold for all agents → `agents/{name}/life_plan.yaml` | (combined with S2) |
| 2 | Foundation | 3–4 | Dialogue state machines + empathy model per agent | All agents deploy via docker-compose, **p95 latency < 200ms** baseline established |
| 3 | Collaboration | 5–6 | Dependency graph wired → Redis pub/sub event bus live | (combined with S4) |
| 4 | Collaboration | 7–8 | Swarm formation rules + RAFT consensus prototype | 3-agent swarm task success **≥ 95%**, formation < **500ms** |
| 5 | Intelligence | 9–10 | Goal decomposition engine + recursive task tree | (combined with S6) |
| 6 | Intelligence | 11–12 | Play framework mini-games + BROski$ reward system | Conversation coherence **≥ 0.9**, decomposition accuracy **≥ 90%** |
| 7 | Future-Proof | 13–14 | LLM-swap interface (LiteLLM) + plugin registry API | (combined with S8) |
| 8 | Future-Proof | 15–16 | Nightly retraining job + drift detection alarms | **99.9% uptime over 30-day soak**, zero-downtime deploys confirmed |

---

## 🎯 Per-Agent Acceptance (Phase 4 exit)

- [ ] Latency p95 < 200ms on all API calls
- [ ] Uptime ≥ 99.9% over 7-day window
- [ ] Conversation coherence ≥ 0.9 (RAGAS or custom scorer)
- [ ] Multi-agent task success ≥ 95%
- [ ] Zero secrets in repo (`.secrets.baseline` clean)
- [ ] OWASP Dependency-Check passes

---

## ⚖️ HS-094 vs HS-096 — Which To Pick?

| Factor | [[HS-094]] 6-Sprint | HS-096 4-Phase / 8-Sprint |
|---|---|---|
| Duration | 12 weeks | 16 weeks |
| Team capacity | ≥ 2 engineers full-time | 1 engineer or part-time team |
| Scope | ≤ 22 agents | > 22 agents, or fragile ecosystem |
| Checkpoint cadence | After each sprint | After each phase (every 2 sprints) |
| KPI strictness | Per-sprint hard gate | Per-phase hard gate (looser inside phase) |
| Best for | Lyndz solo crunch | A future external team / hand-off |

---

## 🚦 Phase-Gate Discipline

```
Phase complete ?
  ├─ KPI green       → close phase, retro, plan next phase
  ├─ KPI yellow      → extend by 2 weeks (1 sprint), no new scope
  └─ KPI red 2 wks   → escalate to architecture review;
                       may redesign before continuing
```

Same discipline as [[HS-094]] but applied at the **phase** boundary, not the sprint boundary.

---

## 🧩 Related Skills

- [[HS-094]] 6-Sprint Production Roadmap — faster sibling cadence
- [[HS-090]] Universal Life Plan YAML — Phase 1 Sprint 1 deliverable
- [[HS-092]] Agent Contract Test Suite — phase-exit harness
- [[HS-093]] Continuous Learning Loop — Phase 4 Sprint 8 lands here
- [[HS-097]] Hyper Agent Dependency Graph — Phase 2 Sprint 3 wiring map
