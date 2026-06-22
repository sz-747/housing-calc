# Property value projection - compounding capital growth.



def calculate_property_value(price: float, years: int, annual_growth: float) -> list:
    if price <= 0:
        raise ValueError("price must be positive")
    if years <= 0:
        raise ValueError("years must be positive")

    yearly_value = []
    current_value = price
    for year_number in range(years):
        current_value = current_value * (1 + annual_growth)
        yearly_value.append(round(current_value, 2))

    return yearly_value


if __name__ == "__main__":
    price = float(input("Enter property price: "))
    years = int(input("Enter number of years: "))
    annual_growth = float(input("Enter annual growth rate (e.g. 0.05): "))
    values = calculate_property_value(price, years, annual_growth)
    for year_index in range(len(values)):
        year = year_index + 1
        print(f"Year {year}: ${values[year_index]:,.2f}")
