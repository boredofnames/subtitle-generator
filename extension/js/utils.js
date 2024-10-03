const debug = true;

const waitUntil = async (promise) => {
	console.log("keeping alive");
	const keepAlive = setInterval(chrome.runtime.getPlatformInfo, 25 * 1000);
	let data;
	try {
		data = await promise;
	} finally {
		console.log("allowing inactive");
		clearInterval(keepAlive);
	}
	return data;
};

const getTab = async () =>
	(await chrome.tabs.query({ active: true, currentWindow: true }))[0];

const initOptions = async () => {
	const options = (await chrome.storage.sync.get("options")).options;
	if (!options) {
		const options = { model: "small", language: "English" };
		chrome.storage.sync.set({ options });
	}
};

export { debug, waitUntil, getTab, initOptions };
