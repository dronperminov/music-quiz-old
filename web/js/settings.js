function GetYears() {
    let icon = document.getElementById("years-icon")
    let error = document.getElementById("error")

    let startYearInput = document.getElementById("years-start")
    let endYearInput = document.getElementById("years-end")

    if (startYearInput.value.match(/^\d\d\d\d$/g) === null) {
        error.innerText = "Начало периода введено некорректно"
        startYearInput.focus()
        startYearInput.classList.add("error-input")
        icon.classList.add("error-icon")
        return null
    }

    if (endYearInput.value.match(/^\d\d\d\d$/g) === null) {
        error.innerText = "Конец периода введён некорректно"
        endYearInput.focus()
        endYearInput.classList.add("error-input")
        icon.classList.add("error-icon")
        return null
    }

    let year1 = Math.max(+startYearInput.min, Math.min(+startYearInput.max, +startYearInput.value))
    let year2 = Math.max(+endYearInput.min, Math.min(+endYearInput.max, +endYearInput.value))

    let startYear = Math.min(year1, year2)
    let endYear = Math.max(year1, year2)

    startYearInput.value = startYear
    endYearInput.value = endYear

    startYearInput.classList.remove("error-input")
    endYearInput.classList.remove("error-input")
    icon.classList.remove("error-icon")

    return {
        start: Math.min(startYear, endYear),
        end: Math.max(startYear, endYear)
    }
}

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

    let years = GetYears()
    if (years === null)
        return

    let questions = GetMultiSelect("questions", ["artist_by_track", "artist_by_intro", "name_by_track", "line_by_text", "line_by_chorus"], "Не выбран ни один тип вопросов")
    if (questions === null)
        return

    let questionArtists = GetMultiSelect("question-artists", ["sole", "feats"], "Не выбран ни один вид исполнителей в вопросах")
    if (questionArtists === null)
        return

    let data = {
        fullname: fullname,
        theme: document.getElementById("theme").value,
        questions: questions,
        question_artists: questionArtists,
        start_year: years.start,
        end_year: years.end
    }

    let button = document.getElementById("save-btn")
    let error = document.getElementById("error")
    error.innerText = ""

    SendRequest("/update-settings", data).then(response => {
        if (response.status != "success") {
            error.innerText = response.message
            return
        }

        button.classList.add("hidden")
    })
}
