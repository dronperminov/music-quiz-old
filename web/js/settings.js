function GetTextField(inputId, errorMessage) {
    let input = document.getElementById(inputId)
    let icon = document.getElementById(`${inputId}-icon`)
    let value = input.value.trim()
    let error = document.getElementById("error")

    input.value = value

    if (value === "" && errorMessage != "") {
        error.innerText = errorMessage
        input.focus()
        input.classList.add("error-input")
        icon.classList.add("error-icon")
        return null
    }

    input.classList.remove("error-input")
    icon.classList.remove("error-icon")
    return value
}

function ToggleToken() {
    let token = document.getElementById("token")
    let hideIcon = document.getElementById("hide-token-icon")
    let showIcon = document.getElementById("show-token-icon")

    hideIcon.classList.toggle("hidden")
    showIcon.classList.toggle("hidden")

    if (token.type == "password")
        token.type = "text"
    else
        token.type = "password"
}

function GetToken() {
    let input = document.getElementById("token")
    let icon = document.getElementById("token-icon")
    let token = input.value.trim()
    let error = document.getElementById("error")

    input.value = token

    if (token === "")
        return token

    if (token.indexOf('"') > -1) {
        error.innerText = "Токен не должен содержать кавычек"
        input.focus()
        input.classList.add("error-input")
        icon.classList.add("error-icon")
        return null
    }

    input.classList.remove("error-input")
    icon.classList.remove("error-icon")
    return token
}

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

function ShowSaveButton() {
    let button = document.getElementById("save-btn")
    button.classList.remove("hidden")
}

function ChangeField(inputId, iconId = null) {
    let input = document.getElementById(inputId)
    let icon = document.getElementById(iconId == null ? `${inputId}-icon` : iconId)
    let error = document.getElementById("error")

    input.classList.remove("error-input")
    icon.classList.remove("error-icon")
    error.innerText = ""

    ShowSaveButton()
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

function SaveSettings(withToken = false) {
    let fullname = GetTextField("fullname", "Полное имя не заполнено")

    if (fullname === null)
        return

    let questions = GetMultiSelect("questions", ["artist_by_track", "artist_by_intro", "name_by_track", "line_by_text", "line_by_chorus"], "Не выбран ни один тип вопросов")

    if (questions === null)
        return

    let years = GetYears()

    if (years === null)
        return

    let data = {
        fullname: fullname,
        theme: document.getElementById("theme").value,
        questions: questions,
        start_year: years.start,
        end_year: years.end
    }

    if (withToken) {
        data.token = GetToken()

        if (data.token === null)
            return
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
