# HS-041 — ⚡ METRICS FORGE — MetricsEngine Integration (Python + Node)
**Category:** agents
**Version:** 1.0


---
skill_id: HS-041
hero_name: "METRICS FORGE"
emoji: "⚡"
version: v1.0.0
status: ACTIVE
category: agents
depends_on:
  - HS-001  # ANATOMY_OF_AN_AGENT — metrics are the Eyes organ
  - HS-019  # OBSERVABLE AGENT OPERATIONS — observability schema defines what to emit
provides:
  - prometheus-wiring-pattern
  - agent-metrics-template
  - grafana-auto-scrape
  - python-and-node-support
related:
  - HS-050  # WATCHDOG PRIME — watchdog consumes these metrics
  - HS-073  # PULSE STREAM — SSE events complement Prometheus metrics
graph_notes: "Standard pattern for wiring any agent into Prometheus/Grafana — apply at agent creation, never retroactively."
problem_keywords:
  - prometheus
  - grafana
  - metrics wiring
  - scrape metrics

---
> *"Wire any agent to Prometheus metrics in under 10 minutes."*

---

## 🎯 What It Does
The standard pattern for wiring an agent into the HyperFocus MetricsEngine. Works for both Python (FastAPI) and Node (HyperAgent SDK) agents.

## 🌍 Why It Exists
Without metrics, agents are black boxes. With this pattern, every agent exposes health, throughput, and error rate to Prometheus + Grafana automatically.

## ⚙️ How To Use
1. Paste when adding metrics to any new or existing agent
2. Fill in `[AGENT_NAME]` and `[PORT]`
3. Prometheus scrapes automatically — no manual config

---

## 📋 THE PROMPT

```
Add MetricsEngine integration to agent: [AGENT_NAME] on port [PORT]

PYTHON (FastAPI) PATTERN:
```python
from prometheus_client import Counter, Histogram, Gauge, generate_latest
import time

# Standard HyperFocus metrics
REQUESTS = Counter('agent_requests_total', 'Total requests', ['agent', 'endpoint', 'status'])
LATENCY = Histogram('agent_request_duration_seconds', 'Request latency', ['agent', 'endpoint'])
ACTIVE = Gauge('agent_active_tasks', 'Active tasks', ['agent'])

@app.get('/metrics')
def metrics():
    return Response(generate_latest(), media_type='text/plain')

@app.middleware('http')
async def metrics_middleware(request, call_next):
    start = time.time()
    response = await call_next(request)
    LATENCY.labels(agent='[AGENT_NAME]', endpoint=request.url.path).observe(time.time() - start)
    REQUESTS.labels(agent='[AGENT_NAME]', endpoint=request.url.path, status=response.status_code).inc()
    return response
```

NODE (HyperAgent SDK) PATTERN:
```javascript
const { MetricsEngine } = require('@w3lshdog/hyper-agent');
const metrics = new MetricsEngine('[AGENT_NAME]');
metrics.trackRequest(endpoint, status, durationMs);
metrics.expose(app, '/metrics'); // Prometheus scrape endpoint
```

Prometheus config addition (monitoring/prometheus/prometheus.yml):
```yaml
  - job_name: '[AGENT_NAME]'
    static_configs:
      - targets: ['[AGENT_NAME]:[PORT]']
```
```

---

## 🔗 Related Skills
- HS-070 — THE ALL-SEEING (Observable Agent Operations)
- HS-105 — THE METRICS OATH
- HS-037 — GRID MASTER (Architecture Quick Ref)

---
*HYPER-SKILLs Vault — welshDog 🐕🏴󠁧󠁢󠁷󠁬󠁳󠁧⚡*
