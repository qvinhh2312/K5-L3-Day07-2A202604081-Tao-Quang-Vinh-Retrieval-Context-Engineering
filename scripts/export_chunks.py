"""Export Day 6 chunks (strategy A/B) to the Day 7 JSON contract. Run from repo root."""
import argparse, json, re, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from day6_src import chunking
from day6_src.ingestion import load_pdf

def norm(t):  # pypdf chèn khoảng trắng trước dấu câu sau chữ small-caps: "GOVERN ," -> "GOVERN,"
    return re.sub(r" (?=[,.;:])", "", t)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--strategy", choices=["A", "B"], default="B")
    ap.add_argument("--out", type=Path, default=ROOT / "data" / "chunks_B.json")
    a = ap.parse_args()
    man = json.loads((ROOT / "data" / "manifest.json").read_text(encoding="utf-8"))
    pages = [p["pdf_page"] for p in man["pages"] if p["counted"]]
    P = load_pdf(ROOT / "data" / "NIST.AI.100-1.pdf", "nist-ai-100-1", "NIST.AI.100-1.pdf", pages=pages)
    if a.strategy == "A":
        cs = [c for p in P for c in chunking.fixed_size(p, 500, 50)]
    else:
        cs = [c for p in P for c in chunking.by_paragraph(p, 800, 50)]
    out = [{"id": c.chunk_id, "source_id": c.document_id, "source": c.source, "page": c.page,
            "text": norm(c.text), "metadata": c.metadata} for c in cs]
    a.out.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"strategy {a.strategy}: {len(out)} chunks -> {a.out}")

if __name__ == "__main__":
    main()
