# HS-054 — ⚡ XP SPARK — Dev Action XP Trigger System
---
skill_id: HS-054
problem_keywords:
  - dev xp
  - xp trigger
  - reward dev actions
  - xp spark
---

> Catalogued → **RESCUED** 2026-06-19. Source pattern: HyperCode-V2.4 dev-XP
> hooks + broski_economy. Category: `web3/`.

## What it Does

Turns real developer actions into durable BROski$ XP that feeds pet evolution —
git commits, focus sessions, quests — each with stable dedup so a rebase or
replay never double-pays.

## Input Format

A dev event: `{type: commit|focus|quest, user, source_id}`.

## THE PROMPT

```
Award XP for a dev action with EXACTLY-ONCE semantics:
  source_id MUST be stable across retries/rebase, e.g.
    git:<repo>:<patch-id>   (patch-id is stable across rebase)
  Pipeline: event → publisher (SETNX dedup gate on source_id) →
    consumer dual-sink:  redis (fast) + POST core /economy/award-dev-xp
    → broski_service.award_xp → durable broski_wallets/broski_transactions.
Prefix → XP table (example): feat:+15  fix:+10  docs:+5  chore:+3.
Rules:
  - Redis AOF on so XP survives restart; postgres is system of record.
  - NEVER award without a source_id (ledger dedup, HS-?? award_tokens rule).
  - Cross the pet-evolution threshold? trigger metadata update (HS-052).
Output: amount, source_id, and whether it was a dedup no-op.
```

## Example

> Rebase replays commit `abc` → same `git:repo:patchid` → SETNX gate blocks the
> second award → wallet unchanged. Honest.

## Related Skills

[[BROSKI_PETS_INTEGRATION_PLAN_v1]] · [[DNFT_ONCHAIN_PORTFOLIO_v1]]
