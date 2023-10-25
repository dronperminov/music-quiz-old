import random
from dataclasses import dataclass
from typing import List, Optional

import yandex_music.exceptions
from fastapi import APIRouter, Body, Depends
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse, Response

from src import constants
from src.api import make_error, templates, tokens
from src.database import database
from src.utils.artists import get_artists_creation
from src.utils.audio import get_track_ids, parse_artist_genres, parse_direct_link, parse_track
from src.utils.auth import get_current_user


@dataclass
class AudioForm:
    link: str = Body(..., embed=True)
    artists: List[dict] = Body(..., embed=True)
    track: str = Body(..., embed=True)
    year: int = Body(..., embed=True)
    lyrics: List[dict] = Body(..., embed=True)


router = APIRouter()


@router.get("/audios")
def get_audios(user: Optional[dict] = Depends(get_current_user)) -> Response:
    if not user:
        return RedirectResponse(url="/login")

    if user["role"] != "admin":
        return make_error(message="Эта страница доступна только администраторам.", user=user)

    audios_count = database.audios.count_documents({})
    lyrics_count = database.audios.count_documents({"lyrics": {"$exists": True, "$ne": []}})

    template = templates.get_template("audios/audios.html")
    content = template.render(user=user, page="audios", version=constants.VERSION, audios_count=audios_count, lyrics_count=lyrics_count)
    return HTMLResponse(content=content)


@router.get("/audios/{link}")
def get_audio(link: str, user: Optional[dict] = Depends(get_current_user)) -> Response:
    if not user:
        return RedirectResponse(url="/login")

    if user["role"] != "admin":
        return make_error(message="Эта страница доступна только администраторам.", user=user)

    audio = database.audios.find_one({"link": link})

    if not audio:
        return make_error(message="Запрашиваемого аудио не существует", user=user)

    template = templates.get_template("audios/audio.html")
    content = template.render(user=user, page="audio", version=constants.VERSION, audio=audio)
    return HTMLResponse(content=content)


@router.get("/add-audios")
def get_add_audios(user: Optional[dict] = Depends(get_current_user)) -> Response:
    if not user:
        return RedirectResponse(url="/login")

    if user["role"] != "admin":
        return make_error(message="Эта страница доступна только администраторам.", user=user)

    template = templates.get_template("audios/add_audios.html")
    content = template.render(user=user, page="add-audios", version=constants.VERSION)
    return HTMLResponse(content=content)


@router.post("/parse-audios")
def parse_audios(user: Optional[dict] = Depends(get_current_user), code: str = Body(..., embed=True), ignore_existing: bool = Body(..., embed=True)) -> JSONResponse:
    if not user:
        return JSONResponse({"status": "error", "message": "Пользователь не залогинен"})

    if user["role"] != "admin":
        return JSONResponse({"status": "error", "message": "Пользователь не является администратором"})

    track_ids = get_track_ids(code, random.choice(tokens))

    if not track_ids:
        return JSONResponse({"status": "error", "message": "Не удалось распарсить ни одного аудио"})

    if ignore_existing:
        existed_track_ids = {audio["link"] for audio in database.audios.find({}, {"link": 1})}
        track_ids = [track_id for track_id in track_ids if track_id not in existed_track_ids]

    return JSONResponse({"status": "success", "track_ids": track_ids})


@router.post("/parse-audio")
def parse_audio(user: Optional[dict] = Depends(get_current_user), track_id: str = Body(..., embed=True), make_link: bool = Body(..., embed=True)) -> JSONResponse:
    if not user:
        return JSONResponse({"status": "error", "message": "Пользователь не залогинен"})

    if user["role"] != "admin":
        return JSONResponse({"status": "error", "message": "Пользователь не является администратором"})

    track = parse_track(track_id, random.choice(tokens), make_link)
    return JSONResponse({"status": "success", "track": track})


def add_artists(new_artists: dict, token: str) -> None:
    artist_ids = [artist_id for artist_id in new_artists]
    artist_genres = parse_artist_genres(artist_ids, token)
    artist_creation = get_artists_creation(artist_ids)

    for artist_id, artist in new_artists.items():
        artist["genres"] = artist_genres[artist_id]
        artist["creation"] = list(artist_creation[artist_id])

    database.artists.insert_many(new_artists.values())


@router.post("/add-audios")
def add_audios(user: Optional[dict] = Depends(get_current_user), audios: List[dict] = Body(..., embed=True)) -> JSONResponse:
    if not user:
        return JSONResponse({"status": "error", "message": "Пользователь не залогинен"})

    if user["role"] != "admin":
        return JSONResponse({"status": "error", "message": "Пользователь не является администратором"})

    database.audios.delete_many({"link": {"$in": [audio["link"] for audio in audios]}})
    database.audios.insert_many(audios)

    existed_artists = {artist["id"] for artist in database.artists.find({}, {"id": 1})}
    new_artists = {artist["id"]: artist for audio in audios for artist in audio["artists"] if artist["id"] not in existed_artists}

    if new_artists:
        add_artists(new_artists, random.choice(tokens))

    return JSONResponse({"status": "success"})


@router.post("/get-direct-link")
def get_direct_link(user: Optional[dict] = Depends(get_current_user), track_id: str = Body(..., embed=True)) -> JSONResponse:
    if not user:
        return JSONResponse({"status": "error", "message": "Пользователь не залогинен"})

    try:
        direct_link = parse_direct_link(track_id, random.choice(tokens))
    except yandex_music.exceptions.BadRequestError:
        return JSONResponse({"status": "error", "message": "Не удалось получить ссылку на аудио"})

    return JSONResponse({"status": "success", "direct_link": direct_link})


@router.post("/update-audio")
def update_audio(user: Optional[dict] = Depends(get_current_user), params: AudioForm = Depends()) -> JSONResponse:
    if not user:
        return JSONResponse({"status": "error", "message": "Пользователь не залогинен"})

    if user["role"] != "admin":
        return JSONResponse({"status": "error", "message": "Пользователь не является администратором"})

    audio = database.audios.find_one({"link": params.link})

    if not audio:
        return JSONResponse({"status": "error", "message": "Указанная аудиозапись не найдена. Возможно, она была удалена"})

    database.audios.update_one({"link": params.link}, {
        "$set": {
            "artists": params.artists,
            "track": params.track,
            "lyrics": params.lyrics,
            "year": params.year
        }
    }, upsert=True)

    return JSONResponse({"status": "success"})


@router.post("/remove-audio")
def remove_audio(user: Optional[dict] = Depends(get_current_user), link: str = Body(..., embed=True)) -> JSONResponse:
    if not user:
        return JSONResponse({"status": "error", "message": "Пользователь не залогинен"})

    if user["role"] != "admin":
        return JSONResponse({"status": "error", "message": "Пользователь не является администратором"})

    audio = database.audios.find_one({"link": link})

    if not audio:
        return JSONResponse({"status": "error", "message": "Указанная аудиозапись не найдена. Возможно, она уже была удалена"})

    database.audios.delete_one({"link": link})
    return JSONResponse({"status": "success"})
