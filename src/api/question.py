import random
from typing import Optional

from fastapi import APIRouter, Depends
from fastapi.responses import HTMLResponse, RedirectResponse, Response

from src import constants
from src.api import templates
from src.database import database
from src.dataclasses.settings import Settings
from src.utils.auth import get_current_user
from src.utils.question import get_question_type, make_question

router = APIRouter()


@router.get("/question")
def get_question(user: Optional[dict] = Depends(get_current_user)) -> Response:
    if not user:
        return RedirectResponse(url="/login")

    settings = Settings.from_dict(user["settings"])

    audios = list(database.audios.find(settings.to_query(), {"link": 1}))
    audio = database.audios.find_one({"link": random.choice(audios)["link"]})
    question_type = get_question_type(settings.questions, audio)
    question = make_question(audio, question_type)

    template = templates.get_template("question.html")
    content = template.render(
        user=user,
        page="question",
        version=constants.VERSION,
        audio=audio,
        question=question,
        question_type=question_type,
        title=constants.QUESTION_TO_TITLE[question_type]
    )

    return HTMLResponse(content=content)
