from __future__ import annotations

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def find_exact_duplicates(df: pd.DataFrame) -> dict:
    duplicate_mask = df.duplicated(keep=False)
    duplicate_rows = int(df.duplicated().sum())
    return {
        "duplicate_rows": duplicate_rows,
        "duplicate_rate": round(duplicate_rows / len(df), 4) if len(df) else 0.0,
        "duplicate_mask": duplicate_mask.tolist(),
    }


def find_text_duplicates(
    df: pd.DataFrame, text_column: str, threshold: float = 0.90
) -> list[dict]:
    if text_column not in df.columns:
        raise ValueError(f"Column not found: {text_column}")

    texts = df[text_column].fillna("").astype(str).tolist()
    if len(texts) < 2 or not any(texts):
        return []

    matrix = TfidfVectorizer(stop_words="english").fit_transform(texts)
    similarities = cosine_similarity(matrix)

    matches = []
    for i in range(len(texts)):
        for j in range(i + 1, len(texts)):
            score = float(similarities[i, j])
            if score >= threshold:
                matches.append({
                    "row_a": i,
                    "row_b": j,
                    "similarity": round(score, 4),
                })
    return matches
