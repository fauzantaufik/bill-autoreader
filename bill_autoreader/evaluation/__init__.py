from bill_autoreader.evaluation.utils import (
    strip_company_suffix,
    is_name_match,
    is_within_levenshtein_distance,
)


def match_site_identity(predicted_value, actual_value):
    return str(predicted_value)[:10] == str(actual_value)[:10]


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
