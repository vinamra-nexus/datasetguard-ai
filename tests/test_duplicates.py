import pandas as pd
from app.analysis.duplicates import find_exact_duplicates, find_text_duplicates


def test_exact_duplicates_are_detected():
    df = pd.DataFrame({"text": ["hello", "hello", "world"]})
    result = find_exact_duplicates(df)
    assert result["duplicate_rows"] == 1


def test_similar_text_rows_are_detected():
    df = pd.DataFrame({"text": ["good product", "good product", "different"]})
    result = find_text_duplicates(df, "text", threshold=0.80)
    assert any(item["row_a"] == 0 and item["row_b"] == 1 for item in result)
