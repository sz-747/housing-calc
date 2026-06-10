class InputValidator:
    # this validates raw data before parsing
    
    def __init__(self):
        self._errors = []
    
    def validate(self, form_data, valid_suburbs):
        # this needs to return true if all fields are valid
        self._errors = []
        suburb = form_data.get("suburb", "").strip()
        if suburb == "":
            self._errors.append("choose a suburb")
        elif suburb not in valid_suburbs:
            self._errors.append("choose a valid suburb from the list")
            
        property_type = form_data.get("property_type", "").strip().lower()
        if property_type not in {"house", "unit"}:
            self._errors.append("type of property needs to be house or unit")
            
        self._check_positive_number(form_data, "annual_income", "Annual income")
        self._check_positive_number(form_data, "deposit", "Deposit")
        self._check_positive_integer(form_data, "horizon", "Time horizon")
        self._check_positive_number(form_data, "mortgage_rate", "Mortgage rate")
        self._check_positive_integer(form_data, "loan_term_years", "Loan term")
        self._check_nonneg_number(form_data, "return_rate", "Investment return rate")
        
        return len(self._errors) == 0
    
    def get_errors(self):
        return list(self._errors)