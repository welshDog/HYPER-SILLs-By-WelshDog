# HS-109 — 🐕 GREP HOUND — Cross-Reference Before You Write

**Category:** `dev/`
**Source:** Original — distilled from 2026-05-21 raid sessions (avoided ~12 duplicate skills across Bible / Roster / Life Plans Master / throttle-agent raids)
**Version:** v1

---

## 🤔 What It Does

A 60-second discipline you run **before** writing a new skill, doc, function, or component. Grep the existing vault/codebase for the concept. If you find it → either link to it (don't duplicate) or extract the **delta** (what's new).

> The Bible raid yielded 12 new skills because I grepped existing ones first and skipped 5 candidates that already existed. The Life Plans Master raid only yielded 2 new skills *for the same reason*. Discipline = honesty.

---

## 🔎 The Pre-Write Grep

```bash
# In the vault root (or codebase root)
grep -ril "concept-keyword" .

# Better — match the skill header pattern
grep -ril "^# HS-.*concept-keyword" agents/ dev/ broski/

# Even better — also check related/synonym terms
for term in "circuit-breaker" "healer protocol" "approval before action"; do
  echo "=== $term ==="
  grep -ril "$term" .
done
```

If you get hits → **read the hit files first.** Don't write yet.

---

## 🎯 The Three Outcomes

After the grep, you land on exactly one of these:

### Outcome 1 — Concept exists, fully covered

**Don't write.** Link to the existing skill from wherever you needed it.

```markdown
> See [[HS-077]] User Agency Approval Gate Pattern.
```

### Outcome 2 — Concept exists, partially covered

**Update the existing skill, don't write a new one.** Bump its version + log what was added.

Example from this session: HS-091 (Top-Tier Identity Cards) had 5 cards. Life Plans Master mentioned AutoEvo as a 6th load-bearing agent. Instead of writing HS-???: "AutoEvo Card" as a new file, I bumped HS-091 → v1.1 and added a 6th card section.

```markdown
**Version:** v1.1 *(YYYY-MM-DD — added X from Y source)*
```

### Outcome 3 — Concept genuinely net-new

**Now you can write.** And because you grepped, you know exactly which existing skills to link to via `[[wikilinks]]` ([[HS-112]]).

---

## 💎 The Non-Obvious Insight

Cross-referencing isn't just about avoiding duplicates. **It's a discovery tool.**

When you grep "circuit breaker" and find HS-103 already covers it — but you were about to write something about *agent-to-agent approval* — that's not a duplicate, it's a **gap** in HS-103. Update HS-103 with the new angle (Outcome 2). The grep showed you where the existing skill was incomplete.

Most "new ideas" turn out to be either duplicates (skip) or extensions (update). Genuinely new concepts are rarer than you think — and that's *good*. A knowledge base that's mostly extensions is healthier than one of disjoint silos.

---

## 🪜 The 60-Second Workflow

```
Before writing skill X:

  1. Pick 2–3 keywords that name X's core concept
  2. grep -ril each keyword across the vault
  3. Open every hit file's header
  4. Land on Outcome 1, 2, or 3
  5. If Outcome 3 — write, with [[links]] back to every related hit
```

Sub-60 seconds. Saves hours of duplicate-skill cleanup.

---

## 🚨 Anti-patterns

- **Grepping only your folder.** Concepts cross folders. Grep `agents/`, `dev/`, `broski/` all together.
- **Trusting "I would have remembered."** You wouldn't. Memory has a 7-day half-life. Grep.
- **Grepping for exact words only.** Use synonyms. "circuit-breaker" / "approval" / "gate" / "permission" all surface related skills.
- **Skipping the grep on "just a quick small skill."** Small skills duplicate the fastest because they feel disposable.

---

## 🤖 For AI Agents

If you're a Claude agent reading this — your equivalent of `grep` is the Grep tool. Same discipline:

```
Before writing a new skill / doc / function:
  - Grep the relevant tree for the core concept
  - Read every hit's header
  - Pick Outcome 1, 2, or 3
  - Only Outcome 3 results in a new file
```

This single discipline is the difference between a vault that compounds in value and one that bloats into noise.

---

## 🧩 Related Skills

- [[HS-108]] Truth-vs-Claim Audit Pattern — sibling discipline (audit before action)
- [[HS-110]] Lean Raid Discipline — what to do when most of a source overlaps with existing
- [[HS-112]] Wikilink Knowledge Graph — how to link instead of duplicate
- [[HS-088]] Agent Final Self-Audit — "Cited Sources?" check is this skill's per-task version
