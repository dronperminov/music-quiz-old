import re
from typing import List

from bs4 import BeautifulSoup
from yandex_music import Client, Track
from yandex_music.exceptions import NotFoundError

TRACK_REGEX = re.compile(r"^.*/album/(?P<album>\d+)/track/(?P<track>\d+)(\?.*)?$")
PLAYLIST_REGEX = re.compile(r"^.*/users/(?P<username>[-\w]+)/playlists/(?P<playlist_id>\d+)(\?.*)?$")


def parse_link(link: str) -> str:
    regex = re.compile(r"/album/(?P<album>\d+)/track/(?P<track>\d+)")
    match = regex.search(link)
    album = match.group("album")
    track = match.group("track")
    return f"{track}:{album}"


def get_tracks(code: str, client: Client) -> List[Track]:
    tracks = []

    for line in code.split("\n"):
        line = line.strip()

        if not line:
            continue

        if match := TRACK_REGEX.search(line):
            tracks.extend(client.tracks([f'{match.group("track")}:{match.group("album")}']))
            continue

        if match := PLAYLIST_REGEX.search(line):
            playlist = client.users_playlists(match.group("playlist_id"), match.group("username"))
            tracks.extend(track.track for track in playlist.tracks)
            continue

    if tracks:
        return tracks

    soup = BeautifulSoup(code, "html.parser")
    links = [f'https://music.yandex.ru/{a["href"]}' for a in soup.findAll("a", class_="d-track__title", href=True)]
    return client.tracks([parse_link(link) for link in links])


def parse_lyrics(lyrics_str: str) -> List[dict]:
    lyrics = []

    for line in lyrics_str.split("\n"):
        match = re.search(r"^\[(?P<timecode>\d+:\d+\.\d+)] (?P<text>.*)$", line)
        text = match.group("text")

        if not text:
            continue

        timecode = match.group("timecode")
        minute, second = timecode.split(":")
        time = round(int(minute) * 60 + float(second), 2)
        lyrics.append({"time": time, "text": text})

    return lyrics


def parse_yandex_music(code: str, token: str) -> dict:
    client = Client(token).init()
    audios = []

    for track in get_tracks(code, client):
        track_id, album_id = track.track_id.split(":")
        track_name = f"{album_id}_{track_id}.mp3"

        info = track.get_specific_download_info("mp3", 192)
        direct_link = info.get_direct_link()

        audio = {
            "album_id": album_id,
            "track_id": track_id,
            "track_name": track_name,
            "title": track.title,
            "direct_link": direct_link,
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
