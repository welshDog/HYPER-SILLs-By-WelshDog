# HS-044 — 🧪 AB SPLITTER — A/B Testing Framework for Agents
**Category:** agents
**Version:** 1.0


---
skill_id: HS-044
hero_name: "AB SPLITTER"
emoji: "🧪"
version: v1.0
category: agents
depends_on:
  - HS-002  # SIX_LAWS_OF_AGENTS — tests must respect agent laws
  - HS-043  # LOOP MASTER — A/B test is a sub-loop of the 5-loop
provides:
  - ab-test-prompt
  - behaviour-comparison-workflow
  - winner-promotion-pattern
related:
  - HS-120  # AB FORGE — Python code companion
  - HS-093  # NIGHT TENDER — nightly evaluation loop
graph_notes: "Prompt-block A/B testing pattern for comparing agent behaviours — use with HS-120 for implementation."
---
> *"Don't guess which agent behaviour is better. Measure it."*

---

## 🎯 What It Does
A/B testing framework for HyperFocus agents. Splits traffic between two agent behaviours, measures outcomes, and automatically promotes the winner.

## 🌍 Why It Exists
Agent tuning is guesswork without A/B tests. This framework makes improvement data-driven and automatic.

## ⚙️ How To Use
1. Paste when testing a behaviour change in any agent
2. Define variant A (current) and variant B (new)
3. Run for `[TEST_DURATION]` then evaluate

---

## 📋 THE PROMPT

```
Implement A/B test for agent: [AGENT_NAME]
Metric to optimise: [SUCCESS_METRIC]

VARIANT A (control — current behaviour):
[DESCRIBE_VARIANT_A]

VARIANT B (challenger — new behaviour):
[DESCRIBE_VARIANT_B]

SPLIT: [SPLIT_%] A / [100-SPLIT_%] B (default: 50/50)
DURATION: [TEST_DURATION] (minimum: 100 requests or 24 hours)
SUCCESS METRIC: [SUCCESS_METRIC] (e.g. response_time_p95, user_satisfaction, error_rate)

IMPLEMENTATION:
```python
import random

def route_ab(user_id: str, split_pct: int = 50) -> str:
    # Sticky assignment: same user always gets same variant
    seed = hash(user_id) % 100
    return 'A' if seed < split_pct else 'B'

@app.post('/action')
async def action(request: Request):
    variant = route_ab(request.user_id)
    result = variant_a(request) if variant == 'A' else variant_b(request)
    log_ab_result(variant, SUCCESS_METRIC, result)
    return result
```

AUTO-PROMOTE RULE:
If variant B beats A by > [MIN_IMPROVEMENT]% with > [MIN_SAMPLE] samples:
→ Promote B to control automatically
→ Alert Lyndz via Discord DM
→ Archive A to experiment_log
```

---

## 🔗 Related Skills
- HS-043 — LOOP MASTER (Self-Improvement 5-Loop)
- HS-045 — Cost Optimisation Auto-Pattern
- HS-041 — METRICS FORGE

---
*HYPER-SKILLs Vault — welshDog 🐕🏴󠁧󠁢󠁷󠁬󠁳󠁧⚡*
