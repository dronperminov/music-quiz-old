function LoadAudio(audio, errorId = "error") {
    let error = document.getElementById(errorId)
    error.innerText = ""

    if (audio.hasAttribute("data-src")) {
        return new Promise((resolve, reject) => {
            audio.src = audio.getAttribute("data-src")
            resolve(true)
        })
    }

    return SendRequest("/get-direct-link", {track_id: audio.getAttribute("data-link")}).then(response => {
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
        let link = audio.getAttribute("data-link")

        audio.addEventListener("loadedmetadata", () => {
            let updater = new LyricsUpdater(`lyrics-${link}`)
            let player = new Player(`player-${link}`, audio, (currentTime) => updater.Update(currentTime))
            player.ResetTimecode()
            player.Init()
            player.Play()
            players[link] = player
        })

        audio.addEventListener("play", () => PausePlayers(link))
    }

    return players
}

function PausePlayers(targetLink) {
    for (let link of Object.keys(players))
        if (link != targetLink)
            players[link].Pause()
}

function PlayAudio(link) {
    let audio = document.getElementById(`audio-${link}`)
    let block = document.getElementById(`play-audio-${link}`)

    LoadAudio(audio, `error-${link}`).then(success => {
        console.log(success)
        if (!success)
            return

        PausePlayers(link)

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
    let link = audio.getAttribute("data-link")

    let button = document.getElementById("save-btn")
    let error = document.getElementById("error")
    error.innerText = ""

    SendRequest("/update-audio", {link, artists, track, lyrics, year, creation}).then(response => {
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
    let link = audio.getAttribute("data-link")
    let error = document.getElementById("error")
    error.innerText = ""

    SendRequest("/remove-audio", {link: link}).then(response => {
        if (response.status != "success") {
            error.innerText = response.message
            return
        }

        window.close()
    })
}