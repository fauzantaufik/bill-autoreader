from bill_autoreader.evaluation.utils import (
    strip_company_suffix,
    is_name_match,
    is_within_levenshtein_distance,
)
from rapidfuzz import fuzz
from bill_autoreader.utils import convert_to_boolean, normalize_list


def match_site_identity(predicted_value, actual_value):
    return str(predicted_value)[:10] == str(actual_value)[:10]


def standardize_string(value):
    return value.lower().replace("_", " ").strip()


def match_additional_tariff(
    predicted_labels, predicted_prices, actual_labels, actual_prices, threshold=80
):
    # Check if all inputs are lists and have the same length
    if not (
        isinstance(predicted_labels, list)
        and isinstance(predicted_prices, list)
        and isinstance(actual_labels, list)
        and isinstance(actual_prices, list)
    ):
        raise ValueError("All inputs should be lists.")

    if not (
        len(predicted_labels)
        == len(predicted_prices)
        == len(actual_labels)
        == len(actual_prices)
    ):
        return False

    # Standardize labels
    normalized_predicted_labels = [
        standardize_string(label) for label in predicted_labels
    ]
    normalized_actual_labels = [standardize_string(label) for label in actual_labels]

    # Create pairs of standardized labels and prices
    predicted_pairs = list(zip(normalized_predicted_labels, predicted_prices))
    actual_pairs = list(zip(normalized_actual_labels, actual_prices))

    # Match each predicted pair to an actual pair
    for predicted_label, predicted_price in predicted_pairs:
        match_found = False
        for actual_label, actual_price in actual_pairs:
            if (
                fuzz.ratio(predicted_label, actual_label) >= threshold
                and predicted_price == actual_price
            ):
                match_found = True
                break
        if not match_found:
            return False
    return True


def match_monthly_demand_multiplier(predicted_value, actual_value):
    normalized_predicted = normalize_list(predicted_value)
    normalized_actual = normalize_list(actual_value)

    return normalized_predicted == normalized_actual


def match_divide_demand(predicted_value, actual_value):
    try:
        predicted_bool = convert_to_boolean(predicted_value)
        actual_bool = convert_to_boolean(actual_value)
    except ValueError:
        return False
    return predicted_bool == actual_bool


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
    "additional_tariff": match_additional_tariff,
    "divide_demand": match_divide_demand,
}
