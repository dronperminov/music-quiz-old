import random
from collections import defaultdict
from dataclasses import dataclass
from typing import List, Set

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

    def to_query(self) -> dict:
        artist_ids = [artist["id"] for artist in database.artists.find({"genres": {"$in": self.genres}}, {"id": 1})]

        query = {
            "$and": [
                {"$or": [{"year": {"$gte": start_year, "$lte": end_year}} for start_year, end_year in self.question_years]},
                {"$or": [self.__question_to_query(question_type) for question_type in self.questions]},
                {"artists.id": {"$in": artist_ids}},
                {"creation": {"$in": self.text_languages}},
                self.__question_artists_to_query()
            ]
        }

        if self.artists:
            query["$and"].append({"artists.id": {"$in": self.artists}})

        return query

    def get_question_type(self, username: str, audio: dict) -> str:
        available_question_types = self.__audio_to_question_types(audio)
        question_types = list(set(self.questions).intersection(available_question_types))

        if len(question_types) == 1:
            return question_types[0]

        if statistics := database.statistic.find({"username": username, "question_type": {"$in": question_types}}, {"question_type": 1}).sort("datetime", -1).limit(100):
            question2count = defaultdict(int)

            for record in statistics:
                question2count[record["question_type"]] += 1

            weights = [1 / (question2count[question_type] + 1) for question_type in question_types]
            return random.choices(question_types, k=1, weights=weights)[0]

        return random.choice(question_types)

    def __question_to_query(self, question_type: str) -> dict:
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

    def __audio_to_question_types(self, audio: dict) -> Set[str]:
        question_types = set()

        if len(audio["artists"]) == 1 and constants.QUESTION_ARTISTS_SOLE in self.question_artists:
            question_types.add(constants.QUESTION_ARTIST_BY_TRACK)
            question_types.add(constants.QUESTION_NAME_BY_TRACK)

        if len(audio["artists"]) > 1 and constants.QUESTION_ARTISTS_FEATS in self.question_artists:
            question_types.add(constants.QUESTION_ARTIST_BY_TRACK)
            question_types.add(constants.QUESTION_NAME_BY_TRACK)

        if audio.get("lyrics", []):
            if "russian" in audio.get("creation", []):
                question_types.add(constants.QUESTION_LINE_BY_TEXT)

                if audio["chorus"]:
                    question_types.add(constants.QUESTION_LINE_BY_CHORUS)

            if audio["lyrics"][0]["time"] >= constants.INTRODUCTION_TIME:
                question_types.add(constants.QUESTION_ARTIST_BY_INTRO)

        return question_types
