const AUDIO_SVG = `<svg class="form-svg-fill-icon" width="24px" height="24px" viewBox="-3 0 24 24" xmlns="http://www.w3.org/2000/svg">
    <path d="m18.07.169c-.148-.106-.333-.169-.532-.169-.111 0-.217.02-.316.055l.006-.002-11.077 3.938c-.361.131-.613.471-.613.869v.001 2.193.042 10.604c-.534-.295-1.169
    -.469-1.846-.471h-.001c-.043-.002-.093-.003-.143-.003-1.904 0-3.458 1.497-3.549 3.379v.008c.091 1.89 1.645 3.388 3.549 3.388.05 0 .1-.001.15-.003h-.007c.043.002.093
    .003.143.003 1.904 0 3.458-1.497 3.549-3.379v-.008-12.883l9.23-3.223v8.973c-.534-.294-1.17-.468-1.846-.47h-.001c-.043-.002-.094-.003-.144-.003-1.904 0-3.457 1.498-3.547
    3.379v.008c.09 1.89 1.644 3.388 3.548 3.388.051 0 .101-.001.151-.003h-.007c.031.001.068.002.105.002 1.696 0 3.12-1.166 3.513-2.74l.005-.025c.042-.101.068-.217.069-.34v
    -15.754c0-.31-.153-.585-.388-.752l-.003-.002z"/>
</svg>`

const ARTIST_SVG = `
<svg class="form-svg-fill-icon" height="24px" width="24px" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128">
    <ellipse transform="matrix(0.1607 -0.987 0.987 0.1607 -3.8377 74.789)" cx="42.1" cy="39.7" rx="17.3" ry="17.3"/>
    <path d="M84.7,40.1c-0.6-1.6-1.6-3-3-4.1c-3.9-2.8-9.3-2-12.1,1.9c-2.8,3.9-2,9.3,1.9,12.1c3.9,2.8,9.3,2,12.1-1.9
        c0.1-0.2,0.2-0.3,0.3-0.5l5.9,0.6L66.3,65.2l-32.2-5.4c-5.4-0.9-10.4,2.7-11.2,8.1l-7.3,45.1h35.8c1.6-5.6,2.8-11.4,3.8-17.3
        c0.1-0.9,0.5-3,0.5-3.3c0.8-4.8,0.4-9.9-1.2-14.3l12.7,2.1c1.8,0.3,3.9-0.1,5.7-1.4l28.1-20.2c2.7-2,3.7-5.6,2.7-8.6l10.9,1.2
        l0.8-7.5L84.7,40.1z"/>
</svg>`

