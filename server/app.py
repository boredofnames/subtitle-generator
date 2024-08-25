from os import scandir, remove, makedirs
from os.path import exists
from time import time
from flask import Flask, jsonify, request  # type: ignore
from lib.yt import get_video
from lib.ffmpeg import segment
from lib.whisper import generate_vtt
from lib.hash import get_hashed
from lib.subtitles import offset

app = Flask(__name__)

options = {
    "remove_vtt": False,
    "segment_length": 5,  # segment_length in minutes
    "keep_tmp": False,
}

total_time = 0


def remove_tmp(path):
    if not options["keep_tmp"]:
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
    create_dirs()
    elapsed = 0
    video_path = f"./tmp/{hashed_url}.mp4"
    get_video(url, video_path)
    segments = segment(
        path=video_path, duration=options["segment_length"] * 60, output_name=hashed_url
    )
    remove_tmp(video_path)
    segment_number = 0
    with scandir("./tmp/segments") as it:
        for entry in it:
            if entry.name.endswith(".mp4") and entry.is_file():
                print(entry.name, entry.path)
                vtt = process_segment(entry.path)
                print(f"segment done. took {str(vtt["process_time"])} seconds")
                if entry.name.endswith("_000.mp4"):
                    data = vtt["data"]
                else:
                    print("elapsed", elapsed)
                    data = offset(vtt["data"], elapsed)
                with open(vtt_path, "a") as final_file:
                    final_file.write(data)
                elapsed += segments[segment_number]["duration"]
                segment_number += 1


@app.route("/")
def hello():
    return "Hello, World!"


@app.route("/vtt", methods=["POST"])
def get_vtt():
    try:
        url = request.get_json()["url"]
        hashed_url = get_hashed(url)
        print(f"user requesting subtitles for url {url}, hash: {hashed_url}")
        vtt_path = f"./vtt/{hashed_url}.vtt"
        if not exists(vtt_path):
            print("vtt not found, generating")
            create_vtt(url, hashed_url, vtt_path)
        with open(vtt_path, "r") as final_file:
            final_vtt = final_file.read()
        if options["remove_vtt"]:
            print(f"removing vtt at {vtt_path}")
            remove(vtt_path)
        return jsonify({"vtt": final_vtt})
    except Exception as e:
        return jsonify(
            {"error": str(type(e).__name__), "cause": str(type(e).__cause__)}
        )
