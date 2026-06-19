# HS-055 — 📜 CHAIN LEDGER — dNFT On-Chain Portfolio Pattern

> Catalogued → **RESCUED** 2026-06-19. Source pattern: HyperCode-V2.4 /
> BROskiPets-LLM-dNFT. Category: `web3/`.

## What it Does

Reads a wallet's pet portfolio straight from chain (source of truth) and renders
it, instead of trusting an off-chain cache — so the UI can never lie about
ownership or evolution stage.

## Input Format

A wallet address + the BROskiPet contract (`0x4daF9e1e9Ebe9240758692Fdd50318a18173A69a`, Base Sepolia 84532).

## THE PROMPT

```
Build an on-chain portfolio view:
  1. balanceOf(owner) → count.
  2. tokenOfOwnerByIndex(owner, i) → tokenIds (ERC-721 Enumerable).
  3. tokenURI(tokenId) → resolve dynamic metadata (stage, species, rarity).
  4. Render holo PetCard per token (see DESIGN_BRAIN aesthetic; NO orange).
Rules:
  - Web3 is LAZY + /pets ONLY — never import wagmi globally (re-bloats cold load).
  - Chain reads are the truth; off-chain cache is a hint, reconciled after login.
  - Logged-out users see a demo-pet gate, not a wallet prompt.
Output: portfolio array [{tokenId, stage, species, rarity, image}].
```

## Example

> Wallet holds 3 BROskiPets → 3 holo cards, stages [2,1,4], one Legendary.
> No wagmi outside /pets. Cold load unchanged.

## Related Skills

[[BROSKI_PETS_INTEGRATION_PLAN_v1]] · [[DEV_ACTION_XP_TRIGGER_v1]]
