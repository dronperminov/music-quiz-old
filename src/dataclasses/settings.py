from dataclasses import dataclass, field
from datetime import datetime
from typing import List

from src import constants


@dataclass
class Settings:
    theme: str = "light"
    question_types: List[str] = field(default_factory=lambda: constants.QUESTIONS)
    start_year: int = 1900
    end_year: int = datetime.now().year

    def to_dict(self) -> dict:
        return {
            "theme": self.theme,
            "question_types": self.question_types,
            "start_year": self.start_year,
            "end_year": self.end_year
        }

    def to_query(self) -> dict:
        query = {
            "year": {"$gte": self.start_year, "$lte": self.end_year}
        }

        return query
