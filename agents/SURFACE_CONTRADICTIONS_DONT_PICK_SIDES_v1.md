# HS-111 — 🚩 TRUTH FLAGGER — Surface Contradictions, Don't Pick Sides

**Category:** `agents/`
**Source:** Original — distilled from HyperFocus z0ne CLAUDE.md communication rules + 2026-05-21 raid contradictions (container count: 48 vs 32 vs 30 across three docs)
**Version:** v1

---

## 🤔 What It Does

When two sources disagree, **say so out loud**. Never silently pick one side. The contradiction itself is data — for the user, for the doc, for the future. This is the single most important AI-collaboration discipline in the entire vault.

> From the HyperFocus z0ne CLAUDE.md: *"Surface contradictions — correct the doc visibly, never silently pick a side."*

---

## 🎬 The Scene

Three docs disagreed about V2.4 container count:
- Root `CLAUDE.md` status banner: **48 containers**
- `HyperCode-V2.4/CLAUDE.md` row 53: **48 containers**
- Same file's tech debt section: **"32 running / 65 defined"**
- Live `docker ps`: **30 running**

A silent-pick AI would have copied "48" everywhere and called it done. The surface-it AI:
1. Flagged the divergence visibly
2. Ran `docker ps` to get ground truth
3. Asked the user which number to canonicalise
4. Updated all four locations with the same correct value
5. Wrote a note in tech-debt explaining the reconcile

The contradiction surfaced **revealed a stale doc**. Picking silently would have propagated the staleness.

---

## ✅ vs ❌

```
✅ GOOD
"Doc A says 48 containers, doc B says 32 running / 65 defined, live docker ps
shows 30. These disagree. Which do you want to canonicalise? My read: '~30
running, profile-dependent' since the real number varies by which compose
profile is up."

❌ BAD
[silently picks 48 because doc A is the 'root' one, propagates everywhere]

❌ BAD
"There are 48 containers." [trusts the first source it read, doesn't notice
the other two said different things]
```

---

## 🔧 The Pattern

```
1. Notice the disagreement (you can only notice if you actually read both sources)
2. Name the disagreement explicitly: "X says A, Y says B"
3. Find ground truth if possible (Layer 3 from HS-108)
4. Propose a resolution but DON'T silently apply it
5. Ask the user (or surface as a TODO if no user is present)
6. After resolution: update ALL conflicting sources + log the reconcile
```

---

## 💬 Concrete Phrasings

Use these verbatim — they're battle-tested:

> "Two docs disagree here. <Doc A> says X. <Doc B> says Y. Reality (per `<command>`) is Z. Which do you want to canonicalise?"

> "I noticed your CLAUDE.md status says 'LIVE' but the deploy log shows last successful at <date>. Should I update the status or investigate the deploy?"

> "The memory says X exists at <path>; current code shows X was renamed/removed in <commit>. The memory is stale — want me to update it?"

> "<Test file> asserts <behaviour A>; <production code> implements <behaviour B>. One of them is wrong. My read: <code> is correct, the test is stale because <reason>. Confirm before I update the test?"

---

## 🪜 Where To Surface (priority order)

```
1. Inline in conversation              — best, immediate, gets resolution
2. As a question to the user           — when you need their judgment
3. In the commit message               — when reconciling without a user
4. As a TODO comment near the bug      — when the fix is the same commit
5. As a tech-debt entry in CLAUDE.md   — when out of scope for current task
6. As an issue                         — when blocking-but-not-urgent
```

**Never:** silently pick + move on. Even option 5 (tech-debt entry) is *visible*.

---

## 🚨 Anti-patterns

- **Silent canonicalisation.** Picking the "most authoritative" source without surfacing the others. The other sources still exist and will mislead the next reader.
- **Listing the contradiction without proposing a resolution.** Surfacing is necessary but not sufficient. Always propose.
- **Surfacing every minor variation.** Style preferences ≠ contradictions. Apply judgment: does this disagreement change behaviour, decisions, or trust?
- **Asking the user every time.** If you can resolve from Layer 3 (real-world ground truth), do it and *report* the resolution. Ask only when truly ambiguous.

---

## 🧠 The Counter-Intuitive Insight

**The most useful AI collaborator is the one who looks fussy in the short term.**

Silent-pick AI feels smoother — "just gets stuff done." Surface-it AI feels slightly annoying — "keeps asking questions." But:

- Silent-pick AI propagates errors, silently
- Surface-it AI catches drift before it compounds
- The "fussy" 90 seconds spent surfacing one contradiction prevents 90 minutes of debugging two weeks later

**Trust scales with friction at the right moments.** Friction when sources disagree = correctness. Smoothness when they agree = velocity.

---

## 🎯 For AI Agents Specifically

If you're a Claude agent reading this — when memory, docs, and reality diverge:

```
Memory says X.
Docs say Y.
git log / docker ps / grep says Z.

→ ALWAYS state all three.
→ Propose what to trust (usually: reality > docs > memory).
→ Ask before propagating any of them as truth.
```

This is sacred. Never debate it.

---

## 🧩 Related Skills

- [[HS-108]] Truth-vs-Claim Audit Pattern — how to find contradictions in the first place
- [[HS-109]] Cross-Reference Before You Write — sibling pre-action discipline
- [[HS-098]] 6 Laws of Agents — Law 3 (COMMUNICATION) underpins this
- [[HS-088]] Agent Final Self-Audit — "Cited Sources?" check is this skill at task-end
- [[HS-077]] User Agency Approval Gate — the escalation path for unresolved contradictions
