import { waitUntil } from "./utils.js"
import { fetchVtt, socketVtt } from "./vtt.js"

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
    else if (info.menuItemId === "genSubsSockets") {
        console.log("clicked genSubsSockets")
        const url = tab.url
        console.log(url)
        socketVtt(url, tab.id)
    }
}

const createContextMenus = () => {
	chrome.contextMenus.create({
		id: "genSubs",
		title: "Generate Subtitles",
		contexts: ["all"],
	});
	chrome.contextMenus.create({
		id: "genSubsSockets",
		title: "Generate Subtitles (sockets)",
		contexts: ["all"],
	});
};

export { onMenuClick, createContextMenus }