function SwitchForm(signUp) {
    let signInTypeButton = document.getElementById("sign-in-type-button")
    let signUpTypeButton = document.getElementById("sign-up-type-button")
    let signInButton = document.getElementById("sign-in-button")
    let signUpButton = document.getElementById("sign-up-button")

    if (signUp) {
        signInTypeButton.classList.remove("login-type-button-selected")
        signUpTypeButton.classList.add("login-type-button-selected")
        signInButton.classList.add("hidden")
        signUpButton.classList.remove("hidden")
    }
    else {
        signInTypeButton.classList.add("login-type-button-selected")
        signUpTypeButton.classList.remove("login-type-button-selected")
        signInButton.classList.remove("hidden")
        signUpButton.classList.add("hidden")
    }

    for (let block of document.getElementsByClassName("sign-up")) {
        if (signUp)
            block.classList.remove("hidden")
        else
            block.classList.add("hidden")
    }
}

function ClearError(inputId) {
    let input = document.getElementById(inputId)
    let icon = document.getElementById(`${inputId}-icon`)
    let error = document.getElementById("error")

    input.classList.remove("error-input")
    icon.classList.remove("error-icon")
    error.innerText = ""
}

function GetTextField(inputId, errorMessage) {
    let input = document.getElementById(inputId)
    let icon = document.getElementById(`${inputId}-icon`)
    let value = input.value.trim()
    let error = document.getElementById("error")

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

function GetPassword() {
    let password = GetTextField("password", "Пароль не заполнен")

    if (password === null)
        return null

    let passwordCheck = GetTextField("password-check", "Подтверждение пароля не заполнено")

    if (passwordCheck === null)
        return null

    let error = document.getElementById("error")
    let passwordInput = document.getElementById("password")
    let passwordCheckInput = document.getElementById("password-check")
    let passwordIcon = document.getElementById("password-icon")
    let passwordCheckIcon = document.getElementById("password-check-icon")

    if (password == passwordCheck)
        return password

    error.innerText = "Введённые пароли не совпадают"
    passwordInput.classList.add("error-input")
    passwordCheckInput.classList.add("error-input")
    passwordCheckInput.focus()

    passwordIcon.classList.add("error-icon")
    passwordCheckIcon.classList.add("error-icon")
    return null
}

function TryAutoSignIn() {
    let token = localStorage.getItem("music_quiz_token")

    if (token === null)
        return

    document.cookie = `music_quiz_token=${token}`
    location.reload()
}

function SignIn() {
    let username = GetTextField("username", "Имя пользователя не заполнено")

    if (username === null)
        return

    let password = GetTextField("password", "Пароль не заполнен")

    if (password === null)
        return

    SendRequest("/sign-in", {"username": username, "password": password}).then(response => {
        if (response.status != "success") {
            let error = document.getElementById("error")
            error.innerText = response.message
            return
        }

        localStorage.setItem("music_quiz_token", response.token)
        window.location.href = "/"
    })
}

function SignUp() {
    let username = GetTextField("username", "Имя пользователя не заполнено")

    if (username === null)
        return

    let fullname = GetTextField("fullname", "Полное имя не заполнено")

    if (fullname === null)
        return

    let password = GetPassword()

    if (password === null)
        return

    SendRequest("/sign-up", {"username": username, "password": password, "fullname": fullname}).then(response => {
        if (response.status != "success") {
            let error = document.getElementById("error")
            error.innerText = response.message
            return
        }

        localStorage.setItem("music_quiz_token", response.token)
        window.location.href = "/"
    })
}

function KeyPress(e) {
    if (event.key != "Enter")
        return

    e.preventDefault()
    let signInButton = document.getElementById("sign-in-button")

    if (signInButton.classList.contains("hidden")) {
        SignUp()
    }
    else {
        SignIn()
    }
}