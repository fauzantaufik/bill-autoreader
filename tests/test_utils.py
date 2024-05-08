from bill_autoreader.utils import calculate_months_between_dates, normalize_string
import pytest
from datetime import date


@pytest.mark.parametrize(
    "case",
    [
        {
            "input": {
                "start_date": date(2024, 3, 20),  # 12 days
                "end_date": date(2024, 4, 10),  # 10 days
            },
            "expected": 2,
        },
        {
            "input": {
                "start_date": date(2024, 3, 20),
                "end_date": date(2024, 3, 29),
            },
            "expected": 1,
        },
    ],
)
def test_calculate_months_between_dates(case):
    params = case["input"]
    assert calculate_months_between_dates(**params) == case["expected"]


# test normalize string


@pytest.mark.parametrize(
    "input_string, expected_output",
    [
        ("Café Émigré", "Cafe Emigre"),  # Tests removal of diacritics
        ("Hello World", "Hello World"),  # Tests strings without diacritics
        ("", ""),  # Tests an empty string
        ("ñandú über", "nandu uber"),  # Tests removal or substitution of diacritics
        ("1234", "1234"),  # Tests numeric characters
        ("@#$%^&*()", "@#$%^&*()"),  # Tests symbols
    ],
)
def test_normalize_string(input_string, expected_output):
    assert (
        normalize_string(input_string) == expected_output
    ), f"Failed on input: {input_string}"
