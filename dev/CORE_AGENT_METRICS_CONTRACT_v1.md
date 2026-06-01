# DS-008 — 📊 THE METRICS OATH — Core Agent Metrics Contract (5 Mandatory)

---
skill_id: HS-105
hero_name: "THE METRICS OATH"
emoji: "📊"
version: v1.0
category: dev
depends_on:
  - HS-019  # OBSERVABLE_AGENT_OPERATIONS — observability philosophy this contract implements
provides:
  - metrics-contract
  - prometheus-metrics-pattern
  - agent-health-signals
related:
  - HS-019  # Observable Agent Operations — parent philosophy
graph_notes: "Concrete metrics contract. Depends on HS-019 for observability philosophy. Consumed by Healer (watches these signals) and Tier protection (reads agent_up)."
---

**Category:** `dev/`
**Source:** HyperCode-V2.4 — `agents/throttle-agent/HYPER-AGENT-BIBLE.md`
**Version:** v1

---

## 🤔 What It Does

The five Prometheus metrics **every HyperCode agent must export**, no exceptions. Different from [[HS-019]] which is the *observability philosophy* — this is the concrete minimum contract.

> Rule: **If Grafana can't see it, it didn't happen.**

---

## 📋 The 5 Mandatory Metrics

```python
from prometheus_client import Counter, Gauge

# 1. Is this agent alive?  (1 if running, 0 if down)
agent_up = Gauge(
    "agent_up",
    "Is this agent alive",
    ["agent"],
)

# 2. How long has it been running?  (seconds since startup)
agent_uptime_seconds = Gauge(
    "agent_uptime_seconds",
    "Agent uptime in seconds",
    ["agent"],
)

# 3. When did it last do something meaningful?  (unix ts)
agent_last_action_ts = Gauge(
    "agent_last_action_ts",
    "Unix timestamp of last meaningful action",
    ["agent"],
)

# 4. How many errors, by type?
agent_error_total = Counter(
    "agent_error_total",
    "Errors by category",
    ["agent", "error_type"],   # error_type = timeout|validation|network|internal|...
)

# 5. Why did it make each decision?
agent_decision_reasons = Counter(
    "agent_decision_reasons",
    "Decision reasons taken by the agent",
    ["agent", "reason"],   # reason = preemptive_pause|reactive_pause|wait|resume|...
)
```

**Label every metric with `agent=<name>`.** Without it Grafana can't slice per-agent.

---

## 🎯 How To Emit

```python
import os, time
from datetime import datetime

AGENT_NAME = os.getenv("AGENT_NAME", "unknown")
STARTUP_TS = time.time()

# At startup
agent_up.labels(agent=AGENT_NAME).set(1)

# Once per autopilot cycle
agent_uptime_seconds.labels(agent=AGENT_NAME).set(time.time() - STARTUP_TS)

# After every action
agent_last_action_ts.labels(agent=AGENT_NAME).set(time.time())

# On every decision
agent_decision_reasons.labels(agent=AGENT_NAME, reason="preemptive_pause").inc()

# On every error
try:
    ...
except TimeoutError:
    agent_error_total.labels(agent=AGENT_NAME, error_type="timeout").inc()
except ValidationError:
    agent_error_total.labels(agent=AGENT_NAME, error_type="validation").inc()

# On graceful shutdown
agent_up.labels(agent=AGENT_NAME).set(0)
```

---

## 📈 The Recommended Add-Ons (per agent type)

Beyond the 5 mandatory, **most agents** should also export:

| Metric | Type | When |
|---|---|---|
| `agent_action_duration_seconds` | Histogram | Wrap every `act()` call |
| `agent_external_call_duration_seconds{target=...}` | Histogram | Wrap every outbound HTTP |
| `agent_queue_depth` | Gauge | If the agent has a backlog |

**Specialty agents add their own** — e.g. throttle-agent exports 15+ including per-container RAM bytes, tier paused states, pause duration histograms.

---

## 🚨 What Healer + Crew Orchestrator Watch

These metrics aren't just for humans — Healer and Crew Orchestrator scrape them:

| Signal | Watcher | Action if abnormal |
|---|---|---|
| `agent_up = 0` for > 60s | Healer | Auto-restart container |
| `agent_last_action_ts` stale > 5× poll interval | Crew Orchestrator | Mark agent stalled, redirect tasks |
| `agent_error_total` spike > 5%/min | Security | Audit log review + Slack alert |
| `agent_decision_reasons{reason=wait}` saturating | DevOps | Watermarks may be too conservative |

---

## ✅ Quick Audit

Before shipping a new agent, hit `/metrics` and grep:

```bash
curl -s localhost:<port>/metrics | grep -E '^agent_(up|uptime|last_action|error_total|decision_reasons)' | sort -u
```

Should print at least 5 lines. Less than 5 = not contract-compliant.

---

## 🧩 Related Skills

- [[HS-019]] Observable Agent Operations — the observability philosophy above this contract
