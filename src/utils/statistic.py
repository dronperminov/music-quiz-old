import datetime
from typing import Optional

from src.database import database
from src.utils.common import get_question_form


def get_statistic(username: str, day_start: Optional[datetime.datetime] = None, day_end: Optional[datetime.datetime] = None) -> dict:
    query = {"username": username}

    if day_start is not None and day_end is not None:
        query["datetime"] = {"$gte": day_start, "$lte": day_end}

    statistic = list(database.statistic.find(query, {"username": 0}))
    question_types = {info["question_type"] for info in statistic}
    links = {info["link"] for info in statistic}

    artists = set()
    for audio in database.audios.find({"link": {"$in": list(links)}}, {"artists": 1}):
        for artist in audio["artists"]:
            artists.add(artist["id"])

    return {
        "question_types": len(question_types),
        "questions": len(statistic),
        "questions_form": get_question_form(len(statistic)),
        "correct_tracks": database.statistic.count_documents({**query, "correct": True}),
        "incorrect_tracks": database.statistic.count_documents({**query, "correct": False}),
        "artists": len(artists)
    }
