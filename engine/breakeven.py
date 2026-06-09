# Rent-vs-buy breakeven - net-wealth crossover.

ANNUAL_OWNERSHIP_COST_RATE = 0.01

MONTHS_PER_YEAR = 12


def find_breakeven(
    property_values: list,
    mortgage_balances: list,
    monthly_payment: float,
    deposit: float,
    stamp_duty: float,
    lmi: float,
    rent_by_year: list,
    invested_balances: list,
):
    number_of_years = len(property_values)
    if number_of_years == 0:
        raise ValueError("yearly lists must not be empty")
    same_length = (
        len(mortgage_balances) == number_of_years
        and len(rent_by_year) == number_of_years
        and len(invested_balances) == number_of_years
    )
    if not same_length:
        raise ValueError("all yearly lists must be the same length")

    annual_mortgage_payment = monthly_payment * MONTHS_PER_YEAR

    yearly_breakdown = []
    breakeven_year = None

    cumulative_rent_paid = 0.0
    cumulative_ownership_cost = 0.0

    for year_index in range(number_of_years):
        year_number = year_index + 1

        cumulative_rent_paid = cumulative_rent_paid + rent_by_year[year_index]
        invested_value = invested_balances[year_index]
        rent_wealth = invested_value - cumulative_rent_paid

        property_value = property_values[year_index]
        ownership_cost_this_year = property_value * ANNUAL_OWNERSHIP_COST_RATE
        cumulative_ownership_cost = cumulative_ownership_cost + ownership_cost_this_year

        cumulative_mortgage_paid = annual_mortgage_payment * year_number
        cumulative_buy_cash = (
            deposit
            + stamp_duty
            + lmi
            + cumulative_mortgage_paid
            + cumulative_ownership_cost
        )

        equity = property_value - mortgage_balances[year_index]
        buy_wealth = equity - cumulative_buy_cash

        yearly_breakdown.append(
            {
                "year": year_number,
                "buy_wealth": round(buy_wealth, 2),
                "rent_wealth": round(rent_wealth, 2),
                "equity": round(equity, 2),
            }
        )

        if breakeven_year is None and buy_wealth >= rent_wealth:
            breakeven_year = year_number

    return breakeven_year, yearly_breakdown


if __name__ == "__main__":
    from engine.stamp_duty import calculate_stamp_duty
    from engine.lmi import calculate_lmi
    from engine.mortgage import calculate_monthly_payment
    from engine.property_value import calculate_property_value
    from engine.mortgage_balance import calculate_mortgage_balance
    from engine.rent_projection import calculate_rent_projection
    from engine.opportunity_cost import calculate_opportunity_cost

    price = float(input("Enter property price: "))
    deposit = float(input("Enter deposit: "))
    mortgage_rate = float(input("Enter mortgage rate (e.g. 0.06): "))
    loan_term_years = int(input("Enter loan term in years: "))
    horizon_years = int(input("Enter horizon in years: "))
    weekly_rent = float(input("Enter weekly rent: "))
    property_growth = float(input("Enter property growth rate (e.g. 0.05): "))
    rent_growth = float(input("Enter rent growth rate (e.g. 0.03): "))
    return_rate = float(input("Enter investment return rate (e.g. 0.07): "))

    loan_amount = price - deposit
    stamp_duty = calculate_stamp_duty(price)
    lmi = calculate_lmi(price, deposit)
    monthly_payment = calculate_monthly_payment(loan_amount, mortgage_rate, loan_term_years)

    property_values = calculate_property_value(price, horizon_years, property_growth)
    mortgage_balances = calculate_mortgage_balance(loan_amount, mortgage_rate, loan_term_years, horizon_years)
    rent_by_year = calculate_rent_projection(weekly_rent, horizon_years, rent_growth)
    invested_balances = calculate_opportunity_cost(deposit, horizon_years, return_rate)

    breakeven_year, yearly_breakdown = find_breakeven(
        property_values = property_values,
        mortgage_balances = mortgage_balances,
        monthly_payment = monthly_payment,
        deposit = deposit,
        stamp_duty = stamp_duty,
        lmi = lmi,
        rent_by_year = rent_by_year,
        invested_balances = invested_balances,
    )

    for row in yearly_breakdown:
        print(f"Year {row['year']}: buy ${row['buy_wealth']:,.2f}  rent ${row['rent_wealth']:,.2f}")
    if breakeven_year is None:
        print("Buying never overtakes renting within the horizon")
    else:
        print(f"Breakeven year: {breakeven_year}")
