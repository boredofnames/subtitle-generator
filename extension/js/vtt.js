const fetchVtt = async (url, mock = false) => {
	const headers = new Headers();
	headers.append("Content-Type", "application/json");
	const response = await fetch("http://127.0.0.1:5000/vtt", {
		method: "POST",
		body: JSON.stringify({ url, mock }),
		headers,
	});

	const data = await response.json();
	console.log(data);
	return data.vtt;
};

const socketVtt = (url, tabId, mock = false) => {
	function sendMessage(data) {
		var message = JSON.stringify(data);
		socket.send(message);
	}

	function keepAlive() {
		const keepAliveIntervalId = setInterval(() => {
			if (socket) {
				sendMessage({ ping: true });
			} else {
				clearInterval(keepAliveIntervalId);
			}
		}, 20 * 1000);
	}

	let socket = new WebSocket("ws://127.0.0.1:5000");

	socket.addEventListener("open", (event) => {
		console.log("Connected to the server");
		keepAlive();
		sendMessage({ url, mock });
	});

	socket.addEventListener("close", (event) => {
		console.log("websocket connection closed");
		socket = null;
	});

	socket.addEventListener("message", (event) => {
		console.log(event.data);
		const message = JSON.parse(event.data);
		if (message.response) console.log("Server says: ", message);
		if (!message.type) return;
		if (message.type === "vtt" || message.type === "updateVtt") {
			console.log("handling vtt part");
			const vtt = message.data;
			console.log(vtt);
			chrome.tabs.sendMessage(tabId, {
				action: message.type,
				vtt,
				done: message.done,
			});
		} else if (message.type === "notify") {
			console.log("notify ready to watch");
			const options = {
				type: "basic",
				title: "Subtitle Generator",
				message: "Video should be watchable!",
				iconUrl: "../icons/48.png",
			};
			chrome.notifications.create("ready", options);
		}
	});
};

export { fetchVtt, socketVtt };
