from typing import Optional

from fastapi import APIRouter, Depends
from fastapi.responses import HTMLResponse, RedirectResponse, Response

from src import constants
from src.api import make_error, templates
from src.database import database
from src.dataclasses.settings import Settings
from src.utils.auth import get_current_user
from src.utils.question import get_question_params, make_question

router = APIRouter()


@router.get("/question")
def get_question(user: Optional[dict] = Depends(get_current_user)) -> Response:
    if not user:
        return RedirectResponse(url="/login")

    settings = Settings.from_dict(user["settings"])

    if database.audios.count_documents(settings.to_query()) == 0:
        error = 'Не удалось сгенерировать вопрос, так как нет подходящих под настройки аудиозаписей. Измените <a href="/settings">настройки</a> и попробуйте снова.'
        return make_error(error, user, title="Не удалось сгенерировать вопрос")

    question_type, audio = get_question_params(settings, user["username"])
    question = make_question(audio, question_type)

    template = templates.get_template("question.html")
    content = template.render(user=user, page="question", version=constants.VERSION, audio=audio, question=question)
    return HTMLResponse(content=content)
