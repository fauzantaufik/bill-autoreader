from bill_autoreader.evaluation.utils import (
    strip_company_suffix,
    is_name_match,
    is_within_levenshtein_distance,
)
from rapidfuzz import fuzz


def match_site_identity(predicted_value, actual_value):
    return str(predicted_value)[:10] == str(actual_value)[:10]


def standardize_string(value):
    return value.lower().replace("_", " ").strip()


def match_additional_label(predicted_tariffs, actual_tariffs, threshold=80):
    if not isinstance(predicted_tariffs, list) or not isinstance(actual_tariffs, list):
        raise ValueError("Both predicted_tariffs and actual_tariffs should be lists.")

    if len(predicted_tariffs) != len(actual_tariffs):
        return False

    standardized_predicted = [
        standardize_string(predicted) for predicted in predicted_tariffs
    ]
    standardized_actual = [standardize_string(actual) for actual in actual_tariffs]

    for predicted in standardized_predicted:
        if not any(
            fuzz.ratio(predicted, actual) >= threshold for actual in standardized_actual
        ):
            return False
    return True


def match_additional_price():
    pass


def match_retailer(autoreader_value, actual_value):
    if autoreader_value is None:
        return False

    if str(autoreader_value).lower() == "winconnect":
        autoreader_value = "win energy"

    simplified_autoreader_value = strip_company_suffix(autoreader_value)
    simplified_actual_value = strip_company_suffix(actual_value)

    if is_name_match(simplified_autoreader_value, simplified_actual_value, 95):
        return True

    if is_within_levenshtein_distance(
        simplified_autoreader_value, simplified_actual_value, 3
    ):
        return True

    if actual_value.lower() == "win energy":
        return any(
            [match_retailer(autoreader_value, act_val) for act_val in ["Win Connect"]]
        )

    return (
        simplified_autoreader_value in simplified_actual_value
        or simplified_actual_value in simplified_autoreader_value
        or is_name_match(simplified_autoreader_value, simplified_actual_value, 95)
    )


variable_to_evaluation_func = {
    "site_identity": match_site_identity,
    "retailer": match_retailer,
}
