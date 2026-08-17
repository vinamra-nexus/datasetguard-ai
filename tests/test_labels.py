import pandas as pd
from app.analysis.labels import analyze_labels


def test_label_distribution():
    df = pd.DataFrame({"label": ["A", "A", "B"]})
    result = analyze_labels(df, "label")
    assert result["classes"] == 2
    assert result["distribution"]["A"] == 2
    assert result["minority_class"] == "B"
