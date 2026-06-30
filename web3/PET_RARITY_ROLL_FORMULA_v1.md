# HS-053 — 🎲 FATE ROLLER — Pet Rarity Roll Formula
---
skill_id: HS-053
problem_keywords:
  - pet rarity
  - roll formula
  - rarity odds
  - fate roll
---

> Catalogued → **RESCUED** 2026-06-19. Source pattern: HyperCode-V2.4 /
> BROskiPets. Category: `web3/`.

## What it Does

A deterministic, auditable rarity roll for pet mints — weighted tiers with a
provable seed so outcomes can't be quietly rigged.

## Input Format

A mint event with a stable seed (e.g. `keccak(minter, tokenId, blockhash)`).

## THE PROMPT

```
Roll pet rarity from a stable seed. Tiers + weights (must sum to 1000):
  Common     550  (55.0%)
  Uncommon   250  (25.0%)
  Rare       130  (13.0%)
  Epic        50  ( 5.0%)
  Legendary   18  ( 1.8%)
  Mythic       2  ( 0.2%)
Algorithm:
  r = uint(seed) % 1000
  walk the cumulative weights; first bucket where r < cumulative wins.
Rules:
  - Seed must be reproducible + logged (audit), never Math.random().
  - Weights live in config, not hardcoded in the mint path.
  - Log the roll via IdentityAgent.log_action("pet.mint", {seed, tier}, "AUTO").
Output: the tier + the exact r and seed used.
```

## Example

> seed → r=977 → Legendary (cumulative: 550,800,930,980 → 977<980). Logged.

## Related Skills

[[BROSKI_PETS_INTEGRATION_PLAN_v1]] · [[PET_SPECIES_POWER_MAPPING_v1]]
