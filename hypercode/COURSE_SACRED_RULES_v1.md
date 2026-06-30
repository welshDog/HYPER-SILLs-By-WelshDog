# HS-032 — 🔴 COURSE SACRED RULES — Course Sacred Rules (11 Rules)
**Category:** hypercode
**Version:** 1.0

> *"The 11 commandments of the Hyper-Vibe-Coding-Course. Paste before every course session."*

---

## 🎯 What It Does
The 11 load-bearing rules for Hyper-Vibe-Coding-Course. Prevents the most expensive mistakes — db schema desyncs, web3 bundle bloat, broken auth, and false "it's down" alerts.

## 🌍 Why It Exists
These rules protect a live production course with real students and real payments. Each rule is a scar from a real incident.

## ⚙️ How To Use
1. Paste at the start of any course / HyperLabs session
2. AI treats these as hard stops — not guidelines
problem_keywords:
  - course rules
  - course sacred rules

---

## 📋 THE PROMPT

```
You are working on Hyper-Vibe-Coding-Course (Vite+React — NOT Next.js). Apply ALL rules:

✔ NEVER `supabase db push` — migrations desynced from remote schema_migrations.
   Deploy via Supabase MCP apply_migration ONLY
✔ Web3 lazy + /pets ONLY — NEVER import wagmi/rainbowkit globally or in main.tsx
   (4 files use wagmi — keep it that way. Global import = +900kB cold load)
✔ NEVER --no-verify — husky+lint-staged catches real ESLint errors
   react-hooks/set-state-in-effect is an ERROR (derive or useRef)
✔ NO orange in UI — sacred HFZ brand rule (master palette only)
✔ Three chrome systems — funnel TopNav · course Navbar · VibeLabShell
   No global shell. Funnel pages skip Layout.
✔ award_tokens() — ALWAYS pass stable p_source_id (ledger dedup)
✔ Pets.tsx @ts-nocheck — pre-existing, non-blocking. Don't chase it.
✔ Course dev command — npm run dev:frontend NOT npm run dev
✔ NEVER curl-poll prod — trips Vercel Attack Challenge Mode (403)
   Deploy truth = Vercel MCP get_deployment
✔ Playwright IS installed — npm run test:e2e. Use it instead of "human must test"
✔ Parallel git workflow — ALWAYS git fetch before pushing. NEVER force-push.

[INPUT: describe the course task]
```

---

## ✅ Example
**Input:** "Push the latest migration to production"
**Output:** AI flags: "SACRED RULE: Never `supabase db push` — use Supabase MCP apply_migration instead."

## 🔗 Related Skills
- HS-031 — V2.4 Sacred Rules
- HS-030 — HyperFocus Master Constitution

---
*HYPER-SKILLs Vault — welshDog 🐕🏴󠁧󠁢󠁷󠁬󠁳󠁧⚡*
