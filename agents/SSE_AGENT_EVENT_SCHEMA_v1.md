# HS-073 — 📡 PULSE STREAM — SSE Agent Event Schema


---
skill_id: HS-073
hero_name: "PULSE STREAM"
emoji: "📡"
version: v1.0
category: agents
depends_on:
  - HS-001  # ANATOMY_OF_AN_AGENT — Voice organ defines what agents emit
  - HS-083  # THE THREE VOICES — streaming is one of the three comms patterns
provides:
  - sse-event-schema
  - real-time-agent-events
  - frontend-streaming-contract
  - typescript-event-interface
related:
  - HS-019  # OBSERVABLE AGENT OPERATIONS — logs + metrics complement SSE events
  - HS-041  # METRICS FORGE — Prometheus and SSE are parallel observability streams
graph_notes: "Canonical SSE schema for streaming real-time agent activity to the frontend — every agent emits structured events so the timeline UI stays live."
---
**Category:** `agents/`  
**Source:** HyperCode-V2.4 — `agents/HYPER-AGENT-BIBLE.md` §4  
**Version:** v1  

---

## 🤔 What It Does

Defines the canonical Server-Sent Events (SSE) schema for streaming real-time agent activity to the frontend (BROski Terminal). Every agent emits structured events so the timeline UI can display what's happening live.

---

## 📡 Event Interface

```typescript
interface AgentEvent {
  event: string;      // Event type
  agent: string;      // Agent name
  timestamp: string;  // ISO 8601
  trace_id?: string;  // For tracing
  data?: any;         // Event-specific data
}
```

---

## 📋 All Standard Event Types

```python
# Task Lifecycle
"task_started"
"task_progress"     # data.progress: 0-100
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

## 🐍 Emission Examples

```python
# Task start
await emit_event({
    "event": "task_started",
    "agent": "Backend Specialist",
    "timestamp": datetime.now().isoformat(),
    "trace_id": "abc123",
    "data": {
        "task": "Implement JWT middleware",
        "estimated_duration_seconds": 120
    }
})

# Progress update
await emit_event({
    "event": "task_progress",
    "agent": "QA Specialist",
    "timestamp": datetime.now().isoformat(),
    "data": {
        "progress": 60,
        "current_step": "Running test suite 6/10"
    }
})

# Failure with recovery hint
await emit_event({
    "event": "task_failed",
    "agent": "Backend Specialist",
    "timestamp": datetime.now().isoformat(),
    "data": {
        "error": "Connection refused",
        "recovery_suggestion": "Check if database is running"
    }
})
```

---

## ⚛️ Frontend SSE Subscription (React)

```typescript
function useAgentEvents(url: string) {
  const [events, setEvents] = useState<AgentEvent[]>([]);

  useEffect(() => {
    const eventSource = new EventSource(url);
    eventSource.onmessage = (event) => {
      const parsed: AgentEvent = JSON.parse(event.data);
      setEvents(prev => [...prev, parsed]);
    };
    return () => eventSource.close();
  }, [url]);

  return events;
}
```

---

## 🎯 THE PROMPT

```
Add SSE event emission to this agent function:

[PASTE FUNCTION HERE]

Emit:
1. task_started — at function entry with trace_id
2. task_progress — after each major step (progress: 0-100)
3. task_completed — on success with duration_ms
4. task_failed — on exception with error + recovery_suggestion

Use ISO 8601 timestamps. Include agent name: "[AGENT_NAME]".
```

---

## 🔗 Related Skills
- HS-070 Observable Agent Operations Pattern
- HS-068 BROski Orchestrator Pattern
- HS-074 API Standards FastAPI Pattern
