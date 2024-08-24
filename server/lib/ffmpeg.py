from subprocess import run, check_output
import re
from json import loads
from os.path import exists
from lib.utils import get_nearest, double_to_time_string


def get_mean_volume(path):
    print("getting mean volume")
    output = run(
        f"ffmpeg -i {path} -filter:a volumedetect -hide_banner -f null /dev/null".split(
            " "
        ),
        capture_output=True,
    )
    match_rx = (
        r"\[Parsed_volumedetect_0 @ 0x[a-z0-9]+\]\smean_volume:\s(-?\d+\.?\d?)\sdB"
    )
    mean_volume = re.findall(match_rx, output.stderr.decode())
    return float(mean_volume[0])


def get_metadata(path):
    print("getting metadata")
    metadata = check_output(
        f"ffprobe -i {path} -v quiet -print_format json -show_format -hide_banner".split(
            " "
        )
    )
    print(metadata)
    metadata = loads(metadata)
    print(metadata)
    return metadata


def get_duration(path):
    print("getting duration")
    metadata = get_metadata(path)
    duration = float(metadata["format"]["duration"])
    print(f"Length of file is: {duration}")
    return duration


def get_silences(path, noise=-30, duration=0.25):
    print("getting silences")
    rx_match = r"silence_start:\s(\d+\.?\d*)"
    sd = "silencedetect=n=" + str(noise) + "dB:d=" + str(duration)
    command = ["ffmpeg", "-i", path, "-af", sd, "-f", "null", "-"]
    silence_process = run(command, capture_output=True)
    silence_out = silence_process.stderr.decode()
    silences = re.findall(rx_match, silence_out)
    silences = [float(silence) for silence in silences]
    return silences


def offset(value, offset):
    if value == 0 and offset < 0:
        return 0
    return value + offset


def segment(path, duration, output_name):
    print("segmenting video", path)
    if not exists(path):
        raise FileNotFoundError("File not found " + path)
    # segment the video file into chunks of specified duration
    segments = []
    file_duration = get_duration(path)
    print("file duration", file_duration)
    mean_volume = get_mean_volume(path=path)
    silences = get_silences(path=path, noise=mean_volume)
    current_time = 0
    segments_total_time = 0

    loop_number = 0
    while True:
        print(loop_number)
        next_silence = get_nearest(silences, current_time + duration)
        last_silence_item = silences[-1]
        last_end = segments[-1]["end"] if len(segments) > 0 else 0
        print(
            "next silence, last silence item, last end",
            next_silence,
            last_silence_item,
            last_end,
        )
        if next_silence is last_silence_item:
            segment_duration = file_duration - segments_total_time
            end = current_time + segment_duration
        else:
            end = next_silence
            segment_duration = next_silence - last_end
        start = current_time
        segments_total_time += segment_duration
        print(
            "segment duration, start, end, segments total time",
            segment_duration,
            start,
            end,
            segments_total_time,
        )
        segments.append(
            {
                "start": start,
                "end": end,
                "duration": segment_duration,
                "start_ts": double_to_time_string(start),
                "end_ts": double_to_time_string(end),
                "duration_ts": double_to_time_string(segment_duration),
            }
        )
        print("segments", segments)
        current_time = next_silence
        print("current time", current_time)
        silences.remove(next_silence)
        print("removed silence", next_silence)
        if next_silence is last_silence_item:
            print("hit last silence, breaking out")
            break
        loop_number += 1

    if segments_total_time != file_duration:
        print(
            "WARNING: total duration of video is not equal to the sum of segment durations",
            segments_total_time,
            file_duration,
        )
        print(segments)
        return

    segment_count = 0
    for segment in segments:
        output_path = (
            "./tmp/segments/" + output_name + "_" + str(segment_count).zfill(3) + ".mp4"
        )
        run(
            [
                "ffmpeg",
                "-i",
                path,
                "-ss",
                segment["start_ts"],
                "-t",
                segment["duration_ts"],
                "-async",
                "1",
                output_path,
            ]
        )
        segment_count += 1

    print("segmented video", segments)

    return segments
