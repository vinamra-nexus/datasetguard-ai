import pandas as pd
from app.analysis.profiling import profile_dataset


def test_profile_counts_rows_columns_and_missing():
    df = pd.DataFrame({"text": ["a", None], "label": [1, 1]})
    result = profile_dataset(df)
    assert result["rows"] == 2
    assert result["columns"] == 2
    assert result["missing_cells"] == 1
