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

    if (inputType == "textarea")
        return MakeElement("basic-textarea default-textarea", inputBlock, {tag: "textarea", "rows": Math.min(10, Math.max(inputValue.length, 2)), innerHTML: inputValue.join("\n"), placeholder: placeholder, name: label})

    if (inputType == "multi-select")
        return MakeMultiSelect("basic-multi-select default-multi-select", inputBlock, placeholder, label,inputValue)

    if (inputType == "audio")
        return MakeElement("", inputBlock, {tag: "audio", controls: "", src: `/audios/${inputValue}`, "data-link": inputValue, "preload": "none", name: label})
}
