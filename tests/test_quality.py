from app.analysis.quality import calculate_quality_score


def test_clean_dataset_has_high_score():
    result = calculate_quality_score(0.0, 0.0, 0.0, 0, 100)
    assert result["score"] == 100.0
    assert result["grade"] == "A"


def test_quality_score_is_bounded():
    result = calculate_quality_score(1.0, 1.0, 1.0, 100, 1)
    assert 0 <= result["score"] <= 100
