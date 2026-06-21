class UserInput:
    # this is for the validated parsed inputs from the comparisson form
    
    def __init__(
        self,
        suburb,
        annual_income,
        deposit,
        property_type,
        horizon,
        mortgage_rate,
        return_rate,
        loan_term_years,
    ):
        self.suburb = suburb
        self.annual_income = annual_income
        self.deposit = deposit
        self.property_type = property_type
        self.horizon = horizon
        self.mortgage_rate = mortgage_rate
        self.return_rate = return_rate
        self.loan_term_years = loan_term_years
        
    @classmethod #e.g. can do UserInput.from_form(form) without first creating UserInput
    def from_form(cls, form): 
        suburb = form.get("suburb", "").strip()
        if suburb == "":
            raise ValueError("choose a suburb")
        
        annual_income = UserInput._parse_positive_float(form, "annual_income", "Annual income")
        deposit = UserInput._parse_positive_float(form, "deposit", "Deposit")
        
        property_type = form.get("property_type", "").strip().lower()
        if property_type not in {"house", "unit"}:
            raise ValueError("Property type must be house or unit")
        
        horizon = UserInput._parse_positive_int(form, "horizon", "Time horizon")
        mortgage_rate = UserInput._parse_positive_float(form, "mortgage_rate", "Mortgage rate") / 100.0
        return_rate = UserInput._parse_nonneg_float(form, "return_rate", "Investment return rate") / 100.0
        loan_term_years = UserInput._parse_positive_int(form, "loan_term_years", "Loan term")

        return UserInput(
            suburb=suburb,
            annual_income=annual_income,
            deposit=deposit,
            property_type=property_type,
            horizon=horizon,
            mortgage_rate=mortgage_rate,
            return_rate=return_rate,
            loan_term_years=loan_term_years,
        )
    
    def to_dict(self): #this is for calc engine.run - return inputs as plain dict
        return {
            "annual_income": self.annual_income,
            "deposit": self.deposit,
            "property_type": self.property_type,
            "horizon": self.horizon,
            "mortgage_rate": self.mortgage_rate,
            "return_rate": self.return_rate,
            "loan_term_years": self.loan_term_years,
        }
        
    @staticmethod #take value from form to make sure its positive
    def _parse_positive_float(form, key, label):
        raw = form.get(key, "").strip()
        if raw == "":
            raise ValueError(f"{label} is required")
        try:
            value = float(raw)
        except ValueError:
            raise ValueError(f"{label} must be a number")
        if value <= 0:
            raise ValueError(f"{label} must be bigger than 0")
        return value
    
    @staticmethod #same thing but for non negs
    def _parse_nonneg_float(form, key, label):
        raw = form.get(key, "").strip()
        if raw == "":
            raise ValueError(f"{label} is required")
        try:
            value = float(raw)
        except ValueError:
            raise ValueError(f"{label} must be a number")
        if value < 0:
            raise ValueError(f"{label} must be 0 or more")
        return value
    
    @staticmethod
    def _parse_positive_int(form, key, label):
        raw = form.get(key, "").strip()
        if raw == "":
            raise ValueError(f"{label} is required")
        try:
            value = int(raw)
        except ValueError:
            raise ValueError(f"{label} must be whole number")
        if value < 1:
            raise ValueError(f"{label} must be at least 1")
        return value
    
class ComparisonResult:
    # this wraps the dict returned by CalcEngine.run for use in templates

    def __init__(self, data):
        self.verdict = data["verdict"]
        self.summary = data["summary"]
        self.buy_projection = data["buy_projection"]
        self.rent_projection = data["rent_projection"]
        self.yearly_breakdown = data["yearly_breakdown"]
        self.breakeven_year = data["breakeven_year"]
        self.affordability = data["affordability"]

    def explanation(self):
        upfront = self.summary["stamp_duty"] + self.summary["lmi"]
        gap = abs(self.summary["net_difference"])
        buy_w = self.summary["buy_wealth"]
        rent_w = self.summary["rent_wealth"]
        growth_rate = self.summary["property_growth_rate"] * 100

        if self.verdict == "buying":
            first = f"Buying wins here. You come out ${gap:,.0f} better off compared to renting."
            if upfront > gap * 0.4:
                second = f"Yeah, you fork out ${upfront:,.0f} upfront in stamp duty and LMI, but your property clocking {growth_rate:.1f}% growth a year stacks your wealth up to ${buy_w:,.0f}. That smashes the ${rent_w:,.0f} you'd end up with if you just rented and chucked your deposit in the market."
            else:
                second = f"Your property clocking {growth_rate:.1f}% growth a year stacks your wealth up to ${buy_w:,.0f}. That smashes the ${rent_w:,.0f} you'd end up with if you just rented and chucked your deposit in the market."
        elif self.verdict == "renting":
            first = f"Renting wins here. You come out ${gap:,.0f} better off compared to buying."
            second = f"Buying hits you with ${upfront:,.0f} upfront in stamp duty and LMI before you even start paying off the mortgage. That drags your buy wealth down to ${buy_w:,.0f}, while renting and investing your deposit quietly builds to ${rent_w:,.0f}."
        else:
            first = "Honestly, it's a coin flip. Buying and renting come out pretty much the same."
            second = f"Buying lands at ${buy_w:,.0f}, renting lands at ${rent_w:,.0f}, only ${gap:,.0f} in it. Tweak your assumed growth rate or investment return and the answer could easily flip."

        return f"{first} {second}"

    def to_dict(self):
        #this returns the result as a plain dict for scenario stage save
        return {
        "verdict": self.verdict,
        "summary": self.summary,
        "buy_projection": self.buy_projection,
        "rent_projection": self.rent_projection,
        "yearly_breakdown": self.yearly_breakdown,
        "breakeven_year": self.breakeven_year,
        "affordability": self.affordability,
    }