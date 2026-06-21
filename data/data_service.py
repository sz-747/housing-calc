import csv
import os

class SuburbDataService:
    # this reads suburb data from suburb.csv
    
    def __init__(self, csv_path = None):
        if csv_path is None:
            csv_path = os.path.join(os.path.dirname(__file__), "suburbs.csv")
        self._csv_path = csv_path
        self._suburbs = None
        
    def get_suburb(self, name):
        # this returns the data dictionary for one subrub or raise error
        data = self._load()
        if name not in data:
            raise ValueError(f"Suburb '{name}' not found")
        return data[name]
    
    def list_suburbs(self):
        #this returns a sorted list of all suburb names
        return sorted(self._load().keys())
    
    def _load(self):
        # this loads csv on first call and returns cached data
        if self._suburbs is None:
            self._suburbs = self._read_csv()
        return self._suburbs
    
    def _read_csv(self):
        # parse surburbs.csv into a dict keyed by suburb name
        suburbs = {}
        with open(self._csv_path, encoding="utf-8", newline="") as file:
            reader = csv.DictReader(file)
            for row in reader:
                suburb = row.get("suburb", "").strip()
                # skip blank rows and repeated header rows
                if suburb == "" or suburb == "suburb":
                    continue
                try:
                    suburbs[suburb] = {
                        "suburb": suburb,
                        "median_house": self._parse_float(row, "median_house"),
                        "median_unit": self._parse_float(row, "median_unit"),
                        "weekly_rent_house": self._parse_float(row, "weekly_rent_house"),
                        "weekly_rent_unit": self._parse_float(row, "weekly_rent_unit"),
                        "growth_rate": self._parse_float(row, "growth_rate"),
                    }
                except ValueError:
                    continue #skip rows with incomplete data
                
            if not suburbs:
                raise ValueError("no suburb records found in suburb.csv")
            return suburbs
        
    def _parse_float(self, row, key):
        raw = row.get(key, "").strip()
        if raw == "":
            raise ValueError(f"Missing numeric field in CSV: {key}")
        try:
            return float(raw)
        except ValueError as exc:
            # Keep the original conversion error attached to the new error
            raise ValueError(f"Invalid numeric field in csv: {key}") from exc