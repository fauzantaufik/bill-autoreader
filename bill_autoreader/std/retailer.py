from typing import List, Dict
from bill_autoreader.constants import (
    PEAK,
    OFF_PEAK,
    SHOULDER,
    UNKNOWN_DEMAND,
    SUPPLY_CHARGE,
    NONSUMMER_DEMAND,
)


UNSTANDARDIZED_TARIFFS = {
    "ORIGIN": [
        "AEMO Participant Charge",
        "AEMO Ancillary Charge",
        "AEMO FRC Operations",
        "PRC Charge",
    ]
}

# Compiled how retailer label tariff
TANGO_TARIFFS = {"Peak": PEAK, "Shoulder": "Shoulder", "Off Peak": "Supply Charge"}
COVAU_TARIFFS = {
    "Peak Usage": PEAK,
    "Off Peak Usage": OFF_PEAK,
    "Shoulder Usage": SHOULDER,
    "Network Capacity Charge": UNKNOWN_DEMAND,
    "Daily Supply Charge": SUPPLY_CHARGE,
}
ORIGIN_TARIFFS = {
    "Peak": PEAK,
    "Shoulder": SHOULDER,
    "Off-Peak": OFF_PEAK,
    "Network Access Charge": SUPPLY_CHARGE,
}

NBE_TARIFFS = {
    "Peak - step 1": PEAK,
    "Peak - step 2": PEAK,
    "Service To Property Charge": SUPPLY_CHARGE,
    "Max Demand": UNKNOWN_DEMAND,
    "Max Demand (non-summer)": NONSUMMER_DEMAND,
}

RETAILERS_TARIFFS = [TANGO_TARIFFS, ORIGIN_TARIFFS, COVAU_TARIFFS, NBE_TARIFFS]


def collect_all_tariffs(
    retailers_tariffs: List[Dict[str, str]], standardized_tariffs: List[str] = None
) -> List[str]:
    """
    Aggregates unique keys from a list of tariff dictionaries, optionally filtering by standardized tariffs.

    Parameters
    ----------
    retailers_tariffs : list of dicts
        A list of dictionaries containing tariff information for specific retailers.
    standardized_tariffs : list of str, optional
        A list of standardized tariff names to filter the collected keys.

    Returns
    -------
    list
        A list containing unique tariff keys that match the criteria.
    """
    if standardized_tariffs is not None:
        # Use set comprehension to collect only matching standardized keys
        all_tariff_keys = {
            key
            for tariffs in retailers_tariffs
            for key, std in tariffs.items()
            if std in standardized_tariffs
        }
    else:
        # Collect all keys without filtering
        all_tariff_keys = {
            key for tariffs in retailers_tariffs for key in tariffs.keys()
        }

    return list(all_tariff_keys)
