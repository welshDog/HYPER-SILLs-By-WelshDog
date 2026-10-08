"""Search-quality regression gate (golden queries in tests/golden_queries.json).

Floors sit a little below the measured baseline (2026-10-08: semantic R@3 0.97 /
MRR 0.966, keyword R@3 0.939 / MRR 0.907) so noise passes but a real regression
fails. Raise the floors when you improve search; never lower them to ship.
"""
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT))

import eval_search  # noqa: E402

GOLDEN = eval_search.load_golden()


def test_golden_set_is_sane():
    assert len(GOLDEN) >= 50
    assert all(g["query"].strip() and g["expect"] for g in GOLDEN)


def test_golden_ids_exist_in_registry():
    import json
    reg = json.loads((ROOT / "skills-registry.json").read_text(encoding="utf-8"))
    ids = {s["id"] for s in reg["skills"]}
    missing = [i for g in GOLDEN for i in g["expect"] if i not in ids]
    assert not missing, f"golden queries reference unknown skills: {missing}"


def test_keyword_search_floor():
    r = eval_search.score(eval_search._keyword, GOLDEN)
    assert r["recall@3"] >= 0.90, r["misses"]
    assert r["mrr"] >= 0.85


def test_semantic_search_floor():
    pytest.importorskip("sentence_transformers")
    r = eval_search.score(eval_search._semantic, GOLDEN)
    assert r["recall@3"] >= 0.93, r["misses"]
    assert r["mrr"] >= 0.92
