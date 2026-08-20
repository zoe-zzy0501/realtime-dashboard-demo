#!/bin/zsh

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR" || exit 1

# Prefer the Python version used to build the demo, then fall back to python3.
PYTHON="/Library/Frameworks/Python.framework/Versions/3.12/bin/python3"
VENV_DIR=".dashboard_env"

if [ ! -x "$PYTHON" ]; then
    PYTHON="python3"
fi

if [ ! -d "$VENV_DIR" ]; then
    "$PYTHON" -m venv "$VENV_DIR"
fi

"$VENV_DIR/bin/python" -m pip install --upgrade pip
"$VENV_DIR/bin/python" -m pip install -r requirements.txt
"$VENV_DIR/bin/python" -m streamlit run app.py --browser.gatherUsageStats false
