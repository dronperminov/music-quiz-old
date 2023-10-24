import os
import shutil
import tempfile
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, File, Form, UploadFile
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse, Response

from src import constants
from src.api import templates
from src.database import database
from src.dataclasses.settings import Settings
from src.utils.auth import get_current_user

router = APIRouter()


@dataclass
class SettingsForm:
    fullname: str = Form(...)
    theme: str = Form(...)
    token: str = Form("")
    questions: str = Form(...)
    start_year: int = Form(...)
    end_year: int = Form(...)


def save_image(image: UploadFile, output_dir: str) -> str:
    file_name = image.filename.split("/")[-1]
    file_path = os.path.join(output_dir, file_name)

    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
    finally:
        image.file.close()

    return file_path


@router.get("/settings")
def get_settings(user: Optional[dict] = Depends(get_current_user)) -> Response:
    if not user:
        return RedirectResponse(url="/login")

    template = templates.get_template("settings.html")
    content = template.render(
        user=user,
        page="settings",
        version=constants.VERSION,
        year=datetime.now().year,
        questions=constants.QUESTIONS,
        question2rus=constants.QUESTION_TO_RUS
    )

    return HTMLResponse(content=content)


@router.post("/settings")
async def update_settings(settings_form: SettingsForm = Depends(), image: UploadFile = File(None), user: Optional[dict] = Depends(get_current_user)) -> JSONResponse:
    if not user:
        return JSONResponse({"status": "error", "message": "Пользователь не залогинен"})

    if image is not None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            file_path = save_image(image, tmp_dir)
            target_path = os.path.join("web", "images", "profiles", f'{user["username"]}.jpg')
            shutil.move(file_path, target_path)
            user["image_src"] = f'images/profiles/{user["username"]}.jpg'

    settings = Settings(settings_form.theme, settings_form.questions.split(","), settings_form.start_year, settings_form.end_year)

    if database.audios.count_documents(settings.to_query()) == 0:
        return JSONResponse({"status": "error", "message": "Для данных настроек нет ни одного трека"})

    user["fullname"] = settings_form.fullname
    user["settings"] = settings.to_dict()
    user["token"] = settings_form.token

    database.users.update_one({"username": user["username"]}, {"$set": user}, upsert=True)
    return JSONResponse({"status": "success"})
