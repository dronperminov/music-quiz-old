from dataclasses import dataclass
from typing import List, Optional

from fastapi import Query


@dataclass
class ArtistsQuery:
    query: Optional[str] = Query(None)
    genres: Optional[List[str]] = Query(None)
    creation: Optional[List[str]] = Query(None)
