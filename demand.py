import math
from datetime import date
from utils import calculate_months_between_dates, to_list, combine_into_list
from typing import Union, List, Dict


class DemandPriceUnitEnum:
    price_per_usage = "price/usage"
    price_per_usage_per_day = "price/(usage*day)"
    unknown = "unknown"


def demand_price_unit(
    demand_usage: float,
    demand_price: float,
    demand_true_subtotal: float,
    billing_days: int = None,
    loss_factor: float = 1,
    abs_tol: float = 0.01,
) -> bool:
    """
    Calculate the unit of demand price based on usage, price, and the true subtotal.
    Optionally includes billing days for more accurate calculation.

    Parameters:
    - demand_usge (float): The amount of usage for one demand value.
    - demand_price (float): The price per unit of usage for one demand value.
    - demand_true_subtotal (float): The subtotal that the calculation should approximate for one demand value.
    - billing_days (int, optional): Number of days in the billing period for daily calculations.
    - loss_factor (float, optional): Factor to account for any losses in calculation.
    - abs_tol (float, optional): Absolute tolerance used for comparing floating point numbers.

    Returns:
    - DemandPriceUnitEnum: Enum value indicating the type of pricing unit (per usage, per day, or unknown).
    """

    # Calculate the subtotal considering the loss factor
    usage_price_subtotal = demand_usage * demand_price * loss_factor

    # Check if calculated subtotal matches the true subtotal within the given tolerance
    is_price_per_usage = math.isclose(
        usage_price_subtotal, demand_true_subtotal, abs_tol=abs_tol
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
            usage_price_subtotal * billing_days, demand_true_subtotal, abs_tol=abs_tol
        )

        if is_price_per_usage:
            return DemandPriceUnitEnum.price_per_usage
        elif is_price_per_usage_per_day:
            return DemandPriceUnitEnum.price_per_usage_per_day
        else:
            return DemandPriceUnitEnum.unknown


def is_monthly_demand(
    all_demand: Union[float, list],
    start_period: date = None,
    end_period: date = None,
):
    """
    Parameters:
    - All Demand : Combination of all kind of demand which are summer and non-summer.
    """
    if not isinstance(all_demand, list):
        return False
    else:
        if start_period and end_period:
            # Calculate the number of complete months between start_period and end_period
            n_months = calculate_months_between_dates(start_period, end_period)
            # Check if the length of the demand list matches the number of months
            return len(all_demand) == n_months
        else:
            # If no start and end periods are provided, check if the demand list is non-empty
            return len(all_demand) > 0


def get_demand_multiplier(
    usages: List[float], prices: List[int], subtotals: List[float]
) -> List[float]:
    """
    Calculate the demand multipliers from subtotal, usage, and price lists.

    Parameters:
    - subtotals (List[float]): List of subtotals for each demand.
    - usages (List[float]): List of usage amounts for each demand.
    - prices (List[float]): List of prices for each demand.

    Returns:
    - List[float]: A list of calculated multipliers for each demand.
    """
    return [
        round(subtotal / (usage * price), 2)
        for subtotal, usage, price in zip(subtotals, usages, prices)
    ]


def get_demand_structure(
    nonsummer_demand: Dict[str, Union[float, List[float]]],
    summer_demand: Dict[str, Union[float, List[float]]],
    start_date: date,
    end_date: date,
    loss_factor: float = 1.0,
) -> dict:
    """
    Analyze the structure of demand based on billing period and demand data for summer and non-summer,
    taking into account a loss factor.

    Parameters:
    - summer_demand (Dict[str, Union[float, List[float]]]): Demand data for summer period with keys 'usage', 'price', 'subtotal'.
    - nonsummer_demand (Dict[str, Union[float, List[float]]]): Demand data for non-summer period with similar structure.
    - start_date (date): Start date of the billing period.
    - end_date (date): End date of the billing period.
    - loss_factor (float, optional): Factor to account for any losses in calculation.

    Returns:
    - dict: Dictionary with details about demand validation, price unit, and multipliers.
    """
    results = {
        "monthly_demand": False,
        "price_unit": DemandPriceUnitEnum.price_per_usage,
        "multipliers": None,
    }

    # Collect price units to validate consistency
    price_units = set()

    # Function to handle individual or list-based calculations
    def process_demand(demand_data: Dict[str, Union[float, List[float]]]):
        """Helper function to process demand data based on whether it's a float or a list of floats."""
        usages = to_list(demand_data["usage"])
        prices = to_list(demand_data["price"])
        subtotals = to_list(demand_data["subtotal"])

        # Validate and calculate price units for each demand data set
        for usage, price, subtotal in zip(usages, prices, subtotals):
            price_unit = demand_price_unit(
                usage, price, subtotal, loss_factor=loss_factor
            )
            price_units.add(price_unit)

    # Process both summer and non-summer demand data
    combine_demand = {
        key: combine_into_list(nonsummer_demand[key], summer_demand[key])
        for key in ["price", "usage", "subtotal"]
    }
    if combine_demand:
        process_demand(combine_demand)

    # Check if all entries have the same price unit
    if len(price_units) == 1:
        results["price_unit"] = list(price_units)[
            0
        ]  # Assuming all entries have the same unit

    print("combine_demand", combine_demand)
    results["monthly_demand"] = is_monthly_demand(
        combine_demand["price"], start_date, end_date
    )

    # Calculate multipliers if the data corresponds to monthly demand and the unit is price per usage per day
    if (
        results["monthly_demand"]
        and results["price_unit"] == DemandPriceUnitEnum.price_per_usage_per_day
    ):
        demand_names = ["nonsummer", "summer"]
        results["multipliers"] = {key: [] for key in demand_names}
        for demand_name, demand_val in zip(
            demand_names, [nonsummer_demand, summer_demand]
        ):
            results["multipliers"][demand_name] = get_demand_multiplier(
                to_list(demand_val["usage"]),
                to_list(demand_val["price"]),
                to_list(demand_val["subtotal"]),
            )

    return results
