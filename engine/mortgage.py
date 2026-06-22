# Monthly mortgage repayment - standard amortisation formula.

"""
Formula: M = P * r * (1 + r)^n / ((1 + r)^n - 1)
    M = monthly repayment
    P = loan principal
    r = monthly interest rate (annual rate / 12)
    n = total number of monthly repayments (years * 12)
"""


def calculate_monthly_payment(principal: float, annual_rate: float, years: int) -> float:
    """Return the fixed monthly repayment on a principal and interest loan.

    Uses amortisation formula above to find the level repayment that pays the loan off exactly over its term.

    Args:
        principal: Amount borrowed in AUD. Must be > 0.
        annual_rate: Annual interest rate as a fraction (0.0609 = 6.09%).
            Tis must be > 0.
        years: Loan term in years. Must be > 0.

    Returns:
        The monthly repayment in AUD, rounded to the nearest cent.

    Raises:
        ValueError: if any argument is not positive.
    """
    if principal <= 0:
        raise ValueError("principal must be positive")
    if annual_rate <= 0:
        raise ValueError("annual_rate must be positive")
    if years <= 0:
        raise ValueError("years must be positive")

    monthly_rate = annual_rate / 12
    number_of_payments = years * 12

    growth_factor = (1 + monthly_rate) ** number_of_payments

    numerator = principal * monthly_rate * growth_factor
    denominator = growth_factor - 1
    monthly_payment = numerator / denominator

    return round(monthly_payment, 2)


if __name__ == "__main__":
    principal = float(input("Enter loan amount: "))
    annual_rate = float(input("Enter annual interest rate (e.g. 0.06): "))
    years = int(input("Enter loan term in years: "))
    monthly_payment = calculate_monthly_payment(principal, annual_rate, years)
    print(f"Monthly repayment on ${principal:,.2f} is ${monthly_payment:,.2f}")
