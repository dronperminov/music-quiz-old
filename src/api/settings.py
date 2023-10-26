import hashlib
import os
import shutil
import tempfile
from typing import Optional

from fastapi import APIRouter, Depends, File, UploadFile
from fastapi.requests import Request
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse, Response

from src import constants
from src.api import templates
from src.database import database
from src.dataclasses.settings import Settings
from src.utils.auth import get_current_user
from src.utils.common import get_default_question_years, get_word_form

router = APIRouter()


def save_image(image: UploadFile, output_dir: str) -> str:
    file_name = image.filename.split("/")[-1]
    file_path = os.path.join(output_dir, file_name)

    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
    finally:
        image.file.close()

    return file_path


def get_hash(filename: str) -> str:
    hash_md5 = hashlib.md5()

    with open(filename, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)

    return hash_md5.hexdigest()


@router.get("/settings")
def get_settings(user: Optional[dict] = Depends(get_current_user)) -> Response:
    if not user:
        return RedirectResponse(url="/login")

    template = templates.get_template("settings.html")
    settings = Settings.from_dict(user["settings"])
    audios_count = database.audios.count_documents(settings.to_query())

    artists = {artist["id"]: artist for artist in database.artists.find({"id": {"$in": user["settings"].get("artists", [])}}, {"id": 1, "name": 1})}
    content = template.render(
        user=user,
        page="settings",
        version=constants.VERSION,
        have_statistic=database.statistic.find_one({"username": user["username"]}) is not None,
        question_years=get_default_question_years(),
        artists=artists,
        audios_count=f'{audios_count} {get_word_form(audios_count, ["аудиозаписей", "аудиозаписи", "аудиозапись"])}',
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

    database.users.update_one({"username": user["username"]}, {"$set": {"image_src": f'images/profiles/{user["username"]}.jpg?v={image_hash}'}}, upsert=True)
    return JSONResponse({"status": "success"})


@router.post("/update-settings")
async def update_settings(request: Request, user: Optional[dict] = Depends(get_current_user)) -> JSONResponse:
    if not user:
        return JSONResponse({"status": "error", "message": "Пользователь не залогинен"})

    data = await request.json()
    settings = Settings.from_dict(data)
    audios_count = database.audios.count_documents(settings.to_query())

    if audios_count == 0:
        return JSONResponse({"status": "error", "message": "Для выбранных настроек нет ни одного трека"})

    user["fullname"] = data["fullname"]
    user["settings"] = settings.to_dict()

    database.users.update_one({"username": user["username"]}, {"$set": user}, upsert=True)
    return JSONResponse({"status": "success", "audios_count": audios_count})
