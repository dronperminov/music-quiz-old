from typing import Optional

from fastapi import APIRouter, Depends
from fastapi.responses import HTMLResponse, RedirectResponse, Response

from src.api import make_error, templates
from src.database import database
from src.dataclasses.settings import Settings
from src.utils.auth import get_current_user
from src.utils.common import get_static_hash
from src.utils.question import get_question_and_audio, get_question_params, make_question

router = APIRouter()


@router.get("/question")
def get_question(user: Optional[dict] = Depends(get_current_user)) -> Response:
    if not user:
        return RedirectResponse(url="/login?back_url=/question")

    settings = Settings.from_dict(database.settings.find_one({"username": user["username"]}))

    if database.audios.count_documents(settings.to_query()) == 0:
        error = 'Не удалось сгенерировать вопрос, так как нет подходящих под настройки аудиозаписей. Измените <a href="/settings">настройки</a> и попробуйте снова.'
        return make_error(error, user, title="Не удалось сгенерировать вопрос")

    question, audio = get_question_and_audio(user["username"], settings)

    if not question:
        question_type, audio = get_question_params(settings, user["username"])
        question = make_question(audio, question_type, settings.change_playback_rate)
        database.questions.delete_one({"username": user["username"]})
        database.questions.insert_one({"username": user["username"], **question})

    if audio:
        artists = database.artists.find({"id": {"$in": [artist["id"] for artist in audio["artists"]]}})
        artist2cover = {artist["id"]: artist.get("cover", "") for artist in artists}
        for artist in audio["artists"]:
            artist["cover"] = artist2cover[artist["id"]]

    template = templates.get_template("question.html")
    content = template.render(user=user, settings=settings, page="question", version=get_static_hash(), audio=audio, question=question)
    return HTMLResponse(content=content)
