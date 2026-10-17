import pytest

from retrievalbench.evaluation import (
    citation_validity,
    precision_at_k,
    recall_at_k,
    reciprocal_rank,
)


def test_recall_at_k():
    assert recall_at_k(["a", "b", "c"], {"b", "c"}, k=2) == 0.5


def test_precision_at_k():
    assert precision_at_k(["a", "b"], {"b"}, k=2) == 0.5


def test_reciprocal_rank():
    assert reciprocal_rank(["x", "b", "c"], {"b"}) == 0.5


def test_no_relevant_results():
    assert reciprocal_rank(["x", "y"], {"z"}) == 0.0


def test_invalid_k():
    with pytest.raises(ValueError):
        recall_at_k(["a"], {"a"}, k=0)


def test_citation_validity_checks_ids_not_claim_support():
    result = citation_validity(["chunk-1", "missing"], {"chunk-1"})
    assert result["valid_citations"] == 1
    assert result["validity_rate"] == 0.5
