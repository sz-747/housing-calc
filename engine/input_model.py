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
        return_rate_,
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
            raise ValueError("Property type must be house or unit.")
        
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