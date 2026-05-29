# HS-091 — 🪪 THE FOUNDING SIX — Top-Tier Agent Identity Cards

**Category:** `agents/`
**Source:** HyperCode-V2.4 — `agents/🧬 The Full Confirmed Hyper Agent Roster` §2 + `agents/🦅 HYPER AGENT LIFE PLANS — MASTER ARCHITECTURE` §2
**Version:** v1.1 *(2026-05-21 — added AutoEvo card from Master Architecture)*

---

## 🤔 What It Does

The six **load-bearing** agents in the HyperCode ecosystem — the ones without which the swarm collapses. Each card captures purpose, hard-stops, evolution path, and special invariants you cannot break.

> Distinct from [[HS-079]] (the worker specialist crew). These are the *infrastructure* agents: meta, memory, healing, routing, security, **deploy pipeline**. Each has invariants that override standard role rules.

---

## 🦅 Agent X / Architect

| Field | Value |
|---|---|
| **Path** | `agents/architect` |
| **Purpose** | Spawns + evolves all agents via Docker Model Runner |
| **Hard-stop** | **Cannot delete Healer** (spawn-lock protected — see [[#🩺 Healer Agent]]) |
| **Special power** | Only agent that can rewrite deployment manifests |
| **Evolution path** | `reactive_spawner → proactive_designer → autonomous_ecosystem_god` |

**Invariant:** Agent X is the only legal source of new agents. If something spawns a container that isn't going through Agent X's manifest pipeline, it's a sacred-rule violation.

---

## 🧠 Brain / Memory Agent

| Field | Value |
|---|---|
| **Path** | `agents/memory` |
| **Purpose** | Cross-session context, Perplexity AI interface, knowledge store |
| **Special** | Full ADHD + Dyslexia empathy mode **always on** — non-toggleable |
| **Storage** | Redis (hot) + PostgreSQL (cold) memory tiering |
| **Evolution path** | `knowledge_retriever → active_reasoner → collective_consciousness_node` |

**Invariant:** Empathy mode flags (`adhd_friendly_mode`, `dyslexia_mode` in [[HS-090]]) are forced `true` for Brain regardless of caller config. Sacred rule — do not let a downstream agent disable them.

---

## 🩺 Healer Agent

| Field | Value |
|---|---|
| **Path** | `agents/healer` |
| **Purpose** | Monitor all 22+ containers, auto-restart failed services |
| **Cannot be killed** | **Protected by Agent X spawn-lock** — refuses kill signals, auto-respawns |
| **Trigger** | Prometheus metric anomaly + 30s heartbeat check |
| **Evolution path** | `reactive_healer → predictive_healer → chaos_immunologist` |

**Invariant:** Healer is the only agent that can `docker restart` other containers. Any other agent attempting it = security violation, escalate to [[HS-077]] approval gate.

---

## 🎭 Crew Orchestrator

| Field | Value |
|---|---|
| **Path** | `agents/crew-orchestrator` |
| **Purpose** | Air traffic controller — routes ALL inter-agent tasks |
| **Consensus** | RAFT-style leader election (highest-uptime wins) |
| **Evolution path** | `manual_dispatcher → event_driven_router → autonomous_swarm_AI` |

**Invariant:** All inter-agent task routing flows through Crew Orchestrator. Direct agent-to-agent calls are allowed for *queries* but **not for task delegation** — that must go via the orchestrator so the One Door rule (see V2.4 sacred rule #14) holds.

---

## 🔐 Security Engineer

| Field | Value |
|---|---|
| **Path** | `agents/06-security-engineer` |
| **Purpose** | Passive audit of every agent, secrets scanner, OWASP enforcer |
| **Never sleeps** | Passive listener on **every** Redis channel |
| **Evolution path** | `reactive_scanner → proactive_threat_hunter → zero_trust_guardian` |

**Invariant:** Security has read-only listen on every channel by design. If you build a "private" channel that Security can't see, you've broken the SOC 2 audit-logging requirement.

---

## 🛠️ AutoEvo / DevOps Engineer

| Field | Value |
|---|---|
| **Path** | `agents/05-devops-engineer` |
| **Codename** | `AutoEvo` |
| **Port** | 8083 |
| **Purpose** | CI/CD, container health, autonomous self-upgrade pipelines (blue-green deploys) |
| **Special power** | Can trigger **blue-green deploys without human input** |
| **Hard-stop** | Must log every auto-deploy to the governance ledger ([[HS-095]]) |
| **Evolution path** | `scheduled_deployer → event_driven_deployer → predictive_pre-emptive_deployer` |

**Invariant:** AutoEvo is the **only** agent that can write to a production deploy manifest *other than Agent X*. The difference: Agent X writes manifests for *agents themselves*, AutoEvo writes manifests for the *CI/CD pipeline + service rollouts*. Healer ([[#🩺 Healer Agent]]) depends on AutoEvo for its deploy lifecycle — see the dependency graph in [[HS-097]].

---

## 🚦 Quick "Which Top-Tier Do I Talk To?" Picker

| Situation | Talk to |
|---|---|
| Need a new agent spawned | 🦅 Agent X |
| Need to remember something across sessions | 🧠 Brain |
| Container keeps falling over | 🩺 Healer |
| Need agent A to do work via agent B | 🎭 Crew Orchestrator |
| Suspect a credential leak / OWASP issue | 🔐 Security |
| Need a blue-green deploy / CI pipeline change | 🛠️ AutoEvo |

---

## 🧩 Related Skills

- [[HS-089]] Hyper Agent Roster — full 22-agent map
- [[HS-079]] Specialist Agent Role Definitions — the worker crew (6)
- [[HS-090]] Universal Life Plan YAML — schema each of these implements
- [[HS-097]] Hyper Agent Dependency Graph — wiring between these 6
- [[HS-095]] Governance Ledger Entry Schema — AutoEvo's mandatory audit trail
- [[HS-077]] User Agency Approval Gate — what Healer's kill-protection escalates to

## 📋 THE PROMPT

```text
Use this skill by copying the relevant sections and adapting placeholders to your context.
```
