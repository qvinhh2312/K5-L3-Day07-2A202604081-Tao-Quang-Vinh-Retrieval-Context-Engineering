import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.filters import infer_filter


def flat(text: str) -> str:
    return re.sub(r" (?=[,.;:])", "", re.sub(r"\s+", " ", text))


def validate(path: Path, expected_split: str, expected_answerable: int, expected_unanswerable: int) -> None:
    cases = json.loads(path.read_text(encoding="utf-8"))
    chunks = json.loads((ROOT / "data" / "chunks_B.json").read_text(encoding="utf-8"))
    if not isinstance(cases, list):
        raise ValueError(f"{path.name} must contain a JSON array")
    if len({q.get("id") for q in cases}) != len(cases):
        raise ValueError(f"{path.name}: duplicate case IDs")
    by_id = {c["id"]: c for c in chunks}
    for q in cases:
        if q.get("split") != expected_split or not isinstance(q.get("question"), str) or not q["question"].strip():
            raise ValueError(f"{q.get('id')}: invalid split or question")
        if not isinstance(q.get("answerable"), bool) or not isinstance(q.get("gold"), list):
            raise ValueError(f"{q['id']}: answerable/gold invalid")
        if q["answerable"]:
            if not q.get("expected_answer") or not q["gold"]:
                raise ValueError(f"{q['id']}: answerable cases need answer and gold")
            for g in q["gold"]:
                matches = [c for c in chunks if c["source_id"] == g.get("source_id") and c["page"] == g.get("page")
                           and flat(g.get("evidence", "")) in flat(c["text"])]
                if not matches:
                    raise ValueError(f"{q['id']}: evidence not found in an exact source/page chunk")
        elif q["gold"] or not q.get("absence_reason"):
            raise ValueError(f"{q['id']}: unanswerable case needs empty gold and an absence_reason")
        if q.get("filter"):
            raise ValueError(f"{q['id']}: runtime filter fields are forbidden; infer only from question text")
        expected = q.get("expected_filter")
        if expected is not None and expected != infer_filter(q["question"]):
            raise ValueError(f"{q['id']}: expected_filter does not match explicit query scope")
        if q.get("oracle_filter") and expected_split != "dev":
            raise ValueError(f"{q['id']}: oracle_filter is only allowed for historical dev annotations")
    n_answerable = sum(q["answerable"] for q in cases)
    n_unanswerable = len(cases) - n_answerable
    if (n_answerable, n_unanswerable) != (expected_answerable, expected_unanswerable):
        raise ValueError(f"{path.name}: expected {expected_answerable}+{expected_unanswerable}, got {n_answerable}+{n_unanswerable}")
    print(f"{path.name}: valid; answerable={n_answerable}, unanswerable={n_unanswerable}")


if __name__ == "__main__":
    validate(ROOT / "data" / "benchmark_dev.json", "dev", 20, 2)
    validate(ROOT / "data" / "benchmark_test.json", "test", 5, 2)
