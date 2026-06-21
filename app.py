from flask import Flask, redirect, render_template, request, url_for

from data.data_service import SuburbDataService
from data.scenario_storage import ScenarioStorage
from engine import CalculationEngine
from engine.input_model import ComparisonResult, UserInput
from engine.validation import InputValidator

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

suburb_service = SuburbDataService()
storage = ScenarioStorage()
engine = CalculationEngine()

@app.route("/", methods=["GET"])
def home():
    return render_template(
        "index.html",
        suburbs=suburb_service.list_suburbs(),
        form_data={},
        error=None,
    )

@app.route("/compare", methods=["POST"])
def compare():
    form_data = request.form.to_dict()
    
    validator = InputValidator()
    if not validator.validate(request.form, suburb_service.list_suburbs()):
        return render_template(
            "index.html",
            suburbs=suburb_service.list_suburbs(),
            form_data=form_data,
            error=validator.errors[0],
        )
    
    user_input = UserInput.from_form(request.form)
    suburb_data = suburb_service.get_suburb(user_input.suburb)
    result = ComparisonResult(engine.run(user_input.to_dict(), suburb_data))

    storage.save(user_input.suburb, user_input.to_dict(), result.to_dict())

    return render_template(
        "results.html",
        suburb=user_input.suburb,
        result=result,
        inputs=user_input.to_dict(),
    )

@app.route("/compare", methods=["GET"])
def compare_get_redirect():
    return redirect(url_for("home"))


@app.route("/scenarios")
def scenarios():
    return render_template("scenarios.html", scenarios=storage.load_all())

@app.route("/scenarios/delete/<int:index>", methods=["POST"])
def delete_scenario(index):
    storage.delete(index)
    return redirect(url_for("scenarios"))

@app.route("/learn")
def learn():
    return render_template("learn.html")


def _format_money(value):
    return f"${value:,.2f}"

app.jinja_env.filters["money"] = _format_money


if __name__ == "__main__":
    app.run(debug=True)
