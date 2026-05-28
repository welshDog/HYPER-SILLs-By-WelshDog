# HS-032 — 🔴 COURSE SACRED RULES — Course Sacred Rules (11 Rules)

## What it Does
11 load-bearing rules for Hyper-Vibe-Coding-Course. Every single one has caused a production incident if broken. Don't skip them.

## When To Use
- Before ANY commit to Hyper-Vibe-Coding-Course
- When touching Supabase migrations, Web3, auth, or build config
- Onboarding any AI to course work

## THE RULES
```
COURSE SACRED RULES — load-bearing gotchas:

✔ NEVER `supabase db push`
  → local migration filenames desynced from remote schema_migrations
  → Deploy via Supabase MCP apply_migration ONLY

✔ Web3 lazy + /pets ONLY
  → NEVER import wagmi/rainbowkit globally / in funnel / in main.tsx
  → Re-bloats cold load ~900 kB (reverts Sprint 2)
  → Only 4 files use wagmi — keep it that way

✔ NEVER `--no-verify`
  → husky + lint-staged catches real ESLint errors
  → react-hooks/set-state-in-effect is an ERROR (derive or useRef)

✔ NO orange in UI
  → sacred HFZ brand rule (master palette only)

✔ Three chrome systems
  → funnel TopNav · course Navbar · VibeLabShell
  → No global shell. Funnel pages skip Layout.

✔ award_tokens() — ALWAYS pass a stable p_source_id
  → ledger dedup = partial unique (user_id, reason, source_id)

✔ Pets.tsx @ts-nocheck — pre-existing, non-blocking, money-path. Don't chase it.

✔ Course dev (repo root) — npm run dev:frontend NOT npm run dev

✔ NEVER curl-poll prod
  → trips Vercel Attack Challenge Mode (403 X-Vercel-Mitigated)
  → Deploy-truth = Vercel MCP get_deployment

✔ Playwright IS installed — npm run test:e2e
  → Use it instead of "human must test"

✔ Parallel git workflow
  → ALWAYS git fetch + check origin/main before pushing
  → NEVER force-push
```

## Related Skills
- HS-031 V2.4 Sacred Rules
- HS-076 THE GATEKEEPER Pre-Commit Testing Checklist
- HS-113 FETCH FORGE Parallel Git Workflow

---
*Source: HyperCode-V2.4 CLAUDE.md §6b | Category: hypercode/*
