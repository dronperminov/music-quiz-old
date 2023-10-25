import re
from collections import defaultdict
from typing import List, Optional, Set

from src.database import database
from src.dataclasses.artists_query import ArtistsQuery


def escape_query(query: str) -> str:
    alternatives = [re.escape(alternative) for alternative in query.split("|") if alternative]
    return "|".join(alternatives)


def search_to_query(params: ArtistsQuery) -> Optional[dict]:
    if params.query is None and params.genres is None and params.creation is None:
        return None

    query = dict()

    if params.query:
        query["name"] = {"$regex": escape_query(params.query), "$options": "i"}

    and_conditions = []
    if params.genres is not None:
        and_conditions.append({"$or": [{"genres": genre if genre != "no" else []} for genre in params.genres]})

    if params.creation is not None:
        and_conditions.append({"$or": [{"creation": creation if creation != "no" else []} for creation in params.creation]})

    if and_conditions:
        query["$and"] = and_conditions

    return query


def get_artists_info(artists: List[dict]) -> dict:
    artist2count = dict()
    for artist in artists:
        artist2count[artist["id"]] = {
            "total": database.audios.count_documents({"artists.id": artist["id"]}),
            "with_lyrics": database.audios.count_documents({"artists.id": artist["id"], "lyrics": {"$exists": True, "$ne": []}}),
        }

    return artist2count


def is_parenthesis_line(line: str) -> bool:
    return re.fullmatch(r"\([^)]+\)", line) is not None


def get_lyrics_creation(lyrics: List[dict]) -> Set[str]:
    text = "\n".join(line["text"] for line in lyrics if not is_parenthesis_line(line["text"]))
    eng_matches = len(re.findall(r"[a-zA-Z]", text))
    rus_matches = len(re.findall(r"[а-яА-ЯёЁ]", text))

    creation = set()
    if eng_matches > rus_matches:
        creation.add("foreign")

    if rus_matches > 0:
        creation.add("russian")

    return creation


def get_artists_creation(artist_ids: List[int]) -> dict:
    audios = database.audios.find({"artists": {"$size": 1}, "artists.id": {"$in": artist_ids}, "lyrics": {"$exists": True, "$ne": []}}, {"artists": 1, "lyrics": 1})
    artist2creation = defaultdict(set)

    for audio in audios:
        creation = get_lyrics_creation(audio["lyrics"])

        for artist in audio["artists"]:
            artist2creation[artist["id"]].update(creation)

    return artist2creation
