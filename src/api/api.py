import random
from typing import Optional

from fastapi import APIRouter, Depends
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse, Response

from src import constants
from src.api import templates
from src.database import database
from src.dataclasses.settings import Settings
from src.utils.auth import get_current_user
from src.utils.statistic import get_statistic

router = APIRouter()


@router.get("/")
def index(user: Optional[dict] = Depends(get_current_user)) -> HTMLResponse:
    template = templates.get_template("index.html")

    usernames = database.statistic.distinct("username")
    statistics = dict()

    for username in usernames:
        statistics[username] = get_statistic(username)
        statistics[username]["image"] = database.users.find_one({"username": username}, {"image_src": 1})["image_src"]

    usernames = sorted(usernames, key=lambda username: -statistics[username]["questions"]["correct"])[:constants.TOP_COUNT]
    content = template.render(user=user, page="index", version=constants.VERSION, statistics=statistics, usernames=usernames)
    return HTMLResponse(content=content)


@router.get("/profile")
def profile(user: Optional[dict] = Depends(get_current_user)) -> Response:
    if not user:
        return RedirectResponse(url="/login")

    # day_start = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    # day_end = day_start + datetime.timedelta(days=1, microseconds=-1)
    statistic = get_statistic(user["username"])

    template = templates.get_template("profile.html")
    content = template.render(user=user, page="profile", version=constants.VERSION, statistic=statistic)
    return HTMLResponse(content=content)


@router.post("/radio-next")
def radio_next(user: Optional[dict] = Depends(get_current_user)) -> JSONResponse:
    if not user:
        return JSONResponse({"status": "error", "message": "Пользователь не залогинен"})

    settings = Settings.from_dict(user["settings"])
    audios = list(database.audios.find(settings.to_audio_query(), {"link": 1}))
    audio = database.audios.find_one({"link": random.choice(audios)["link"]})
    artist_src = f'https://dronperminov.ru/music/artists/{audio["artists"][0]["id"]}.mp3'

    return JSONResponse({
        "status": "success",
        "link": audio["link"],
        "artists": audio["artists"],
        "track": audio["track"],
        "lyrics": audio.get("lyrics", []),
        "artist_src": artist_src
    })
