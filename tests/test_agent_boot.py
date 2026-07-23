"""TDD tests for the agent boot-check helper (scripts/agent_boot.py)."""
import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
from agent_boot import resolve_loadout, boot_check, Loadout, BootCheckError  # noqa: E402

REGISTRY = {
    "HS-098": {"id": "HS-098", "hero_name": "THE SACRED SIX", "status": "active"},
    "HS-085": {"id": "HS-085", "hero_name": "THE FIVE WARDS", "status": "active"},
    "HS-069": {"id": "HS-069", "hero_name": "MERCY MESSAGE", "status": "active"},
    "HS-032": {"id": "HS-032", "hero_name": "COURSE RULES", "status": "active"},
    "HS-900": {"id": "HS-900", "hero_name": "OLD THING", "status": "deprecated"},
}
LOADOUTS = {
    "_defaults": {"required": ["HS-098", "HS-085"], "optional": ["HS-069"]},
    "agents": {
        "broski-bot":    {"required": ["HS-032"], "forbidden": ["HS-069"]},
        "needs-missing": {"required": ["HS-777"]},   # not in registry
        "needs-dead":    {"required": ["HS-900"]},   # deprecated
    },
}


def _write(root: Path) -> None:
    (root / "skills-registry.json").write_text(
        json.dumps({"skills": list(REGISTRY.values())}), encoding="utf-8"
    )
    (root / "agent-loadouts.json").write_text(json.dumps(LOADOUTS), encoding="utf-8")


# ── resolve_loadout (pure) ──────────────────────────────────────────────────
def test_resolve_merges_defaults_and_agent():
    lo = resolve_loadout("broski-bot", LOADOUTS, REGISTRY)
    assert lo.required == {"HS-098", "HS-085", "HS-032"}


def test_unknown_agent_gets_defaults_only():
    lo = resolve_loadout("ghost-agent", LOADOUTS, REGISTRY)
    assert lo.required == {"HS-098", "HS-085"}
    assert lo.missing == []


def test_forbidden_is_never_resolved():
    lo = resolve_loadout("broski-bot", LOADOUTS, REGISTRY)
    assert "HS-069" in lo.forbidden
    assert "HS-069" not in lo.resolved


def test_missing_required_id_flagged():
    lo = resolve_loadout("needs-missing", LOADOUTS, REGISTRY)
    assert "HS-777" in lo.missing
    assert "HS-777" not in lo.resolved


def test_deprecated_required_counts_as_missing():
    lo = resolve_loadout("needs-dead", LOADOUTS, REGISTRY)
    assert "HS-900" in lo.missing


def test_resolved_carries_registry_metadata():
    lo = resolve_loadout("broski-bot", LOADOUTS, REGISTRY)
    assert lo.resolved["HS-098"]["hero_name"] == "THE SACRED SIX"


# ── boot_check (file IO + enforcement) ──────────────────────────────────────
def test_boot_check_strict_raises_on_missing(tmp_path):
    _write(tmp_path)
    with pytest.raises(BootCheckError):
        boot_check("needs-missing", root=tmp_path, strict=True)


def test_boot_check_nonstrict_returns_missing(tmp_path):
    _write(tmp_path)
    lo = boot_check("needs-missing", root=tmp_path, strict=False)
    assert "HS-777" in lo.missing


def test_boot_check_ok_agent_passes_strict(tmp_path):
    _write(tmp_path)
    lo = boot_check("broski-bot", root=tmp_path, strict=True)
    assert lo.required == {"HS-098", "HS-085", "HS-032"}
    assert lo.missing == []
