# HS-033 — 🔴 BROSKI SHOP SACRED RULES — BROski$ Shop Sacred Rules

## What it Does
Sacred rules specifically for the BROski$ token economy and Shop Fulfillment system. Protects the money path and prevents double-spend or silent failures.

## When To Use
- Before touching ShopPage.tsx, shop-purchase edge function, or award_tokens()
- When debugging token balance issues
- When adding new shop items or tier discounts

## THE RULES
```
BROski$ SHOP SACRED RULES:

✔ award_tokens() — ALWAYS pass a stable p_source_id
  → Ledger dedup: partial unique (user_id, reason, source_id)
  → Without it: tokens awarded multiple times silently

✔ Tier discounts are server-enforced
  → 0% / 5% / 10% / 15% by tier
  → Source of truth: supabase/functions/shop-purchase/
  → Client UI shows discount — server ALWAYS recalculates

✔ Buy-confirm + auto-refund pattern
  → Every purchase = confirm modal before deduct
  → Failed fulfillment = auto-refund to wallet
  → NEVER deduct without confirm

✔ Shop Fulfillment v2 categories all deliver
  → Every category must have a delivery surface
  → Test all categories in E2E before deploy

✔ Stripe webhook — rate-limit EXEMPT always
  → NEVER add rate limiting to Stripe webhook endpoint
  → Webhook secret stored in .env only

✔ VITE_STRIPE_PAYMENT_LINK_URL must be set
  → Set in .env.local AND Vercel env vars
  → Empty = broken checkout flow

✔ Token economy uses BROski$ (not ETH, not SOL)
  → BROski$ = in-platform currency
  → Web3 mint is separate (BROskiPets only)
```

## Related Skills
- HS-025 COIN MENDER Token Sync Debug
- HS-054 Dev Action XP Trigger System
- HS-032 Course Sacred Rules

---
*Source: HyperCode-V2.4 CLAUDE.md §6 | Category: hypercode/*
