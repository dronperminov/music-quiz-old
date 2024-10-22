function LoadProfileImage() {
    let input = document.getElementById("profile-input")
    input.click()
}

function UpdateProfileImage(e) {
    let error = document.getElementById("error")
    let input = document.getElementById("profile-input")
    let image = document.getElementById("profile-image")
    image.src = URL.createObjectURL(input.files[0])

    let formData = new FormData()
    formData.append("image", input.files[0])

    error.innerText = ""

    SendRequest("/update-avatar", formData).then(response => {
        if (response.status != "success") {
            error.innerText = response.message
            return
        }
    })
}

function ChangeTheme() {
    let theme = document.getElementById("theme").value
    let html = document.getElementsByTagName("html")[0]
    html.setAttribute("data-theme", theme)

    let themeColors = {
        "dark": "#1e2027",
        "light": "#f7e06e"
    }

    let themeColor = document.querySelector('meta[name="theme-color"]')
    themeColor.setAttribute("content", themeColors[theme])

    ShowSaveButton()
}

function SaveSettings() {
    let fullname = GetTextField("fullname", "Полное имя не заполнено")
    if (fullname === null)
        return

    let showQuestionsCount = GetMultiSelect("show-questions-count", null)
    if (showQuestionsCount === null)
        return

    let autoPlay = GetMultiSelect("auto-play", null)
    if (autoPlay === null)
        return

    let changePlaybackRate = GetMultiSelect("change-playback-rate", null)
    if (changePlaybackRate === null)
        return

    let questionYears = GetMultiSelect("question-years", null, "Не выбран ни один год выхода")
    if (questionYears === null)
        return

    let questions = GetMultiSelect("questions", ["artist_by_track", "artist_by_intro", "name_by_track", "line_by_text", "line_by_chorus"], "Не выбран ни один тип вопросов")
    if (questions === null)
        return

    let questionArtists = GetMultiSelect("question-artists", ["sole", "feats"], "Не выбран ни один вид исполнителей в вопросах")
    if (questionArtists === null)
        return

    let genres = GetMultiSelect("genres", null, "Не выбран ни один жанр")
    if (genres === null)
        return

    let textLanguages = GetMultiSelect("text-languages", ["russian", "foreign"], "Не выбран ни один язык")
    if (textLanguages === null)
        return

    let preferList = GetMultiSelect("prefer-list", null)
    if (preferList === null)
        return

    let ignoreList = GetMultiSelect("ignore-list", null)
    if (ignoreList === null)
        return

    let data = {
        fullname: fullname,
        theme: document.getElementById("theme").value,
        question_years: questionYears.map((value) => value.split("-").map(v => +v)),
        questions: questions,
        question_artists: questionArtists,
        genres: genres,
        text_languages: textLanguages,
        prefer_list: preferList.map(artist => +artist),
        ignore_list: ignoreList.map(artist => +artist),
        show_questions_count: showQuestionsCount.length > 0,
        auto_play: autoPlay.length > 0,
        change_playback_rate: changePlaybackRate.length > 0,
        hits: document.getElementById("hits").value
    }

    let button = document.getElementById("save-btn")
    let error = document.getElementById("error")
    let info = document.getElementById("info")
    error.innerText = ""
    info.innerText = ""

    SendRequest("/update-settings", data).then(response => {
        if (response.status != "success") {
            error.innerText = response.message
            return
        }

        button.classList.add("hidden")
        info.innerText = `Настройкам соответствует ${response.audios_count} ${GetWordForm(response.audios_count, ["аудиозаписей", "аудиозаписи", "аудиозапись"])}`
    })
}

function UpdateActionsVisibility() {
    let block = document.getElementById("actions")

    if (block.children.length < 3)
        block.classList.add("hidden")
    else
        block.classList.remove("hidden")
}

function ResetStatistic() {
    if (!confirm("Вы уверены, что хотите сбросить всю статистику? Отменить данное действие будет невозможно!"))
        return

    let button = document.getElementById("reset-statistic-btn")
    let error = document.getElementById("actions-error")
    error.innerText = ""

    SendRequest("/clear-statistic", {}).then(response => {
        if (response.status != "success") {
            error.innerText = response.message
            return
        }

        button.remove()
        UpdateActionsVisibility()
    })
}
