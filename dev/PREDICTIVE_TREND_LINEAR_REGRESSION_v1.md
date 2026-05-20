# HS-102 — Predictive Trend via Linear Regression 📈

**Category:** `dev/`
**Source:** HyperCode-V2.4 — `agents/throttle-agent/HYPER-AGENT-BIBLE.md`
**Version:** v1

---

## 🤔 What It Does

Turn a reactive agent into a **predictive** one. Keep the last N readings of a signal (RAM, CPU, queue depth, latency, error rate) in a deque. Every cycle, compute the slope and project forward. Act on the *projection*, not the current value.

> The difference between "RAM is at 80%, pause now" and "RAM will hit 90% in 5 minutes, pause now to stop the cliff."

---

## 🐍 The Core Math (simplified)

```python
from collections import deque
from datetime import datetime
from statistics import mean

# Keep last N readings: (timestamp, value)
history: deque[tuple[datetime, float]] = deque(maxlen=30)

def add_reading(value: float):
    history.append((datetime.utcnow(), value))

def project_forward(steps_ahead: int = 5) -> float | None:
    """Project value `steps_ahead` cycles into the future.
    Returns None if too little history."""
    if len(history) < 3:
        return None

    # Convert timestamps to seconds-since-first-reading
    t0 = history[0][0]
    xs = [(t - t0).total_seconds() for t, _ in history]
    ys = [v for _, v in history]

    n = len(xs)
    mean_x, mean_y = mean(xs), mean(ys)
    num = sum((x - mean_x) * (y - mean_y) for x, y in zip(xs, ys))
    den = sum((x - mean_x) ** 2 for x in xs)
    if den == 0:
        return None
    slope = num / den            # Δvalue per second
    intercept = mean_y - slope * mean_x

    # Project: how far is `steps_ahead` cycles into the future?
    last_t = xs[-1]
    cycle_seconds = (xs[-1] - xs[-2]) if n >= 2 else 30
    future_t = last_t + cycle_seconds * steps_ahead
    return slope * future_t + intercept
```

---

## 🎯 Usage in an Autopilot Loop

```python
HIGH_WATERMARK = 0.90

async def decide(signals):
    add_reading(signals["ram_pct"])
    projected = project_forward(steps_ahead=10)  # ~5 minutes ahead at 30s cycle

    if projected and projected >= HIGH_WATERMARK:
        return {
            "action": "preemptive_pause",
            "reason": f"projection: ram→{projected:.0%} in ~5min",
        }

    if signals["ram_pct"] >= HIGH_WATERMARK:
        return {"action": "reactive_pause"}  # already at the cliff

    return {"action": "wait"}
```

Logs both branches separately — the **`preemptive_pause` ratio** is a quality metric for the predictor. If it's near 0%, the predictor is useless. If it's near 100%, the watermark is too aggressive.

---

## 📊 Quality Metrics To Export

```python
# Prometheus
prediction_made_total           = Counter("prediction_made_total", "...", ["signal"])
preemptive_action_total         = Counter("preemptive_action_total", "...", ["signal", "action"])
prediction_error                = Histogram("prediction_error_pct", "abs(actual - predicted)/actual")
```

After each cycle, compare yesterday's projection to today's actual reading — append to `prediction_error`. Drift in this histogram = retrain the model or extend the deque.

---

## 🎛️ Tuning Knobs

| Knob | Default | Effect |
|---|---|---|
| `deque maxlen` | 30 | Longer = smoother trend, slower to react to regime change |
| `steps_ahead` | 5–10 | Further = more pre-emptive, more false positives |
| `min_history` | 3 | Lower = act on weak data, risk noise |
| `cycle_seconds` | 30 | Sync with autopilot loop interval |

**Anti-pattern:** projecting > 30 steps with maxlen=30. The model is a *trend extrapolation*, not a real forecast — past 1× window size it's guessing.

---

## 🚫 When NOT To Use This

- **Non-monotonic signals** (e.g. user-driven traffic with seasonality) — fit a seasonal model instead, not raw linear regression
- **High-variance signals** (queue depth in a bursty workload) — use percentile thresholds, not means
- **Signals with hard ceilings** (RAM ≤ 100%) — projection clamps; predicting "120% in 5min" is meaningless

For those, prefer EWMA, Holt-Winters, or a rolling-quantile alarm.

---

## 🧩 Related Skills

- [[HS-099]] Anatomy of an Agent — the Brain organ runs this
- [[HS-101]] Sleep Cycle + Anti-Thrash — pairs with predictive trend for proactive pausing
- [[HS-100]] Agent Lifecycle State Machine — lives in DECIDE state
- [[HS-105]] Core Agent Metrics Contract — quality metrics above belong here
- [[HS-093]] Nightly Continuous Learning Loop — `prediction_error` drift triggers retrain
