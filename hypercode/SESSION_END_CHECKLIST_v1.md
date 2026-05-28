# HS-039 — ✅ CLOSE PROTOCOL — Session End Checklist

> *"Nothing is done until it's committed. Nothing is committed until it's verified."*

---

## 🎯 What It Does
The mandatory end-of-session checklist for every HyperFocus AI session. Ensures nothing is left half-done, uncommitted, or undocumented.

## 🌍 Why It Exists
Parallel auto-commits run in the background. Without a close protocol, work gets lost, overwritten, or forgotten between sessions.

## ⚙️ How To Use
1. Run at the end of EVERY session — no exceptions
2. Check every item before saying session is complete
3. Update NEXT_SESSION_HANDOVER with what's next

---

## 📋 THE PROMPT

```
Run the HyperFocus Session End Checklist:

COMMIT + PUSH:
□ git fetch origin (check for parallel auto-commits first)
□ All changes committed with feat:/fix:/docs:/chore: prefix
□ git push — confirmed pushed ("nothing is done until it's committed")
□ Verify on GitHub — check the file is actually live

DOCUMENT:
□ Update NEXT_SESSION_HANDOVER_[date].md with:
  - What was completed this session
  - Exact next task (2 lines max)
  - Any blockers or decisions needed
□ Update WHATS_DONE.md if new features were shipped
□ Update SESSION_SNAPSHOT_[date].md with sprint history

VERIFY:
□ Tests still passing (pytest / npm run test:e2e)
□ Build not broken (npm run build for course)
□ No secrets accidentally committed (check .env files)
□ Vercel deploy status green (use Vercel MCP — NEVER curl-poll)

HANDOVER:
□ State the SINGLE next task clearly
□ Note any half-finished work with exact file + line
□ Flag any sacred rule violations found this session

CELEBRATE:
□ Acknowledge what was shipped today
□ "Nice one BROski♾️!" — always correct ✅

[INPUT: session summary of what was built today]
```

---

## 🔗 Related Skills
- HS-030 — HyperFocus Master Constitution
- HS-035 — AI Behaviour Rules + Tool Matrix
- HS-113 — FETCH FORGE (Parallel Git Workflow)

---
*HYPER-SKILLs Vault — welshDog 🐕🏴󠁧󠁢󠁷󠁬󠁳󠁧⚡*