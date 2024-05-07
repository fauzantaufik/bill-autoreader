import pytest
from datetime import date
from demand import (
    demand_price_unit,
    DemandPriceUnitEnum,
    is_monthly_demand,
    get_demand_structure,
    get_demand_multiplier,
)


def test_demand_price_unit_with_billing_days_price_per_usage():
    assert (
        demand_price_unit(89.38, 0.3081, 27.54, 4)
        == DemandPriceUnitEnum.price_per_usage
    )


def test_demand_price_unit_with_billing_days_price_per_usage_per_day():
    assert (
        demand_price_unit(19, 0.3711, 98.72, 14)
        == DemandPriceUnitEnum.price_per_usage_per_day
    )
    assert (
        demand_price_unit(19, 0.3711, 105.77, 15)
        == DemandPriceUnitEnum.price_per_usage_per_day
    )


def test_demand_price_unit_with_billing_days_price_per_usage_wo_billing_days_varied_loss_factor():
    # Case with exact match when no billing days are provided
    assert (
        demand_price_unit(89.38, 0.3081, 27.54) == DemandPriceUnitEnum.price_per_usage
    )
    # Case with non-exact match due to loss factor adjustment
    assert (
        demand_price_unit(89.38, 0.3081, 27.54 * 0.9, loss_factor=0.9)
        == DemandPriceUnitEnum.price_per_usage
    )


def test_demand_price_unit_price_per_usage_per_day_wo_billing_days_with_varied_loss_factors():
    # Adjusted subtotals for different loss factors, expecting price per usage as no billing days are provided
    assert (
        demand_price_unit(19, 0.3711, 98.72 * 0.95, loss_factor=0.95)
        == DemandPriceUnitEnum.price_per_usage_per_day
    )
    # Adjusted subtotal but with a significant change in loss factor
    assert (
        demand_price_unit(19, 0.3711, 105.77 * 0.8, loss_factor=0.8)
        == DemandPriceUnitEnum.price_per_usage_per_day
    )


# Is Monthly Demand
def test_is_monthly_demand_with_correct_months():
    # Case where the number of demands matches the number of months exactly
    assert (
        is_monthly_demand([100, 200, 300], date(2022, 1, 1), date(2022, 3, 31)) == True
    )


def test_is_monthly_demand_with_incorrect_months():
    # Case where the number of demands does not match the number of months
    assert is_monthly_demand([100, 200], date(2022, 1, 1), date(2022, 3, 31)) == False


def test_is_monthly_demand_without_dates():
    # Case where no dates are provided but there is a demand list
    assert is_monthly_demand([100, 200]) == True


def test_is_monthly_demand_empty_demand():
    # Case where the demand list is empty
    assert is_monthly_demand([], date(2022, 1, 1), date(2022, 2, 28)) == False
    assert is_monthly_demand([100], date(2022, 1, 1), date(2022, 2, 28)) == False


def test_is_monthly_demand_non_list_demand():
    # Case where demand is not a list (should return False regardless of other parameters)
    assert is_monthly_demand(100, date(2022, 1, 1), date(2022, 1, 31)) == False


def test_is_monthly_demand_single_month():
    # Case where there is exactly one month of demand
    assert is_monthly_demand([150], date(2022, 1, 1), date(2022, 1, 31)) == True


def test_is_monthly_demand_partial_month():
    # Check behavior when the end date does not fully include the last month
    assert is_monthly_demand([100, 200], date(2022, 1, 15), date(2022, 2, 14)) == True


sample_demand_data_monthly_per_usage_per_day = [
    {
        "input": {
            "summer_demand": {"usage": [100], "price": [10], "subtotal": [12000]},
            "nonsummer_demand": {
                "usage": [150],
                "price": [15],
                "subtotal": [22500],
            },
            "start_date": date(2024, 3, 20),  # 12 days
            "end_date": date(2024, 4, 10),  # 10 days
        },
        "expected": {
            "monthly_demand": True,  # Adjust based on expected results
            "price_unit": DemandPriceUnitEnum.price_per_usage_per_day,
            "multipliers": {
                "summer": [12],
                "nonsummer": [10],
            },
        },
    },
    {
        "input": {
            "summer_demand": {"usage": 100, "price": 10, "subtotal": 12000},
            "nonsummer_demand": {
                "usage": [150],
                "price": [15],
                "subtotal": [22500],
            },
            "start_date": date(2024, 3, 20),  # 12 days
            "end_date": date(2024, 4, 10),  # 10 days
        },
        "expected": {
            "monthly_demand": True,  # Adjust based on expected results
            "price_unit": DemandPriceUnitEnum.price_per_usage_per_day,
            "multipliers": {
                "summer": [12],
                "nonsummer": [10],
            },
        },
    },
    {
        "input": {
            "summer_demand": {"usage": 100, "price": 10, "subtotal": 12000},
            "nonsummer_demand": {
                "usage": [150, 10],
                "price": [15, 10],
                "subtotal": [22500, 10000],
            },
            "start_date": date(2024, 3, 20),  # 12 days
            "end_date": date(2024, 4, 10),  # 10 days
        },
        "expected": {
            "monthly_demand": False,  # Adjust based on expected results
            "price_unit": DemandPriceUnitEnum.price_per_usage_per_day,
            "multipliers": None,
        },
    },
    {
        "input": {
            "summer_demand": {"usage": None, "price": None, "subtotal": None},
            "nonsummer_demand": {
                "usage": [100, 150],
                "price": [10, 15],
                "subtotal": [12000, 22500],
            },
            "start_date": date(2024, 3, 20),  # 12 days
            "end_date": date(2024, 4, 10),  # 10 days
        },
        "expected": {
            "monthly_demand": True,  # Adjust based on expected results
            "price_unit": DemandPriceUnitEnum.price_per_usage_per_day,
            "multipliers": {
                "summer": [],
                "nonsummer": [12, 10],
            },
        },
    },
    {
        "input": {
            "nonsummer_demand": {"usage": None, "price": None, "subtotal": None},
            "summer_demand": {
                "usage": [100, 150],
                "price": [10, 15],
                "subtotal": [12000, 22500],
            },
            "start_date": date(2024, 3, 20),  # 12 days
            "end_date": date(2024, 4, 10),  # 10 days
        },
        "expected": {
            "monthly_demand": True,  # Adjust based on expected results
            "price_unit": DemandPriceUnitEnum.price_per_usage_per_day,
            "multipliers": {
                "nonsummer": [],
                "summer": [12, 10],
            },
        },
    },
]


@pytest.mark.parametrize("case", sample_demand_data_monthly_per_usage_per_day)
def test_demand_structure_with_multipliers(case):
    """Test to check demand structure calculation including multipliers."""
    params = case["input"]
    expected = case["expected"]
    result = get_demand_structure(**params)

    # Verify that multipliers are calculated as expected
    assert result == expected
