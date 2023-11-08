from dataclasses import dataclass
from typing import List

from fastapi import Body


@dataclass
class AudioForm:
    track_id: str = Body(..., embed=True)
    artists: List[dict] = Body(..., embed=True)
    track: str = Body(..., embed=True)
    lyrics: List[dict] = Body(..., embed=True)
    year: int = Body(..., embed=True)
    creation: List[str] = Body(..., embed=True)

    def to_dict(self) -> dict:
        return {
            "artists": self.artists,
            "track": self.track,
            "lyrics": self.lyrics,
            "year": self.year,
            "creation": self.creation
        }
