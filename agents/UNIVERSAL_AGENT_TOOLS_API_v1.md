# HS-080 — 🧰 THE TOOL BELT — Universal Agent Tools API

**Category:** `agents/`
**Source:** HyperCode-V2.4 — `agents/HYPER-AGENT-BIBLE.md` §3
**Version:** v1

---

## 🤔 What It Does

The minimum tool surface every BROski-crew agent must expose. Anything not in this list is role-specific (see [[HS-079]]). Use as a checklist when stubbing a new agent or auditing an existing one.

---

## 📁 File Operations

```python
await read_file(path: str) -> str
await write_file(path: str, content: str, require_approval: bool = True)
await list_files(directory: str, pattern: str = "*") -> List[str]
await file_exists(path: str) -> bool
```

> `require_approval=True` is the default — links to [[HS-077]] gate.

---

## 🔎 Search

```python
await search_files(
    pattern: str,
    directory: str = ".",
    file_type: str = "*"
) -> List[str]

await search_code(
    query: str,
    file_types: List[str] = ["*.py", "*.ts", "*.tsx"]
) -> List[SearchResult]
```

---

## 🧠 Context Management

```python
await create_context(name: str, value: dict)
await read_context(name: str) -> dict
await update_context(name: str, value: dict)
await delete_context(name: str)
await list_contexts() -> List[str]
```

> Schema + naming convention = [[HS-082]].

---

## 📝 Logging

```python
await log_info(message: str, **kwargs)
await log_warning(message: str, **kwargs)
await log_error(message: str, **kwargs)
```

---

## 📡 Events (SSE timeline)

```python
await emit_event(event: dict)
```

> Event schema = [[HS-073]].

---

## 💬 User Communication

```python
await ask_user(question: str) -> str
await inform_user(message: str, priority: str = "normal")
await request_approval(plan: str) -> bool
```

> Priority levels + when-to-interrupt = [[HS-078]].
> Approval gate semantics = [[HS-077]].

---

## ✅ Quick Audit Checklist

When you add a new agent, verify it exposes:
- [ ] All 4 file ops
- [ ] Both search functions
- [ ] All 5 context functions
- [ ] All 3 log levels
- [ ] `emit_event`
- [ ] All 3 user-comm functions

Missing any of these = agent can't participate in the standard crew loop.

---

## 🧩 Related Skills

- [[HS-079]] Specialist Agent Role Definitions — what each specialist adds **on top of** this base
- [[HS-081]] MCP Server + Agent Registration — how to expose these via MCP
- [[HS-073]] SSE Agent Event Schema
- [[HS-077]] User Agency Approval Gate
