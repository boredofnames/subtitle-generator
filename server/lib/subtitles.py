import datetime
import re

def time_string_to_double(time_str, offset=0):
    parts = time_str.split(':')
    if(len(parts) < 3):
      parts.insert(0, "00")
    hours = int(parts[0])
    minutes = int(parts[1])
    seconds = int(parts[2].split('.')[0])
    f_seconds = int(parts[2].split('.')[1])
    total_seconds = (hours * 60 * 60) + (minutes * 60) + seconds + f_seconds/1000 + offset
    return round(total_seconds, 3)

def double_to_time_string(double):
    timeString = datetime.datetime.utcfromtimestamp(double).strftime('%H:%M:%S.%f')[:-3]
    return timeString

def offset(sub, offset=0):
    match_rx = r'((?:\d+:)?\d{2}:\d{2}\.\d{3}) --> ((?:\d+:)?\d{2}:\d{2}\.\d{3})\r?\n(.+)'
    cues = re.findall(match_rx, sub)
    cues = [[double_to_time_string(time_string_to_double(cue[0], offset)), double_to_time_string(time_string_to_double(cue[1], offset)), cue[2]] for cue in cues]
    cues = ['{} --> {}\n{}\n'.format(cue[0], cue[1], cue[2]) for i, cue in enumerate(cues)]
    return '\n'.join(cues)