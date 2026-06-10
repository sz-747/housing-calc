import json
import os

class ScenarioStorage:
    # this saves and loads comparison results to or from a json file
    
    def __init__(self, storage_path=None):
        if storage_path is None:
            storage_path = os.path.join(os.path.dirname(__file__), "saved_scenarios.json")
            self._path = storage_path
            
    def save(self, suburb, inputs, result):
        #append one scenario to stoage file
        scenarios = self.load_all()
        scenarios.append({
            "suburb": suburb,
            "inputs": inputs,
            "result": result,
        })
        with open(self._path, "w", encoding="utf-8") as file:
            json.dump(scenarios, file, indent=2)
            
    def load_all(self):
        #returns all saved scenarios as a list of dicts
        if not os.path.exists(self._path):
            return []
        with open(self._path) as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return []
            