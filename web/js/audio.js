function LoadAudio(audio, errorId = "error") {
    let error = document.getElementById(errorId)
    error.innerText = ""

    if (audio.hasAttribute("data-src")) {
        return new Promise((resolve, reject) => {
            audio.src = audio.getAttribute("data-src")
            resolve(true)
        })
    }

    return SendRequest("/get-direct-link", {track_id: audio.getAttribute("data-track-id")}).then(response => {
        if (response.status != "success") {
            error.innerText = response.message
            return false
        }

        audio.src = response.direct_link
        return true
    })
}

function InitPlayers() {
    let players = {}

    for (let audio of document.getElementsByTagName("audio")) {
        let trackId = audio.getAttribute("data-track-id")

        audio.addEventListener("loadedmetadata", () => {
            let updater = new LyricsUpdater(`lyrics-${trackId}`)
            let player = new Player(`player-${trackId}`, audio, (currentTime) => updater.Update(currentTime))
            player.ResetTimecode()
            player.Init()
            player.Play()
            players[trackId] = player
        })

        audio.addEventListener("play", () => PausePlayers(trackId))
    }

    return players
}

function PausePlayers(targetTrackId) {
    for (let trackId of Object.keys(players))
        if (trackId != targetTrackId)
            players[trackId].Pause()
}

function PlayAudio(trackId) {
    let audio = document.getElementById(`audio-${trackId}`)
    let block = document.getElementById(`play-audio-${trackId}`)

    LoadAudio(audio, `error-${trackId}`).then(success => {
        console.log(success)
        if (!success)
            return

        PausePlayers(trackId)

        block.classList.remove("table-block")
        block.children[1].classList.remove("table-cell")
        block.children[0].remove()
    })
}

function SaveAudio() {
    let artists = GetJSONField("artists", "Некорректно задан исполнитель", "Исполнитель не введён")
    if (artists === null)
        return

    let track = GetTextField("track", "Название не указано")
    if (track === null)
        return


    let lyrics = GetJSONField("lyrics", "Некорректно задан текст")
    if (lyrics === null)
        return

    let year = GetNumberField("year", /^\d+$/g, "Год введён неверно")
    if (year === null)
        return

    let creation = GetMultiSelect("creation", ["russian", "foreign"])
    if (creation === null)
        return

    let audio = document.getElementById("audio")
    let track_id = audio.getAttribute("data-track-id")

    let button = document.getElementById("save-btn")
    let error = document.getElementById("error")
    error.innerText = ""

    SendRequest("/update-audio", {track_id, artists, track, lyrics, year, creation}).then(response => {
        if (response.status != "success") {
            error.innerText = response.message
            return
        }

        button.classList.add("hidden")
    })
}

function RemoveAudio() {
    if (!confirm("Вы уверены, что хотите удалить эту аудиозапись?"))
        return

    let audio = document.getElementById("audio")
    let trackId = audio.getAttribute("data-track-id")
    let error = document.getElementById("error")
    error.innerText = ""

    SendRequest("/remove-audio", {track_id: trackId}).then(response => {
        if (response.status != "success") {
            error.innerText = response.message
            return
        }

        window.close()
    })
}