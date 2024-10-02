from flask import Flask, jsonify, request, render_template  # type: ignore
from flask_websockets import WebSockets, ws
from json import loads as json, dumps as stringify
from lib.vtt import get_vtt, get_mock_vtt
from lib.utils import get_config

config = get_config()

app = Flask(__name__)
app.secret_key = bytes(config["server"]["secret"], "utf-8")
app.config.update(SESSION_COOKIE_SECURE=True, SESSION_COOKIE_SAMESITE="Strict")
sockets = WebSockets(app, patch_app_run=True)


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/vtt", methods=["POST"])
def vtt_route():
    try:
        data = request.get_json()
        url = data["url"]
        mock = data["mock"]
        if mock:
            vtt, had = get_mock_vtt(url).values()
        else:
            vtt, had = get_vtt(url).values()
        return jsonify({"vtt": vtt})
    except Exception as e:
        print(e)
        return jsonify(
            {"error": str(type(e).__name__), "cause": str(type(e).__cause__)}
        )


@sockets.on_message
def handle_message(message):
    data = json(message)
    print("Received message:", data)
    if "url" not in data:
        return
    url = data["url"]
    mock = data["mock"]
    response = f'{{"response": "Server received your message: {url}"}}'
    ws.send(response)
    if mock:
        vtt, had = get_mock_vtt(url, ws=ws).values()
    else:
        vtt, had = get_vtt(url, ws=ws).values()
    if had:
        data = {"type": "vtt", "data": vtt}
        ws.send(stringify(data))
    ws.close()


if __name__ == "__main__":
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler

    print(
        f"Server starting up at {config["server"]["host"]}:{config["server"]["port"]}"
    )
    server = pywsgi.WSGIServer(
        (config["server"]["host"], config["server"]["port"]),
        app,
        handler_class=WebSocketHandler,
    )
    server.serve_forever()
