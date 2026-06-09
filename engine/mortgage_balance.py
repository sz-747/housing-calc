# Remaining mortgage balance at the end of each year.

from engine.mortgage import calculate_monthly_payment

MONTHS_PER_YEAR = 12


def calculate_mortgage_balance(
    principal: float, annual_rate: float, loan_term_years: int, horizon_years: int
) -> list:
    if principal <= 0:
        raise ValueError("principal must be positive")
    if annual_rate <= 0:
        raise ValueError("annual_rate must be positive")
    if loan_term_years <= 0:
        raise ValueError("loan_term_years must be positive")
    if horizon_years <= 0:
        raise ValueError("horizon_years must be positive")
    if horizon_years > loan_term_years:
        raise ValueError("horizon_years must not exceed loan_term_years")

    monthly_payment = calculate_monthly_payment(principal, annual_rate, loan_term_years)
    monthly_rate = annual_rate / MONTHS_PER_YEAR

    balances = []
    remaining = principal
    for year_number in range(horizon_years):
        for month_number in range(MONTHS_PER_YEAR):
            interest = remaining * monthly_rate
            remaining = remaining + interest - monthly_payment
        balances.append(round(remaining, 2))

    return balances


if __name__ == "__main__":
    principal = float(input("Enter loan amount: "))
    annual_rate = float(input("Enter annual interest rate (e.g. 0.06): "))
    loan_term_years = int(input("Enter loan term in years: "))
    horizon_years = int(input("Enter number of years to show: "))
    balances = calculate_mortgage_balance(principal, annual_rate, loan_term_years, horizon_years)
    for year_index in range(len(balances)):
        year = year_index + 1
        print(f"Year {year}: ${balances[year_index]:,.2f} still owing")
