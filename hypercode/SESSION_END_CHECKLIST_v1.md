# HS-039 — ✅ SESSION END CHECKLIST — Session End Checklist

## What it Does
The mandatory end-of-session checklist for every HyperFocus ecosystem build session. Ensures nothing is left uncommitted, no context is lost, and the next session starts fast.

## When To Use
- End of EVERY build session, no exceptions
- Before closing Claude Code / Perplexity / any AI session
- After completing a sprint or major feature

## THE CHECKLIST
```
SESSION END CHECKLIST — do these before closing:

✅ CODE
  □ All changed files committed (feat:/fix:/docs:/chore: only)
  □ Pushed to GitHub — "nothing is done until it's committed"
  □ git fetch run — check no parallel auto-commits conflict
  □ No .env files committed (double-check git status)
  □ No secrets in any committed file

✅ DOCS
  □ WHATS_DONE.md updated with what was completed
  □ SESSION_SNAPSHOT updated with current state
  □ NEXT_SESSION_HANDOVER written with:
      - What was done this session
      - Exact next task (2 lines max)
      - Any blockers or decisions needed
      - Files changed this session

✅ TESTS
  □ Tests run (pytest / npm run test:e2e)
  □ No new failures introduced
  □ Playwright E2E green if course work done

✅ DEPLOY (if applicable)
  □ Vercel deployment verified via Vercel MCP (NOT curl-poll)
  □ Supabase migration applied via apply_migration (NOT db push)
  □ Health checks passing (curl localhost ports)

✅ CELEBRATE
  □ Name the win: "Today I shipped [X]"
  □ Nice one BROski♾️! — you earned it

If you only do ONE thing: push to GitHub.
"Done" means committed + pushed. Nothing else counts.
```

## Related Skills
- HS-030 HyperFocus Master Constitution
- HS-031 V2.4 Sacred Rules
- HS-113 FETCH FORGE Parallel Git Workflow

---
*Source: HyperCode-V2.4 CLAUDE.md §11 | Category: hypercode/*
