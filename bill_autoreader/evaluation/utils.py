from rapidfuzz import fuzz, distance


def is_within_levenshtein_distance(predicted_value, actual_value, max_distance=3):
    distance_val = distance.Levenshtein.distance(predicted_value, actual_value)
    return distance_val <= max_distance


def is_name_match(predicted_value, actual_value, threshold=97):
    token_ratio = fuzz.token_set_ratio(predicted_value, actual_value)
    return token_ratio >= threshold


def strip_company_suffix(value):
    if value is None:
        return value
    # Convert to lowercase and replace underscores with spaces
    suffixes = [
        "pty ltd",
        "ltd",
        "inc",
        "corporation",
        "limited",
        "real estate",
        "license",
        "centres",
        "sales",
        "group",
        "energy",  # energy is largely used in company name but it's not a unique name of company that can be identified. so we better to remove it
    ]
    value = value.lower().replace("_", " ")
    # Remove common suffixes
    for suffix in suffixes:
        value = value.replace(suffix, "").strip()
    return value


# ----------------------------------------------------------------
