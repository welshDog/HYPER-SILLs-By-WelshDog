#!/usr/bin/env python3
"""
HYPER-SILLs Agent Boot-Check Helper

An agent calls boot_check("<its-name>") on startup to resolve its skill loadout
(from agent-loadouts.json, merged with _defaults) and confirm every REQUIRED
skill is available. If any required skill is missing, strict mode refuses full
boot — so the FIVE WARDS / SACRED SIX are binding, not aspirational.

"Available" = present in skills-registry.json AND status not deprecated/archived.
This is deliberately self-contained (no live MCP dependency at container start);
the registry is the boot-time source of truth. Forbidden skills are never
resolved, so an agent can't load another repo's rules even by accident.

Usage (library):
    from agent_boot import boot_check
    loadout = boot_check("crew-orchestrator")        # raises if required missing
    inject(loadout.resolved)                          # required + optional metadata

Usage (CLI / ops):
    python scripts/agent_boot.py crew-orchestrator          # exit 1 if missing
    python scripts/agent_boot.py <agent> <repo-root> --soft # never fail
"""
from __future__ import annotations

import json
import sys
from dataclasses import dataclass, field
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

# Lifecycle states a live agent must never depend on (mirrors skill_linter.py).
DEAD_STATUSES = {"deprecated", "archived"}


class BootCheckError(RuntimeError):
    """Raised when an agent's required skills are not available at boot."""


@dataclass
class Loadout:
    agent: str
    required: set[str]
    optional: set[str]
    forbidden: set[str]
    resolved: dict[str, dict] = field(default_factory=dict)  # id -> registry entry
    missing: list[str] = field(default_factory=list)          # required ids not available


def _available(sid: str, registry: dict[str, dict]) -> bool:
    entry = registry.get(sid)
    return entry is not None and entry.get("status", "").lower() not in DEAD_STATUSES


def resolve_loadout(agent: str, loadouts: dict, registry: dict[str, dict]) -> Loadout:
    """Merge _defaults with the agent's entry and resolve against the registry.

    Pure function — no IO — so it's trivially testable. Unknown agents still
    inherit _defaults (the universal laws apply to everyone).
    """
    defaults = loadouts.get("_defaults", {})
    entry = loadouts.get("agents", {}).get(agent, {})

    def effective(key: str) -> set[str]:
        return set(defaults.get(key, [])) | set(entry.get(key, []))

    required = effective("required")
    optional = effective("optional")
    forbidden = effective("forbidden")

    missing = sorted(sid for sid in required if not _available(sid, registry))

    resolved: dict[str, dict] = {}
    for sid in (required | optional) - forbidden:
        if _available(sid, registry):
            resolved[sid] = registry[sid]

    return Loadout(agent, required, optional, forbidden, resolved, missing)


def _load(root: Path) -> tuple[dict, dict[str, dict]]:
    root = Path(root)
    registry = {
        s["id"]: s
        for s in json.loads(
            (root / "skills-registry.json").read_text(encoding="utf-8")
        )["skills"]
    }
    loadouts = json.loads((root / "agent-loadouts.json").read_text(encoding="utf-8"))
    return loadouts, registry


def boot_check(agent: str, root: Path | str = ".", strict: bool = True) -> Loadout:
    """Resolve + enforce an agent's loadout at boot.

    strict=True (default): raise BootCheckError if any required skill is missing
    (refuse full boot). strict=False: return the Loadout with .missing populated
    so the caller can run degraded.
    """
    loadouts, registry = _load(Path(root))
    loadout = resolve_loadout(agent, loadouts, registry)
    if loadout.missing and strict:
        raise BootCheckError(
            f"Agent '{agent}' is missing required skills {loadout.missing} "
            f"— refusing full boot. Run with strict=False to degrade."
        )
    return loadout


def _main(argv: list[str]) -> int:
    if not argv:
        print("usage: python scripts/agent_boot.py <agent> [repo-root] [--soft]")
        return 2
    agent = argv[0]
    root = argv[1] if len(argv) > 1 and not argv[1].startswith("-") else "."
    strict = "--soft" not in argv
    try:
        lo = boot_check(agent, root=root, strict=strict)
    except BootCheckError as e:
        print(f"BOOT REFUSED: {e}")
        return 1
    heroes = ", ".join(sorted(v.get("hero_name", k) for k, v in lo.resolved.items()))
    print(f"boot OK: '{agent}' wears {len(lo.resolved)} skills [{heroes}]")
    if lo.missing:
        print(f"  (degraded — missing required: {lo.missing})")
    return 0


if __name__ == "__main__":
    sys.exit(_main(sys.argv[1:]))
