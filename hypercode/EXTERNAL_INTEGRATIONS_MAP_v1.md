# HS-065 — 🔗 THE CONNECTOR — External Integrations Map

**Category:** hypercode
**Version:** 1.0

> *"Every third-party wire in one place — and which mode it's in."*

---

## 🎯 What It Does

Maps every external service HyperFocus talks to, its mode/state, and the sacred
rule for touching it — so an AI never swaps a test key for live or trips a guard.

## 🌍 Why It Exists

Each integration has a footgun (Stripe test-vs-live, Vercel attack mode, MetaMask
human gate). One map prevents the classic mistakes.

## ⚙️ How To Use

Paste when wiring, debugging, or deploying anything that crosses a system
boundary.
problem_keywords:
  - external integrations
  - third party services
  - integrations map
  - connectors

---

## 📋 THE PROMPT

```
HyperFocus external integrations + sacred rules:

| Service | Used for | Mode / State | Sacred rule |
|---|---|---|---|
| Stripe | Course checkout/webhooks | TEST mode (live blocked on Companies House reg) | webhook rate-limit EXEMPT; never swap to sk_live_ without sign-off |
| Supabase | Course DB/Auth/Edge fns | prod | NEVER `supabase db push` — deploy via MCP apply_migration |
| Vercel | Course frontend hosting | prod | NEVER curl-poll prod (Attack Challenge 403); deploy-truth = MCP get_deployment |
| Discord | broski-bot | live | ban/kick NEVER fully autonomous (veto-gated) |
| Anthropic | agent LLMs | live (Claude); Ollama fallback | key via secret file, never client |
| Base Sepolia (84532) | BROskiPets dNFT | testnet | MetaMask = human gate; mainnet never without sign-off |
| GitHub | repos + Actions | live | Actions billing-locked; fetch before push, never force-push |
```

## ✅ Example

> "Test the Stripe webhook" → it's TEST mode; price IDs resolve to /test/ URLs;
> Workbench resend is the only realistic smoke path. Don't touch live keys.

## 🔗 Related Skills

[[ECOSYSTEM_INVENTORY_v1]] · [[ARCHITECTURE_QUICK_REF_v1]]
