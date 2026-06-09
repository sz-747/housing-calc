import csv


def load_suburbs(csv_path="data/suburbs.csv"):
    suburbs = {}
    with open(csv_path, encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            parsed = _parse_row(row)
            suburb = parsed["suburb"]
            suburbs[suburb] = parsed

    if not suburbs:
        raise ValueError("No suburb records found in CSV file.")
    return suburbs


def _parse_row(row):
    suburb = row.get("suburb", "").strip()
    if suburb == "":
        raise ValueError("Missing suburb field in CSV row.")

    return {
        "suburb": suburb,
        "median_house": _parse_float(row, "median_house"),
        "median_unit": _parse_float(row, "median_unit"),
        "weekly_rent_house": _parse_float(row, "weekly_rent_house"),
        "weekly_rent_unit": _parse_float(row, "weekly_rent_unit"),
        "growth_rate": _parse_float(row, "growth_rate"),
    }


def get_suburb(name):
    data = _get_market_data()
    if name not in data:
        raise ValueError("Suburb not found.")
    return data[name]


def list_suburbs():
    return sorted(_get_market_data().keys())


def _parse_float(row, key):
    raw = row.get(key, "").strip()
    if raw == "":
        raise ValueError(f"Missing numeric field: {key}")
    try:
        return float(raw)
    except ValueError as exc:
        raise ValueError(f"Invalid numeric field: {key}") from exc


_MARKET_DATA = None


def _get_market_data():
    global _MARKET_DATA
    if _MARKET_DATA is None:
        _MARKET_DATA = load_suburbs("data/suburbs.csv")
    return _MARKET_DATA
