from dataclasses import dataclass
from typing import List

from fastapi import Body


@dataclass
class AudioForm:
    link: str = Body(..., embed=True)
    artists: List[dict] = Body(..., embed=True)
    track: str = Body(..., embed=True)
    year: int = Body(..., embed=True)
    lyrics: List[dict] = Body(..., embed=True)
