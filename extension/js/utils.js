const debug = false;

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

const getTab = async () => (await chrome.tabs.query({active: true, currentWindow: true}))[0]

export { debug, waitUntil, getTab };
