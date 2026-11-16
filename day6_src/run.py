import argparse
import json
import os
import platform
import statistics
import sys
import time
from pathlib import Path

from dotenv import load_dotenv

from . import chunking, evaluation
from .ingestion import load_pdf

ROOT = Path(__file__).resolve().parents[1]
PDF_PATH = ROOT / "data" / "NIST.AI.100-1.pdf"
MANIFEST = ROOT / "data" / "manifest.json"
BENCH = ROOT / "data" / "benchmark_day6_seed.json"
RESULTS = ROOT / "results"
DOCUMENT_ID = "nist-ai-100-1"
SOURCE = "NIST.AI.100-1.pdf"
MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# Tham số phải khớp artifacts/experiment_log.csv. C dùng lại index của B và chỉ thêm filter.
FIXED = {"size": 500, "overlap": 50}
PARA = {"max_size": 800, "split_overlap": 50}
STRATEGIES = {
    "A": {"index": "A", "use_filter": False},
    "B": {"index": "B", "use_filter": False},
    "C": {"index": "B", "use_filter": True},
}


def load_pages():
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    counted = [p["pdf_page"] for p in manifest["pages"] if p["counted"]]
    return load_pdf(PDF_PATH, DOCUMENT_ID, SOURCE, pages=counted), manifest


def build_chunks(pages):
    a = [c for p in pages for c in chunking.fixed_size(p, **FIXED)]
    b = [c for p in pages for c in chunking.by_paragraph(p, **PARA)]
    return {"A": a, "B": b}


def length_stats(chunks):
    lens = sorted(len(c.text) for c in chunks)
    return {"n_chunks": len(lens), "total_chars": sum(lens), "min": lens[0], "median": statistics.median(lens),
            "mean": round(statistics.mean(lens), 1), "p90": lens[int(0.9 * (len(lens) - 1))], "max": lens[-1]}


def load_questions(split=None):
    qs = json.loads(BENCH.read_text(encoding="utf-8"))
    return [q for q in qs if split in (None, q["split"])]


def cmd_check_chunks(_args):
    """Kiểm tra cấu trúc chunk và, CHỈ trên dev, evidence có nằm trọn trong một chunk của trang gold không."""
    pages, _ = load_pages()
    sets = build_chunks(pages)
    dev = load_questions("dev")
    for name, chunks in sets.items():
        print(f"\n[{name}] {length_stats(chunks)}")
        miss = []
        for q in dev:
            gold = [c for c in chunks if c.page == q["gold_page"]]
            if not any(evaluation.flat(q["evidence_quote"]) in evaluation.flat(c.text) for c in gold):
                miss.append(q["id"])
        print(f"  dev có evidence nằm trọn trong 1 chunk của trang gold: {len(dev) - len(miss)}/{len(dev)}"
              + (f" | bị tách/thiếu: {miss}" if miss else ""))
    print("\nVí dụ 3 chunk B đầu của trang PDF 9:")
    for c in [c for c in sets["B"] if c.page == 9][:3]:
        print(f"  {c.chunk_id} ({len(c.text)} ký tự): {c.text[:110]}...")


def cmd_ingest(_args):
    from .embeddings import SentenceTransformerEmbedder
    from .store import PgVectorStore
    load_dotenv(ROOT / ".env")
    url = os.getenv("DATABASE_URL")
    if not url:
        sys.exit("Thiếu DATABASE_URL trong starter/.env")
    t0 = time.perf_counter()
    pages, manifest = load_pages()
    sets = build_chunks(pages)
    embedder = SentenceTransformerEmbedder(MODEL)
    store = PgVectorStore(url, embedder.dimensions)
    store.create_schema()
    stats = {"model": MODEL, "dimensions": embedder.dimensions, "max_seq_length": embedder.max_seq_length,
             "sentence_transformers": embedder.library_version, "python": platform.python_version(),
             "pdf_sha256": manifest["sha256"], "counted_pages": manifest["counted_pages"],
             "cost_usd": 0.0, "strategies": {}, **store.versions()}
    for name, chunks in sets.items():
        before = store.count(name)
        t1 = time.perf_counter()
        vecs = embedder.embed_documents([c.text for c in chunks])
        t_embed = time.perf_counter() - t1
        t2 = time.perf_counter()
        store.upsert(name, chunks, vecs)
        t_db = time.perf_counter() - t2
        after = store.count(name)
        stats["strategies"][name] = {**length_stats(chunks), "rows_before": before, "rows_after": after,
                                     "embed_seconds": round(t_embed, 2), "db_seconds": round(t_db, 2)}
        print(f"[{name}] chunks={len(chunks)} dòng DB trước={before} sau={after} embed={t_embed:.1f}s")
    stats["total_seconds"] = round(time.perf_counter() - t0, 2)
    RESULTS.mkdir(exist_ok=True)
    (RESULTS / "ingest_stats.json").write_text(json.dumps(stats, ensure_ascii=False, indent=2), encoding="utf-8")
    print("Đã ghi results/ingest_stats.json. Chạy lại lệnh này: 'sau' phải bằng số cũ (không nhân đôi).")


def cmd_eval(args):
    if args.split == "test" and not args.final:
        sys.exit("Split test chỉ chạy khi đã đóng băng cấu hình: thêm --final.")
    from .embeddings import SentenceTransformerEmbedder
    from .store import PgVectorStore
    load_dotenv(ROOT / ".env")
    url = os.getenv("DATABASE_URL")
    if not url:
        sys.exit("Thiếu DATABASE_URL trong starter/.env")
    questions = load_questions(args.split)
    embedder = SentenceTransformerEmbedder(MODEL)
    store = PgVectorStore(url, embedder.dimensions)
    qvecs = {q["id"]: embedder.embed_query(q["question"]) for q in questions}   # cùng query vector cho A/B/C
    traces = []
    t0 = time.perf_counter()
    for name, cfg in STRATEGIES.items():
        if store.count(cfg["index"]) == 0:
            sys.exit(f"Index {cfg['index']} rỗng. Chạy 'python -m src.run ingest' trước.")
        for q in questions:
            flt = q.get("filter") if cfg["use_filter"] else None   # A, B không bao giờ lọc
            hits = store.search(cfg["index"], qvecs[q["id"]], top_k=3, filters=flt)
            tr = evaluation.evaluate_query(q, hits)
            tr["strategy"], tr["filter_applied"] = name, flt
            traces.append(tr)
    RESULTS.mkdir(exist_ok=True)
    with (RESULTS / f"trace_{args.split}.jsonl").open("w", encoding="utf-8") as f:
        for t in traces:
            f.write(json.dumps(t, ensure_ascii=False) + "\n")
    summary = evaluation.summarize(traces)
    summary["_run"] = {"split": args.split, "seconds": round(time.perf_counter() - t0, 2), "model": MODEL}
    (RESULTS / f"metrics_{args.split}.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    for name in STRATEGIES:
        print(name, summary[name][args.split])


def main() -> None:
    ap = argparse.ArgumentParser(prog="python -m src.run")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("check-chunks").set_defaults(fn=cmd_check_chunks)
    sub.add_parser("ingest").set_defaults(fn=cmd_ingest)
    ev = sub.add_parser("eval")
    ev.add_argument("--split", choices=["dev", "test"], required=True)
    ev.add_argument("--final", action="store_true")
    ev.set_defaults(fn=cmd_eval)
    args = ap.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()
