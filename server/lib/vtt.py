from os import scandir, remove, makedirs
from os.path import exists
from time import time
from json import dumps as stringify
from time import sleep
from lib.yt import get_video
from lib.ffmpeg import segment
from lib.whisper import generate_vtt
from lib.subtitles import offset
from lib.utils import get_config, average
from lib.hash import get_hashed

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


def create_vtt(url, hashed_url, vtt_path, ws=None):
    segment_process_times = []
    elapsed = 0
    video_path = f"./tmp/{hashed_url}.mp4"
    create_dirs()
    get_video(url, video_path)
    segments = segment(
        path=video_path,
        duration=config["files"]["segments"]["length"] * 60,
        output_name=hashed_url,
    )
    remove_tmp(video_path)
    segment_number = 0
    notifed = False
    with scandir("./tmp/segments") as it:
        for entry in it:
            if entry.name.endswith(".mp4") and entry.is_file():
                print(entry.name, entry.path)
                vtt = process_segment(entry.path)
                segment_process_times.append(vtt["process_time"])
                average_process_time = average(segment_process_times)
                print(
                    f"segment {segment_number} done.\ntook {str(vtt["process_time"])} seconds.\naverage process time: {str(average_process_time)}"
                )

                if entry.name.endswith("_000.mp4"):
                    data = vtt["data"]
                else:
                    print("elapsed", elapsed)
                    data = offset(vtt["data"], elapsed)
                if ws is not None:
                    ws_data = {
                        "type": "updateVtt",
                        "data": data,
                        "done": len(segments) == segment_number,
                    }
                    ws.send(stringify(ws_data))
                with open(vtt_path, "a") as final_file:
                    final_file.write(data)

                elapsed += segments[segment_number]["duration"]
                segment_number += 1
                estimated_remaining_time = average_process_time * (
                    len(segments) - (segment_number)
                )
                if elapsed >= estimated_remaining_time:
                    print(
                        f"should be able to watch?\nelapsed: {elapsed} >= estimated remaining time {estimated_remaining_time}"
                    )
                    if ws is not None and not notifed:
                        ws.send('{"type": "notify"}')
                    notifed = True


def get_vtt(url, ws=None):
    hashed_url = get_hashed(url)
    print(f"user requesting subtitles for url {url}, hash: {hashed_url}")
    vtt_path = f"./vtt/{hashed_url}.vtt"
    had = True
    if not exists(vtt_path):
        print("vtt not found, generating")
        create_vtt(url, hashed_url, vtt_path, ws)
        had = False
    with open(vtt_path, "r") as final_file:
        final_vtt = final_file.read()
    if config["files"]["vtt"]["remove"]:
        print(f"removing vtt at {vtt_path}")
        remove(vtt_path)
    return {"vtt": final_vtt, "had": had}


def get_mock_vtt(url, ws=None, had=False):
    vtt_parts = [
        "WEBVTT\n\n00:00:00.000 --> 00:01:00.000\nThis is a test one of four\n\n",
        "00:01:00.000 --> 00:02:00.000\nThis is a test two of four\n\n",
        "00:02:00.000 --> 00:03:00.000\nThis is a test three of four\n\n",
        "00:03:00.000 --> 00:04:00.000\nThis is a test four of four\n\n",
    ]
    if ws is not None:
        for i, part in enumerate(vtt_parts):
            done = i == len(vtt_parts) - 1
            ws_data = {"type": "updateVtt", "data": part, "done": done, "bitch": "yes"}
            ws.send(stringify(ws_data))
            sleep(5)

    final_vtt = "".join(vtt_parts)
    sleep(1)
    return {"vtt": final_vtt, "had": had}
