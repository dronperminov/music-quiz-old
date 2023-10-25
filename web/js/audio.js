function LoadAudio(audio) {
    let link = audio.getAttribute("data-link")
    let error = document.getElementById("error")

    return SendRequest("/get-direct-link", {track_id: link}).then(response => {
        if (response.status != "success") {
            error.innerText = response.message
            return
        }

        audio.src = response.direct_link
        error.innerText = ""
    })
}

function UpdateLyrics(currentTime) {
    if (lyrics === null)
        return

    for (let line of document.getElementsByClassName("audio-text-line"))
        line.classList.remove("audio-text-line-curr")

    if (currentTime < lyrics[0]["time"])
        return

    let index = 0
    while (index < lyrics.length - 1 && currentTime >= lyrics[index + 1]["time"])
        index++

    let line = document.getElementById(`text-line-${index}`)
    line.classList.add("audio-text-line-curr")
    line.parentNode.scrollTop = line.offsetTop - line.parentNode.offsetTop
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
