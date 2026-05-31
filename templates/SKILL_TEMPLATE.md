# HS-NNN — 🦸 HERO NAME — Short Skill Title

---
skill_id: HS-NNN
hero_name: "HERO NAME"
emoji: "🦸"
version: v1.0
category: agents  # agents | dev | content | youtube | broski
depends_on:
  - HS-XXX  # Skill this one builds on — e.g. HS-098 SACRED SIX
  # Add more dependencies, or '- none' if truly standalone
provides:
  - feature-slug-one      # What downstream skills can consume from this one
  - pattern-name-two
related:
  - HS-YYY  # Lateral reference — not a hard dependency, just connected
graph_notes: "One sentence: where this skill sits in the graph and what it connects."
---

**Category:** `agents/`
**Source:** HyperCode-V2.4 — `path/to/source/file`
**Version:** v1

---

## 🤔 What It Does

> One-line summary. What problem does this skill solve? Why does it exist?

Expand to 2–3 sentences max. Plain English — no jargon until the How section.

---

## 🎯 Purpose

- **Who uses it:** Which agents or humans reach for this skill?
- **When to use it:** What triggers reaching for this skill?
- **What it unlocks:** What becomes possible once you have it?

---

## 📥 Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `param_name` | `string` | ✅ | What it is |
| `optional_param` | `int` | ❌ | What it does |

---

## 📤 Output Format

```json
{
  "status": "ok",
  "result": "..."
}
```

---

## 🔮 Prompt Block

```
You are a [ROLE].

Given [CONTEXT], your job is to [TASK].

Rules:
1. [Rule one]
2. [Rule two]
3. [Rule three]

Output format:
[Describe expected output]
```

---

## 💡 Example Usage

```python
# One concrete example — copy-paste ready
result = skill_function(
    param="value",
    optional=42
)
print(result)  # Expected: {...}
```

---

## 🚨 Anti-patterns

- **Don't do X** — because Y happens
- **Don't do A** — use B instead

---

## 🔗 Related Skills

- [[HS-XXX]] Skill Name — why it's related
- [[HS-YYY]] Another Skill — how they connect

---

## 📋 THE PROMPT

> Copy this block into any AI session to activate the skill:

```text
Use skill HS-NNN [HERO NAME]. [One-sentence instruction for the AI.]
```
