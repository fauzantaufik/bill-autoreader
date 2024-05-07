from datetime import date, timedelta
from typing import Union, List, Any, Optional


def days_between_dates_inclusive(start_date: date, end_date: date) -> int:
    """
    Calculate the number of days between two dates, inclusive of both start and end dates.

    Parameters:
    - start_date (date): The starting date.
    - end_date (date): The ending date.

    Returns:
    - int: The inclusive number of days between the start_date and end_date.
    """
    # Calculate the difference between the two dates
    delta = end_date - start_date
    # Add 1 to include both the start and end date in the count
    return delta.days + 1


def calculate_end_date(start_date: date, supply_days: int) -> date:
    """
    Calculate the end date by adding a given number of days to the start date.

    Parameters:
    - start_date (date): The starting date.
    - supply_days (int): The number of days to add to the start date.

    Returns:
    - date: The end date calculated by adding the supply days to the start date.
    """
    # Add the number of supply days to the start date using timedelta
    end_date = start_date + timedelta(days=supply_days)
    return end_date


def calculate_months_between_dates(
    start_date: Optional[date], end_date: Optional[date]
) -> int:
    """
    Calculate the number of complete months between two dates, inclusive.

    Parameters:
    - start_date (Optional[date]): Start date.
    - end_date (Optional[date]): End date.

    Returns:
    - int: Number of complete months between the two dates. Returns 0 if either date is not provided.
    """
    if not start_date or not end_date:
        return 0

    return (
        (end_date.year - start_date.year) * 12 + (end_date.month - start_date.month) + 1
    )


def to_list(value: Union[Any, List[Any], None]) -> List[Any]:
    """
    Converts a single value into a list if it's not already a list and filters out None values.

    Parameters:
    - value (Union[Any, List[Any], None]): The input value that may be a single value, a list, or None.

    Returns:
    - List[Any]: A list containing the input value(s), excluding None values.
    """
    if value is None:
        return []
    return value if isinstance(value, list) else [value]


def combine_into_list(
    value1: Union[Any, List[Any], None], value2: Union[Any, List[Any], None]
) -> List[Any]:
    """
    Combines two values into a single flattened list, excluding None values.

    Parameters:
    - value1 (Union[Any, List[Any], None]): The first value that may be a single value, a list, or None.
    - value2 (Union[Any, List[Any], None]): The second value that may be a single value, a list, or None.

    Returns:
    - List[Any]: A single list combining both input values.
    """
    # Convert each value to a list and concatenate them
    return to_list(value1) + to_list(value2)
