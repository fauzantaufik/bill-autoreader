from utils import calculate_months_between_dates
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
