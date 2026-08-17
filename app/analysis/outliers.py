from __future__ import annotations

import pandas as pd
from sklearn.ensemble import IsolationForest


def detect_outliers(df: pd.DataFrame, contamination: float = 0.05) -> dict:
    numeric = df.select_dtypes(include="number")
    if numeric.empty or len(numeric) < 5:
        return {
            "numeric_columns": numeric.columns.tolist(),
            "outlier_rows": [],
            "outlier_count": 0,
            "outlier_rate": 0.0,
        }

    clean = numeric.fillna(numeric.median(numeric_only=True))
    model = IsolationForest(
        contamination=min(max(contamination, 0.01), 0.49),
        random_state=42,
        n_estimators=100,
    )
    predictions = model.fit_predict(clean)
    indices = [int(i) for i, value in enumerate(predictions) if value == -1]

    return {
        "numeric_columns": numeric.columns.tolist(),
        "outlier_rows": indices,
        "outlier_count": len(indices),
        "outlier_rate": round(len(indices) / len(df), 4),
    }
