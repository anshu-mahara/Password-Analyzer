
import re
import string
from zxcvbn import zxcvbn


# --------------------------------------------------
# Configuration
# --------------------------------------------------

COMMON_PASSWORDS = {
    "password",
    "password123",
    "123456",
    "12345678",
    "123456789",
    "qwerty",
    "qwerty123",
    "admin",
    "admin123",
    "letmein",
    "welcome",
    "iloveyou",
    "abc123",
    "111111",
    "000000",
    "passw0rd",
    "changeme",
    "dragon",
    "monkey",
    "football",
    "sunshine",
    "princess",
    "login",
    "master",
    "secret",
}

# Predictable character substitutions sometimes used
# instead of ordinary letters.
LEET_TRANSLATION = str.maketrans({
    "0": "o",
    "1": "i",
    "3": "e",
    "4": "a",
    "5": "s",
    "7": "t",
    "@": "a",
    "$": "s",
})


# --------------------------------------------------
# Helper functions
# --------------------------------------------------

def normalize_password(password):
    """Normalize common character substitutions for checks."""
    return password.lower().translate(LEET_TRANSLATION)


def detect_character_types(password):
    """Identify the character types present."""
    return {
        "lowercase": any(c in string.ascii_lowercase for c in password),
        "uppercase": any(c in string.ascii_uppercase for c in password),
        "digits": any(c.isdigit() for c in password),
        "symbols": any(
            not c.isalnum() and not c.isspace()
            for c in password
        ),
        "spaces": any(c.isspace() for c in password),
    }


def detect_repetition(password):
    """Detect excessive repeated characters."""
    return bool(re.search(r"(.)\1{2,}", password))


def detect_sequences(password):
    """Detect common ascending or descending sequences."""
    normalized = password.lower()

    known_patterns = (
        "0123456789",
        "9876543210",
        "abcdefghijklmnopqrstuvwxyz",
        "zyxwvutsrqponmlkjihgfedcba",
        "qwertyuiop",
        "poiuytrewq",
        "asdfghjkl",
        "lkjhgfdsa",
        "zxcvbnm",
        "mnbvcxz",
    )

    for pattern in known_patterns:
        for length in (4, 5, 6):
            for start in range(len(pattern) - length + 1):
                sequence = pattern[start:start + length]
                if sequence in normalized:
                    return True

    return False



def detect_common_password(password):
    """Check for common passwords and simple character substitutions."""

    # First, check the exact password.
    if password.lower() in COMMON_PASSWORDS:
        return True

    # Then compare normalized versions to detect simple substitutions.
    normalized = normalize_password(password)

    for common_password in COMMON_PASSWORDS:
        if normalize_password(common_password) == normalized:
            return True

    return False


def detect_predictable_year(password):
    """Detect standalone years in a common modern range."""
    return bool(
        re.search(r"(?<!\d)(19\d{2}|20\d{2})(?!\d)", password)
    )


def detect_keyboard_pattern(password):
    """Detect several common keyboard sequences."""
    normalized = password.lower()

    patterns = (
        "qwerty",
        "asdf",
        "zxcv",
        "qazwsx",
        "1qaz",
        "zaq1",
    )

    return any(pattern in normalized for pattern in patterns)


# --------------------------------------------------
# Main analysis function
# --------------------------------------------------

