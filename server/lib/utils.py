from tomllib import load as load_config
from os.path import exists
from shutil import copy2
import datetime

if not exists("./config.toml"):
    if not exists("./config-example.toml"):
        raise OSError("Missing config-example.toml! Exiting.")
    copy2("./config-example.toml", "./config.toml")

with open("./config.toml", "rb") as f:
    config = load_config(f)


def get_config():
    return config


def time_string_to_double(time_str, offset=0):
    parts = time_str.split(":")
    if len(parts) < 3:
        parts.insert(0, "00")
    hours = int(parts[0])
    minutes = int(parts[1])
    seconds = int(parts[2].split(".")[0])
    f_seconds = int(parts[2].split(".")[1])
    total_seconds = (
        (hours * 60 * 60) + (minutes * 60) + seconds + f_seconds / 1000 + offset
    )
    return round(total_seconds, 3)


def double_to_time_string(double):
    timeString = datetime.datetime.utcfromtimestamp(double).strftime("%H:%M:%S.%f")[:-3]
    return timeString


def get_nearest(lst, K):
    return lst[min(range(len(lst)), key=lambda i: abs(lst[i] - K))]


def average(lst):
    return sum(lst) / len(lst)
