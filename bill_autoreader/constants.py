import numpy as np
from decimal import Decimal
from math import nan


LRET = "LRET"
ESC = "ESC"
SRES = "SRES"
SREC = "SREC"
VEET = "VEET"
AEMO_ANCILLARY = "aemo_ancillary"
AEMO_POOL_FEES = "aemo_pool_fees"
PARTICIPANT_CHARGE = "participant_charge"

SUPPLY_CHARGE = "supply_charge"
PEAK = "peak"
OFF_PEAK = "off_peak"
SHOULDER = "shoulder"
UNKNOWN_DEMAND = "unknown_demand"
NONSUMMER_DEMAND = "nonsummer_demand"
SUMMER_DEMAND = "summer_demand"
CONTROLLED_LOAD = "controlled_load"
SOLAR_FIT = "solar_fit"
METERING_CHARGE = "metering_charge"
OTHER = "other"
ADDITIONAL_PRICE = "additional_price"
ADDITIONAL_LABEL = "additional_label"


ENERGY_CONSUMPTION_TARIFF = [  # charge row for regular bill
    SUPPLY_CHARGE,
    PEAK,
    OFF_PEAK,
    SHOULDER,
    CONTROLLED_LOAD,
    METERING_CHARGE,
    NONSUMMER_DEMAND,
    SUMMER_DEMAND,
    SOLAR_FIT,
    UNKNOWN_DEMAND,
    OTHER,
]

MARKET_TARIFF = {
    LRET: LRET,
    ESC: ESC,
    SRES: SRES,
    SREC: SREC,
    VEET: VEET,
    AEMO_ANCILLARY: "AEMO Ancillary",
    AEMO_POOL_FEES: "AEMO Pool Fees",
    PARTICIPANT_CHARGE: "Participant Charge",
}

LIST_FIELDS = [OFF_PEAK, SHOULDER, PEAK, SOLAR_FIT, CONTROLLED_LOAD]

TYPE_TARIFFS = {
    "energy_consumption": ENERGY_CONSUMPTION_TARIFF,
    "market_tariff": MARKET_TARIFF,
}
UNBUNDLED = "unbundled"


USAGE_DISCOUNT = "usage_discount"
POT_DISCOUNT = "pot_discount"
SUPPLY_DISCOUNT = "supply_discount"

GST_RATE = 1.1
NONE_DEMAND = [None, 999, "999", "", Decimal(999), Decimal("999"), 0, nan, np.nan]
