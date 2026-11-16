"""Ba phương pháp retrieval cho Day 7. Mọi retriever: search(query, top_k, filters) -> list[chunk+score,rank]."""
import math, re, unicodedata
from collections import Counter

def tokenize(text):
    return re.findall(r"\w+", unicodedata.normalize("NFC", text).casefold())

STOP = set("the of and a an to in is are be for on or by with as that this it its at from which what how does do can should".split())

def tok_nostop(text):
    return [t for t in tokenize(text) if t not in STOP]

class BM25:
    """BM25 Okapi tự viết (không cần thư viện). k1=1.5, b=0.75 là giá trị mặc định phổ biến."""
    name = "bm25"
    def __init__(self, chunks, k1=1.5, b=0.75, tokenizer=tok_nostop):
        self.chunks, self.k1, self.b, self.tk = chunks, k1, b, tokenizer
        self.tf = [Counter(tokenizer(c["text"])) for c in chunks]
        self.len = [sum(t.values()) for t in self.tf]
        self.avg = sum(self.len) / len(self.len)
        df = Counter(w for t in self.tf for w in t)
        n = len(chunks)
        self.idf = {w: math.log(1 + (n - d + 0.5) / (d + 0.5)) for w, d in df.items()}

    def search(self, query, top_k=3, filters=None):
        q = self.tk(query)
        rows = []
        for i, c in enumerate(self.chunks):
            if filters and any(c["metadata"].get(k) != v for k, v in filters.items()):
                continue
            s = 0.0
            for w in q:
                f = self.tf[i].get(w, 0)
                if f:
                    s += self.idf.get(w, 0) * f * (self.k1 + 1) / (f + self.k1 * (1 - self.b + self.b * self.len[i] / self.avg))
            if s > 0:
                rows.append({**c, "score": s})
        rows.sort(key=lambda r: (-r["score"], r["id"]))
        return [{**r, "rank": n + 1, "strategy": self.name} for n, r in enumerate(rows[:top_k])]

def rrf(ranked_lists, top_k=3, k=60):
    """Reciprocal Rank Fusion: score(d) = sum 1/(k + rank). Chỉ dùng thứ hạng nên không cần chuẩn hóa score."""
    score, keep = Counter(), {}
    for lst in ranked_lists:
        for r, c in enumerate(lst, 1):
            score[c["id"]] += 1.0 / (k + r)
            keep.setdefault(c["id"], c)
    ordered = sorted(score, key=lambda i: (-score[i], i))[:top_k]   # dedupe theo id, tối đa top_k
    return [{**keep[i], "score": score[i], "rank": n + 1, "strategy": "hybrid_rrf"} for n, i in enumerate(ordered)]

class Hybrid:
    name = "hybrid_rrf"
    def __init__(self, dense, lexical, pool=20, k=60):
        self.dense, self.lexical, self.pool, self.k = dense, lexical, pool, k
    def search(self, query, top_k=3, filters=None):
        return rrf([self.dense.search(query, top_k=self.pool, filters=filters),
                    self.lexical.search(query, top_k=self.pool, filters=filters)], top_k=top_k, k=self.k)
