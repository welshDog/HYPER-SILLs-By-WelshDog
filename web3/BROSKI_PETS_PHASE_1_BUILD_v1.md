# HS-058 — 🐣 HATCH PROMPT — BROskiPets Phase 1 Build Prompt

> Catalogued → **RESCUED** 2026-06-19. Source pattern: HyperCode-V2.4 /
> BROskiPets. Category: `web3/`.

## What it Does

The Phase 1 build prompt — take the Phase 0 testnet mint and make it a living
game: XP-driven evolution, the portfolio UI, and the dev-action loop.

## Input Format

"Phase 0 mint works — now make pets evolve and render."

## THE PROMPT

```
Build BROskiPets Phase 1 (on top of Phase 0):
  1. Wire dev-action XP (HS-054) → wallet thresholds → evolution stage.
  2. On threshold cross, update tokenURI metadata via the relay edge fn (HS-052).
  3. Build the /pets portfolio: on-chain reads (HS-055), holo PetCards, XpFeed,
     logged-out demo-pet gate.
  4. Rarity + species on mint (HS-053 + HS-056), seed logged to governance.
Sacred:
  - Web3 lazy + /pets ONLY (never global wagmi). NO orange.
  - Playwright for UI verification — never "human must test".
Output: a pet that visibly evolves when the owner ships code, rendered live.
```

## Example

> 5 commits → wallet crosses stage-2 → edge fn bumps metadata → PetCard
> re-renders at Juvenile, XpFeed shows the gain. Verified via Playwright.

## Related Skills

[[BROSKI_PETS_PHASE_0_BUILD_v1]] · [[DEV_ACTION_XP_TRIGGER_v1]] · [[DNFT_ONCHAIN_PORTFOLIO_v1]]
