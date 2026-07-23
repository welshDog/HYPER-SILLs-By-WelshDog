# Agent Skill Loadouts — Design

> **Turn "123 skills in a vault" into "every agent provably wears the right ones — and can't wear the wrong ones."**
> Status: DESIGN + STARTER FILE (`agent-loadouts.json`). Validator + wiring = next.
> Grounded against the live registry + MCP on 2026-07-23.

---

## 1. The problem

HYPER-SILLs already has a canonical registry (123 skills), a Graph-of-Skills
(`get_skill_graph`), semantic search, packs, and skill routing into the crew-orchestrator
(`/route` → `/execute` injection). What it **doesn't** have: any agent declaring **which skills
it must, may, or must-not load.** Skills reach agents *fuzzily* (semantic routing). Nothing makes
the FIVE WARDS or SACRED SIX actually *binding*, and nothing stops an agent loading another
repo's rules.

A grep for `loadout` / `required_skills` / `skill_manifest` across the repo returns **nothing**.
This is the highest-leverage gap in the whole Skill OS.

## 2. The file — `agent-loadouts.json` (repo root, beside `skills-registry.json`)

Three lists per agent, DRY via a shared `_defaults`:

```jsonc
{
  "_defaults": {
    "required":  ["HS-098","HS-085","HS-105","HS-088","HS-083"], // every agent
    "optional":  ["HS-069","HS-108"]
  },
  "agents": {
    "broski-bot": {
      "required":  ["HS-077","HS-038","HS-031"],
      "forbidden": ["HS-032"]                                    // wrong-repo rules
    }
  }
}
```

**Resolution:** an agent's effective set = `_defaults` merged with its own entry
(`required` = union, `forbidden` = union). `optional` is advisory (surfaced to the agent, not enforced).

**Invariants** (the validator enforces these):
- every id exists in `skills-registry.json`
- `effective_required ∩ effective_forbidden = ∅`
- every agent key is a real service name
- no id is `deprecated`/`archived` in the registry

## 3. The starter loadout (real IDs, verified against the registry)

| Skill | ID | Role |
|---|---|---|
| THE SACRED SIX | `HS-098` | the 6 laws of agents — **default required** |
| THE FIVE WARDS | `HS-085` | 5 mandatory guardrails — **default required** |
| THE METRICS OATH | `HS-105` | metrics contract — **default required** |
| THE MIRROR OATH | `HS-088` | 8-point self-audit — **default required** |
| THE THREE VOICES | `HS-083` | comms patterns — **default required** |
| MERCY MESSAGE | `HS-069` | ND-first error copy — default optional |
| REALITY ANCHOR | `HS-108` | truth-vs-claim audit — default optional |
| THE CHOICE MATRIX | `HS-075` | decision framework — orchestrator |
| CONSENT GUARDIAN | `HS-077` | approval gate — anything that acts |
| THE GRAND ROSTER | `HS-089` | agent roster — registry/orchestrator |
| THE THRONE LADDER | `HS-067` | role hierarchy — orchestrator |
| THE BIRTH RITE | `HS-106` | new-agent checklist — factory |
| CRADLE-TO-GRAVE | `HS-100` | lifecycle machine — factory/spawner |
| FOCUS HAWK | `HS-124` | focus manifest — focus-tracker |
| FLOW KEEPER | `HS-078` | anti-interrupt — brain agents |
| THE TOOL BELT | `HS-080` | tools API — mcp-bridge |
| THE PORT WARDEN | `HS-061` | network map — mcp-bridge |
| PHASE WARDEN | `HS-038` | guardian phases — broski-bot |
| METRICS FORGE | `HS-041` | Prom/Grafana wiring — nemoclaw |
| V2.4 SACRED RULES | `HS-031` | required for V2.4-native agents |
| COURSE SACRED RULES | `HS-032` | **forbidden** on V2.4 agents (wrong repo) |

See `agent-loadouts.json` for the full per-agent mapping (12 agents: core + brain).

## 4. The killer feature — `forbidden` = the cross-repo guard, in data

`broski-bot → "forbidden": ["HS-032"]` (Course Sacred Rules).

That's the AGENT-START **"don't apply another repo's sacred rules"** trap — the one that bites
every session — turned into a **schema violation**. A V2.4 agent literally *cannot* load the
Course's rules. Guardrails stop being aspirational and become enforced.

## 5. Wiring — 3 steps, all on rails that already exist

1. **Validate** — `scripts/validate_loadouts.py`: checks the invariants in §2. Drop it into the
   **existing pre-push lint gate** (the one that gates every HYPER-SILLs push). Loadouts can never
   drift from the registry.
2. **Boot check** — each agent resolves `_defaults + own` on startup and calls the existing MCP
   `load_skill(id)` for each `required`. Any missing/unloadable → **refuse full boot**, log,
   run degraded (safe mode). Concretises "refuse to boot without the SACRED SIX."
3. **Injection** — `crew-orchestrator` already injects graph-routed skills into `/execute`
   (`GRAPH_ROUTE_URL`). Extend ~3 lines: prepend the agent's loadout (`required + optional`) to the
   routed set, so every prompt is seeded with mandatory skills *before* task-routing adds
   situational ones.

**New code = 1 JSON file + 1 validator + a boot hook + a 3-line injection tweak.** Everything else
(registry, `load_skill`, `/route`, lint gate) already exists.

## 6. Rollout

- [x] Starter `agent-loadouts.json` (validated against the registry)
- [x] This design doc
- [x] `scripts/validate_loadouts.py` + wired into the pre-push lint gate (via `skill_linter.py`) — catches unknown ids, dead-status refs, and required/forbidden clashes
- [x] Boot-check helper (`scripts/agent_boot.py` + `tests/test_agent_boot.py`, 9 tests) — `boot_check("<agent>")` resolves the loadout, refuses full boot (strict) when a required skill is missing/dead, and never resolves a forbidden skill. Registry-based (self-contained, no live-MCP dependency at container start). CLI: `python scripts/agent_boot.py <agent> [root] [--soft]`.
- [x] Orchestrator injection — `crew-orchestrator` (HyperCode-V2.4) `loadout.py` prepends the agent's mandatory skills to every plan, before the routed skills, at both `/execute` and the route-dispatch path. Fail-open; JSON files mounted read-only at `/skills`. 7 tests, full suite green (32). *(V2.4-local resolve per decision — mirrors `agent_boot.resolve_loadout`.)*
- [x] Single shared module — logic lives in `agents/shared/loadout.py` (one impl, no per-agent copies). crew-orchestrator migrated onto it; its local copy deleted. Agents import via `from shared.loadout import ...` (shared at `/app/shared`, or baked-in for healer) + the two HYPER-SILLs JSON at `/skills`.
- [x] Startup boot-check wired on **4 agents**: `crew-orchestrator`, `nemoclaw-agent` (agents.yml), `healer-agent` (agents.yml), `agent-factory` (registry.yml). Each calls `boot_check("<name>")` on startup (lifespan / on_event), strict via `LOADOUT_STRICT`, fail-open on missing mount. All boot clean (0 missing).
- [ ] Remaining agents  ← next. Blockers: `agent-registry`/`agent-spawner` have no `main.py` (not runnable Python); `broski-bot` is discord.py (no FastAPI startup — wire into its `on_ready`); the 4 brain agents live in the BROski-Obsidian-Brain repo (separate).
- [ ] Extend loadouts to the full 25-agent roster

---

> 🐶♾️ Built for the HyperFocus z0ne — makes the FIVE WARDS binding, not aspirational.
