# Annual rent projection - compounding growth.


WEEKS_PER_YEAR = 52


def calculate_rent_projection(weekly_rent: float, years: int, annual_growth: float) -> list:
    if weekly_rent <= 0:
        raise ValueError("weekly_rent must be positive")
    if years <= 0:
        raise ValueError("years must be positive")
    if annual_growth < 0:
        raise ValueError("annual_growth must be non-negative")

    first_year_rent = weekly_rent * WEEKS_PER_YEAR

    yearly_rent = []
    current_rent = first_year_rent
    for year_number in range(years):
        yearly_rent.append(round(current_rent, 2))
        current_rent = current_rent * (1 + annual_growth)

    return yearly_rent


if __name__ == "__main__":
    weekly_rent = float(input("Enter weekly rent: "))
    years = int(input("Enter number of years: "))
    annual_growth = float(input("Enter annual rent growth rate (e.g. 0.03): "))
    yearly_rent = calculate_rent_projection(weekly_rent, years, annual_growth)
    for year_index in range(len(yearly_rent)):
        year = year_index + 1
        print(f"Year {year}: ${yearly_rent[year_index]:,.2f}")
