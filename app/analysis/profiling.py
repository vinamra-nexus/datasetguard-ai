from __future__ import annotations

import pandas as pd


def profile_dataset(df: pd.DataFrame) -> dict:
    # Return deterministic structural and missing-value statistics.
    rows, columns = df.shape
    missing = int(df.isna().sum().sum())
    total_cells = rows * columns

    numeric_columns = df.select_dtypes(include="number").columns.tolist()
    text_columns = df.select_dtypes(include=["object", "string"]).columns.tolist()

    column_details = []
    for column in df.columns:
        series = df[column]
        column_details.append({
            "name": str(column),
            "dtype": str(series.dtype),
            "missing": int(series.isna().sum()),
            "unique": int(series.nunique(dropna=True)),
        })

    return {
        "rows": int(rows),
        "columns": int(columns),
        "total_cells": int(total_cells),
        "missing_cells": missing,
        "missing_rate": round(missing / total_cells, 4) if total_cells else 0.0,
        "numeric_columns": numeric_columns,
        "text_columns": text_columns,
        "column_details": column_details,
    }
