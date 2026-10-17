from __future__ import annotations

import json
import time
from pathlib import Path

import pandas as pd

from .evaluation import evaluate_query


def load_questions(path: str | Path) -> list[dict]:
    with Path(path).open(encoding="utf-8") as file:
        questions = json.load(file)
    if not isinstance(questions, list):
        raise ValueError("Question file must contain a JSON list")
    for i, item in enumerate(questions):
        if not item.get("question") or not isinstance(item.get("relevant_doc_ids"), list):
            raise ValueError(f"Invalid question record at index {i}")
    return questions


def run_benchmark(retrievers: dict, questions: list[dict], k: int = 5) -> pd.DataFrame:
    rows: list[dict] = []
    for question in questions:
        for name, retriever in retrievers.items():
            started = time.perf_counter()
            results = retriever.search(question["question"], top_k=k)
            elapsed_ms = (time.perf_counter() - started) * 1000
            metrics = evaluate_query(results, set(question["relevant_doc_ids"]), k=k)
            rows.append({
                "question_id": question.get("question_id", ""),
                "question": question["question"],
                "retriever": name,
                "latency_ms": round(elapsed_ms, 3),
                "retrieved_doc_ids": [result["doc_id"] for result in results],
                **metrics,
            })
    return pd.DataFrame(rows)


def summarize_benchmark(results: pd.DataFrame) -> pd.DataFrame:
    metric_columns = [col for col in results.columns if col.startswith(("recall@", "precision@"))]
    metric_columns += ["mrr", "latency_ms"]
    return results.groupby("retriever", as_index=False)[metric_columns].mean().round(4)
