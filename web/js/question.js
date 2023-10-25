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

function CheckAnswer(isCorrect) {
    let questionType = document.getElementById("question").getAttribute("data-question-type")
    let link = document.getElementById("audio").getAttribute("data-link")

    let error = document.getElementById("check-answer-error")
    error.innerText = ""

    SendRequest("/add-statistic", {question_type: questionType, link: link, correct: isCorrect}).then(response => {
        if (response.status != "success") {
            error.innerText = response.message
            return
        }

        let block = document.getElementById("check-answer")
        block.remove()
    })
}
