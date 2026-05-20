# HS-101 — Sleep Cycle + 5-Minute Anti-Thrash Hold 😴

**Category:** `dev/`
**Source:** HyperCode-V2.4 — `agents/throttle-agent/HYPER-AGENT-BIBLE.md`
**Version:** v1

---

## 🤔 What It Does

The RAM-tiered pause/resume pattern with a **5-minute anti-thrash hold** that the throttle-agent uses to manage memory pressure without ping-pong oscillation. Reusable for **any** system that pauses & resumes resources based on a load signal — RAM, CPU, queue depth, error rate.

> Implements Law 5 (REST) from [[HS-098]]. Sleep is not death — it's conservation.

---

## 📊 The Pressure Thresholds

```
RAM < 75%  →  [ALL GREEN]   Agent monitors, does nothing
RAM ≥ 80%  →  [WARN]        Tier 6 containers paused (sleep)
RAM ≥ 90%  →  [HIGH]        Tier 5 + 6 paused
RAM ≥ 95%  →  [EMERGENCY]   Tier 4 + 5 + 6 paused
```

Tier definitions (which containers fall in each tier) live in [[HS-104]].

---

## ⏱️ The Wake-Up Rules

1. RAM must drop **below 75%** to begin wake sequence
2. Must stay below 75% for **5 full minutes** (anti-thrash hold)
3. **Healer must approve** each container's resume ([[HS-103]] circuit-breaker)
4. If still paused after **15 minutes** → auto-resume regardless (TTL)

---

## 🚫 Why The 5-Minute Hold Matters

Without it:

```
RAM 80% → pause → RAM 70% → resume → RAM spikes 80% → pause →
RAM 70% → resume → RAM spikes 80% → pause → ... (forever)
```

This is **thrashing** — and it's worse than either always-paused or always-running:
- Each pause/resume cycle costs Docker socket calls (~100ms each)
- Containers in the middle of work get killed mid-task
- Logs flood, observability noise spikes
- Healer circuit-breaker opens, real recoveries get blocked

The 5-minute hold creates **calm, not chaos**.

---

## 🐍 Reference Implementation

```python
import asyncio
from collections import deque
from datetime import datetime, timedelta

class AntiThrashHold:
    def __init__(self, hold_minutes: int = 5, low_watermark: float = 0.75):
        self.hold_minutes = hold_minutes
        self.low_watermark = low_watermark
        self.below_watermark_since: datetime | None = None

    def update(self, current_pressure: float) -> bool:
        """Returns True if we're cleared to resume, False otherwise."""
        now = datetime.utcnow()

        if current_pressure >= self.low_watermark:
            # We're back above the line — reset the hold
            self.below_watermark_since = None
            return False

        if self.below_watermark_since is None:
            # First moment under the line — start the timer
            self.below_watermark_since = now
            return False

        # We've been under the line — has it been long enough?
        elapsed = now - self.below_watermark_since
        return elapsed >= timedelta(minutes=self.hold_minutes)
```

Usage in the autopilot loop ([[HS-100]] DECIDE state):

```python
hold = AntiThrashHold(hold_minutes=5, low_watermark=0.75)

async def decide(signals):
    ram_pct = signals["ram_pct"]
    if ram_pct >= 0.80:
        return {"action": "pause", "tier": tier_for_pressure(ram_pct)}
    if hold.update(ram_pct):
        return {"action": "resume", "tier": "all_paused"}
    return {"action": "wait"}  # in hold period
```

---

## ⏰ TTL Auto-Resume (the safety net)

Even with the hold, paused containers must eventually wake — otherwise a stuck pressure signal would orphan them forever. **TTL = 15 minutes default.**

```python
async def check_ttl_expiry():
    for container, paused_at in paused_containers.items():
        if datetime.utcnow() - paused_at >= timedelta(minutes=15):
            await resume(container, reason="ttl_expired")
```

TTL is the floor on responsiveness. Hold is the ceiling on thrash. Together they bound the system.

---

## 🎯 Generalising Beyond RAM

The pattern works for any monotonic load signal:

| Signal | High-water | Low-water + hold | Tier 1 protected |
|---|---|---|---|
| RAM % | 80 / 90 / 95 | 75% for 5 min | postgres, redis, core |
| CPU % | 70 / 85 / 95 | 60% for 3 min | core, dashboard |
| Queue depth | 100 / 500 / 1000 | 50 for 2 min | api gateway |
| Error rate | 1% / 5% / 10% | 0.5% for 5 min | auth, payment |

Tune watermarks per-signal; keep the hold ≥ 3 min minimum (lower = thrashes).

---

## 🧩 Related Skills

- [[HS-098]] 6 Laws — Law 5 (REST) is this pattern
- [[HS-104]] Tier Protection Rules — which containers map to which tier
- [[HS-103]] Healer Circuit-Breaker Protocol — wake approval
- [[HS-102]] Predictive Trend — pairs with this for *preemptive* pausing
- [[HS-100]] Agent Lifecycle State Machine — pattern lives in DECIDE state
