from dataclasses import dataclass
from typing import List, Optional

from fastapi import Query

from src.utils.common import escape_query


@dataclass
class AudiosQuery:
    query: Optional[str] = Query(None)
    start_year: Optional[int] = Query(None)
    end_year: Optional[int] = Query(None)
    creation: Optional[List[str]] = Query(None)
    lyrics: Optional[bool] = Query(None)

    def is_empty(self) -> bool:
        return self.query == "" and self.start_year is None and self.end_year is None and self.creation is None and self.lyrics is None

    def to_query(self) -> Optional[dict]:
        if self.query is None and self.start_year is None and self.end_year and self.creation is None and self.lyrics is None:
            return None

        query = dict()

        if self.query:
            query["track"] = {"$regex": escape_query(self.query), "$options": "i"}

        and_conditions = []
        if self.start_year is not None:
            and_conditions.append({"year": {"$gte": self.start_year}})

        if self.end_year is not None:
            and_conditions.append({"year": {"$gt": 0, "$lte": self.end_year}})

        if self.creation is not None:
            and_conditions.append({"$or": [{"creation": creation if creation != "no" else []} for creation in self.creation]})

        if self.lyrics is not None:
            and_conditions.append({"lyrics.0": {"$exists": self.lyrics}})

        if and_conditions:
            query["$and"] = and_conditions

        return query
