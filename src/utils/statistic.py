import datetime
from typing import Optional

from src import constants
from src.database import database
from src.utils.artists import get_artists_by_audio_links
from src.utils.common import get_word_form


def get_statistic(username: str, day_start: Optional[datetime.datetime] = None, day_end: Optional[datetime.datetime] = None) -> dict:
    query = {"username": username}

    if day_start is not None and day_end is not None:
        query["datetime"] = {"$gte": day_start, "$lte": day_end}

    # общие вопросы
    correct_questions = database.statistic.count_documents({**query, "correct": True})
    incorrect_questions = database.statistic.count_documents({**query, "correct": False})
    total_questions = correct_questions + incorrect_questions

    # вопросы по исполнителям
    artists_questions = list(database.statistic.find({**query, "question_type": {"$in": constants.ARTIST_QUESTIONS}}, {"link": 1, "correct": 1}))
    correct_artists = len(get_artists_by_audio_links([question["link"] for question in artists_questions if question["correct"]]))
    incorrect_artists = len(get_artists_by_audio_links([question["link"] for question in artists_questions if not question["correct"]]))
    total_artists = correct_artists + incorrect_artists

    # вопросы по текстам
    correct_texts = database.statistic.count_documents({**query, "question_type": {"$in": constants.TEXT_QUESTIONS}, "correct": True})
    incorrect_texts = database.statistic.count_documents({**query, "question_type": {"$in": constants.TEXT_QUESTIONS}, "correct": False})
    total_texts = correct_texts + incorrect_texts

    return {
        "questions_form": get_word_form(total_questions, ["вопросов", "вопроса", "вопрос"]),
        "questions": {
            "correct": correct_questions,
            "incorrect": incorrect_questions,
            "total": total_questions
        },
        "artists": {
            "correct": correct_artists,
            "incorrect": incorrect_artists,
            "total": total_artists
        },
        "texts": {
            "correct": correct_texts,
            "incorrect": incorrect_texts,
            "total": total_texts
        }
    }
