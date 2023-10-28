function LyricsUpdater(blockId, deltaTime = 4000) {
    this.block = document.getElementById(blockId)
    this.deltaTime = deltaTime

    if (this.block === null)
        return

    this.Init()

    this.block.addEventListener("wheel", (e) => this.Wheel())
    this.block.addEventListener("resize", (e) => this.Wheel())
    this.block.addEventListener("input", (e) => this.Wheel())
    this.block.addEventListener("touchmove", (e) => this.Wheel())
    this.wheelTime = null
}

LyricsUpdater.prototype.Init = function() {
    this.lines = this.block.getElementsByClassName("audio-text-line")
    this.lyrics = this.GetLyrics()
}

LyricsUpdater.prototype.GetLyrics = function() {
    let lyrics = []

    for (let line of this.lines)
        lyrics.push(+line.getAttribute("data-time"))

    if (lyrics.length == 0)
        return null

    return lyrics
}

LyricsUpdater.prototype.ResetLines = function() {
    for (let line of this.lines)
        line.classList.remove("audio-text-line-curr")
}

LyricsUpdater.prototype.Update = function(currentTime) {
    if (this.block === null || this.lyrics === null)
        return

    this.ResetLines()

    if (currentTime < this.lyrics[0])
        return

    let index = 0
    while (index < this.lyrics.length - 1 && currentTime >= this.lyrics[index + 1])
        index++

    let line = this.lines[index]
    line.classList.add("audio-text-line-curr")

    if (this.wheelTime === null || performance.now() - this.wheelTime > this.deltaTime) {
        line.parentNode.scrollTop = line.offsetTop - line.parentNode.offsetTop
        this.wheelTime = null
    }
}

LyricsUpdater.prototype.Wheel = function() {
    this.wheelTime = performance.now()
}
