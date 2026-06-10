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