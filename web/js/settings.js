function GetTextField(inputId, errorMessage) {
    let input = document.getElementById(inputId)
    let icon = document.getElementById(`${inputId}-icon`)
    let value = input.value.trim()
    let error = document.getElementById("error")

    input.value = value

    if (value === "") {
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

function LoadProfileImage() {
    let input = document.getElementById("profile-input")
    input.click()
}

function UpdateProfileImage(e) {
    let input = document.getElementById("profile-input")
    let image = document.getElementById("profile-image")
    image.src = URL.createObjectURL(input.files[0])

    ShowSaveButton()
}

function ShowSaveButton() {
    let button = document.getElementById("save-btn")
    button.classList.remove("hidden")
}

function ChangeField(inputId) {
    let input = document.getElementById(inputId)
    let icon = document.getElementById(`${inputId}-icon`)
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

function SaveSettings() {
    let fullname = GetTextField("fullname", "Полное имя не заполнено")

    if (fullname === null)
        return

    let theme = document.getElementById("theme").value
    let input = document.getElementById("profile-input")
    let error = document.getElementById("error")
    let button = document.getElementById("save-btn")

    let formData = new FormData()
    formData.append("fullname", fullname)
    formData.append("theme", theme)

    if (input.files.length == 1)
        formData.append("image", input.files[0])

    error.innerText = ""

    SendRequest("/settings", formData).then(response => {
        if (response.status != "success") {
            error.innerText = response.message
            return
        }

        button.classList.add("hidden")
    })
}
