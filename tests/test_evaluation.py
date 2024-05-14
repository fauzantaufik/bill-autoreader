import pytest
from bill_autoreader.evaluation import (
    match_retailer,
    match_site_identity,
    match_additional_label,
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
    "predicted_tariffs, actual_tariffs, expected",
    [
        (
            ["Off-Peak Usage", "Demand Charge"],
            ["Demand Charge", "Off-Peak Usage"],
            True,
        ),
        (
            ["Green Energy Surcharge", "Metering Service Fee"],
            ["metering service fee", "green energy surcharge"],
            True,
        ),
        (
            ["Feed-in Tariff", "Environmental Recovery"],
            ["Feed-in Tariff", "Demand Charge"],
            False,
        ),
        (
            ["Solar Feed-in Tariff"],
            ["Solar Feed-in Tariff", "Off-Peak Usage", "Environmental Recovery"],
            False,
        ),
        (
            ["Feed-in Tariff", "Demand Charge", "Green Energy Surcharge"],
            ["Green Energy Surcharge", "Feed-in Tariff"],
            False,
        ),
        (
            ["Renewable Energy Fee", "Time-of-Use Rate"],
            ["renewable energy fee", "time-of-use rate"],
            True,
        ),
        (
            ["Service Charge", "Late Payment Fee"],
            ["LATE PAYMENT FEE", "SERVICE CHARGE"],
            True,
        ),
        (
            ["Network Access Charge", "Service Charge"],
            ["NETWORK ACCESS CHARGE", "FIXED CHARGE"],
            False,
        ),
        (["Carbon Offset Charge"], ["carbon_offset_charge"], True),
        (["Fixed Supply Charge"], ["variable supply charge"], False),
    ],
)
def test_match_additional_label(predicted_tariffs, actual_tariffs, expected):
    assert match_additional_label(predicted_tariffs, actual_tariffs) == expected
