import subprocess
import webbrowser
import time
import os
import sys

# GET BASE DIRECTORY

if getattr(sys, "frozen", False):

    BASE_DIR = os.path.dirname(
        sys.executable
    )

else:

    BASE_DIR = os.path.dirname(
        os.path.abspath(__file__)
    )

# PYTHON EXE FROM VENV

PYTHON_EXE = os.path.join(
    BASE_DIR,
    "venv",
    "Scripts",
    "python.exe"
)

# APP PATH

APP_FILE = os.path.join(
    BASE_DIR,
    "app.py"
)

# START STREAMLIT

subprocess.Popen(
    [
        PYTHON_EXE,

        "-m",

        "streamlit",

        "run",

        APP_FILE,

        "--server.headless=true"
    ],
    cwd=BASE_DIR
)

# WAIT FOR SERVER

time.sleep(5)

# OPEN ONLY ONE TAB

webbrowser.open(
    "http://localhost:8501"
)