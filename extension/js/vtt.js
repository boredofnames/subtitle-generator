const fetchVtt = async (url) => {
    const headers = new Headers();
    headers.append("Content-Type", "application/json");

    const response = await fetch("http://127.0.0.1:5000/vtt", {
        method: "POST",
        body: JSON.stringify({ url }),
        headers,
    });

    const data = await response.json()
    console.log(data)
    return data.vtt
}

const socketVtt = (url, tabId) => {
    function sendMessage(data) {
        var message = JSON.stringify(data);
        socket.send(message);
    }

    const socket = new WebSocket('ws://127.0.0.1:5000');

    socket.addEventListener('open', (event) => {
        console.log('Connected to the server');
        sendMessage({ url })
    });

    socket.addEventListener('message', (event) => {
        console.log(event.data)
        const message = JSON.parse(event.data)
        if (message.response)
            console.log('Server says: ', message);
        if (!message.type) return
        if (message.type === "vtt" || message.type === "updateVtt") {
            console.log("handling vtt part")
            const vtt = message.data
            console.log(vtt)
            chrome.tabs.sendMessage(tabId, { action: message.type, vtt })
        } else if (message.type === "notify") {
            console.log("notify ready to watch")
            const options = {
                type: "basic",
                title: "Subtitle Generator",
                message: "Video should be watchable!",
                iconUrl: "../icons/48.png"
            }
            chrome.notifications.create("ready", options)
        }

    });

}

export { fetchVtt, socketVtt }