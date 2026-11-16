"""Run the real agent on dev or, after freeze, on the held-out test cases."""
import argparse
import json
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "starter"))

from agentic import run_agent
from src.agent import OpenAICompatibleController
from src.retrievers import BM25


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--split", choices=("dev", "test"), default="dev")
    parser.add_argument("--final", action="store_true")
    parser.add_argument("--config", choices=("bm25_baseline", "bm25_filter_selected"), default="bm25_filter_selected")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if args.split == "test":
        freeze = ROOT / "results" / "freeze-config.json"
        if not args.final or not freeze.exists():
            parser.error("test requires --final and results/freeze-config.json after config freeze")
    load_dotenv(ROOT / ".env")
    model = os.getenv("AGENT_MODEL", "gpt-4o-mini")
    chunks = json.loads((ROOT / "data" / "chunks_B.json").read_text(encoding="utf-8"))
    cases = json.loads((ROOT / "data" / f"benchmark_{args.split}.json").read_text(encoding="utf-8"))
    retriever = BM25(chunks)
    traces = []
    for case in cases:
        controller = None
        try:
            controller = OpenAICompatibleController(model=model)
            result = run_agent(case["question"], controller, retriever,
                               filters=case.get("filter") if args.config == "bm25_filter_selected" else None,
                               max_searches=4, top_k=3, budget=800)
            traces.append({"query_id": case["id"], **result, "model": model,
                           "total_tokens": controller.total_tokens,
                           "prompt_tokens": controller.prompt_tokens,
                           "completion_tokens": controller.completion_tokens,
                           "config": args.config})
        except Exception as exc:
            traces.append({"query_id": case["id"], "status": "error", "error": str(exc),
                           "events": [], "citations": [], "model": model,
                           "total_tokens": controller.total_tokens if controller else 0,
                           "prompt_tokens": controller.prompt_tokens if controller else 0,
                           "completion_tokens": controller.completion_tokens if controller else 0,
                           "config": args.config})
    output = args.output or ROOT / "results" / "agent" / f"{args.split}_{args.config}.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(traces, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"saved {len(traces)} traces to {output.relative_to(ROOT)}; model={model}; "
          f"tokens={sum(t.get('total_tokens', 0) for t in traces)} "
          f"(prompt={sum(t.get('prompt_tokens', 0) for t in traces)}, "
          f"completion={sum(t.get('completion_tokens', 0) for t in traces)})")
    print(f"errors={sum(t.get('status') == 'error' for t in traces)}")


if __name__ == "__main__":
    main()
