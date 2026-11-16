import re

from .models import Chunk, DocumentPage

# Dòng mở đầu một khối mới: heading số, GOVERN/MAP/MEASURE/MANAGE x.y, Table, Fig., Appendix, Part, bullet.
HEAD = re.compile(
    r"^(?:\d+(?:\.\d+)*\.?\s+[A-Z]|(?:GOVERN|MAP|MEASURE|MANAGE)\s+\d|Table\s+\d|"
    r"Fig\.\s+\d|Appendix\s+[A-D]\b|Part\s+\d:|•)"
)
SENTENCE_END = re.compile(r"[.:;?!)”\"]$")


def _make(page: DocumentPage, tag: str, idx: int, text: str) -> Chunk:
    meta = dict(page.metadata)
    meta["chunk_index"] = idx
    return Chunk(
        chunk_id=f"{page.document_id}-{tag}-p{page.page:03d}-c{idx:02d}",
        document_id=page.document_id, source=page.source, page=page.page,
        text=text, metadata=meta,
    )


def fixed_size(page: DocumentPage, size: int, overlap: int) -> list[Chunk]:
    if not 0 <= overlap < size:
        raise ValueError("overlap phải nằm trong [0, size)")
    text = " ".join(page.text.split())
    chunks, start, idx = [], 0, 0
    while start < len(text):
        end = min(start + size, len(text))
        chunks.append(_make(page, "fixed", idx, text[start:end]))
        idx += 1
        if end == len(text):
            break
        start = end - overlap
    return chunks


def _blocks(text: str) -> list[str]:
    lines = [l.strip() for l in text.split("\n") if l.strip()]
    if not lines:
        return []
    ordered = sorted(len(l) for l in lines)
    full_width = ordered[int(0.9 * (len(lines) - 1))]
    blocks, cur = [], []
    for line in lines:
        if cur and HEAD.match(line):
            blocks.append(cur)
            cur = []
        cur.append(line)
        is_title_stub = bool(re.match(r"^(?:Appendix\s+[A-D]|Part\s+\d):$", line))   # 'Appendix A:' phải đi cùng thân bài
        if not is_title_stub and len(line) < 0.8 * full_width and SENTENCE_END.search(line):
            blocks.append(cur)
            cur = []
    if cur:
        blocks.append(cur)
    return [" ".join(b) for b in blocks]


def _split_long(text: str, size: int, overlap: int) -> list[str]:
    parts, start = [], 0
    while start < len(text):
        end = min(start + size, len(text))
        if end < len(text):
            cut = text.rfind(" ", start + size // 2, end)
            end = cut if cut != -1 else end
        parts.append(text[start:end].strip())
        if end >= len(text):
            break
        nxt = max(end - overlap, start + 1)
        sp = text.find(" ", nxt, end)            # bắt đầu mảnh sau ở đầu từ, không giữa từ
        start = sp + 1 if sp != -1 else nxt
    return parts


def by_paragraph(page: DocumentPage, max_size: int, split_overlap: int = 50) -> list[Chunk]:
    pieces: list[str] = []
    for block in _blocks(page.text):
        pieces.extend(_split_long(block, max_size, split_overlap) if len(block) > max_size else [block])
    chunks, cur = [], ""
    for piece in pieces:
        if cur and len(cur) + 1 + len(piece) > max_size:
            chunks.append(_make(page, "para", len(chunks), cur))
            cur = piece
        else:
            cur = f"{cur} {piece}".strip()
    if cur:
        chunks.append(_make(page, "para", len(chunks), cur))
    return chunks