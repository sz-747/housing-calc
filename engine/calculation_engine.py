from engine.breakeven import find_breakeven
from engine.lmi import calculate_lmi
from engine.mortgage import calculate_monthly_payment
from engine.mortgage_balance import calculate_mortgage_balance
from engine.opportunity_cost import calculate_opportunity_cost
from engine.property_value import calculate_property_value
from engine.rent_projection import calculate_rent_projection
from engine.stamp_duty import calculate_stamp_duty
from engine.borrowing_power import assess_borrowing_power

ANNUAL_RENTAL_GROWTH_RATE = 0.03
ANNUAL_OWNERSHIP_COST_RATE = 0.01
MARGINAL_VERDICT_THRESHOLD = 0.05


class CalculationEngine:
    def run(self, user_inputs, suburb_data):
        self._assert_dict(user_inputs, "user_inputs")
        self._assert_dict(suburb_data, "suburb_data")

        annual_income = self._read_float(
            user_inputs, ("annual_income", "income"), "annual income", min_value=1.0
        )
        deposit = self._read_float(
            user_inputs, ("deposit", "savings"), "deposit/savings", min_value=0.0
        )
        property_type = self._read_property_type(
            self._read_any(user_inputs, ("property_type", "home_type"), "property_type")
        )
        years = self._read_int(
            user_inputs, ("horizon", "years"), "time horizon", min_value=1
        )
        mortgage_rate = self._read_float(
            user_inputs,
            ("mortgage_rate", "interest_rate"),
            "mortgage rate",
            min_value=0.0001,
        )
        return_rate = self._read_float(
            user_inputs,
            ("return_rate", "investment_return_rate"),
            "investment return rate",
            default=0.07,
            min_value=0.0,
        )
        loan_term_years = self._read_int(
            user_inputs,
            ("loan_term_years", "loan_term"),
            "loan term (years)",
            min_value=1,
            default=30,
        )

        property_price = self._read_float(
            suburb_data,
            (f"median_{property_type}",),
            "property price",
        )
        weekly_rent = self._read_float(
            suburb_data, (f"weekly_rent_{property_type}",), "weekly rent"
        )
        property_growth = self._read_float(
            suburb_data,
            ("growth_rate", "property_growth_rate"),
            "property growth rate",
            default=ANNUAL_RENTAL_GROWTH_RATE,
            min_value=0.0,
        )
        rent_growth = self._read_float(
            suburb_data,
            ("rent_growth_rate",),
            "rent growth rate",
            default=ANNUAL_RENTAL_GROWTH_RATE,
            min_value=0.0,
        )

        loan_amount = self._derive_loan_amount(
            property_price, deposit, suburb_data
        )
        if loan_term_years < years:
            raise ValueError("loan term must be at least the comparison horizon")

        stamp_duty = calculate_stamp_duty(property_price)
        lmi = calculate_lmi(property_price, deposit)
        monthly_payment = calculate_monthly_payment(
            loan_amount, mortgage_rate, loan_term_years
        )

        property_values = calculate_property_value(
            property_price, years, property_growth
        )
        mortgage_balances = calculate_mortgage_balance(
            loan_amount, mortgage_rate, loan_term_years, years
        )
        rent_by_year = calculate_rent_projection(
            weekly_rent, years, rent_growth
        )
        invested_balances = calculate_opportunity_cost(
            deposit, years, return_rate
        )

        breakeven_year, yearly_breakdown = find_breakeven(
            property_values = property_values,
            mortgage_balances = mortgage_balances,
            monthly_payment = monthly_payment,
            deposit = deposit,
            stamp_duty = stamp_duty,
            lmi = lmi,
            rent_by_year = rent_by_year,
            invested_balances = invested_balances,
        )

        buy_projection = self._build_buy_projection(
            years = years,
            property_values = property_values,
            mortgage_balances = mortgage_balances,
            monthly_payment = monthly_payment,
            deposit = deposit,
            stamp_duty = stamp_duty,
            lmi = lmi,
            property_type = property_type,
        )
        rent_projection = self._build_rent_projection(
            years = years,
            rent_by_year = rent_by_year,
            invested_balances = invested_balances,
        )
        summary = self._build_summary(
            yearly_breakdown = yearly_breakdown,
            rent_by_year = rent_by_year,
            property_price = property_price,
            deposit = deposit,
            annual_income = annual_income,
            mortgage_rate = mortgage_rate,
            return_rate = return_rate,
            property_growth = property_growth,
            rent_growth = rent_growth,
            stamp_duty = stamp_duty,
            lmi = lmi,
            monthly_payment = monthly_payment,
            property_type = property_type,
            loan_amount = loan_amount,
        )
        verdict = self._decide_verdict(yearly_breakdown)
        affordability = assess_borrowing_power(
            annual_income = annual_income,
            deposit = deposit,
            price = property_price,
        )

        return {
            "buy_projection": buy_projection,
            "rent_projection": rent_projection,
            "yearly_breakdown": yearly_breakdown,
            "breakeven_year": breakeven_year,
            "verdict": verdict,
            "summary": summary,
            "affordability": affordability,
        }

    def _derive_loan_amount(
        self,
        property_price,
        deposit,
        suburb_data,
    ):
        if deposit < 0:
            raise ValueError("deposit must be non-negative")
        if property_price <= 0:
            raise ValueError("property price must be positive")
        if deposit >= property_price:
            raise ValueError("deposit must be less than property price")
        if suburb_data.get("min_deposit") is not None:
            min_deposit = self._read_float(
                suburb_data, ("min_deposit",), "minimum deposit", min_value = 0.0
            )
            if deposit < min_deposit:
                raise ValueError(f"deposit must be at least {min_deposit}")
        return property_price - deposit
    
    def _build_buy_projection(
        self,
        years,
        property_values,
        mortgage_balances,
        monthly_payment,
        deposit,
        stamp_duty,
        lmi,
        property_type,
    ):
        annual_payment = monthly_payment * 12
        cumulative_mortgage_paid = 0.0
        cumulative_ownership_cost = 0.0
        rows = []
        for year_index in range(years):
            year = year_index + 1
            property_value = property_values[year_index]
            mortgage_balance = mortgage_balances[year_index]
            equity = property_value - mortgage_balance
            annual_ownership_cost = property_value * ANNUAL_OWNERSHIP_COST_RATE
            cumulative_ownership_cost = cumulative_ownership_cost + annual_ownership_cost
            cumulative_mortgage_paid = cumulative_mortgage_paid + annual_payment
            cumulative_buy_cash = (deposit + stamp_duty + lmi + cumulative_mortgage_paid + cumulative_ownership_cost)
            buy_wealth = equity - cumulative_buy_cash
            net_cashflow = annual_payment + annual_ownership_cost
            rows.append({
                "year": year, 
                "property_value": round(property_value, 2),
                "mortgage_balance": round(property_value, 2),
                "buy_wealth": round(buy_wealth, 2),
                "monthly_payment": round(monthly_payment, 2),
                "net_cashflow": round(net_cashflow, 2),
                "cumulative_cashflow": round(cumulative_buy_cash, 2),
            })
        return rows
    
    def _build_rent_projection(self, years, rent_by_year, invested_balances):
        cumulative_rent_paid = 0.0
        rows = []
        for year_index in range(years):
            year = year_index + 1
            annual_rent = rent_by_year[year_index]
            cumulative_rent_paid = cumulative_rent_paid + annual_rent
            invested_value = invested_balances[year_index]
            rent_wealth = invested_value - cumulative_rent_paid
            rows.append({
                "year": year,
                "annual_rent": round(annual_rent, 2).
                "cumulative_rent_paid": round(cumulative_rent_paid, 2),
                "rent_wealth": round(rent_wealth, 2),
                "net_cashflow": round(annual_rent, 2),
            })
        return rows
    
    def _build_summary(
        self, 
        yearly_breakdown,
        rent_by_year,
        property_price,
        deposit,
        annual_income,
        mortgage_rate,
        return_rate,
        property_growth,
        rent_growth,
        stamp_duty,
        lmi,
        monthly_payment,
        property_type,
        loan_amount,
    ):
        
        final_year = yearly_breakdown[-1]
        buy_wealth = final_year["buy_wealth"]
        rent_wealth = final_year["rent_wealth"]
        return {
            "property_type": property_type
            "loan_amount": round(loan_amount, 2),
            "annual_payment": round(monthly_payment * 12, 2),
            "first_year_monthly_rent_estimate": round(rent_by_year[0] / 12, 2),
            "property_growth_rate": property_growth,
            "rent_growth_rate": rent_growth,
            "annual_ownership_cost_rate": ANNUAL_OWNERSHIP_COST_RATE,
            "buy_wealth": round(buy_wealth, 2),
            "rent_wealth": round(rent_wealth, 2),
            "net_difference": round(buy_wealth - rent_wealth, 2),
            "monthly_payment": round(monthly_payment, 2),
            "stamp_duty": round(stamp_duty, 2),
            "lmi": round(lmi, 2),
        }
        
    def _decide_verdict(self, yearly_breakdown):
        final_year = yearly_breakdown[-1]
        buy = final_year["buy_wealth"]
        rent = final_year["rent_wealth"]
        larger = max(abs(buy), abs(rent))
        if larger == 0:
            return "marginal"
        diff_pct = abs(buy - rent) / larger
        if diff_pct < MARGINAL_VERDICT_THRESHOLD:
            return "marginal"
        if buy > rent:
            return "buying"
        return "renting"
    
# these are js some helper methods for reading typed values from dicts

def _assert_dict(self, obj, name):
    if not isinstance(obj, dict):
        raise ValueError(f"{name} must be a dict")
    
    # this raises a value error if obj isn't a dict
    # called at the top of run() to catch callers who pass the wrong type before anything else happens

def _read_float(self, source, keys, label, default=None):
    #this reads a float from source using the first matching key in keys
    
    value = None
    for key in keys:
        if key in source:
            value = source[key]
            break
    if value is None:
        if default is not None:
            return default
        raise ValueError(f"{label} is required")
    try:
        value = float(value)
    except (TypeError, ValueError):
        raise ValueError(f"{label} must be a number")
    if min_value is not None and value < min_value:
        raise ValueError(f"{label} must be at least {min_value}")
    return value

