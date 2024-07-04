from dataclasses import dataclass
from typing import List

from fastapi import Body


@dataclass
class ArtistForm:
    artist_id: int = Body(..., embed=True)
    creation: List[str] = Body(..., embed=True)
    genres: List[str] = Body(..., embed=True)
    form: str = Body(..., embed=True)

    def to_dict(self) -> dict:
        return {
            "creation": self.creation,
            "genres": self.genres,
            "form": self.form
        }
