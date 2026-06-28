#!/usr/bin/env python3
"""
search_skills.py — Semantic skill search over the HYPER-SILLs vault.

Find skills by *describing the problem*, not memorising hero names or IDs.

Pluggable embedding backends (resolved automatically, best-first):
  1. local   — sentence-transformers all-MiniLM-L6-v2 (offline, free, real dense
               embeddings). Used when the package + model are available.
  2. openai  — text-embedding-3-small, if OPENAI_API_KEY is set.
  3. tfidf   — zero-dependency local TF-IDF fallback (always works offline).

    python scripts/search_skills.py "make my agent restart when it crashes"
    python scripts/search_skills.py "publish my skills" --backend tfidf

The vector index is built by `embed_skills.py` and cached in
`vector-store/skill_index.json`. If missing, it's built on the fly.

Importable: `from search_skills import semantic_search` for the MCP server.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import re
import sys
from pathlib import Path

VAULT_ROOT = Path(__file__).resolve().parent.parent
REGISTRY_PATH = VAULT_ROOT / "skills-registry.json"
INDEX_PATH = VAULT_ROOT / "vector-store" / "skill_index.json"

LOCAL_MODEL = "all-MiniLM-L6-v2"
OPENAI_MODEL = "text-embedding-3-small"

_STOP = {
    "the", "a", "an", "and", "or", "to", "of", "in", "on", "for", "with", "is",
    "are", "be", "this", "that", "it", "as", "at", "by", "my", "your", "how",
    "do", "i", "you", "when", "what", "which", "use", "using", "via",
}


def tokenize(text: str) -> list[str]:
    words = re.split(r"[^a-z0-9]+", text.lower())
    return [w for w in words if len(w) > 2 and w not in _STOP]


# ── Document text per skill (what we embed) ────────────────────────────────────

def skill_document(skill: dict) -> str:
    """The searchable text for a skill: hero + description + tags + body excerpt."""
    parts = [
        skill.get("hero_name", ""),
        skill.get("hero_name", ""),  # weight hero name x2
        skill.get("description", ""),
        skill.get("category", ""),
        " ".join(skill.get("tags", [])),
    ]
    fp = VAULT_ROOT / skill.get("file", "")
    if fp.exists():
        body = fp.read_text(encoding="utf-8", errors="replace")
        gn = re.search(r'graph_notes:\s*["\'](.+?)["\']', body)
        if gn:
            parts.append(gn.group(1))
        parts.append(body[:1200])
    return " ".join(parts)


# ── Embedding backends ─────────────────────────────────────────────────────────

_EMBEDDER_CACHE: dict[str, object] = {}


class _LocalEmbedder:
    name = f"local:{LOCAL_MODEL}"

    def __init__(self):
        # Keep stdout pristine — the MCP server speaks JSON-RPC over stdout, so a
        # stray progress bar / log line would corrupt the protocol.
        os.environ.setdefault("HF_HUB_DISABLE_PROGRESS_BARS", "1")
        os.environ.setdefault("TRANSFORMERS_VERBOSITY", "error")
        import logging
        for n in ("sentence_transformers", "transformers", "torch"):
            logging.getLogger(n).setLevel(logging.ERROR)
        from sentence_transformers import SentenceTransformer
        self.model = SentenceTransformer(LOCAL_MODEL)

    def encode(self, texts: list[str]) -> list[list[float]]:
        vecs = self.model.encode(texts, normalize_embeddings=True, show_progress_bar=False)
        return [[round(float(x), 6) for x in v] for v in vecs]


class _OpenAIEmbedder:
    name = f"openai:{OPENAI_MODEL}"

    def __init__(self):
        from openai import OpenAI
        self.client = OpenAI()

    def encode(self, texts: list[str]) -> list[list[float]]:
        out = []
        # batch to stay under request limits
        for i in range(0, len(texts), 256):
            resp = self.client.embeddings.create(model=OPENAI_MODEL, input=texts[i:i + 256])
            for d in resp.data:
                v = d.embedding
                norm = math.sqrt(sum(x * x for x in v)) or 1.0
                out.append([round(x / norm, 6) for x in v])
        return out


def resolve_embedder(backend: str = "auto"):
    """Return an embedder instance, or None to signal the TF-IDF fallback."""
    backend = (backend or "auto").lower()
    if backend in ("tfidf", "keyword", "none"):
        return None

    order = []
    if backend in ("auto",):
        order = ["local", "openai"]
    elif backend in ("local", "st", "sentence-transformers"):
        order = ["local"]
    elif backend == "openai":
        order = ["openai"]

    for kind in order:
        if kind in _EMBEDDER_CACHE:
            return _EMBEDDER_CACHE[kind]
        try:
            if kind == "local":
                import importlib.util
                if not importlib.util.find_spec("sentence_transformers"):
                    continue
                emb = _LocalEmbedder()
            elif kind == "openai":
                if not os.environ.get("OPENAI_API_KEY"):
                    continue
                emb = _OpenAIEmbedder()
            else:
                continue
            _EMBEDDER_CACHE[kind] = emb
            return emb
        except Exception as e:  # noqa: BLE001 — any failure -> try next / fall back
            print(f"(embedder '{kind}' unavailable: {type(e).__name__}: {str(e)[:80]})",
                  file=sys.stderr)
            continue
    return None  # -> TF-IDF


def _embedder_for_index(index: dict):
    """Re-create the embedder that matches an index's stored backend name."""
    name = index.get("backend", "")
    if name.startswith("local:"):
        return resolve_embedder("local")
    if name.startswith("openai:"):
        return resolve_embedder("openai")
    return None


