from os import scandir, remove, makedirs
from os.path import exists
from time import time
from flask import Flask, jsonify, request # type: ignore
from lib.yt import get_audio
from lib.ffmpeg import segment_audio
from lib.whisper import generate_vtt
from lib.hash import get_hashed
from lib.subtitles import offset

app = Flask(__name__)

options = {
    "remove_vtt": False,
    "segment_length": 2, # in minutes
    "keep_tmp": False
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
    tmp_vtt_path = path.replace("/segments/", "/vtt/").replace("mp3", "vtt")
    with open(tmp_vtt_path, "r") as file:
        vtt = file.read()
    remove_tmp(tmp_vtt_path)
    return {"data":vtt, "process_time": end - start}

def create_dirs():
    needed_dirs = ["./tmp/segments", "./vtt"]
    for adir in needed_dirs:
        if not exists(adir):
            makedirs(adir)

def create_vtt(url, hashed_url, vtt_path):
    create_dirs()
    total_time = 0
    audio_path = "./tmp/" + hashed_url + ".mp3"
    get_audio(url, audio_path)
    segment_audio(audio_path, options["segment_length"] * 60)
    remove_tmp(audio_path)
    segment_number = 0
    with scandir("tmp/segments") as it:
        for entry in it:
            if entry.name.endswith(".mp3") and entry.is_file():
                print(entry.name, entry.path)
                total_time += options["segment_length"]
                vtt = process_segment(entry.path)
                print('segment done. took ' + str(vtt["process_time"]) + ' seconds')
                if entry.name.endswith("_000.mp3"):
                    data = vtt["data"]
                else:
                    data =  offset(vtt["data"], options["segment_length"] * 60 * segment_number)                
                with open(vtt_path, "a") as final_file:
                    final_file.write(data)
                segment_number += 1

@app.route("/")
def hello():
    return "Hello, World!"

@app.route('/vtt', methods=['POST'])
def get_vtt():
    try:
        url = request.get_json()["url"]
        print("user requesting subtitles for url " + url)
        hashed_url = get_hashed(url)
        vtt_path = './vtt/' + hashed_url + ".vtt"
        if not exists(vtt_path):
            create_vtt(url, hashed_url, vtt_path)
        with open(vtt_path, "r") as final_file:
            final_vtt = final_file.read()                 
        if(options["remove_vtt"]):
            print("removing vtt at "+ vtt_path)
            remove(vtt_path)
        return jsonify({"vtt": final_vtt})
    except Exception as e:
        return jsonify({"error": str(type(e).__name__), "cause": str(type(e).__cause__)})