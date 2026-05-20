# HS-113 — ⚒️ FETCH FORGE — Parallel Git Workflow Survival Guide

**Category:** `dev/`
**Source:** Original — from Lyndz's parallel-workflow memory (`verify-roadmap-against-main.md`) + 2026-05-21 raid commits where every push needed a pre-fetch + diverge check
**Version:** v1

---

## 🤔 What It Does

The git-hygiene moves that keep collaboration safe when **two pushers operate on the same branch concurrently** — typically Lyndz's auto-tooling out-of-band + an interactive session. Race conditions are real. These commands stop you from stomping work that wasn't there when you started.

> Memory anchor: *"Lyndz runs a PARALLEL git workflow — tooling auto-commits/pushes the same work out-of-band. ALWAYS `git fetch` + check `origin/main` before pushing. NEVER force-push. Verified dup → `reset --hard origin/main`"*

---

## 🛡️ The 3 Survival Moves

### Move 1 — Pre-action fetch

**Always before starting work on a branch:**

```bash
git fetch origin
git rev-list --left-right --count HEAD...origin/main
```

Output is two numbers: `<local-only commits>\t<remote-only commits>`.

| Output | Meaning | Action |
|---|---|---|
| `0  0` | Synced | Safe to start |
| `N  0` | Local ahead of remote | Safe to push when done |
| `0  M` | Remote ahead of local | `git pull --rebase` first |
| `N  M` | Diverged | **Investigate** — parallel work happened |

The diverged case is the one to handle carefully — never assume your local is right.

---

### Move 2 — Pre-push re-fetch

**Always immediately before `git push`:**

```bash
git fetch origin && git rev-list --left-right --count HEAD...origin/main
```

Even if Move 1 said clean, parallel tooling might have pushed in the seconds between. Re-fetch costs ~200ms and saves potential force-resolution headaches.

If diverged at this point → see the "Stomp Recovery" section below.

---

### Move 3 — Commit by explicit path

**Never `git add -A` or `git add .`** in a parallel-workflow repo:

```bash
# ✅ GOOD
git add specific-file-1.md specific-file-2.md

# ❌ BAD — risks committing files the parallel tooling was about to touch
git add -A
```

Sacred-rule reminder: also catches stray secrets / build artifacts / scratchpad files. Cost: one extra second of typing. Value: huge.

---

## 🚑 Stomp Recovery — "Verified Duplicate"

If you `git fetch` and find that the remote already has the work you just committed locally (your tooling auto-pushed the same work out-of-band):

```bash
# Verify it really is the same work
git log --oneline origin/main..HEAD     # what's local-only?
git log --oneline HEAD..origin/main     # what's remote-only?
git diff HEAD origin/main               # are the changes equivalent?

# If yes, the safe recovery:
git reset --hard origin/main
```

**`reset --hard origin/main`** because the parallel tooling already pushed the equivalent work — you don't need yours. Throwing away your duplicate local commit IS the right move.

**Never:**
- Force-push your version "to win"
- Merge your local in (creates a duplicate-changes merge commit, confuses history)
- Cherry-pick yours on top (same problem)

The remote won.

---

## ❌ The Forbidden Moves

| Forbidden | Why |
|---|---|
| `git push --force` to main | Overwrites the parallel work — **lost commits** |
| `git push --force-with-lease` to main | Same risk if your lease is stale |
| `git commit --amend` on pushed commits | Rewrites already-shared history |
| `git rebase` of pushed commits | Same |
| Skipping pre-push fetch "just this once" | This is when the race happens |

If the user explicitly asks for one of these, surface the risk first ([[HS-111]]) — never silently agree.

---

## 🪜 The Full Commit Flow (drill it)

```bash
# 1. Pre-fetch
git fetch origin
git rev-list --left-right --count HEAD...origin/main
# expect 0 0 ideally; if remote ahead, pull --rebase

# 2. Do work...

# 3. Stage by explicit path
git add <each-file>

# 4. Commit (conventional commit prefix)
git commit -m "<verb>: <change>"

# 5. Pre-push re-fetch
git fetch origin
git rev-list --left-right --count HEAD...origin/main
# if diverged HERE — investigate first

# 6. Push
git push origin main
```

Steps 1, 3, and 5 are the ones AI assistants skip first. Don't.

---

## 🎯 The Counter-Intuitive Insight

**Parallel git workflows look chaotic, but they're actually safer than serial single-pusher workflows — IF you respect the fetch discipline.**

Why: serial workflows assume "I'm the only writer" and skip checks. When that assumption breaks (a forgotten teammate pushes, CI commits, dependabot lands), the silent stomp is catastrophic.

Parallel workflows ASSUME another writer and check every time. The check becomes muscle memory. Errors get caught at fetch-time, not at git-history-archeology time three days later.

The friction trains the discipline.

---

## 🚨 Special Cases

- **First push to a new branch:** no pre-fetch possible (branch doesn't exist remotely). Use `git push -u origin <branch>` and accept that the remote will have exactly your changes. Safe.
- **Tooling that commits to feature branches:** check the tooling's branch convention. If it only writes to `main`, your feature branch is safe to bypass these moves *until* you merge.
- **Pre-commit hooks that modify files:** rare but possible. After hook fixes, restage explicitly (`git add <hook-touched-files>`) and recommit. Don't `--amend` if you've already pushed.

---

## 🧩 Related Skills

- [[HS-108]] Truth-vs-Claim Audit Pattern — sibling pre-action discipline
- [[HS-111]] Surface Contradictions, Don't Pick Sides — what to do when local + remote both have changes
- [[HS-076]] Pre-Commit Testing Checklist — what runs between Move 3 and Move 4
- [[HS-077]] User Agency Approval Gate — destructive moves (force-push) escalate here
