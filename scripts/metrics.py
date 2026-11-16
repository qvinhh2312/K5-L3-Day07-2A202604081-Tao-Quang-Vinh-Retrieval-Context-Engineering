"""Hit@1 / Evidence Hit@3 / Context Evidence Rate cho mọi retriever, cùng định nghĩa hit với starter/baseline.py."""
import sys, json, time, statistics
sys.path.insert(0, "starter")
from baseline import hit, pack_context

def run(retriever, questions, top_k=3, budget=800, use_filter=False):
    traces = []
    for q in questions:
        t0 = time.perf_counter()
        flt = q.get("filter") if use_filter else None
        res = retriever.search(q["question"], top_k=top_k, filters=flt)
        ctx, ids = pack_context(res, budget)
        ms = (time.perf_counter() - t0) * 1000
        top3 = res[:3]
        marks = [hit(c, q["gold"]) for c in top3]
        traces.append({"query_id": q["id"], "hit1": bool(marks and marks[0]), "hit3": any(marks),
                       "context_hit": any(hit(c, q["gold"]) and c["id"] in ids for c in res),
                       "ctx_chars": len(ctx), "ms": ms, "top3_ids": [c["id"] for c in top3], "filter": flt})
    n = len(traces)
    s = {"n": n, "hit1": f'{sum(t["hit1"] for t in traces)}/{n}', "hit3": f'{sum(t["hit3"] for t in traces)}/{n}',
         "ctx": f'{sum(t["context_hit"] for t in traces)}/{n}', "median_ms": round(statistics.median(t["ms"] for t in traces), 2)}
    return s, traces
