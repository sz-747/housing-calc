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
        suburbs=list_suburbs(),
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
            error=str(error),
        )
    
    return render_template(
        "results.html",
        suburb=user_input.suburb,
        result=result,
        inputs=user_input.to_dict(),
    )

@app.route("/compare", methods=["GET"])
def compare_get_redirect():
    return redirect(url_for("home"))


@app.route("/learn")
def learn():
    return render_template("learn.html")


app.jinja_env.filters["money"] = _format_money


if __name__ == "__main__":
    app.run(debug=True)
