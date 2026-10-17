import pytest

from retrievalbench.chunking import chunk_documents
from retrievalbench.retrieval import TfidfRetriever, BM25Retriever


DOCS = [
    {"doc_id": "a", "title": "Python", "source": "a.txt", "text": "Python uses indentation to define code blocks."},
    {"doc_id": "b", "title": "Databases", "source": "b.txt", "text": "SQLite is a lightweight relational database."},
]


def test_chunking_preserves_document_id():
    chunks = chunk_documents(DOCS, chunk_words=5, overlap_words=1)
    assert chunks
    assert all(chunk["doc_id"] in {"a", "b"} for chunk in chunks)


def test_tfidf_finds_relevant_document():
    chunks = chunk_documents(DOCS, chunk_words=50, overlap_words=0)
    results = TfidfRetriever(chunks).search("Python indentation code blocks", top_k=2)
    assert results
    assert results[0]["doc_id"] == "a"


def test_empty_query_returns_no_results():
    chunks = chunk_documents(DOCS, chunk_words=50, overlap_words=0)
    assert TfidfRetriever(chunks).search("   ") == []


def test_invalid_chunk_parameters():
    with pytest.raises(ValueError):
        chunk_documents(DOCS, chunk_words=5, overlap_words=5)


def test_bm25_if_installed():
    pytest.importorskip("rank_bm25")
    chunks = chunk_documents(DOCS, chunk_words=50, overlap_words=0)
    results = BM25Retriever(chunks).search("SQLite database", top_k=2)
    assert results[0]["doc_id"] == "b"
