import { waitUntil } from "./utils.js";

const fetchVtt = async (url, mock = false) => {
	const headers = new Headers();
	headers.append("Content-Type", "application/json");
	const options = (await chrome.storage.sync.get("options")).options
	const response = await fetch("http://127.0.0.1:5000/vtt", {
		method: "POST",
		body: JSON.stringify({ url, options, mock }),
		headers,
	});

	const {vtt, language} = await response.json();
	return {vtt, language};
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

	socket.addEventListener("open", async (event) => {
		console.log("Connected to the server");
		const options = (await chrome.storage.sync.get("options")).options
		keepAlive();
		sendMessage({ url, options, mock });
	});

	socket.addEventListener("close", (event) => {
		console.log("websocket connection closed");
		socket = null;
	});

	socket.addEventListener("message", (event) => {
		console.log(event.data);
		const {response, type, message, data:vtt, language, done} = JSON.parse(event.data);
		if (response) console.log("Server says: ", message);
		if (!type) return;
		if (type === "vtt" || type === "updateVtt") {
			console.log("handling vtt part");
			console.log(vtt);
			chrome.tabs.sendMessage(tabId, {
				action: type,
				vtt,
				language,
				done,
			});
		} else if (type === "notify") {
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

const genSubs = async (url, tabId, mock = false) => {
	const {vtt, language} = await waitUntil(fetchVtt(url, mock));
	chrome.tabs.sendMessage(tabId, { action: "vtt", vtt, language });
}

const genSubsSockets = (url, tabId, mock = false) => {
	socketVtt(url, tabId, mock);
}

export { genSubs, genSubsSockets };
