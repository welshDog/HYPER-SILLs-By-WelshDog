# HS-033 — 🔴 BROSKI SHOP SACRED RULES — BROski$ Shop Sacred Rules

> *"The shop handles real BROski$ tokens. These rules protect the token economy."*

---

## 🎯 What It Does
Sacred rules specifically for the BROski$ Shop and token economy. Prevents double-spending, dedup failures, and unsecured discounts.

## 🌍 Why It Exists
The BROski$ token economy is the gamification backbone. A bug here breaks trust with real students.

## ⚙️ How To Use
1. Paste when working on ShopPage, award_tokens, or any BROski$ flow
2. AI respects token economy integrity rules automatically

---

## 📋 THE PROMPT

```
You are working on the BROski$ Shop and token economy. Apply ALL rules:

✔ award_tokens() — ALWAYS pass a stable p_source_id
   Ledger dedup = partial unique (user_id, reason, source_id)
   Missing source_id = duplicate awards possible
✔ Tier discounts — 0/5/10/15% — enforced server-side in supabase/functions/shop-purchase/
   NEVER client-side only
✔ Shop Fulfillment v2 — every category delivers · buy-confirm + server auto-refund
✔ Token awards — ALWAYS go through Core API (One Door pattern)
   NEVER award tokens directly from the frontend
✔ BROski$ balance — source of truth is Supabase, NOT local state
✔ NEVER merge Supabase ↔ V2.4 schemas — separate systems
✔ Stripe webhook — rate-limit EXEMPT always

Current shop state:
- Fulfillment v2 BUILT (deploy + E2E pending)
- Tier discounts: 0% (no role) / 5% (student) / 10% (graduate) / 15% (BROski)
- Auto-refund on failed fulfillment: active

[INPUT: describe the shop/token task]
```

---

## ✅ Example
**Input:** "Award 100 tokens when user completes module 3"
**Output:** AI generates `award_tokens(user_id, 100, 'module_complete', source_id='module_3_complete')` with dedup key — never duplicates.

## 🔗 Related Skills
- HS-032 — Course Sacred Rules
- HS-025 — COIN MENDER (Token Sync Debug)

---
*HYPER-SKILLs Vault — welshDog 🐕🏴󠁧󠁢󠁷󠁬󠁳󠁧⚡*