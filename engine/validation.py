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
    
    def _check_positive_number(self, form_data, key, label):
        raw = form_data.get(key, "").strip()
        if raw == "":
            self._errors.append(f"{label} is required")
            return
        try:
            value = float(raw)
        except ValueError:
            self._errors.append(f"{label} must be a number")
            return
        if value <= 0:
            self._errors.append(f"{label} must be greater than zero")
            
            
    def _check_nonneg_number(self, form_data, key, label):
        raw = form_data.get(key, "").strip()
        if raw == "":
            self._errors.append(f"{label} is required.")
            return
        try:
            value = float(raw)
        except ValueError:
            self._errors.append(f"{label} must be a number.")
            return
        if value < 0:
            self._errors.append(f"{label} must be zero or more.")
            
    def _check_positive_integer(self, form_data, key, label):
        raw = form_data.get(key, "").strip()
        if raw == "":
            self._errors.append(f"{label} is required.")
            return
        try:
            value = int(raw)
        except ValueError:
            self._errors.append(f"{label} must be a whole number.")
            return
        if value < 1:
            self._errors.append(f"{label} must be at least 1.")