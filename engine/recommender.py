"""Suburb recommender - rank every suburb by buy vs rent outcome.

The recommender runs the existing calculation engine once for each suburb,
using the same financial inputs each time, and lines the suburbs up best buy
outcome first. 
"""


def _net_difference_of(result_row):
    """Sort key: pull the net difference out of one ranked result row."""
    return result_row["net_difference"]


def rank_suburbs(engine, financial_inputs, all_suburbs):
    """Rank every suburb by buy vs rent outcome for one user's financials.

    Args:
        engine: A CalculationEngine whose run(inputs, suburb_data) is called.
        financial_inputs: The inputs dict engine.run expects (no suburb).
        all_suburbs: The suburb dict keyed by suburb name.

    Returns:
        A dict with ranked list of per suburb result dicts, best buy first and skipped which is count of suburbs that could not be evaluated.
    """
    ranked = []
    skipped = 0

    for suburb_name in all_suburbs:
        suburb_data = all_suburbs[suburb_name]
        try:
            result = engine.run(financial_inputs, suburb_data)
        except (ValueError, OverflowError):
            # a suburb that cannot be evaluated (deposit bigger than the price, or numbers too large to calculate) - skip it and keep going rather than crash
            skipped += 1
            continue

        summary = result["summary"]
        ranked.append({
            "suburb": suburb_name,
            "verdict": result["verdict"],
            "net_difference": summary["net_difference"],
            "buy_wealth": summary["buy_wealth"],
            "rent_wealth": summary["rent_wealth"],
            "breakeven_year": result["breakeven_year"],
        })

    ranked.sort(key=_net_difference_of, reverse=True)
    return {"ranked": ranked, "skipped": skipped}
