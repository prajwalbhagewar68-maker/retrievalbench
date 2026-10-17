# RetrievalBench

**A reproducible laboratory for evaluating information retrieval methods.**

## Overview
RetrievalBench compares TF-IDF, BM25, and semantic retrieval on a small, manually authored document corpus. It evaluates retrieval quality and latency and provides an interactive interface for testing queries.

## Methods
- TF-IDF
- BM25
- Semantic retrieval

## Evaluation metrics
- Recall@3
- Precision@3
- Mean Reciprocal Rank (MRR)
- Retrieval latency

## Current experimental findings
In the current 30-question benchmark, semantic retrieval achieved a mean Recall@3 of 1.00 and MRR of 0.9833. BM25 achieved mean Recall@3 of 0.80 and MRR of 0.80, with lower measured latency in the reported experiments.

These are results from this specific benchmark, not general claims about the methods.

## Limitations
The dataset is small and manually authored. Results depend on the corpus, relevance labels, runtime environment, and implementation.

## Future improvements
- Expand the document corpus and relevance-labelled questions.
- Investigate failed retrieval queries.
- Improve evaluation reproducibility.
- Add more retrievers and configurable chunking.
- Add automated tests and continuous integration.

## Technologies
Python, pandas, scikit-learn, BM25, Streamlit, and pytest.
