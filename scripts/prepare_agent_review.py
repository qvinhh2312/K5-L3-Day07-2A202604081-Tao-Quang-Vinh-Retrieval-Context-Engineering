"""Create cases.json and a blank human-review sheet from agent traces."""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--split", choices=("dev", "test"), required=True)
    ap.add_argument("--traces", type=Path, required=True)
    ap.add_argument("--outdir", type=Path, required=True)
    args = ap.parse_args()
    cases = json.loads((ROOT / "data" / f"benchmark_{args.split}.json").read_text(encoding="utf-8"))
    traces = json.loads(args.traces.read_text(encoding="utf-8"))
    trace_ids = {t["query_id"] for t in traces}
    if trace_ids != {c["id"] for c in cases}:
        raise ValueError("trace IDs do not match benchmark case IDs")
    trace_by_id = {t["query_id"]: t for t in traces}
    reviews = []
    for c in cases:
        t = trace_by_id[c["id"]]
        row = {"query_id": c["id"], "citation_support": [None for _ in t.get("citations", [])]}
        if c["answerable"]:
            row["answer_grade"] = None
            if args.split == "test":
                row["context_grade"] = None
        else:
            row["abstention_correct"] = None
        reviews.append(row)
    args.outdir.mkdir(parents=True, exist_ok=True)
    (args.outdir / "cases.json").write_text(json.dumps([{"id": c["id"], "split": c["split"],
        "answerable": c["answerable"]} for c in cases], ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (args.outdir / "traces.json").write_text(json.dumps(traces, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (args.outdir / "reviews.json").write_text(json.dumps(reviews, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Review templates written to {args.outdir}; replace nulls with human labels before aggregation.")


if __name__ == "__main__":
    main()
