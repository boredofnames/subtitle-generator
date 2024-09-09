const getUrl = () => location.href
const getVideoElement = () => document.querySelector("video")

let vttData = "WEBVTT\n\n"

const checkForSubs = () => {
    const videoEl = getVideoElement()
    if (videoEl.textTracks.length == 0) return false

    for (const track of videoEl.textTracks)
        if (track.label.includes("(SG)"))
            return track

    return false
}

const makeVttBlob = (vttText) => new Blob([vttText], { type: 'text/plain' })

let id = 0
const makeTrack = (vttBlob) => {
    console.log("making track ", id)
    const track = document.createElement("track")
    track.id = "sg-track-" + id++
    track.kind = "captions"
    track.label = "English (SG)"
    track.srclang = "en"
    track.src = URL.createObjectURL(vttBlob)
    return track
}

const vttRegEx = /\[((?:\d+:)?\d{2}:\d{2}\.\d{3} --> (?:\d+:)?\d{2}:\d{2}\.\d{3})\]  (.+)/g
const formatVTT = (vttText) => 'WEBVTT\n\n' + vttText.replace(vttRegEx, "$1\n$2\n")

const removeCues = (track) => {
    console.log("removing cues")
    for (const cue of track.cues) {
        track.removeCue(cue)
    }
    console.log("track should be empty", track.cues)
}

const removeTrack = (track) => {
    removeCues(track)
    document.getElementById(track.id).remove()
}

const updateSubs = (track, vttText) => {
    track.mode = "hidden"
    removeTrack(track)
    setTimeout(() =>
        injectSubs(vttText)
        , 0)
}

const injectSubs = (vttText) => {
    const videoEl = getVideoElement()
    const vttBlob = makeVttBlob(vttText)
    const trackEl = makeTrack(vttBlob)
    videoEl.addEventListener("loadedmetadata", (evt) => {
        trackEl.mode = "showing";
        videoEl.textTracks[videoEl.textTracks.length - 1].mode = "showing";
    });
    videoEl.append(trackEl);
    videoEl.addEventListener('emptied', () => { removeTrack(videoEl.textTracks[videoEl.textTracks.length - 1]) })
}

const onMessage = (request, sender, sendResponse) => {
    console.log("got message: ", request)
    let track = checkForSubs()
    if (!track) {
        console.log("no track found, injecting", request.vtt)
        vttData += request.vtt
        injectSubs(request.vtt)
        return
    }

    if (request.action === "vtt") {
        vttData = "WEBVTT\n\n"
        data = request.vtt
    } else if (request.action === "updateVtt") {
        vttData += request.vtt
        data = vttData
    }
    console.log("track found, updating with ", data)
    updateSubs(track, data)
}

// learn now to attach a debugger.
// if(location.origin === "https://rumble.com"){
//     videoEl = getVideoElement()
//     videoEl.removeEventListener("contextmenu", DOMDebugger.getEventListeners(videoEl).contextmenu[0].listener)
// }

chrome.runtime.onMessage.addListener(onMessage);

console.log("injected Subtitle Generator content script")