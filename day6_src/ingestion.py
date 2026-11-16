import re
import unicodedata
from pathlib import Path

import pypdf

from .models import DocumentPage

HEADER = "NIST AI 100-1 AI RMF 1.0"
FOOTER = re.compile(r"^Page ([ivxlcdm]+|\d+)$", re.IGNORECASE)

# `part` lấy từ mục lục của tài liệu; PDF page = số trang in + 5.
PART_RANGES = {
    "executive_summary": range(6, 9),   # printed 1-3
    "part1": range(9, 25),              # printed 4-19
    "part2": range(25, 40),             # printed 20-34
    "appendix": range(40, 48),          # printed 35-42
}


def part_of(pdf_page: int) -> str | None:
    for name, rng in PART_RANGES.items():
        if pdf_page in rng:
            return name
    return None


def normalize_text(text: str) -> str:
    text = unicodedata.normalize("NFKC", text)
    text = text.replace("\u00ad", "")
    text = re.sub(r"-\n(?=[a-z])", "", text)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def strip_furniture(text: str) -> tuple[str, str | None]:
    lines = text.split("\n")
    if lines and lines[0].strip() == HEADER:
        lines = lines[1:]
    printed = None
    if lines:
        m = FOOTER.match(lines[-1].strip())
        if m:
            printed = m.group(1)
            lines = lines[:-1]
    return "\n".join(lines).strip(), printed


def load_pdf(path: Path, document_id: str, source: str,
             pages: list[int] | None = None) -> list[DocumentPage]:
    reader = pypdf.PdfReader(str(path))
    wanted = pages if pages is not None else list(range(1, len(reader.pages) + 1))
    out: list[DocumentPage] = []
    for n in wanted:
        raw = reader.pages[n - 1].extract_text() or ""
        body, printed = strip_furniture(normalize_text(raw))
        if not body:
            print(f"[canh bao] PDF page {n} không có text")
            continue
        out.append(DocumentPage(
            document_id=document_id, source=source, page=n, text=body,
            metadata={"part": part_of(n), "printed_page": printed},
        ))
    return out