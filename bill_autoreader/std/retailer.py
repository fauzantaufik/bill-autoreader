from typing import List, Dict
from bill_autoreader.constants import (
    PEAK,
    OFF_PEAK,
    SHOULDER,
    UNKNOWN_DEMAND,
    SUPPLY_CHARGE,
    NONSUMMER_DEMAND,
    UNBUNDLED,
    CONTROLLED_LOAD,
    METERING_CHARGE,
)


UNSTANDARDIZED_TARIFFS = {}

# Compiled how retailer label tariff
TANGO_TARIFFS = {
    "Peak": PEAK,
    "Shoulder": SHOULDER,
    "Off Peak": OFF_PEAK,
    "Supply Charge": SUPPLY_CHARGE,
}
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
    "AEMO Participant Charge": UNBUNDLED,
    "AEMO Ancillary Charge": UNBUNDLED,
    "AEMO FRC Operations": UNBUNDLED,
    "PRC Charge": UNBUNDLED,
    "Access Charge": SUPPLY_CHARGE,
}
NBE_TARIFFS = {
    "Peak - step 1": PEAK,
    "Peak - step 2": PEAK,
    "Service To Property Charge": SUPPLY_CHARGE,
    "Max Demand": UNKNOWN_DEMAND,
    "Max Demand (non-summer)": NONSUMMER_DEMAND,
    "Metering Charge": METERING_CHARGE,
    "Network Daily Charge (Cost)": SUPPLY_CHARGE,
    "GEC Charge": UNBUNDLED,
    "RET (STCs & LGCs)": UNBUNDLED,
}
MOMENTUM_TARIFFS = {"Peak": PEAK, "Off Peak": OFF_PEAK, "Daily Charge": SUPPLY_CHARGE}
BLUENRG_TARIFFS = {
    "Daily Supply Charge": SUPPLY_CHARGE,
    "Peak period": PEAK,
    "Off peak period": OFF_PEAK,
    "Off-Peak": OFF_PEAK,
}
REDENERGY_TARIFFS = {
    "Total CL1": CONTROLLED_LOAD,
    "TOTAL CL2": CONTROLLED_LOAD,
    "Total Peak": PEAK,
    "Total Shoulder": SHOULDER,
    "Total Off Peak": OFF_PEAK,
    "Demand": UNKNOWN_DEMAND,
    "Service to Property Charge": SUPPLY_CHARGE,
}
GLOBIRD_TARIFFS = {
    "Daily Charge": SUPPLY_CHARGE,
    "Peak Usage": PEAK,
    "Offpeak Usage": OFF_PEAK,
    "Shoulder Usage": SHOULDER,
}
AGL_TARIFFS = {
    "General usage": PEAK,
    "General usage next": PEAK,
    "Supply charge": SUPPLY_CHARGE,
}
ALINTA_TARIFFS = {
    "Anytime - Step 1": PEAK,
    "Anytime - Step 2": PEAK,
    "Anytime - Step 3": PEAK,
    "Anytime - Remaining balance": PEAK,
    "Daily": SUPPLY_CHARGE,
}
SUMO_TARIFFS = {
    "Off Peak Energy": OFF_PEAK,
    "Peak Energy": PEAK,
    "Standing Charge": SUPPLY_CHARGE,
}
SYNERGY_RETAILER = {
    "On peak": PEAK,
    "Off peak": OFF_PEAK,
    "Supply charge": SUPPLY_CHARGE,
}
FIRSTENERGY_TARIFFS = {
    "General Usage (22) ‐ Step 1": PEAK,
    "General Usage (22) ‐ Step 2": PEAK,
    "Daily Supply Charge": SUPPLY_CHARGE,
}
POWERSHOP_TARIFFS = {
    "All Day Usage": PEAK,
    "Daily (125.88 c/day x 2 days)": SUPPLY_CHARGE,
}
REAMPED_TARIFFS = {
    "Peak": PEAK,
    "Off Peak": OFF_PEAK,
    "Daily Supply Charge": SUPPLY_CHARGE,
}
SIMPLY_TARIFFS = {
    "Supply Charges ( 31 Days )": SUPPLY_CHARGE,
    "First": PEAK,
    "Next": PEAK,
}
Q_TARIFFS = {
    "Supply Charge": SUPPLY_CHARGE,
    "Usage Off Peak Usage": OFF_PEAK,
    "Usage Peak Usage": PEAK,
    "Usage Shoulder Usage": SHOULDER,
    "Peak Demand": UNKNOWN_DEMAND,
}

RETAILERS_TARIFFS = [
    TANGO_TARIFFS,
    ORIGIN_TARIFFS,
    COVAU_TARIFFS,
    NBE_TARIFFS,
    REDENERGY_TARIFFS,
    BLUENRG_TARIFFS,
    MOMENTUM_TARIFFS,
    GLOBIRD_TARIFFS,
    ALINTA_TARIFFS,
    SUMO_TARIFFS,
    SYNERGY_RETAILER,
    FIRSTENERGY_TARIFFS,
    POWERSHOP_TARIFFS,
    REAMPED_TARIFFS,
    SIMPLY_TARIFFS,
    Q_TARIFFS,
]


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
