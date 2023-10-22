import os
from typing import List, Optional

from fastapi import APIRouter, Body, Depends, Header
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse, Response

from src import constants
from src.api import make_error, templates
from src.constants import AUDIO_CHUNK_SIZE
from src.database import database
from src.utils.audio import parse_yandex_music
from src.utils.auth import get_current_user

router = APIRouter()


@router.get("/audios/{name}")
async def get_audio(name: str, range: str = Header(None)) -> Response:  # noqa
    start, end = range.replace("bytes=", "").split("-")
    start = int(start)
    end = int(end) if end else start + AUDIO_CHUNK_SIZE

    audio_path = os.path.join(os.path.dirname(__file__), "..", "..", "web", "audios", f"{name}")

    with open(audio_path, "rb") as video:
        video.seek(start)
        data = video.read(end - start)
        headers = {
            "Content-Range": f"bytes {start}-{end}/{os.path.getsize(audio_path)}",
            "Accept-Ranges": "bytes"
        }
        return Response(data, status_code=206, headers=headers, media_type="audio/mpeg")


@router.get("/audios")
def get_audios(user: Optional[dict] = Depends(get_current_user)) -> Response:
    if not user:
        return RedirectResponse(url="/login")

    if user["role"] != "admin":
        return make_error(message="Эта страница доступна только администраторам.", user=user)

    template = templates.get_template("audios/audios.html")
    content = template.render(user=user, page="audios", version=constants.VERSION)
    return HTMLResponse(content=content)


@router.get("/add-audios")
def get_add_audios(user: Optional[dict] = Depends(get_current_user)) -> Response:
    if not user:
        return RedirectResponse(url="/login")

    if user["role"] != "admin":
        return make_error(message="Эта страница доступна только администраторам.", user=user)

    template = templates.get_template("audios/add_audios.html")
    content = template.render(user=user, page="add_audios", version=constants.VERSION)
    return HTMLResponse(content=content)


@router.post("/parse-audios")
def parse_audios(user: Optional[dict] = Depends(get_current_user), code: str = Body(..., embed=True)) -> JSONResponse:
    if not user:
        return JSONResponse({"status": "error", "message": "Пользователь не залогинен"})

    if user["role"] != "admin":
        return JSONResponse({"status": "error", "message": "Пользователь не является администратором"})

    if not user.get("token", ""):
        return JSONResponse({"status": "error", "message": "Не указан токен для Яндекс.Музыки"})

    parsed_data = parse_yandex_music(code, token=user["token"])

    return JSONResponse(parsed_data)


@router.post("/add-audios")
def add_audios(user: Optional[dict] = Depends(get_current_user), audios: List[dict] = Body(..., embed=True)) -> JSONResponse:
    if not user:
        return JSONResponse({"status": "error", "message": "Пользователь не залогинен"})

    if user["role"] != "admin":
        return JSONResponse({"status": "error", "message": "Пользователь не является администратором"})

    database.audios.delete_many({"link": {"$in": [audio["link"] for audio in audios]}})
    database.audios.insert_many(audios)

    return JSONResponse({"status": "success"})
