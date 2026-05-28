# HS-044 — 🧪 A/B TESTING FRAMEWORK — A/B Testing Framework for Agents

## What it Does
Standard A/B testing pattern for comparing two agent behaviours, prompts, or decision paths. Used in the self-improvement loop to safely test changes before committing them.

## When To Use
- Testing a new agent prompt against the current one
- Comparing two decision paths in an agent
- Shadow-mode testing before a behaviour change goes live

## THE PATTERN
```python
import random
from dataclasses import dataclass
from typing import Callable, Any

@dataclass
class ABVariant:
    name: str          # 'control' or 'treatment'
    weight: float      # 0.0-1.0, control + treatment = 1.0
    handler: Callable

class AgentABTest:
    def __init__(self, test_id: str, variants: list[ABVariant]):
        self.test_id = test_id
        self.variants = variants
        self.results = {'control': [], 'treatment': []}

    def assign(self, user_id: str) -> ABVariant:
        # Deterministic assignment by user_id hash
        seed = hash(f'{self.test_id}:{user_id}') % 100
        cumulative = 0
        for variant in self.variants:
            cumulative += variant.weight * 100
            if seed < cumulative:
                return variant
        return self.variants[-1]

    async def run(self, user_id: str, input_data: Any) -> Any:
        variant = self.assign(user_id)
        result = await variant.handler(input_data)
        self.results[variant.name].append({
            'user_id': user_id,
            'result': result,
            'variant': variant.name
        })
        return result

    def winner(self, metric: str = 'success_rate') -> str:
        # Returns 'control' or 'treatment'
        # Compare metric across results
        # Promote treatment only if delta > 5%
        ...

# Usage
test = AgentABTest('prompt-v2-test', [
    ABVariant('control', 0.5, old_handler),
    ABVariant('treatment', 0.5, new_handler),
])
result = await test.run(user_id='lyndz_123', input_data=task)
```

## Sacred Rules
- Shadow mode first (HS-043 Loop 4)
- Promote only if delta > threshold
- All results logged to governance ledger (HS-095)

## Related Skills
- HS-043 Self-Improvement 5-Loop Logic
- HS-095 THE LEDGER LAW Governance Ledger

---
*Source: HyperCode-V2.4 | Category: agents/*
