class UnbundlePatterns:
    """
    Register pattern to find unbundled field data
    """

    LRET = ["LRET"]
    ESC = ["ESC"]
    SRES = ["SRES"]
    SREC = ["SREC"]
    VEET = ["VEET"]
    AEMO_ANCILLARY = ["ancillary"]
    AEMO_POOL_FEES = ["pool"]
    PARTICIPANT_CHARGE = ["participant"]

    ENVIRONMENT = LRET + ESC + SRES + LRET + SREC + VEET
    MARKET = AEMO_ANCILLARY + AEMO_POOL_FEES + PARTICIPANT_CHARGE
    UNBUNDLED = ENVIRONMENT + MARKET


class TariffPatterns(UnbundlePatterns):
    """
    Register pattern to find field data
    """

    START_DATE = [
        "%d %b %Y",
        "%d-%b-%Y",
        "%d/%b/%Y",
        "%d %b %y",
        "%d %m %Y",
        "%d-%m-%Y",
        "%d/%m/%Y",
        "%d%m%Y",
        "%d %B %Y",
        "%d-%B-%Y",
    ]

    # Charge Table
    PEAK = [
        # has peak and doesnt contain off/summer/demand before step
        r"^[\.]*((?!(off|summer|demand|shoulder|solar|controlled)).)*step",
        # has peak and doesnt contain off/summer/demand before peak,
        # r"^[\.]*((?!(off|summer|demand|shoulder|solar|controlled)).)*peak (usage|energy|charge|period|consumption)",
        # r"^[\.]*((?!(off|summer|demand|shoulder|solar|controlled)).)*(peak\s|\bpeak)(usage|energy|charge|period|consumption)",
        # has usage and doesnt contain off/summer/demand before peak,
        r"^(?!.*\b(?:off|summer|demand|shoulder|solar|controlled)\b).*\bpeak\b.*$",
        r"^[\.]*((?!(off|summer|demand|shoulder|solar|controlled)).)*usage",
        "^summer peak$",
        "retail peak",
        "retail - peak",
        "network - peak",
        "vic peak",
        "nsw peak",
        "cmg - peak",
        "^peak$",
        r"^peak\s\(.*?\)$",
        # r"^(?!.*\boff\b).*\bpeak\b.*$",  # has peak and doesnt contain off before peak,
        "^peak gas",
        "general usage",
        "anytime",
        "any time",
        "flat usage",
        "^(?!.*feed-in).*standard.*",  # feed in is for solar export
        "total peak",
        "electricity consumption",
        # TODO: contains "all usage but does not contain off-peak, shoulder, controlled etc"
        "all usage",
        "next",
        "first",
        "balance",
        # lpg pattern
        "metered lpg",
        "kg",
        "lpg propane",
    ]

    OFF_PEAK = [
        "off_peak",
        "off peak",
        "off-peak",
        "(vic|cmg) off-peak",
        "offpeak",
        "retail - off peak",
    ]
    SHOULDER = ["Shoulder", "retail - shoulder"]
    SUPPLY_CHARGE = [
        "supply_charge",
        "^daily",
        "^supply",
        "daily",
        r"supply\s*charge",
        r".aily\s*supply",
        r"s\w+y\s*ch\w+e",  # s[any chars]y[optional whitespace]ch[anychars]e
        "supply days",
        "network daily charge",
        "service to property charge",
        "service",
        r"service\s*to\s*property",
        # "^[\.]*((?!(solar|peak|participant|supply|daily|capacity|gas|aemo|metering|demand|usage|meter)).)*charge",
        "Gas Daily Charge",
        "(CMG)*Supply Charge",
        "fixed",
        "standing charge",
    ]
    OTHER_CHARGES = ["fee", "credit card", "Meter Read Fee", "debit card", "meter read"]
    SUMMER_DEMAND = ["summer_demand", "^(?!(non)).*Summer"]
    NONSUMMER_DEMAND = [
        "nonsummer_demand",
        "Non-Summer Demand",
        "non summer",
        r"^[\.]*((?!(off|peak)).)*winter",
    ]
    UNKNOWN_DEMAND = ["unknown_demand", "demand", "capacity"]
    SOLAR_FIT = ["solar_fit", "solar", "feed-in"]
    CONTROLLED_LOAD = ["controlled_load", "controlled load", "CL2", "dedicated circuit"]
    METERING_CHARGE = ["metering_charge", "metering", "Microgrid Child"]
    OTHER = [r"^other$", "AEMO Charges"]

    # Discount Table
    DISCOUNT = ["discount"]
    DISCOUNT_FROM_LABEL = [r"[0-9]+%"]
    TOTAL_BEFORE_DISCOUNT = [r"electricity charge", r"gas charge", r"total charge"]
