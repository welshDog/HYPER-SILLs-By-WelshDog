# HS-112 — Wikilink Knowledge Graph for Docs 🕸️

**Category:** `dev/`
**Source:** Original — the convention used throughout the HYPER-SILLs vault (every skill from HS-067 onwards uses `[[HS-###]]` cross-links)
**Version:** v1

---

## 🤔 What It Does

A doc-linking convention that turns a folder of files into a navigable knowledge graph. Use `[[HS-###]]` (or `[[skill-slug]]`) inline. Two outcomes: forward-link to anything that exists (resolves) and forward-link to anything that *should* exist (TODO marker, doesn't resolve, intentional).

> The vault grew from 35 to 66 skills in two days with zero "wait, do we have something for X?" rounds — because the wikilinks made the graph self-navigating.

---

## 🔗 The Syntax

```markdown
The full pattern: see [[HS-090]] Universal Life Plan YAML — schema each agent implements.

Or: drives the Sleep organ ([[HS-101]]) anti-thrash logic.

For orphan refs (skill not yet written): see [[HS-???]] Pet Skill Rotation Pattern.
```

Two-bracket convention is borrowed from Obsidian/Roam/Notion. Renders as plain text in any markdown — no fancy tooling required.

---

## 🌱 The Three Link Types

### Type 1 — Existence link (resolves)

```markdown
See [[HS-090]] Universal Life Plan YAML.
```

The skill `HS-090_*.md` exists in the vault. Reader can navigate to it. Standard usage.

### Type 2 — Orphan link (intentional TODO)

```markdown
See [[HS-???]] Quick-Win Momentum Loop.
```

The skill doesn't exist yet — but referencing it from another skill MARKS it as worth writing. When you next ask "what should I write next?", grep for `[[HS-???]]` and `[[HS-` patterns that don't resolve to a file. **Those are your TODOs.**

### Type 3 — Concept link (alias)

```markdown
See [[approval-gate]] for the discipline.
```

Use a concept name instead of an ID when the link is semantic. Useful when IDs change or get renumbered. Less rigid, more readable, but no auto-resolution.

---

## 💎 The Non-Obvious Insight

**Orphan links aren't broken — they're the most valuable signal in the vault.**

When a skill says "see [[HS-???]] Pet Rotation" and no such skill exists yet, three things just happened:
1. You discovered a concept that *deserves* its own skill
2. You marked it as worth writing
3. The next time someone searches the vault for "pet rotation" they hit at least one existing skill that references it — context preserved

This is the opposite of how most doc systems treat orphan links (as errors to fix). In a growing vault, **orphans are seeds**.

---

## 📐 The Linking Discipline

When writing or updating a skill:

1. **Link to every related existing skill in the `## Related Skills` section.** Bidirectional is ideal — if you link to HS-090, ideally HS-090 links back.
2. **Link inline mid-content when natural.** "Implements Law 5 ([[HS-098]]) at the code level." Not every mention needs a link, but key references should resolve.
3. **Orphan-link liberally for sister concepts.** If HS-103 needs a "queue-pressure" sibling that doesn't exist yet, write `[[HS-???]] Queue Pressure Protocol` and move on. It becomes a self-generated TODO.
4. **Don't backfill orphan links eagerly.** Wait until you write the missing skill, then update the resolved links.

---

## 🪜 Maintenance Recipes

```bash
# Find all skills that link to HS-XXX (its "depended_by" set)
grep -l '\[\[HS-090\]\]' agents/ dev/ broski/

# Find all orphan links (worth writing)
grep -roh '\[\[HS-[0-9?]*\]\]' . | sort -u > all_links.txt
ls agents/*.md dev/*.md broski/*.md | sed 's/.*HS-\([0-9]*\).*/\1/' | sort -u > existing_skills.txt
# Diff to find orphans

# Walk the graph backwards: which skills depend on this one?
grep -rln '\[\[HS-085\]\]' .   # all skills that link to "5 Mandatory Guardrails"
```

---

## 🎯 What This Replaces

| Without wikilinks | With wikilinks |
|---|---|
| Manual "see also" lists that rot | Inline links the eye follows naturally |
| `TODO.md` file that goes stale | Orphan links co-located with the context that needs them |
| Index that has to be maintained by hand | Vault-index that *cross-references* the wikilink graph |
| "Did I write something about X?" → manual grep | Pre-write `grep` for `[[concept]]` references finds you immediately |

---

## 🚨 Anti-patterns

- **Bare URLs instead of links.** `(see /agents/HEALER_CIRCUIT_BREAKER_PROTOCOL_v1.md)` — fragile, breaks on rename. Use `[[HS-103]]`.
- **Linking everything.** If half your prose is links, none of them stand out. Link key concepts only.
- **Renumbering skills frequently.** Wikilinks break on renumber. Treat HS IDs as immutable once assigned.
- **Forgetting back-references.** When HS-X links to HS-Y, ideally HS-Y eventually links back. Bidirectional graphs are navigable in both directions.

---

## 🧩 Related Skills

- [[HS-109]] Cross-Reference Before You Write — grep the vault, find the existing links
- [[HS-110]] Lean Raid Discipline — link to existing instead of duplicating
- [[HS-108]] Truth-vs-Claim Audit — verify a link target actually exists (Layer 2)
- [[HS-082]] Context Key Naming Convention — sibling discipline for context store keys
