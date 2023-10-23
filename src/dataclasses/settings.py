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
