@echo off
REM Dominus - start script for Windows

REM Create the virtual environment the first time only, then install Flask.
if not exist venv (
    python -m venv venv
    venv\Scripts\pip install -r requirements.txt
)

REM Start the Flask app. Open http://127.0.0.1:5000 in a browser.
venv\Scripts\python app.py
