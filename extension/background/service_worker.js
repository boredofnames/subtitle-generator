import { createContextMenus, onMenuClick } from "../js/context.js";
import { genSubs, genSubsSockets } from "../js/vtt.js";
import { getTab, initOptions } from "../js/utils.js";

const onInstalled = async (details) => {
	if (details.reason !== "install" && details.reason !== "update") return;
	createContextMenus();
	initOptions();
};

const onMessage = async (message, sender, sendResponse) => {
	console.log("got message", message);
	if (message === "genSubs") {
		const tab = await getTab();
		genSubs(tab.url, tab.id);
	}
	if (message === "genSubsSockets") {
		const tab = await getTab();
		genSubsSockets(tab.url, tab.id);
	}
};

chrome.runtime.onMessage.addListener(onMessage);
chrome.runtime.onInstalled.addListener(onInstalled);
chrome.contextMenus.onClicked.addListener(onMenuClick);
