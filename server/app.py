from flask import Flask, jsonify, request
import subprocess
import os

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello, World!"

@app.route('/vtt', methods=['POST'])
def get_vtt():
    url = request.get_json()["url"]
    print("user requesting subtitles for url " + url)
    subprocess.run(["yt-dlp", "-f", "worst", "-x", "--audio-format", "wav", url, "-o", "output.wav"])
    subprocess.run(["whisper", "output.wav", "--model", "small", "--language", "English", "--output_format", "vtt"])
    with open("output.vtt", "r") as file:
        vtt = file.read()
    print(vtt)
    os.remove("./output.wav")
    os.remove("./output.vtt")
    return jsonify({"vtt": vtt})