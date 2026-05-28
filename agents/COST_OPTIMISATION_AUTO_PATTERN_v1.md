# HS-045 — 💰 FRUGAL ENGINE — Cost Optimisation Auto-Pattern

> *"The swarm that pays attention to its own bills and tunes itself to spend less."*

---

## 🎯 What It Does
Autonomous cost optimisation pattern for the HyperFocus agent swarm. Monitors LLM token spend, container resource usage, and API costs — then auto-tunes to reduce waste.

## 🌍 Why It Exists
At scale, unmonitored LLM calls and idle containers drain budget fast. This pattern keeps costs visible and self-correcting.

## ⚙️ How To Use
1. Paste when building cost monitoring into any agent or the orchestrator
2. Define `[BUDGET_LIMIT]` and `[ALERT_THRESHOLD]`
3. Agent self-throttles before hitting the limit

---

## 📋 THE PROMPT

```
Add cost optimisation to: [AGENT_NAME or SYSTEM]
Monthly budget limit: [BUDGET_LIMIT]
Alert threshold: [ALERT_THRESHOLD] (e.g. 80% of budget)

MONITOR THESE COSTS:
1. LLM token spend (OpenAI/Anthropic API)
2. Container memory + CPU (Docker stats)
3. External API calls (Stripe, Supabase, Discord)
4. Storage growth (Postgres + Redis + Minio)

AUTO-TUNE RULES (in order of severity):
🟢 Under 50% budget: normal operation
🟡 50-80% budget: cache aggressive, reduce polling frequency
🟠 80-95% budget: alert Lyndz via Discord, defer non-critical tasks
🔴 95%+ budget: throttle all LLM calls, human approval required to continue

COST TRACKING SCHEMA:
```python
{
  'timestamp': datetime,
  'agent_id': str,
  'cost_type': 'llm|api|compute|storage',
  'amount_usd': float,
  'tokens_used': int,  # LLM only
  'monthly_total': float
}
```

NEVER: auto-cancel running jobs to save cost (data corruption risk)
ALWAYS: alert before throttling, log every throttle decision
```

---

## 🔗 Related Skills
- HS-043 — LOOP MASTER (Self-Improvement 5-Loop)
- HS-101 — DREAM GUARD (Sleep Cycle + Anti-Thrash)
- HS-105 — THE METRICS OATH

---
*HYPER-SKILLs Vault — welshDog 🐕🏴󠁧󠁢󠁷󠁬󠁳󠁧⚡*