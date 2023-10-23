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

function ShowSaveButton() {
    let button = document.getElementById("save-btn")
    button.classList.remove("hidden")
}

function ChangeField(inputId) {
    let input = document.getElementById(inputId)
    let icon = document.getElementById(`${inputId}-icon`)
    let error = document.getElementById("error")

    input.classList.remove("error-input")
    icon.classList.remove("error-icon")
    error.innerText = ""

    ShowSaveButton()
}

function GetMultiSelect(multiSelectId, names, errorMessage = "") {
    let values = []
    let input = document.getElementById(multiSelectId)
    let icon = document.getElementById(`${multiSelectId}-icon`)
    let error = document.getElementById("error")

    for (let name of names)
        if (document.getElementById(`${multiSelectId}-${name}`).checked)
            values.push(name)

    if (values.length == 0 && errorMessage != "") {
        error.innerText = errorMessage
        input.classList.add("error-input")
        icon.classList.add("error-icon")
        return null
    }

    input.classList.remove("error-input")
    icon.classList.remove("error-icon")
    return values
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
