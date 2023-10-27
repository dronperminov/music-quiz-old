from typing import Optional

from fastapi import APIRouter, Body, Depends
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse, Response

from src import constants
from src.api import make_error, templates
from src.database import database
from src.dataclasses.artist_form import ArtistForm
from src.dataclasses.artists_query import ArtistsQuery
from src.utils.artists import get_artists_info, search_to_query
from src.utils.auth import get_current_user
from src.utils.common import get_word_form

router = APIRouter()


@router.get("/artists")
def get_artists(user: Optional[dict] = Depends(get_current_user), search_params: ArtistsQuery = Depends()) -> Response:
    if not user:
        return RedirectResponse(url="/login")

    if search_params.query == "" and search_params.genres is None and search_params.creation is None:
        return RedirectResponse(url="/artists")

    query = search_to_query(search_params)
    artists = list(database.artists.find(query)) if query else []
    artist2count = get_artists_info(artists)
    artists = sorted(artists, key=lambda artist: (-artist2count[artist["id"]]["total"], artist["name"]))

    total_artists = database.artists.count_documents({})
    query_correspond_form = get_word_form(len(artists), ["запросу соответствуют", "запросу соответствуют", "запросу соответствует"])
    query_artists_form = get_word_form(len(artists), ["исполнителей", "исполнителя", "исполнитель"])
    total_correspond_form = get_word_form(len(total_artists), ["находятся", "находятся", "находится"])
    total_artists_form = get_word_form(total_artists, ["исполнителей", "исполнителя", "исполнитель"])

    template = templates.get_template("artists/artists.html")
    content = template.render(
        user=user,
        page="artists",
        version=constants.VERSION,
        artists=artists,
        total_artists=f"{total_correspond_form} {total_artists} {total_artists_form}",
        query_artists=f"{query_correspond_form} {len(artists)} {query_artists_form}",
        genres=constants.GENRES,
        query=search_params.query if search_params.query else "",
        search_genres=search_params.genres if search_params.genres else [],
        search_creation=search_params.creation if search_params.creation else [],
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
        genres=constants.GENRES,
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


@router.post("/artist-to-questions")
def artist_to_questions(user: Optional[dict] = Depends(get_current_user), artist_id: int = Body(..., embed=True)) -> JSONResponse:
    if not user:
        return JSONResponse({"status": "error", "message": "Пользователь не залогинен"})

    artists = user["settings"].get("artists", [])
    if artist_id in artists:
        artists = [artist for artist in artists if artist != artist_id]
    else:
        artists.append(artist_id)

    database.users.update_one({"username": user["username"]}, {"$set": {"settings.artists": artists}})
    return JSONResponse({"status": "success", "include": artist_id in artists})
