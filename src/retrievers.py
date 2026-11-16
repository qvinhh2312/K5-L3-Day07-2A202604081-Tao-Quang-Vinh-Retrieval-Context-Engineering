import math
import re
import unicodedata
from collections import Counter


def tokenize(text: str) -> list[str]:
    return re.findall(r"\w+", unicodedata.normalize("NFC", text).casefold())


STOP = set("the of and a an to in is are be for on or by with as that this it its at from which what how does do can should".split())


def tok_nostop(text: str) -> list[str]:
    return [token for token in tokenize(text) if token not in STOP]


class BM25:
    name = "bm25"

    def __init__(self, chunks: list[dict], k1: float = 1.5, b: float = 0.75) -> None:
        if not chunks:
            raise ValueError("BM25 needs at least one chunk")
        self.chunks, self.k1, self.b = chunks, k1, b
        self.tf = [Counter(tok_nostop(c["text"])) for c in chunks]
        self.lengths = [sum(row.values()) for row in self.tf]
        self.avg_len = sum(self.lengths) / len(self.lengths) or 1
        df = Counter(term for row in self.tf for term in row)
        self.idf = {term: math.log(1 + (len(chunks) - freq + 0.5) / (freq + 0.5))
                    for term, freq in df.items()}

    def search(self, query: str, top_k: int = 3, filters: dict | None = None) -> list[dict]:
        terms, rows = tok_nostop(query), []
        for i, chunk in enumerate(self.chunks):
            if filters and any(chunk.get("metadata", {}).get(k) != v for k, v in filters.items()):
                continue
            score = 0.0
            for term in terms:
                tf = self.tf[i].get(term, 0)
                if tf:
                    denom = tf + self.k1 * (1 - self.b + self.b * self.lengths[i] / self.avg_len)
                    score += self.idf.get(term, 0) * tf * (self.k1 + 1) / denom
            if score > 0:
                rows.append({**chunk, "score": score, "strategy": self.name})
        rows.sort(key=lambda row: (-row["score"], row["id"]))
        return [{**row, "rank": i + 1} for i, row in enumerate(rows[:top_k])]


def rrf(ranked_lists: list[list[dict]], top_k: int = 3, k: int = 60) -> list[dict]:
    scores, first = Counter(), {}
    for ranked in ranked_lists:
        for rank, chunk in enumerate(ranked, 1):
            scores[chunk["id"]] += 1.0 / (k + rank)
            first.setdefault(chunk["id"], chunk)
    ids = sorted(scores, key=lambda chunk_id: (-scores[chunk_id], chunk_id))[:top_k]
    return [{**first[cid], "score": scores[cid], "rank": rank, "strategy": "hybrid_rrf"}
            for rank, cid in enumerate(ids, 1)]


class Hybrid:
    name = "hybrid_rrf"

    def __init__(self, dense, lexical, pool: int = 20, k: int = 60) -> None:
        self.dense, self.lexical, self.pool, self.k = dense, lexical, pool, k

    def search(self, query: str, top_k: int = 3, filters: dict | None = None) -> list[dict]:
        return rrf([self.dense.search(query, top_k=self.pool, filters=filters),
                    self.lexical.search(query, top_k=self.pool, filters=filters)], top_k=top_k, k=self.k)
