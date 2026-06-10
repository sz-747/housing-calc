import csv
import os

class SuburbDataService:
    # this reads suburb data from suburb.csv
    
    def __init__(self, csv_path = None):
        if csv_path is None:
            csv_path = os.path.join(os.path.dirname(__file__), "suburbs.csv")
        self._csv_path = csv_path
        self._surburbs = None
        
    def get_suburb(self, name):
        # this returns the data dictionary for one subrub or raise error
        data = self._load()
        if name not in data:
            raise ValueError(f"Suburb '{name}' not found")
        return data[name]
    
    def list_suburbs(self):
        #this returns a sorted list of all suburb names
        return sorted(self._load().keys())
    
    #come back here with load csv and parsing