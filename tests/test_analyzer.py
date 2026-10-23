
from analyzer import analyze_password


def test_empty_password():
    result = analyze_password("")

    assert result["length"] == 0
    assert result["rating"] == "No password entered"


def test_short_password_is_flagged():
    result = analyze_password("abc")

    assert any(
        "short" in finding.lower()
        for finding in result["findings"]
    )


def test_repeated_characters_are_detected():
    result = analyze_password("aaaBBB111!!!")

    assert any(
        "repeated" in finding.lower()
        for finding in result["findings"]
    )


def test_sequence_is_detected():
    result = analyze_password("abcd1234")

    assert any(
        "sequence" in finding.lower()
        for finding in result["findings"]
    )


def test_result_has_required_fields():
    result = analyze_password("River-Candle-Maple-Orbit-47")

    assert "score" in result
    assert "rating" in result
    assert "findings" in result
    assert "recommendations" in result
    assert 0 <= result["score"] <= 4


def test_common_password_is_detected():
    result = analyze_password("password123")

    assert any(
        "common password" in finding.lower()
        for finding in result["findings"]
    )


def test_common_password_with_simple_substitution_is_detected():
    result = analyze_password("P@ssw0rd")

    assert any(
        "common password" in finding.lower()
        for finding in result["findings"]
    )


def test_predictable_year_is_detected():
    result = analyze_password("River-Candle-1999-Maple")

    assert any(
        "year" in finding.lower()
        for finding in result["findings"]
    )


def test_spaces_are_detected_as_character_type():
    result = analyze_password("river candle maple orbit")

    assert result["character_types"]["spaces"] is True


def test_very_long_input_is_handled():
    result = analyze_password("a" * 4097)

    assert result["rating"] == "Input too long to analyze"
    assert result["guessability"] is None


def test_non_string_input_raises_type_error():
    import pytest

    with pytest.raises(TypeError):
        analyze_password(None)


def test_score_and_rating_are_consistent():
    result = analyze_password("River-Candle-Maple-Orbit-47")

    expected_ratings = {
        0: "Very weak",
        1: "Weak",
        2: "Moderate",
        3: "Strong",
        4: "Very strong",
    }

    assert result["rating"] == expected_ratings[result["score"]]
