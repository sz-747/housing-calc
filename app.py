from flask import Flask, redirect, render_template, request, url_for

from data.data_service import SuburbDataService
from data.scenario_storage import ScenarioStorage
from engine import CalculationEngine
from engine.input_model import ComparisonResult, UserInput
from engine.validation import InputValidator

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True


ENGINE = CalculationEngine()


def _format_money(value):
    try:
        return f"${value:,.2f}"
    except (TypeError, ValueError):
        return "$0.00"


def _parse_float(form_data, key, label, *, allow_zero=False, min_value=0.0):
    raw = form_data.get(key, "").strip()
    if raw == "":
        raise ValueError(f"{label} is required.")
    try:
        value = float(raw)
    except ValueError as exc:
        raise ValueError(f"{label} must be a number.") from exc
    if value < min_value or (not allow_zero and value == 0):
        raise ValueError(f"{label} must be greater than 0.")
    return value


def _parse_int(form_data, key, label, *, min_value=1):
    raw = form_data.get(key, "").strip()
    if raw == "":
        raise ValueError(f"{label} is required.")
    try:
        value = int(raw)
    except ValueError as exc:
        raise ValueError(f"{label} must be an integer.") from exc
    if value < min_value:
        raise ValueError(f"{label} must be at least {min_value}.")
    return value


def _parse_percentage(form_data, key, label):
    value = _parse_float(form_data, key, label, min_value=0.0)
    return value / 100.0


def _parse_input(form_data):
    suburb = form_data.get("suburb", "").strip()
    if suburb == "":
        raise ValueError("Please choose a suburb.")
    if suburb not in list_suburbs():
        raise ValueError("Please choose a valid suburb from the list.")

    property_type = form_data.get("property_type", "").strip().lower()
    if property_type not in {"house", "unit"}:
        raise ValueError("Property type must be house or unit.")

    annual_income = _parse_float(form_data, "annual_income", "Annual income")
    deposit = _parse_float(form_data, "deposit", "Deposit")
    horizon = _parse_int(form_data, "horizon", "Time horizon", min_value=1)
    mortgage_rate = _parse_percentage(
        form_data, "mortgage_rate", "Mortgage rate (%)"
    )
    return_rate = _parse_percentage(
        form_data, "return_rate", "Investment return rate (%)"
    )
    loan_term_years = _parse_int(
        form_data, "loan_term_years", "Loan term (years)", min_value=1
    )

    user_inputs = {
        "annual_income": annual_income,
        "deposit": deposit,
        "property_type": property_type,
        "horizon": horizon,
        "mortgage_rate": mortgage_rate,
        "return_rate": return_rate,
        "loan_term_years": loan_term_years,
    }

    return suburb, user_inputs


@app.route("/", methods=["GET"])
def home():
    return render_template(
        "index.html",
        suburbs=list_suburbs(),
        form_data={},
        error=None,
    )


@app.route("/compare", methods=["POST"])
def compare():
    try:
        suburb, user_inputs = _parse_input(request.form)
        suburb_data = get_suburb(suburb)
        result = ENGINE.run(user_inputs, suburb_data)
    except ValueError as error:
        return render_template(
            "index.html",
            suburbs=list_suburbs(),
            form_data=request.form.to_dict(),
            error=str(error),
        )

    return render_template(
        "results.html",
        suburb=suburb,
        result=result,
        inputs=user_inputs,
    )


@app.route("/compare", methods=["GET"])
def compare_get_redirect():
    return redirect(url_for("home"))


app.jinja_env.filters["money"] = _format_money


if __name__ == "__main__":
    app.run(debug=True)
