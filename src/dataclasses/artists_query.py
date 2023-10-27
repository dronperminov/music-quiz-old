from dataclasses import dataclass
from typing import List, Optional

from fastapi import Query

from src.utils.common import escape_query


@dataclass
class ArtistsQuery:
    query: Optional[str] = Query(None)
    genres: Optional[List[str]] = Query(None)
    creation: Optional[List[str]] = Query(None)

    def is_empty(self) -> bool:
        return self.query == "" and self.genres is None and self.creation is None

    def to_query(self) -> Optional[dict]:
        if self.query is None and self.genres is None and self.creation is None:
            return None

        query = dict()

        if self.query:
            query["name"] = {"$regex": escape_query(self.query), "$options": "i"}

        and_conditions = []
        if self.genres is not None:
            and_conditions.append({"$or": [{"genres": genre if genre != "no" else []} for genre in self.genres]})

        if self.creation is not None:
            and_conditions.append({"$or": [{"creation": creation if creation != "no" else []} for creation in self.creation]})

        if and_conditions:
            query["$and"] = and_conditions

        return query
