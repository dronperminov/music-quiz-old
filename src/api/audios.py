from typing import List, Optional

from fastapi import APIRouter, Body, Depends
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse, Response

from src import constants
from src.api import make_error, templates
from src.database import database
from src.utils.audio import get_track_ids, parse_track
from src.utils.auth import get_current_user

router = APIRouter()


@router.get("/audios")
def get_audios(user: Optional[dict] = Depends(get_current_user)) -> Response:
    if not user:
        return RedirectResponse(url="/login")

    if user["role"] != "admin":
        return make_error(message="Эта страница доступна только администраторам.", user=user)

    audios_count = database.audios.count_documents({})
    lyrics_count = database.audios.count_documents({"lyrics": {"$exists": True}})

    template = templates.get_template("audios/audios.html")
    content = template.render(user=user, page="audios", version=constants.VERSION, audios_count=audios_count, lyrics_count=lyrics_count)
    return HTMLResponse(content=content)


@router.get("/artists")
def get_artists(user: Optional[dict] = Depends(get_current_user)) -> Response:
    if not user:
        return RedirectResponse(url="/login")

    if user["role"] != "admin":
        return make_error(message="Эта страница доступна только администраторам.", user=user)

    artists = list(database.artists.find({}))
    artist2count = dict()
    for artist in artists:
        artist2count[artist["id"]] = database.audios.count_documents({"artists.id": {"$in": [artist["id"]]}})
    artists = sorted(artists, key=lambda artist: (-artist2count[artist["id"]], artist["name"]))

    template = templates.get_template("audios/artists.html")
    content = template.render(user=user, page="artists", version=constants.VERSION, artists=artists, artist2count=artist2count)
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

    track_ids = get_track_ids(code, user["token"])

    if not track_ids:
        return JSONResponse({"status": "error", "message": "Не удалось распарсить ни одного аудио"})

    return JSONResponse({"status": "success", "track_ids": track_ids})


@router.post("/parse-audio")
def parse_audio(user: Optional[dict] = Depends(get_current_user), track_id: str = Body(..., embed=True)) -> JSONResponse:
    if not user:
        return JSONResponse({"status": "error", "message": "Пользователь не залогинен"})

    if user["role"] != "admin":
        return JSONResponse({"status": "error", "message": "Пользователь не является администратором"})

    if not user.get("token", ""):
        return JSONResponse({"status": "error", "message": "Не указан токен для Яндекс.Музыки"})

    track = parse_track(track_id, user["token"])
    return JSONResponse({"status": "success", "track": track})


@router.post("/add-audios")
def add_audios(user: Optional[dict] = Depends(get_current_user), audios: List[dict] = Body(..., embed=True)) -> JSONResponse:
    if not user:
        return JSONResponse({"status": "error", "message": "Пользователь не залогинен"})

    if user["role"] != "admin":
        return JSONResponse({"status": "error", "message": "Пользователь не является администратором"})

    # TODO: make more optimal
    existed_artists = {artist["id"] for artist in database.artists.find({}, {"id": 1})}
    new_artists = {artist["id"]: artist for audio in audios for artist in audio["artists"] if artist["id"] not in existed_artists}

    if new_artists:
        database.artists.insert_many(new_artists.values())

    database.audios.delete_many({"link": {"$in": [audio["link"] for audio in audios]}})
    database.audios.insert_many(audios)

    return JSONResponse({"status": "success"})
