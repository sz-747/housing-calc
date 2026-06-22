"""Lenders Mortgage Insurance - tiered LVR lookup.

LMI is a one-off premium a lender charges when the deposit is small (the loan
is a high share of the price, so the loan-to-value ratio or LVR is high). The
premium is looked up from a tier table: the higher the LVR, the higher the
rate charged on the loan. No LMI is owed once the deposit reaches 20% (LVR
80% or below).
"""


LMI_TIERS = (
    (0.80, 0.85, 0.010),
    (0.85, 0.90, 0.020),
    (0.90, 1.00, 0.028),
)


def calculate_lmi(price: float, deposit: float) -> float:
    """Return the LMI premium owed for a given price and deposit.

    Args:
        price: Purchase price in AUD. Must be > 0.
        deposit: Deposit in AUD. Must be >= 0 and less than ``price``.

    Returns:
        The LMI premium in AUD, rounded to the nearest cent. Returns 0.0 when
        the deposit is 20% or more (LVR <= 80%).

    Raises:
        ValueError: if price is not positive, deposit is negative, deposit is not less than price, or the LVR matches no tier.
    """
    if price <= 0:
        raise ValueError("price must be positive")
    if deposit < 0:
        raise ValueError("deposit must be non-negative")
    if deposit >= price:
        raise ValueError("deposit must be less than price (no loan needed)")

    loan = price - deposit
    lvr = loan / price

    if lvr <= 0.80:
        return 0.0

    for lower, upper, rate in LMI_TIERS:
        if lower < lvr <= upper:
            return round(loan * rate, 2)

    raise ValueError(f"LVR {lvr:.4f} did not match any LMI tier")


if __name__ == "__main__":
    price = float(input("Enter property price: "))
    deposit = float(input("Enter deposit: "))
    premium = calculate_lmi(price, deposit)
    print(f"LMI on ${price:,.2f} with ${deposit:,.2f} deposit is ${premium:,.2f}")
