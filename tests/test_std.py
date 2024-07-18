import pytest
from bill_autoreader.std import (
    get_regex_patterns,
    identify_tariffs,
    map_to_standardize_tariffs,
)
from bill_autoreader.std.patterns import TariffPatterns
from bill_autoreader.std.retailer import collect_all_tariffs, RETAILERS_TARIFFS
from bill_autoreader.constants import (
    PEAK,
    OFF_PEAK,
    SHOULDER,
    SUPPLY_CHARGE,
    UNKNOWN_DEMAND,
    UNBUNDLED,
    CONTROLLED_LOAD,
    NONSUMMER_DEMAND,
    METERING_CHARGE,
    SUMMER_DEMAND,
    SOLAR_FIT,
)

ALL_TARIFFS = collect_all_tariffs(RETAILERS_TARIFFS)


def test_get_regex_patterns_valid():
    """Test that valid tariff groups return correct patterns."""
    assert (
        get_regex_patterns("peak") == TariffPatterns.PEAK
    )  # Adjust according to actual implementation


def test_get_regex_patterns_invalid():
    """Test that invalid tariff groups raise an exception."""
    with pytest.raises(Exception):
        get_regex_patterns("invalid_tariff")


@pytest.mark.parametrize(
    "std_tariff",
    [
        PEAK,
        OFF_PEAK,
        SHOULDER,
        SUPPLY_CHARGE,
        UNKNOWN_DEMAND,
        UNBUNDLED,
        NONSUMMER_DEMAND,
        CONTROLLED_LOAD,
        METERING_CHARGE,
        SUMMER_DEMAND,
        SOLAR_FIT,
    ],
)
def test_identify_tariffs_found(std_tariff):
    """Test identifying tariffs when patterns match."""
    expected = collect_all_tariffs(RETAILERS_TARIFFS, [std_tariff])
    assert set(expected) == set(identify_tariffs(ALL_TARIFFS, std_tariff))


class TestStandardizeTariffs:

    def test_standardize_known_tariffs(self):
        # Test with a list of known tariff names
        tariffs = ["Peak Usage", "Off Peak Usage", "Unknown Tariff"]
        expected_result = {
            "Peak Usage": PEAK,  # Assuming 'PEAK' is a standardized name in TYPE_TARIFFS
            "Off Peak Usage": OFF_PEAK,  # Assuming 'OFF_PEAK' is a standardized name
            "Unknown Tariff": None,  # Expecting unrecognized tariffs to be None
        }
        tariff_group = "energy_consumption"  # Example group
        result = map_to_standardize_tariffs(tariffs, tariff_group)
        assert result == expected_result

    def test_standardize_duplicate_tariffs(self):
        # Test with a list of known tariff names
        tariffs = ["First", "Next", "Next", "Supply Charge"]
        expected_result = {
            "First": PEAK,
            "Next": PEAK,
            "Supply Charge": SUPPLY_CHARGE,
        }
        tariff_group = "energy_consumption"  # Example group
        result = map_to_standardize_tariffs(tariffs, tariff_group)
        assert result == expected_result

    def test_standardize_step(self):
        # Test with a list of known tariff names
        tariffs = ["Step1", "Step2", "Step3", "Step4", "Step5", "Supply Charge"]
        expected_result = {
            "Step1": PEAK,
            "Step2": PEAK,
            "Step3": PEAK,
            "Step4": PEAK,
            "Step5": PEAK,
            "Supply Charge": SUPPLY_CHARGE,
        }
        tariff_group = "energy_consumption"  # Example group
        result = map_to_standardize_tariffs(tariffs, tariff_group)
        assert result == expected_result

    def test_empty_tariff_list(self):
        # Test with an empty list
        tariffs = []
        expected_result = {}
        tariff_group = "energy_consumption"
        result = map_to_standardize_tariffs(tariffs, tariff_group)
        assert result == expected_result

    def test_non_existent_group(selfs):
        # Test with a non-existent tariff group
        tariffs = ["Peak Usage", "Off Peak Usage"]
        tariff_group = "non_existent_group"
        with pytest.raises(KeyError):
            map_to_standardize_tariffs(tariffs, tariff_group)
