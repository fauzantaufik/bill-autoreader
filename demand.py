import math


class DemandPriceUnitEnum:
    price_per_usage = "price/usage"
    price_per_usage_per_day = "price/(usage*day)"
    unknown = "unknown"


def demand_price_unit(
    usage: float,
    price: float,
    true_subtotal: float,
    billing_days: int = None,
    loss_factor: float = 1,
    abs_tol: float = 0.01,
) -> bool:
    """
    Calculate the unit of demand price based on usage, price, and the true subtotal.
    Optionally includes billing days for more accurate calculation.

    Parameters:
    - usage (float): The amount of usage.
    - price (float): The price per unit of usage.
    - true_subtotal (float): The subtotal that the calculation should approximate.
    - billing_days (int, optional): Number of days in the billing period for daily calculations.
    - loss_factor (float, optional): Factor to account for any losses in calculation.
    - abs_tol (float, optional): Absolute tolerance used for comparing floating point numbers.

    Returns:
    - DemandPriceUnitEnum: Enum value indicating the type of pricing unit (per usage, per day, or unknown).
    """

    # Calculate the subtotal considering the loss factor
    usage_price_subtotal = usage * price * loss_factor

    # Check if calculated subtotal matches the true subtotal within the given tolerance
    is_price_per_usage = math.isclose(
        usage_price_subtotal, true_subtotal, abs_tol=abs_tol
    )

    if not billing_days:
        # If no billing days provided, determine if price per usage or per day based on comparison
        return (
            DemandPriceUnitEnum.price_per_usage
            if is_price_per_usage
            else DemandPriceUnitEnum.price_per_usage_per_day
        )
    else:
        # Adjust the check for price per usage per day when billing days are provided
        is_price_per_usage_per_day = math.isclose(
            usage_price_subtotal * billing_days, true_subtotal, abs_tol=abs_tol
        )

        if is_price_per_usage:
            return DemandPriceUnitEnum.price_per_usage
        elif is_price_per_usage_per_day:
            return DemandPriceUnitEnum.price_per_usage_per_day
        else:
            return DemandPriceUnitEnum.unknown
