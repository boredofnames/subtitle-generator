#!/bin/bash

VENV_PATH="./venv"

if [ ! -d "$VENV_PATH" ]; then
  echo "$VENV_PATH doesn't exist. Creating virtual environment.."
  python3 -m venv ./venv
fi

source ./venv/bin/activate
./venv/bin/python3 -m pip install -r requirements.txt