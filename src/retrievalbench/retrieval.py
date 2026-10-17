from __future__ import annotations

import re
from collections.abc import Sequence

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def tokenize(text: str) -> list[str]:
    return re.findall(r"[a-zA-Z0-9_]+", text.lower())


class TfidfRetriever:
    """Simple lexical baseline using TF-IDF vectors and cosine similarity."""

    name = "tfidf"

    def __init__(self, chunks: Sequence[dict]):
        if not chunks:
            raise ValueError("At least one chunk is required")
        self.chunks = list(chunks)
        self.vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
        self.matrix = self.vectorizer.fit_transform([str(c["text"]) for c in self.chunks])

       def search(self, query: str, top_k: int = 5) -> list[dict]:
        if top_k <= 0:
            raise ValueError("top_k must be greater than zero")
        if not query.strip():
            return []

        scores = self.model.get_scores(tokenize(query))
        ranked = sorted(
            enumerate(scores),
            key=lambda pair: (-float(pair[1]), pair[0]),
        )

        return [
            {
                **self.chunks[index],
                "score": float(score),
                "retriever": self.name,
            }
            for index, score in ranked[:top_k]
        ]


class BM25Retriever:
    """BM25 lexical retriever. Requires the rank-bm25 package."""

    name = "bm25"

    def __init__(self, chunks: Sequence[dict]):
        from rank_bm25 import BM25Okapi

        if not chunks:
            raise ValueError("At least one chunk is required")
        self.chunks = list(chunks)
        tokenized = [tokenize(str(c["text"])) for c in self.chunks]
        self.model = BM25Okapi(tokenized)

    def search(self, query: str, top_k: int = 5) -> list[dict]:
        if top_k <= 0:
            raise ValueError("top_k must be greater than zero")
        if not query.strip():
            return []
       scores = self.model.get_scores(tokenize(query))
ranked = sorted(enumerate(scores), key=lambda pair: (-float(pair[1]), pair[0]))
positive = [(index, score) for index, score in ranked if score > 0]

return [
    {**self.chunks[index], "score": float(score), "retriever": self.name}
    for index, score in ranked[:top_k]
]


def available_retrievers(chunks: Sequence[dict]) -> dict[str, object]:
    """Build retrievers that are available in the current environment."""
    retrievers: dict[str, object] = {"TF-IDF": TfidfRetriever(chunks)}
    try:
        retrievers["BM25"] = BM25Retriever(chunks)
    except ImportError:
        pass
    return retrievers
