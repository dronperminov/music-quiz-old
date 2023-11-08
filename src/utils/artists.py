from collections import defaultdict
from typing import List

from src.database import database
from src.utils.audio import get_lyrics_creation


def get_artists_info(artists: List[dict]) -> dict:
    artist2count = dict()
    for artist in artists:
        artist2count[artist["id"]] = {
            "total": database.audios.count_documents({"artists.id": artist["id"]}),
            "with_lyrics": database.audios.count_documents({"artists.id": artist["id"], "lyrics": {"$exists": True, "$ne": []}}),
        }

    return artist2count


def get_artists_creation(artist_ids: List[int]) -> dict:
    audios = database.audios.find({"artists": {"$size": 1}, "artists.id": {"$in": artist_ids}, "lyrics": {"$exists": True, "$ne": []}}, {"artists": 1, "lyrics": 1})
    artist2creation = defaultdict(set)

    for audio in audios:
        creation = get_lyrics_creation(audio["lyrics"])

        for artist in audio["artists"]:
            artist2creation[artist["id"]].update(creation)

    return artist2creation


def get_artists_by_track_ids(track_ids: List[str]) -> List[int]:
    audios = database.audios.find({"track_id": {"$in": track_ids}}, {"artists": 1})
    artists = {artist["id"] for audio in audios for artist in audio["artists"]}
    return list(artists)
