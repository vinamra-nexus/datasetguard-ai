import pandas as pd
from app.analysis.pii import scan_pii


def test_email_is_detected():
    df = pd.DataFrame({"text": ["Contact test@example.com"]})
    result = scan_pii(df)
    assert result["finding_count"] == 1
    assert "email" in result["types"]
