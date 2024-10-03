import { debug } from "./utils.js";
import { genSubs, genSubsSockets } from "./vtt.js";

const onMenuClick = async (info, tab) => {
	const url = tab.url;
	const id = tab.id
	if (info.menuItemId === "genSubs") {
		genSubs(url, id)
	} else if (info.menuItemId === "genSubsSockets") {
		genSubsSockets(url, id)
	} else if (info.menuItemId === "mockSubs") {
		genSubs(url, id, true)
	} else if (info.menuItemId === "mockSubsSockets") {
		genSubsSockets(url, id, true)
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
