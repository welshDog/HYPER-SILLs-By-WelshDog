# HS-036 — 🧠 ANALOGY ARSENAL — Analogy Arsenal
**Category:** broski
**Version:** 1.0


---
skill_id: HS-036
hero_name: "ANALOGY ARSENAL"
emoji: "🧠"
version: v1.0.0
status: ACTIVE
category: broski
depends_on:
  - HS-002  # SIX_LAWS_OF_AGENTS — Law 3 (EXPLAIN SIMPLY) motivates this arsenal
provides:
  - nd-friendly-analogies
  - explanation-arsenal
  - concept-to-concrete-bridges
related:
  - HS-069  # MERCY MESSAGE — ND-first comms pair with ND-first analogies
  - HS-034  # BEAT ARCHITECT — 7-beat structure uses these analogies in teaching beats
graph_notes: "Library of battle-tested analogies for explaining AI/tech concepts to ND brains — use before writing docs or error messages."
---
> *"Complex tech explained in 10 words or less. ADHD-brain approved."*

---

## 🎯 What It Does
A bank of battle-tested analogies for explaining complex tech concepts to neurodivergent learners. Each analogy unlocks instant understanding without jargon.

## 🌍 Why It Exists
ADHD + Dyslexic brains need a pattern match before they can absorb detail. The right analogy = 10x faster learning.

## ⚙️ How To Use
1. Paste when writing course content, docs, or explaining tech to Lyndz
2. Pick the right analogy from the bank
3. Lead with the analogy BEFORE the technical explanation

---

## 📋 THE PROMPT

```
Explain [TECH CONCEPT] to a neurodivergent learner using an analogy from this bank.
Lead with the analogy. Then give the technical explanation in 3 sentences max.

ANALOGY BANK:

Docker containers     → Lunchboxes. Each has everything it needs. Won't spill into others.
FastAPI routes        → The menu at a restaurant. Each item = one thing you can order.
Redis cache           → Post-it note on your monitor. Fast to read, gone after a while.
PostgreSQL database   → Filing cabinet. Organised, searchable, stays forever.
Webhooks              → Someone texting you when something happens. You don't have to keep asking.
Agent swarm           → Football team. Each player has a role. Coach (orchestrator) calls the plays.
Docker networks       → Different floors in a building. Some can talk to each other, some can't.
Migrations            → Renovating a house while people live in it. One careful room at a time.
JWT tokens            → A wristband at a festival. Proves you paid. No need to show your ticket again.
Environment variables → Secrets in a locked drawer. The app knows where the drawer is.
Prometheus            → A doctor taking your system's vitals every 15 seconds.
Grafana               → The heart monitor screen the doctor watches.
Circuit breakers      → The fuse box. When one thing overloads, it trips before burning the house down.
SSE (Server-Sent Events) → A live radio broadcast. Server talks, client listens. No back-and-forth.
RLS (Row Level Security) → A bouncer for each row of data. You only see what you're allowed to see.

[INPUT: TECH CONCEPT to explain]
```

---

## ✅ Example
**Input:** "Explain Prometheus monitoring"
**Output:** "Think of Prometheus as a doctor taking your system's vitals every 15 seconds. It scrapes metrics from all your containers and stores them. If something spikes, Grafana (the heart monitor screen) shows you the moment it happened."

## 🔗 Related Skills
- HS-034 — BEAT ARCHITECT (7-Beat Module Structure)
- HS-069 — MERCY MESSAGE (ND-First Error Messages)

---
*HYPER-SKILLs Vault — welshDog 🐕🏴󠁧󠁢󠁷󠁬󠁳󠁧⚡*
