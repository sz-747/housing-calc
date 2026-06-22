# Dominus

Dominus is a Sydney-focused rent-vs-buy decision tool for houses and apartments.
You enter your income, savings, deposit, time horizon and pick a suburb, and the
app works out whether buying or renting leaves you better off over that period. It
includes stamp duty, lenders mortgage insurance (LMI), the opportunity cost of your
deposit, and annual growth, then shows a year-by-year breakdown and the breakeven
year. If you leave the suburb blank it ranks every suburb for you instead.

## Requirements

- Python 3.11 or newer
- Flask

## Install and run

Double-click `run.bat`, or run it from a terminal:

```
run.bat
```

The first time it runs it creates a virtual environment and installs Flask, then
starts the app. After that it just starts the app.

To do it by hand instead:

```
python -m venv venv
venv\Scripts\pip install -r requirements.txt
venv\Scripts\python app.py
```

Then open `http://127.0.0.1:5000` in a browser.
