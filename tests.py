from demand import demand_price_unit, DemandPriceUnitEnum


def test_demand_price_unit_with_billing_days_price_per_usage():
    assert (
        demand_price_unit(89.38, 0.3081, 27.54, 4)
        == DemandPriceUnitEnum.price_per_usage
    )


def test_demand_price_unit_with_billing_days_price_per_usage_per_day():
    assert (
        demand_price_unit(19, 0.3711, 98.72, 14)
        == DemandPriceUnitEnum.price_per_usage_per_day
    )
    assert (
        demand_price_unit(19, 0.3711, 105.77, 15)
        == DemandPriceUnitEnum.price_per_usage_per_day
    )
