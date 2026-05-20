# HS-108 — 🔱 REALITY ANCHOR — Truth-vs-Claim Audit Pattern

**Category:** `dev/`
**Source:** Original — distilled from 2026-05-21 raid lessons (phantom commits in HYPER-SILLs vault-index, container count drift across CLAUDE.md files, empty Bible stubs)
**Version:** v1

---

## 🤔 What It Does

A three-layer audit pattern for spotting **doc drift** before you act on a claim. Used when any "source of truth" doc names a concrete artifact (file path, container count, deployed feature, ticket status). Saves you from chasing ghosts.

> Lesson from this very vault: `vault-index.md` claimed 66 rescued skills. Disk had 35 files. 37 entries pointed at folders that didn't exist. The index wasn't malicious — just optimistic. **Most docs are.**

---

## 🔍 The 3 Layers

```
LAYER 1 — What the doc CLAIMS
  "We have X. Path is Y. It does Z."

LAYER 2 — What the disk SHOWS
  ls / grep / git ls-tree — does the file exist? At that path?

LAYER 3 — What the behaviour DOES
  curl / docker ps / actual runtime — does it actually work?
```

A claim is **only trustworthy when all three match.** If Layer 1 ≠ Layer 2 → silent fiction. If Layer 2 ≠ Layer 3 → bit-rotted infra. If all three diverge → the doc is dangerous.

---

## ⏰ When To Run It

**Best time: BEFORE you take action based on the doc.**

After-action audits assign blame; pre-action audits prevent damage. Run when:

- A doc tells you to use a tool / path / endpoint you haven't personally used in the last week
- A status banner says "✅ LIVE" — verify with Layer 3
- A roster, ledger, or index claims completeness — sample 5 random entries with Layer 2
- A teammate (or your past self) says "we have X already" — verify before duplicating

**Skip when:** the doc is your own commit message from the last hour. Trust freshness.

---

## 🧰 Quick Recipes

```bash
# Layer 2 — does the file exist?
ls -la <path>

# Layer 2 — was the commit only metadata, or did it add real content?
git show --stat <sha>           # if file count = 0 and the commit "added" things,
                                # that's the phantom-commit pattern

# Layer 2 — what's actually tracked vs what the index claims?
git ls-tree -r --name-only HEAD | sort > tracked.txt
# compare against the index's claimed list

# Layer 3 — is the service the doc says is "live" actually responding?
curl -fsS <url>/health | jq .

# Layer 3 — is the running container count what the doc claims?
docker ps -q | wc -l
```

---

## 🎯 The Phantom-Commit Smell

A specific Layer 2 failure mode worth naming: commits that **say** they added skills/features/tests but only touched the index doc. Spot them with `git show --stat`:

```
chore: add HS-052 to HS-058 from BROSKI_PETS_INTEGRATION_PLAN raid
 vault-index.md | 19 +++++++++++++------    ← ONLY the index changed
 1 file changed, 13 insertions(+), 6 deletions(-)
```

If the commit message claims a new artifact but the diff only touches one doc → the artifact doesn't exist. Add it to the "catalogued, not yet built" list and move on.

---

## 🚨 Anti-patterns

- **Silently picking a side when sources disagree.** Either reconcile or surface — never quietly pick. See [[HS-111]].
- **Auditing only after a failure.** The cheap audit is before action; the expensive one is after damage.
- **Auditing the docs *for* the docs.** Audit against disk and behaviour, not against other docs (which may have drifted in the same direction).
- **Single-layer trust.** Three layers exist because each lies in different ways.

---

## 🪜 The Audit Output Format

When you find drift, write the reconciliation visibly:

```markdown
## Honesty pass YYYY-MM-DD

| What it claimed | What is actually true | Action |
|---|---|---|
| 66 rescued skills | 35 files on disk | Demoted 31 entries to "catalogued" |
| `hypercode/` folder exists | Folder absent | Marked as "extraction TODO" |

Status changed from ✅ RESCUED → 📝 CATALOGUED so the index stops lying.
```

Make the reconciliation a first-class entry in the doc you're correcting. Future readers need the receipt.

---

## 🧩 Related Skills

- [[HS-109]] Cross-Reference Before You Write — pre-write audit
- [[HS-110]] Lean Raid Discipline — what to do when most of a "new" doc is a duplicate
- [[HS-111]] Surface Contradictions, Don't Pick Sides — when audit finds disagreement
- [[HS-085]] 5 Mandatory Agent Guardrails — Rule 1 (Never Hallucinate APIs) is this pattern at code-level
- [[HS-092]] Agent Contract Test Suite — Layer 3 verification for agents
