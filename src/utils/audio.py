import re
from typing import Dict, List

from bs4 import BeautifulSoup
from yandex_music import Artist, Client
from yandex_music.exceptions import NotFoundError

from src import constants
from src.utils.artists import get_lyrics_creation

TRACK_REGEX = re.compile(r"^.*/album/(?P<album>\d+)/track/(?P<track>\d+)(\?.*)?$")
PLAYLIST_REGEX = re.compile(r"^.*/users/(?P<username>[-\w]+)/playlists/(?P<playlist_id>\d+)(\?.*)?$")


def parse_link(link: str) -> str:
    regex = re.compile(r"/album/(?P<album>\d+)/track/(?P<track>\d+)")
    match = regex.search(link)
    album = match.group("album")
    track = match.group("track")
    return f"{track}:{album}"


def get_track_ids(code: str, token: str) -> List[str]:
    client = Client(token).init()
    tracks = []

    for line in code.split("\n"):
        line = line.strip()

        if not line:
            continue

        if match := TRACK_REGEX.search(line):
            tracks.append(f'{match.group("track")}:{match.group("album")}')
            continue

        if match := PLAYLIST_REGEX.search(line):
            playlist = client.users_playlists(match.group("playlist_id"), match.group("username"))
            tracks.extend(track.track.track_id for track in playlist.tracks)
            continue

    if tracks:
        return tracks

    soup = BeautifulSoup(code, "html.parser")
    links = [f'https://music.yandex.ru/{a["href"]}' for a in soup.findAll("a", class_="d-track__title", href=True)]
    return [parse_link(link) for link in links]


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


def parse_artists(artists: List[Artist]) -> List[dict]:
    parsed_artists = []

    for artist in artists:
        parsed_artists.append({"id": artist["id"], "name": artist["name"]})

        if not artist.decomposed:
            continue

        for decomposed_artist in artist.decomposed:
            if isinstance(decomposed_artist, Artist):
                parsed_artists.append({"id": decomposed_artist["id"], "name": decomposed_artist["name"]})

    return parsed_artists


def parse_tracks(track_ids: List[str], token: str, make_link: bool) -> List[dict]:
    client = Client(token).init()
    audios = []

    for track in client.tracks(track_ids):
        track_id, album_id = track.track_id.split(":")

        audio = {
            "album_id": album_id,
            "track_id": track_id,
            "title": track.title,
            "artists": parse_artists(track.artists),
            "year": 0,
            "lyrics": None,
            "creation": []
        }

        album = client.albums([album_id])[0]
        if album.year:
            audio["year"] = album.year

        if make_link:
            info = track.get_specific_download_info("mp3", 192)
            audio["direct_link"] = info.get_direct_link()

        try:
            lyrics_str = track.get_lyrics("LRC").fetch_lyrics()
            audio["lyrics"] = parse_lyrics(lyrics_str)
            audio["creation"] = get_lyrics_creation(audio["lyrics"])
        except NotFoundError:
            pass

        audios.append(audio)

    return audios


def parse_direct_link(track_id: str, token: str) -> str:
    client = Client(token).init()
    track = client.tracks([track_id])[0]
    info = track.get_specific_download_info("mp3", 192)
    return info.get_direct_link()


def parse_artist_genres(artist_ids: List[int], token: str) -> Dict[int, List[str]]:
    client = Client(token)
    genres = dict()

    for artist_id, artist in zip(artist_ids, client.artists(artist_ids)):
        if not artist.genres:
            genres[artist_id] = []
            continue

        artist_genres = set()

        for genre in artist.genres:
            if genre in constants.ROCK_GENRES:
                artist_genres.add(constants.ROCK_GENRE)
            elif genre in constants.POP_GENRES:
                artist_genres.add(constants.POP_GENRE)
            elif genre in constants.HIP_HOP_GENRES:
                artist_genres.add(constants.HIP_HOP_GENRE)

        genres[artist_id] = list(artist_genres)

    return genres
