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

function ChangeField(inputId) {
    let input = document.getElementById(inputId)
    let icon = document.getElementById(`${inputId}-icon`)
    let error = document.getElementById("error")

    input.classList.remove("error-input")
    icon.classList.remove("error-icon")
    error.innerText = ""
}

function ChangeTheme() {
    let theme = document.getElementById("theme").value
    let html = document.getElementsByTagName("html")[0]
    html.setAttribute("data-theme", theme)

    let themeColors = {
        "dark": "#825ce0",
        "light": "#825ce0"
    }

    let themeColor = document.querySelector('meta[name="theme-color"]')
    themeColor.setAttribute("content", themeColors[theme])
}

function SaveSettings() {
    let fullname = GetTextField("fullname", "Полное имя не заполнено")

    if (fullname === null)
        return

    let theme = document.getElementById("theme").value
    let error = document.getElementById("error")

    error.innerText = ""

    SendRequest("/settings", {"fullname": fullname, "theme": theme}).then(response => {
        if (response.status != "success") {
            error.innerText = response.message
            return
        }
    })
}
