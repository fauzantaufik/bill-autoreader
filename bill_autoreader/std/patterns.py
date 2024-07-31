class UnbundlePatterns:
    """
    Register pattern to find unbundled field data
    """

    LRET = ["LRET"]
    ESC = ["ESC"]
    SRES = ["SRES"]
    SREC = ["SREC"]
    VEET = ["VEET"]
    PRC = ["PRC"]
    AEMO_ANCILLARY = ["ancillary"]
    AEMO_POOL_FEES = ["pool"]
    PARTICIPANT_CHARGE = ["participant"]

    ENVIRONMENT = LRET + ESC + SRES + LRET + SREC + VEET + PRC
    MARKET = AEMO_ANCILLARY + AEMO_POOL_FEES + PARTICIPANT_CHARGE
    UNBUNDLED = ENVIRONMENT + MARKET + ["AEMO", "GEC"]


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

    PEAK = [
        # Step-based patterns
        r"^(?!.*\b(?:off|summer|demand|shoulder|solar|controlled|shoulder usage|off peak|offpeak usage)\b).*step\b.*$",
        # Patterns specifically excluding 'off', 'summer', 'demand', etc.
        r"^(?!.*\b(?:off|summer|demand|shoulder|solar|controlled|shoulder usage|off peak|offpeak usage)\b).*peak\b.*(usage|energy|charge|period|consumption)",
        # Direct match excluding unwanted words
        r"^(?!.*\b(?:off|summer|demand|shoulder|solar|controlled|shoulder usage|off peak|offpeak usage)\b).*\busage\b.*$",
        "^summer peak$",
        "retail peak",
        "retail - peak",
        "network - peak",
        "vic peak",
        "nsw peak",
        "cmg - peak",
        "^peak$",
        r"^peak\s\(.*?\)$",
        "^peak gas",
        "general usage",
        "anytime",
        "any time",
        "flat usage",
        r"^(?!.*\b(?:off|shoulder|offpeak usage)\b).*standard.*$",  # Excludes 'off', 'shoulder', 'offpeak'
        "total peak",
        "electricity consumption",
        "all usage",
        "next",
        "first",
        "balance",
        "metered lpg",
        "kg",
        "lpg propane",
        # Include 'On peak'
        r"^(?!.*\b(?:off|summer|demand|shoulder|solar|controlled|shoulder usage|off peak|offpeak usage)\b).*on peak\b.*$",
        "Consumption Charge",
        "total consumption",
        r"^step[1-5]$",
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
        "access charge",
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
    SUMMER_DEMAND = [
        "summer_demand",  # Literal keyword
        r"^(?!.*\bnon[- ]summer\b).*Summer",  # Exclude non-summer variants (with hyphens or spaces)
        r"high season demand",  # Literal keyword for high season demand
    ]

    NONSUMMER_DEMAND = [
        "nonsummer_demand",
        "Non-Summer Demand",
        "non summer",
        "non-summer",
        r"^[\.]*((?!(off|peak)).)*winter",
    ]
    UNKNOWN_DEMAND = [
        r"^(?!.*\bsummer\b)(?!.*\bnonsummer\b)(?!.*\bhigh season demand\b).*\bdemand\b",  # Matches 'demand' but excludes 'summer', 'nonsummer', and 'high season demand'
        r"^(?!.*\bsummer\b)(?!.*\bnonsummer\b)(?!.*\bhigh season demand\b).*\bcapacity\b",  # Matches 'capacity' but excludes 'summer', 'nonsummer', and 'high season demand'
        "unknown_demand",  # Literal keyword
    ]
    SOLAR_FIT = ["solar_fit", "solar", "feed-in"]
    CONTROLLED_LOAD = [
        "controlled_load",
        "controlled load",
        "CL\d+",
        "dedicated circuit",
    ]
    METERING_CHARGE = [
        r"^(?!.*\bsolar\b).*meter charge",  # Matches 'meter charge' excluding those containing 'solar'
        r"^(?!.*\bsolar\b).*metering",  # Matches 'metering' excluding those containing 'solar'
        "metering_charge",  # Literal keyword
        "Microgrid Child",  # Literal keyword
        r"^(?!.*\bsolar\b).*meter",  # Matches 'meter' excluding those containing 'solar'
    ]

    OTHER = [r"^other$", "AEMO Charges"]

    # Discount Table
    DISCOUNT = ["discount"]
    DISCOUNT_FROM_LABEL = [r"[0-9]+%"]
    TOTAL_BEFORE_DISCOUNT = [r"electricity charge", r"gas charge", r"total charge"]
