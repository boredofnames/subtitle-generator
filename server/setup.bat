set VENV_PATH = ".\venv"

if not exist %VENV_PATH% (
  echo "$VENV_PATH doesn't exist. Creating virtual environment.."
  python3 -m venv %VENV_PATH%
)

.\venv\scripts\python.exe -m pip install -r requirements.txt
