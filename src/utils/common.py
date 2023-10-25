from datetime import datetime
from typing import List

from src import constants


def get_default_question_years() -> List[List[int]]:
    years = []

    for i, year in enumerate(constants.QUESTION_YEARS[1:]):
        years.append([constants.QUESTION_YEARS[i], year - 1])

    years.append([constants.QUESTION_YEARS[-1], datetime.now().year])
    return years
