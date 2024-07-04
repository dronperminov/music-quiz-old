import re
from collections import defaultdict
from typing import List

from yandex_music import Client, exceptions

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


def get_artist_form(artist_id: int, client: Client, max_retries: int = 3) -> str:
    text = ""

    for _ in range(max_retries):
        try:
            info = client._request.get(f"{client.base_url}/artists/{artist_id}/brief-info")["artist"]
            text = info.get("description", {"text": "<none>"})["text"].replace("\n", " ")
            break
        except TypeError:
            text = "<error>"
            break
        except exceptions.TimedOutError:
            text = "<timeout error>"

    form2variant = {
        "group": ["группа"],
        "singer_man": ["певец"],
        "singer_woman": ["певица"],
        "artist_man": ["исполнитель", "рэпер"],
        "artist_woman": ["исполнительница", "рэперша"],
        "musician": ["музыкант"],
        "project": ["проект"],
        "duet": ["дуэт"],
        "trio": ["трио"],
        "dj": ["диджей", "ди-джей"],
        "via": ["вокально-инструментальный ансамбль", "виа"],
        "composer": ["композитор"]
    }

    variant2form = {}

    for form, form_variants in form2variant.items():
        for variant in form_variants:
            variant2form[variant] = form

    variants = []
    for variant in form2variant.values():
        variants.extend(variant)

    matched_variants = re.findall(rf'\b({"|".join(variants)})\b', text.lower())

    if len(matched_variants) > 0:
        return variant2form[matched_variants[0]]

    return "default"
