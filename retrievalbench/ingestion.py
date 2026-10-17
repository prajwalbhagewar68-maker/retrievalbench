from __future__ import annotations

from pathlib import Path
from typing import Iterable


def load_text_documents(directory: str | Path) -> list[dict[str, str]]:
    """Load .txt and .md files recursively into {doc_id, title, text, source} records."""
    root = Path(directory)
    if not root.exists():
        raise FileNotFoundError(f"Document directory does not exist: {root}")

    documents: list[dict[str, str]] = []
    for path in sorted(root.rglob("*")):
        if path.is_file() and path.suffix.lower() in {".txt", ".md"}:
            text = path.read_text(encoding="utf-8").strip()
            if not text:
                continue
            documents.append({
                "doc_id": path.relative_to(root).as_posix(),
                "title": path.stem.replace("_", " ").replace("-", " ").title(),
                "text": text,
                "source": str(path),
            })
    return documents


def validate_documents(documents: Iterable[dict[str, str]]) -> list[dict[str, str]]:
    """Validate document records and return a clean copy."""
    cleaned: list[dict[str, str]] = []
    seen: set[str] = set()
    for index, doc in enumerate(documents):
        required = {"doc_id", "title", "text", "source"}
        missing = required.difference(doc)
        if missing:
            raise ValueError(f"Document at index {index} is missing fields: {sorted(missing)}")
        doc_id = str(doc["doc_id"]).strip()
        text = str(doc["text"]).strip()
        if not doc_id or not text:
            raise ValueError(f"Document at index {index} has an empty doc_id or text")
        if doc_id in seen:
            raise ValueError(f"Duplicate doc_id: {doc_id}")
        seen.add(doc_id)
        cleaned.append({
            "doc_id": doc_id,
            "title": str(doc["title"]).strip() or doc_id,
            "text": text,
            "source": str(doc["source"]),
        })
    return cleaned
