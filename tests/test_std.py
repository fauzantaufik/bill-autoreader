import pytest
from bill_autoreader.std import get_regex_patterns, identify_tariffs
from bill_autoreader.std.patterns import TariffPatterns
from bill_autoreader.std.retailer import collect_all_tariffs, RETAILERS_TARIFFS
from bill_autoreader.constants import PEAK, OFF_PEAK, SHOULDER

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
    [PEAK, OFF_PEAK, SHOULDER],
)
def test_identify_tariffs_found(std_tariff):
    """Test identifying tariffs when patterns match."""
    expected = collect_all_tariffs(RETAILERS_TARIFFS, PEAK)
    assert set(identify_tariffs(ALL_TARIFFS, std_tariff)) == set(expected)
