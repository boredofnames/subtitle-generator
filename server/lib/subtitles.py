import datetime
import re
from lib.utils import time_string_to_double, double_to_time_string


def offset(sub, offset=0):
    match_rx = (
        r"((?:\d+:)?\d{2}:\d{2}\.\d{3}) --> ((?:\d+:)?\d{2}:\d{2}\.\d{3})\r?\n(.+)"
    )
    cues = re.findall(match_rx, sub)
    cues = [
        [
            double_to_time_string(time_string_to_double(cue[0], offset)),
            double_to_time_string(time_string_to_double(cue[1], offset)),
            cue[2],
        ]
        for cue in cues
    ]
    cues = [
        "{} --> {}\n{}\n".format(cue[0], cue[1], cue[2]) for i, cue in enumerate(cues)
    ]
    return "\n".join(cues)
