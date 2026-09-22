import json
from pathlib import Path

import faiss
from sentence_transformers import SentenceTransformer


PROJECT_ROOT = Path(__file__).resolve().parents[2]

PROCESSED_DIR = (
    PROJECT_ROOT
    / "data"
    / "processed"
)

CHUNKS_PATH = (
    PROCESSED_DIR
    / "chunks_v2.json"
)

INDEX_PATH = (
    PROCESSED_DIR
    / "faiss_v2.index"
)

EMBEDDING_MODEL_NAME = (
    "sentence-transformers/all-MiniLM-L6-v2"
)


class Retriever:

    def __init__(
        self,
        model_name=EMBEDDING_MODEL_NAME,
        device=None,
    ):

        if not CHUNKS_PATH.exists():
            raise FileNotFoundError(
                f"Chunks not found: {CHUNKS_PATH}"
            )

        if not INDEX_PATH.exists():
            raise FileNotFoundError(
                f"FAISS index not found: {INDEX_PATH}"
            )

        with open(
            CHUNKS_PATH,
            "r",
            encoding="utf-8",
        ) as f:
            self.chunks = json.load(f)

        self.index = faiss.read_index(
            str(INDEX_PATH)
        )

        if self.index.ntotal != len(self.chunks):
            raise ValueError(
                "FAISS vector count and chunk count do not match."
            )

        self.model = SentenceTransformer(
            model_name,
            device=device,
        )


    def retrieve(
        self,
        query,
        top_k=5,
    ):

        if not isinstance(query, str):
            raise TypeError(
                "Query must be a string."
            )

        query = query.strip()

        if not query:
            raise ValueError(
                "Query cannot be empty."
            )

        if top_k < 1:
            raise ValueError(
                "top_k must be at least 1."
            )

        query_embedding = self.model.encode(
            [query],
            convert_to_numpy=True,
            normalize_embeddings=True,
        ).astype("float32")

        scores, indices = self.index.search(
            query_embedding,
            top_k,
        )

        results = []

        for rank, (score, index) in enumerate(
            zip(scores[0], indices[0]),
            start=1,
        ):

            if index < 0:
                continue

            chunk = self.chunks[index].copy()

            chunk["rank"] = rank
            chunk["score"] = float(score)

            results.append(chunk)

        return results
