import os
import shutil
import tempfile
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, File, UploadFile
from fastapi.requests import Request
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse, Response

from src import constants
from src.api import templates
from src.database import database
from src.dataclasses.settings import Settings
from src.utils.auth import get_current_user
from src.utils.common import get_default_question_years, get_hash, get_static_hash, get_word_form, save_image

router = APIRouter()


@router.get("/settings")
def get_settings(user: Optional[dict] = Depends(get_current_user)) -> Response:
    if not user:
        return RedirectResponse(url="/login")

    template = templates.get_template("settings.html")
    settings = Settings.from_dict(database.settings.find_one({"username": user["username"]}))
    audios_count = database.audios.count_documents(settings.to_query())

    prefer_list = {artist["id"]: artist for artist in database.artists.find({"id": {"$in": settings.prefer_list}}, {"id": 1, "name": 1})}
    ignore_list = {artist["id"]: artist for artist in database.artists.find({"id": {"$in": settings.ignore_list}}, {"id": 1, "name": 1})}

    content = template.render(
        user=user,
        settings=settings,
        page="settings",
        version=get_static_hash(),
        have_statistic=database.statistic.find_one({"username": user["username"]}) is not None,
        question_years=get_default_question_years(),
        prefer_list=prefer_list,
        ignore_list=ignore_list,
        audios_count=f'{audios_count} {get_word_form(audios_count, ["аудиозаписей", "аудиозаписи", "аудиозапись"])}',
        genres=constants.GENRES,
        genre2rus=constants.GENRE_TO_RUS,
        questions=constants.QUESTIONS,
        question2rus=constants.QUESTION_TO_RUS,
        question_artists=constants.QUESTION_ARTISTS,
        question_artists2rus=constants.QUESTION_ARTISTS_TO_RUS,
        text_languages=constants.TEXT_LANGUAGES,
        text_language2rus=constants.TEXT_LANGUAGE_TO_RUS
    )

    return HTMLResponse(content=content)


@router.post("/update-avatar")
async def update_avatar(image: UploadFile = File(...), user: Optional[dict] = Depends(get_current_user)) -> JSONResponse:
    if not user:
        return JSONResponse({"status": "error", "message": "Пользователь не залогинен"})

    with tempfile.TemporaryDirectory() as tmp_dir:
        file_path = save_image(image, tmp_dir)
        target_path = os.path.join("web", "images", "profiles", f'{user["username"]}.jpg')
        shutil.move(file_path, target_path)
        image_hash = get_hash(target_path)

    database.users.update_one({"username": user["username"]}, {"$set": {"image_src": f'/images/profiles/{user["username"]}.jpg?v={image_hash}'}}, upsert=True)
    return JSONResponse({"status": "success"})


@router.post("/update-settings")
async def update_settings(request: Request, user: Optional[dict] = Depends(get_current_user)) -> JSONResponse:
    if not user:
        return JSONResponse({"status": "error", "message": "Пользователь не залогинен"})

    data = await request.json()
    settings = Settings.from_dict(data)
    current_settings = Settings.from_dict(database.settings.find_one({"username": user["username"]}))

    if set(settings.questions) != set(current_settings.questions):
        settings.last_update = datetime.now()

    database.users.update_one({"username": user["username"]}, {"$set": {"fullname": data["fullname"]}})
    database.settings.update_one({"username": user["username"]}, {"$set": settings.to_dict()}, upsert=True)

    audios_count = database.audios.count_documents(settings.to_query())
    return JSONResponse({"status": "success", "audios_count": audios_count})
