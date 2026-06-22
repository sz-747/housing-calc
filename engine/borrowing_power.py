"""Borrowing power - simple income-multiple affordability check.

A rough guide to how much a buyer can spend: lenders cap the loan at a multiple
of yearly income, then the most that can be paid is that loan plus the deposit.
"""

INCOME_MULTIPLIER = 6


def assess_borrowing_power(annual_income: float, deposit: float, price: float) -> dict:
    """Estimate whether a buyer can afford a property and by how much they miss.

    Args:
        annual_income: Gross yearly income in AUD. Must be > 0.
        deposit: Deposit in AUD. Must be >= 0.
        price: Property price in AUD. Must be > 0.

    Returns:
        A dictionary. 

    Raises:
        ValueError: if annual_income or pric is not positive, or if
            deposit is negative.
    """
    if annual_income <= 0:
        raise ValueError("annual_income must be positive")
    if deposit < 0:
        raise ValueError("deposit must be non-negative")
    if price <= 0:
        raise ValueError("price must be positive")

    max_borrow = annual_income * INCOME_MULTIPLIER
    max_purchase_price = deposit + max_borrow
    affordable = price <= max_purchase_price

    if affordable:
        shortfall = 0.0
        extra_deposit_needed = 0.0
        extra_income_needed = 0.0
    else:
        shortfall = price - max_purchase_price
        extra_deposit_needed = shortfall
        extra_income_needed = shortfall / INCOME_MULTIPLIER

    return {
        "affordable": affordable,
        "max_borrow": round(max_borrow, 2),
        "max_purchase_price": round(max_purchase_price, 2),
        "shortfall": round(shortfall, 2),
        "extra_deposit_needed": round(extra_deposit_needed, 2),
        "extra_income_needed": round(extra_income_needed, 2),
    }


if __name__ == "__main__":
    annual_income = float(input("Enter annual income: "))
    deposit = float(input("Enter deposit: "))
    price = float(input("Enter property price: "))
    result = assess_borrowing_power(annual_income, deposit, price)
    print(f"Max borrow: ${result['max_borrow']:,.2f}")
    print(f"Max purchase price: ${result['max_purchase_price']:,.2f}")
    if result["affordable"]:
        print("Affordable: yes")
    else:
        print("Affordable: no")
        print(f"Shortfall: ${result['shortfall']:,.2f}")
        print(f"Extra deposit needed: ${result['extra_deposit_needed']:,.2f}")
        print(f"Extra income needed: ${result['extra_income_needed']:,.2f}")