const TRACK_SVG = `<svg class="form-svg-fill-icon" width="24px" height="24px" viewBox="14 14 46 46" xmlns="http://www.w3.org/2000/svg">
    <path fill-opacity="1" stroke-width="0.2" stroke-linejoin="round" d="M 15.8333,25.3333L 60.1667,25.3333L 60.1667,52.25L 15.8333,52.25L 15.8333,25.3333 Z
        M 19,28.5L 19,49.0833L 57,49.0833L 57,28.5L 19,28.5 Z M 29.4078,44.3333L 27.1911,44.3333L 27.1911,43.2319L 27.1611,43.2319C 26.6608,44.0647 25.9204,44.4811
        24.9398,44.4811C 24.2163,44.4811 23.6471,44.2791 23.2323,43.875C 22.8174,43.4709 22.61,42.9318 22.61,42.2575C 22.61,40.8336 23.4666,40.0116 25.1799,39.7915L
        27.205,39.5259C 27.205,38.7901 26.7639,38.4222 25.8819,38.4222C 24.9937,38.4222 24.1493,38.6685 23.3489,39.1611L 23.3489,37.4247L 24.6708,36.986L
        26.1982,36.7967C 28.3379,36.7967 29.4078,37.8434 29.4078,39.937L 29.4078,44.3333 Z M 27.205,41.3385L 27.205,40.8559L 25.8242,41.0245C 25.0606,41.1169
        24.6789,41.4409 24.6789,41.9966C 24.6789,42.2475 24.7716,42.4534 24.9571,42.6143C 25.1426,42.7751 25.3939,42.8556 25.711,42.8556C 26.1528,42.8556
        26.5123,42.7124 26.7893,42.4261C 27.0664,42.1398 27.205,41.7772 27.205,41.3385 Z M 33.4278,43.4143L 33.3978,43.4143L 33.3978,44.3333L 31.1811,44.3333L
        31.1811,33.3978L 33.3978,33.3978L 33.3978,38.1151L 33.4278,38.1151C 33.9973,37.2362 34.807,36.7967 35.8569,36.7967C 36.8205,36.7967 37.5629,37.1211
        38.0839,37.7699C 38.605,38.4188 38.8655,39.3058 38.8655,40.4311C 38.8655,41.6518 38.5615,42.632 37.9535,43.3716C 37.3454,44.1113 36.5327,44.4811
        35.5151,44.4811C 34.5946,44.4811 33.8988,44.1255 33.4278,43.4143 Z M 33.3631,40.3664L 33.3631,41.1007C 33.3631,41.564 33.5017,41.9477 33.7788,42.2517C
        34.0558,42.5558 34.4114,42.7078 34.8455,42.7078C 35.3704,42.7078 35.7776,42.5127 36.067,42.1224C 36.3564,41.7322 36.5011,41.1792 36.5011,40.4634C
        36.5011,39.8692 36.3687,39.4051 36.104,39.0711C 35.8392,38.737 35.4605,38.57 34.9679,38.57C 34.5061,38.57 34.1232,38.7359 33.8192,39.0676C 33.5152,39.3993
        33.3631,39.8323 33.3631,40.3664 Z M 45.8111,44.017C 45.3077,44.3264 44.5804,44.4811 43.6291,44.4811C 42.5177,44.4811 41.6183,44.1401 40.931,43.4582C
        40.2437,42.7763 39.9,41.8958 39.9,40.8167C 39.9,39.5729 40.2683,38.5919 41.0049,37.8738C 41.7414,37.1557 42.727,36.7967 43.9616,36.7967C 44.8128,36.7967
        45.4294,36.9167 45.8111,37.1569L 45.8111,39.1611C 45.357,38.767 44.8506,38.57 44.2918,38.57C 43.6683,38.57 43.1746,38.7559 42.8105,39.1276C 42.4465,39.4994
        42.2644,40.0124 42.2644,40.6666C 42.2644,41.3023 42.4384,41.8015 42.7863,42.164C 43.1342,42.5265 43.6129,42.7078 44.2225,42.7078C 44.7644,42.7078 45.2941,42.5107
        45.8111,42.1167L 45.8111,44.017 Z M 47.1042,47.5L 47.1042,30.0833L 49.0833,30.0833L 49.0833,47.5L 47.1042,47.5 Z "/>
</svg>
`

const LYRICS_SVG = `<svg class="form-svg-fill-icon" width="24px" height="24px" viewBox="0 0 32 32" xmlns="http://www.w3.org/2000/svg">
    <path d="M27,3H5A1,1,0,0,0,5,5H27a1,1,0,0,0,0-2Z"/>
    <path d="M27,7H5A1,1,0,0,0,5,9H27a1,1,0,0,0,0-2Z"/>
    <path d="M27,11H5a1,1,0,0,0,0,2H27a1,1,0,0,0,0-2Z"/>
    <path d="M27,15H5a1,1,0,0,0,0,2H27a1,1,0,0,0,0-2Z"/>
    <path d="M27,19H5a1,1,0,0,0,0,2H27a1,1,0,0,0,0-2Z"/>
    <path d="M27,23H5a1,1,0,0,0,0,2H27a1,1,0,0,0,0-2Z"/>
    <path d="M27,27H5a1,1,0,0,0,0,2H27a1,1,0,0,0,0-2Z"/>
</svg>`

