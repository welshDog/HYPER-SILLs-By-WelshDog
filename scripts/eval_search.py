#!/usr/bin/env python3
"""
eval_search.py - Measure skill-search quality against tests/golden_queries.json.

Reports recall@1/3/5 and MRR for each retriever:
  semantic  - scripts/search_skills.semantic_search (dense or TF-IDF, per index)
  keyword   - the MCP server's search_skills tool (token match)

    python scripts/eval_search.py                # table for all retrievers
    python scripts/eval_search.py --json         # machine-readable
    python scripts/eval_search.py --misses       # list queries that miss @5
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GOLDEN = ROOT / "tests" / "golden_queries.json"
KS = (1, 3, 5)

sys.path.insert(0, str(ROOT / "scripts"))


def load_golden(path: Path = GOLDEN) -> list[dict]:
    return json.loads(path.read_text(encoding="utf-8"))["queries"]


def _semantic(query: str, limit: int) -> list[str]:
    from search_skills import semantic_search
    return [h["id"] for h in semantic_search(query, limit=limit)]


def _keyword(query: str, limit: int) -> list[str]:
    sys.path.insert(0, str(ROOT))
    import mcp_server  # type: ignore
    raw = mcp_server.search_skills(query=query, limit=limit)
    return [r["id"] for r in json.loads(raw)["results"]]


RETRIEVERS = {"semantic": _semantic, "keyword": _keyword}


def score(retrieve, golden: list[dict], depth: int = max(KS)) -> dict:
    hits = {k: 0 for k in KS}
    rr_sum = 0.0
    misses = []
    for g in golden:
        ranked = retrieve(g["query"], depth)
        expect = set(g["expect"])
        rank = next((i + 1 for i, sid in enumerate(ranked) if sid in expect), None)
        if rank:
            rr_sum += 1.0 / rank
            for k in KS:
                if rank <= k:
                    hits[k] += 1
        if rank is None:
            misses.append({"query": g["query"], "expect": g["expect"], "got": ranked[:3]})
    n = len(golden)
    out = {f"recall@{k}": round(hits[k] / n, 3) for k in KS}
    out["mrr"] = round(rr_sum / n, 3)
    out["n"] = n
    out["misses"] = misses
    return out


def evaluate(names: list[str] | None = None) -> dict:
    golden = load_golden()
    return {name: score(RETRIEVERS[name], golden) for name in (names or RETRIEVERS)}


def main() -> int:
    ap = argparse.ArgumentParser(description="Evaluate HYPER-SILLs search quality.")
    ap.add_argument("--retriever", choices=list(RETRIEVERS), action="append")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--misses", action="store_true", help="list queries missing @5")
    args = ap.parse_args()

    results = evaluate(args.retriever)
    if args.json:
        print(json.dumps(results, indent=2))
        return 0

    print(f"{'retriever':<10} {'n':>4} {'R@1':>6} {'R@3':>6} {'R@5':>6} {'MRR':>6}")
    for name, r in results.items():
        print(f"{name:<10} {r['n']:>4} {r['recall@1']:>6} {r['recall@3']:>6} "
              f"{r['recall@5']:>6} {r['mrr']:>6}")
    if args.misses:
        for name, r in results.items():
            for m in r["misses"]:
                print(f"\n[{name}] MISS {m['query']!r}\n   expect {m['expect']}  got {m['got']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
