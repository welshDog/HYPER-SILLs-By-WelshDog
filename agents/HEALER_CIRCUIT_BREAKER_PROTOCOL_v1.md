# HS-103 — 🤝 HEALER’S CHORUS — Healer Circuit-Breaker Protocol

---
skill_id: HS-103
hero_name: "HEALER'S CHORUS"
emoji: "🤝"
version: v1.0
category: agents
depends_on:
  - HS-098  # SACRED SIX — implements Law 3 (COMMUNICATION)
  - HS-099  # SIX-ORGAN HEART — Voice organ protocol
  - HS-085  # FIVE WARDS — fail-safe on timeout (Law 4 GRACE)
  - HS-105  # METRICS OATH — Healer watches agent_up signals
provides:
  - healer-circuit-breaker-protocol
  - ask-before-act-pattern
  - report-after-action-pattern
  - healer-client-wrapper
related:
  - HS-077  # User Agency Approval Gate — escalation path when circuit is open
  - HS-091  # Founding Six — Healer agent invariants
  - HS-095  # Governance Ledger — healer_unreachable events go here
graph_notes: "Voice organ implementation. Sits above HS-085 (guardrails) and depends on HS-098 (laws). Required by any agent that mutates system state. Consumed by HS-089 (all 22+ roster agents use this protocol)."
---

**Category:** `agents/`
**Source:** HyperCode-V2.4 — `agents/throttle-agent/HYPER-AGENT-BIBLE.md`
**Version:** v1

---

## 🤔 What It Does

The two-call protocol every HyperCode agent uses to coordinate with the Healer Agent before mutating state. **Ask before resuming. Report after acting.** Implements Law 3 (COMMUNICATION) from [[HS-098]] and the Voice organ from [[HS-099]].

> Healer holds the circuit breaker. Agents respect it.

---

## 1️⃣ Ask — Check Circuit Breaker (BEFORE action)

```http
GET http://healer-agent:8008/circuit-breaker/{container}
```

**Response:**

```json
// safe to act
{ "state": "closed", "since": "2026-03-23T01:00:00Z" }

// DO NOT act — healer is mid-recovery on this container
{ "state": "open",   "until": "2026-03-23T02:15:00Z", "reason": "crash_loop" }

// recently healed — probationary, act with caution
{ "state": "half_open", "trial_until": "2026-03-23T02:05:00Z" }
```

**Rule:** only `closed` is a green light. `open` = refuse, `half_open` = defer one cycle.

---

## 2️⃣ Report — State Change (AFTER action)

```http
POST http://healer-agent:8008/throttle/state
Content-Type: application/json

{
  "agent": "throttle-agent",
  "action": "pause",
  "containers": ["analytics-worker", "report-builder"],
  "paused": true,
  "ttl_seconds": 900,
  "reason": "ram_pressure:0.92"
}
```

Healer responds `200 OK` with an acknowledgement ID. If you don't get the ack, the action **didn't happen** from the swarm's POV — retry the report up to 3 times, then escalate to [[HS-077]] approval gate.

---

## 🐍 Reference Wrapper

```python
import httpx
from typing import Literal

HEALER_URL = "http://healer-agent:8008"

class HealerClient:
    def __init__(self, url: str = HEALER_URL, timeout: float = 5.0):
        self.url = url
        self.timeout = timeout

    async def can_act_on(self, container: str) -> bool:
        async with httpx.AsyncClient(timeout=self.timeout) as c:
            try:
                r = await c.get(f"{self.url}/circuit-breaker/{container}")
                return r.json().get("state") == "closed"
            except (httpx.TimeoutException, httpx.NetworkError):
                # Law 4 GRACE — fail safe, don't act
                return False

    async def report_state(self, payload: dict) -> str | None:
        async with httpx.AsyncClient(timeout=self.timeout) as c:
            for attempt in range(3):
                try:
                    r = await c.post(f"{self.url}/throttle/state", json=payload)
                    return r.json().get("ack_id")
                except (httpx.TimeoutException, httpx.NetworkError):
                    if attempt == 2:
                        await emit_event({
                            "event": "healer_unreachable",
                            "payload": payload,
                        })
                        return None
```

---

## 🛡️ The Sacred Rules of the Protocol

1. **No silent actions.** Every mutation is reported. If Healer is unreachable, log the action and try again — never proceed as if it succeeded.
2. **Closed = go. Anything else = wait.** Don't try to outsmart the half-open state.
3. **Healer's word is final.** If the circuit-breaker says open, the only legal action is wait. (Override path = explicit [[HS-077]] approval gate.)
4. **Self-Healer-check exception.** The Healer agent itself does NOT call its own circuit-breaker.
5. **`/throttle/state` is one of several reporter endpoints.** Other patterns use `/queue/state`, `/db/state`, etc. — but the shape is the same.

---

## ⏱️ Timeouts + Retry Budget

| Call | Timeout | Retries | On final failure |
|---|---|---|---|
| `GET /circuit-breaker` | 5s | 0 (single-shot) | Treat as `open` (fail safe) |
| `POST /throttle/state` | 5s | 2 (3 total tries, exp backoff) | Emit `healer_unreachable` event, log to governance ledger ([[HS-095]]) |

---

## 🚨 Anti-patterns

- **Acting then asking.** "I already paused it, just let me tell Healer after" — no. Ask first. Always.
- **Caching circuit-breaker state.** State changes mid-cycle; cache for ≤ 1 cycle only.
- **Treating timeout as `closed`.** Treat as `open`. Fail safe.
- **Skipping the ack.** No ack = action didn't propagate to Healer's state.

---

## 🧩 Related Skills

- [[HS-098]] 6 Laws — Law 3 (COMMUNICATION) is this protocol
- [[HS-099]] Anatomy of an Agent — Voice organ
- [[HS-091]] Top-Tier Identity Cards — Healer agent invariants
- [[HS-077]] User Agency Approval Gate — escalation path on `open` state
- [[HS-095]] Governance Ledger — where `healer_unreachable` events go
