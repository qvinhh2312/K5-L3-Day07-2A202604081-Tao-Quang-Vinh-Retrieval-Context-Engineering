from typing import Protocol


class Embedder(Protocol):
    model_name: str
    dimensions: int

    def embed_documents(self, texts: list[str]) -> list[list[float]]: ...
    def embed_query(self, question: str) -> list[float]: ...


class SentenceTransformerEmbedder:
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2",
                 batch_size: int = 32) -> None:
        try:
            import sentence_transformers
            from sentence_transformers import SentenceTransformer
        except ImportError as exc:
            raise RuntimeError("Chưa cài sentence-transformers: pip install sentence-transformers") from exc
        self.model_name = model_name
        self.batch_size = batch_size
        self.library_version = sentence_transformers.__version__
        self._model = SentenceTransformer(model_name)
        # sentence-transformers renamed this method; prefer the new API while
        # retaining compatibility with older installed versions.
        get_dimension = (getattr(self._model, "get_embedding_dimension", None)
                         or self._model.get_sentence_embedding_dimension)
        self.dimensions = int(get_dimension())
        self.max_seq_length = int(self._model.max_seq_length)

    def _encode(self, texts: list[str]) -> list[list[float]]:
        vecs = self._model.encode(texts, batch_size=self.batch_size,
                                  normalize_embeddings=True, convert_to_numpy=True,
                                  show_progress_bar=False)
        return vecs.tolist()

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return self._encode(texts)

    def embed_query(self, question: str) -> list[float]:
        return self._encode([question])[0]
