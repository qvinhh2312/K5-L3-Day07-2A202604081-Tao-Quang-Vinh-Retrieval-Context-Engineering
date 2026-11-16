from typing import Any

import psycopg
from psycopg.types.json import Jsonb

from .models import Chunk

TABLE = "lab_chunks"
ALLOWED_FILTERS = {"part", "document_id"}


def _vec(v: list[float]) -> str:
    return "[" + ",".join(f"{x:.8f}" for x in v) + "]"


class PgVectorStore:
    def __init__(self, database_url: str, dimensions: int) -> None:
        self.url = database_url
        self.dim = int(dimensions)

    def _conn(self) -> psycopg.Connection:
        return psycopg.connect(self.url, connect_timeout=5)

    def create_schema(self) -> None:
        with self._conn() as conn:
            conn.execute(f"""
                CREATE TABLE IF NOT EXISTS {TABLE} (
                    strategy      text NOT NULL,
                    chunk_id      text NOT NULL,
                    document_id   text NOT NULL,
                    source        text NOT NULL,
                    page          int  NOT NULL,
                    printed_page  text,
                    part          text,
                    chunk_index   int  NOT NULL,
                    text          text NOT NULL,
                    char_count    int  NOT NULL,
                    metadata      jsonb NOT NULL,
                    embedding     vector({self.dim}) NOT NULL,
                    PRIMARY KEY (strategy, chunk_id)
                )""")
            conn.execute(f"CREATE INDEX IF NOT EXISTS {TABLE}_part_idx ON {TABLE} (strategy, part)")
            row = conn.execute(
                "SELECT atttypmod FROM pg_attribute WHERE attrelid = %s::regclass AND attname = 'embedding'",
                (TABLE,)).fetchone()
            if row and row[0] != self.dim:
                raise RuntimeError(
                    f"Bảng {TABLE} có vector({row[0]}) nhưng model cho {self.dim} chiều; "
                    "dùng bảng khác hoặc xóa bảng thử nghiệm.")

    def upsert(self, strategy: str, chunks: list[Chunk], vectors: list[list[float]]) -> None:
        if len(chunks) != len(vectors):
            raise ValueError("số chunk và số vector khác nhau")
        for v in vectors:
            if len(v) != self.dim:
                raise ValueError(f"vector {len(v)} chiều, cần {self.dim}")
        rows = [(strategy, c.chunk_id, c.document_id, c.source, c.page,
                 c.metadata.get("printed_page"), c.metadata.get("part"),
                 int(c.metadata.get("chunk_index", 0)), c.text, len(c.text),
                 Jsonb(c.metadata), _vec(v)) for c, v in zip(chunks, vectors)]
        with self._conn() as conn, conn.cursor() as cur:   # một transaction
            cur.executemany(f"""
                INSERT INTO {TABLE} (strategy, chunk_id, document_id, source, page, printed_page,
                    part, chunk_index, text, char_count, metadata, embedding)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s::vector)
                ON CONFLICT (strategy, chunk_id) DO UPDATE SET
                    text = EXCLUDED.text, char_count = EXCLUDED.char_count,
                    metadata = EXCLUDED.metadata, embedding = EXCLUDED.embedding,
                    page = EXCLUDED.page, printed_page = EXCLUDED.printed_page,
                    part = EXCLUDED.part, chunk_index = EXCLUDED.chunk_index""", rows)
            # xóa chunk cũ không còn trong lần nạp này (tài liệu đổi / đổi tham số chunk)
            cur.execute(f"""DELETE FROM {TABLE}
                WHERE strategy = %s AND document_id = ANY(%s) AND chunk_id <> ALL(%s)""",
                        (strategy, list({c.document_id for c in chunks}), [c.chunk_id for c in chunks]))

    def count(self, strategy: str | None = None) -> int:
        with self._conn() as conn:
            if strategy is None:
                return conn.execute(f"SELECT count(*) FROM {TABLE}").fetchone()[0]
            return conn.execute(f"SELECT count(*) FROM {TABLE} WHERE strategy = %s", (strategy,)).fetchone()[0]

    def versions(self) -> dict[str, str]:
        with self._conn() as conn:
            pg = conn.execute("SELECT current_setting('server_version')").fetchone()[0]
            vec = conn.execute("SELECT extversion FROM pg_extension WHERE extname = 'vector'").fetchone()[0]
        return {"postgresql": pg, "pgvector": vec, "psycopg": psycopg.__version__}

    def search(self, strategy: str, query_vector: list[float], top_k: int = 3,
               filters: dict[str, Any] | None = None) -> list[dict[str, Any]]:
        where, params = ["strategy = %s"], [strategy]
        for key, value in (filters or {}).items():
            if key not in ALLOWED_FILTERS:
                raise ValueError(f"filter không được phép: {key}")
            where.append(f"{key} = %s")          # tên cột lấy từ whitelist, giá trị được tham số hóa
            params.append(value)
        qv = _vec(query_vector)
        sql = f"""SELECT chunk_id, document_id, source, page, printed_page, part, chunk_index, text,
                         1 - (embedding <=> %s::vector) AS score
                  FROM {TABLE} WHERE {' AND '.join(where)}
                  ORDER BY embedding <=> %s::vector LIMIT %s"""
        with self._conn() as conn:
            rows = conn.execute(sql, [qv, *params, qv, top_k]).fetchall()
        cols = ["chunk_id", "document_id", "source", "page", "printed_page", "part",
                "chunk_index", "text", "score"]
        return [dict(zip(cols, r)) for r in rows]