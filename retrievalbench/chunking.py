from __future__ import annotations

import re
from typing import Iterable


def chunk_documents(
    documents: Iterable[dict[str, str]],
    chunk_words: int = 120,
    overlap_words: int = 20,
) -> list[dict[str, str | int]]:
    """Split documents into overlapping word-based chunks while preserving source IDs."""
    if chunk_words <= 0:
        raise ValueError("chunk_words must be greater than zero")
    if overlap_words < 0 or overlap_words >= chunk_words:
        raise ValueError("overlap_words must be >= 0 and smaller than chunk_words")

    chunks: list[dict[str, str | int]] = []
    for doc in documents:
        words = re.findall(r"\S+", doc["text"])
        step = chunk_words - overlap_words
        for start in range(0, len(words), step):
            segment = words[start:start + chunk_words]
            if not segment:
                continue
            chunks.append({
                "chunk_id": f'{doc["doc_id"]}::chunk-{len(chunks) + 1}',
                "doc_id": doc["doc_id"],
                "title": doc["title"],
                "source": doc["source"],
                "start_word": start,
                "end_word": start + len(segment),
                "text": " ".join(segment),
            })
            if start + chunk_words >= len(words):
                break
    return chunks
