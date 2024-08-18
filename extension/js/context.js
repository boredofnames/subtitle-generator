import { waitUntil } from "./utils.js"
import { fetchVtt } from "./vtt.js"

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

const createContextMenus = () =>
    chrome.contextMenus.create({
        "id": "genSubs",
        "title": "Generate Subtitles",
        "contexts": ["all"]
    });


export { onMenuClick, createContextMenus }