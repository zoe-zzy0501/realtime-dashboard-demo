#!/bin/zsh

cd "$(dirname "$0")"

PYTHON="/Library/Frameworks/Python.framework/Versions/3.12/bin/python3"

if [ ! -x "$PYTHON" ]; then
    PYTHON="python3"
fi

if [ ! -d ".dashboard_env" ]; then
    "$PYTHON" -m venv .dashboard_env
fi

.dashboard_env/bin/python -m pip install --upgrade pip
.dashboard_env/bin/python -m pip install -r requirements.txt
.dashboard_env/bin/python -m streamlit run app.py --browser.gatherUsageStats false