const REMOVE_SVG = `<svg class="form-svg-fill-icon" width="20px" height="20px" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
    <path d="M12 4h3c.6 0 1 .4 1 1v1H3V5c0-.6.5-1 1-1h3c.2-1.1 1.3-2 2.5-2s2.3.9 2.5 2zM8 4h3c-.2-.6-.9-1-1.5-1S8.2 3.4 8 4zM4 7h11l-.9 10.1c0 .5-.5.9-1 .9H5.9c-.5 0-.9-.4-1-.9L4 7z"/>
</svg>`

function GetCode() {
    let input = document.getElementById("code")
    let icon = document.getElementById("code-icon")
    let error = document.getElementById("error")
    let code = input.value.trim()
    input.value = code

    if (code == "") {
        error.innerText = "html код пуст"
        input.classList.add("error-input")
        icon.classList.add("error-icon")
        return null
    }

    input.classList.remove("error-input")
    icon.classList.remove("error-icon")
    return code
}

function HideParsedAudios() {
    let parentBlock = document.getElementById("audios-block")
    let removeBlock = document.getElementById("remove-all-block")

    parentBlock.classList.add("hidden")
    removeBlock.classList.add("hidden")
}

function RemoveAudio(audioBlock) {
    audioBlock.remove()

    let block = document.getElementById("audios")
    let currentCount = document.getElementById("current-count")
    let totalCount = document.getElementById("total-count")

    currentCount.innerText = block.children.length
    totalCount.innerText = block.children.length

    if (block.children.length == 0)
        HideParsedAudios()
}

function RemoveAllAudios(withConfirm = true) {
    if (withConfirm && !confirm("Вы уверены, что хотите удалить все эти аудио?"))
        return

    let block = document.getElementById("audios")
    block.innerHTML = ""

    HideParsedAudios()
}

function ParseAudio(trackId) {
    let currentCount = document.getElementById("current-count")
    let error = document.getElementById("error")

    return SendRequest("/parse-audio", {track_id: trackId}).then(response => {
        if (response.status != "success") {
            error.innerText = "Некоторые треки не удалось скачать"
            return
        }

        AddParsedAudio(response.track)
        currentCount.innerText = 1 + +currentCount.innerText
    })
}

function AddParsedAudio(audio) {
    let block = document.getElementById("audios")
    let artists = audio.artists.map(artist => artist.name)

    let div = MakeElement("audio-form", block)
    let caption = MakeElement("audio-caption", div, {innerText: `${artists.join(", ")} - ${audio.title}`})
    let removeIcon = MakeElement("audio-close-icon", div, {innerHTML: REMOVE_SVG, title: "Удалить"})
    removeIcon.addEventListener("click", () => RemoveAudio(div))

    let audioTag = MakeIconInputRow(div, AUDIO_SVG, audio.direct_link, "Аудио", "audio", "audio")
    audioTag.addEventListener("play", () => StopOtherAudios(audioTag))
    audioTag.setAttribute("data-album-id", audio.album_id)
    audioTag.setAttribute("data-track-id", audio.track_id)

    let artistInput = MakeIconInputRow(div, ARTIST_SVG, audio.artists.map(artist => JSON.stringify(artist)), "Исполнитель", "artists", "textarea")
    artistInput.addEventListener("input", () => ClearSaveError(artistInput))

    let trackInput = MakeIconInputRow(div, TRACK_SVG, audio.title, "Трек", "track", "text")
    trackInput.addEventListener("input", () => ClearSaveError(trackInput))

    if (audio.lyrics) {
        let lyricsInput = MakeIconInputRow(div, LYRICS_SVG, audio.lyrics.map(line => JSON.stringify(line)), "Текст", "lyrics", "textarea")
        lyricsInput.addEventListener("input", () => ClearSaveError(lyricsInput))
        lyricsInput.classList.add("one-line-textarea")
    }

    MakeElement("error", div, {})
}

function AddParsedAudios(trackIds) {
    let parentBlock = document.getElementById("audios-block")
    let currentCount = document.getElementById("current-count")
    let totalCount = document.getElementById("total-count")

    parentBlock.classList.remove("hidden")
    currentCount.innerText = "0"
    totalCount.innerText = trackIds.length

    return Promise.all(trackIds.map(trackId => ParseAudio(trackId)))
}

