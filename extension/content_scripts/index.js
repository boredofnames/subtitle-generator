const getUrl = () => location.href
const getVideoElement = () => document.querySelector("video")

const checkForSubs = () => {
    const videoEl = getVideoElement()
    if (videoEl.textTracks.length > 0) {
        console.log("has subs")
    } else {
        console.log("no subs found")
    }
}

const makeVttBlob = (vttText) => new Blob([vttText], { type: 'text.plain' })

const makeTrack = (vttBlob) => {
    const track = document.createElement("track")
    track.kind = "captions"
    track.label = "English"
    track.srclang = "en"
    track.src = URL.createObjectURL(vttBlob)
    return track
}

const vttRegEx = /\[((?:\d+:)?\d{2}:\d{2}\.\d{3} --> (?:\d+:)?\d{2}:\d{2}\.\d{3})\]  (.+)/g
const formatVTT = (vttText) => 'WEBVTT\n\n' + vttText.replace(vttRegEx, "$1\n$2\n")

const removeSubs = (e, trackEl) => {
    e.currentTarget.remove(trackEl)
}

const injectSubs = (vttText) => {
    const videoEl = getVideoElement()
    const vttBlob = makeVttBlob(vttText)
    const trackEl = makeTrack(vttBlob)
    videoEl.addEventListener("loadedmetadata", (evt) => {
        trackEl.mode = "showing";
        videoEl.textTracks[0].mode = "showing";
    });
    videoEl.append(trackEl);

    videoEl.addEventListener('emptied', (e) => { removeSubs(e, trackEl) })
}

const onMessage = (request, sender, sendResponse) => {
    if (request.action === "vtt") {
        injectSubs(formatVTT(request.vtt))
    }
}

// learn now to attach a debugger.
// if(location.origin === "https://rumble.com"){
//     videoEl = getVideoElement()
//     videoEl.removeEventListener("contextmenu", DOMDebugger.getEventListeners(videoEl).contextmenu[0].listener)
// }

chrome.runtime.onMessage.addListener(onMessage);

console.log("injected Subtitle Generator content script")