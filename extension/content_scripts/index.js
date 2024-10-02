let vttData = "";
let id = 0;

const getVideoElement = () => document.querySelector("video");

const checkForSubs = () => {
	const videoEl = getVideoElement();
	if (videoEl.textTracks.length == 0) return false;

	for (const track of videoEl.textTracks)
		if (track.label.includes("(SG)")) return track;

	return false;
};

const makeVttBlob = (vttText) => new Blob([vttText], { type: "text/plain" });

const makeTrack = (vttBlob) => {
	const track = document.createElement("track");
	track.id = "sg-track-" + id++;
	track.kind = "captions";
	track.label = "English (SG)";
	track.srclang = "en";
	track.src = URL.createObjectURL(vttBlob);
	return track;
};

const removeTrack = (track) => {
	track.mode = "disabled";
	document.getElementById(track.id).remove();
};

const updateSubs = (track, vttText) => {
	removeTrack(track);
	injectSubs(vttText);
};

const injectSubs = (vttText) => {
	const videoEl = getVideoElement();
	const vttBlob = makeVttBlob(vttText);
	const trackEl = makeTrack(vttBlob);
	videoEl.append(trackEl);
};

const onMessage = (request, sender, sendResponse) => {
	let track = checkForSubs();
	if (!track) {
		vttData += request.vtt;
		injectSubs(request.vtt);
		return;
	}

	if (request.action === "vtt") {
		data = request.vtt;
	} else if (request.action === "updateVtt") {
		vttData += request.vtt;
		data = vttData;
	}

	updateSubs(track, data);

	if (request.done) vttData = "";
};

const showTrack = (trackEl) => {
	const videoEl = getVideoElement();
	trackEl.mode = "showing";
	videoEl.textTracks[videoEl.textTracks.length - 1].mode = "showing";
};

const attachVideoObserver = () => {
	const videoEl = getVideoElement();
	if (!videoEl) return;

	const config = { attributes: true, childList: true };

	const callback = (mutationList, observer) => {
		for (const mutation of mutationList) {
			if (mutation.type === "childList" && mutation.addedNodes[0]) {
				showTrack(mutation.addedNodes[0]);
			} else if (
				mutation.type === "attributes" &&
				mutation.attributeName === "src"
			) {
				const track = checkForSubs();
				if (track) removeTrack(track);
			}
		}
	};

	const observer = new MutationObserver(callback);
	observer.observe(videoEl, config);
};

chrome.runtime.onMessage.addListener(onMessage);
attachVideoObserver();

console.log("injected Subtitle Generator content script");
