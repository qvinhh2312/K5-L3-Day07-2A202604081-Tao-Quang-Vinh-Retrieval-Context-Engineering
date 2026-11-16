import os
import re
from pathlib import Path

from dotenv import load_dotenv

from day6_src.embeddings import SentenceTransformerEmbedder
from day6_src.store import PgVectorStore


def normalize(text: str) -> str:
    return re.sub(r" (?=[,.;:])", "", text)


class Dense:
    name = "dense"

    def __init__(self, index: str = "B") -> None:
        load_dotenv(Path(__file__).resolve().parents[1] / ".env")
        url = os.getenv("DATABASE_URL")
        if not url:
            raise RuntimeError("DATABASE_URL is missing in the repository .env")
        self.embedder = SentenceTransformerEmbedder("sentence-transformers/all-MiniLM-L6-v2")
        self.store = PgVectorStore(url, self.embedder.dimensions)
        self.index = index

    def search(self, query: str, top_k: int = 3, filters: dict | None = None) -> list[dict]:
        rows = self.store.search(self.index, self.embedder.embed_query(query), top_k=top_k, filters=filters)
        return [{"id": r["chunk_id"], "source_id": r["document_id"], "source": r["source"],
                 "page": r["page"], "text": normalize(r["text"]),
                 "metadata": {"part": r["part"], "printed_page": r["printed_page"],
                              "chunk_index": r["chunk_index"]},
                 "score": float(r["score"]), "rank": i + 1, "strategy": self.name}
                for i, r in enumerate(rows)]
