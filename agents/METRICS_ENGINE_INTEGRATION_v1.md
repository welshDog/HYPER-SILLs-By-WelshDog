# HS-041 — ⚡ METRICS ENGINE — MetricsEngine Integration (Python + Node)

## What it Does
Standard pattern for wiring any agent or service into the HyperFocus MetricsEngine. Covers both Python (FastAPI) and Node.js (HyperAgent SDK) integration patterns.

## When To Use
- Adding observability to a new agent
- Wiring Prometheus metrics into a Python service
- Connecting a Node agent to the metrics stream

## THE PATTERN
```python
# PYTHON (FastAPI) — metrics integration pattern
from prometheus_client import Counter, Histogram, Gauge, start_http_server
import time

# Standard metric types
TASK_COUNTER = Counter('agent_tasks_total', 'Total tasks', ['agent', 'status'])
LATENCY = Histogram('agent_task_duration_seconds', 'Task duration', ['agent'])
ACTIVE_TASKS = Gauge('agent_active_tasks', 'Active tasks', ['agent'])

# Decorator pattern — wrap any agent method
def track_task(agent_name: str):
    def decorator(func):
        async def wrapper(*args, **kwargs):
            ACTIVE_TASKS.labels(agent=agent_name).inc()
            start = time.time()
            try:
                result = await func(*args, **kwargs)
                TASK_COUNTER.labels(agent=agent_name, status='success').inc()
                return result
            except Exception as e:
                TASK_COUNTER.labels(agent=agent_name, status='error').inc()
                raise
            finally:
                LATENCY.labels(agent=agent_name).observe(time.time() - start)
                ACTIVE_TASKS.labels(agent=agent_name).dec()
        return wrapper
    return decorator

# Usage
@track_task('goalkeeper')
async def process_goal(goal_id: str): ...
```

```js
// NODE (HyperAgent SDK) — metrics integration
const { HyperAgent } = require('@w3lshdog/hyper-agent');

const agent = new HyperAgent({
  manifest: require('./manifest.json'),
  metrics: {
    enabled: true,
    endpoint: 'http://localhost:9090',
    labels: { agent: 'my-agent', version: '1.0.0' }
  }
});

// Emit custom metric
agent.metrics.increment('tasks_completed', { status: 'success' });
agent.metrics.timing('task_duration_ms', durationMs);
```

## Sacred Rules
- Prometheus config: `monitoring/prometheus/prometheus.yml` = ACTIVE (root = STALE)
- 5 mandatory metrics per agent (see HS-105 THE METRICS OATH)

## Related Skills
- HS-105 THE METRICS OATH Core Agent Metrics Contract
- HS-040 GOALKEEPER Self-Improving Agent
- HS-070 THE ALL-SEEING Observable Agent Operations

---
*Source: HyperCode-V2.4 | Category: agents/*
