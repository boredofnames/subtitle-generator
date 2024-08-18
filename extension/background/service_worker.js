const waitUntil = async (promise) => {
    console.log("keeping alive")
    const keepAlive = setInterval(chrome.runtime.getPlatformInfo, 25 * 1000);
    let data
    try {
        data = await promise;
    } finally {
        console.log("allowing inactive")
        clearInterval(keepAlive);
    }
    return data
}

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

const onMenuClick = async (info, tab) => {
    console.log(info.menuItemId, tab)
    if (info.menuItemId === "genSubs") {
        console.log("clicked genSubs")
        const url = tab.url
        console.log(url)
        const vtt = await waitUntil(fetchVtt(url))
        console.log(vtt)
        chrome.tabs.sendMessage(tab.id, { action: "vtt", vtt })
    }
}

const onInstalled = (details) => {
    if (details.reason !== "install" && details.reason !== "update") return;
    chrome.contextMenus.create({
        "id": "genSubs",
        "title": "Generate Subtitles",
        "contexts": ["all"]
    });
}

chrome.runtime.onInstalled.addListener(onInstalled);
chrome.contextMenus.onClicked.addListener(onMenuClick)
