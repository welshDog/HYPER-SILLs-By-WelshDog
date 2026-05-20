# HS-099 — Anatomy of an Agent (6 Organs) 🧬

**Category:** `agents/`
**Source:** HyperCode-V2.4 — `agents/throttle-agent/HYPER-AGENT-BIBLE.md`
**Version:** v1

---

## 🤔 What It Does

A conceptual decomposition of every HyperCode agent into six **organs**. Use this when designing a new agent — if you can't name what plays the role of each organ, the agent isn't complete. Different angle from [[HS-090]] (which is the YAML schema) and [[HS-079]] (which is role boundaries).

---

## 🧠 Brain — Decision Engine

The logic core. Reads signals (RAM %, CPU %, Docker state, business metrics) and decides what to do. Uses **linear regression** for prediction — not just reaction, but anticipation. See [[HS-102]] for the predictive technique.

**Concrete in throttle-agent:** deque of last 30 RAM readings + slope projection.

---

## 👁️ Eyes — Observability Layer

15+ Prometheus metrics. JSON-structured logs. Health check endpoints. **The Eyes never sleep.** They watch everything and report honestly.

**Mandatory minimum:** 5 metrics per [[HS-105]] Core Agent Metrics Contract.

---

## 🫀 Heart — Autopilot Loop

An async loop that pulses every N seconds (default: 30s). The heartbeat of the agent. **When it stops, the agent is dead.**

```python
async def autopilot():
    while not shutdown:
        await watch()
        await decide()
        await act()
        await report()
        await asyncio.sleep(POLL_INTERVAL_SECONDS)
```

Maps to the WATCH → DECIDE → ACT → REPORT phases of [[HS-100]] Agent Lifecycle.

---

## 🛡️ Shield — Protection Rules

Tiers 1–3 and named containers are ALWAYS protected. **The Shield is hardcoded.** No config can override a protected core. See [[HS-104]] for the full tier definitions.

```python
if container in PROTECTED_TIERS_1_2_3 or container in PROTECT_CONTAINERS:
    return  # untouchable
```

---

## 🤝 Voice — Healer Integration

Agents talk to the Healer Agent before making big moves. Before resuming a paused container: *"Healer, is it safe?"* The Healer holds the circuit breaker. Agents respect it. See [[HS-103]] for the protocol.

---

## 😴 Sleep Mode — TTL Pause System

When RAM pressure hits, non-critical containers sleep (pause). They auto-wake after 15 minutes (TTL) or when RAM drops below 75%. **Sleep is not death. It's conservation.** Full pattern in [[HS-101]].

---

## ✅ Anatomy Audit (per new agent)

When spawning a new agent, verify all 6 organs exist:

- [ ] **Brain:** named decision function with explicit input/output schema
- [ ] **Eyes:** `/metrics` endpoint + structured JSON logs
- [ ] **Heart:** async loop with `POLL_INTERVAL_SECONDS` env var
- [ ] **Shield:** protected-list constant + self-protection auto-add
- [ ] **Voice:** Healer client wired with circuit-breaker check
- [ ] **Sleep:** TTL pause or equivalent rest mechanism (skip only if agent must be always-on)

Missing any organ → not a fully-formed agent.

---

## 🧩 Related Skills

- [[HS-098]] 6 Laws — the laws each organ obeys
- [[HS-090]] Universal Life Plan YAML — the schema each organ implements
- [[HS-101]] Sleep Cycle + Anti-Thrash — the Sleep organ in detail
- [[HS-102]] Predictive Trend — the Brain organ's prediction engine
- [[HS-103]] Healer Circuit-Breaker Protocol — the Voice organ's protocol
- [[HS-104]] Tier Protection Rules — the Shield organ's config
- [[HS-105]] Core Agent Metrics Contract — the Eyes organ's contract
- [[HS-106]] New Agent Build Checklist — uses this anatomy audit
