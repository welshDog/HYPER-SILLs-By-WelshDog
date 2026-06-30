# HS-057 — 🥚 GENESIS PROMPT — BROskiPets Phase 0 Build Prompt
---
skill_id: HS-057
problem_keywords:
  - broskipets phase 0
  - genesis build prompt
  - pet phase zero
---

> Catalogued → **RESCUED** 2026-06-19. Source pattern: HyperCode-V2.4 /
> BROskiPets. Category: `web3/`.

## What it Does

The cold-start build prompt for BROskiPets Phase 0 — scaffold the contract,
metadata, and a testnet mint path with zero mainnet risk.

## Input Format

"Start BROskiPets from scratch on testnet."

## THE PROMPT

```
Build BROskiPets Phase 0 (testnet only):
  1. ERC-721 (Enumerable) BROskiPet contract — open supply, updatable tokenURI.
  2. Deploy to Base Sepolia (chainId 84532). Fund deployer (~0.05 ETH).
     Foundry lives at ~/.foundry/bin (NOT on PATH).
  3. Metadata schema: {name, species, rarity, stage, image} (dynamic).
  4. Relay mint: Supabase edge fn holds the deployer key (Supabase secret +
     Vercel env); client calls the edge fn, NEVER the key directly.
  5. Smoke: relay mint 1 pet → confirm tokenURI resolves.
Sacred:
  - MetaMask = human gate. Mainnet NEVER without explicit sign-off.
  - No secrets in client bundle or git.
Output: contract address, a successful testnet mint tx, tokenURI.
```

## Example

> Deployed `0x4daF9e1e9Ebe9240758692Fdd50318a18173A69a` on Base Sepolia; relay
> mint E2E green.

## Related Skills

[[BROSKI_PETS_PHASE_1_BUILD_v1]] · [[BROSKI_PETS_INTEGRATION_PLAN_v1]]
