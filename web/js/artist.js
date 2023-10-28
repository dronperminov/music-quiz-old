function GetCreation() {
}

function SaveArtist(artistId) {
    let creation = GetMultiSelect("creation", ["russian", "foreign"], "Творчество не выбрано")

    if (creation === null)
        return

    let genres = GetMultiSelect("genres", null)

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

    let block = document.getElementById(`audio-block-${link}`)
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
