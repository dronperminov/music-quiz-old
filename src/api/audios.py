from typing import List, Optional

import requests
from fastapi import APIRouter, Body, Depends, Query
from fastapi.requests import Request
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse, Response

from src import constants
from src.api import make_error, templates
from src.database import database
from src.utils.audio import parse_audio_html
from src.utils.auth import get_current_user

router = APIRouter()


@router.get("/audio")
async def get_audio(request: Request, link: str = Query("")) -> Response:
    if await request.is_disconnected():
        return JSONResponse({})

    response = requests.get(link)
    return Response(response.content, headers={"Accept-Ranges": "bytes"}, media_type="audio/mpeg")


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
        return JSONResponse({"status": "error", "message": "пользователь не залогинен"})

    parsed_data = parse_audio_html(code)
    return JSONResponse(parsed_data)


@router.post("/add-audios")
def add_audios(user: Optional[dict] = Depends(get_current_user), audios: List[dict] = Body(..., embed=True)) -> JSONResponse:
    if not user:
        return JSONResponse({"status": "error", "message": "пользователь не залогинен"})

    database.audios.delete_many({"link": {"$in": [audio["link"] for audio in audios]}})
    database.audios.insert_many(audios)

    return JSONResponse({"status": "success"})
