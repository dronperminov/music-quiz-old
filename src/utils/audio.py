import os
import re
from typing import List

from bs4 import BeautifulSoup
from yandex_music import Client
from yandex_music.exceptions import NotFoundError


def parse_link(link: str) -> str:
    regex = re.compile(r"/album/(?P<album>\d+)/track/(?P<track>\d+)")
    match = regex.search(link)
    album = match.group("album")
    track = match.group("track")
    return f"{track}:{album}"


def parse_lyrics(lyrics_str: str) -> List[dict]:
    lyrics = []

    for line in lyrics_str.split("\n"):
        match = re.search(r"^\[(?P<timecode>\d+:\d+\.\d+)] (?P<text>.*)$", line)
        timecode = match.group("timecode")
        minute, second = timecode.split(":")
        time = round(int(minute) * 60 + float(second), 2)
        text = match.group("text")
        lyrics.append({"time": time, "text": text})

    return lyrics


def parse_yandex_music(html: str, token: str) -> dict:
    if re.fullmatch(r".*/album/\d+/track/\d+", html):
        links = [html]
    else:
        soup = BeautifulSoup(html, "html.parser")
        links = [f'https://music.yandex.ru/{a["href"]}' for a in soup.findAll("a", class_="d-track__title", href=True)]

    client = Client(token).init()
    tracks = client.tracks([parse_link(link) for link in links])
    audios = []

    for track in tracks:
        track_id, album_id = track.track_id.split(":")
        track_name = f"{album_id}_{track_id}.mp3"
        track_path = os.path.join(os.path.dirname(__file__), "..", "..", "web", "audios", track_name)

        if not os.path.isfile(track_path):
            track.download(track_path)

        audio = {
            "album_id": album_id,
            "track_id": track_id,
            "track_name": track_name,
            "title": track.title,
            "artists": [{"id": artist["id"], "name": artist["name"]} for artist in track.artists],
            "lyrics": None
        }

        try:
            lyrics_str = track.get_lyrics("LRC").fetch_lyrics()
            audio["lyrics"] = parse_lyrics(lyrics_str)
        except NotFoundError:
            pass

        audios.append(audio)

    if not audios:
        return {"status": "error", "message": "не удалось распарсить ни одного аудио"}

    return {"status": "success", "audios": audios}
