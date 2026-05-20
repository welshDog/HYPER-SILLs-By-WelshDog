# HS-100 — 🔄 CRADLE-TO-GRAVE — Agent Lifecycle State Machine (BIRTH → DEATH)

**Category:** `agents/`
**Source:** HyperCode-V2.4 — `agents/throttle-agent/HYPER-AGENT-BIBLE.md`
**Version:** v1

---

## 🤔 What It Does

The per-cycle state machine every HyperCode agent runs from container start to graceful shutdown. Different from [[HS-087]] (per-task Decision Tree) — this is the *autopilot loop* lifecycle, not the per-task flow. Also distinct from [[HS-090]] life-plan `dialogue_state_machine` which is the per-conversation flow.

> **Three state machines, three layers:**
> 1. **Container lifecycle** ← this skill (BIRTH → DEATH)
> 2. **Per-task flow** → [[HS-087]] Decision Tree
> 3. **Per-conversation** → [[HS-090]] dialogue_state_machine

---

## 🔄 The 8 States

```
BIRTH    →  Container starts, FastAPI boots, startup() fires
WAKE     →  Autopilot loop begins (if AUTO_*_ENABLED=true)
WATCH    →  Poll cycle every N s: check signals, Docker, Healer
DECIDE   →  Apply decision engine (linear regression + thresholds)
ACT      →  Pause / resume / send / write — the actual mutation
REPORT   →  Log action (JSON) · update Prometheus · tell Healer
REST     →  Sleep POLL_INTERVAL_SECONDS · repeat from WATCH
DEATH    →  Container stops · graceful FastAPI shutdown
```

---

## 🗺️ Transitions

```
BIRTH ──on_boot_complete──▶ WAKE
WAKE  ──autopilot_enabled──▶ WATCH
                            ▲
                            │
WATCH ──signals_collected──▶ DECIDE
DECIDE ─action_chosen──────▶ ACT
ACT   ─completed──────────▶ REPORT
REPORT ─logged────────────▶ REST
REST  ─tick───────────────┘   (loops back to WATCH)

ANY state ─on_SIGTERM────▶ DEATH
```

---

## 🧱 Skeleton

```python
# main.py
import asyncio
from fastapi import FastAPI

app = FastAPI()
shutdown_event = asyncio.Event()

@app.on_event("startup")
async def birth():
    # BIRTH: init clients, register with Crew Orchestrator
    await register_self()
    if os.getenv("AUTO_ENABLED", "true").lower() == "true":
        asyncio.create_task(autopilot())  # WAKE

async def autopilot():
    while not shutdown_event.is_set():
        signals  = await watch()          # WATCH
        decision = await decide(signals)  # DECIDE
        result   = await act(decision)    # ACT
        await report(result)              # REPORT
        await asyncio.sleep(int(os.getenv("POLL_INTERVAL_SECONDS", "30")))  # REST

@app.on_event("shutdown")
async def death():
    shutdown_event.set()
    await deregister_self()
```

---

## 🚨 Mandatory Per-State Hooks

Every state must emit at least one observability signal:

| State | Required signal |
|---|---|
| BIRTH | log `component=<name> action=startup version=<ver>` |
| WAKE | metric `agent_up = 1` |
| WATCH | metric `agent_last_watch_ts = now` |
| DECIDE | metric `agent_decision_reasons{reason=...}` incremented |
| ACT | log `action=<verb> target=<id>` + emit `task_started` event |
| REPORT | metric `agent_last_action_ts = now` + emit `task_completed` event |
| REST | (none — quiet by design) |
| DEATH | log `component=<name> action=shutdown` + metric `agent_up = 0` |

If any hook is missing, observability drift detection in [[HS-093]] will flag the agent.

---

## ⚠️ Anti-patterns

- **Skipping REPORT** → silent action = Law 3 violation ([[HS-098]])
- **WATCH without DECIDE** → busy loop that does nothing → wastes cycles → Law 5 violation
- **ACT before DECIDE** → reactive without reasoning → not a real agent, just a script
- **No graceful DEATH** → container kill doesn't deregister → Crew Orchestrator has stale entries → swarm formations fail

---

## 🧩 Related Skills

- [[HS-099]] Anatomy of an Agent — Heart organ runs this loop
- [[HS-087]] Agent Decision Tree — per-task flow nested inside DECIDE
- [[HS-098]] 6 Laws — Law 3 (REPORT) + Law 5 (REST) live here
- [[HS-105]] Core Agent Metrics — what to emit per state
- [[HS-070]] Observable Agent Operations Pattern
