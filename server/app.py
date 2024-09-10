from flask import Flask, jsonify, request, render_template  # type: ignore
from flask_websockets import WebSockets, ws, has_socket_context
from lib.vtt import get_vtt
from lib.utils import get_config
from json import loads as json, dumps as stringify

config = get_config()

app = Flask(__name__)
app.secret_key = bytes(config["server"]["secret"], 'utf-8')
app.config.update(
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_SAMESITE='Strict'
)
sockets = WebSockets(app, patch_app_run=True)


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/vtt", methods=["POST"])
def vtt_route():
    try:
        url = request.get_json()["url"]
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
    print('Received message:', data)
    url = data["url"]
    if url is None:
        return
    response = f'{{"response": "Server received your message: {url}"}}'
    ws.send(response)
    vtt, had = get_vtt(url, ws=ws).values()
    data = {"type": "vtt", "data": vtt}
    if had:
        ws.send(stringify(data))

if __name__ == '__main__':
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
