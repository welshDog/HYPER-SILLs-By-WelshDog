# NEXT SESSION HANDOVER — 2026-06-07

> Read this FIRST next session. This always wins over older files.
> Updated: Sun 7 June 2026, late evening BST

---

## ✅ What Got Done Tonight

### Job 1 — github-sync healthcheck fix · `HyperCode-V2.4`
- Diagnosed: container was `unhealthy` for 29 hours / **835 consecutive probe failures** despite `cron -f` running fine as PID 1.
- Root cause: `ps`/`pgrep`/`curl` are **not** installed in `python:3.11-slim`. The compose healthcheck `ps aux | grep -v grep | grep cron` errored every probe with `/bin/sh: 1: ps: not found`.
- Fix: swapped to `grep -q cron /proc/1/comm || exit 1` in `docker-compose.agents.yml:303` — zero new deps, no image rebuild, container healthy on first probe after `--force-recreate`.
- Commit `54a90f2` · pushed to `welshDog/HyperCode-V2.4`.

### Job 2 — Stripe webhook smoke test · `Hyper-Vibe-Coding-Course`
- Method: Stripe Workbench resend of `evt_1TeZt82LoEeIEPVEDqDCHXPt` (pro tier purchase, 2026-06-04).
- Result: Edge Function returned `200` in 1925 ms; row counts unchanged; idempotency proven end-to-end.
- Results doc: `Hyper-Vibe-Coding-Course/docs/Notes/REVENUE_SMOKE_TEST_RESULTS_2026-06-06.md` (commits `22085ca` → `dbade80`).

