# Opportunity cost of the deposit - compounding investment return.


def calculate_opportunity_cost(deposit: float, years: int, annual_return: float) -> list:
    if deposit <= 0:
        raise ValueError("deposit must be positive")
    if years <= 0:
        raise ValueError("years must be positive")
    if annual_return < 0:
        raise ValueError("annual_return must be non-negative")

    yearly_balance = []
    current_balance = deposit
    for year_number in range(years):
        current_balance = current_balance * (1 + annual_return)
        yearly_balance.append(round(current_balance, 2))

    return yearly_balance


if __name__ == "__main__":
    deposit = float(input("Enter deposit: "))
    years = int(input("Enter number of years: "))
    annual_return = float(input("Enter annual return rate (e.g. 0.07): "))
    balances = calculate_opportunity_cost(deposit, years, annual_return)
    for year_index in range(len(balances)):
        year = year_index + 1
        print(f"Year {year}: ${balances[year_index]:,.2f}")
