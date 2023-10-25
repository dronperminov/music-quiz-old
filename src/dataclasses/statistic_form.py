from dataclasses import dataclass

from fastapi import Body


@dataclass
class StatisticForm:
    question_type: str = Body(..., embed=True)
    link: str = Body(..., embed=True)
    correct: bool = Body(..., embed=True)

    def to_dict(self) -> dict:
        return {
            "question_type": self.question_type,
            "link": self.link,
            "correct": self.correct
        }
