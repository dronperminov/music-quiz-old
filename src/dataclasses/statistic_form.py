from dataclasses import dataclass

from fastapi import Body


@dataclass
class StatisticForm:
    question_type: str = Body(..., embed=True)
    track_id: str = Body(..., embed=True)
    correct: bool = Body(..., embed=True)

    def to_dict(self) -> dict:
        return {
            "question_type": self.question_type,
            "track_id": self.track_id,
            "correct": self.correct
        }
