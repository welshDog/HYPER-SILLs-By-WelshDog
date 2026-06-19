# HS-052 — 🐾 PET MASTER — BROskiPets Full Integration Plan

> Catalogued → **RESCUED** 2026-06-19. Source pattern: HyperCode-V2.4 +
> `BROskiPets-LLM-dNFT`. Category: `web3/`.

## What it Does

Gives an agent the end-to-end blueprint for wiring **BROskiPets** (LLM-backed
dynamic NFTs) into the HyperFocus ecosystem: dev activity → XP → BROski$ →
pet evolution, with on-chain mint via a relay.

## Input Format

A request to design or extend the pets integration, e.g. *"wire commit XP to pet
evolution"* or *"add a new pet species end to end."*

## THE PROMPT

```
You are integrating BROskiPets into HyperFocus. The spine is:
1. Dev action (git commit / focus session / quest) → XP event.
2. XP → BROski$ durable wallet (broski_wallets/broski_transactions, postgres).
3. Wallet thresholds → pet evolution stage (dynamic NFT metadata).
4. On-chain mint/update via RELAY (never expose the deployer key client-side):
   Supabase edge function holds the secret → calls the BROskiPet contract.
Contracts (Base Sepolia, chainId 84532):
  - BROskiPet (open supply): 0x4daF9e1e9Ebe9240758692Fdd50318a18173A69a
  - EEPVengers (78 minted): 0x8012...
Rules:
  - MetaMask popups are a HUMAN gate — never claim to automate them.
  - Mainnet NEVER without explicit sign-off.
  - dNFT metadata is updatable; portfolio reads are on-chain (see HS-055).
Output the integration steps + which existing tables/edge-fns to reuse.
```

## Example

> Input: "Make 5 commits evolve a starter pet to stage 2."
> Output: commit hook → `award-dev-xp` → wallet xp crosses stage-2 threshold →
> edge fn updates tokenURI metadata → pet card re-renders. No new contract.

## Related Skills

[[DEV_ACTION_XP_TRIGGER_v1]] · [[PET_RARITY_ROLL_FORMULA_v1]] ·
[[DNFT_ONCHAIN_PORTFOLIO_v1]] · [[PET_SPECIES_POWER_MAPPING_v1]]
