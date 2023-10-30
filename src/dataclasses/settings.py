from dataclasses import dataclass
from typing import List

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
    artists: List[int]

    @classmethod
    def from_dict(cls: "Settings", data: dict) -> "Settings":
        theme = data.get("theme", "light")
        question_years = data.get("question_years", get_default_question_years())
        questions = data.get("questions", constants.QUESTIONS)
        question_artists = data.get("question_artists", constants.QUESTION_ARTISTS)
        genres = data.get("genres", constants.GENRES)
        text_languages = data.get("text_languages", constants.TEXT_LANGUAGES)
        artists = data.get("artists", [])
        return cls(theme, question_years, questions, question_artists, genres, text_languages, artists)

    def to_dict(self) -> dict:
        return {
            "theme": self.theme,
            "question_years": self.question_years,
            "questions": self.questions,
            "question_artists": self.question_artists,
            "genres": self.genres,
            "text_languages": self.text_languages,
            "artists": self.artists
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

        if self.artists:
            query["$and"].append({"artists.id": {"$in": self.artists}})

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
