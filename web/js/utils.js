async function SendRequest(url, data = null) {
    try {
        let params = {
            method: data == null ? 'GET' : 'POST',
            mode: 'cors',
            cache: 'no-cache',
            credentials: 'same-origin',
            redirect: 'follow',
            referrerPolicy: 'no-referrer'
        }

        let isForm = data !== null && data instanceof FormData

        if (data != null)
            params.body = isForm ? data : JSON.stringify(data)

        if (!isForm)
            params.headers = {'Content-Type': 'application/json'}

        const response = await fetch(url, params)

        if (response?.ok)
            return await response.json()

        const error = await response.json()
        return {"status": "error", "message": error["message"]}
    }
    catch (error) {
        return {"status": "error", "message": error}
    }
}

function ClearFormRowError(inputId) {
    let input = document.getElementById(inputId)
    let icon = document.getElementById(`${inputId}-icon`)
    let error = document.getElementById("error")

    input.classList.remove("error-input")
    icon.classList.remove("error-icon")
    error.innerText = ""
}

function SetAttributes(element, attributes) {
    if (attributes === null)
        return

    for (let [name, value] of Object.entries(attributes)) {
        if (name == "innerText")
            element.innerText = value
        else if (name == "innerHTML")
            element.innerHTML = value
        else
            element.setAttribute(name, value)
    }
}

function MakeElement(className, parent = null, attributes = null) {
    let tagName = attributes !== null && "tag" in attributes ? attributes["tag"] : "div"
    let element = document.createElement(tagName)
    element.className = className

    SetAttributes(element, attributes)

    if (parent !== null)
        parent.appendChild(element)

    return element
}

function MakeMultiSelect(className, parent, title, name, values) {
    let select = MakeElement(className, parent, {name: name})
    let checkboxes = []

    MakeElement("multi-select-title", select, {innerHTML: title})

    for (let value of values) {
        let row = MakeElement("multi-select-row", select)
        let label = MakeElement("", row, {tag: "label"})
        let checkboxAttributes = {tag: "input", type: "checkbox", name: value["name"]}

        if (value["value"])
            checkboxAttributes["checked"] = ""

        let checkbox = MakeElement("", label, checkboxAttributes)
        let span = MakeElement("", label, {tag: "span", innerText: value["title"]})

        checkboxes.push(checkbox)
    }

    return checkboxes
}

function MakeIconInputRow(parent, iconHTML, inputValue, placeholder, label, inputType = "text") {
    let formBlock = MakeElement("form-row", parent)
    let iconBlock = MakeElement("form-row-icon", formBlock, {innerHTML: iconHTML})
    let inputBlock = MakeElement("form-row-input", formBlock)

    if (inputType == "text")
        return MakeElement("basic-input default-input", inputBlock, {tag: "input", type: "text", value: inputValue, placeholder: placeholder, name: label})

    if (inputType == "number")
        return MakeElement("basic-input default-input", inputBlock, {tag: "input", type: "number", value: inputValue, placeholder: placeholder, name: label, min: 0})

    if (inputType == "textarea")
        return MakeElement("basic-textarea default-textarea", inputBlock, {tag: "textarea", "rows": Math.min(10, Math.max(inputValue.length, 2)), innerHTML: inputValue.join("\n"), placeholder: placeholder, name: label})

    if (inputType == "multi-select")
        return MakeMultiSelect("basic-multi-select default-multi-select", inputBlock, placeholder, label, inputValue)

    if (inputType == "audio")
        return MakeElement("", inputBlock, {tag: "audio", controls: "", src: inputValue, name: label, preload: "metadata"})
}

function StopOtherAudios(target) {
    for (let audio of document.getElementsByTagName("audio"))
        if (audio != target)
            audio.pause()
}

function GetTextField(inputId, errorMessage = "") {
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

function GetJSONField(inputId, parseErrorMessage, errorMessage = "") {
    let input = document.getElementById(inputId)
    let icon = document.getElementById(`${inputId}-icon`)
    let error = document.getElementById("error")
    let value

    if (input.tagName == "TEXTAREA") {
        value = input.value.trim()
        input.value = value
    }
    else {
        let lines = []

        for (let div of input.children) {
            div.innerText = div.innerText.trim()
            lines.push(div.innerText)
        }

        value = lines.join("\n")
    }

    if (value === "" && errorMessage != "") {
        error.innerText = errorMessage
        input.focus()
        input.classList.add("error-input")
        icon.classList.add("error-icon")
        return null
    }

    try {
        value = JSON.parse(`[${value.split("\n").join(",")}]`)
    }
    catch (exception) {
        error.innerText = parseErrorMessage
        input.focus()
        input.classList.add("error-input")
        icon.classList.add("error-icon")
        return null
    }

    input.classList.remove("error-input")
    icon.classList.remove("error-icon")
    return value
}

function GetNumberField(inputId, regex, errorMessage = "") {
    let input = document.getElementById(inputId)
    let icon = document.getElementById(`${inputId}-icon`)
    let value = input.value
    let error = document.getElementById("error")

    if (value.match(regex) === null && errorMessage != "") {
        error.innerText = errorMessage
        input.focus()
        input.classList.add("error-input")
        icon.classList.add("error-icon")
        return null
    }

    if (input.hasAttribute("min"))
        value = Math.max(+value, +input.min)

    if (input.hasAttribute("max"))
        value = Math.min(+value, +input.max)

    input.value = value
    input.classList.remove("error-input")
    icon.classList.remove("error-icon")
    return +value
}

function GetMultiSelect(multiSelectId, names, errorMessage = "") {
    let values = []
    let input = document.getElementById(multiSelectId)
    let icon = document.getElementById(`${multiSelectId}-icon`)
    let error = document.getElementById("error")

    for (let name of names)
        if (document.getElementById(`${multiSelectId}-${name}`).checked)
            values.push(name)

    if (values.length == 0 && errorMessage != "") {
        error.innerText = errorMessage
        input.classList.add("error-input")
        icon.classList.add("error-icon")
        return null
    }

    input.classList.remove("error-input")
    icon.classList.remove("error-icon")
    return values
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
