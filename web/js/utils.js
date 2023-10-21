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

function MakeIconInputRow(parent, iconHTML, inputValue, placeholder, label, inputType = "text") {
    let formBlock = MakeElement("form-row", parent)
    let iconBlock = MakeElement("form-row-icon", formBlock, {innerHTML: iconHTML})
    let inputBlock = MakeElement("form-row-input", formBlock)

    if (inputType == "text")
        return MakeElement("basic-input default-input", inputBlock, {tag: "input", type: "text", value: inputValue, placeholder: placeholder, name: label})

    if (inputType == "textarea")
        return MakeElement("basic-textarea default-textarea", inputBlock, {tag: "textarea", "rows": Math.max(inputValue.length, 2), innerHTML: inputValue.join("\n"), placeholder: placeholder, name: label})

    if (inputType == "audio")
        return MakeElement("", inputBlock, {tag: "audio", controls: "", src: `/audio?link=${inputValue}`, "data-link": inputValue, "preload": "none", name: label})
}
