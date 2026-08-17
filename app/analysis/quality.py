from __future__ import annotations


def calculate_quality_score(
    missing_rate: float,
    duplicate_rate: float,
    outlier_rate: float,
    pii_findings: int,
    rows: int,
) -> dict:
    # Explainable 0-100 score; penalties are intentionally bounded.
    score = 100.0
    reasons = []

    score -= min(30.0, missing_rate * 100)
    score -= min(25.0, duplicate_rate * 100)
    score -= min(15.0, outlier_rate * 100)
    score -= min(20.0, pii_findings * 2.0)

    if missing_rate > 0.10:
        reasons.append("High missing-value rate")
    if duplicate_rate > 0.05:
        reasons.append("Many duplicate rows")
    if outlier_rate > 0.10:
        reasons.append("High outlier rate")
    if pii_findings:
        reasons.append("Potential PII detected")
    if rows < 50:
        reasons.append("Small dataset; quality conclusions may be less reliable")

    score = round(max(0.0, min(100.0, score)), 1)
    grade = "A" if score >= 80 else "B" if score >= 60 else "C" if score >= 40 else "D"

    return {"score": score, "grade": grade, "reasons": reasons}