# ── Index build ────────────────────────────────────────────────────────────────

def _load_skills() -> list[dict]:
    reg = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    return [s for s in reg.get("skills", []) if s.get("status", "").lower() != "archived"]


def _build_tfidf(skills: list[dict]) -> dict:
    tokenized, df = [], {}
    for s in skills:
        tf: dict[str, int] = {}
        for t in tokenize(skill_document(s)):
            tf[t] = tf.get(t, 0) + 1
        tokenized.append(tf)
        for t in tf:
            df[t] = df.get(t, 0) + 1
    n = len(skills)
    idf = {t: math.log((n + 1) / (c + 1)) + 1 for t, c in df.items()}
    docs = []
    for s, tf in zip(skills, tokenized):
        vec = {t: (1 + math.log(c)) * idf[t] for t, c in tf.items()}
        norm = math.sqrt(sum(v * v for v in vec.values())) or 1.0
        docs.append({"id": s["id"], "hero_name": s.get("hero_name", ""),
                     "description": s.get("description", ""), "category": s.get("category", ""),
                     "vec": vec, "norm": norm})
    return {"backend": "tfidf", "idf": idf, "docs": docs}


def _build_dense(skills: list[dict], embedder) -> dict:
    vecs = embedder.encode([skill_document(s) for s in skills])
    docs = []
    for s, v in zip(skills, vecs):
        docs.append({"id": s["id"], "hero_name": s.get("hero_name", ""),
                     "description": s.get("description", ""), "category": s.get("category", ""),
                     "vec": v})
    return {"backend": embedder.name, "dim": len(vecs[0]) if vecs else 0, "docs": docs}


def build_index(backend: str = "auto") -> dict:
    skills = _load_skills()
    embedder = resolve_embedder(backend)
    if embedder is None:
        return _build_tfidf(skills)
    try:
        return _build_dense(skills, embedder)
    except Exception as e:  # noqa: BLE001
        print(f"(dense embedding failed: {type(e).__name__}; using TF-IDF)", file=sys.stderr)
        return _build_tfidf(skills)


def load_index(rebuild: bool = False, backend: str = "auto") -> dict:
    if not rebuild and INDEX_PATH.exists():
        return json.loads(INDEX_PATH.read_text(encoding="utf-8"))
    return build_index(backend)


# ── Search ─────────────────────────────────────────────────────────────────────

def _tfidf_query_vec(query: str, idf: dict) -> tuple[dict, float]:
    tf: dict[str, int] = {}
    for t in tokenize(query):
        tf[t] = tf.get(t, 0) + 1
    vec = {t: (1 + math.log(c)) * idf.get(t, 1.0) for t, c in tf.items()}
    norm = math.sqrt(sum(v * v for v in vec.values())) or 1.0
    return vec, norm


