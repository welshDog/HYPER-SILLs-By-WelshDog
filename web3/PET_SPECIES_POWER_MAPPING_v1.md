# HS-056 — 🦈 BEAST CODEX — Pet Species Power Mapping
---
skill_id: HS-056
problem_keywords:
  - pet species
  - power mapping
  - beast codex
---

> Catalogued → **RESCUED** 2026-06-19. Source pattern: HyperCode-V2.4 /
> BROskiPets. Category: `web3/`.

## What it Does

Maps each pet species to a power profile + evolution path, so rarity and species
combine into deterministic, balanced traits (no magic numbers in the mint path).

## Input Format

A species id + rarity tier (from HS-053).

## THE PROMPT

```
Resolve a pet's power profile from {species, rarity}:
  Species archetypes (base stats: focus, build, guard):
    Wolf   → focus-heavy  (10/6/7)
    Shark  → build-heavy  (6/10/7)
    Owl    → guard-heavy  (7/6/10)
    Dragon → balanced-high(9/9/9)   (rarer species)
  Final stat = base * rarity_multiplier:
    Common 1.0 · Uncommon 1.15 · Rare 1.35 · Epic 1.6 · Legendary 2.0 · Mythic 2.5
  Evolution stages (XP-gated): Hatchling → Juvenile → Prime → Apex.
Rules:
  - Species + multipliers live in config, not code (HS-053 alignment).
  - Stats are display/utility only — never gate money on them.
Output: {species, rarity, stats, stage}.
```

## Example

> Legendary Wolf, Prime stage → focus 20 / build 12 / guard 14. From config.

## Related Skills

[[PET_RARITY_ROLL_FORMULA_v1]] · [[BROSKI_PETS_INTEGRATION_PLAN_v1]]
