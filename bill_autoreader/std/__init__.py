import re, warnings
from typing import List, Dict
from bill_autoreader.constants import TYPE_TARIFFS
from bill_autoreader.std.patterns import TariffPatterns
from bill_autoreader.utils import normalize_string


def get_regex_patterns(field: str) -> List[str]:
    """Get all regex patterns to find tariffs."""
    try:
        return getattr(TariffPatterns, field.upper())
    except AttributeError:
        raise Exception(f"Invalid field name: {field}")


def identify_tariffs(ori_tariff_names: List[str], std_tariff: str) -> list[str]:
    """
    Identifies tariff where the tariff names matches a specified standard tariff.
    """
    pattern_list = get_regex_patterns(std_tariff)
    found_tariffs = [
        tariff
        for tariff in ori_tariff_names
        if any(
            re.search(pattern, normalize_string(tariff), re.IGNORECASE)
            for pattern in pattern_list
        )
    ]
    return found_tariffs


def standardize_tariffs(
    tariffs: List[str], tariff_group: str = "energy_consumption"
) -> Dict[str, str]:
    """
    Standardizes tariff names in a list based on a predefined group of standard tariffs.

    Parameters
    ----------
    tariffs : List[str]
        List of original tariff names to standardize.
    tariff_group : str, optional
        The standard tariff group to use for standardization.

    Returns
    -------
    Dict[str, str]
        A mapping of each original tariff to its standardized equivalent.
    """
    warnings.filterwarnings("ignore")
    all_std_tariffs = get_regex_patterns(tariff_group)
    tariff_mapping = {}

    for std_tariff in all_std_tariffs:
        matched_tariffs = identify_tariffs(tariffs, std_tariff)
        for tariff in matched_tariffs:
            tariff_mapping[tariff] = std_tariff.replace(
                r"\b|\b", ""
            ).capitalize()  # Standardized output format

    # Mark remaining unmatched tariffs as None
    for tariff in tariffs:
        if tariff not in tariff_mapping:
            tariff_mapping[tariff] = None

    return tariff_mapping


def standardize_tariffs(
    tariffs: List[str], tariff_group: str = "energy_consumption"
) -> Dict[str, str]:
    """
    Standardizes tariff names in a list based on a predefined group of standard tariffs.

    Parameters
    ----------
    tariffs : List[str]
        List of original tariff names to standardize.
    tariff_group : str, optional
        The standard tariff group to use for standardization.

    Returns
    -------
    Dict[str, str]
        A mapping of each original tariff to its standardized equivalent.
    """
    warnings.filterwarnings("ignore")
    all_std_tariffs: list[str] = TYPE_TARIFFS[tariff_group]
    tariff_mapping = {}
    remaining_tariffs = list(tariffs)

    for standard_tariff in all_std_tariffs:
        matched_tariffs = identify_tariffs(remaining_tariffs, standard_tariff)
        for tariff in matched_tariffs:
            tariff_mapping[tariff] = standard_tariff

        # Remove all occurrences of matched tariffs
        remaining_tariffs = [
            tariff for tariff in remaining_tariffs if tariff not in matched_tariffs
        ]

    # Mark remaining unmatched tariffs as None
    for tariff in remaining_tariffs:
        tariff_mapping[tariff] = None

    return tariff_mapping
