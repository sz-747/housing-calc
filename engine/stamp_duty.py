"""NSW stamp duty - bracket based transfer duty.

Stamp duty is a one-off tax paid to the NSW government when a property is
bought. It is worked out in brackets. Firstly a fixed amount up to a threshold, then a
percentage of the part of the price above that threshold. 
"""


def calculate_stamp_duty(price: float) -> float:
    """Return the NSW stamp duty owed on a property price.

    Args:
        price: Purchase price in AUD. Must be > 0.

    Returns:
        The stamp duty owed in AUD, rounded to the nearest cent.

    Raises:
        ValueError: if price is not positive.
    """
    if price <= 0:
        raise ValueError("price must be positive")

    if price <= 1_033_000:
        duty = 9_805 + 0.045 * (price - 310_000)
    else:
        duty = 42_340 + 0.055 * (price - 1_033_000)

    return round(duty, 2)


if __name__ == "__main__":
    price = float(input("Enter property price: "))
    duty = calculate_stamp_duty(price)
    print(f"Stamp duty on ${price:,.2f} is ${duty:,.2f}")
