from os import scandir, remove, makedirs
from os.path import exists
from time import time
from lib.yt import get_video
from lib.ffmpeg import segment
from lib.whisper import generate_vtt
from lib.subtitles import offset
from lib.utils import get_config, average

config = get_config()

def remove_tmp(path):
    if config["files"]["tmp"]["remove"]:
        remove(path)


def process_segment(path):
    start = time()
    generate_vtt(path, "small", "English")
    end = time()
    remove_tmp(path)
    tmp_vtt_path = path.replace("/segments", "/vtt").replace("mp4", "vtt")
    with open(tmp_vtt_path, "r") as file:
        vtt = file.read()
    remove_tmp(tmp_vtt_path)
    return {"data": vtt, "process_time": end - start}


def create_dirs():
    needed_dirs = ["./tmp/segments", "./vtt"]
    for adir in needed_dirs:
        if not exists(adir):
            makedirs(adir)


def create_vtt(url, hashed_url, vtt_path):
    segment_process_times = []
    elapsed = 0
    video_path = f"./tmp/{hashed_url}.mp4"
    create_dirs()
    get_video(url, video_path)
    segments = segment(
        path=video_path, duration=config["files"]["segments"]["length"] * 60, output_name=hashed_url
    )
    remove_tmp(video_path)
    segment_number = 0
    with scandir("./tmp/segments") as it:
        for entry in it:
            if entry.name.endswith(".mp4") and entry.is_file():
                print(entry.name, entry.path)
                vtt = process_segment(entry.path)
                segment_process_times.append(vtt["process_time"])
                average_process_time = average(segment_process_times)
                print(f"segment done. took {str(vtt["process_time"])} seconds. average process time: {str(average_process_time)}")
                estimated_remaining_time = average_process_time * (len(segments)-(segment_number + 1))
                if(elapsed >= estimated_remaining_time):
                    print(f"should be able to watch? elapsed: {elapsed} >= estimated remaining time {estimated_remaining_time}")
                if entry.name.endswith("_000.mp4"):
                    data = vtt["data"]
                else:
                    print("elapsed", elapsed)
                    data = offset(vtt["data"], elapsed)
                with open(vtt_path, "a") as final_file:
                    final_file.write(data)
                elapsed += segments[segment_number]["duration"]
                segment_number += 1
