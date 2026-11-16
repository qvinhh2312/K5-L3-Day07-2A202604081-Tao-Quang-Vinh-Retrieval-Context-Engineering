import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.dense import Dense
from src.metrics import run
from src.retrievers import BM25, Hybrid
from src.frozen import verify_freeze
from baseline import TfidfIndex


class Tfidf:
    name = "tfidf"

    def __init__(self, chunks):
        self.index = TfidfIndex(chunks)
        self.size = len(chunks)

    def search(self, query, top_k=3, filters=None):
        # Search the full corpus, apply any metadata constraint, then preserve rank.
        rows = self.index.search(query, top_k=self.size)
        if filters:
            rows = [r for r in rows if all(r.get("metadata", {}).get(k) == v for k, v in filters.items())]
        return [{**r, "rank": i + 1, "strategy": self.name} for i, r in enumerate(rows[:top_k])]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--split", choices=("dev", "test"), default="dev")
    parser.add_argument("--final", action="store_true", help="required to read the held-out test split")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if args.split == "test":
        if not args.final:
            parser.error("test requires --final and results/freeze-config.json after config freeze")
        verify_freeze(ROOT)
    chunks = json.loads((ROOT / "data" / "chunks_B.json").read_text(encoding="utf-8"))
    cases = json.loads((ROOT / "data" / f"benchmark_{args.split}.json").read_text(encoding="utf-8"))
    questions = [q for q in cases if q["answerable"]]
    lexical = BM25(chunks)
    if args.split == "test":
        # Only frozen baseline and selected configuration are allowed on test.
        retrievers = {"bm25": lexical}
        configs = [("bm25_baseline", 3, 800), ("bm25_selected_frozen", 3, 2500)]
    else:
        dense = Dense(index="B")
        retrievers = {"tfidf": Tfidf(chunks), "dense": dense, "bm25": lexical,
                      "hybrid_rrf": Hybrid(dense, lexical, pool=20, k=60)}
        # Two single-variable follow-up experiments over the hybrid baseline.
        configs = [(name, 3, 800) for name in retrievers]
        configs += [("hybrid_rrf_top5", 5, 800), ("hybrid_rrf_top5_budget1200", 5, 1200),
                    ("bm25_budget1200_exploratory", 3, 1200),
                    ("bm25_budget2500_exploratory", 3, 2500)]
    summaries, all_traces = [], []
    for label, top_k, budget in configs:
        if args.split == "test":
            base = "bm25"
            use_filter = label == "bm25_query_filter_selected"
        else:
            if label.startswith("hybrid_rrf"):
                base = "hybrid_rrf"
            elif label.startswith("bm25_budget"):
                base = "bm25"
            else:
                base = label
            use_filter = False
        summary, traces = run(retrievers[base], questions, top_k=top_k, budget=budget,
                              use_filter=use_filter)
        summary.update({"config": label, "top_k": top_k, "budget_chars": budget,
                        "use_filter": use_filter, "split": args.split})
        summaries.append(summary)
        all_traces.extend({**t, "config": label, "use_filter": use_filter} for t in traces)
    if args.split == "dev":
        # Explicit filter ablation for each retrieval strategy, as a separate dev analysis.
        for label in ("tfidf", "dense", "bm25", "hybrid_rrf"):
            base = "hybrid_rrf" if label == "hybrid_rrf" else label
            summary, traces = run(retrievers[base], questions, top_k=3, budget=800, use_filter=True)
            summary.update({"config": f"{label}_with_query_filters", "top_k": 3, "budget_chars": 800,
                            "use_filter": True, "split": args.split})
            summaries.append(summary)
            all_traces.extend({**t, "config": f"{label}_with_query_filters", "use_filter": True} for t in traces)
    output = args.output or ROOT / "results" / f"retrieval_{args.split}.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps({"summaries": summaries, "traces": all_traces}, ensure_ascii=False, indent=2) + "\n",
                      encoding="utf-8")
    print(json.dumps(summaries, ensure_ascii=False, indent=2))
    print(f"Wrote {output.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
