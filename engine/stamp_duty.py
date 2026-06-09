def calculate_stamp_duty(price: float) -> float:
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
