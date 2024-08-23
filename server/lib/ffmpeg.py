from subprocess import run
import re
from os.path import exists
try:
    from lib.utils import get_nearest, double_to_time_string
except:
    from utils import get_nearest, double_to_time_string

def get_duration(path, format="seconds"):
    command = ['ffprobe', '-v', 'error', '-show_entries','stream=duration', '-of', 'default=noprint_wrappers=1:nokey=1', path]
    output = run(command, capture_output=True)
    return float(output.stdout.decode('utf-8'))

def get_silences(path, noise=-30, duration=0.25):
    print("getting silences")
    rx_match = r'silence_start:\s(\d+\.?\d*)'
    sd = 'silencedetect=n=' + str(noise) + 'dB:d=' + str(duration)
    command = ['ffmpeg', '-i', path, '-af', sd, '-f', 'null', '-']
    silence_process = run(command, capture_output=True)
    silence_out = silence_process.stderr.decode()
    silences = re.findall(rx_match, silence_out)
    silences = [float(silence) for silence in silences]
    print("got silences", silences)
    return silences

def offset(value, offset):
    if value == 0 and offset < 0:
        return 0
    return value + offset

def segment_audio(path, duration, output_name):
    print("segmenting audio")
    if not exists(path):
        raise FileNotFoundError('File not found ' + path)
    # segment the audio file into chunks of specified duration
    segments = []
    file_duration = get_duration(path)
    silences = get_silences(path)
    
    current_time = 0
    segments_total_time = 0
    
    while True:
        next_silence = get_nearest(silences, current_time + duration)
        last_silence_item = silences[-1]
        last_end = segments[-1]["end"] if len(segments) > 0 else 0
        if next_silence is last_silence_item:
            segment_duration = file_duration - segments_total_time
            end = next_silence + segment_duration
        else:
            end = next_silence
            segment_duration = next_silence - last_end
        print(segment_duration)
        start = current_time
        segments_total_time += segment_duration
        segments.append({
            "start": start,
            "end": end, 
            "duration": segment_duration,
            "start_ts": double_to_time_string(start),
            "end_ts": double_to_time_string(end), 
            "duration_ts": double_to_time_string(segment_duration),
        })
        current_time = next_silence
        silences.remove(next_silence)
        if next_silence is last_silence_item:
            break
        
    if segments_total_time != file_duration:
        print(
            "WARNING: total duration of audio is not equal to the sum of segment durations", 
            segments_total_time, 
            file_duration
        )
        print(segments)
        return

    segment_count = 0
    for segment in segments:
        output_path = "./tmp/segments/" + output_name + "_" + str(segment_count).zfill(3) + ".mp3"
        run(["ffmpeg", "-i", path, "-ss", segment["start_ts"], "-t", segment["duration_ts"], "-async", "1", output_path])
        segment_count += 1

    print("segmented audio", segments)

    return segments

if __name__ == "__main__":
    seg = segment_audio(path="./tmp/48541a66b1.mp3", duration=60, output_name="48541a66b1")
    print(seg)