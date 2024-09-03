from os import remove
from os.path import exists
from flask import Flask, jsonify, request  # type: ignore
from lib.hash import get_hashed
from lib.vtt import create_vtt
from lib.utils import get_config

config = get_config()

app = Flask(__name__)


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
        if config["files"]["vtt"]["remove"]:
            print(f"removing vtt at {vtt_path}")
            remove(vtt_path)
        return jsonify({"vtt": final_vtt})
    except Exception as e:
        print(e)
        return jsonify(
            {"error": str(type(e).__name__), "cause": str(type(e).__cause__)}
        )
