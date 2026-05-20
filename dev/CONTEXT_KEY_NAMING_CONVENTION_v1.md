# HS-082 — Context Key Naming Convention + Value Schema 🏷️

**Category:** `dev/`
**Source:** HyperCode-V2.4 — `agents/HYPER-AGENT-BIBLE.md` §4 + §7
**Version:** v1

---

## 🤔 What It Does

Defines the dot-notation key format and the structured value schema for every entry in the BROski context store. Stops the store from devolving into a key-value swamp. Use this whenever an agent calls `create_context()` or `update_context()`.

> Sits on top of the store architecture defined in [[HS-072]].

---

## 🔑 Key Format

```
{domain}.{subdomain}.{specific}
```

**Good:**
```
api.routes.current_structure
auth.design.jwt_strategy
language.grammar.version_0
frontend.editor.monaco_config
```

**Bad:**
```
stuff                          # too vague
the_api_routes_we_found        # not structured
data                           # too generic
api_routes_current_structure   # underscores instead of dots
```

---

## 📦 Value Schema (required)

```python
{
    "created_at": "2026-02-03T16:00:00Z",
    "created_by": "Backend Specialist",
    "version": 1,
    "data": {
        # actual context payload
    },
    "metadata": {
        "source_files": ["app/routers/execution.py"],
        "confidence": "high",       # high | medium | low
        "expires_at": None          # ISO-8601 or None
    }
}
```

**Mandatory fields:** `created_at`, `created_by`, `version`, `data`.
**Recommended fields:** `metadata.source_files`, `metadata.confidence`.
**Optional:** `metadata.expires_at` — set for ephemeral contexts (e.g. "current build status").

---

## ✅ DO

- Use structured hierarchical keys
- Include metadata (source, confidence, timestamp)
- Keep contexts focused and single-purpose
- Version contexts when they evolve (`version: 2`, then 3…)
- Expire contexts that become stale

## ❌ DON'T

- Store full file contents (use summaries instead — referenced by `source_files`)
- Create vague keys (`data`, `stuff`)
- Let contexts grow unbounded — set size limits per key
- Store secrets unencrypted
- Create circular dependencies (`api.x` points to `api.y` which points back to `api.x`)

---

## 🧪 Quick Lint

Before writing a context, check:
- [ ] Key has ≥ 2 dots
- [ ] All required value fields present
- [ ] `confidence` set
- [ ] `data` payload < 100 kB (else summarise + link to source files)

---

## 🧩 Related Skills

- [[HS-072]] Context Store Architecture (Redis) — the underlying store
- [[HS-080]] Universal Agent Tools API — context functions every agent has
- [[HS-068]] BROski Orchestrator — creates context slots before delegating
