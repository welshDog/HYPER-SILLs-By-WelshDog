# .skill-memory/ — HYPER-SILLs usage learning loop

Git-tracked, lightweight usage memory. Skills get smarter the more they're used.

| File | What it holds |
|---|---|
| `usage-log.jsonl` | One JSON line per session: `{ts, skills, task, success}` |

**How it fills:** the `sills_session_end.py` hook scans the session transcript for
skill IDs (`HS-NNN` / `DS-NNN`) and appends a record automatically. You can also
record manually:

```bash
python scripts/skill_memory.py record "HS-128,HS-129" "shipped a plugin"
```

**Analyse it:**

```bash
python scripts/hyper_brain_ops.py analyze-skill-usage
# → most-used skills, co-occurrence super-pack candidates, never-used drift list
```

The log is append-only JSONL so it's cheap to write and conflict-free across branches.
