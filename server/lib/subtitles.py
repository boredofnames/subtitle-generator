import datetime
import re


def offset_time_string(time_string, seconds):
    """This function takes a time string and an integer representing seconds to be added to it, then returns the new time string.
    The input time string is in the format 'HH:MM:SS.fff', where HH is hours, MM is minutes, SS is seconds, and fff is milliseconds.
    """
    try:
        time = datetime.datetime.strptime(time_string, "%H:%M:%S.%f")
    except ValueError:
        time = datetime.datetime.strptime(time_string, "%M:%S.%f")
    except:
        raise Exception("Unreadable time_string in vtt")
    new_time = time + datetime.timedelta(seconds=seconds)
    return new_time.strftime("%H:%M:%S.%f")[:-3]


def offset(sub, offset=0):
    match_rx = (
        r"((?:\d+:)?\d{2}:\d{2}\.\d{3}) --> ((?:\d+:)?\d{2}:\d{2}\.\d{3})\r?\n(.+)"
    )
    cues = re.findall(match_rx, sub)
    cues = [
        [offset_time_string(cue[0], offset), offset_time_string(cue[1], offset), cue[2]]
        for cue in cues
    ]
    cues = [
        "{} --> {}\n{}\n".format(cue[0], cue[1], cue[2]) for i, cue in enumerate(cues)
    ]
    return "\n".join(cues)


if __name__ == "__main__":
    print(offset_time_string("01:00:50.000", 10.5))
    print(offset_time_string("59:50.000", 10.5))
