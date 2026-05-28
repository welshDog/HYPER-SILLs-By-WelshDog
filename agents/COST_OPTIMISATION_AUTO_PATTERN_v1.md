# HS-045 — 💰 COST OPTIMISATION AUTO — Cost Optimisation Auto-Pattern

## What it Does
Automatic cost optimisation pattern for LLM-powered agents. Routes requests to the cheapest model capable of handling the task, with fallback escalation.

## When To Use
- Building any LLM-powered agent that calls external APIs
- Reducing OpenAI / Anthropic spend in production
- Implementing tiered model routing

## THE PATTERN
```python
from enum import Enum
from typing import Optional

class ModelTier(Enum):
    FAST = 'gpt-4o-mini'       # cheap, fast — simple tasks
    STANDARD = 'gpt-4o'        # mid — complex reasoning
    POWER = 'claude-opus-4'    # expensive — last resort

def classify_task_complexity(task: str) -> ModelTier:
    """Route to cheapest capable model."""
    word_count = len(task.split())
    has_code = any(kw in task.lower() for kw in
                   ['debug', 'refactor', 'architect', 'design'])
    has_analysis = any(kw in task.lower() for kw in
                       ['analyse', 'compare', 'evaluate', 'strategy'])

    if has_code or has_analysis:
        return ModelTier.POWER
    elif word_count > 200:
        return ModelTier.STANDARD
    else:
        return ModelTier.FAST

async def smart_llm_call(task: str, force_tier: Optional[ModelTier] = None):
    tier = force_tier or classify_task_complexity(task)

    try:
        return await call_model(tier.value, task)
    except RateLimitError:
        # Escalate on rate limit, not on capability
        if tier == ModelTier.FAST:
            return await call_model(ModelTier.STANDARD.value, task)
        raise
    except ContextLengthError:
        # Escalate on context, not on capability
        return await call_model(ModelTier.POWER.value, task)

# Cost tracking (emit to MetricsEngine HS-041)
COST_COUNTER = Counter('llm_cost_usd', 'LLM spend', ['model', 'agent'])
```

## Cost Targets
- FAST: ~$0.00015 per 1K tokens
- STANDARD: ~$0.005 per 1K tokens  
- POWER: ~$0.075 per 1K tokens
- Default rule: start FAST, escalate only on capability or context failure

## Related Skills
- HS-041 METRICS ENGINE Integration
- HS-103 HEALER’S CHORUS Circuit-Breaker Protocol

---
*Source: HyperCode-V2.4 | Category: agents/*
