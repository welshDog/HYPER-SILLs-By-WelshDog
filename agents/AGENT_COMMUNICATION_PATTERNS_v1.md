# HS-083 — 🗣️ THE THREE VOICES — Agent Communication Patterns (Req-Res, Stream, Error)


---
skill_id: HS-083
hero_name: "THE THREE VOICES"
emoji: "🗣️"
version: v1.0.0
status: ACTIVE
category: agents
depends_on:
  - HS-067  # THE THRONE LADDER — roles determine who talks to whom
  - HS-008  # BROSKI ORCHESTRATOR PATTERN — orchestrator drives comms
provides:
  - request-response-pattern
  - streaming-pattern
  - error-signalling-pattern
  - inter-agent-comms
related:
  - HS-073  # PULSE STREAM — SSE schema for streaming events
  - HS-080  # THE TOOL BELT — tools use these patterns
graph_notes: "Three canonical inter-agent comms patterns (req-res, streaming, errors) — every agent-to-agent call uses one of these three."
---
**Category:** `agents/`
**Source:** HyperCode-V2.4 — `agents/HYPER-AGENT-BIBLE.md` §4
**Version:** v1

---

## 🤔 What It Does

Three canonical patterns for inter-agent comms in the BROski crew. Every agent-to-agent interaction lands in one of these. Pick the right one or you'll either block the UI (request-response on a long task) or flood the timeline (streaming on something instant).

---

## 1️⃣ Request-Response (default, short tasks)

For sub-second to ~30s synchronous calls.

```python
# BROski delegates to specialist
result = await delegate_task(
    agent="Language Specialist",
    task="Parse this HyperCode",
    contexts=["language.grammar.version_0"],
    timeout=30
)
```

**Use for:** parsing, validation, single API calls, fixture lookups.
**Don't use for:** anything > 30s — switch to streaming.

---

## 2️⃣ Streaming Progress (long tasks)

For multi-step or > 30s work where the user wants to see motion.

```python
async def long_running_task():
    total_steps = 10

    for step in range(total_steps):
        await do_work(step)

        await emit_event({
            "event": "task_progress",
            "agent": "QA Specialist",
            "data": {
                "progress": int((step + 1) / total_steps * 100),
                "current_step": f"Running test suite {step + 1}/{total_steps}"
            }
        })
```

**Use for:** test suites, batch builds, multi-agent orchestration, anything the user might think hung.
**Required:** emit `task_progress` at minimum every 5s OR every meaningful step boundary, whichever comes first.

---

## 3️⃣ Error Propagation (when it goes wrong)

Never let an agent crash silently. The crew needs to see the failure on the timeline AND get a structured result back.

```python
try:
    result = await risky_operation()
except Exception as e:
    # Log
    await log_error(
        "Operation failed",
        error=str(e),
        agent="Backend Specialist"
    )

    # Emit to timeline
    await emit_event({
        "event": "task_failed",
        "agent": "Backend Specialist",
        "data": {
            "error": str(e),
            "recovery_suggestion": "Check API connectivity"
        }
    })

    # Return graceful failure — DO NOT raise
    return TaskResult(
        success=False,
        error=str(e),
        recovery_suggestion="Check API connectivity"
    )
```

**Three-step rule:** **log → emit → return graceful**. Skip any and the orchestrator can't synthesise.

---

## 🎯 Quick Picker

| Task duration | User waiting? | Pattern |
|---|---|---|
| < 30 s | Yes | Request-Response |
| > 30 s | Yes | Streaming Progress |
| Anything | Failed | Error Propagation |
| Background, low priority | No | Request-Response + low-priority notify ([[HS-078]]) |

---

## 🧩 Related Skills

- [[HS-073]] SSE Agent Event Schema — event types catalog
- [[HS-071]] Fail Gracefully + Fallback Chain — what to do *before* error propagation
- [[HS-070]] Observable Agent Operations Pattern
- [[HS-078]] Context Retention — low-priority notify path
