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

function SwitchList(artistId, listName) {
    let error = document.getElementById(`error-${artistId}`)
    let preferIcon = document.getElementById(`prefer-list-${artistId}`)
    let ignoreIcon = document.getElementById(`ignore-list-${artistId}`)
    error.innerText = ""

    SendRequest("/artist-to-questions", {artist_id: artistId, list_name: listName}).then(response => {
        if (response.status != "success") {
            error.innerText = response.message
            return
        }

        preferIcon.classList.remove("artist-question-selected-icon")
        ignoreIcon.classList.remove("artist-question-selected-icon")

        if (response.prefer)
            preferIcon.classList.add("artist-question-selected-icon")

        if (response.ignore)
            ignoreIcon.classList.add("artist-question-selected-icon")
    })
}
