import re
import statistics
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "starter"))
from baseline import pack_context
from src.filters import infer_filter


def flat(text: str) -> str:
    text = re.sub(r"\s+", " ", text)
    return re.sub(r" (?=[,.;:])", "", text)


def is_hit(chunk: dict, gold: list[dict]) -> bool:
    return any(chunk["source_id"] == item["source_id"] and chunk["page"] == item["page"]
               and flat(item["evidence"]) in flat(chunk["text"]) for item in gold)


def run(retriever, questions: list[dict], top_k: int = 3, budget: int = 800,
        use_filter: bool = False) -> tuple[dict, list[dict]]:
    answerable = [q for q in questions if q.get("answerable", True)]
    if not answerable:
        raise ValueError("retrieval metrics require at least one answerable question")
    traces = []
    for question in answerable:
        filters = infer_filter(question["question"]) if use_filter else None
        started = time.perf_counter()
        results = retriever.search(question["question"], top_k=top_k, filters=filters)
        elapsed_ms = (time.perf_counter() - started) * 1000
        if len(results) > top_k or len({r["id"] for r in results}) != len(results):
            raise ValueError(f"{question['id']}: retriever returned duplicate IDs or more than top_k")
        context, context_ids = pack_context(results, budget=budget)
        hits = [is_hit(row, question["gold"]) for row in results]
        hit1 = bool(hits and hits[0])
        hit3 = any(hits[:3])
        context_hit = any(is_hit(row, question["gold"]) and row["id"] in context_ids for row in results)
        filter_ok = (all(r.get("metadata", {}).get(k) == v for k, v in filters.items() for r in results)
                     if filters else None)
        traces.append({"query_id": question["id"], "split": question["split"],
                       "question": question["question"], "strategy": retriever.name,
                       "top_k": top_k, "budget_chars": budget, "filter": filters,
                       "filter_source": "explicit_query_scope" if filters else None,
                       "filter_compliant": filter_ok, "results": results,
                       "context": context, "context_ids": context_ids,
                       "context_chars": len(context), "elapsed_ms": round(elapsed_ms, 3),
                       "hit1": hit1, "hit3": hit3, "context_hit": context_hit})
    n = len(traces)
    filter_traces = [t for t in traces if t["filter"]]
    summary = {"strategy": retriever.name, "n": n,
               "hit1": f"{sum(t['hit1'] for t in traces)}/{n}",
               "hit3": f"{sum(t['hit3'] for t in traces)}/{n}",
               "context_evidence": f"{sum(t['context_hit'] for t in traces)}/{n}",
               "avg_context_chars": round(statistics.mean(t["context_chars"] for t in traces), 1),
               "median_ms": round(statistics.median(t["elapsed_ms"] for t in traces), 3),
               "filter_questions": len(filter_traces),
               "filter_compliant_top3": (f"{sum(bool(t['filter_compliant']) for t in filter_traces)}/{len(filter_traces)}"
                                          if filter_traces else "N/A")}
    return summary, traces
