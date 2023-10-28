function Player(playerId, audio, onUpdate, onNext = null) {
    this.audio = audio
    this.onUpdate = onUpdate
    this.onNext = onNext

    let block = document.getElementById(playerId)
    this.controls = block.getElementsByClassName("player-controls")[0]
    this.playIcon = block.getElementsByClassName("player-play-icon")[0]
    this.pauseIcon = block.getElementsByClassName("player-pause-icon")[0]
    this.nextIcon = block.getElementsByClassName("player-next-icon")[0]

    this.progressBar = block.getElementsByClassName("player-progress-bar")[0]
    this.currentProgress = block.getElementsByClassName("player-current-progress")[0]
    this.time = block.getElementsByClassName("player-time")[0]

    this.InitEvents()
    this.ResetTimecode()
    this.UpdateLoop()
}

Player.prototype.InitEvents = function() {
    this.pressed = false

    this.playIcon.addEventListener("click", () => this.Play())
    this.pauseIcon.addEventListener("click", () => this.Pause())

    if (this.onNext !== null)
        this.nextIcon.addEventListener("click", () => this.onNext())

    this.progressBar.parentNode.addEventListener("touchstart", (e) => this.ProgressMouseDown(e.touches[0].clientX - this.progressBar.parentNode.offsetLeft))
    this.progressBar.parentNode.addEventListener("touchmove", (e) => this.ProgressMouseMove(e.touches[0].clientX - this.progressBar.parentNode.offsetLeft))
    this.progressBar.parentNode.addEventListener("touchend", (e) => this.ProgressMouseUp())

    this.progressBar.parentNode.addEventListener("mousedown", (e) => this.ProgressMouseDown(e.offsetX))
    this.progressBar.parentNode.addEventListener("mousemove", (e) => this.ProgressMouseMove(e.offsetX))
    this.progressBar.parentNode.addEventListener("mouseup", (e) => this.ProgressMouseUp())
    this.progressBar.parentNode.addEventListener("mouseleave", (e) => this.ProgressMouseUp())
}

Player.prototype.UpdateLoop = function() {
    if (!this.audio.paused)
        this.UpdateProgressBar()

    window.requestAnimationFrame(() => this.UpdateLoop())
}

Player.prototype.Init = function() {
    this.audio.currentTime = this.startTime
    this.audio.pause()

    this.controls.classList.remove("player-hidden")
    this.playIcon.classList.remove("player-hidden")
    this.pauseIcon.classList.add("player-hidden")
    this.time.classList.remove("player-hidden")

    if (this.onNext !== null)
        this.nextIcon.classList.remove("player-hidden")

    this.UpdateProgressBar()
}

Player.prototype.Hide = function() {
    this.controls.classList.add("player-hidden")
    this.playIcon.classList.add("player-hidden")
    this.pauseIcon.classList.add("player-hidden")
    this.nextIcon.classList.add("player-hidden")
    this.time.classList.add("player-hidden")
}

Player.prototype.ParseTimecode = function(timecode) {
    this.startTime = 0
    this.endTime = this.audio.duration

    if (timecode != "") {
        let parts = timecode.split(",")
        this.startTime = +parts[0]

        if (parts.length > 1)
            this.endTime = +parts[1]
    }

    this.UpdateProgressBar()
}

Player.prototype.ResetTimecode = function() {
    this.startTime = 0
    this.endTime = this.audio.duration

    this.UpdateProgressBar()
}

Player.prototype.TimeToString = function(time) {
    let seconds = `${Math.floor(time) % 60}`.padStart(2, '0')
    let minutes = `${Math.floor(time / 60)}`.padStart(2, '0')
    return `${minutes}:${seconds}`
}

Player.prototype.UpdateProgressBar = function() {
    if ((this.audio.currentTime >= this.endTime || this.audio.ended) && this.onNext === null)
        this.audio.currentTime = this.startTime

    if (this.onUpdate !== null)
        this.onUpdate(this.audio.currentTime)

    let currentTime = this.audio.currentTime - this.startTime
    let duration = this.endTime - this.startTime

    this.currentProgress.style.width = `${(currentTime / duration) * 100}%`
    this.time.innerText = `${this.TimeToString(currentTime)} / ${this.TimeToString(duration)}`
}

Player.prototype.Play = function() {
    this.playIcon.classList.add("player-hidden")
    this.pauseIcon.classList.remove("player-hidden")
    this.audio.play()
}

Player.prototype.Pause = function() {
    this.playIcon.classList.remove("player-hidden")
    this.pauseIcon.classList.add("player-hidden")
    this.audio.pause()
}

Player.prototype.Seek = function(time) {
    this.audio.currentTime = time
    this.UpdateProgressBar()
}

Player.prototype.ProgressMouseDown = function(x) {
    let part = x / this.progressBar.clientWidth
    this.audio.currentTime = this.startTime + part * (this.endTime - this.startTime)
    this.audio.pause()
    this.pressed = true

    this.UpdateProgressBar()
}

Player.prototype.ProgressMouseMove = function(x) {
    if (!this.pressed)
        return

    let part = x / this.progressBar.clientWidth
    this.audio.currentTime = this.startTime + part * (this.endTime - this.startTime)
    this.UpdateProgressBar()
}

Player.prototype.ProgressMouseUp = function() {
    if (!this.pressed)
        return

    this.pressed = false

    if (this.playIcon.classList.contains("player-hidden"))
        this.audio.play()
}
