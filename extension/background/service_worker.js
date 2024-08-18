import { createContextMenus, onMenuClick } from "../js/context.js";

const onInstalled = (details) => {
    if (details.reason !== "install" && details.reason !== "update") return;
    createContextMenus()
}

chrome.runtime.onInstalled.addListener(onInstalled);
chrome.contextMenus.onClicked.addListener(onMenuClick)
