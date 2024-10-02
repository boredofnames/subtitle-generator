import { debug, waitUntil } from "./utils.js";
import { fetchVtt, socketVtt } from "./vtt.js";

const onMenuClick = async (info, tab) => {
	const url = tab.url;
	if (info.menuItemId === "genSubs") {
		const vtt = await waitUntil(fetchVtt(url));
		chrome.tabs.sendMessage(tab.id, { action: "vtt", vtt });
	} else if (info.menuItemId === "genSubsSockets") {
		socketVtt(url, tab.id);
	} else if (info.menuItemId === "mockSubs") {
		const vtt = await waitUntil(fetchVtt(url, true));
		chrome.tabs.sendMessage(tab.id, { action: "vtt", vtt });
	} else if (info.menuItemId === "mockSubsSockets") {
		socketVtt(url, tab.id, true);
	}
};

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
	if (debug === true) {
		chrome.contextMenus.create({
			id: "mockSubs",
			title: "Mock Subtitles",
			contexts: ["all"],
		});
		chrome.contextMenus.create({
			id: "mockSubsSockets",
			title: "Mock Subtitles (sockets)",
			contexts: ["all"],
		});
	}
};
export { onMenuClick, createContextMenus };
