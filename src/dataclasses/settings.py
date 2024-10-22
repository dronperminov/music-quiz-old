from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

from src import constants
from src.database import database
from src.utils.common import get_default_question_years


@dataclass
class Settings:
    theme: str
    question_years: List[List[int]]
    questions: List[str]
    question_artists: List[str]
    genres: List[str]
    text_languages: List[str]
    prefer_list: List[int]
    ignore_list: List[int]
    last_update: datetime
    show_questions_count: bool
    auto_play: bool
    change_playback_rate: bool
    hits: str

    @classmethod
    def from_dict(cls: "Settings", data: Optional[dict]) -> "Settings":
        if data is None:
            data = {}

        return cls(
            theme=data.get("theme", "light"),
            question_years=data.get("question_years", get_default_question_years()),
            questions=data.get("questions", constants.QUESTIONS),
            question_artists=data.get("question_artists", constants.QUESTION_ARTISTS),
            genres=data.get("genres", constants.GENRES),
            text_languages=data.get("text_languages", constants.TEXT_LANGUAGES),
            prefer_list=data.get("prefer_list", []),
            ignore_list=data.get("ignore_list", []),
            last_update=data.get("last_update", datetime(1900, 1, 1)),
            show_questions_count=data.get("show_questions_count", True),
            auto_play=data.get("auto_play", False),
            change_playback_rate=data.get("change_playback_rate", False),
            hits=data.get("hits", "all")
        )

    def to_dict(self) -> dict:
        return {
            "theme": self.theme,
            "question_years": self.question_years,
            "questions": self.questions,
            "question_artists": self.question_artists,
            "genres": self.genres,
            "text_languages": self.text_languages,
            "prefer_list": self.prefer_list,
            "ignore_list": self.ignore_list,
            "last_update": self.last_update,
            "show_questions_count": self.show_questions_count,
            "auto_play": self.auto_play,
            "change_playback_rate": self.change_playback_rate,
            "hits": self.hits
        }

    def to_audio_query(self) -> dict:
        artist_ids = [artist["id"] for artist in database.artists.find({"genres": {"$in": self.genres}}, {"id": 1})]

        query = {
            "$and": [
                {"$or": [{"year": {"$gte": start_year, "$lte": end_year}} for start_year, end_year in self.question_years]},
                {"artists.id": {"$in": artist_ids}},
                {"creation": {"$in": self.text_languages}},
                self.__question_artists_to_query()
            ]
        }

        if self.prefer_list:
            query["$and"].append({"artists.id": {"$in": self.prefer_list}})

        if self.ignore_list:
            query["$and"].append({"artists.id": {"$nin": self.ignore_list}})

        if self.hits == "only-hits":
            query["$and"].append({"position": {"$exists": True, "$lte": 5}})
        elif self.hits == "no-hits":
            query["$and"].append({"position": {"$exists": True, "$gt": 5}})

        return query

    def to_query(self, question_type: str = "") -> dict:
        question_types = [question_type] if question_type else self.questions

        query = self.to_audio_query()
        query["$and"].append({"$or": [self.question_to_query(question_type) for question_type in question_types]})
        return query

    def question_to_query(self, question_type: str) -> dict:
        if question_type == constants.QUESTION_ARTIST_BY_TRACK:
            return {}

        if question_type == constants.QUESTION_ARTIST_BY_INTRO:
            return {"lyrics": {"$exists": True, "$ne": []}, "lyrics.0.time": {"$gte": constants.INTRODUCTION_TIME}}

        if question_type == constants.QUESTION_NAME_BY_TRACK:
            return {}

        if question_type == constants.QUESTION_LINE_BY_TEXT:
            return {"lyrics": {"$exists": True, "$ne": []}, "creation": ["russian"]}

        if question_type == constants.QUESTION_LINE_BY_CHORUS:
            return {"lyrics": {"$exists": True, "$ne": []}, "chorus": True, "creation": ["russian"]}

        raise ValueError(f'Invalid question_type "{question_type}"')

    def __question_artists_to_query(self) -> dict:
        if self.question_artists == constants.QUESTION_ARTISTS:
            return {}

        if self.question_artists == [constants.QUESTION_ARTISTS_SOLE]:
            return {"artists": {"$size": 1}}

        if self.question_artists == [constants.QUESTION_ARTISTS_FEATS]:
            return {"artists.1": {"$exists": True}}

        raise ValueError(f'Invalid question_artists "{self.question_artists}"')