def analyze_password(password):
    """
    Analyze a password and return structured results.

    Returns:
        dict containing:
        - score: integer from 0 to 4
        - rating: human-readable strength rating
        - findings: list of potential weaknesses
        - recommendations: list of improvement tips
        - character_types: detected character types
        - length: password length
        - guessability: zxcvbn's estimated crack-time category
        - feedback: additional zxcvbn feedback

    This is a heuristic assessment, not a guarantee of security.
    """

    if not isinstance(password, str):
        raise TypeError("Password must be a string.")

    if not password:
        return {
            "score": 0,
            "rating": "No password entered",
            "findings": [],
            "recommendations": [
                "Enter a sample password to begin analysis."
            ],
            "character_types": detect_character_types(""),
            "length": 0,
            "guessability": None,
            "feedback": [],
        }

    findings = []
    recommendations = []

    # Character features
    length = len(password)
    character_types = detect_character_types(password)

    # Do not run a dictionary-based guessability estimator
    # on arbitrarily large input.
    if length > 4096:
        return {
            "score": 0,
            "rating": "Input too long to analyze",
            "findings": [
                "The input exceeds the analyzer's supported length."
            ],
            "recommendations": [
                "Enter a shorter sample for this prototype."
            ],
            "character_types": character_types,
            "length": length,
            "guessability": None,
            "feedback": [],
        }

    # Run the guessability estimator.
    zxcvbn_result = zxcvbn(password)

    # 1. Length assessment
    if length < 8:
        findings.append("Very short password.")
        recommendations.append(
            "Use a longer password. Short passwords are generally "
            "easier to guess."
        )
    elif length < 15:
        findings.append("Password is shorter than 15 characters.")
        recommendations.append(
            "Consider a longer password or passphrase, especially "
            "when the service does not require multifactor "
            "authentication."
        )

    # 2. Common-password check
    is_common = detect_common_password(password)

    if is_common:
        findings.append(
            "Password matches a common password or simple substitution."
        )
        recommendations.append(
            "Replace it with a unique password that is not commonly used."
        )

    # 3. Repeated characters
    has_repetition = detect_repetition(password)

    if has_repetition:
        findings.append("Contains three or more consecutive repeated characters.")
        recommendations.append(
            "Avoid predictable repetition, such as repeated letters or digits."
        )

    # 4. Sequential patterns
    has_sequence = detect_sequences(password)

    if has_sequence:
        findings.append("Contains a predictable alphabetical, numeric, or keyboard sequence.")
        recommendations.append(
            "Avoid recognizable sequences and keyboard patterns."
        )

    # 5. Keyboard patterns
    has_keyboard_pattern = detect_keyboard_pattern(password)

    if has_keyboard_pattern and not has_sequence:
        findings.append("Contains a common keyboard pattern.")
        recommendations.append(
            "Avoid familiar keyboard walks and patterns."
        )

    # 6. Predictable year
    has_year = detect_predictable_year(password)

    if has_year:
        findings.append("Contains a recognizable four-digit year.")
        recommendations.append(
            "Avoid predictable dates or years, particularly when "
            "they relate to you personally."
        )

    # 7. Character variety (informational, not a mandatory requirement)
    variety_count = sum(
        character_types[key]
        for key in ("lowercase", "uppercase", "digits", "symbols")
    )

    if variety_count == 1 and length < 15:
        findings.append(
            "Uses only one basic character type and is relatively short."
        )
        recommendations.append(
            "Consider using a longer, less predictable password or "
            "passphrase."
        )

    # 8. Use zxcvbn's score as the baseline.
    score = zxcvbn_result["score"]

    # A known common password should not receive a high rating.
    if is_common:
        score = min(score, 1)

    # Avoid presenting an obvious weakness as a very strong result.
    if has_sequence or has_repetition or has_keyboard_pattern:
        score = min(score, 3)

    ratings = {
        0: "Very weak",
        1: "Weak",
        2: "Moderate",
        3: "Strong",
        4: "Very strong",
    }

    # 9. Provide general recommendations if no custom tips were generated.
    if not recommendations:
        recommendations.append(
            "Use a unique password for every account and consider "
            "storing it in a reputable password manager."
        )

    # Avoid duplicate messages while preserving order.
    findings = list(dict.fromkeys(findings))
    recommendations = list(dict.fromkeys(recommendations))

    # Return structured data for the Streamlit interface.
    return {
        "score": score,
        "rating": ratings[score],
        "findings": findings,
        "recommendations": recommendations,
        "character_types": character_types,
        "length": length,
        "guessability": zxcvbn_result.get("crack_times_display", {}),
        "feedback": zxcvbn_result.get("feedback", {}),
    }


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
