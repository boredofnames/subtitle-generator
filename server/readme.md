# Pre

### Windows

- [python](https://python.org) (built with 3.12.5)
- [ffmpeg](https://ffmpeg.org)

# Easy Mode (scripts)

## Setup / Update

### Linux

first set permissions to execute script

```
chmod +x ./setup.sh
```

then run with

```
./setup.sh
```

### Windows

```
setup.bat
```

## Run

### Linux

first set permissions to execute script

```
chmod +x ./run.sh
```

then run with

```
./run.sh
```

### Windows

```
run.bat
```

# Hard Mode (manual)

## Setup venv

ensure you're in subtitle-generator/server

```
cd server
```

```
python3 -m venv ./venv
```

## Activate venv

### Linux

bash

```
source ./venv/bin/activate
```

fish

```
source ./venv/bin/activate.fish
```

etc. Other activate scripts can be found here for different shells.

### Windows

```
venv\Scripts\activate.bat
```

## Install requirements

### Linux

```
./venv/bin/python3 -m pip install -r requirements.txt
```

### Windows

```
venv\Scripts\python.exe -m pip install -r requirements.txt
```

## Run Manual

### Linux

```
./venv/bin/flask run
```

### Windows

```
.\venv\Scripts\flask.exe run
```

## Deactivate venv

```
deactivate
```