def _search_tfidf(query: str, index: dict, limit: int) -> list[dict]:
    qvec, qnorm = _tfidf_query_vec(query, index["idf"])
    if not qvec:
        return []
    out = []
    for d in index["docs"]:
        dot = sum(qvec.get(t, 0.0) * v for t, v in d["vec"].items())
        score = dot / (qnorm * d["norm"]) if dot else 0.0
        if score > 0:
            out.append((score, d))
    out.sort(key=lambda x: x[0], reverse=True)
    return _fmt(out[:limit])


def _search_dense(query: str, index: dict, limit: int) -> list[dict] | None:
    embedder = _embedder_for_index(index)
    if embedder is None:
        return None  # signal caller to fall back
    try:
        qv = embedder.encode([query])[0]
    except Exception:  # noqa: BLE001
        return None
    try:
        import numpy as np
        mat = np.array([d["vec"] for d in index["docs"]], dtype="float32")
        q = np.array(qv, dtype="float32")
        scores = mat @ q  # vectors are normalised -> dot == cosine
        order = scores.argsort()[::-1][:limit]
        ranked = [(float(scores[i]), index["docs"][i]) for i in order if scores[i] > 0]
    except Exception:  # noqa: BLE001 — numpy missing: pure-python cosine
        ranked = []
        for d in index["docs"]:
            dot = sum(a * b for a, b in zip(qv, d["vec"]))
            if dot > 0:
                ranked.append((dot, d))
        ranked.sort(key=lambda x: x[0], reverse=True)
        ranked = ranked[:limit]
    return _fmt(ranked)


def _fmt(ranked: list[tuple]) -> list[dict]:
    return [{"id": d["id"], "hero_name": d["hero_name"], "description": d["description"],
             "category": d["category"], "score": round(score, 4)} for score, d in ranked]


# Records the engine actually used by the last semantic_search() call, so the MCP
# server can report the TRUE backend (tfidf / local:… / openai:…) instead of a
# hardcoded label. Honest observability beats a pretty lie.
_ACTIVE_BACKEND: dict[str, str | None] = {"name": None}


def active_backend() -> str:
    return _ACTIVE_BACKEND["name"] or "unknown"


def semantic_search(query: str, limit: int = 5, index: dict | None = None) -> list[dict]:
    """Rank skills by semantic similarity to the query. Returns a list of dicts."""
    if not query.strip():
        return []
    idx = index or load_index()
    _ACTIVE_BACKEND["name"] = idx.get("backend")
    if idx.get("backend") == "tfidf":
        return _search_tfidf(query, idx, limit)
    hits = _search_dense(query, idx, limit)
    if hits is not None:
        return hits
    # Dense index but the embedder is unavailable now → robust TF-IDF fallback.
    return _search_tfidf(query, build_index("tfidf"), limit)


def main() -> int:
    ap = argparse.ArgumentParser(description="Semantic search over HYPER-SILLs.")
    ap.add_argument("query", nargs="*", help="What you're trying to do")
    ap.add_argument("--limit", type=int, default=5)
    ap.add_argument("--backend", default="auto", choices=["auto", "local", "openai", "tfidf"])
    ap.add_argument("--rebuild", action="store_true", help="Rebuild the index first")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    query = " ".join(args.query).strip()
    if not query:
        print('Describe what you need, e.g.: search_skills.py "auto-restart a crashed agent"')
        return 1

    if args.rebuild or args.backend != "auto":
        idx = build_index(args.backend)
    else:
        idx = load_index()
    hits = semantic_search(query, limit=args.limit, index=idx)

    if args.json:
        print(json.dumps({"query": query, "backend": idx.get("backend"), "results": hits},
                         ensure_ascii=False, indent=2))
        return 0
    if not hits:
        print(f"No stress — nothing matched '{query}'. Try fewer / different words.")
        return 0
    print(f"\nTop {len(hits)} for: {query}   [backend: {idx.get('backend')}]\n")
    for h in hits:
        print(f"  {h['id']}  {h['hero_name']}  (score {h['score']}, {h['category']})")
        print(f"      {h['description']}")
    print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
