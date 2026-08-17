import pandas as pd
from app.analysis.outliers import detect_outliers


def test_outlier_detector_returns_expected_schema():
    df = pd.DataFrame({"value": list(range(30))})
    result = detect_outliers(df)
    assert "outlier_count" in result
    assert "outlier_rows" in result
    assert result["numeric_columns"] == ["value"]