### Job 3 — `early_access_signups` RLS hardening · `Hyper-Vibe-Coding-Course`
- Closes Supabase advisor lint 0024 (`rls_policy_always_true`).
- Replaced `WITH CHECK (true)` with: email not null + 6..320 chars + contains `@`, name not null + trimmed 1..100. Source whitelist deliberately NOT added (per the original migration's design comment).
- Applied via Supabase MCP `apply_migration` as version `20260606231810_harden_early_access_signups_rls`. Local mirror file written + committed `fd5f39b`.
- Verified anon-role smoke: happy path inserts, garbage paths blocked with `42501`.

### Job 4 — Broken-migration hunt
- Result: **no broken migration.** Earlier Postgres-log noise (2026-06-06 22:56→23:04 UTC) was dashboard SQL editor mishaps that self-corrected — read-only toggle was on for two `ALTER VIEW` attempts, plus two syntax errors and one bad column reference. Final state: `broski_economy_snapshot` and `broski_leaderboard` are both `security_invoker=on`. Migration history clean (110 rows, 0 with NULL statements).

### Job 5 — Audit of 3 "unmatched" payments
- All three are **TEST noise**, not real lost revenue:
  - `evt_3Tc9pN…` (USD) — `stripe trigger` default PaymentIntent.
  - `evt_1Tc9pO…` (USD, `stripe@example.com`) — `stripe trigger` default Checkout (placeholder email).
  - `evt_3TcAF4…` (GBP £29) — PaymentIntent sibling of the successful TEST starter checkout `evt_1TcAF52` at the same 280 ms instant. Tokens already credited via the checkout event.
- **No replays needed.**

### 🚨 Knock-on finding: Stripe is still in TEST mode
- Verified: every `price_*` ID in `PRICE_TO_TIER` (`stripe-webhook/index.ts:11-20`) resolves to a `https://dashboard.stripe.com/test/prices/...` URL. Stripe price IDs are mode-scoped — a TEST price ID **cannot** exist in LIVE. Therefore the integration is TEST-only today.
- `HyperCode-V2.4/CLAUDE.md` and the smoke test results doc both claimed "Stripe LIVE 💳 since May 5" — **wrong**. Patched in commits `0518d01` (V2.4) and `dbade80` (Course).
- Implication: **real LIVE customers cannot buy yet.** Going live is the next-priority work — see below.

### Memory updates
- Added: `slim-python-healthcheck.md`, `supabase-dashboard-readonly-toggle.md`
- Added then updated: `stripe-webhook-smoke-test.md` (now reflects TEST-mode reality + audit verdict)
- Deleted: `unmatched-payments-backlog.md` (resolved — not load-bearing)

---

## 🔴 Next Priority — Wire Stripe LIVE Price IDs into `PRICE_TO_TIER`

The Course Stripe integration runs end-to-end in TEST mode. To accept real money, three things have to land together:

1. Create the same 8 product/price pairs in **Stripe LIVE mode** (Dashboard → flip to Live → Products → create starter/pro/builder/architect/hyper_legend at the same GBP amounts). Record the new `price_*` LIVE IDs.
2. Add the LIVE IDs to `PRICE_TO_TIER` in `Hyper-Vibe-Coding-Course/supabase/functions/stripe-webhook/index.ts:11-20`. Keep the TEST IDs in the map too so test events keep flowing — Stripe events arrive with `event.livemode: true/false` and the price IDs distinguish themselves.
3. Create a **LIVE-mode webhook endpoint** in Stripe Dashboard pointing at `https://yhtmuibgdnxhbgboajhc.supabase.co/functions/v1/stripe-webhook`. Store its secret as `STRIPE_WEBHOOK_SECRET_LIVE` (a new Supabase secret) alongside the existing TEST secret. Update the function to pick the right secret by `event.livemode` (currently it reads only `STRIPE_WEBHOOK_SECRET`).

---

## ⚡ First Task Next Session

**Replace TEST price IDs with LIVE ones in `PRICE_TO_TIER`** (`Hyper-Vibe-Coding-Course/supabase/functions/stripe-webhook/index.ts:11-20`). Either:

- **Conservative (recommended):** keep both maps. Add a `PRICE_TO_TIER_LIVE` constant with the LIVE IDs; pick between them by `event.livemode`. Lets test events keep working for future smoke runs.
- **Cutover:** swap TEST IDs out entirely. Cleaner but loses the ability to test through the function without re-deploying.

Either way, **deploy the Edge Function via Supabase MCP `deploy_edge_function`** (NOT `supabase db push` and NOT `supabase functions deploy` from CLI — the parallel git workflow + history desync rules apply).

Verification: after deploy, fire a `stripe trigger checkout.session.completed` in TEST mode → confirm a row still lands. Then in Stripe Dashboard, make a £1 LIVE test purchase with a real card → confirm a row lands AND `event.livemode = true` → refund yourself.

---

## 📝 Add to NotebookLM

Add this doc to your NotebookLM notebook so the smoke-test reasoning + audit verdict are queryable across future sessions:

- **File:** `Hyper-Vibe-Coding-Course/docs/Notes/REVENUE_SMOKE_TEST_RESULTS_2026-06-06.md`
- **Why:** captures the full Workbench-resend method, the idempotency proof, the TEST-mode correction, and the 3-row unmatched-payments audit verdict in one place. Future me + future Claude both benefit.
- **Raw URL** (paste into NotebookLM "Add source"): https://github.com/welshDog/Hyper-Vibe-Coding-Course/blob/main/docs/Notes/REVENUE_SMOKE_TEST_RESULTS_2026-06-06.md

---

## 📂 Commits Pushed Tonight

| Repo | Commit | What |
|---|---|---|
| `HyperCode-V2.4` | `54a90f2` | fix: github-sync healthcheck — swap ps grep for /proc/1/comm read |
| `HyperCode-V2.4` | `0518d01` | docs: correct Stripe LIVE claims — integration is still TEST mode |
| `Hyper-Vibe-Coding-Course` | `fd5f39b` | fix: harden early_access_signups RLS policy |
| `Hyper-Vibe-Coding-Course` | `22085ca` | docs: Stripe webhook smoke test results 2026-06-06 |
| `Hyper-Vibe-Coding-Course` | `dbade80` | docs: correct smoke test results — event was TEST mode, not LIVE |

---

## ⚠️ Watch Out For Next Session

- **Don't take "Stripe LIVE" at face value** anywhere in the docs — the CLAUDE.md banners are now corrected but other status reports / handovers may still echo the old claim. Verify via the price-ID-URL test (`/test/` segment) before believing any "LIVE" label.
- **Supabase dashboard SQL editor opens read-only by default** — flip the toggle off before running DDL, or hit `cannot execute ... in a read-only transaction`. For prod DDL prefer Supabase MCP `apply_migration`.
- **`python:3.11-slim` has no `ps`/`pgrep`/`curl`** — if you write a healthcheck for any slim-based image, use `grep /proc/1/comm` or install the tool explicitly.
- **Course repo:** local migration filenames are desynced from remote `schema_migrations`. NEVER `supabase db push`. Always Supabase MCP `apply_migration`.
- **Parallel git workflow** in both V2.4 and Course — `git fetch origin` before any push. NEVER force-push.
