from dataclasses import dataclass, field
from datetime import datetime
from typing import List

from src import constants


@dataclass
class Settings:
    theme: str = "light"
    questions: List[str] = field(default_factory=lambda: constants.QUESTIONS)
    start_year: int = 1900
    end_year: int = datetime.today().year

    @classmethod
    def from_dict(cls: "Settings", data: dict) -> "Settings":
        theme = data.get("theme", "light")
        questions = data.get("questions", constants.QUESTIONS)
        start_year = data.get("start_year", 1900)
        end_year = data.get("end_year", datetime.today().year)
        return cls(theme, questions, start_year, end_year)

    def to_dict(self) -> dict:
        return {
            "theme": self.theme,
            "questions": self.questions,
            "start_year": self.start_year,
            "end_year": self.end_year
        }

    def to_query(self) -> dict:
        query = {
            "year": {"$gte": self.start_year, "$lte": self.end_year}
        }

        return query
