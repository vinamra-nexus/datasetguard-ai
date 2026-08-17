from __future__ import annotations

import pandas as pd


def analyze_labels(df: pd.DataFrame, label_column: str) -> dict:
    if label_column not in df.columns:
        raise ValueError(f"Column not found: {label_column}")

    series = df[label_column].dropna()
    counts = series.astype(str).value_counts()

    if counts.empty:
        return {
            "label_column": label_column,
            "classes": 0,
            "distribution": {},
            "imbalance_ratio": 0.0,
            "minority_class": None,
        }

    largest = int(counts.max())
    smallest = int(counts.min())

    return {
        "label_column": label_column,
        "classes": int(len(counts)),
        "distribution": {str(k): int(v) for k, v in counts.items()},
        "imbalance_ratio": round(largest / smallest, 2) if smallest else 0.0,
        "minority_class": str(counts.idxmin()),
    }
