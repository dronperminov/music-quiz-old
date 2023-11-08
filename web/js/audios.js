function GetYears() {
    let error = document.getElementById("error")

    let startYearInput = document.getElementById("years-start")
    let endYearInput = document.getElementById("years-end")

    let startYear = startYearInput.value
    let endYear = endYearInput.value
    let year = new Date().getFullYear()

    if (startYear.match(/^\d+$/g))
        startYear = Math.max(Math.min(+startYear, year), +startYearInput.getAttribute("min")).toString()

    if (endYear.match(/^\d+$/g))
        endYear = Math.max(Math.min(+endYear, year), +endYearInput.getAttribute("min")).toString()

    startYearInput.value = startYear
    endYearInput.value = endYear

    if (startYear.match(/^(\d\d\d\d)?$/g) === null) {
        error.innerText = "Начало периода введено некорректно"
        startYearInput.focus()
        startYearInput.classList.add("error-input")
        return null
    }

    if (endYear.match(/^(\d\d\d\d)?$/g) === null) {
        error.innerText = "Конец периода введён некорректно"
        endYearInput.focus()
        endYearInput.classList.add("error-input")
        return null
    }

    startYearInput.classList.remove("error-input")
    endYearInput.classList.remove("error-input")

    if (startYear.match(/^\d\d\d\d$/g) !== null && endYear.match(/^\d\d\d\d$/g) !== null)
        return {start: Math.min(+startYear, +endYear), end: Math.max(+startYear, +endYear)}

    return {start: startYear, end: endYear}
}

function ChangeYear(inputId) {
    let input = document.getElementById(inputId)
    let error = document.getElementById("error")

    input.classList.remove("error-input")
    error.innerText = ""
}

function SearchAudios() {
    let queryInput = document.getElementById("query")
    let query = queryInput.value.trim()
    queryInput.value = query

    let params = [`query=${query}`]

    let years = GetYears()
    if (years === null)
        return

    if (years.start != "")
        params.push(`start_year=${years.start}`)

    if (years.end != "")
        params.push(`end_year=${years.end}`)

    for (let creation of GetMultiSelectNames("creation"))
        if (document.getElementById(`creation-${creation}`).checked)
            params.push(`creation=${creation}`)

    let lyrics = document.getElementById("lyrics").value
    if (lyrics == "yes")
        params.push("lyrics=true")
    else if (lyrics == "no")
        params.push("lyrics=false")

    window.location = `/audios?${params.join("&")}`   
}

function SeekPlayer(trackId, time) {
    if (!players[trackId])
        return

    players[trackId].Seek(time)
}

function ToggleText(trackId) {
    let block = document.getElementById(`lyrics-${trackId}`)
    let icon = document.getElementById(`lyrics-icon-${trackId}`)
    block.classList.toggle("hidden")
    icon.classList.toggle("lyrics-selected-icon")
}
