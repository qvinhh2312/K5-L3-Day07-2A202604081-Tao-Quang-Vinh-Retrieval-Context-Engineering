import re
from collections import defaultdict
from typing import Any


def flat(s: str) -> str:
    s = re.sub(r"\s+", " ", s)
    return re.sub(r" (?=[,.;:])", "", s)    # pypdf chèn khoảng trắng sau chữ small-caps (GOVERN ,)


def _gold_pages(q: dict[str, Any]) -> set[int]:
    return {q["gold_page"], *q.get("alt_gold_pages", [])}


def _hit_flags(q: dict[str, Any], h: dict[str, Any]) -> tuple[bool, bool, bool]:
    same_doc = h["document_id"] == q["gold_source_id"]
    page_ok = same_doc and h["page"] in _gold_pages(q)
    evidence_ok = flat(q["evidence_quote"]) in flat(h["text"])
    return page_ok, evidence_ok, page_ok and evidence_ok


def evaluate_query(question: dict[str, Any], hits: list[dict[str, Any]]) -> dict[str, Any]:
    """Hit = đúng nguồn/trang gold VÀ chunk chứa đủ evidence_quote. Evidence bị tách qua 2 chunk = không hit."""
    rows = []
    for rank, h in enumerate(hits[:3], 1):
        page_ok, evidence_ok, hit = _hit_flags(question, h)
        rows.append({"rank": rank, "chunk_id": h["chunk_id"], "document_id": h.get("document_id"),
                     "source": h.get("source"), "page": h["page"], "printed_page": h.get("printed_page"),
                     "part": h.get("part"), "score": round(float(h["score"]), 4), "page_match": page_ok,
                     "evidence_in_chunk": evidence_ok, "hit": hit, "text": h["text"]})
    f = question.get("filter")
    filter_ok = None if not f else all(r["part"] == f["part"] for r in rows)
    first = next((r["rank"] for r in rows if r["hit"]), None)
    return {"id": question["id"], "split": question["split"], "type": question["type"],
            "question": question["question"], "filter": f, "gold_page": question["gold_page"],
            "evidence_quote": question["evidence_quote"], "hit1": bool(rows and rows[0]["hit"]),
            "hit3": first is not None, "first_hit_rank": first, "filter_compliant": filter_ok,
            "top3": rows}


def summarize(traces: list[dict[str, Any]]) -> dict[str, Any]:
    """traces mỗi phần tử có thêm khóa 'strategy'. Trả về tử/mẫu theo strategy và split."""
    groups: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for t in traces:
        groups[(t["strategy"], t["split"])].append(t)
    out: dict[str, Any] = {}
    for (strategy, split), ts in sorted(groups.items()):
        fq = [t for t in ts if t["filter"]]
        out.setdefault(strategy, {})[split] = {
            "n": len(ts),
            "hit1": f"{sum(t['hit1'] for t in ts)}/{len(ts)}",
            "hit3": f"{sum(t['hit3'] for t in ts)}/{len(ts)}",
            "filter_questions": len(fq),
            "filter_compliant_top3": f"{sum(bool(t['filter_compliant']) for t in fq)}/{len(fq)}" if fq else "N/A",
        }
    return out
