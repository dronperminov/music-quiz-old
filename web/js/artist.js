function GetCreation() {
}

function SaveArtist(artistId) {
    let creation = GetMultiSelect("creation", ["russian", "foreign"], "Творчество не выбрано")

    if (creation === null)
        return

    let genres = GetMultiSelect("genres", null)

    if (genres === null)
        return

    let form = document.getElementById("form").value

    let button = document.getElementById("save-btn")
    let error = document.getElementById("error")
    error.innerText = ""

    SendRequest("/edit-artist", {artist_id: artistId, creation: creation, genres: genres, form: form}).then(response => {
        if (response.status != "success") {
            error.innerText = response.message
            return
        }

        button.classList.add("hidden")
    })
}

function RemoveAudio(trackId) {
    if (!confirm("Вы уверены, что хотите удалить эту аудиозапись?"))
        return

    let block = document.getElementById(`audio-block-${trackId}`)
    let error = document.getElementById(`error-${trackId}`)
    error.innerText = ""

    SendRequest("/remove-audio", {track_id: trackId}).then(response => {
        if (response.status != "success") {
            error.innerText = response.message
            return
        }

        block.remove()
    })
}
