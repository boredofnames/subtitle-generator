import { getLanguages } from "../js/supported_languages.js";

const languages = getLanguages()
const selectModel = document.getElementById('model')
const selectLanguage = document.getElementById('language')
const browserLanguage = new Intl.DisplayNames(['en'], { type: 'language' }).of(navigator.language);
const options = {
    language: languages.includes(browserLanguage) ? browserLanguage : "English",
    model: "small"
}

function checkLanguageEligblity() {
    if (options.model.includes(".en")) {
        selectLanguage.value = "English"
        options.language = "English"
        selectLanguage.disabled = true
    } else {
        selectLanguage.disabled = false
    }
}

async function getStoredOptions() {
    const data = await chrome.storage.sync.get('options')
    Object.assign(options, data.options)
    selectModel.value = options.model
    selectLanguage.value = options.language
    checkLanguageEligblity()
}

function onOptionChange(e) {
    options[e.currentTarget.id] = e.currentTarget.value
    checkLanguageEligblity()
    console.log(options)
    chrome.storage.sync.set({ options })
}

function setupModel() {
    selectModel.addEventListener('change', onOptionChange)
}

function setupLanguage() {
    for (const language of languages) {
        const el = document.createElement('option')
        el.innerHTML = language
        el.value = language
        selectLanguage.appendChild(el)
    }

    selectLanguage.addEventListener('change', onOptionChange)
}

async function genSubs() {
    chrome.runtime.sendMessage("genSubs")
    window.close()
}

async function genSubsSockets() {
    chrome.runtime.sendMessage("genSubsSockets")
    window.close()
}

function attachEvents(){
    document.getElementById('gen-subs').addEventListener('click', genSubs)
    document.getElementById('gen-subs-sockets').addEventListener('click', genSubsSockets)
}

async function init() {
    setupModel()
    setupLanguage()
    getStoredOptions()
    attachEvents()
}

init()