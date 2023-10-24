function Player(audio, onUpdate) {
    this.audio = audio
    this.onUpdate = onUpdate

    this.controls = document.getElementById("player-controls")
    this.playIcon = document.getElementById("player-play-icon")
    this.pauseIcon = document.getElementById("player-pause-icon")

    this.progressBar = document.getElementById("player-progress-bar")
    this.currentProgress = document.getElementById("player-current-progress")
    this.time = document.getElementById("player-time")

    this.InitEvents()
    this.ResetTimecode()
    this.UpdateLoop()
}

Player.prototype.InitEvents = function() {
    this.pressed = false

    this.playIcon.addEventListener("click", () => this.Play())
    this.pauseIcon.addEventListener("click", () => this.Pause())

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

    this.UpdateProgressBar()
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
    if (this.audio.currentTime >= this.endTime)
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
