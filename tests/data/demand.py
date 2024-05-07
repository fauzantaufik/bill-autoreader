from datetime import date
from bill_autoreader.demand import DemandPriceUnitEnum


sample_demand_data_monthly_per_usage_per_day = [
    {
        "input": {
            "summer_demand": {"usage": [100], "price": [10], "subtotal": [12000]},
            "nonsummer_demand": {
                "usage": [150],
                "price": [15],
                "subtotal": [22500],
            },
            "start_date": date(2024, 3, 20),  # 12 days
            "end_date": date(2024, 4, 10),  # 10 days
        },
        "expected": {
            "monthly_demand": True,  # Adjust based on expected results
            "price_unit": DemandPriceUnitEnum.price_per_usage_per_day,
            "multipliers": {
                "summer": [12],
                "nonsummer": [10],
            },
        },
    },
    {
        "input": {
            "summer_demand": {"usage": 100, "price": 10, "subtotal": 12000},
            "nonsummer_demand": {
                "usage": [150],
                "price": [15],
                "subtotal": [22500],
            },
            "start_date": date(2024, 3, 20),  # 12 days
            "end_date": date(2024, 4, 10),  # 10 days
        },
        "expected": {
            "monthly_demand": True,  # Adjust based on expected results
            "price_unit": DemandPriceUnitEnum.price_per_usage_per_day,
            "multipliers": {
                "summer": [12],
                "nonsummer": [10],
            },
        },
    },
    {
        "input": {
            "summer_demand": {"usage": 100, "price": 10, "subtotal": 12000},
            "nonsummer_demand": {
                "usage": [150, 10],
                "price": [15, 10],
                "subtotal": [22500, 1000],
            },
            "start_date": date(2024, 3, 20),  # 12 days
            "end_date": date(2024, 4, 10),  # 10 days
        },
        "expected": {
            "monthly_demand": False,  # Adjust based on expected results
            "price_unit": DemandPriceUnitEnum.price_per_usage_per_day,
            "multipliers": {
                "summer": [12],
                "nonsummer": [10, 10],
            },
        },
    },
    {
        "input": {
            "summer_demand": {"usage": None, "price": None, "subtotal": None},
            "nonsummer_demand": {
                "usage": [100, 150],
                "price": [10, 15],
                "subtotal": [12000, 22500],
            },
            "start_date": date(2024, 3, 20),  # 12 days
            "end_date": date(2024, 4, 10),  # 10 days
        },
        "expected": {
            "monthly_demand": True,  # Adjust based on expected results
            "price_unit": DemandPriceUnitEnum.price_per_usage_per_day,
            "multipliers": {
                "summer": [],
                "nonsummer": [12, 10],
            },
        },
    },
    {
        "input": {
            "nonsummer_demand": {"usage": None, "price": None, "subtotal": None},
            "summer_demand": {
                "usage": [100, 150],
                "price": [10, 15],
                "subtotal": [12000, 22500],
            },
            "start_date": date(2024, 3, 20),  # 12 days
            "end_date": date(2024, 4, 10),  # 10 days
        },
        "expected": {
            "monthly_demand": True,  # Adjust based on expected results
            "price_unit": DemandPriceUnitEnum.price_per_usage_per_day,
            "multipliers": {
                "nonsummer": [],
                "summer": [12, 10],
            },
        },
    },
]


sample_demand_non_monthly_per_usage_per_day = [
    {
        "input": {
            "summer_demand": {"usage": [100], "price": [10], "subtotal": [12000]},
            "nonsummer_demand": {
                "usage": None,
                "price": None,
                "subtotal": None,
            },
            "start_date": date(2024, 3, 20),  # 12 days
            "end_date": date(2024, 4, 10),  # 10 days
        },
        "expected": {
            "monthly_demand": False,  # Adjust based on expected results
            "price_unit": DemandPriceUnitEnum.price_per_usage_per_day,
            "multipliers": {
                "summer": [12],
                "nonsummer": [],
            },
        },
    },
    {
        "input": {
            "nonsummer_demand": {"usage": [100], "price": [10], "subtotal": [12000]},
            "summer_demand": {
                "usage": None,
                "price": None,
                "subtotal": None,
            },
            "start_date": date(2024, 3, 20),  # 12 days
            "end_date": date(2024, 4, 10),  # 10 days
        },
        "expected": {
            "monthly_demand": False,  # Adjust based on expected results
            "price_unit": DemandPriceUnitEnum.price_per_usage_per_day,
            "multipliers": {
                "nonsummer": [12],
                "summer": [],
            },
        },
    },
    {
        "input": {
            "nonsummer_demand": {"usage": 100, "price": 10, "subtotal": 12000},
            "summer_demand": {
                "usage": None,
                "price": None,
                "subtotal": None,
            },
            "start_date": date(2024, 3, 20),  # 12 days
            "end_date": date(2024, 4, 10),  # 10 days
        },
        "expected": {
            "monthly_demand": False,  # Adjust based on expected results
            "price_unit": DemandPriceUnitEnum.price_per_usage_per_day,
            "multipliers": {
                "nonsummer": [12],
                "summer": [],
            },
        },
    },
]


sample_demand_per_usage = [
    {
        "input": {
            "summer_demand": {"usage": [100], "price": [10], "subtotal": [1000]},
            "nonsummer_demand": {
                "usage": None,
                "price": None,
                "subtotal": None,
            },
            "start_date": date(2024, 3, 20),  # 12 days
            "end_date": date(2024, 4, 10),  # 10 days
        },
        "expected": {
            "monthly_demand": False,  # Adjust based on expected results
            "price_unit": DemandPriceUnitEnum.price_per_usage,
            "multipliers": None,
        },
    },
    {
        "input": {
            "summer_demand": {"usage": 100, "price": 10, "subtotal": 1000},
            "nonsummer_demand": {
                "usage": None,
                "price": None,
                "subtotal": None,
            },
            "start_date": date(2024, 3, 20),  # 12 days
            "end_date": date(2024, 4, 10),  # 10 days
        },
        "expected": {
            "monthly_demand": False,  # Adjust based on expected results
            "price_unit": DemandPriceUnitEnum.price_per_usage,
            "multipliers": None,
        },
    },
    {
        "input": {
            "summer_demand": {"usage": [100], "price": [10], "subtotal": [1000]},
            "nonsummer_demand": {
                "usage": [150],
                "price": [15],
                "subtotal": [2250],
            },
            "start_date": date(2024, 3, 20),  # 12 days
            "end_date": date(2024, 4, 10),  # 10 days
        },
        "expected": {
            "monthly_demand": True,  # Adjust based on expected results
            "price_unit": DemandPriceUnitEnum.price_per_usage,
            "multipliers": None,
        },
    },
]
