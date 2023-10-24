function LoadAudio(audio) {
    let link = audio.getAttribute("data-link")
    let error = document.getElementById(`error-${link}`)
    let btn = document.getElementById("load-audios-btn")

    return SendRequest("/get-direct-link", {track_id: link}).then(response => {
        if (response.status != "success") {
            error.innerText = response.message
            return false
        }

        audio.src = response.direct_link
        btn.classList.remove("hidden")
        error.innerText = ""
        return true
    })
}

function LoadAudios() {
    let btn = document.getElementById("load-audios-btn")
    btn.setAttribute("disabled", "")

    let fetches = []
    for (let audio of document.getElementsByTagName("audio"))
        fetches.push(LoadAudio(audio))

    Promise.all(fetches).then((results) => {
        btn.removeAttribute("disabled")

        if (results.indexOf(false) == -1)
            btn.classList.add("hidden")
    })
}

function GetCreation() {
}

function SaveArtist(artistId) {
    let creation = GetMultiSelect("creation", ["russian", "foreign"], "Творчество не выбрано")

    if (creation === null)
        return

    let genres = GetMultiSelect("genres", ["rock", "pop", "hip-hop"])

    if (genres === null)
        return

    let button = document.getElementById("save-btn")
    let error = document.getElementById("error")
    error.innerText = ""

    SendRequest("/edit-artist", {artist_id: artistId, creation: creation, genres: genres}).then(response => {
        if (response.status != "success") {
            error.innerText = response.message
            return
        }

        button.classList.add("hidden")
    })
}

function RemoveAudio(link) {
    if (!confirm("Вы уверены, что хотите удалить эту аудиозапись?"))
        return

    let block = document.getElementById(`audio-${link}`)
    let error = document.getElementById(`error-${link}`)
    error.innerText = ""

    SendRequest("/remove-audio", {link: link}).then(response => {
        if (response.status != "success") {
            error.innerText = response.message
            return
        }

        block.remove()
    })
}
