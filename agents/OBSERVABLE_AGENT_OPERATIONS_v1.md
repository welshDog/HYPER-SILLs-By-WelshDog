# HS-070 — 👁️ THE ALL-SEEING — Observable Agent Operations Pattern

**Category:** `agents/`  
**Source:** HyperCode-V2.4 — `agents/HYPER-AGENT-BIBLE.md` §1 Principle 4 + §4  
**Version:** v1  

---

## 🤔 What It Does

Every agent action must be traceable, measurable, and debuggable. This skill gives you the pattern for logging, metrics, and event emission so nothing in your agent system is a black box.

---

## 🏗️ Core Decorators

```python
@trace_operation   # Log start/end with trace_id
@emit_metrics      # Record duration, status, cost
@handle_errors     # Structured error logging
async def agent_function():
    pass
```

---

## 📡 Event Emission Pattern

```python
# On start
await emit_event({
    "event": "task_started",
    "agent": "Backend Specialist",
    "task_id": "abc123",
    "timestamp": datetime.now().isoformat()
})

# Do work...

# On complete
await emit_event({
    "event": "task_completed",
    "agent": "Backend Specialist",
    "task_id": "abc123",
    "duration_ms": 1234,
    "success": True
})
```

---

## 📊 Standard Event Types

```python
# Task Lifecycle
"task_started"
"task_progress"   # With progress: 0-100
"task_completed"
"task_failed"

# Context Operations
"context_created"
"context_updated"
"context_deleted"

# Execution
"execution_started"
"execution_completed"
"execution_failed"

# Delegation
"delegation_started"
"delegation_completed"

# System
"agent_registered"
"agent_heartbeat"
"agent_disconnected"
```

---

## 📈 Prometheus Metrics to Add

```python
from prometheus_client import Counter, Histogram, Gauge

http_requests_total = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint", "status"]
)

http_request_duration_seconds = Histogram(
    "http_request_duration_seconds",
    "HTTP request duration",
    ["method", "endpoint"]
)

agent_task_duration_seconds = Histogram(
    "agent_task_duration_seconds",
    "Agent task duration",
    ["agent_name", "task_type"]
)

agent_task_status_total = Counter(
    "agent_task_status_total",
    "Agent task status",
    ["agent_name", "status"]
)
```

---

## 🎯 THE PROMPT

```
Add observability to this agent function:

[PASTE FUNCTION HERE]

Add:
1. Emit task_started event with trace_id + timestamp
2. Emit task_progress events if multi-step
3. Emit task_completed or task_failed on finish
4. Add Prometheus Counter + Histogram for this operation
5. Log errors with structlog including trace_id

Use this event schema:
{ "event": str, "agent": str, "task_id": str, "timestamp": ISO8601, "data": dict }
```

---

## 🔗 Related Skills
- HS-073 SSE Agent Event Schema
- HS-068 BROski Orchestrator Pattern
- HS-074 API Standards FastAPI Pattern
