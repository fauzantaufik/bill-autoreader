import pytest
from bill_autoreader.evaluation import (
    match_retailer,
    match_site_identity,
    match_additional_tariff,
    match_divide_demand,
    match_monthly_demand_multiplier,
    match_read_type,
)


@pytest.mark.parametrize(
    "autoreader_value, actual_value, expected",
    [
        # Test exact matches
        ("Energy Australia", "Energy Australia", True),
        ("AGL Energy", "AGL Energy", True),
        ("agl sales pty limited", "AGL Energy", True),
        # Test variations in case and punctuation
        ("energyaustralia", "Energy Australia", True),
        ("agl energy", "AGL Energy", True),
        # Test with common suffixes removed
        ("Energy Australia Pty Ltd", "Energy Australia", True),
        ("AGL Energy Limited", "AGL Energy", True),
        # Special matching logic cases
        (
            "Win Energy",
            "Win Energy",
            True,
        ),
        (
            "Win Connect",
            "Win Energy",
            True,
        ),
        ("winconnect", "Win Energy", True),
        # Test to ensure unrelated names do not match
        ("Mojo Power", "AGL Energy", False),
        ("Elgas", "Energy Australia", False),
        # Test variations of a retailer with spaces, punctuation, and suffixes
        ("Elysian Energy", "ElysianEnergy", True),
        ("Dodo Power & Gas", "Dodo Power and Gas", True),
        ("Dodo Power & Gas Pty Ltd", "Dodo Power and Gas", True),
        # Test for a retailer not in the list, expecting False
        ("Nonexistent Energy Co", "Energy Australia", False),
        # Test for Sumo
        ("sumo power", "Sumo Energy", True),
        # Test for Momentum
        ("momentum energy", "Momentum Energy", True),
        ("lumo energy (sa)", "Lumo Energy", True),
        ("vicinity real estate licence", "Vicinity Centres", True),
    ],
)
def test_match_retailer(autoreader_value, actual_value, expected):
    assert match_retailer(autoreader_value, actual_value) == expected


def test_exact_match():
    assert match_site_identity("1234567890", "1234567890") == True


def test_partial_match():
    assert match_site_identity("1234567890", "12345678901") == True


def test_numeric_match():
    assert match_site_identity(1234567890, 1234567890) == True


def test_numeric_partial_match():
    assert match_site_identity(1234567890, 12345678901) == True
    assert match_site_identity(12345678901, 1234567890) == True


def test_no_match():
    assert match_site_identity("1234567890", "abcdefghij") == False


def test_numeric_no_match():
    assert match_site_identity(1234567890, 9876543210) == False


def test_mixed_type_match():
    assert match_site_identity(1234567890, "1234567890") == True


def test_mixed_type_no_match():
    assert match_site_identity(1234567890, "abcdefghij") == False


@pytest.mark.parametrize(
    "predicted_labels, predicted_prices, actual_labels, actual_prices, expected",
    [
        (["Off-Peak Usage"], [0.12], ["off_peak_usage"], [0.12], True),
        (
            ["Green Energy Surcharge", "Metering Service Fee"],
            [0.05, 1.00],
            ["metering service fee", "green energy surcharge"],
            [1.00, 0.05],
            True,
        ),
        (["Feed-in Tariff"], [0.08], ["feed_in tariff"], [0.07], False),
        (
            ["Solar Feed-in Tariff"],
            [0.10],
            ["Solar Feed-in Tariff", "Off-Peak Usage"],
            [0.10, 0.12],
            False,
        ),
        (
            ["Renewable Energy Fee", "Time-of-Use Rate"],
            [0.02, 0.15],
            ["renewable energy fee", "time_of_use rate"],
            [0.02, 0.15],
            True,
        ),
        (
            ["Service Charge", "Late Payment Fee"],
            [10.00, 5.00],
            ["LATE PAYMENT FEE", "SERVICE CHARGE"],
            [5.00, 10.00],
            True,
        ),
        (["Network Access Charge"], [3.50], ["network_access_charge"], [3.50], True),
        (["Carbon Offset Charge"], [0.03], ["carbon offset charge"], [0.03], True),
        (["Fixed Supply Charge"], [20.00], ["variable supply charge"], [20.00], False),
        (
            ["Service Charge", "Late Payment Fee"],
            [10.00, 5.00],
            ["LATE PAYMENT FEE", None],
            [5.00, 10.00],
            False,
        ),
    ],
)
def test_match_additional_price_label(
    predicted_labels, predicted_prices, actual_labels, actual_prices, expected
):
    assert (
        match_additional_tariff(
            predicted_labels, predicted_prices, actual_labels, actual_prices
        )
        == expected
    )


@pytest.mark.parametrize(
    "predicted_value, actual_value, expected",
    [
        (True, True, True),
        (False, False, True),
        ("true", "true", True),
        ("false", "false", True),
        ("yes", "true", True),
        ("no", "false", True),
        ("1", "1", True),
        ("0", "0", True),
        (1, 1, True),
        (0, 0, True),
        (1.0, 1.0, True),
        (0.0, 0.0, True),
        ("true", True, True),
        ("false", False, True),
        ("yes", True, True),
        ("no", False, True),
        ("1", True, True),
        ("0", False, True),
        (1, True, True),
        (0, False, True),
        (1.0, True, True),
        (0.0, False, True),
        ("true", "yes", True),
        ("false", "no", True),
        ("yes", "1", True),
        ("no", "0", True),
        ("yes", "true", True),
        ("no", "false", True),
        ("YES", "true", True),
        ("NO", "false", True),
        (" True ", "true", True),
        (" False ", "false", True),
        (True, "false", False),
        (False, "true", False),
        ("yes", "no", False),
        ("1", "0", False),
        (1, 0, False),
        (1.0, 0.0, False),
        ("invalid", "true", False),
        ("true", "invalid", False),
        (None, True, False),
        (True, None, False),
    ],
)
def test_match_divide_demand(predicted_value, actual_value, expected):
    assert match_divide_demand(predicted_value, actual_value) == expected


@pytest.mark.parametrize(
    "predicted_price, actual_price, expected",
    [
        (None, None, True),
        (None, [], True),
        ([], None, True),
        ([], [], True),
        ([None, None], [[], []], True),
        ([1, 2, 3], [1, 2, 3], True),
        ([1, 2, 3], [3, 2, 1], False),
        ([None, [1, 2]], [[], [1, 2]], True),
        ([[1, 2], [3, 4]], [[1, 2], [3, 4]], True),
        ([[1, 2], [3, 4]], [[3, 4], [1, 2]], False),
        ([[1, 2], None], [[1, 2], []], True),
        ([[1, 2]], [[1, 2]], True),
        ([[1, 2]], [[2, 1]], False),
        ([[1, 2], [3, 4]], [[1, 2], [4, 3]], False),
        ([1, [2, 3]], [1, [2, 3]], True),
        ([1, [2, 3]], [1, [3, 2]], False),
    ],
)
def test_match_monthly_demand_multiplier(predicted_price, actual_price, expected):
    assert match_monthly_demand_multiplier(predicted_price, actual_price) == expected


@pytest.mark.parametrize(
    "predicted_value, actual_value, expected",
    [
        ("estimated", "estimated", True),
        ("Estimated", "estimated", True),
        ("ESTIMATED", "estimated", True),
        ("unknown", None, True),
        (None, "unknown", True),
        ("estimated", "actual", False),
        ("substituted", "unknown", False),
        (None, "actual", False),
    ],
)
def test_match_read_type(predicted_value, actual_value, expected):
    assert match_read_type(predicted_value, actual_value) == expected
