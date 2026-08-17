from __future__ import annotations

import re
import pandas as pd

PATTERNS = {
    "email": re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.I),
    "phone": re.compile(r"\b(?:\+?\d[\d\s().-]{8,}\d)\b"),
}


def scan_pii(df: pd.DataFrame) -> dict:
    findings = []
    text_columns = df.select_dtypes(include=["object", "string"]).columns

    for column in text_columns:
        for row_index, value in df[column].items():
            if pd.isna(value):
                continue
            text = str(value)
            for kind, pattern in PATTERNS.items():
                if pattern.search(text):
                    findings.append({
                        "row": int(row_index),
                        "column": str(column),
                        "type": kind,
                    })

    return {
        "findings": findings,
        "finding_count": len(findings),
        "types": sorted({item["type"] for item in findings}),
    }
