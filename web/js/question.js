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

function ShowAnswer(player) {
    let button = document.getElementById("show-btn")
    let answer = document.getElementById("answer")
    answer.classList.remove("hidden")
    button.remove()

    let audio = document.getElementById("audio")
    let timecode = audio.getAttribute("data-answer-timecode")
    player.ParseTimecode(timecode)
}

function MakeFullTrack(player) {
    let block = document.getElementById("full-track")
    block.remove()

    player.ResetTimecode()
}
