let vttData = "";
let id = 0;

//todo: add a compiler cause no imports -.-
const languages = {
    "Afrikaans": "af",
    "Arabic": "ar",
    "Armenian": "hy",
    "Azerbaijani": "az",
    "Belarusian": "be",
    "Bosnian": "bs",
    "Bulgarian": "bg",
    "Catalan": "ca",
    "Chinese": "zh",
    "Croatian": "hr",
    "Czech": "cs",
    "Danish": "da",
    "Dutch": "nl",
    "English": "en",
    "Estonian": "et",
    "Finnish": "fi",
    "French": "fr",
    "Galician": "gl",
    "German": "de",
    "Greek": "el",
    "Hebrew": "he",
    "Hindi": "hi",
    "Hungarian": "hu",
    "Icelandic": "is",
    "Indonesian": "id",
    "Italian": "it",
    "Japanese": "ja",
    "Kannada": "kn",
    "Kazakh": "kk",
    "Korean": "ko",
    "Latvian": "lv",
    "Lithuanian": "lt",
    "Macedonian": "mk",
    "Malay": "ms",
    "Maori": "mi",
    "Marathi": "mr",
    "Nepali": "ne",
    "Norwegian": "no",
    "Persian": "fa",
    "Polish": "pl",
    "Portuguese": "pt",
    "Romanian": "ro",
    "Russian": "ru",
    "Serbian": "sr",
    "Slovak": "sk",
    "Slovenian": "sl",
    "Spanish": "es",
    "Swahili": "sw",
    "Swedish": "sv",
    "Tagalog": "tl",
    "Tamil": "ta",
    "Thai": "th",
    "Turkish": "tr",
    "Ukrainian": "uk",
    "Urdu": "ur",
    "Vietnamese": "vi",
    "Welsh": "cy"
}
const getLanguageCode = (language) => languages[language]

const getVideoElement = () => document.querySelector("video");

const checkForTrack = () => {
	const videoEl = getVideoElement();
	if (videoEl.textTracks.length == 0) return false;

	for (const track of videoEl.textTracks)
		if (track.label.includes("(SG)")) return track;

	return false;
};

const makeVttBlob = (vttText) => new Blob([vttText], { type: "text/plain" });

const makeTrack = (vttBlob, language) => {
	const track = document.createElement("track");
	track.id = "sg-track-" + id++;
	track.kind = "captions";
	track.label = language + " (SG)";
	track.srclang = getLanguageCode(language);
	track.src = URL.createObjectURL(vttBlob);
	return track;
};

const removeTrack = (track) => {
	track.mode = "disabled";
	document.getElementById(track.id).remove();
};

const updateSubs = (track, vttText, language) => {
	removeTrack(track);
	injectSubs(vttText, language);
};

const injectSubs = (vttText, language) => {
	const videoEl = getVideoElement();
	const vttBlob = makeVttBlob(vttText);
	const trackEl = makeTrack(vttBlob, language);
	videoEl.append(trackEl);
};

const showTrack = (trackEl) => {
	const videoEl = getVideoElement();
	trackEl.mode = "showing";
	checkForTrack().mode = "showing";
};

const attachVideoObserver = () => {
	const videoEl = getVideoElement();
	if (!videoEl) return;

	const options = { attributes: true, childList: true };

	const callback = (mutationList, observer) => {
		for (const mutation of mutationList) {
			if (mutation.type === "childList" && mutation.addedNodes[0]) {
				console.log(mutation)
                showTrack(mutation.addedNodes[0]);
			} else if (
				mutation.type === "attributes" &&
				mutation.attributeName === "src"
			) {
				const track = checkForTrack();
				if (track) removeTrack(track);
			}
		}
	};

	const observer = new MutationObserver(callback);
	observer.observe(videoEl, options);
};

const onMessage = ({action, vtt, language, done}, sender, sendResponse) => {
	console.log("got message", action)
    if (action !== "vtt" && action !== "updateVtt") return

    let track = checkForTrack();
	if (!track) {
		vttData += vtt;
		injectSubs(vtt, language);
		return;
	}
    let data
	if (action === "vtt") {
		data = vtt;
	} else if (action === "updateVtt") {
		vttData += vtt;
		data = vttData;
	}

	updateSubs(track, data, language);

	if (done) vttData = "";
};

attachVideoObserver();
chrome.runtime.onMessage.addListener(onMessage);

console.log("injected Subtitle Generator content script");