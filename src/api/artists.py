from dataclasses import dataclass
from typing import List, Optional

from fastapi import APIRouter, Body, Depends
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse, Response

from src import constants
from src.api import make_error, templates
from src.database import database
from src.utils.auth import get_current_user


@dataclass
class ArtistForm:
    artist_id: int = Body(..., embed=True)
    creation: List[str] = Body(..., embed=True)
    genres: List[str] = Body(..., embed=True)


router = APIRouter()


@router.get("/artists")
def get_artists(user: Optional[dict] = Depends(get_current_user)) -> Response:
    if not user:
        return RedirectResponse(url="/login")

    if user["role"] != "admin":
        return make_error(message="Эта страница доступна только администраторам.", user=user)

    artists = list(database.artists.find({}))
    artist2count = dict()
    for artist in artists:
        artist2count[artist["id"]] = {
            "total": database.audios.count_documents({"artists.id": artist["id"]}),
            "with_lyrics": database.audios.count_documents({"artists.id": artist["id"], "lyrics": {"$exists": True, "$ne": []}}),
        }

    artists = sorted(artists, key=lambda artist: (-artist2count[artist["id"]]["total"], artist["name"]))

    template = templates.get_template("artists/artists.html")
    content = template.render(
        user=user,
        page="artists",
        version=constants.VERSION,
        artists=artists,
        artist2count=artist2count,
        creation2rus=constants.CREATION_TO_RUS,
        genre2rus=constants.GENRE_TO_RUS
    )
    return HTMLResponse(content=content)


@router.get("/artists/{artist_id}")
def get_artist(artist_id: int, user: Optional[dict] = Depends(get_current_user)) -> Response:
    if not user:
        return RedirectResponse(url="/login")

    if user["role"] != "admin":
        return make_error(message="Эта страница доступна только администраторам.", user=user)

    artist = database.artists.find_one({"id": artist_id})
    audios = list(database.audios.find({"artists.id": artist_id}))

    template = templates.get_template("artists/artist.html")
    content = template.render(
        user=user,
        page="artist",
        version=constants.VERSION,
        artist=artist,
        audios=audios,
        creation2rus=constants.CREATION_TO_RUS,
        genre2rus=constants.GENRE_TO_RUS
    )
    return HTMLResponse(content=content)


@router.post("/edit-artist")
def edit_artist(user: Optional[dict] = Depends(get_current_user), artist_params: ArtistForm = Depends()) -> JSONResponse:
    if not user:
        return JSONResponse({"status": "error", "message": "Пользователь не залогинен"})

    if user["role"] != "admin":
        return JSONResponse({"status": "error", "message": "Пользователь не является администратором"})

    database.artists.update_one({"id": artist_params.artist_id}, {"$set": {"creation": artist_params.creation, "genres": artist_params.genres}})
    return JSONResponse({"status": "success"})