function ParseAudios() {
    let code = GetCode()

    if (code === null)
        return

    let error = document.getElementById("error")
    let parseBtn = document.getElementById("parse-btn")
    let saveBtn = document.getElementById("save-btn")
    parseBtn.setAttribute("disabled", "")
    saveBtn.setAttribute("disabled", "")

    RemoveAllAudios(false)

    SendRequest("/parse-audios", {code: code}).then(response => {
        if (response.status != "success") {
            error.innerText = response.message
            parseBtn.removeAttribute("disabled")
            return
        }

        error.innerText = ""
        AddParsedAudios(response.track_ids).then(() => {
            let removeBlock = document.getElementById("remove-all-block")
            removeBlock.classList.remove("hidden")

            parseBtn.removeAttribute("disabled")
            saveBtn.removeAttribute("disabled")
            saveBtn.scrollIntoView({behavior: "smooth"})
        })
    })
}

function MakeSaveError(message, inputBlock) {
    let error = inputBlock.parentNode.parentNode.getElementsByClassName("error")[0]
    let input = inputBlock.children[0]
    let icon = inputBlock.parentNode.children[0]

    error.innerText = message
    input.classList.add("error-input")
    icon.classList.add("error-icon")
    inputBlock.parentNode.parentNode.scrollIntoView({behavior: "smooth"})
}

function ClearSaveError(input) {
    let inputBlock = input.parentNode
    let icon = inputBlock.parentNode.children[0]
    let error = inputBlock.parentNode.parentNode.getElementsByClassName("error")[0]

    error.innerText = ""
    input.classList.remove("error-input")
    icon.classList.remove("error-icon")
}

function StopOtherAudios(target) {
    for (let audio of document.getElementsByTagName("audio"))
        if (audio != target)
            audio.pause()
}

function GetAudios() {
    let audios = []

    for (let audioBlock of document.getElementsByClassName("audio-form")) {
        let audio = {}

        for (let inputBlock of audioBlock.getElementsByClassName("form-row-input")) {
            let input = inputBlock.children[0]
            let name = input.getAttribute("name")

            if (name == "audio") {
                audio["album_id"] = input.getAttribute("data-album-id")
                audio["track_id"] = input.getAttribute("data-track-id")
                audio["link"] = `${audio["track_id"]}:${audio["album_id"]}`
            }
            else if (name == "artists") {
                try {
                    audio[name] = JSON.parse(`[${input.value.split("\n").join(",").trim()}]`)
                }
                catch (Error) {
                    MakeSaveError("Исполнитель введён некорректно", inputBlock)
                    return null
                }

                if (audio["artists"].length == 0) {
                    MakeSaveError("Исполнитель пуст", inputBlock)
                    return null
                }
            }
            else if (name == "track"){
                audio[name] = input.value.trim()

                if (audio["track"].length == 0) {
                    MakeSaveError("Исполнитель пуст", inputBlock)
                    return null
                }
            }
            else if (name == "lyrics") {
                try {
                    audio["lyrics"] = JSON.parse(`[${input.value.split("\n").join(",").trim()}]`)
                }
                catch (Error) {
                    MakeSaveError("Текст введён некорректно", inputBlock)
                    return null
                }

                if (audio["lyrics"].length == 0) {
                    MakeSaveError("Текст пуст", inputBlock)
                    return null
                }
            }
        }

        audios.push(audio)
    }

    return audios
}

function SaveAudios() {
    let audios = GetAudios()

    if (audios === null)
        return

    let error = document.getElementById("save-error")
    let info = document.getElementById("save-info")
    let code = document.getElementById("code")

    SendRequest("/add-audios", {audios: audios}).then(response => {
        if (response.status != "success") {
            error.innerText = response.message
            error.scrollIntoView({behavior: "smooth"})
            return
        }

        error.innerText = ""
        info.innerText = "Аудиозаписи успешно добавлены"
        info.scrollIntoView({behavior: "smooth"})

        setTimeout(() => {
            info.innerText = ""
            code.value = ""
            RemoveAllAudios(false)
        }, 1500)
    })
}
