import { createContextMenus, onMenuClick } from "../js/context.js";

createContextMenus()
chrome.contextMenus.onClicked.addListener(onMenuClick)
