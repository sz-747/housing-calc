# Lenders Mortgage Insurance - tiered LVR lookup.



LMI_TIERS = (
    (0.80, 0.85, 0.010),
    (0.85, 0.90, 0.020),
    (0.90, 1.00, 0.028),
)


def calculate_lmi(price: float, deposit: float) -> float:
    
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
