import re
from typing import Dict, List, Optional

from Levenshtein import ratio
from thefuzz import fuzz
from yandex_music import Artist, Client
from yandex_music.exceptions import NotFoundError

from src import constants

TRACK_REGEX = re.compile(r"^.*/album/(?P<album>\d+)/track/(?P<track>\d+)(\?.*)?$")
TRACK_ONLY_REGEX = re.compile(r"^.*/track/(?P<track>\d+)(\?.*)?$")
PLAYLIST_REGEX = re.compile(r"^.*/users/(?P<username>[-\w]+)/playlists/(?P<playlist_id>\d+)(\?.*)?$")
ARTIST_REGEX = re.compile(r"^.*/artist/(?P<artist>\d+)(/tracks)?(\?.*)?$")
ALBUM_REGEX = re.compile(r"^.*/album/(?P<album>\d+)(/?\?.*)?$")


def get_track_ids(code: str, token: str) -> List[str]:
    client = Client(token).init()
    tracks = []

    for line in code.split("\n"):
        line = line.strip()

        if not line:
            continue

        if match := TRACK_REGEX.search(line):
            tracks.append(match.group("track"))
            continue

        if match := TRACK_ONLY_REGEX.search(line):
            tracks.extend(track.track_id.split(":")[0] for track in client.tracks(f'{match.group("track")}'))
            continue

        if match := PLAYLIST_REGEX.search(line):
            playlist = client.users_playlists(match.group("playlist_id"), match.group("username"))
            tracks.extend(track.track.track_id.split(":")[0] for track in playlist.tracks)
            continue

        if match := ARTIST_REGEX.search(line):
            artist_tracks = client.artists_tracks(match.group("artist"), page_size=500)
            tracks.extend(track.track_id.split(":")[0] for track in artist_tracks.tracks)
            continue

        if match := ALBUM_REGEX.search(line):
            album = client.albums_with_tracks(match.group("album"))

            for volume in album.volumes:
                tracks.extend(track.track_id.split(":")[0] for track in volume)
            continue

    return tracks


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
            "track_id": track_id,
            "title": track.title,
            "artists": parse_artists(track.artists),
            "year": 0,
            "lyrics": None,
            "creation": [],
            "chorus": False,
            "source": "yandex-music"
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
            audio["chorus"] = detect_chorus(audio["lyrics"]) is not None
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
            for target_genre, yandex_genres in constants.GENRE_TO_YANDEX.items():
                if genre in yandex_genres:
                    artist_genres.add(target_genre)

        genres[artist_id] = list(artist_genres)

    return genres


def is_parenthesis_line(line: str) -> bool:
    return re.fullmatch(r"\([^)]+\)", line) is not None


def get_lyrics_creation(lyrics: List[dict]) -> List[str]:
    text = "\n".join(line["text"] for line in lyrics if not is_parenthesis_line(line["text"]))
    eng_matches = len(re.findall(r"[a-zA-Z]", text))
    rus_matches = len(re.findall(r"[а-яА-ЯёЁ]", text))

    creation = []
    if eng_matches > rus_matches:
        creation.append("foreign")

    if rus_matches > 0:
        creation.append("russian")

    return creation


def preprocess_line(line: str) -> str:
    line = line.lower()
    line = re.sub(r"-", "", line)
    return re.sub(r"\s+", " ", line)


def is_equal_lines(line1: str, line2: str) -> bool:
    words1 = re.findall(r"\w+", preprocess_line(line1))
    words2 = re.findall(r"\w+", preprocess_line(line2))
    return ratio(words1, words2) > constants.CHORUS_THRESHOLD


def contain_line(lyrics: List[dict], indices: List[int], text: str) -> bool:
    for index in indices:
        if fuzz.partial_ratio(preprocess_line(text), preprocess_line(lyrics[index]["text"])) > constants.LINE_THRESHOLD:
            return True

    return False


def detect_chorus(lyrics: List[dict]) -> Optional[List[int]]:
    indices = [i for i, line in enumerate(lyrics) if not is_parenthesis_line(line["text"])]
    chorus_start, chorus_length = 0, 0

    for i in range(1, len(indices)):
        diagonal = "".join("1" if is_equal_lines(lyrics[indices[j]]["text"], lyrics[indices[j + i]]["text"]) else " " for j in range(len(indices) - i))

        for match in re.finditer(r"1+", diagonal):
            start, end = match.span()
            if end - start > chorus_length:
                chorus_start, chorus_length = start + i, end - start

    if chorus_length < constants.CHORUS_MIN_LENGTH:
        return None

    chorus_indices = [indices[chorus_start + i] for i in range(chorus_length)]
    if contain_line(lyrics, chorus_indices[:-1], lyrics[chorus_indices[-1]]["text"]):
        return None

    return chorus_indices
