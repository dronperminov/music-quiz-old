from dataclasses import dataclass
from datetime import datetime
from typing import List

from src import constants


@dataclass
class Settings:
    theme: str
    start_year: int
    end_year: int
    questions: List[str]
    question_artists: List[str]

    @classmethod
    def from_dict(cls: "Settings", data: dict) -> "Settings":
        theme = data.get("theme", "light")
        start_year = data.get("start_year", 1900)
        end_year = data.get("end_year", datetime.today().year)
        questions = data.get("questions", constants.QUESTIONS)
        question_artists = data.get("question_artists", constants.QUESTION_ARTISTS)
        return cls(theme, start_year, end_year, questions, question_artists)

    def to_dict(self) -> dict:
        return {
            "theme": self.theme,
            "start_year": self.start_year,
            "end_year": self.end_year,
            "questions": self.questions,
            "question_artists": self.question_artists,
        }

    def to_query(self) -> dict:
        query = {
            "year": {"$gte": self.start_year, "$lte": self.end_year}
        }

        if self.question_artists == [constants.QUESTION_ARTISTS_SOLE]:
            query["artists"] = {"$size": 1}
        elif self.question_artists == [constants.QUESTION_ARTISTS_FEATS]:
            query["artists.1"] = {"$exists": True}

        return query
