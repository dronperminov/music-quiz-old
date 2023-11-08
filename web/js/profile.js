function Play() {
    let audio = document.getElementById("audio")
    let block = document.getElementById("play-audio")

    return LoadAudio(audio).then(success => {
        if (!success)
            return false

        block.classList.remove("table-block")
        block.children[1].classList.remove("table-cell")
        block.children[0].classList.add("hidden")
        return true
    })
}

function MakeLyrics(lyrics) {
    let block = document.getElementById("lyrics").children[0]
    block.innerHTML = ""

    for (let line of lyrics) {
        let lineBlock = MakeElement("audio-text-line", block, {"data-time": line.time, innerText: line.text})
        lineBlock.addEventListener("click", () => player.Seek(line.time))
    }

    if (updater !== null)
        updater.Init()
}

function UpdatePlayer(correct, response) {
    if (!correct)
        return

    let audio = document.getElementById("audio")
    let audioArtist = document.getElementById("audio-artist")
    let caption = document.getElementById("caption")
    let lyrics = document.getElementById("lyrics")

    audioArtist.setAttribute("src", response.artist_src)
    audio.volume = response.artist_src && !audioArtist.ended ? 0.2 : 1

    let artists = response.artists.map((artist) => `<a href="/artists/${artist.id}">${artist.name}</a>`).join(", ")
    caption.innerHTML = `${artists} - ${response.track}`

    if (response.lyrics.length > 0) {
        lyrics.classList.remove("hidden")
        MakeLyrics(response.lyrics)
    }
    else {
        lyrics.classList.add("hidden")
    }

    if ('mediaSession' in navigator) {
        navigator.mediaSession.setPositionState(null)
        navigator.mediaSession.metadata = new MediaMetadata({
            title: response.track,
            artist: response.artists.map((artist) => artist.name).join(", "),
            artwork: []
        });
    }
}

function PlayNext() {
    let audio = document.getElementById("audio")
    let error = document.getElementById("error")
    error.innerText = ""

    SendRequest("/radio-next", {}).then(response => {
        if (response.status != "success") {
            error.innerText = response.message
            return
        }

        audio.removeAttribute("src")
        audio.setAttribute("data-track-id", response.track_id)

        if (response.src !== "")
            audio.setAttribute("data-src", response.src)

        Play().then(correct => UpdatePlayer(correct, response))
    })
}
