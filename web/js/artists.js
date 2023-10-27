function SearchArtists() {
    let queryInput = document.getElementById("query")
    let query = queryInput.value.trim()
    queryInput.value = query

    let params = [`query=${query}`]

    for (let genre of GetMultiSelectNames("genres"))
        if (document.getElementById(`genres-${genre}`).checked)
            params.push(`genres=${genre}`)

    for (let creation of GetMultiSelectNames("creation"))
        if (document.getElementById(`creation-${creation}`).checked)
            params.push(`creation=${creation}`)

    window.location = `/artists?${params.join("&")}`
}

function SwitchArtistQuestion(artistId) {
    let error = document.getElementById(`error-${artistId}`)
    let icon = document.getElementById(`artist-question-${artistId}`)
    error.innerText = ""

    SendRequest("/artist-to-questions", {artist_id: artistId}).then(response => {
        if (response.status != "success") {
            error.innerText = response.message
            return
        }

        if (response.include)
            icon.classList.add("artist-question-selected-icon")
        else
            icon.classList.remove("artist-question-selected-icon")
    })
}
