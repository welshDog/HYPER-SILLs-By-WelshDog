# HS-110 — Lean Raid Discipline (Anti-Inflation) ⚖️

**Category:** `dev/`
**Source:** Original — coined during 2026-05-21 Life Plans Master raid (extracted 2 skills from a 354-line doc by declaring 6 sections as duplicates of existing skills)
**Version:** v1

---

## 🤔 What It Does

When extracting reusable patterns from a large source doc, **declare overlap upfront** and extract only the net-new content. Resist the temptation to inflate skill counts by re-wrapping concepts you've already captured under fresh titles.

> A vault of 100 thin skills is *less useful* than a vault of 50 dense ones. Inflated counts make navigation harder, not easier.

---

## 💎 The Core Principle

```
The job of a knowledge vault is to be NAVIGABLE.
Every duplicate skill is a fork in the road that doesn't need to exist.
Every inflated entry costs the next reader 30 seconds of "is this the same as the other one?"
30 seconds × N readers × M skills = hours of wasted attention.
```

---

## 🧪 The 3-Step Lean Raid

### Step 1 — Section-by-section overlap pass

Before writing anything, scan the source doc's table of contents and grep each section's core concept against your existing vault ([[HS-109]]).

Output: a status table you put **directly in the raid commit message** or the index update.

| Source § | Status |
|---|---|
| §1 Identity Manifest | ❌ Duplicate of [[HS-090]] — skip |
| §2 Top-tier cards | ⚠️ 3 dupes + 1 new → update [[HS-091]] to v1.1 |
| §3 4-phase roadmap | ✅ NEW (distinct cadence from [[HS-094]]) → write HS-X |
| §4 Test suite | ❌ Duplicate of [[HS-092]] — skip |
| §5 Nightly loop | ❌ Duplicate of [[HS-093]] — skip |

### Step 2 — Write only the ✅ rows

For each net-new section, write the skill. For ⚠️ rows, update the existing skill.

### Step 3 — Declare the math in the commit

```
feat: rescue HS-096 + HS-097 from Life Plans Master + HS-091 v1.1

Honest assessment: this doc is mostly a v1.0 predecessor of the Roster
doc — same Life Plan YAML, same nightly loop, same test suite.

Lean raid — only 2 net-new skills + 1 update:
  HS-096 (new) ← §3
  HS-097 (new) ← §1 dependency_graph subsection
  HS-091 v1.1  ← §2 added AutoEvo
```

The commit message becomes the receipt. Future readers see the reasoning, not just the result.

---

## 🚫 Anti-Inflation Tests

Before adding skill N+1, ask:

- [ ] Is this concept already at least 60% covered by an existing skill?
- [ ] Would a careful reader of the existing skill ALREADY do the right thing?
- [ ] Could I add this as a section in the existing skill instead of a new file?
- [ ] Am I naming the *same* concept with a *different* emoji and pretending it's new?

If any answer is "yes" → don't write a new skill. Update the existing one.

---

## ⚖️ When To Split vs Merge

| Situation | Action |
|---|---|
| Same concept, different audience (devs vs PMs) | One skill, two `## For X audience` sections |
| Same concept, different platforms (Py vs TS) | One skill, two code-block columns |
| Same concept, slightly different cadence (6-sprint vs 8-sprint roadmap) | **Two skills** — distinct templates with a "which to pick" matrix |
| Same concept, refined over time | **One skill, bumped version** (v1 → v1.1) |
| Different concepts, accidentally co-located | **Two skills** — split them out |

The borderline test: if you can write a one-sentence DECISION TREE between two candidates ("use A when X, use B when Y"), they're distinct enough to split. If you can't, they're the same skill.

---

## 📐 The Lean-Raid Receipt

Worth doing every time so the vault stays auditable:

```markdown
> *Note: <Source doc name> was largely a v1.0 predecessor of <newer doc> —
> most patterns already covered by HS-X→Y, hence the lean raid.*
```

Append this to the vault index alongside the new skill rows. Future readers see at a glance:
- Why the raid yielded only 2 skills not 7
- Which existing skills already covered the territory
- That the lean count is intentional, not lazy

---

## 🎯 The Counter-Intuitive Insight

**Inflated raids feel productive in the moment and degrade the vault in the long run.**

Writing 7 skills feels like 7× the progress of writing 2. But if 5 of the 7 are duplicates with new emojis, you've:
- Increased navigation cost for every future reader
- Made [[HS-109]] (cross-reference before writing) MORE expensive — more skills to grep through
- Eroded the trust that says "if it's in the vault, it earned its slot"

Two honest skills > seven inflated ones. Every time.

---

## 🧩 Related Skills

- [[HS-108]] Truth-vs-Claim Audit Pattern — sister discipline (be honest about reality)
- [[HS-109]] Cross-Reference Before You Write — pre-write check that feeds into this
- [[HS-111]] Surface Contradictions, Don't Pick Sides — what to do when two sources disagree
- [[HS-112]] Wikilink Knowledge Graph — links + updates beat duplicates
